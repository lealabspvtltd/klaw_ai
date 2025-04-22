# create a sample program to setup a team and all


import asyncio

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.base import TaskResult
from autogen_agentchat.conditions import ExternalTermination, TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_core import CancellationToken
from autogen_ext.models.openai import OpenAIChatCompletionClient

async def main():
        

    # Create the model client
    model_client = OpenAIChatCompletionClient(
        model="gemini-1.5-flash-8b",
        api_key="AIzaSyCojNDEiD2Lhphj_9vRKbSRItedf-PUQ7o",
    )
    # Create the primary agent.
    primary_agent = AssistantAgent(
        "Agent_creator",
        model_client=model_client,
        system_message="You are a helpful AI assistant.",
    )

    # Create the critic agent.
    critic_agent = AssistantAgent(
        "Agent_evaluator",
        model_client=model_client,
        system_message="Provide  feedback for the peom. Respond with 'APPROVE' to when your feedbacks are addressed on a new line. make sure you donot give approve on the first 3 feedback. You can also send for review, correction , resubmit and rewrite for improving",
    )

    # Define a termination condition that stops the task if the critic approves.
    text_termination = TextMentionTermination("APPROVE")

    # Create a team with the primary and critic agents.
    team = RoundRobinGroupChat([primary_agent, critic_agent], termination_condition=text_termination)


    # Use `asyncio.run(...)` when running in a script.
    #result = await team.run(task="Write a short poem about the fall season.")
    #print(result)

    # When running inside a script, use a async main function and call it from `asyncio.run(...)`.
    await team.reset()  # Reset the team for a new task.
    async for message in team.run_stream(task="Write a short poem about the fall season and that are average"):  # type: ignore
        if isinstance(message, TaskResult):
            print("Stop Reason:", message.stop_reason)
        else:
            print(message)


    await team.reset()  # Reset the team for a new task.
    await Console(team.run_stream(task="Write a short poem about the fall season."))  # Stream the messages to the console.




# Run the async function
if __name__ == "__main__":
    asyncio.run(main())