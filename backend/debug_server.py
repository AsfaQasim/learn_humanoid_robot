import uvicorn
import sys
import os

if __name__ == "__main__":
    # Add the parent directory to the path so we can import modules
    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
    
    print("Importing app module...")
    import app
    print("App module imported successfully")
    
    print("Available routes:")
    for route in app.app.routes:
        print(f"  {route.methods} {route.path}")
    
    print("Running the FastAPI server...")
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=False,  # Disable reload to simplify debugging
        log_level="info"
    )