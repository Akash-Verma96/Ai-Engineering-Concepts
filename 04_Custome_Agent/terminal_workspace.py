import platform
import subprocess


class TerminalWorkspace:

    def launch_terminal(self, command: str) -> str:
        """
            Spawns a new GUI terminal window and runs the specified command inside it.
            Returns a status message to feed back to the LLM.
        """
        current_os = platform.system()
    
        try:
            if current_os == "Windows":
                # /K keeps the command prompt window open after the command runs
                subprocess.Popen(f'start cmd.exe /K "{command}"', shell=True)
            else:
                return f"Error: Unsupported operating system: {current_os}"
                
            return f"Successfully opened a new terminal window and initiated command: '{command}'"
            
        except Exception as e:
            return f"Failed to open terminal execution environment. Error: {str(e)}"


terminal = TerminalWorkspace()

def approve_command(tool_name: str, arguments: dict) -> str:
     """
    Orchestration wrapper that handles Human-In-The-Loop validation before tool run.
    """

     if tool_name == "launch_terminal":

        command_to_run = arguments.get("command","")

        print("\n" + "="*50)
        print("⚠️  AGENT REQUESTING TERMINAL ACCESS")
        print(f"👉 Proposed Command: {command_to_run}")
        print("="*50)

        user_approval = input("Approve execution? (y/n): ").strip().lower()

        if user_approval == 'y':
            return terminal.launch_terminal(command_to_run)
        else:
            print("❌ Execution rejected by user.")
            return "Error: The user declined authorization to run this command. Modify your approach or ask for permission."
        
     return "Error: Unknown tool invoked."

