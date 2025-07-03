import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

def get_files_info(working_directory, directory=None):
    try:
        # Resolve paths securely
        base_dir = os.path.abspath(working_directory)
        target = directory or '.'
        full_path = os.path.abspath(os.path.join(working_directory, target))

        # Ensure the target is inside the working directory
        if not full_path.startswith(base_dir):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        # Check if path is a directory
        if not os.path.isdir(full_path):
            return f'Error: "{directory}" is not a directory'

        # Gather file info
        response = []
        for entry in os.listdir(full_path):
            entry_path = os.path.join(full_path, entry)
            size = os.path.getsize(entry_path)
            is_dir = os.path.isdir(entry_path)
            response.append(f"- {entry}: file_size={size} bytes, is_dir={is_dir}\n")

        return "".join(response)

    except OSError as error:
        return f"Error: {error}"