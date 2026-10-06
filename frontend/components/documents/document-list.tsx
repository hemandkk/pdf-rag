"use client";

import { useQuery } from "@tanstack/react-query";

import { getDocuments } from "@/lib/api/document";
import { DocumentCard } from "@/components/documents/document-card";
import { DocumentListSkeleton } from "@/components/documents/document-list-skeleton";
import { EmptyState } from "@/components/ui/empty-state";
import { ErrorState } from "@/components/ui/error-state";

export function DocumentList() {
  const { data, isLoading, isError, error, refetch } = useQuery({
    queryKey: ["documents"],
    queryFn: getDocuments,
  });

  if (isLoading) {
    return <DocumentListSkeleton />;
  }

  if (isError) {
    return (
      <ErrorState
        title="Unable to load documents"
        message={
          error instanceof Error
            ? error.message
            : "The document service could not be reached."
        }
        onRetry={() => refetch()}
      />
    );
  }

  const documents = data?.documents ?? [];

  if (documents.length === 0) {
    return (
      <EmptyState
        icon="📚"
        title="No documents yet"
        description="Upload your first PDF to start building your searchable document library."
      />
    );
  }

  return (
    <div className="space-y-4">
      {documents.map((document) => (
        <DocumentCard key={document.id} document={document} />
      ))}
    </div>
  );
}
