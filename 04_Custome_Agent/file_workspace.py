import os


class WorkspaceManager:
    def __init__(self, workspace_root: str):
        self.root = workspace_root

    def create_file(self, filename: str, content: str) -> str:
        """Creates a file inside the allowed workspace."""
        path = os.path.join(self.root, filename)
        with open(path, "w") as f:
            f.write(content)
        return f"Created {filename} in workspace."
    
    def read_file(self, filename: str) -> str:
        """Read a existing file inside the allowed wrokspace"""
        path = os.path.join(self.root,filename)
        if not os.path.exists(path):
            return f"{filename} does not exist."
        with open(path) as file:
            content = file.read()
        return content

    def update_file(self, filename: str, content: str) -> str:
        """Update a existing file inside the allowed workspace."""
        path = os.path.join(self.root, filename)
        if not os.path.exists(path):
            return f"{filename} does not exist."
        with open(path, "w") as f:
            f.write(content)
        return f"Updated {filename} in workspace."

    def delete_file(self,filename: str) -> str:
        """Delete a existing file inside the allowed workspace"""
        path = os.path.join(self.root,filename)
        if os.path.exists(path):
            os.remove(path)
            return f"{filename} has been deleted."
        else:
            return f"{filename} does not exist."

# creating workspace manager instance with the root directory
workspace = WorkspaceManager(workspace_root="C:/Users/AKASH VERMA/Ai_Engineering_Workspace/Ai_Engineering_Concepts/04_Custome_Agent")

