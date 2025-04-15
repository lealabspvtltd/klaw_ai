import chromadb
chroma_client = chromadb.PersistentClient(path="db/sub102")


# switch `create_collection` to `get_or_create_collection` to avoid creating a new collection every time
collection = chroma_client.get_or_create_collection(name="my_collection")



# switch `add` to `upsert` to avoid adding the same documents every time
collection.add(
    documents=[
        "This is a document about machine learning",
        "This is another document about data science",
        "A third document about artificial intelligence"
    ],
    metadatas=[
        {"source": "test1"},
        {"source": "test2"},
        {"source": "test3"}
    ],
    ids=[
        "id1",
        "id2",
        "id3"
    ]
)


results = collection.query(
    query_texts=["This is a query document about florida"], # Chroma will embed this for you
    n_results=2 # how many results to return
)

print(results)
