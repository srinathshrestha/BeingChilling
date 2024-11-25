from typing import Optional
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy import Column, Integer, String, DateTime, asc, create_engine, desc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
import uuid
import os
from dotenv import load_dotenv
import uvicorn

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
    uploaded_at = Column(DateTime, default=datetime.now)
    movie_cast = Column(String, nullable=True)
    director = Column(String, nullable=True)
    runtime = Column(Integer, nullable=True)  # Runtime in minutes
    release_date = Column(DateTime, nullable=True)

# Create tables in the database
Base.metadata.create_all(bind=engine)

# Home route to display movies
@app.get("/")
async def home(request: Request, db: Session = Depends(get_db)):
    # Fetch all movies from the database
    movies = db.query(Movie).all()
    return templates.TemplateResponse("index.html", {"request": request, "movies": movies})

# # Route to list movies with filtering options
# @app.get("/movies/")
# async def list_movies(category: str = None, name: str = None, db: Session = Depends(get_db)):
#     query = db.query(Movie)
#     if category:
#         query = query.filter(Movie.category.ilike(f"%{category}%"))
#     if name:
#         query = query.filter(Movie.title.ilike(f"%{name}%"))
#     movies = query.all()
#     return {"movies": movies}


@app.get("/movies/")
async def list_movies(
    category: Optional[str] = None,
    name: Optional[str] = None,
    sort: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Movie)

    # Apply filters
    if category:
        query = query.filter(Movie.category.ilike(f"%{category}%"))
    if name:
        query = query.filter(Movie.title.ilike(f"%{name}%"))

    # Apply sorting
    if sort:
        if sort == "release_date_desc":
            query = query.order_by(desc(Movie.release_date))
        elif sort == "release_date_asc":
            query = query.order_by(asc(Movie.release_date))
        elif sort == "runtime_desc":
            query = query.order_by(desc(Movie.runtime))
        elif sort == "runtime_asc":
            query = query.order_by(asc(Movie.runtime))
    else:
        # Default sorting by release date (newest first)
        query = query.order_by(desc(Movie.release_date))

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



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))  # Default to 8080 if PORT is not set
    uvicorn.run("main:app", host="0.0.0.0", port=port)