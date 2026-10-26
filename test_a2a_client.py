
import asyncio
import uuid

from a2a.client import create_client
from a2a.types import Message, Part, Role, SendMessageRequest


async def main():
    # Connect to Agent 2 using its Agent Card URL.
    client = await create_client("http://localhost:8001/")

    message = Message(
        message_id=str(uuid.uuid4()),
        role=Role.ROLE_USER,
        parts=[
            Part(
                text=(
                    "Analyze these sales: Product A sold 100 units, "
                    "Product B sold 250 units, and Product C sold "
                    "150 units. Which product performed best?"
                )
            )
        ],
    )

    request = SendMessageRequest(message=message)

    print("Sending request to Agent 2...")

    async for response in awaitable_stream(client, request):
        print("\nAgent 2 response:")
        print(response)


async def awaitable_stream(client, request):
    async for response in client.send_message(request):
        yield response


if __name__ == "__main__":
    asyncio.run(main())
