from app.services.llm_service import (
    LLMService,
)
from app.services.retrieval_service import (
    RetrievalService,
)
from app.services.vector_service import (
    SearchResult,
)


class RAGService:
    def __init__(self) -> None:
        self.retrieval_service = (
            RetrievalService()
        )

        self.llm_service = (
            LLMService()
        )

    def answer_question(
        self,
        document_id: str,
        question: str,
        top_k: int | None = None,
    ) -> tuple[
        str,
        list[SearchResult],
    ]:

        search_results = (
            self.retrieval_service.search(
                document_id=document_id,
                query=question,
                top_k=top_k,
            )
        )

        if not search_results:
            return (
                "I could not find relevant "
                "information in the document.",
                [],
            )

        context = self._build_context(
            search_results
        )

        prompt = self._build_prompt(
            question=question,
            context=context,
        )

        answer = self.llm_service.generate(
            prompt
        )

        return answer, search_results

    @staticmethod
    def _build_context(
        search_results: list[
            SearchResult
        ],
    ) -> str:

        context_parts: list[str] = []

        for result in search_results:
            context_parts.append(
                (
                    f"[Page "
                    f"{result.page_number}]\n"
                    f"{result.text}"
                )
            )

        return "\n\n".join(
            context_parts
        )

    @staticmethod
    def _build_prompt(
        question: str,
        context: str,
    ) -> str:

        return f"""
You are a document question-answering assistant.

Answer the user's question using ONLY the
information contained in the provided context.

Rules:

1. Do not use outside knowledge.
2. Do not invent information.
3. If the context does not contain enough
   information to answer the question, say:
   "I could not find that information in
   the document."
4. Keep the answer clear and concise.
5. When appropriate, mention the page number
   using the format [Page X].

Context:

{context}

Question:

{question}

Answer:
""".strip()