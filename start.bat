@echo off
REM Start the backend server in a new window
start "Backend Server" cmd /k "cd backend && uvicorn app.main:app --reload --port 8000"

REM Start the frontend in a new window
start "Frontend Server" cmd /k "cd frontend && npm run dev -- --port 3000"

echo Both servers are starting...
echo Backend will be available at: http://localhost:8000
echo Frontend will be available at: http://localhost:3000

REM Keep the window open
pause
