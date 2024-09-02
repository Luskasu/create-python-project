import os
import subprocess
import sys
from constants import *

def create_and_activate_venv(venv_path):
    # Create venv if it doesn't exist
    if not os.path.exists(venv_path):
        subprocess.run([sys.executable, "-m", "venv", venv_path], check=True)
    
    # Determine the path to the activate script
    if sys.platform == "win32":
        activate_script = os.path.join(venv_path, "Scripts", "activate.bat")
        python_executable = os.path.join(venv_path, "Scripts", "python.exe")
    else:
        activate_script = os.path.join(venv_path, "bin", "activate")
        python_executable = os.path.join(venv_path, "bin", "python")
    
    # Activate the venv and run a Python command to verify
    if sys.platform == "win32":
        command = f'"{activate_script}" && "{python_executable}" -c "import sys; print(sys.prefix)"'
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
    else:
        command = f'source "{activate_script}" && "{python_executable}" -c "import sys; print(sys.prefix)"'
        result = subprocess.run(command, shell=True, capture_output=True, text=True, executable='/bin/bash')
    
    return python_executable


def create_python_project(name:str, open_IDE = True):
    full_path = os.path.join(PROJECTS_PATH, name)
    src_path = os.path.join(full_path, "src")
    os.mkdir(full_path)
    os.mkdir(src_path)

    with open(f"{src_path}/main.py", "w") as file:
        file.write(MAIN_TEXT)
        file.close()
    with open(f"{full_path}/.gitignore", "w") as file:
        file.write(".venv\n")
        file.write(".env")
        file.close()

    create_and_activate_venv(f"{full_path}/.venv")

    if open_IDE:
        subprocess.run(["code", full_path])
    return full_path

if __name__ == "__main__":
    try:
        path = create_python_project(input("Enter project name:\n"))
        print(f"project created successfully at {path}")
        
    except Exception as e:
        print(e)
    
