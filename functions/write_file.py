import os

def write_file(working_directory, file_path, content):
    try:
        # Resolve paths securely
        basedir = os.path.abspath(working_directory)
        full_path = os.path.abspath(os.path.join(working_directory, file_path))

        # Ensure the file is inside the working directory
        if not full_path.startswith(basedir):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.exists(os.path.dirname(full_path)):
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
        
        with open(full_path, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except OSError as error:
        return f"Error: {error}"