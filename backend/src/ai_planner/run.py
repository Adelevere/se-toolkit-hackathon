"""Run the AI Planner FastAPI server."""

import sys
from pathlib import Path

# Add the src directory to the Python path
src_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(src_dir))


def run_server():
    """Run the uvicorn server with configured settings."""
    import uvicorn
    from ai_planner.settings import settings

    uvicorn.run(
        app="ai_planner.main:app",
        host=settings.address,
        port=settings.port,
        reload=settings.reload,
    )


if __name__ == "__main__":
    run_server()
