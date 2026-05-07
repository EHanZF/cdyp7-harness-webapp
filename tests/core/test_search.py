import json

import pytest

from app.core import search


def test_cosine_similarity_identical():
    a = [1.0, 0.0, 0.0]
    b = [1.0, 0.0, 0.0]
    assert pytest.approx(search.cosine_similarity(a, b), rel=1e-6) == 1.0


def test_cosine_similarity_zero_vector():
    a = [0.0, 0.0]
    b = [1.0, 0.0]
    assert search.cosine_similarity(a, b) == 0.0


def test_search_empty_vecstore(tmp_path, monkeypatch):
    # point search at an empty/nonexistent vecstore
    monkeypatch.setattr(search, "VECSTORE_PATH", tmp_path / "vecstore.json")
    # patch embeddings to return a fixed vector
    monkeypatch.setattr(search, "embed_texts", lambda texts: [[1.0, 0.0]])
    res = search.search("anything", limit=5)
    assert isinstance(res, list)
    assert res == []


def test_search_returns_top_result(tmp_path, monkeypatch):
    vecs = {
        "vectors": [
            {"id": "f1:0", "file_id": "f1", "text": "hello world", "embedding": [1.0, 0.0]},
            {"id": "f2:0", "file_id": "f2", "text": "goodbye world", "embedding": [0.0, 1.0]},
        ]
    }
    path = tmp_path / "vecstore.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(vecs), encoding="utf-8")

    monkeypatch.setattr(search, "VECSTORE_PATH", path)
    # mock embeddings to ensure query maps to first vector
    monkeypatch.setattr(search, "embed_texts", lambda texts: [[1.0, 0.0]])

    results = search.search("hello", limit=2)
    assert len(results) >= 1
    assert results[0]["id"] == "f1:0"
    assert results[0]["score"] == pytest.approx(1.0, rel=1e-6)
