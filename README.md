# 📍 marong-matching
<img width="800" alt="스크린샷 2025-06-01 오전 5 04 20" src="https://github.com/user-attachments/assets/db61d246-992a-4e7f-95c6-ada4e0915182" />



# 📍 Overview

- 프로젝트 이름: Marong
- 프로젝트 설명: 마니또 기반 SNS 서비스

## 📍 파일 구조
```
matching/
├── __pycache__/  
├── core/  
│   ├──  get_week_index.py  # 주차 계산
│   └── matcher.py  # 매칭
├── db/  
│   ├── __pycache__/  
│   ├── db_models.py  # 관계 세팅
│   └── db.py  #DB 연결
├── weight/ 
│   ├── __pycache__/  
│   ├── hobby_weight.py  # 취미 가중치 부여
│   ├── mission_weight.py  # 최근 미션 이력 가중치 부여
│   ├── mbti_weight.py  # mbti 가중치 부여
│   └── match_weight.py  # 과거 매칭 기록 가중치 부여
├── .gitignore  
├── main.py  # 실행파일
├── requirements.txt  
└── .env  
```
---


## 📍 weight
### ✔ match_weight: 과거 매칭 기록

```
def edge_cost(self, u_from: int, u_to: int, scale: int = 50) -> int:
        key = frozenset([u_from, u_to])
        history = self.previous_matches.get(key, [])
        if history:
            sorted_history = sorted(history)
            weighted_sum = sum((self.current_week - week)* 3 * (idx + 1)
                               for idx, week in enumerate(sorted_history))
            cost = weighted_sum * scale
            return cost
        else:
            return scale
```

> 과거 이력이 없을 경우 -> 50 반환
> 과거 이력이 있을 경우 -> (현재 week - 과거 매칭되었던 week) * 3(임의의 상수) *(idx+1) 
> idx: 과거 매칭이 여러번 반복될수록 idx가 커짐

### ✔ mission_weight: 얼마나 최근에 미션을 수행했는지
```
def calc_recency(user_history: List[int]) -> float:
            score = 0.0
            for week in user_history:
                delta = self.current_week - week
                if delta >= 0:
                    score += 1.0 / (delta + 1) # delta를 분모로 두어서 현재에 가까울수록 커짐
            return score

        recency_from = calc_recency(history_from)
        recency_to   = calc_recency(history_to)
```

- 미션 수행 개수
```
count_from = len(history_from)
count_to   = len(history_to)
```

- 최근 수행 가중치 + 수행 횟수, 미션 많이 수행할수록, 더 최근에 수행할수록 비용 낮아짐
```
combined_score = ((recency_from + count_from) + (recency_to + count_to)) * 1/10
```

### ✔ hobby_weight: 같은 취미 선택시
`discount_rate=0.8
`
```
common_count = len(hobbies_u & hobbies_v)

        if common_count > 0:
            discount_factor = self.discount_rate ** common_count
            return int(base_cost * discount_factor)
        return base_cost
```

> 공통 취미 0개 -> 비용 = base_cost
> 공통 취미 1개 -> 비용 = base_cost * 0.8
> 공통 취미 2개 -> 비용 = base_cost * 0.8^2
> 공통 취미 3개 -> 비용 = base_cost * 0.8^3


### ✔ mbti_weight: mbti 궁합
<img width="500" alt="Image" src="https://github.com/user-attachments/assets/96390fc2-6658-4717-a0d2-ab58f07e2e7c" />

```
def get_cost(self, mbti1: str, mbti2: str) -> int:
        score = self.get_compatibility_score(mbti1, mbti2)
        penalty_per_score = 10 
        return self.base_cost + (score * penalty_per_score)
```

> score = '0: 파랑, 1: 연두, 2: 초록, 3: 노랑, 4: 빨강'
> score * penalty_per_score
> `penalty_per_score` = 10 임의 설정


### 결과 예시
<img width="1057" alt="Image" src="https://github.com/user-attachments/assets/5fc47549-6869-4713-97e6-2f129b78bba6" />
