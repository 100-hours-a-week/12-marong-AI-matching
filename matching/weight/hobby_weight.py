from typing import Set

class HobbyWeight:
    def __init__(self, discount_rate: float = 0.8):
        self.discount_rate = discount_rate

    def parse_hobby_string(self, hobby_str: str) -> Set[str]:
        if not hobby_str:
            return set()
        
        hobby_list = [h for h in hobby_str.split(",") if h != ""]
        return set(hobby_list)

    def apply_discount(
        self,
        base_cost: int, 
        hobbies_u: Set[str],
        hobbies_v: Set[str]
    ) -> int:
        
        if hobbies_u & hobbies_v:
            return int(base_cost * self.discount_rate)
        return base_cost