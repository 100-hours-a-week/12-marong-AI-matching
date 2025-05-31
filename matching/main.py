import random
from typing import Dict, List, FrozenSet, Set
from db.db import SessionLocal
from db.db_models import Manittos, UserGroups, SurveyHobby
from core.matcher import ORToolsMatcher
from core.get_week_index import GetWeekIndex
from datetime import datetime
from weight.hobby_weight import HobbyWeight


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
group_users: Dict[int, List[int]] = {}
for record in session.query(UserGroups.user_id, UserGroups.group_id):
    uid = record.user_id
    gid = record.group_id
    group_users.setdefault(gid, []).append(uid)

hobby_weight = HobbyWeight()

user_hobbies: Dict[int, Set[str]] = {}
for uid, hobby_str in session.query(SurveyHobby.user_id, SurveyHobby.hobby_name).all():
    parsed_set = hobby_weight.parse_hobby_string(hobby_str)
    user_hobbies.setdefault(uid, set()).update(parsed_set)


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
    matcher = ORToolsMatcher(previous_matches, current_week, user_hobbies)

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

        hobbies_from = user_hobbies.get(u_from, set())
        hobbies_to = user_hobbies.get(u_to, set())
        hobbies_from_str = ", ".join(hobbies_from) if hobbies_from else "없음"
        hobbies_to_str = ", ".join(hobbies_to) if hobbies_to else "없음"

        print(
            f"[Group {group_id}] {u_from} -> {u_to}, 비용={cost_uv}"
            f"{u_from} (취미: {hobbies_from_str}) ->"
            f"{u_to} (취미: {hobbies_to_str})")

# DB 반영 및 세션 종료
session.commit()
session.close()