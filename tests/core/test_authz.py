import pytest

from app.core.authz import require_actor


def test_require_actor_accepts_non_empty_actor():
    require_actor("user@example.com")


def test_require_actor_rejects_empty_actor():
    with pytest.raises(PermissionError):
        require_actor("")


def test_require_actor_rejects_none():
    with pytest.raises(PermissionError):
        require_actor(None)
