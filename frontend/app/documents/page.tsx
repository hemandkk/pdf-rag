import { AppHeader } from "@/components/ui/app-header";
import { DocumentList } from "@/components/documents/document-list";
import { DocumentUpload } from "@/components/documents/document-upload";

export default function DocumentsPage() {
  return (
    <main className="min-h-screen bg-slate-950 text-white">
      <AppHeader
        title="Documents"
        description="Upload PDFs and ask questions about their content."
        backHref="/"
        backLabel="PDF RAG"
      />

      <div className="mx-auto max-w-6xl px-6 py-10">
        <section>
          <div className="mb-5">
            <h2 className="text-xl font-semibold">Upload Document</h2>

            <p className="mt-1 text-sm text-slate-400">
              Your PDF will be processed and indexed for semantic search.
            </p>
          </div>

          <DocumentUpload />
        </section>

        <section className="mt-12">
          <div className="mb-5 flex items-end justify-between gap-4">
            <div>
              <h2 className="text-xl font-semibold">Your Documents</h2>

              <p className="mt-1 text-sm text-slate-400">
                Documents available for RAG-based questions.
              </p>
            </div>
          </div>

          <DocumentList />
        </section>
      </div>
    </main>
  );
}
