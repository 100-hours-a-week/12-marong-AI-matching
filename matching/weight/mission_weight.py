from typing import Dict, List

class MissionWeight:
    def __init__(self, previous_missions: Dict[int, List[int]], current_week: int):
        self.previous_missions = previous_missions
        self.current_week = current_week


    def edge_cost(self, u_from: int, u_to: int, scale: int = 100) -> int:
        # 두 유저의 이력(history) 가져오기
        history_from: List[int] = self.previous_missions.get(u_from, [])
        history_to:   List[int] = self.previous_missions.get(u_to, [])
        # print(len(history_from), len(history_to))


        # 얼마나 최근에 미션을 수행했는지
        def calc_recency(user_history: List[int]) -> float:
            score = 0.0
            for week in user_history:
                delta = self.current_week - week
                if delta >= 0:
                    score += 1.0 / (delta + 1) # delta를 분모로 두어서 현재에 가까울수록 커짐
            return score

        recency_from = calc_recency(history_from)
        recency_to   = calc_recency(history_to)

        # 수행 미션 개수
        count_from = len(history_from)
        count_to   = len(history_to)

        # 최근 수행 가중치 + 수행 횟수
        # 미션 많이 수행할수록, 더 최근에 수행할수록 비용 낮아짐
        combined_score = (recency_from + count_from) + (recency_to + count_to)

        # 비용 계산
        # 둘 다 미션 이력이 없는 경우
        if combined_score == 0:
            return scale

        cost = int(scale / (1 + combined_score))
        return cost