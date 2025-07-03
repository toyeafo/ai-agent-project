import os
from google.genai import types
from config import MAX_CHARS

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=f"Reads files in the specified directory and prints the first {MAX_CHARS} characters, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to read from, relative to the working directory. If empty, prints out file is empty.",
            ),
        },
        required=["file_path"],
    ),
)

def get_file_content(working_directory, file_path):
    try:
        # Resolve paths securely
        base_dir = os.path.abspath(working_directory)
        full_path = os.path.abspath(os.path.join(working_directory, file_path))

        # Ensure the file is inside the working directory
        if not full_path.startswith(base_dir):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(full_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(full_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if len(file_content_string) < len(f.read()):
                file_content_string += f"[...File '{file_path}' truncated at 10000 characters]"
            return file_content_string if file_content_string else "File is empty."
    except OSError as error:
        return f"Error: {error}"