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