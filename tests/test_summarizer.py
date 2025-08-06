from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.utils import summarize_text


def test_summarize_text_picks_relevant_sentences():
    text = (
        "Python is great for AI development. "
        "I love writing Python code. "
        "Bananas are yellow. "
        "Python makes tasks easier."
    )
    summary = summarize_text(text, max_sentences=2)
    assert "Python is great for AI development." in summary
    assert "Python makes tasks easier." in summary
    assert "Bananas are yellow." not in summary
    assert summary.count('.') <= 2
