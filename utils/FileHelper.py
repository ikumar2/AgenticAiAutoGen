from pathlib import Path
import os

def get_project_path (*subpaths):
    """ Returns an absolute path based on the project root.
    works in Jenkins and local environment

    :param subpaths: Optional subdirectories or file names.
    :return: Absolute Path Object.
    """
    # if Jenkins sets WORKSPACE, use it;otherwise use current working directory.
    project_root = Path(os.getenv("WORKSPACE", Path.cwd()))
    return project_root.joinpath(*subpaths)

get_project_path()
