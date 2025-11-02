
import asyncio
from app.llm import async_openai_client


# async def main():
#     response = await async_openai_client.responses.create(
#         model="gpt-4.1-nano", 
#         input=[{"role": "user", 
#                 "content": "Tell me a story"}], stream=True
#     )

#     async for event in response:
#         if event.type == "response.output_text.delta":
#             print(event.delta, end="")
#         elif event.type == "response.completed":
#             print("\n")
#             print(event.response.output_text)
#             print(event.response.usage.input_tokens)
#             print(event.response.usage.output_tokens)
#             print(event.response.usage.total_tokens)


# if __name__ == "__main__":
#     asyncio.run(main=main())


from typing import AsyncGenerator

async def stream_story(user_prompt: str) -> AsyncGenerator[str, None]:
    """
    Streams text output from the OpenAI response.
    
    Yields:
        str: Each incremental text chunk from the model.
    """
    response = await async_openai_client.responses.create(
        model="gpt-4.1-nano",
        input=[{"role": "user", "content": user_prompt}],
        stream=True
    )

    async for event in response:
        if event.type == "response.output_text.delta":
            yield event.delta  # yield incremental text
        elif event.type == "response.completed":
            # yield final text if needed (redundant if all deltas were streamed)
            yield "\n--- Completed ---\n"
            yield event.response.output_text  # final full text
            # Optionally, yield token usage info
            usage_info = (
                f"Tokens used:\n"
                f"  Input: {event.response.usage.input_tokens}\n"
                f"  Output: {event.response.usage.output_tokens}\n"
                f"  Total: {event.response.usage.total_tokens}\n"
            )
            yield usage_info

async def main():
    async for chunk in stream_story("Tell me a story"):
        print(chunk, end="", flush=True)

# Run the async main function
if __name__ == "__main__":
    asyncio.run(main())