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

add_topic_data(
    subject="Biology",
    topic="Genetics",
    documents=[
        "Mendel's laws form the foundation of classical genetics.",
        "Genes are segments of DNA that code for proteins.",
        "A genotype refers to the genetic makeup, while phenotype refers to observable traits.",
        "DNA replication is a semi-conservative process involving several enzymes."
    ],
    source_name="Biology Textbook Chapter 3"
)
add_topic_data(
    subject="Physics",
    topic="Newtonian_Mechanics",
    documents=[
        "Newton's First Law states that an object remains at rest or in uniform motion unless acted upon by a force.",
        "Force equals mass times acceleration, as per Newton's Second Law.",
        "Every action has an equal and opposite reaction — Newton's Third Law.",
        "Friction is a force that opposes the relative motion between two surfaces in contact."
    ],
    source_name="Physics Textbook Chapter 2"
)

add_topic_data(
    subject="Physics",
    topic="Thermodynamics",
    documents=[
        "The First Law of Thermodynamics is the law of conservation of energy.",
        "Entropy is a measure of disorder in a system.",
        "The Second Law states that the entropy of an isolated system never decreases.",
        "Heat always flows from a body at a higher temperature to a body at a lower temperature."
    ],
    source_name="Physics Textbook Chapter 5"
)
add_topic_data(
    subject="Chemistry",
    topic="Atomic_Structure",
    documents=[
        "An atom is composed of protons, neutrons, and electrons.",
        "Electrons occupy orbitals based on increasing energy levels — Aufbau Principle.",
        "The atomic number is equal to the number of protons in an atom.",
        "Isotopes are atoms of the same element with different numbers of neutrons."
    ],
    source_name="Chemistry Textbook Chapter 1"
)

add_topic_data(
    subject="Chemistry",
    topic="Chemical_Bonding",
    documents=[
        "Ionic bonds are formed when electrons are transferred from one atom to another.",
        "Covalent bonds involve the sharing of electron pairs between atoms.",
        "The octet rule states that atoms tend to gain, lose or share electrons to have eight in their valence shell.",
        "Polarity in covalent bonds arises due to differences in electronegativity."
    ],
    source_name="Chemistry Textbook Chapter 4"
)


#response = query_topic("sub101", "sub101A", "How is energy produced in cells?")
#print(response)
