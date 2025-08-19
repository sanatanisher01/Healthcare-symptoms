import uvicorn
import os
import sys

if __name__ == "__main__":
    # Ensure we're using the virtual environment
    venv_python = "/opt/render/project/src/backend/venv/bin/python"
    if os.path.exists(venv_python) and sys.executable != venv_python:
        os.execv(venv_python, [venv_python] + sys.argv)
    
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)