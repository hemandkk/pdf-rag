import Link from "next/link";

import type { Document } from "@/lib/types/document";

import { DocumentStatus } from "@/components/documents/document-status";

interface DocumentCardProps {
  document: Document;
}

function formatCharacterCount(characters: number): string {
  if (characters < 1000) {
    return `${characters} chars`;
  }

  if (characters < 1_000_000) {
    return `${(characters / 1000).toFixed(1)}K chars`;
  }

  return `${(characters / 1_000_000).toFixed(1)}M chars`;
}

export function DocumentCard({ document }: DocumentCardProps) {
  return (
    <article className="rounded-xl border border-slate-800 bg-slate-900 p-5 transition hover:border-slate-700">
      <div className="flex flex-col gap-5 lg:flex-row lg:items-center lg:justify-between">
        <div className="flex min-w-0 items-start gap-4">
          <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-lg bg-slate-800 text-xl">
            📄
          </div>

          <div className="min-w-0">
            <h3 className="truncate font-semibold text-white">
              {document.filename}
            </h3>

            <div className="mt-2 flex flex-wrap gap-x-4 gap-y-1 text-xs text-slate-400">
              <span>{document.page_count} pages</span>

              <span>{document.chunk_count} chunks</span>

              <span>{formatCharacterCount(document.character_count)}</span>
            </div>

            <p className="mt-2 text-xs text-slate-500">
              Embeddings: {document.embedding_provider}
            </p>
          </div>
        </div>

        <div className="flex flex-wrap items-center gap-3">
          <DocumentStatus status={document.status} />

          {document.status === "ready" && (
            <>
              <Link
                href={`/debug/${document.id}`}
                className="rounded-lg border border-slate-700 px-4 py-2 text-sm font-medium text-slate-300 transition hover:bg-slate-800"
              >
                Debug
              </Link>

              <Link
                href={`/chat/${document.id}`}
                className="rounded-lg bg-white px-4 py-2 text-sm font-medium text-slate-950 transition hover:bg-slate-200"
              >
                Chat
              </Link>
            </>
          )}

          {document.status === "processing" && (
            <span className="text-xs text-slate-500">
              Preparing document...
            </span>
          )}
        </div>
      </div>

      {document.status === "failed" && document.error_message && (
        <div className="mt-4 rounded-lg border border-red-900 bg-red-950/30 p-4">
          <p className="text-xs font-medium text-red-300">Processing failed</p>

          <p className="mt-1 text-xs leading-5 text-red-300/70">
            {document.error_message}
          </p>
        </div>
      )}
    </article>
  );
}
