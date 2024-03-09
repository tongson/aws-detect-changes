
import pytest
import shutil
import tempfile
from pathlib import Path
from aws_detect_changes import *

@pytest.fixture
def setup_git_init():
    cwd = tempfile.mkdtemp()
    yield cwd
    shutil.rmtree(cwd)

def test_git_init(setup_git_init):
    cwd = setup_git_init
    git_init(setup_git_init)
    config = Path(f"{cwd}/.git/config")
    assert config.is_file()

def test_git_status(setup_git_init):
    cwd = setup_git_init
    git_init(cwd)
    write_file = open(f"{cwd}/x", "w")
    print(f"test", file=write_file)
    x = git_status(cwd)
    assert "?? x\n" == x
