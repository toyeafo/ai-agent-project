import os
import subprocess

def run_python_file(working_directory, file_path):
    # Resolve paths securely
    base_dir = os.path.abspath(working_directory)
    full_path = os.path.abspath(os.path.join(working_directory, file_path))

    # Ensure the file is inside the working directory
    if not full_path.startswith(base_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(full_path):
        return f'Error: File "{file_path}" not found.'
    
    if not full_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        result = subprocess.run(["python", full_path], timeout=30, 
                             capture_output=True, text=True, check=True,
                             )
        if result.returncode != 0:
            return f"Process exited with code {result.returncode}"
        if result is None:
            return f"No output produced."
        return f"STDOUT: {result.stdout} \nSTDERR: {result.stderr}"
    except subprocess.CalledProcessError as e:
        return f'Error: executing python file: {e}'