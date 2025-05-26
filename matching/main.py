import random
from typing import Dict, List, FrozenSet
from db import SessionLocal
from db_models import Manittos, UserGroups
from matcher import ORToolsMatcher
from get_week_index import GetWeekIndex
from datetime import datetime


# 날짜 기준 추가 게산
base_date = datetime(2025, 1, 6)
today = datetime.today()
current_week = GetWeekIndex(today, base_date).get()

# DB 세션 열기
session = SessionLocal()

# user_id -> groutp_id 매핑
user_group_map = {
    r.user_id: r.group_id
    for r in session.query(UserGroups.user_id, UserGroups.group_id)
}

# group_id -> user_id 목록 매핑
group_users = {}
for uid, gid in user_group_map.items():
    group_users.setdefault(gid, []).append(uid)

# 과거 매칭 정보 로드
previous_matches: Dict[FrozenSet[int], List[int]] = {}
matches = session.query(Manittos.manittee_id, Manittos.manitto_id, Manittos.week).all()
for manittee, manitto, week in matches:
    if week < current_week:
        key = frozenset([manittee, manitto])
        previous_matches.setdefault(key, []).append(week)


# 매칭 결과 저장
result = []

# 그룹별 매칭 수행
for group_id, users in group_users.items():
    # 과거 매칭 기반 비용 행렬 생성
    N = len(users)
    cost_matrix = [
        [99999 if i == j else random.randint(1, 100) for j in range(N)]
        for i in range(N)
    ]

    # 매칭 실행
    start_user = users[0]  # 시작 노드를 첫 번째 사용자로 고정
    matcher = ORToolsMatcher(previous_matches, current_week)
    route, total_cost = matcher.solve_route(users, start_user)

    if not route:
        print(f"[Group {group_id}] 매칭 실패: 유효한 경로를 찾을 수 없습니다.")
        continue

    # 결과 DB 저장 및 출력
    for u_from, u_to in route:
        session.add(
            Manittos(
                group_id=group_id,
                manittee_id=u_from,
                manitto_id=u_to,
                week=current_week
            )
        )
        cost_uv = matcher.calculator.edge_cost(u_from, u_to)
        print(f"[Group {group_id}] {u_from} -> {u_to}, 비용={cost_uv}")

# DB 반영 및 세션 종료
session.commit()
session.close()