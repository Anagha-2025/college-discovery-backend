from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi.security import OAuth2PasswordRequestForm

# Local imports
from . import models, schemas, auth_utils 
from .database import engine, get_db
from .models import College, User
from .auth_utils import verify_password, create_access_token

# Automatically create tables in Postgres if they don't exist
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="College Discovery API")

# --- 🌐 CORS CONFIGURATION (Aggressive Fix) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
def home():
    return {"message": "College Discovery API is running!"}

# --- 🔍 COLLEGE ROUTES ---

@app.get("/colleges")
def get_colleges(
    db: Session = Depends(get_db),
    search: Optional[str] = None,
    min_fees: Optional[int] = None,
    max_fees: Optional[int] = None,
    limit: int = 20,
    offset: int = 0
):
    query = db.query(College)
    if search:
        query = query.filter(College.name.ilike(f"%{search}%"))
    if min_fees:
        query = query.filter(College.fees >= min_fees)
    if max_fees:
        query = query.filter(College.fees <= max_fees)

    return query.offset(offset).limit(limit).all()

@app.get("/colleges/{college_id}")
def get_college_detail(college_id: int, db: Session = Depends(get_db)):
    college = db.query(College).filter(College.id == college_id).first()
    if not college:
        raise HTTPException(status_code=404, detail="College not found")
    return college

@app.get("/compare")
def compare_colleges(
    ids: List[int] = Query(...), 
    db: Session = Depends(get_db)
):
    if len(ids) > 3:
        raise HTTPException(status_code=400, detail="Cannot compare more than 3 colleges")
    
    return db.query(College).filter(College.id.in_(ids)).all()

# --- 🔐 AUTHENTICATION ROUTES ---

@app.post("/signup")
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first() 
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    try:
        hashed_password = auth_utils.hash_password(user.password)
    except AttributeError:
        hashed_password = auth_utils.get_password_hash(user.password)
    
    new_user = models.User(
        email=user.email, 
        hashed_password=hashed_password, 
        full_name=user.full_name,
        is_active=True 
    )
    
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {"message": "User created successfully"}
    except Exception as e:
        db.rollback()
        print(f"Database Error: {e}")
        raise HTTPException(status_code=500, detail="Database save failed.")
    

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": user.email})
    
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "user_name": user.full_name 
    }