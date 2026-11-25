import json
import os
import random
import time

class TypingEngine:
    """Handles speed calculations, passage selection, and session history management."""
    def __init__(self, passages_file="data/passages.json", history_file="data/history.json"):
        self.passages_file = passages_file
        self.history_file = history_file
        self.passages = self._load_passages()
        self.target_text = ""
        self.start_time = None
        self.end_time = None
        self.duration = 30
        self.is_active = False
        self.difficulty = "medium"

    def _load_passages(self):
        if os.path.exists(self.passages_file):
            try:
                with open(self.passages_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {
            "easy": ["The quick brown fox jumps over the lazy dog."],
            "medium": ["Python is an interpreted high-level programming language."],
            "hard": ["Asynchronous execution handles non-blocking high-throughput IO operations."]
        }

    def start_test(self, difficulty="medium", duration=30):
        self.difficulty = difficulty if difficulty in self.passages else "medium"
        self.duration = duration
        pool = self.passages.get(self.difficulty, [])
        self.target_text = random.choice(pool) if pool else "Default typing passage."
        self.start_time = time.time()
        self.end_time = None
        self.is_active = True

    def evaluate(self, user_text):
        """Calculates current typing metrics."""
        if not self.start_time:
            return {
                "wpm": 0.0, "net_wpm": 0.0, "cpm": 0.0,
                "accuracy": 100.0, "correct_chars": 0,
                "total_typed": 0, "elapsed": 0.0, "progress": 0.0
            }

        current_time = self.end_time if self.end_time else time.time()
        elapsed = max(current_time - self.start_time, 0.001)
        total_typed = len(user_text)
        correct_chars = 0

        for i, char in enumerate(user_text):
            if i < len(self.target_text) and char == self.target_text[i]:
                correct_chars += 1

        minutes = elapsed / 60.0
        gross_wpm = round((total_typed / 5.0) / minutes, 1) if minutes > 0 else 0.0
        net_wpm = round((correct_chars / 5.0) / minutes, 1) if minutes > 0 else 0.0
        cpm = round(correct_chars / minutes, 1) if minutes > 0 else 0.0
        accuracy = round((correct_chars / max(total_typed, 1)) * 100.0, 1)
        progress = min(round((total_typed / max(len(self.target_text), 1)) * 100.0, 1), 100.0)

        return {
            "wpm": gross_wpm,
            "net_wpm": net_wpm,
            "cpm": cpm,
            "accuracy": accuracy,
            "correct_chars": correct_chars,
            "total_typed": total_typed,
            "elapsed": round(elapsed, 1),
            "progress": progress
        }

    def stop_test(self, user_text):
        if not self.is_active:
            return None
        self.end_time = time.time()
        self.is_active = False
        stats = self.evaluate(user_text)
        self._save_history(stats)
        return stats

    def _save_history(self, stats):
        history = self.get_history()
        entry = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "difficulty": self.difficulty,
            "duration": self.duration,
            "net_wpm": stats["net_wpm"],
            "accuracy": stats["accuracy"],
            "cpm": stats["cpm"]
        }
        history.append(entry)
        os.makedirs(os.path.dirname(self.history_file), exist_ok=True)
        try:
            with open(self.history_file, "w", encoding="utf-8") as f:
                json.dump(history, f, indent=2)
        except IOError:
            pass

    def get_history(self):
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return []
        return []
