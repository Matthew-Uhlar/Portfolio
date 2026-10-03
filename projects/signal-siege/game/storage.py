import json
from pathlib import Path


SAVE_PATH = Path(__file__).resolve().parent.parent / "highscore.json"


def load_high_score() -> int:
    try:
        data = json.loads(SAVE_PATH.read_text(encoding="utf-8"))
        return int(data.get("high_score", 0))
    except (FileNotFoundError, ValueError, json.JSONDecodeError):
        return 0


def save_high_score(score: int) -> None:
    SAVE_PATH.write_text(
        json.dumps({"high_score": score}, indent=2),
        encoding="utf-8",
    )
