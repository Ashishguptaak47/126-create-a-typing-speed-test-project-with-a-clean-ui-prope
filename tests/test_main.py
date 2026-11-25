import os
import json
import pytest
from src.engine import TypingEngine

@pytest.fixture
def engine(tmp_path):
    passages_file = tmp_path / "passages.json"
    history_file = tmp_path / "history.json"
    
    passages_data = {
        "easy": ["The quick brown fox."],
        "medium": ["Testing typing engine performance."],
        "hard": ["Complex concurrency architecture pattern."]
    }
    passages_file.write_text(json.dumps(passages_data), encoding="utf-8")
    return TypingEngine(passages_file=str(passages_file), history_file=str(history_file))

def test_engine_initialization(engine):
    assert engine.is_active is False
    assert engine.target_text == ""

def test_start_test(engine):
    engine.start_test(difficulty="easy", duration=15)
    assert engine.is_active is True
    assert engine.difficulty == "easy"
    assert engine.duration == 15
    assert engine.target_text == "The quick brown fox."

def test_evaluate_perfect_typing(engine):
    engine.start_test(difficulty="easy", duration=30)
    sample_input = "The quick"
    metrics = engine.evaluate(sample_input)
    
    assert metrics["accuracy"] == 100.0
    assert metrics["correct_chars"] == len(sample_input)
    assert metrics["total_typed"] == len(sample_input)

def test_evaluate_with_errors(engine):
    engine.start_test(difficulty="easy", duration=30)
    sample_input = "The qxick"  # 1 mistake ('x' instead of 'u')
    metrics = engine.evaluate(sample_input)
    
    assert metrics["correct_chars"] == 8
    assert metrics["total_typed"] == 9
    assert metrics["accuracy"] == round((8 / 9) * 100.0, 1)

def test_stop_test_and_history(engine):
    engine.start_test(difficulty="medium", duration=30)
    user_input = "Testing typing"
    stats = engine.stop_test(user_input)
    
    assert engine.is_active is False
    assert stats is not None
    assert stats["correct_chars"] == len(user_input)
    
    history = engine.get_history()
    assert len(history) == 1
    assert history[0]["difficulty"] == "medium"
    assert history[0]["net_wpm"] == stats["net_wpm"]
