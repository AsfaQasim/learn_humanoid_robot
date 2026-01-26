import sys
import os

# Add current directory first
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

print("Python path:")
for p in sys.path[:5]:  # Just show first 5 paths
    print(f"  {p}")

print("\nTrying to import the local app module...")

# Check if our app.py exists and what it contains
app_path = os.path.join(current_dir, "app.py")
if os.path.exists(app_path):
    print(f"Found app.py at: {app_path}")
    
    # Read the first few lines to verify it's our file
    with open(app_path, 'r', encoding='utf-8') as f:
        first_lines = ''.join(f.readlines()[:20])
        print("First 20 lines of app.py:")
        print(first_lines[:500])  # Just first 500 chars
else:
    print("app.py not found!")

try:
    import app
    print(f"\nSuccessfully imported app module from: {app.__file__}")
    
    # Check if the app has the expected attributes
    if hasattr(app, 'app'):
        print("Found 'app' attribute in imported module")
        print(f"Type: {type(app.app)}")
        
        # Check routes
        if hasattr(app.app, 'routes'):
            print("Routes in app:")
            for route in app.app.routes:
                print(f"  {route.methods} {route.path}")
    else:
        print("No 'app' attribute found in imported module")
        
except ImportError as e:
    print(f"Failed to import app: {e}")
    
    # Try to see what's causing the issue
    import traceback
    traceback.print_exc()