from typing import Dict, Any


class AbstractionFeedback:
    def __init__(self):
        self.feedback_store: Dict[str, Dict[str, Any]] = {}

    def add_feedback(
        self, code_id: str, abstraction: str, rating: int, correction: str = None
    ) -> None:
        self.feedback_store[code_id] = {
            "abstraction": abstraction,
            "rating": rating,
            "correction": correction,
        }

    def get_feedback(self, code_id: str) -> Dict[str, Any]:
        return self.feedback_store.get(code_id, None)
