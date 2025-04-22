# creating agents to use multiple tools and all

import asyncio

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import StructuredMessage, TextMessage
from autogen_agentchat.ui import Console
from autogen_core import CancellationToken
from autogen_ext.models.openai import OpenAIChatCompletionClient

async def main():
    # Define a tool that searches the web for information.
    async def web_search(query: str) -> str:
        """Find information on the web, this is a function need to create if we want to use it and search web"""
        return "AutoGen is a programming framework for building multi-agent applications."


    # Create an agent that uses the gemini model.
    model_client = OpenAIChatCompletionClient(
        model="gemini-1.5-flash-8b",
        api_key="AIzaSyCojNDEiD2Lhphj_9vRKbSRItedf-PUQ7o",
    )

    agent = AssistantAgent(
        name="assistant",
        model_client=model_client,
        tools=[web_search],
        system_message="Use tools to solve tasks.",
    )


    """ 
    Getting Responses

    We can use the on_messages() method to get the agent response to a given message.

    """

    async def assistant_run() -> None:
        response = await agent.on_messages(
            [TextMessage(content="Find information on AutoGen", source="user")],
            cancellation_token=CancellationToken(),
        )
        print(response.inner_messages)
        print(response.chat_message)


    # Use asyncio.run(assistant_run()) when running in a script.
    await assistant_run()


# Run the async function
if __name__ == "__main__":
    asyncio.run(main())
