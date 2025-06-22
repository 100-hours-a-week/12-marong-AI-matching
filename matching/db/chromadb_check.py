from chromadb_client import (
    get_user_latest_collection,
    get_user_history_collection,
)


# Chroma 컬렉션 연결
latest_mbti = get_user_latest_collection()
history_mbti = get_user_history_collection()


def to_items(raw):
    ids = raw.get('ids', [])
    docs = raw.get('documents', [])
    embs = raw.get('embeddings', [])
    metas = raw.get('metadatas', [])
    items = []
    for i, _id in enumerate(ids):
        emb = embs[i] if i < len(embs) else None
        try:
            emb = emb.tolist()
        except Exception:
            pass
        items.append({
            'id': _id,
            'document': docs[i] if i < len(docs) else None,
            'embedding': emb,
            'metadata': metas[i] if i < len(metas) else {},
        })
    return items


# 최신값 확인
print("\n=== USER Latest ===")
latest_raw = latest_mbti.peek(limit=None)
latest_items = to_items(latest_raw)
for item in latest_items:
    print(f"user_id: {item['metadata'].get('user_id')}")
    print(f"MBTI scores: {item['metadata'].get('ei_score')}, {item['metadata'].get('sn_score')}, {item['metadata'].get('tf_score')}, {item['metadata'].get('jp_score')}")
    print(f"updated_at: {item['metadata'].get('updated_at')}")
    print("---")

# 히스토리 확인
print("\n=== USER History ===")
history_raw = history_mbti.peek(limit=None)
history_items = to_items(history_raw)
for item in history_items:
    print(f"user_id: {item['metadata'].get('user_id')} | ts: {item['metadata'].get('timestamp')}")
    print(f"MBTI: {item['metadata'].get('ei_score')}, {item['metadata'].get('sn_score')}, {item['metadata'].get('tf_score')}, {item['metadata'].get('jp_score')}")
    print("---")