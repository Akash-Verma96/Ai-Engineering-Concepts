from file_workspace import workspace
from terminal_workspace import terminal, approve_command

create_file_schema = {
  "type": "function",
  "function": {
    "name": "create_file",
    "description": "Creates a new file inside the allowed workspace directory with the specified text content.",
    "parameters": {
      "type": "object",
      "properties": {
        "filename": {
          "type": "string",
          "description": "The name or relative path of the file to create (e.g., 'script.py' or 'data/config.json')."
        },
        "content": {
          "type": "string",
          "description": "The full text content to write into the file."
        }
      },
      "required": ["filename", "content"],
      "additionalProperties": False
    }
  }
}


read_file_schema = {
  "type": "function",
  "function": {
    "name": "read_file",
    "description": "Read a existing file inside the allowed workspace directory with the specified text content.",
    "parameters": {
      "type": "object",
      "properties": {
        "filename": {
          "type": "string",
          "description": "The name or relative path of the file to read (e.g., 'script.py' or 'data/config.json')."
        }
      },
      "required": ["filename"],
      "additionalProperties": False
    }
  }
}

update_file_schema = {
  "type": "function",
  "function": {
    "name": "update_file",
    "description": "Update an existing file inside the allowed workspace directory with the specified text content.",
    "parameters": {
      "type": "object",
      "properties": {
        "filename": {
          "type": "string",
          "description": "The name or relative path of the file to read (e.g., 'script.py' or 'data/config.json')."
        },
        "content": {
                  "type": "string",
                  "description": "The full text content to write into the file."
        }
      },
      "required": ["filename", "content"],
      "additionalProperties": False
    }
  }
}

delete_file_schema = {
  "type": "function",
  "function": {
    "name": "delete_file",
    "description": "Delete an existing file inside the allowed workspace directory.",
    "parameters": {
      "type": "object",
      "properties": {
        "filename": {
          "type": "string",
          "description": "The name or relative path of the file to delete (e.g., 'script.py' or 'data/config.json')."
        }
      },
      "required": ["filename"],
      "additionalProperties": False
    }
  }
}


TOOLS = {
    "create_file": workspace.create_file,
    "read_file": workspace.read_file,
    "update_file": workspace.update_file,
    "delete_file": workspace.delete_file,
    "approve_command": approve_command
}