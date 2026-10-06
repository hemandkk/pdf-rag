export type DocumentStatus = "processing" | "ready" | "failed";

export interface DocumentUploadResponse {
  document_id: string;
  filename: string;
  page_count: number;
  character_count: number;
  chunk_count: number;
  status: DocumentStatus;
  text_preview: string;
}

export interface Document {
  id: string;
  filename: string;
  page_count: number;
  character_count: number;
  chunk_count: number;
  embedding_provider: string;
  embedding_model: string;
  status: DocumentStatus;
  error_message: string | null;
  created_at: string;
  updated_at: string;
}

export interface DocumentListResponse {
  documents: Document[];
}
