
# create venv
    python -m venv venv
# activate venv
    venv\Scripts\activate



# removing vector index 
    Your vector database collection has to use embeddings from the same vector space/dimension.
    You cannot mix the existing local vectors with OpenAI vectors in the same collection.
    Therefore, whenever you change the embedding provider/model, we should rebuild the vector index.
     Remove-Item -Recurse -Force .\chroma

     Then re-upload your PDFs.

# get vector dimention
    run python -c "from app.services.embedding_service import EmbeddingService; e=EmbeddingService(); print(len(e.embed_query('What is this document about?')))"
# provide name for local
    run python -c "from app.services.embedding_service import EmbeddingService; e=EmbeddingService(); print(type(e.provider).__name__)"


# We're currently using:
        LOCAL_EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

    That's perfectly fine for learning.
    But it isn't specifically optimized for asymmetric question → passage retrieval.
    Sentence Transformers lists models specifically trained for semantic search, including the multi-qa family. Sentence Transformers
    Later we could change to something like:
        LOCAL_EMBEDDING_MODEL=sentence-transformers/multi-qa-MiniLM-L6-cos-v1

    Then rebuild Chroma:
        Remove-Item -Recurse -Force .\chroma

    and re-upload the PDFs.
    Don't switch yet. First get the current pipeline working so you have a baseline.