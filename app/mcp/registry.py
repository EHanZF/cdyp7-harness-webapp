from app.tools import (
    generate_release_sheet,
    validate_release_sheet,
    write_receipt,
    fetch_artifact,
    resolve_replay
)

TOOL_REGISTRY = {
    "harness.generate_release_sheet": generate_release_sheet,
    "harness.validate_release_sheet": validate_release_sheet,
    "harness.write_receipt": write_receipt,
    "harness.fetch_artifact": fetch_artifact,
    "harness.resolve_replay": resolve_replay,
}
