# Movie Streaming App

Welcome to the **Movie Streaming App**! This project is a web application that allows users to stream movies with advanced search, personalized recommendations, and a seamless, high-quality video streaming experience.

🔗 **Live App URL**: [Movie Streaming App](https://movie-streaming-app-144879262315.asia-south2.run.app/)

---

## 📜 Table of Contents

1. [Features](#features)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Deployment](#deployment)
5. [Future Improvements](#future-improvements)
6. [Technologies Used](#technologies-used)
7. [Contributing](#contributing)
8. [License](#license)

---

## 🎥 Features

### User Features
- **Authentication**: Login via Google SSO. Manage accounts with profile settings.
- **Movie Search and Filtering**:
  - Search by **title**, **genre**, **director**, **actor**, **release year**, and more.
  - Genre-based suggestions and trending movies displayed on the homepage.
- **Personalized Recommendations**:
  - Collaborative filtering to suggest movies based on user preferences.
  - "Users who watched X also watched Y" recommendations.
- **Video Player**:
  - High-quality video streaming with **adaptive bitrate** (HLS/DASH).
  - Interactive controls for subtitles, playback speed, volume, and “skip intro.”
  - Resume playback on multiple devices.
- **User Engagement**:
  - Rate and review movies.
  - Add movies to a **favorites** list and **watchlist**.

### Admin Features
- **Content Management**: Add, edit, delete movies and metadata (title, genre, cast, etc.).
- **User Management**: Admin dashboard to manage user accounts.
- **Logs and Analytics**: Track user engagement and monitor app performance.

### Performance and Caching
- **Memorystore (Redis)**: Cache frequently accessed resources for faster load times.
- **CDN Integration**: Use CDN for optimized content delivery based on user location.

### Security
- **Token-Based Video Access**: Prevent hotlinking and secure video content.
- **Role-Based Access Control**: Different access levels for users and admins.
- **Audit Logging**: Log all admin actions for transparency.

---

## 🛠 Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/movie-streaming-app.git
   cd movie-streaming-app
2. **Create and Activate a Virtual Environment**:

    ```bash
    python3 -m venv venv
    source venv/bin/activate

3. **Install Dependencies**:

    ```bash
    pip install -r requirements.txt

4. **Environment Variables**:

    ```bash
    DATABASE_URL=your_postgresql_database_url
    SECRET_KEY=your_secret_key
    GOOGLE_CLIENT_ID=your_google_client_id
    GOOGLE_CLIENT_SECRET=your_google_client_secret
    REDIS_URL=redis://your_redis_instance

5. **Run the App Locally**:
   ```bash
     uvicorn main:app --reload


## 🚀 Deployment
## Deploying on Google Cloud Run

### Build and Push Docker Image:

    ```bash
    docker build -t gcr.io/[YOUR_PROJECT_ID]/movie-streaming-app .
    docker push gcr.io/[YOUR_PROJECT_ID]/movie-streaming-app

### Build and Push Docker Image:
    ```bash
      gcloud run deploy movie-streaming-app \
    --image gcr.io/[YOUR_PROJECT_ID]/movie-streaming-app \
    --platform managed \
    --region asia-south2 \
    --allow-unauthenticated \
    --memory 1Gi \
    --cpu 2
### Continuous Deployment with GitHub Actions:
  GitHub Actions are set up to automatically deploy to Cloud Run on every push to the main branch. See the .github/workflows/deploy.yml file for the deployment workflow.


## 🔧 Configuration

### Google Cloud Setup
- **Cloud Storage**: Store movie files and metadata securely.
- **Memorystore (Redis)**: For caching movie metadata and other frequently accessed data.
- **BigQuery**: Used for analytics and user behavior insights.
- **Artifact Registry**: Host Docker images for deployment.

### Additional Services
- **CDN**: Integrate a CDN to reduce latency and improve streaming quality.
- **Cloud Monitoring and Sentry**: For logging, error tracking, and monitoring.

## 📈 Future Improvements
- **Advanced Search Capabilities**: Improve search by adding natural language processing for flexible queries.
- **Multi-Language Support**: Subtitle and audio options in multiple languages.
- **Machine Learning for Recommendations**: Leverage collaborative filtering to offer personalized recommendations.
- **Real-Time Chat**: Enable users to chat or discuss movies in real-time.
- **Improved Analytics**: Use BigQuery for complex insights, such as churn prediction and movie popularity trends.
- **Push Notifications**: Notify users about new movies or updates on their favorite genres.
- **Dark Mode**: Enable dark mode for user-friendly viewing at night.
- **Admin Dashboard**: Provide insights for admins, including user statistics, movie engagement, and app performance metrics.

## 📚 Technologies Used
- **Backend**: FastAPI, SQLAlchemy
- **Frontend**: Jinja2 Templates
- **Database**: PostgreSQL
- **Caching**: Redis
- **Containerization**: Docker
- **Deployment**: Google Cloud Run, Google Cloud Artifact Registry
- **Authentication**: Google OAuth2
- **CI/CD**: GitHub Actions
- **Monitoring**: Google Cloud Monitoring, Sentry (for error tracking)

## 🤝 Contributing
Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a feature branch:
   ```bash
   git checkout -b feature-name
3. Commit your changes:
   ```bash
      git commit -m "Add a feature"
5. Push to the branch:
    ```bash
       git push origin feature-name
## 📜 License
This project is licensed under the MIT License. See the LICENSE file for more details.


## 🚀 Deployment


