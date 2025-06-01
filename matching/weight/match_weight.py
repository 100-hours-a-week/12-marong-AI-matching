from typing import Dict, FrozenSet


class MatchWeight:
    def __init__(self, previous_matches: Dict[FrozenSet[int], int], current_week: int):
        self.previous_matches = previous_matches 
        self.current_week = current_week 

    # 가중치 계산
    def edge_cost(self, u_from: int, u_to: int, scale: int = 100) -> int:
        key = frozenset([u_from, u_to])
        history = self.previous_matches.get(key, [])
        if history:
            sorted_history = sorted(history)
            weighted_sum = sum((self.current_week - week)* 5 * (idx + 1)
                               for idx, week in enumerate(sorted_history))
            cost = weighted_sum * scale
            return cost
        else:
            return scale