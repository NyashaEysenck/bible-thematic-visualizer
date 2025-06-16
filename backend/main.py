
from fastapi import FastAPI, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from pathlib import Path

from database import get_db, close_db_connection
from data_loader import load_all_data
from routers import bible, themes, explanations

@asynccontextmanager
async def lifespan(app: FastAPI):
   # Startup
   db = get_db()
   app.state.DATA = await load_all_data(db)
   yield
   # Shutdown
   close_db_connection()

app = FastAPI(
   title="Thematic Bible Visualizer API",
   description="API for accessing biblical themes, books, and their connections",
   version="1.0.0",
   lifespan=lifespan
)

app.add_middleware(
   CORSMiddleware,
   allow_origins=["*"],
   allow_credentials=True,
   allow_methods=["*"],
   allow_headers=["*"],
)

# Include routers
app.include_router(bible.router)
app.include_router(themes.router)
app.include_router(explanations.router)

# Exception Handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
   return JSONResponse(
       status_code=exc.status_code,
       content={"detail": exc.detail}
   )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
   return JSONResponse(
       status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
       content={"detail": "An unexpected error occurred"}
   )

# Health check
@app.get("/api/v1/health")
async def health_check():
   """Health check endpoint to verify the API is running."""
   return {"status": "healthy"}

# Static files configuration
frontend_dist_path = Path("frontend/dist")
if frontend_dist_path.exists():
   assets_path = frontend_dist_path / "assets"
   if assets_path.exists():
       app.mount("/assets", StaticFiles(directory=str(assets_path)), name="assets")

   for static_dir in ["js", "css", "img", "images", "fonts"]:
       static_path = frontend_dist_path / static_dir
       if static_path.exists():
           app.mount(f"/{static_dir}", StaticFiles(directory=str(static_path)), name=static_dir)
   
   @app.get("/{catchall:path}")
   async def serve_spa(catchall: str):
       if not catchall.startswith("api/"):
           index_path = frontend_dist_path / "index.html"
           if index_path.exists():
               return FileResponse(str(index_path))
       raise HTTPException(status_code=404, detail="Not Found")

if __name__ == "__main__":
   import uvicorn
   uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)