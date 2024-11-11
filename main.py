from fastapi import FastAPI, Depends, HTTPException
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

# Setup SQLAlchemy
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# FastAPI instance
app = FastAPI()

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

# Create tables in the database (run only once or manage migrations separately)
Base.metadata.create_all(bind=engine)

# Home route to display all movies (JSON response)
@app.get("/")
async def home(db: Session = Depends(get_db)):
    # Fetch all movies from the database
    movies = db.query(Movie).all()
    # Convert movies to a dictionary for JSON response
    movies_list = [{"id": movie.id, "title": movie.title, "category": movie.category} for movie in movies]
    return {"movies": movies_list}

# Route to list movies with filtering options
@app.get("/movies/")
async def list_movies(category: str = None, name: str = None, db: Session = Depends(get_db)):
    query = db.query(Movie)
    if category:
        query = query.filter(Movie.category.ilike(f"%{category}%"))
    if name:
        query = query.filter(Movie.title.ilike(f"%{name}%"))
    movies = query.all()
    # Convert movies to a dictionary for JSON response
    movies_list = [{"id": movie.id, "title": movie.title, "category": movie.category} for movie in movies]
    return {"movies": movies_list}

# Route to get movie details for streaming
@app.get("/movies/{movie_id}")
async def get_movie_details(movie_id: str, db: Session = Depends(get_db)):
    # Retrieve the movie from the database
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    # Return movie details as JSON
    movie_data = {
        "id": movie.id,
        "title": movie.title,
        "description": movie.description,
        "category": movie.category,
        "poster_url": movie.poster_url,
        "gcp_path": movie.gcp_path,
        "uploaded_at": movie.uploaded_at.isoformat()
    }
    return {"movie": movie_data}

# Entry point for local development
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))  # Default to 8080 if PORT is not set
    uvicorn.run("main:app", host="0.0.0.0", port=port)
