
# This router handles endpoints for biblical themes.
from fastapi import APIRouter, HTTPException, status, Request
from typing import List
from models import Theme, ThemeConnection

router = APIRouter()

@router.get("/api/v1/themes", response_model=List[Theme])
async def get_themes(request: Request):
   """Get all biblical themes."""
   return request.app.state.DATA["themes"]

@router.get("/api/v1/themes/{theme_id}/connections", response_model=List[ThemeConnection])
async def get_theme_connections(theme_id: str, request: Request):
   """Get connections for a specific theme."""
   connections = request.app.state.DATA["theme_connections"].get(theme_id)
   if connections is None:
       raise HTTPException(
           status_code=status.HTTP_404_NOT_FOUND,
           detail=f"No connections found for theme '{theme_id}'"
       )
   return connections
