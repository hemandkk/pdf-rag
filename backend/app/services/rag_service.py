from collections.abc import Iterator

from app.schemas.chat import (
    ChatResponse,
    SourceResponse,
)
from app.services.llm_service import LLMService
from app.services.retrieval_service import RetrievalService
from app.services.source_enrichment_service import (
    SourceEnrichmentService,
)


class RAGService:
    def __init__(
        self,
        retrieval_service: RetrievalService,
        llm_service: LLMService,
        source_enrichment_service: SourceEnrichmentService,
    ) -> None:
        self.retrieval_service = retrieval_service
        self.llm_service = llm_service
        self.source_enrichment_service = source_enrichment_service

    def _build_prompt(
        self,
        question: str,
        context: str,
        history: list[dict[str, str]] | None = None,
    ) -> str:
        history = history or []

        history_text = "\n".join(
            (
                f"{message['role'].capitalize()}: "
                f"{message['content']}"
            )
            for message in history
        )

        if not history_text:
            history_text = "No previous conversation."

        return f"""
You are a helpful assistant answering questions
about the documents available in the knowledge base.

Answer the user's question using ONLY the
provided document context.

Conversation history may be used to understand
references such as "it", "they", "that section",
or follow-up questions.

However, conversation history is NOT evidence.
The retrieved document context is the source of truth.

Rules:
1. Do not use outside knowledge.
2. Do not invent information.
3. If the retrieved context does not contain enough
   information, say:
   "I could not find that information in the documents."
4. When useful, mention the relevant page using
   [Page X].
5. When useful, identify the source document.
6. Give a clear and concise answer.

Conversation history:
--------------------
{history_text}
--------------------

Retrieved document context:
----------------------------
{context}
----------------------------

Current user question:
{question}

Answer:
""".strip()

    def _build_context(
        self,
        results,
    ) -> str:
        context_parts: list[str] = []

        for result in results:
            context_parts.append(
                f"[Document: {result.filename}]\n"
                f"[Page {result.page_number}]\n"
                f"{result.text}"
            )

        return "\n\n".join(context_parts)

    def _build_sources(
        self,
        results,
    ) -> list[SourceResponse]:
        return [
            SourceResponse(
                document_id=result.document_id,
                filename=result.filename,
                page_number=result.page_number,
                chunk_index=result.chunk_index,
                text=result.text,
                similarity=result.similarity,
            )
            for result in results
        ]

    def chat(
        self,
        question: str,
        history: list[dict[str, str]] | None = None,
        top_k: int | None = None,
    ) -> ChatResponse:

        print("[RAG] Starting chat")
        print("[RAG] Question:", question)
        results = self.retrieval_service.search(
            query=question,
            top_k=top_k,
        )
        print(f"[RAG] Retrieval completed: {len(results)} results")

        if not results:
            return ChatResponse(
                question=question,
                answer=(
                    "I could not find that information "
                    "in the documents."
                ),
                sources=[],
            )
        print("[RAG] Starting source enrichment")

        enriched_results = self.source_enrichment_service.enrich(
            results
        )
        print(
            f"[RAG] Source enrichment completed: "
            f"{len(enriched_results)} results"
        )
        if not enriched_results:
            print("[RAG] No enriched results")

            return ChatResponse(
                question=question,
                answer=(
                    "I could not find that information "
                    "in the documents."
                ),
                sources=[],
            )

        context = self._build_context(enriched_results)
        print("[RAG] Context built")
        print("[RAG] Calling LLM")
        prompt = self._build_prompt(
            question=question,
            context=context,
            history=history,
        )

        answer = self.llm_service.generate(prompt)
        print("[RAG] LLM completed")

        return ChatResponse(
            question=question,
            answer=answer,
            sources=self._build_sources(enriched_results),
        )

    def stream(
        self,
        question: str,
        history: list[dict[str, str]] | None = None,
        top_k: int | None = None,
    ) -> tuple[list[SourceResponse], Iterator[str]]:
        print("[RAG] stream() entered")
        print("[RAG] Question:", question)

        results = self.retrieval_service.search(
            query=question,
            top_k=top_k,
        )

        print(
            f"[RAG] Retrieval completed: {len(results)} results"
        )
      
        if not results:

            def fallback_stream() -> Iterator[str]:
                yield (
                    "I could not find that information "
                    "in the documents."
                )

            return [], fallback_stream()
        print("[RAG] Starting source enrichment")

        enriched_results = self.source_enrichment_service.enrich(
            results
        )
        print("[RAG] Source enrichment completed")

        if not enriched_results:

            def enrichment_fallback_stream() -> Iterator[str]:
                yield (
                    "I could not find that information "
                    "in the documents."
                )

            return [], enrichment_fallback_stream()
        print("[RAG] Starting _build_sources ")

        sources = self._build_sources(enriched_results)
        print("[RAG] Starting Context built")
        context = self._build_context(enriched_results)
        print("[RAG] Context built")
        prompt = self._build_prompt(
            question=question,
            context=context,
            history=history,
        )

        return (
            sources,
            self.llm_service.stream(prompt),
        )