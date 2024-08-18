from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.routers.auth.utils import authorize
from backend.routers.auth import crud, schemas, utils, models

from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

router = APIRouter(prefix="/auth", tags=["auth"])

# Define endpoints for token generation and authentication
@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(utils.get_db)):
    user = utils.authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=utils.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = utils.create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/user/create", response_model=schemas.GetUser)
async def create_user(user: schemas.CreateUser, db: Session = Depends(utils.get_db)):
    return crud.create_user(db, user)

@router.get('/user/me', summary='Get details of currently logged in user', response_model=schemas.GetUser)
async def get_me(user: schemas.GetUser = Depends(utils.get_current_user)):
    return user

@router.post('/user/verify/{user_id}', response_model=schemas.VerifyUser)
@authorize(role=[models.Role.Admin])
async def create_user(user_id: str, db: Session = Depends(utils.get_db), user: schemas.GetUser = Depends(utils.get_current_user)):
    user = db.query(models.User).get(user_id)
    user.verfied_status = True
    db.commit()
    return user

@router.post("/kkks/create", response_model=schemas.GetKKKS)
@authorize(role=[models.Role.Admin])
async def create_user(kkks: schemas.CreateKKKS, db: Session = Depends(utils.get_db), user: schemas.GetUser = Depends(utils.get_current_user)):
    return crud.create_kkks(db, kkks)

@router.get("/kkks/{kkks_id}", response_model=schemas.GetKKKS)
@authorize(role=[models.Role.Admin])
async def get_user(kkks_id: str, db: Session = Depends(utils.get_db), user: schemas.GetUser = Depends(utils.get_current_user)):
    kkks = crud.get_kkks(db, kkks_id)
    if kkks is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="KKKS not found")
    return kkks
