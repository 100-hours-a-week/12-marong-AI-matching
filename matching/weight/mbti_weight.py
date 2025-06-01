from typing import Tuple

# 0: 파랑, 1: 연두, 2: 초록, 3: 노랑, 4: 빨강

class MBTIWeight:
    # MBTI List
    MBTI_TYPES = [
        "INFP", "ENFP", "INFJ", "ENFJ",
        "INTJ", "ENTJ", "INTP", "ENTP",
        "ISFP", "ESFP", "ISTP", "ESTP",
        "ISFJ", "ESFJ", "ISTJ", "ESTJ",
    ]

    # 조합에 따른 점수
    COMPATIBILITY_SCORE = {

    # INFP 행 
    ("INFP", "INFP"): 2,
    ("INFP", "ENFP"): 2,
    ("INFP", "INFJ"): 2,
    ("INFP", "ENFJ"): 0,
    ("INFP", "INTJ"): 0,
    ("INFP", "ENTJ"): 0,
    ("INFP", "INTP"): 2,
    ("INFP", "ENTP"): 2,
    ("INFP", "ISFP"): 4,
    ("INFP", "ESFP"): 4,
    ("INFP", "ISTP"): 4,
    ("INFP", "ESTP"): 4,
    ("INFP", "ISFJ"): 4,
    ("INFP", "ESFJ"): 4,
    ("INFP", "ISTJ"): 4,
    ("INFP", "ESTJ"): 4,

    # 역방향
    ("ENFP", "INFP"): 2,
    ("INFJ", "INFP"): 2,
    ("ENFJ", "INFP"): 0,
    ("INTJ", "INFP"): 0,
    ("ENTJ", "INFP"): 0,
    ("INTP", "INFP"): 2,
    ("ENTP", "INFP"): 2,
    ("ISFP", "INFP"): 4,
    ("ESFP", "INFP"): 4,
    ("ISTP", "INFP"): 4,
    ("ESTP", "INFP"): 4,
    ("ISFJ", "INFP"): 4,
    ("ESFJ", "INFP"): 4,
    ("ISTJ", "INFP"): 4,
    ("ESTJ", "INFP"): 4,

    # ENFP 행
    ("ENFP", "ENFP"): 2,
    ("ENFP", "INFJ"): 0,
    ("ENFP", "ENFJ"): 2,
    ("ENFP", "INTJ"): 0,
    ("ENFP", "ENTJ"): 0,
    ("ENFP", "INTP"): 2,
    ("ENFP", "ENTP"): 2,
    ("ENFP", "ISFP"): 4,
    ("ENFP", "ESFP"): 4,
    ("ENFP", "ISTP"): 4,
    ("ENFP", "ESTP"): 4,
    ("ENFP", "ISFJ"): 4,
    ("ENFP", "ESFJ"): 4,
    ("ENFP", "ISTJ"): 4,
    ("ENFP", "ESTJ"): 4,

    # 역방향
    ("INFJ", "ENFP"): 0,
    ("ENFJ", "ENFP"): 2,
    ("INTJ", "ENFP"): 0,
    ("ENTJ", "ENFP"): 0,
    ("INTP", "ENFP"): 2,
    ("ENTP", "ENFP"): 2,
    ("ISFP", "ENFP"): 4,
    ("ESFP", "ENFP"): 4,
    ("ISTP", "ENFP"): 4,
    ("ESTP", "ENFP"): 4,
    ("ISFJ", "ENFP"): 4,
    ("ESFJ", "ENFP"): 4,
    ("ISTJ", "ENFP"): 4,
    ("ESTJ", "ENFP"): 4,

    # INFJ 행
    ("INFJ", "INFJ"): 2,
    ("INFJ", "ENFJ"): 2,
    ("INFJ", "INTJ"): 2,
    ("INFJ", "ENTJ"): 2,
    ("INFJ", "INTP"): 2,
    ("INFJ", "ENTP"): 0,
    ("INFJ", "ISFP"): 4,
    ("INFJ", "ESFP"): 4,
    ("INFJ", "ISTP"): 4,
    ("INFJ", "ESTP"): 4,
    ("INFJ", "ISFJ"): 4,
    ("INFJ", "ESFJ"): 4,
    ("INFJ", "ISTJ"): 4,
    ("INFJ", "ESTJ"): 4,

    # 역방향
    ("ENFJ", "INFJ"): 2,
    ("INTJ", "INFJ"): 2,
    ("ENTJ", "INFJ"): 2,
    ("INTP", "INFJ"): 2,
    ("ENTP", "INFJ"): 0,
    ("ISFP", "INFJ"): 4,
    ("ESFP", "INFJ"): 4,
    ("ISTP", "INFJ"): 4,
    ("ESTP", "INFJ"): 4,
    ("ISFJ", "INFJ"): 4,
    ("ESFJ", "INFJ"): 4,
    ("ISTJ", "INFJ"): 4,
    ("ESTJ", "INFJ"): 4,

    # ENFJ 행
    ("ENFJ", "ENFJ"): 2,
    ("ENFJ", "INTJ"): 2,
    ("ENFJ", "ENTJ"): 2,
    ("ENFJ", "INTP"): 2,
    ("ENFJ", "ENTP"): 2,
    ("ENFJ", "ISFP"): 4,
    ("ENFJ", "ESFP"): 4,
    ("ENFJ", "ISTP"): 4,
    ("ENFJ", "ESTP"): 4,
    ("ENFJ", "ISFJ"): 4,
    ("ENFJ", "ESFJ"): 4,
    ("ENFJ", "ISTJ"): 4,
    ("ENFJ", "ESTJ"): 4,

    # 역방향
    ("INTJ", "ENFJ"): 2,
    ("ENTJ", "ENFJ"): 2,
    ("INTP", "ENFJ"): 2,
    ("ENTP", "ENFJ"): 2,
    ("ISFP", "ENFJ"): 4,
    ("ESFP", "ENFJ"): 4,
    ("ISTP", "ENFJ"): 4,
    ("ESTP", "ENFJ"): 4,
    ("ISFJ", "ENFJ"): 4,
    ("ESFJ", "ENFJ"): 4,
    ("ISTJ", "ENFJ"): 4,
    ("ESTJ", "ENFJ"): 4,

    # INTJ 행
    ("INTJ", "INTJ"): 2,
    ("INTJ", "ENTJ"): 2,
    ("INTJ", "INTP"): 2,
    ("INTJ", "ENTP"): 2,
    ("INTJ", "ISFP"): 2,
    ("INTJ", "ESFP"): 2,
    ("INTJ", "ISTP"): 2,
    ("INTJ", "ESTP"): 2,
    ("INTJ", "ISFJ"): 3,
    ("INTJ", "ESFJ"): 3,
    ("INTJ", "ISTJ"): 3,
    ("INTJ", "ESTJ"): 3,

    # 역방향
    ("ENTJ", "INTJ"): 2,
    ("INTP", "INTJ"): 2,
    ("ENTP", "INTJ"): 2,
    ("ISFP", "INTJ"): 2,
    ("ESFP", "INTJ"): 2,
    ("ISTP", "INTJ"): 2,
    ("ESTP", "INTJ"): 2,
    ("ISFJ", "INTJ"): 3,
    ("ESFJ", "INTJ"): 3,
    ("ISTJ", "INTJ"): 3,
    ("ESTJ", "INTJ"): 3,

    # ENTJ 행
    ("ENTJ", "ENTJ"): 2,
    ("ENTJ", "INTP"): 2,
    ("ENTJ", "ENTP"): 2,
    ("ENTJ", "ISFP"): 2,
    ("ENTJ", "ESFP"): 2,
    ("ENTJ", "ISTP"): 2,
    ("ENTJ", "ESTP"): 2,
    ("ENTJ", "ISFJ"): 3,
    ("ENTJ", "ESFJ"): 3,
    ("ENTJ", "ISTJ"): 3,
    ("ENTJ", "ESTJ"): 3,

    # 역방향
    ("INTP", "ENTJ"): 2,
    ("ENTP", "ENTJ"): 2,
    ("ISFP", "ENTJ"): 2,
    ("ESFP", "ENTJ"): 2,
    ("ISTP", "ENTJ"): 2,
    ("ESTP", "ENTJ"): 2,
    ("ISFJ", "ENTJ"): 3,
    ("ESFJ", "ENTJ"): 3,
    ("ISTJ", "ENTJ"): 3,
    ("ESTJ", "ENTJ"): 3,

    # INTP 행
    ("INTP", "INTP"): 2,
    ("INTP", "ENTP"): 0,
    ("INTP", "ISFP"): 2,
    ("INTP", "ESFP"): 2,
    ("INTP", "ISTP"): 2,
    ("INTP", "ESTP"): 2,
    ("INTP", "ISFJ"): 2,
    ("INTP", "ESFJ"): 2,
    ("INTP", "ISTJ"): 0,
    ("INTP", "ESTJ"): 0,

    # 역방향
    ("ENTP", "INTP"): 0,
    ("ISFP", "INTP"): 2,
    ("ESFP", "INTP"): 2,
    ("ISTP", "INTP"): 2,
    ("ESTP", "INTP"): 2,
    ("ISFJ", "INTP"): 2,
    ("ESFJ", "INTP"): 2,
    ("ISTJ", "INTP"): 0,
    ("ESTJ", "INTP"): 0,

    # ENTP 행
    ("ENTP", "ENTP"): 2,
    ("ENTP", "ISFP"): 2,
    ("ENTP", "ESFP"): 2,
    ("ENTP", "ISTP"): 2,
    ("ENTP", "ESTP"): 2,
    ("ENTP", "ISFJ"): 3,
    ("ENTP", "ESFJ"): 3,
    ("ENTP", "ISTJ"): 3,
    ("ENTP", "ESTJ"): 3,

    # 역방향
    ("ISFP", "ENTP"): 2,
    ("ESFP", "ENTP"): 2,
    ("ISTP", "ENTP"): 2,
    ("ESTP", "ENTP"): 2,
    ("ISFJ", "ENTP"): 3,
    ("ESFJ", "ENTP"): 3,
    ("ISTJ", "ENTP"): 3,
    ("ESTJ", "ENTP"): 3,

    # ISFP 행
    ("ISFP", "ISFP"): 4,
    ("ISFP", "ESFP"): 4,
    ("ISFP", "ISTP"): 4,
    ("ISFP", "ESTP"): 4,
    ("ISFP", "ISFJ"): 1,
    ("ISFP", "ESFJ"): 1,
    ("ISFP", "ISTJ"): 0,
    ("ISFP", "ESTJ"): 0,

    # 역방향
    ("ESFP", "ISFP"): 4,
    ("ISTP", "ISFP"): 4,
    ("ESTP", "ISFP"): 4,
    ("ISFJ", "ISFP"): 1,
    ("ESFJ", "ISFP"): 1,
    ("ISTJ", "ISFP"): 0,
    ("ESTJ", "ISFP"): 0,

    # ESFP 행
    ("ESFP", "ESFP"): 4,
    ("ESFP", "ISTP"): 4,
    ("ESFP", "ESTP"): 4,
    ("ESFP", "ISFJ"): 1,
    ("ESFP", "ESFJ"): 1,
    ("ESFP", "ISTJ"): 0,
    ("ESFP", "ESTJ"): 0,

    # 역방향
    ("ISTP", "ESFP"): 4,
    ("ESTP", "ESFP"): 4,
    ("ISFJ", "ESFP"): 1,
    ("ESFJ", "ESFP"): 1,
    ("ISTJ", "ESFP"): 0,
    ("ESTJ", "ESFP"): 0,

    # ISTP 행
    ("ISTP", "ISTP"): 4,
    ("ISTP", "ESTP"): 4,
    ("ISTP", "ISFJ"): 0,
    ("ISTP", "ESFJ"): 0,
    ("ISTP", "ISTJ"): 0,
    ("ISTP", "ESTJ"): 0,

    # 역방향
    ("ESTP", "ISTP"): 4,
    ("ISFJ", "ISTP"): 0,
    ("ESFJ", "ISTP"): 0,
    ("ISTJ", "ISTP"): 0,
    ("ESTJ", "ISTP"): 0,

    # ESTP 행
    ("ESTP", "ESTP"): 4,
    ("ESTP", "ISFJ"): 0,
    ("ESTP", "ESFJ"): 0,
    ("ESTP", "ISTJ"): 0,
    ("ESTP", "ESTJ"): 0,

    # 역방향
    ("ISFJ", "ESTP"): 0,
    ("ESFJ", "ESTP"): 0,
    ("ISTJ", "ESTP"): 0,
    ("ESTJ", "ESTP"): 0,

    # ISFJ 행
    ("ISFJ", "ISFJ"): 3,
    ("ISFJ", "ESFJ"): 1,
    ("ISFJ", "ISTJ"): 2,
    ("ISFJ", "ESTJ"): 2,

    # 역방향
    ("ESFJ", "ISFJ"): 1,
    ("ISTJ", "ISFJ"): 2,
    ("ESTJ", "ISFJ"): 2,

    # ESFJ 행
    ("ESFJ", "ESFJ"): 3,
    ("ESFJ", "ISTJ"): 2,
    ("ESFJ", "ESTJ"): 2,

    # 역방향
    ("ISTJ", "ESFJ"): 2,
    ("ESTJ", "ESFJ"): 2,

    # ISTJ 행
    ("ISTJ", "ISTJ"): 3,
    ("ISTJ", "ESTJ"): 2,

    # 역방향
    ("ESTJ", "ISTJ"): 2,

    # ESTJ 행
    ("ESTJ", "ESTJ"): 2,
    }


    def __init__(self, base_cost: int = 100):
        self.base_cost = base_cost


    def _normalize_key(self, mbti1: str, mbti2: str) -> Tuple[str, str]:
        a = mbti1.strip().upper()
        b = mbti2.strip().upper()
        return (a,b)

    def get_compatibility_score(self, mbti1: str, mbti2: str) -> int:
        key = self._normalize_key(mbti1, mbti2)
        # 사전에 없으면 2로 설정
        return self.COMPATIBILITY_SCORE.get(key, 2)


    # 비용 계산
    def get_cost(self, mbti1: str, mbti2: str) -> int:
        score = self.get_compatibility_score(mbti1, mbti2)
        penalty_per_score = 10 
        return self.base_cost + (score * penalty_per_score)