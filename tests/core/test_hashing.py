from app.core.hashing import sha256_bytes, sha256_file


def test_sha256_bytes_is_deterministic():
    first = sha256_bytes(b"abc")
    second = sha256_bytes(b"abc")

    assert first == second
    assert first.startswith("sha256:")


def test_sha256_file_is_deterministic(tmp_path):
    path = tmp_path / "sample.txt"
    path.write_text("abc", encoding="utf-8")

    first = sha256_file(path)
    second = sha256_file(path)

    assert first == second
    assert first.startswith("sha256:")
