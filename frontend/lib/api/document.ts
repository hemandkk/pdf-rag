import { apiRequest } from "@/lib/api/client";
import type {
  Document,
  DocumentListResponse,
  DocumentUploadResponse,
} from "@/lib/types/document";

export async function uploadDocument(
  file: File,
): Promise<DocumentUploadResponse> {
  const formData = new FormData();

  formData.append("file", file);

  return apiRequest<DocumentUploadResponse>("/documents/upload", {
    method: "POST",
    body: formData,
  });
}

export async function getDocuments(): Promise<DocumentListResponse> {
  return apiRequest<DocumentListResponse>("/documents");
}

export async function getDocument(documentId: string): Promise<Document> {
  return apiRequest<Document>(`/documents/${documentId}`);
}
