import Link from "next/link";

import { AppHeader } from "@/components/ui/app-header";
import { RetrievalDebug } from "@/components/search/retrieval-debug";

interface DebugPageProps {
  params: Promise<{
    documentId: string;
  }>;
}

export default async function DebugPage({ params }: DebugPageProps) {
  const { documentId } = await params;

  return (
    <main className="min-h-screen bg-slate-950 text-white">
      <AppHeader
        title="Retrieval Debugger"
        description="Inspect semantic search before the LLM."
        backHref={`/chat/${documentId}`}
        backLabel="Chat"
        rightContent={
          <Link
            href={`/chat/${documentId}`}
            className="rounded-lg border border-slate-700 px-4 py-2 text-sm font-medium text-slate-300 transition hover:bg-slate-900"
          >
            Chat
          </Link>
        }
      />

      <div className="mx-auto max-w-6xl px-6 py-8">
        <RetrievalDebug documentId={documentId} />
      </div>
    </main>
  );
}
