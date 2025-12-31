"""
Complete Python cache cleanup script.
Removes all .pyc files and __pycache__ directories.
"""
import os
import shutil
import pathlib

def clear_cache():
    """Remove all Python cache files and directories."""
    base_dir = pathlib.Path(__file__).parent.parent
    removed_count = 0

    print("Clearing Python cache files...")
    print(f"Base directory: {base_dir}\n")

    # Remove all __pycache__ directories
    for cache_dir in base_dir.rglob("__pycache__"):
        try:
            shutil.rmtree(cache_dir)
            print(f"[OK] Removed: {cache_dir}")
            removed_count += 1
        except Exception as e:
            print(f"[FAIL] Failed to remove {cache_dir}: {e}")

    # Remove all .pyc files
    for pyc_file in base_dir.rglob("*.pyc"):
        try:
            pyc_file.unlink()
            print(f"[OK] Removed: {pyc_file}")
            removed_count += 1
        except Exception as e:
            print(f"[FAIL] Failed to remove {pyc_file}: {e}")

    # Remove all .pyo files
    for pyo_file in base_dir.rglob("*.pyo"):
        try:
            pyo_file.unlink()
            print(f"[OK] Removed: {pyo_file}")
            removed_count += 1
        except Exception as e:
            print(f"[FAIL] Failed to remove {pyo_file}: {e}")

    print(f"\n[DONE] Cleanup complete! Removed {removed_count} cache items.")
    print("\nNow restart your server with:")
    print("  python run_server.py")

if __name__ == "__main__":
    clear_cache()
