from sqlalchemy.orm import Session
from app.api.auth import crud, schemas, models
from fastapi import HTTPException, Depends, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from app.core.schema_operations import create_api_response
from app.core.config import settings
from app.core.security import authenticate_user, create_access_token, get_current_user, get_db, authorize,refresh_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        return create_api_response(success=False, message="Incorrect username or password", status_code=401)

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/refresh-token")
async def refresh_token_route(new_token: dict = Depends(refresh_token)):
    return new_token

@router.post("/user/create-admin")
async def create_admin(admin: schemas.CreateAdmin, db: Session = Depends(get_db)):
    created_admin = crud.create_admin(db, admin)
    if not created_admin:
        return create_api_response(success=False, message="Failed to create admin user", status_code=400)
    return create_api_response(success=True, message="Admin created successfully")

@router.get('/user/me', summary='Get details of currently logged in user', response_model=schemas.GetKKKSUser, response_model_exclude_unset=True)
async def get_me(user = Depends(get_current_user)):
    return schemas.GetKKKSUser.model_validate(user)

@router.post('/user/verify/{user_id}', response_model=schemas.VerifyUser)
@authorize(role=[models.Role.Admin])
async def verify_user(user_id: str, db: Session = Depends(get_db), user: schemas.GetUser = Depends(get_current_user)):
    db_user = db.query(models.User).get(user_id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    db_user.verified_status = True
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/kkks/create", response_model=schemas.GetKKKS)
@authorize(role=[models.Role.Admin])
async def create_user(kkks: schemas.CreateKKKS, db: Session = Depends(get_db), user: schemas.GetUser = Depends(get_current_user)):
    created_kkks = crud.create_kkks(db, kkks)
    if not created_kkks:
        raise HTTPException(status_code=400, detail="Failed to create KKKS")
    return created_kkks

@router.get("/kkks/{kkks_id}", response_model=schemas.GetKKKS)
@authorize(role=[models.Role.Admin])
async def get_user(kkks_id: str, db: Session = Depends(get_db), user: schemas.GetUser = Depends(get_current_user)):
    kkks = crud.get_kkks(db, kkks_id)
    if kkks is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="KKKS not found")
    return kkks