import os
import shutil

# Folders and patterns to target
TARGETS = ['__pycache__', '.venv', '.pytest_cache', 'build', 'dist']

def clean_projects(base_path):
    for root, dirs, files in os.walk(base_path):
        for name in dirs:
            if name in TARGETS:
                path = os.path.join(root, name)
                print(f"Deleting: {path}")
                shutil.rmtree(path, ignore_errors=True)

# Run this in your main "Projects" directory
clean_projects('./')