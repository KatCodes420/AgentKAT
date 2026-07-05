import os
import subprocess


def run_python_file(
    working_directory: str,
    file_path: str,
    args: list[str] | None = None
) -> str:
    try:
        # resolve working directory
        working_dir_abs = os.path.abspath(working_directory)

        # build absolute target path
        absolute_file_path = os.path.normpath(
            os.path.join(working_dir_abs, file_path)
        )

        # security check: stay in workdirectory
        valid_path = (
            os.path.commonpath([working_dir_abs, absolute_file_path]) == working_dir_abs
        )

        if not valid_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        # must exist and be a file
        if not os.path.isfile(absolute_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        # Python file?
        if not absolute_file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        # buildcommand
        command = ["python", absolute_file_path]

        if args:
            command.extend(args)

        # run subprocess
        result = subprocess.run(
            command,
            cwd=working_dir_abs,
            capture_output=True,
            text=True,
            timeout=30,
        )

        output_parts = []

        # checking exit code
        if result.returncode != 0:
            output_parts.append(f"Process exited with code {result.returncode}")

        # hande output
        stdout = result.stdout.strip()
        stderr = result.stderr.strip()

        if not stdout and not stderr and result.returncode == 0:
            output_parts.append("No output produced")

        if stdout:
            output_parts.append(f"STDOUT:\n{stdout}")

        if stderr:
            output_parts.append(f"STDERR:\n{stderr}")

        return "\n".join(output_parts)

    except Exception as e:
        return f"Error: executing Python file: {e}"
        
schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Run a Python file inside the working directory with optional arguments",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to Python file relative to working directory"
                },
                "args": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": "Optional command-line arguments"
                }
            },
            "required": ["file_path"]
        }
    }
}