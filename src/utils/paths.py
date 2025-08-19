from os.path import abspath
from pathlib import Path

class Paths:
    def __init__(self) -> None:
        pass

    def get_project_root(self) -> Path:
        return Path(__file__).parent.parent.parent

    def get_script_dir(self) -> Path:
        return Path(abspath(__file__)).parent