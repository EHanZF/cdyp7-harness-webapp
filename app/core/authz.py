def require_actor(actor: str | None) -> None:
    if not actor or "@" not in actor:
        raise PermissionError("Actor must be explicit, such as user@example.com")
