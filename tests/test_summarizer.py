from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from chat_summarizer import summarize_text


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


def test_summarize_text_empty_string():
    assert summarize_text("") == ""


def test_summarize_text_no_stopwords():
    text = "Bright sun shines. Green grass grows."
    summary = summarize_text(text, max_sentences=1)
    assert summary == "Bright sun shines."


def test_summarize_text_only_stopwords():
    text = "And the a. The and the."
    summary = summarize_text(text)
    assert summary == "And the a."


def test_summarize_text_max_sentences_zero():
    text = "First sentence. Second sentence."
    summary = summarize_text(text, max_sentences=0)
    assert summary == ""


def test_summarize_text_max_sentences_exceeds():
    text = "First sentence. Second sentence."
    summary = summarize_text(text, max_sentences=5)
    assert summary == "First sentence. Second sentence."
