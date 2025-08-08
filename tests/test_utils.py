import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from utils import debug_log, ensure_dir


def test_debug_log(capsys):
    debug_log("message")
    captured = capsys.readouterr()
    assert captured.out.strip() == "DEBUG: message"


def test_ensure_dir(tmp_path):
    target = tmp_path / "new_dir"
    assert not target.exists()
    ensure_dir(target)
    assert target.exists() and target.is_dir()

