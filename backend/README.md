# Thematic Bible Visualizer - Backend

This is the FastAPI backend for the Thematic Bible Visualizer application.

## Setup

1. **Install Python 3.8+** if you haven't already.

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Backend

1. **Start the FastAPI server**:
   ```bash
   cd backend
   uvicorn app.main:app --reload
   ```

2. The API will be available at `http://localhost:8000`

3. **API Documentation**:
   - Swagger UI: `http://localhost:8000/docs`
   - ReDoc: `http://localhost:8000/redoc`

## API Endpoints

- `GET /api/v1/themes` - Get all biblical themes
- `GET /api/v1/books` - Get all biblical books
- `GET /api/v1/themes/{theme_id}/connections` - Get theme connections for a specific theme
- `GET /api/v1/books/{book_id}/insights` - Get insights for a specific book

## Development

- The main application code is in `app/main.py`
- The application uses Pydantic models for request/response validation
- Error handling is implemented using FastAPI's exception handlers

## Deployment

For production deployment, consider using:
- Gunicorn with Uvicorn workers
- A production ASGI server like Hypercorn or Daphne
- Environment variables for configuration
- A proper database instead of in-memory storage
