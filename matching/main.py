import random
from typing import Dict, List, FrozenSet, Set
from db.db import SessionLocal
from db.db_models import Manittos, UserGroups, SurveyHobby, UserMissions, SurveyMBTI
from core.matcher import ORToolsMatcher
from core.get_week_index import GetWeekIndex
from datetime import datetime
from weight.hobby_weight import HobbyWeight
from weight.mbti_weight import MBTIWeight
from db.chromadb_client import get_chroma_client, get_user_latest_collection


# 날짜 기준 추가 게산
base_date = datetime(2025, 1, 6)
today = datetime.today()
current_week = GetWeekIndex(today, base_date).get()

# DB 세션 열기
session = SessionLocal()

# group_id -> user_id 목록 매핑
group_users: Dict[int, List[int]] = {}
for record in session.query(UserGroups.user_id, UserGroups.group_id):
    uid = record.user_id
    gid = record.group_id
    group_users.setdefault(gid, []).append(uid)

# 사용자별 취미 로드
hobby_weight = HobbyWeight()
user_hobbies: Dict[int, Set[str]] = {}
for uid, hobby_str in session.query(SurveyHobby.user_id, SurveyHobby.hobby_name).all():
    parsed_set = hobby_weight.parse_hobby_string(hobby_str)
    user_hobbies.setdefault(uid, set()).update(parsed_set)

# ChromaDB에서 MBTI 로드
get_chroma_client()
user_latest_col = get_user_latest_collection()

# 사용자별 MBTI 로드
user_mbti: Dict[int, str] = {}
user_ids = [r.user_id for r in session.query(UserGroups.user_id).distinct()]

for uid in user_ids:
    rec = user_latest_col.get(where={"user_id": int(uid)}, limit=1, include=["metadatas"])
    if rec.get("ids"):
        meta = rec["metadatas"][0]
        ei, sn, tf, jp = meta["ei_score"], meta["sn_score"], meta["tf_score"], meta["jp_score"]
    else:
        row = (
            session.query(SurveyMBTI.ei_score, SurveyMBTI.sn_score,
                          SurveyMBTI.tf_score, SurveyMBTI.jp_score)
            .filter(SurveyMBTI.user_id == uid)
            .order_by(SurveyMBTI.created_at.desc())
            .first()
        )
        if not row:
            continue
        ei, sn, tf, jp = row.ei_score, row.sn_score, row.tf_score, row.jp_score

    mbti = (
        ("E" if ei >= 50 else "I") +
        ("N" if sn >= 50 else "S") +
        ("F" if tf >= 50 else "T") +
        ("P" if jp >= 50 else "J")
    )
    user_mbti[uid] = mbti


# 과거 매칭 이력 로드
previous_matches: Dict[FrozenSet[int], List[int]] = {}
matches = session.query(Manittos.manittee_id, Manittos.manitto_id, Manittos.week).all()
for manittee, manitto, week in matches:
    if week < current_week:
        key = frozenset([manittee, manitto])
        previous_matches.setdefault(key, []).append(week)

# 과거 미션 이력 로드
previous_missions: Dict[int, List[int]] = {}
mission_rows = (
    session.query(UserMissions.user_id, UserMissions.week)
    .filter(
        UserMissions.week <= current_week
    )
    .all()
)

for uid, week in mission_rows:
    previous_missions.setdefault(uid, []).append(week)


# 매칭 결과 저장
result = []

# 그룹별 매칭 수행
for group_id, users in group_users.items():
    # 해당 주차에 이미 매칭된 유저 조회
    matched_user_ids = set(
        uid for uid, in session.query(Manittos.manittee_id)
        .filter(Manittos.group_id == group_id, Manittos.week == current_week)
        .all()
    )

    # 매칭 대상 유저 필터링
    valid_users = [uid for uid in users if uid not in matched_user_ids]

    if len(valid_users) < 2:
        print(f"[Group {group_id}] 매칭할 수 있는 유저가 부족합니다.")
        continue


    # 매칭 실행
    start_user = valid_users[0]  # 시작 노드를 첫 번째 사용자로 고정
    matcher = ORToolsMatcher(previous_matches, current_week, user_hobbies, previous_missions, user_mbti)

    route, total_cost = matcher.solve_route(valid_users, start_user, group_id)

    if not route:
        print(f"[Group {group_id}] 매칭 실패: 유효한 경로를 찾을 수 없습니다.")
        continue

    print(f"[Group {group_id}] 최종 매칭 결과 (총 비용 = {total_cost}):")
    for u_from, u_to in route:
        print(f"{u_from} -> {u_to}")

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

# DB 반영 및 세션 종료
session.commit()
session.close()