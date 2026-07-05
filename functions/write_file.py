import os


def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        # resolve working directory
        working_dir_abs = os.path.abspath(working_directory)

        # build target path
        target_path = os.path.normpath(
            os.path.join(working_dir_abs, file_path)
        )

        # Security check in work directory
        valid_path = (
            os.path.commonpath([working_dir_abs, target_path]) == working_dir_abs
        )

        if not valid_path:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        # If target exists and is a directory to error
        if os.path.isdir(target_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        # parent directories must exist
        parent_dir = os.path.dirname(target_path)
        os.makedirs(parent_dir, exist_ok=True)

        # Write file
        with open(target_path, "w", encoding="utf-8") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {e}"
        
schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Write or overwrite a file in the working directory",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file relative to working directory"
                },
                "content": {
                    "type": "string",
                    "description": "Content to write into the file"
                }
            },
            "required": ["file_path", "content"]
        }
    }
}