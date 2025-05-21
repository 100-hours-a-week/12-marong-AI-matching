from db import SessionLocal
from db_models import Users, Manittos, UserGroups
from matcher import ManittoMatcher
from get_week_index import GetWeekIndex
from datetime import datetime
import json

# 날짜 기준 주차 계산
base_date = datetime(2025, 1, 6)
today = datetime.today()
current_week = GetWeekIndex(today, base_date).get()

# DB 세션 열기
session = SessionLocal()

# user_id → group_id 매핑
user_group_map = {
    row.user_id: row.group_id
    for row in session.query(UserGroups.user_id, UserGroups.group_id).all()
}

# group_id → user_id 목록 매핑
group_users = {}
for user_id, group_id in user_group_map.items():
    group_users.setdefault(group_id, []).append(user_id)

# 과거 매칭 정보
previous_matches = {}
matches = session.query(Manittos.manittee_id, Manittos.manitto_id, Manittos.week).all()
for manittee, manitto, week in matches:
    key = frozenset([manittee, manitto])
    if key not in previous_matches or week > previous_matches[key]:
        previous_matches[key] = week

# 매칭 결과 저장용
result = []

# 그룹별 매칭 수행
for group_id, user_ids in group_users.items():
    matcher = ManittoMatcher(user_ids, previous_matches, current_week)
    pairs, excluded = matcher.assign_weighted_pairs()

    for u1, u2 in pairs:
        result.append({
            "week": current_week,
            "user_id": u1,
            "manitto_id": u2,
            "group_id": group_id
        })
        session.add(Manittos(
            group_id=group_id,
            manittee_id=u1,
            manitto_id=u2,
            week=current_week
        ))

    if excluded:
        for u in excluded:
            result.append({
                "week": current_week,
                "user_id": u,
                "manitto_id": None,
                "group_id": group_id
            })

# DB 반영
session.commit()
session.close()

# JSON 출력
print(json.dumps(result, indent=2, ensure_ascii=False))