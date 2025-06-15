#!/bin/bash

# Start the backend server in the background
echo "Starting FastAPI backend..."
cd backend
uvicorn app.main:app --reload --port 8000 &

# Save the backend process ID
BACKEND_PID=$!

# Go back to the project root
cd ..

# Start the frontend development server
echo "Starting Vite frontend..."
cd frontend
npm run dev -- --port 3000 &

# Save the frontend process ID
FRONTEND_PID=$!

# Go back to the project root
cd ..

# Function to clean up processes on script exit
cleanup() {
  echo "Stopping servers..."
  kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
  exit 0
}

# Set up trap to catch script termination
trap cleanup SIGINT SIGTERM

# Keep the script running
wait $BACKEND_PID $FRONTEND_PID
