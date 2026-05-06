def require_actor(actor: str | None) -> None:
<<<<<<< HEAD
    if not actor or "@" not in actor:
        raise PermissionError("Actor must be explicit, such as user@example.com")
=======
    if not actor or '@' not in actor:
        raise PermissionError('Actor must be explicit, such as user@example.com')
>>>>>>> b0f8b70 (Add tooling API contract tests and validation output)
