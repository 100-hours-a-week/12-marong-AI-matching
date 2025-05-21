import random
from typing import List, Dict, Tuple, FrozenSet

class ManittoMatcher:
    def __init__(
            self,
            user_ids: List[int],
            previous_matches: Dict[FrozenSet[int], int],
            current_week: int
    ):
        self.user_ids = user_ids
        self.previous_matchers = previous_matches
        self.current_week = current_week

    
    def assign_weighted_pairs(self) -> Tuple[List[Tuple[int, int]], List[int]]:
        # 사용자 리스트 랜덤 셔플
        users = self.user_ids[:]
        random.shuffle(users)

        # 순환 구조
        pairs: List[Tuple[int, int]] = [
            (users[i], users[(i + 1) % len(users)])
            for i in range(len(users))
        ]

        # 제외 대상 없음
        excluded: List[int] = []
        return pairs, excluded