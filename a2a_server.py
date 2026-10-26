
import asyncio

from starlette.applications import Starlette
import uvicorn

from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.routes import (
    create_agent_card_routes,
    create_jsonrpc_routes,
)
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import (
    AgentCard,
    AgentCapabilities,
    AgentInterface,
    AgentSkill,
    Message,
    Part,
    Role,
)

from remote_agent import analyze_data


class DataAnalysisExecutor(AgentExecutor):
    """Connect the A2A request to the existing Groq agent."""

    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        user_request = context.get_user_input()

        if not user_request.strip():
            result = "Please provide data or a question to analyze."
        else:
            result = await asyncio.to_thread(
                analyze_data, user_request
            )

        response = Message(
            role=Role.ROLE_AGENT,
            parts=[Part(text=result)],
        )

        await event_queue.enqueue_event(response)

    async def cancel(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        # No long-running background operation to cancel yet.
        return


agent_card = AgentCard(
    name="Remote Data Analysis Agent",
    description=(
        "Analyzes supplied data using Groq and explains "
        "the findings in simple English."
    ),
    supported_interfaces=[
        AgentInterface(
            url="http://localhost:8001/",
            protocol_binding="JSONRPC",
            protocol_version="1.0",
        )
    ],
    version="1.0.0",
    capabilities=AgentCapabilities(),
    default_input_modes=["text/plain"],
    default_output_modes=["text/plain"],
    skills=[
        AgentSkill(
            id="data-analysis",
            name="Data Analysis",
            description=(
                "Find patterns, compare values, and summarize "
                "data provided by the caller."
            ),
            tags=["data", "analysis", "groq"],
            examples=[
                "Compare sales for three products."
            ],
        )
    ],
)

request_handler = DefaultRequestHandler(
    agent_executor=DataAnalysisExecutor(),
    task_store=InMemoryTaskStore(),
    agent_card=agent_card,
)

routes = []
routes.extend(create_agent_card_routes(agent_card))
routes.extend(create_jsonrpc_routes(request_handler, rpc_url="/"))

app = Starlette(routes=routes)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
