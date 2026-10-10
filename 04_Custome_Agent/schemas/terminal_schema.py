launch_terminal_schema = {
  "type": "function",
  "function": {
    "name": "launch_terminal",
    "description": "Opens a brand new visible operating system terminal window and executes the user's requested command inside it. Use this whenever the user wants to visually monitor scripts, start interactive CLI tools, or keep a process running separately.",
    "parameters": {
      "type": "object",
      "properties": {
        "command": {
          "type": "string",
          "description": "The complete terminal/shell command string to execute (e.g., 'python script.py', 'npm start', 'ping 8.8.8.8')."
        }
      },
      "required": ["command"]
    }
  }
}

approve_command_to_launch_terminal = {
     "type": "function",
      "function": {
        "name": "approve_command",
        "description": "Asks user to approve the suggested command to run in terminal.",
        "parameters": {
          "type": "object",
          "properties": {
            "tool_name": {
              "type": "string",
              "description": "The name of the tool intended for execution (e.g., 'launch_terminal'"
            },
            "arguments":{
                "type": "object",
                "description": "A key-value dictionary containing the parameters required by the target tool.",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "The shell or terminal command string to be executed if tool_name is 'launch_terminal'."
                    }
                },
                "required": ["command"]
            }
          },
          "required": ["tool_name","arguments"]
        }
      }
}
