
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
    git_init(cwd)
    config = Path(f"{cwd}/.git/config")
    assert config.is_file()

def test_git_status(setup_git_init):
    cwd = setup_git_init
    git_init(cwd)
    write_file = open(f"{cwd}/x", "w")
    print(f"test", file=write_file)
    x = git_status(cwd)
    assert "?? x\n" == x

def test_git_commit(setup_git_init):
    cwd = setup_git_init
    git_init(cwd)
    write_file = open(f"{cwd}/x", "w")
    print(f"test", file=write_file)
    git_commit(cwd, "xxx")
    run = subprocess.run(["git", "log", "-1", "HEAD", "--pretty=format:%B"], cwd=cwd, text=True, check=True, capture_output=True)
    assert "xxx\n" == run.stdout
