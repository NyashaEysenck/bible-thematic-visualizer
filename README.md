# Thematic Bible Visualizer

A web application for exploring biblical themes across scripture, built with React (Vite) and FastAPI.

## Features

- Browse biblical themes and their connections across scripture
- Interactive timeline showing theme prominence throughout the Bible
- Detailed insights for each book of the Bible
- Responsive design that works on desktop and tablet
- Interactive timeline navigation
- Responsive design for all devices

## System Architecture

The application consists of two main components:

1. **Frontend**: React-based web application
2. **Backend**: FastAPI RESTful API service

## Getting Started

### Prerequisites

- Node.js (v16 or later) for the frontend
- Python 3.8+ for the backend
- npm or yarn
- pip (Python package manager)

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create and activate a virtual environment (recommended):
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Start the backend server:
   ```bash
   uvicorn app.main:app --reload
   ```

   The API will be available at `http://localhost:8000`

### Frontend Setup

1. In a new terminal, navigate to the project root directory.

2. Install Node.js dependencies:
   ```bash
   npm install
   # or
   yarn install
   ```

3. Start the development server:
   ```bash
   npm run dev
   # or
   yarn dev
   ```

4. Open [http://localhost:3000](http://localhost:3000) in your browser.

## Development

### Project Structure

- `/src` - Frontend React application
  - `/components` - Reusable React components
  - `/utils` - Utility functions and API clients
  - `/styles` - CSS styles
- `/backend` - FastAPI backend
  - `/app` - Python application code
  - `requirements.txt` - Python dependencies

### Environment Variables

Create a `.env` file in the project root with the following variables:

```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

## API Documentation

When the backend is running, you can access:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Built With

### Frontend
- [React](https://reactjs.org/)
- [Vite](https://vitejs.dev/)
- [Lucide Icons](https://lucide.dev/)
- [Tailwind CSS](https://tailwindcss.com/)

### Backend
- [FastAPI](https://fastapi.tiangolo.com/)
- [Uvicorn](https://www.uvicorn.org/)
- [Pydantic](https://pydantic-docs.helpmanual.io/)

## License

This project is licensed under the MIT License.
