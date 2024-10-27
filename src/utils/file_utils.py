from pathlib import Path


@staticmethod
def get_project_root(app_dir="/src") -> str:
    """
    Finds project root by looking for common project files/directories (ex .git, pyproject.toml,...)
    """
    current = Path.cwd()
    while current != current.parent:
        if any((current / marker).exists() for marker in [
            '.git',
            'pyproject.toml',
        ]):
            return str(current) + app_dir

        current = current.parent

    raise FileNotFoundError("Project root not found")
