export interface SearchRequest {
  document_id: string;
  query: string;
  top_k?: number;
}

export interface SearchResult {
  page_number: number;
  chunk_index: number;
  text: string;
  similarity: number;
  accepted: boolean;
}

export interface SearchResponse {
  document_id: string;
  query: string;
  threshold: number;
  results: SearchResult[];
}
