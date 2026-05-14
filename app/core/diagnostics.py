from fastapi import APIRouter
from app.core.agent_context import AgentContext

router = APIRouter(prefix="/diagnostics", tags=["diagnostics"])


@router.get("/agent")
def agent_diagnostics(agent_ctx: AgentContext):
    return {
        "namespace": agent_ctx.namespace,
        "allowed_tools": sorted(agent_ctx.allowed_tools),
    }
