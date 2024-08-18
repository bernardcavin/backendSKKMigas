from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, extract, and_, cast, Integer
from sqlalchemy.orm import Session
from typing import Dict
from backend.routers.job.models import Job,Drilling,DrillingClass,JobType,WOWS,WOWSClass
from backend.routers.auth.models import Role
from backend.routers.auth.schemas import GetUser
from calendar import monthrange, month_name as calendar_month_name
from datetime import datetime,timedelta
import plotly.graph_objects as go
import numpy as np

from backend.routers.auth.utils import authorize, get_db, get_current_user
from backend.routers.job import crud, schemas, models

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

@router.post("/count-jobs-month")
@authorize(role=[Role.KKKS, Role.Admin])
async def count_jobs(db: Session = Depends(get_db), user: GetUser = Depends(get_current_user)):
    current_date = datetime.now()
    current_year = current_date.year
    current_month = current_date.month

    # Fungsi untuk menghitung job berdasarkan tipe, kelas, dan bulan
    def get_monthly_count(job_type, job_class, year, month):
        query = db.query(func.count(Job.id)).filter(
            extract('year', Job.plan_start) == year,
            extract('month', Job.plan_start) == month
        )
        if job_type == JobType.DRILLING:
            query = query.filter(Job.job_type == JobType.DRILLING, Drilling.drilling_class == job_class)
        elif job_type == JobType.WOWS:
            query = query.filter(Job.job_type == JobType.WOWS, WOWS.wows_class == job_class)
        return query.scalar()

    # Menghitung total untuk setiap jenis pekerjaan
    total_exploration = db.query(func.count(Job.id)).filter(Job.job_type == JobType.DRILLING, Drilling.drilling_class == DrillingClass.EXPLORATION).scalar()
    total_development = db.query(func.count(Job.id)).filter(Job.job_type == JobType.DRILLING, Drilling.drilling_class == DrillingClass.DEVELOPMENT).scalar()
    total_work_over = db.query(func.count(Job.id)).filter(Job.job_type == JobType.WOWS, WOWS.wows_class == WOWSClass.WORKOVER).scalar()
    total_well_service = db.query(func.count(Job.id)).filter(Job.job_type == JobType.WOWS, WOWS.wows_class == WOWSClass.WELLSERVICE).scalar()

    # Menghitung pekerjaan bulan ini
    current_month_exploration = get_monthly_count(JobType.DRILLING, DrillingClass.EXPLORATION, current_year, current_month)
    current_month_development = get_monthly_count(JobType.DRILLING, DrillingClass.DEVELOPMENT, current_year, current_month)
    current_month_work_over = get_monthly_count(JobType.WOWS, WOWSClass.WORKOVER, current_year, current_month)
    current_month_well_service = get_monthly_count(JobType.WOWS, WOWSClass.WELLSERVICE, current_year, current_month)

    # Menghitung pekerjaan per bulan untuk semua jenis
    monthly_breakdown = db.query(
        extract('year', Job.plan_start).label('year'),
        extract('month', Job.plan_start).label('month'),
        Job.job_type,
        func.count(Job.id).label('count')
    ).group_by(
        extract('year', Job.plan_start),
        extract('month', Job.plan_start),
        Job.job_type
    ).order_by(
        extract('year', Job.plan_start),
        extract('month', Job.plan_start),
        Job.job_type
    ).all()

    # Mengubah hasil query menjadi format yang lebih mudah dibaca
    monthly_data: Dict[str, Dict[str, int]] = {}
    for year, month, job_type, count in monthly_breakdown:
        key = f"{year}-{month:02d}"
        if key not in monthly_data:
            monthly_data[key] = {'DRILLING': 0, 'WOWS': 0}
        monthly_data[key][job_type.name] = count

    return {
        'TOTAL': {
            'DRILLING': {
                'EXPLORATION': total_exploration,
                'DEVELOPMENT': total_development
            },
            'WOWS': {
                'WORKOVER': total_work_over,
                'WELLSERVICE': total_well_service
            }
        },
        'CURRENT_MONTH': {
            'DRILLING': {
                'EXPLORATION': current_month_exploration,
                'DEVELOPMENT': current_month_development
            },
            'WOWS': {
                'WORKOVER': current_month_work_over,
                'WELLSERVICE': current_month_well_service
            }
        },
        'MONTHLY_BREAKDOWN': monthly_data
    }
    
