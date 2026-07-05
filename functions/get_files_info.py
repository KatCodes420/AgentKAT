import os


def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)

        target_dir = os.path.normpath(
            os.path.join(working_dir_abs, directory)
        )

        valid_target_dir = (
            os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        )

        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        items = os.listdir(target_dir)

        lines = []
        for item in items:
            item_path = os.path.join(target_dir, item)

            try:
                is_dir = os.path.isdir(item_path)
                size = os.path.getsize(item_path)

                lines.append(
                    f"- {item}: file_size={size} bytes, is_dir={is_dir}"
                )
            except Exception as e:
                return f"Error: {e}"

        result = f"Result for '{directory}' directory:\n"
        result += "\n".join(lines)
        return result

    except Exception as e:
        return f"Error: {e}"


schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "List files in a directory within the project. This tool only works inside the working directory.",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory to list files from. Use '.' for the project root (current working directory). Do NOT use '/' because it refers to the system root and is not allowed."
                }
            },
            "required": ["directory"]
        }
    }
}