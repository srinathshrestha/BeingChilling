from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy import Column, String, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
import uuid
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# FastAPI instance
app = FastAPI()

# Jinja2 templates
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Model for Movie
class Movie(Base):
    __tablename__ = "movies"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    category = Column(String, nullable=True)
    poster_url = Column(String, nullable=True)
    gcp_path = Column(String, nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)

# Create tables in the database
Base.metadata.create_all(bind=engine)

# Home route to display movies
@app.get("/")
async def home(request: Request, db: Session = Depends(get_db)):
    # Fetch all movies from the database
    movies = db.query(Movie).all()
    return templates.TemplateResponse("index.html", {"request": request, "movies": movies})

# Route to list movies with filtering options
@app.get("/movies/")
async def list_movies(category: str = None, name: str = None, db: Session = Depends(get_db)):
    query = db.query(Movie)
    if category:
        query = query.filter(Movie.category.ilike(f"%{category}%"))
    if name:
        query = query.filter(Movie.title.ilike(f"%{name}%"))
    movies = query.all()
    return {"movies": movies}

# Route to stream a movie on a separate page
@app.get("/movies/{movie_id}/stream")
async def stream_movie_page(movie_id: str, request: Request, db: Session = Depends(get_db)):
    # Retrieve the movie from the database
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    # Render the streaming template
    return templates.TemplateResponse("stream.html", {"request": request, "movie": movie})