@router.post("/count-jobs-weeks")
@authorize(role=[Role.KKKS, Role.Admin])
async def count_jobs(db: Session = Depends(get_db), user: GetUser = Depends(get_current_user)):
    current_date = datetime.now()
    current_year = current_date.year
    current_month = current_date.month
    current_week = (current_date.day - 1) // 7 + 1  # Calculate week of the month (1-5)

    def get_month_name(month_number):
        return calendar_month_name[month_number]

    def get_week_dates(year, month, week):
        first_day = datetime(year, month, 1)
        week_start = first_day + timedelta(days=(week-1)*7)
        week_end = min(week_start + timedelta(days=6), datetime(year, month, monthrange(year, month)[1]))
        return week_start, week_end

    def get_weekly_count(job_type, job_class, year, month, week):
        week_start, week_end = get_week_dates(year, month, week)
        query = db.query(func.count(Job.id)).filter(
            and_(
                Job.plan_start >= week_start,
                Job.plan_start <= week_end
            )
        )
        if job_type == JobType.DRILLING:
            query = query.filter(Job.job_type == JobType.DRILLING, Drilling.drilling_class == job_class)
        elif job_type == JobType.WOWS:
            query = query.filter(Job.job_type == JobType.WOWS, WOWS.wows_class == job_class)
        return query.scalar()

    # Menghitung total untuk setiap jenis pekerjaan
    total_exploration = db.query(func.count(Job.id)).filter(Job.job_type == JobType.DRILLING, Drilling.drilling_class == DrillingClass.EXPLORATION).scalar()
    total_development = db.query(func.count(Job.id)).filter(Job.job_type == JobType.DRILLING, Drilling.drilling_class == DrillingClass.DEVELOPMENT).scalar()
    total_work_over = db.query(func.count(Job.id)).filter(Job.job_type == JobType.WOWS, WOWS.wows_class == WOWSClass.WORKOVER).scalar()
    total_well_service = db.query(func.count(Job.id)).filter(Job.job_type == JobType.WOWS, WOWS.wows_class == WOWSClass.WELLSERVICE).scalar()

    # Menghitung pekerjaan minggu ini
    current_week_exploration = get_weekly_count(JobType.DRILLING, DrillingClass.EXPLORATION, current_year, current_month, current_week)
    current_week_development = get_weekly_count(JobType.DRILLING, DrillingClass.DEVELOPMENT, current_year, current_month, current_week)
    current_week_work_over = get_weekly_count(JobType.WOWS, WOWSClass.WORKOVER, current_year, current_month, current_week)
    current_week_well_service = get_weekly_count(JobType.WOWS, WOWSClass.WELLSERVICE, current_year, current_month, current_week)

    # Menghitung pekerjaan per minggu untuk semua jenis
    weekly_breakdown = db.query(
        cast(func.strftime('%Y', Job.plan_start), Integer).label('year'),
        cast(func.strftime('%m', Job.plan_start), Integer).label('month'),
        (cast(func.strftime('%d', Job.plan_start), Integer) - 1) / 7 + 1,
        Job.job_type,
        func.count(Job.id).label('count')
    ).group_by(
        func.strftime('%Y', Job.plan_start),
        func.strftime('%m', Job.plan_start),
        (cast(func.strftime('%d', Job.plan_start), Integer) - 1) / 7 + 1,
        Job.job_type
    ).order_by(
        func.strftime('%Y', Job.plan_start),
        func.strftime('%m', Job.plan_start),
        (cast(func.strftime('%d', Job.plan_start), Integer) - 1) / 7 + 1,
        Job.job_type
    ).all()

    # Mengubah hasil query menjadi format yang lebih mudah dibaca
    weekly_data: Dict[str, Dict[str, Dict[str, int]]] = {}
    for year, month, week, job_type, count in weekly_breakdown:
        month_name = get_month_name(month)
        month_key = f"{year} {month_name}"
        week_key = f"W{int(week)}"
        if month_key not in weekly_data:
            weekly_data[month_key] = {}
        if week_key not in weekly_data[month_key]:
            weekly_data[month_key][week_key] = {'DRILLING': 0, 'WOWS': 0}
        weekly_data[month_key][week_key][job_type.name] = count

    return {
        'TOTAL': {
            'DRILLING': {
                'EXPLORATION': total_exploration,
                'DEVELOPMENT': total_development
            },
            'WOWS': {
                'WORKOVER': total_work_over,
                'WELLSERVICE': total_well_service
            }
        },
        'CURRENT_WEEK': {
            'DRILLING': {
                'EXPLORATION': current_week_exploration,
                'DEVELOPMENT': current_week_development
            },
            'WOWS': {
                'WORKOVER': current_week_work_over,
                'WELLSERVICE': current_week_well_service
            }
        },
        'WEEKLY_BREAKDOWN': weekly_data
    }
    
