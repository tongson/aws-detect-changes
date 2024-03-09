
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
    git_init(setup_git_init)
    config = Path(f"{setup_git_init}/.git/config")
    assert config.is_file()
