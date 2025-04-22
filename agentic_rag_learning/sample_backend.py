# not a working program, neither have i worked in it , but very useful to understand the structure.


import sqlite3
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_core.tools import FunctionTool
from autogen_ext.models.openai import OpenAIChatCompletionClient

import asyncio


# --- Step 1: Database Functions ---

def get_syllabus(course_code: str) -> str:
    """
    Fetch the syllabus text from the database based on course_code.
    """
    conn = sqlite3.connect('courses.db')
    cursor = conn.cursor()
    cursor.execute("SELECT syllabus_text FROM courses WHERE course_code = ?", (course_code,))
    syllabus = cursor.fetchone()
    conn.close()
    return syllabus[0] if syllabus else ""

def get_materials(course_code: str) -> list:
    """
    Fetch all material texts for the given course_code.
    """
    conn = sqlite3.connect('courses.db')
    cursor = conn.cursor()
    cursor.execute("SELECT extracted_text FROM materials WHERE course_code = ?", (course_code,))
    materials = cursor.fetchall()
    conn.close()
    return [material[0] for material in materials]

# --- Step 2: Define Functions for the Tools ---

# Function to split syllabus into subtopics
def split_syllabus(syllabus: str) -> list:
    return syllabus.strip().split("\n")

# Function to find relevant content for each subtopic
def match_material_to_subtopics(subtopics: list, material: str) -> dict:
    from sentence_transformers import SentenceTransformer, util
    import torch

    model = SentenceTransformer('all-MiniLM-L6-v2')
    material_chunks = material.split("\n\n")  # break material into paragraphs

    material_embeddings = model.encode(material_chunks, convert_to_tensor=True)
    results = {}

    for sub in subtopics:
        query_emb = model.encode(sub, convert_to_tensor=True)
        scores = util.pytorch_cos_sim(query_emb, material_embeddings)[0]
        top_idx = torch.topk(scores, k=3).indices.tolist()
        matched = [material_chunks[i] for i in top_idx]
        results[sub] = matched

    return results


async def main():

    # --- Step 3: Convert them to FunctionTool ---
    split_syllabus_tool = FunctionTool(split_syllabus, description="Split syllabus into subtopics")
    match_tool = FunctionTool(match_material_to_subtopics, description="Match subtopics to material")

    # --- Step 4: Model Client ---
    
    # Create the model client
    model_client = OpenAIChatCompletionClient(
        model="gemini-1.5-flash-8b",
        api_key="AIzaSyCojNDEiD2Lhphj_9vRKbSRItedf-PUQ7o",
    )

    # --- Step 5: Define Agents ---
    syllabus_agent = AssistantAgent(
        name="SyllabusSplitterAgent",
        model_client=model_client,
        tools=[split_syllabus_tool],
        description="Splits the syllabus text into subtopics",
        system_message="You are responsible for breaking down the syllabus into clear subtopics.",
    )

    material_agent = AssistantAgent(
        name="MaterialMatcherAgent",
        model_client=model_client,
        tools=[match_tool],
        description="Matches subtopics with relevant content from the provided material",
        system_message="Your job is to find relevant content from the material for each subtopic.",
    )

    report_agent = AssistantAgent(
        name="ReportAgent",
        model_client=model_client,
        description="Generate a structured report mapping subtopics to content",
        system_message="Use the outputs from the other agents to produce a final report. End the report with TERMINATE.",
    )

    # --- Step 6: Group Chat Team ---
    team = RoundRobinGroupChat(
        [syllabus_agent, material_agent, report_agent],
        max_turns=5,
        termination_condition=TextMentionTermination("TERMINATE")
    )

    # --- Step 7: Input task (Fetch syllabus and materials from DB) ---
    course_code = "HUT300"  # Example course code

    syllabus = get_syllabus(course_code)  # Fetch syllabus from DB
    materials = get_materials(course_code)  # Fetch materials from DB

    # Task input: pass syllabus and materials dynamically
    task = f"""
    Here is the syllabus and content. Process it and map the subtopics with related content.

    Syllabus:
    {syllabus}

    Materials:
    {', '.join(materials)}
    """

    # --- Step 8: Run team stream ---
    stream = team.run_stream(task=task)
    await Console(stream)

    # --- Step 9: Close client ---
    await model_client.close()


# Run the async function
if __name__ == "__main__":
    asyncio.run(main())
