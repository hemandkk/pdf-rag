import Link from "next/link";

import { AppHeader } from "@/components/ui/app-header";
import { ChatWindow } from "@/components/chat/chat-window";

interface ChatPageProps {
  params: Promise<{
    documentId: string;
  }>;
}

export default async function ChatPage({ params }: ChatPageProps) {
  const { documentId } = await params;

  return (
    <main className="min-h-screen bg-slate-950 text-white">
      <AppHeader
        title="Document Chat"
        description="Ask questions using retrieval-augmented generation."
        backHref="/documents"
        backLabel="Documents"
        rightContent={
          <Link
            href={`/debug/${documentId}`}
            className="rounded-lg border border-slate-700 px-4 py-2 text-sm font-medium text-slate-300 transition hover:bg-slate-900"
          >
            Retrieval Debug
          </Link>
        }
      />

      <ChatWindow documentId={documentId} />
    </main>
  );
}
