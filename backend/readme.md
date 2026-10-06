
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