@router.post("/count-jobs-days")
@authorize(role=[Role.KKKS, Role.Admin])
async def count_jobs(db: Session = Depends(get_db), user: GetUser = Depends(get_current_user)):
    current_date = datetime.now()
    current_year = current_date.year
    current_month = current_date.month
    current_day = current_date.day

    def get_month_name(month_number):
        return calendar_month_name[month_number]

    def get_daily_count(job_type, job_class, year, month, day):
        start_date = datetime(year, month, day)
        end_date = start_date + timedelta(days=1)
        query = db.query(func.count(Job.id)).filter(
            and_(
                Job.plan_start >= start_date,
                Job.plan_start < end_date
            )
        )
        if job_type == JobType.DRILLING:
            query = query.filter(Job.job_type == JobType.DRILLING, Drilling.drilling_class == job_class)
        elif job_type == JobType.WOWS:
            query = query.filter(Job.job_type == JobType.WOWS, WOWS.wows_class == job_class)
        return query.scalar()

    # Menghitung total untuk setiap jenis pekerjaan
    total_exploration = db.query(func.count(Job.id)).filter(Job.job_type == JobType.DRILLING, Drilling.drilling_class == DrillingClass.EXPLORATION).scalar()
    total_development = db.query(func.count(Job.id)).filter(Job.job_type == JobType.DRILLING, Drilling.drilling_class == DrillingClass.DEVELOPMENT).scalar()
    total_work_over = db.query(func.count(Job.id)).filter(Job.job_type == JobType.WOWS, WOWS.wows_class == WOWSClass.WORKOVER).scalar()
    total_well_service = db.query(func.count(Job.id)).filter(Job.job_type == JobType.WOWS, WOWS.wows_class == WOWSClass.WELLSERVICE).scalar()

    # Menghitung pekerjaan hari ini
    current_day_exploration = get_daily_count(JobType.DRILLING, DrillingClass.EXPLORATION, current_year, current_month, current_day)
    current_day_development = get_daily_count(JobType.DRILLING, DrillingClass.DEVELOPMENT, current_year, current_month, current_day)
    current_day_work_over = get_daily_count(JobType.WOWS, WOWSClass.WORKOVER, current_year, current_month, current_day)
    current_day_well_service = get_daily_count(JobType.WOWS, WOWSClass.WELLSERVICE, current_year, current_month, current_day)

    # Menghitung pekerjaan per hari untuk semua jenis
    daily_breakdown = db.query(
        cast(func.strftime('%Y', Job.plan_start), Integer).label('year'),
        cast(func.strftime('%m', Job.plan_start), Integer).label('month'),
        cast(func.strftime('%d', Job.plan_start), Integer).label('day'),
        Job.job_type,
        func.count(Job.id).label('count')
    ).group_by(
        func.strftime('%Y', Job.plan_start),
        func.strftime('%m', Job.plan_start),
        func.strftime('%d', Job.plan_start),
        Job.job_type
    ).order_by(
        func.strftime('%Y', Job.plan_start),
        func.strftime('%m', Job.plan_start),
        func.strftime('%d', Job.plan_start),
        Job.job_type
    ).all()

    # Mengubah hasil query menjadi format yang lebih mudah dibaca
    daily_data: Dict[str, Dict[str, Dict[str, int]]] = {}
    for year, month, day, job_type, count in daily_breakdown:
        month_name = get_month_name(month)
        month_key = f"{year} {month_name}"
        day_key = f"D{day:02d}"
        if month_key not in daily_data:
            daily_data[month_key] = {}
        if day_key not in daily_data[month_key]:
            daily_data[month_key][day_key] = {'DRILLING': 0, 'WOWS': 0}
        daily_data[month_key][day_key][job_type.name] = count

    return {
        'TOTAL': {
            'DRILLING': {
                'EXPLORATION': total_exploration,
                'DEVELOPMENT': total_development
            },
            'WOWS': {
                'WORKOVER': total_work_over,
                'WELLSERVICE': total_well_service
            }
        },
        'CURRENT_DAY': {
            'DRILLING': {
                'EXPLORATION': current_day_exploration,
                'DEVELOPMENT': current_day_development
            },
            'WOWS': {
                'WORKOVER': current_day_work_over,
                'WELLSERVICE': current_day_well_service
            }
        },
        'DAILY_BREAKDOWN': daily_data
    }
    
@router.get("/plot3d-data")
async def plot3d_data():
    # Membuat data untuk plot 3D
    x = np.linspace(-5, 5, 100)
    y = np.linspace(-5, 5, 100)
    X, Y = np.meshgrid(x, y)
    Z = np.sin(np.sqrt(X**2 + Y**2))

    # Membuat plot 3D
    fig = go.Figure(data=[go.Surface(z=Z, x=x, y=y)])
    fig.update_layout(title='Plot 3D Contoh', autosize=True,
                      scene=dict(
                          xaxis_title='X Axis',
                          yaxis_title='Y Axis',
                          zaxis_title='Z Axis'))

    # Mengembalikan data plot sebagai dictionary
    return fig.to_dict()