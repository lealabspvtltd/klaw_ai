#sample code to use gemini using autogen


import asyncio
from autogen_core.models import UserMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient

async def main():
    # Create the model client
    model_client = OpenAIChatCompletionClient(
        model="gemini-1.5-flash-8b",
        api_key="AIzaSyCojNDEiD2Lhphj_9vRKbSRItedf-PUQ7o",
    )

    # Send a message and await response
    response = await model_client.create([
        UserMessage(content="What is the capital of India?", source="user")
    ])

    # Print the response
    print(response)

    # Close the client
    await model_client.close()

# Run the async function
if __name__ == "__main__":
    asyncio.run(main())
