The complete upload flow
Now you can see how everything connects.
User uploads:
architecture.pdf

Step 1
Router receives:
POST /documents/upload

↓
Step 2
Document metadata created:
DocumentService
    ↓
DocumentRepository
    ↓
SQLite

status:
processing

↓
Step 3
PDF extraction:
PDFService

↓
Page 1
Page 2
Page 3
...

↓
Step 4
Chunking:
ChunkService

↓
Chunk 1
Chunk 2
Chunk 3
...

↓
Step 5
Embedding:
EmbeddingService

↓
[0.12, -0.33, ...]
[0.45,  0.11, ...]
...

↓
Step 6
Store vectors:
VectorService

↓
ChromaDB

↓
Step 7
Update metadata:
DocumentService

↓
SQLite

status = ready
page_count = 24
chunk_count = 143

27. Then the question flow
User asks:
"What architecture does the document use?"

Router:
POST /chat

↓
RAGService
↓
RetrievalService
↓
EmbeddingService
↓
Query becomes vector:
[0.14, -0.22, ...]

↓
VectorService
↓
Chroma:
Top 5 chunks

↓
RAGService
Builds context:
[Page 4]
...

[Page 7]
...

[Page 12]
...

↓
LLMService
↓
Gemini/OpenAI
↓
Answer

↓
Router
↓
Frontend.



| Service | Responsibility |
|---|---|
| `PDFService` | Read PDF |
| `ChunkService` | Split text |
| `EmbeddingService` | Convert text → vectors |
| `VectorService` | Store/search vectors |
| `RetrievalService` | Find relevant chunks |
| `LLMService` | Generate text |
| `RAGService` | Retrieval + generation |
| `RAGIngestionService` | PDF → RAG pipeline |
| `DocumentService` | Document metadata |




# multiple document upload
But there's an even more important RAG problem
Suppose you upload 100 PDFs.
A naive system might retrieve:
top 10 chunks

and accidentally return:
PDF 1 → 8 chunks
PDF 2 → 1 chunk
PDF 3 → 1 chunk

That may not be ideal.
For multi-document RAG, we eventually want diverse retrieval.
For example:
Top 10 results

PDF A → 3 chunks
PDF B → 2 chunks
PDF C → 3 chunks
PDF D → 2 chunks

This helps when the question requires comparing documents.
Eventually we can introduce:
- metadata filtering
- similarity threshold
- MMR/diversity retrieval
- document-level ranking
- reranking
- query expansion
- hybrid search

# A stronger RAG architecture is:

                         USER QUESTION
                              │
                              ↓
                    Query preprocessing
                              │
                              ↓
                    ┌─────────────────┐
                    │ Dense Retrieval │
                    │   Embeddings    │
                    └────────┬────────┘
                             ↓
                         Top 20-50
                         candidates
                             │
                             ↓
                    ┌─────────────────┐
                    │    Reranker     │
                    │  Cross Encoder  │
                    └────────┬────────┘
                             ↓
                          Top 3-8
                             │
                             ↓
                    Context construction
                             │
                             ↓
                           LLM
                             │
                             ↓
                  Answer + citations

    OpenAI embeddings
        A strong managed option is:
        text-embedding-3-large

        OpenAI describes it as its most capable embedding model, with up to 3072 dimensions. OpenAI Developers
        You could configure:
        EMBEDDING_PROVIDER=openai
        OPENAI_EMBEDDING_MODEL=text-embedding-3-large

        Your factory would choose it:
        settings
        ↓
        EMBEDDING_PROVIDER=openai
        ↓
        OpenAIEmbeddingProvider
        ↓
        text-embedding-3-large

    Voyage AI
        Another serious retrieval-oriented option is Voyage.
        Their current API offers embedding models such as:
        voyage-4-large
        voyage-4
        voyage-4-lite
        voyage-3.5
        voyage-3.5-lite
    Cohere 
        is another particularly interesting RAG provider because it has both:
        Embed
        Rerank
        Chat

        and its current rerank family includes:
        rerank-v4.0-pro
        rerank-v4.0-fast

        with the pro variant aimed at higher-quality/complex use cases and fast at lower latency/high throughput