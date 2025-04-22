# using functions to access chromadb.
# for each subject a new collection and db is created.
# for each topic in subject, it is set to auto increment and save the data.

import chromadb




def get_subject_collection(subject_code):
    chroma_client = chromadb.PersistentClient(path=f"db/{subject_code}")
    return chroma_client.get_or_create_collection(name=subject_code)




def add_topic_data(subject, topic, documents, source_name):
    """
    Adds documents under a specific subject and topic.
    
    subject: e.g. "sub101"
    topic: e.g. "sub101A"
    documents: List of strings (text content)
    source_name: e.g. "NCERT Textbook", "PDF Notes"
    """

    collection = get_subject_collection(subject)

    # Generate unique IDs
    doc_ids = [f"{topic}_{i}" for i in range(len(documents))]

    # Metadata to store topic and source
    metadatas = [{"topic": topic, "source": source_name} for _ in documents]

    collection.upsert(
        documents=documents,
        metadatas=metadatas,
        ids=doc_ids
    )



def query_topic(subject, topic_query, user_question):
    collection = get_subject_collection(subject)

    results = collection.query(
        query_texts=[user_question],
        n_results=5,
        where={"topic": topic_query}
    )

    return results

"""

# sample usage

add_topic_data(
    subject="Biology",
    topic="Cell_Biology",
    documents=[
        "The mitochondria is the powerhouse of the cell.",
        "ATP is generated during cellular respiration.",
        "Ribosomes are responsible for protein synthesis in cells.",
        "The nucleus contains the genetic material of the cell in the form of DNA."
    ],
    source_name="Biology Textbook Chapter 1"
)


#response = query_topic("sub101", "sub101A", "How is energy produced in cells?")
#print(response)

"""