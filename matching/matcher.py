import random
from typing import List, Tuple, Dict, FrozenSet
from ortools.constraint_solver import routing_enums_pb2, pywrapcp
from match_weight import MatchCostCalculator


class ORToolsMatcher:
    def __init__(
        self,
        previous_matches: Dict[FrozenSet[int], int],
        current_week: int
    ):
        self.calculator = MatchCostCalculator(previous_matches, current_week)

    def solve_route(
        self,
        user_ids: List[int],  # 실제 사용자 ID 리스트
        start_node: int, # 시작할 사용자 ID
        time_limit: int = 5 # 탐색 시간 제한
    ) -> Tuple[List[Tuple[int, int]], int]:
        if len(user_ids) <=2:
            print("매칭을 진행할 수 없습니다")
            return [], 0
       

        # 비용 행렬 생성
        N = len(user_ids)
        cost_matrix = [[0] * N for _ in range(N)]
        for i, u in enumerate(user_ids):
            for j, v in enumerate(user_ids):
                if u == v:
                    cost_matrix[i][j] = 99999 # 정방행렬 방지
                else:
                    cost_matrix[i][j] = self.calculator.edge_cost(u, v)

        start_index = user_ids.index(start_node)
        manager = pywrapcp.RoutingIndexManager(N, 1, start_index)
        routing = pywrapcp.RoutingModel(manager)

        # 비용 콜백
        def cost_callback(from_index, to_index):
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return cost_matrix[from_node][to_node]

        transit_index = routing.RegisterTransitCallback(cost_callback)
        routing.SetArcCostEvaluatorOfAllVehicles(transit_index)

        # 탐색 파라미터 설정
        search_params = pywrapcp.DefaultRoutingSearchParameters()
        search_params.first_solution_strategy = (
            routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
        )
        search_params.local_search_metaheuristic = (
            routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
        )
        search_params.time_limit.seconds = time_limit
        search_params.log_search = False

        # 최적화 실행
        solution = routing.SolveWithParameters(search_params)
        if not solution:
            return [], 0

        # 결과 추출
        index = routing.Start(0)
        route: List[Tuple[int, int]] = []
        total_cost = 0
        while not routing.IsEnd(index):
            from_idx = manager.IndexToNode(index)
            next_idx = solution.Value(routing.NextVar(index))
            to_idx = manager.IndexToNode(next_idx)

            route.append((user_ids[from_idx], user_ids[to_idx]))
            total_cost += routing.GetArcCostForVehicle(index, next_idx, 0)
            index = next_idx

        return route, total_cost