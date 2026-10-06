import Link from "next/link";

export default function HomePage() {
  return (
    <main className="min-h-screen bg-slate-950 text-white">
      <div className="mx-auto flex min-h-screen max-w-6xl items-center px-6">
        <div className="max-w-3xl">
          <div className="mb-6 inline-flex rounded-full border border-slate-800 bg-slate-900 px-3 py-1 text-xs font-medium text-slate-400">
            Retrieval-Augmented Generation
          </div>

          <h1 className="text-5xl font-bold tracking-tight sm:text-6xl">
            Ask questions about your PDFs.
          </h1>

          <p className="mt-6 max-w-2xl text-lg leading-8 text-slate-400">
            Upload documents, retrieve relevant sections using semantic search,
            and get grounded answers with transparent sources.
          </p>

          <div className="mt-10 flex flex-wrap gap-4">
            <Link
              href="/documents"
              className="rounded-lg bg-white px-6 py-3 font-medium text-slate-950 transition hover:bg-slate-200"
            >
              Open Documents
            </Link>

            <div className="flex items-center rounded-lg border border-slate-800 px-5 py-3 text-sm text-slate-400">
              Semantic Search · ChromaDB · LLM
            </div>
          </div>

          <div className="mt-16 grid gap-4 sm:grid-cols-3">
            <Feature
              title="Upload"
              description="Process PDF documents into searchable chunks."
            />

            <Feature
              title="Retrieve"
              description="Find semantically relevant document sections."
            />

            <Feature
              title="Answer"
              description="Generate grounded answers with source pages."
            />
          </div>
        </div>
      </div>
    </main>
  );
}

interface FeatureProps {
  title: string;
  description: string;
}

function Feature({ title, description }: FeatureProps) {
  return (
    <div className="rounded-xl border border-slate-800 bg-slate-900/50 p-5">
      <h2 className="font-semibold">{title}</h2>

      <p className="mt-2 text-sm leading-6 text-slate-500">{description}</p>
    </div>
  );
}
