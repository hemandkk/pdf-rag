export interface ChatRequest {
  document_id: string;
  question: string;
  top_k?: number;
}

export interface ChatSource {
  page_number: number;
  chunk_index: number;
  text: string;
  similarity: number;
}

export interface ChatResponse {
  document_id: string;
  question: string;
  answer: string;
  sources: ChatSource[];
}
