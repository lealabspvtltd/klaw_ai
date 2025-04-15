import chromadb

# Set up ChromaDB
client = chromadb.Client()
collection = client.create_collection("dog_info")

text1 = "sample text 1"

# Add the text to ChromaDB
collection.add(documents=[text1], ids=["dog_doc1"])
print("Stored in ChromaDB!")