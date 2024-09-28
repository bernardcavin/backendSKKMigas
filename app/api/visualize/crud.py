from app.api.job.models import *
from app.api.utils.schemas import *
from sqlalchemy.orm import Session
from app.api.well.models import *
import app.api.visualize.lib.gantt_chart as gantt

def get_well_data(data_class: DataClass, db: Session, well_id: str):
    return db.query(WellDigitalData).filter(WellDigitalData.data_class == data_class, WellDigitalData.well_id == well_id).first()

def visualize_work_breakdown_structure(db: Session, job_id: str):
    
    db_job = db.query(Job).filter(Job.id == job_id).first()
    
    plan_wbs = db_job.job_plan.work_breakdown_structure
    actual_wbs = getattr(db_job.actual_job, 'work_breakdown_structure', None)
    
    actual_wbs_event_dict = {
        event.event : {
            'start_date': getattr(event, 'start_date'),
            'end_date': getattr(event, 'end_date')
        } for event in actual_wbs.events
    } if actual_wbs else {}
    
    if db_job.job_type in [JobType.EXPLORATION, JobType.DEVELOPMENT]:
        
        wrm_data = {
            "wrm_internal_kkks": {
                "label": "Internal KKKS",
                "plan_start_date": getattr(getattr(plan_wbs, "wrm_internal_kkks", None), "start_date", None),
                "plan_end_date": getattr(getattr(plan_wbs, "wrm_internal_kkks", None), "end_date", None),
                "actual_start_date": getattr(getattr(actual_wbs, "wrm_internal_kkks", None), "start_date", None),
                "actual_end_date": getattr(getattr(actual_wbs, "wrm_internal_kkks", None), "end_date", None)
            },
            "wrm_persiapan_lokasi": {
                "label": "Persiapan Lokasi",
                "plan_start_date": getattr(getattr(plan_wbs, "wrm_persiapan_lokasi", None), "start_date", None),
                "plan_end_date": getattr(getattr(plan_wbs, "wrm_persiapan_lokasi", None), "end_date", None),
                "actual_start_date": getattr(getattr(actual_wbs, "wrm_persiapan_lokasi", None), "start_date", None),
                "actual_end_date": getattr(getattr(actual_wbs, "wrm_persiapan_lokasi", None), "end_date", None)
            },
            "wrm_pengadaan_lli": {
                "label": "Pengadaan LLI",
                "plan_start_date": getattr(getattr(plan_wbs, "wrm_pengadaan_lli", None), "start_date", None),
                "plan_end_date": getattr(getattr(plan_wbs, "wrm_pengadaan_lli", None), "end_date", None),
                "actual_start_date": getattr(getattr(actual_wbs, "wrm_pengadaan_lli", None), "start_date", None),
                "actual_end_date": getattr(getattr(actual_wbs, "wrm_pengadaan_lli", None), "end_date", None)
            },
            "wrm_pembebasan_lahan": {
                "label": "Pembebasan Lahan",
                "plan_start_date": getattr(getattr(plan_wbs, "wrm_pembebasan_lahan", None), "start_date", None),
                "plan_end_date": getattr(getattr(plan_wbs, "wrm_pembebasan_lahan", None), "end_date", None),
                "actual_start_date": getattr(getattr(actual_wbs, "wrm_pembebasan_lahan", None), "start_date", None),
                "actual_end_date": getattr(getattr(actual_wbs, "wrm_pembebasan_lahan", None), "end_date", None)
            },
            "wrm_ippkh": {
                "label": "IPPKH",
                "plan_start_date": getattr(getattr(plan_wbs, "wrm_ippkh", None), "start_date", None),
                "plan_end_date": getattr(getattr(plan_wbs, "wrm_ippkh", None), "end_date", None),
                "actual_start_date": getattr(getattr(actual_wbs, "wrm_ippkh", None), "start_date", None),
                "actual_end_date": getattr(getattr(actual_wbs, "wrm_ippkh", None), "end_date", None)
            },
            "wrm_ukl_upl": {
                "label": "UKL/UPL",
                "plan_start_date": getattr(getattr(plan_wbs, "wrm_ukl_upl", None), "start_date", None),
                "plan_end_date": getattr(getattr(plan_wbs, "wrm_ukl_upl", None), "end_date", None),
                "actual_start_date": getattr(getattr(actual_wbs, "wrm_ukl_upl", None), "start_date", None),
                "actual_end_date": getattr(getattr(actual_wbs, "wrm_ukl_upl", None), "end_date", None)
            },
            "wrm_amdal": {
                "label": "Amdal",
                "plan_start_date": getattr(getattr(plan_wbs, "wrm_amdal", None), "start_date", None),
                "plan_end_date": getattr(getattr(plan_wbs, "wrm_amdal", None), "end_date", None),
                "actual_start_date": getattr(getattr(actual_wbs, "wrm_amdal", None), "start_date", None),
                "actual_end_date": getattr(getattr(actual_wbs, "wrm_amdal", None), "end_date", None)
            },
            "wrm_pengadaan_rig": {
                "label": "Pengadaan Rig",
                "plan_start_date": getattr(getattr(plan_wbs, "wrm_pengadaan_rig", None), "start_date", None),
                "plan_end_date": getattr(getattr(plan_wbs, "wrm_pengadaan_rig", None), "end_date", None),
                "actual_start_date": getattr(getattr(actual_wbs, "wrm_pengadaan_rig", None), "start_date", None),
                "actual_end_date": getattr(getattr(actual_wbs, "wrm_pengadaan_rig", None), "end_date", None)
            },
            "wrm_pengadaan_drilling_services": {
                "label": "Pengadaan Drilling Services",
                "plan_start_date": getattr(getattr(plan_wbs, "wrm_pengadaan_drilling_services", None), "start_date", None),
                "plan_end_date": getattr(getattr(plan_wbs, "wrm_pengadaan_drilling_services", None), "end_date", None),
                "actual_start_date": getattr(getattr(actual_wbs, "wrm_pengadaan_drilling_services", None), "start_date", None),
                "actual_end_date": getattr(getattr(actual_wbs, "wrm_pengadaan_drilling_services", None), "end_date", None)
            },
            "wrm_evaluasi_subsurface": {
                "label": "Evaluasi Subsurface",
                "plan_start_date": getattr(getattr(plan_wbs, "wrm_evaluasi_subsurface", None), "start_date", None),
                "plan_end_date": getattr(getattr(plan_wbs, "wrm_evaluasi_subsurface", None), "end_date", None),
                "actual_start_date": getattr(getattr(actual_wbs, "wrm_evaluasi_subsurface", None), "start_date", None),
                "actual_end_date": getattr(getattr(actual_wbs, "wrm_evaluasi_subsurface", None), "end_date", None)
            },
        }
        
        if db_job.job_type == JobType.DEVELOPMENT:
            
            wrm_data["wrm_cutting_dumping"] = {
                "label": "Cutting/Dumping",
                "plan_start_date": getattr(getattr(plan_wbs, "wrm_cutting_dumping", None), "start_date", None),
                "plan_end_date": getattr(getattr(plan_wbs, "wrm_cutting_dumping", None), "end_date", None)
            }
        
    elif db_job.job_type in [JobType.WORKOVER, JobType.WELLSERVICE]:
        
        wrm_data = {
            'wrm_internal_kkks': {
                'label': 'Internal KKKS',
                'plan_start_date': getattr(getattr(plan_wbs, 'wrm_internal_kkks', None), 'start_date', None),
                'plan_end_date': getattr(getattr(plan_wbs, 'wrm_internal_kkks', None), 'end_date', None),
                'actual_start_date': getattr(getattr(actual_wbs, 'wrm_internal_kkks', None), 'start_date', None),
                'actual_end_date': getattr(getattr(actual_wbs, 'wrm_internal_kkks', None), 'end_date', None)
            },
            'wrm_persiapan_lokasi': {
                'label': 'Persiapan Lokasi',
                'plan_start_date': getattr(getattr(plan_wbs, 'wrm_persiapan_lokasi', None), 'start_date', None),
                'plan_end_date': getattr(getattr(plan_wbs, 'wrm_persiapan_lokasi', None), 'end_date', None),
                'actual_start_date': getattr(getattr(actual_wbs, 'wrm_persiapan_lokasi', None), 'start_date', None),
                'actual_end_date': getattr(getattr(actual_wbs, 'wrm_persiapan_lokasi', None), 'end_date', None)
            },
            'wrm_pengadaan_lli': {
                'label': 'Pengadaan LLI',
                'plan_start_date': getattr(getattr(plan_wbs, 'wrm_pengadaan_lli', None), 'start_date', None),
                'plan_end_date': getattr(getattr(plan_wbs, 'wrm_pengadaan_lli', None), 'end_date', None),
                'actual_start_date': getattr(getattr(actual_wbs, 'wrm_pengadaan_lli', None), 'start_date', None),
                'actual_end_date': getattr(getattr(actual_wbs, 'wrm_pengadaan_lli', None), 'end_date', None)
            },
            'wrm_pengadaan_equipment': {
                'label': 'Pengadaan Equipment',
                'plan_start_date': getattr(getattr(plan_wbs, 'wrm_pengadaan_equipment', None), 'start_date', None),
                'plan_end_date': getattr(getattr(plan_wbs, 'wrm_pengadaan_equipment', None), 'end_date', None),
                'actual_start_date': getattr(getattr(actual_wbs, 'wrm_pengadaan_equipment', None), 'start_date', None),
                'actual_end_date': getattr(getattr(actual_wbs, 'wrm_pengadaan_equipment', None), 'end_date', None)
            },
            'wrm_pengadaan_services': {
                'label': 'Pengadaan Services',
                'plan_start_date': getattr(getattr(plan_wbs, 'wrm_pengadaan_services', None), 'start_date', None),
                'plan_end_date': getattr(getattr(plan_wbs, 'wrm_pengadaan_services', None), 'end_date', None),
                'actual_start_date': getattr(getattr(actual_wbs, 'wrm_pengadaan_services', None), 'start_date', None),
                'actual_end_date': getattr(getattr(actual_wbs, 'wrm_pengadaan_services', None), 'end_date', None)
            },
            'wrm_pengadaan_handak': {
                'label': 'Pengadaan Handak',
                'plan_start_date': getattr(getattr(plan_wbs, 'wrm_pengadaan_handak', None), 'start_date', None),
                'plan_end_date': getattr(getattr(plan_wbs, 'wrm_pengadaan_handak', None), 'end_date', None),
                'actual_start_date': getattr(getattr(actual_wbs, 'wrm_pengadaan_handak', None), 'start_date', None),
                'actual_end_date': getattr(getattr(actual_wbs, 'wrm_pengadaan_handak', None), 'end_date', None)
            },
            'wrm_pengadaan_octg': {
                'label': 'Pengadaan OCTG',
                'plan_start_date': getattr(getattr(plan_wbs, 'wrm_pengadaan_octg', None), 'start_date', None),
                'plan_end_date': getattr(getattr(plan_wbs, 'wrm_pengadaan_octg', None), 'end_date', None),
                'actual_start_date': getattr(getattr(actual_wbs, 'wrm_pengadaan_octg', None), 'start_date', None),
                'actual_end_date': getattr(getattr(actual_wbs, 'wrm_pengadaan_octg', None), 'end_date', None)
            },
            'wrm_pengadaan_artificial_lift': {
                'label': 'Pengadaan Artificial Lift',
                'plan_start_date': getattr(getattr(plan_wbs, 'wrm_pengadaan_artificial_lift', None), 'start_date', None),
                'plan_end_date': getattr(getattr(plan_wbs, 'wrm_pengadaan_artificial_lift', None), 'end_date', None),
                'actual_start_date': getattr(getattr(actual_wbs, 'wrm_pengadaan_artificial_lift', None), 'start_date', None),
                'actual_end_date': getattr(getattr(actual_wbs, 'wrm_pengadaan_artificial_lift', None), 'end_date', None)
            },
            'wrm_sumur_berproduksi': {
                'label': 'Sumur Berproduksi',
                'plan_start_date': getattr(getattr(plan_wbs, 'wrm_sumur_berproduksi', None), 'start_date', None),
                'plan_end_date': getattr(getattr(plan_wbs, 'wrm_sumur_berproduksi', None), 'end_date', None),
                'actual_start_date': getattr(getattr(actual_wbs, 'wrm_sumur_berproduksi', None), 'start_date', None),
                'actual_end_date': getattr(getattr(actual_wbs, 'wrm_sumur_berproduksi', None), 'end_date', None)
            },
            'wrm_fasilitas_produksi': {
                'label': 'Fasilitas Produksi',
                'plan_start_date': getattr(getattr(plan_wbs, 'wrm_fasilitas_produksi', None), 'start_date', None),
                'plan_end_date': getattr(getattr(plan_wbs, 'wrm_fasilitas_produksi', None), 'end_date', None),
                'actual_start_date': getattr(getattr(actual_wbs, 'wrm_fasilitas_produksi', None), 'start_date', None),
                'actual_end_date': getattr(getattr(actual_wbs, 'wrm_fasilitas_produksi', None), 'end_date', None)
            },
            'wrm_persiapan_lokasi': {
                'label': 'Persiapan Lokasi',
                'plan_start_date': getattr(getattr(plan_wbs, 'wrm_persiapan_lokasi', None), 'start_date', None),
                'plan_end_date': getattr(getattr(plan_wbs, 'wrm_persiapan_lokasi', None), 'end_date', None),
                'actual_start_date': getattr(getattr(actual_wbs, 'wrm_persiapan_lokasi', None), 'start_date', None),
                'actual_end_date': getattr(getattr(actual_wbs, 'wrm_persiapan_lokasi', None), 'end_date', None)
            },
            'wrm_well_integrity': {
                'label': 'Well Integrity',
                'plan_start_date': getattr(getattr(plan_wbs, 'wrm_well_integrity', None), 'start_date', None),
                'plan_end_date': getattr(getattr(plan_wbs, 'wrm_well_integrity', None), 'end_date', None),
                'actual_start_date': getattr(getattr(actual_wbs, 'wrm_well_integrity', None), 'start_date', None),
            },
        }
    
    last_index = 1
    
    all_data = []
    plans = []
    actuals = []
    
    for wrm in wrm_data.values():
        if wrm:
        
            all_data.append({
                'name': wrm['label'],
                'start': wrm.get('plan_start_date', None),
                'finish': wrm.get('plan_end_date', None),
                'resource': None,
                'predecessor': None,
                'milestone': None,
                'parent': ''
            })
            
            plans.append({
                'name': 'Plan',
                'start': wrm.get('plan_start_date', None),
                'finish': wrm.get('plan_end_date', None),
                'resource': None,
                'predecessor': None,
                'milestone': None,
                'parent': last_index
            })
            
            actuals.append({
                'name': 'Actual',
                'start': wrm.get('actual_start_date', None),
                'finish': wrm.get('actual_end_date', None),
                'resource': None,
                'predecessor': None,
                'milestone': None,
                'parent': last_index,
                'color':'red'
            })
            
            last_index += 1

    for i, event in enumerate(plan_wbs.events):
        
        parent = {
            'name': getattr(event, 'event'),
            'start': getattr(event, 'start_date'),
            'finish': getattr(event, 'end_date'),
            'resource': None,
            'predecessor': None,
            'milestone': None,
            'parent': ''
        }
        
        all_data.append(parent)
        
        plan = {
            'name': 'Plan',
            'start': getattr(event, 'start_date'),
            'finish': getattr(event, 'end_date'),
            'resource': None,
            'predecessor': None,
            'milestone': None,
            'parent': last_index + i
        }
        
        actual = {
            'name': 'Actual',
            'start': actual_wbs_event_dict.get(event.event, {}).get('start_date', None),
            'finish': actual_wbs_event_dict.get(event.event, {}).get('end_date', None),
            'resource': None,
            'predecessor': None,
            'milestone': None,
            'parent': last_index + i,
            'color':'red'
        }
        
        plans.append(plan)
        actuals.append(actual)
        
    all_data = all_data + plans + actuals

    data = gantt.Data()
    index = 1
    for d in all_data:
        
        if d['start'] and d['finish']:
            data.add(index,d['name'],d['start'].strftime('%Y-%m-%d'),d['finish'].strftime('%Y-%m-%d'),d['resource'],d['predecessor'],d['milestone'],d['parent'], d.get('color', '#67AAFF'))
        else:
            data.add(index,d['name'],d['start'],d['finish'],d['resource'],d['predecessor'],d['milestone'],d['parent'], d.get('color', '#67AAFF'))
        index += 1
    # print(data.data)
    
    temp = gantt.Gantt()
    temp.load(data.data)
    temp.ganttChart('Work Breakdown Structure')
    svg_string = temp.to_string()

    return svg_string