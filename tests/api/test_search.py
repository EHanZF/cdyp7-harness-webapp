import json

from fastapi.testclient import TestClient

from app import main


def test_api_search_get(monkeypatch, tmp_path):
    client = TestClient(main.app)

    # prepare vecstore file
    vecs = {
        "vectors": [
            {"id": "f1:0", "file_id": "f1", "text": "hello world", "embedding": [1.0, 0.0]},
            {"id": "f2:0", "file_id": "f2", "text": "goodbye", "embedding": [0.0, 1.0]},
        ]
    }
    # monkeypatch the VECSTORE_PATH used by search to tmp
    import app.core.search as search_mod

    path = tmp_path / "vecstore.json"
    path.write_text(json.dumps(vecs), encoding="utf-8")
    monkeypatch.setattr(search_mod, "VECSTORE_PATH", path)
    # patch embeddings to deterministic vector for query
    monkeypatch.setattr(search_mod, "embed_texts", lambda texts: [[1.0, 0.0]])
    # mock file metadata
    monkeypatch.setattr(
        search_mod,
        "get_file_entry",
        lambda fid: {
            "id": fid,
            "blob_uri": f"file://artifacts/{fid}.docx",
            "container": "artifacts",
            "blob_name": f"{fid}.docx",
            "filename": f"{fid}.docx",
            "content_type": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "uploaded_by": "tester",
            "uploaded_at": "2026-05-07T00:00:00Z",
            "tags": {"program": "CDYP7"},
        },
    )

    r = client.get("/api/search", params={"q": "hello", "limit": 2})
    assert r.status_code == 200
    j = r.json()
    assert j.get("query") == "hello"
    assert "results" in j
    assert len(j["results"]) >= 1
    assert j["results"][0]["id"] == "f1:0"
    assert j["results"][0].get("file", {}).get("filename") == "f1.docx"


def test_api_search_post(monkeypatch, tmp_path):
    client = TestClient(main.app)
    import app.core.search as search_mod

    vecs = {"vectors": [{"id": "f1:0", "file_id": "f1", "text": "t1", "embedding": [1.0, 0.0]}]}
    path = tmp_path / "vecstore.json"
    path.write_text(json.dumps(vecs), encoding="utf-8")
    monkeypatch.setattr(search_mod, "VECSTORE_PATH", path)
    monkeypatch.setattr(search_mod, "embed_texts", lambda texts: [[1.0, 0.0]])
    monkeypatch.setattr(
        search_mod,
        "get_file_entry",
        lambda fid: {
            "id": fid,
            "blob_uri": f"file://artifacts/{fid}.docx",
            "container": "artifacts",
            "blob_name": f"{fid}.docx",
            "filename": f"{fid}.docx",
            "content_type": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "uploaded_by": "tester",
            "uploaded_at": "2026-05-07T00:00:00Z",
            "tags": {"program": "CDYP7"},
        },
    )

    r = client.post("/api/search", json={"query": "t1", "limit": 1})
    assert r.status_code == 200
    j = r.json()
    assert j.get("query") == "t1"
    assert len(j.get("results", [])) == 1
    assert j.get("results")[0].get("file", {}).get("filename") == "f1.docx"
