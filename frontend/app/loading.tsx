import { LoadingState } from "@/components/ui/loading-state";

export default function Loading() {
  return (
    <main className="flex min-h-screen items-center justify-center bg-slate-950 px-6 text-white">
      <LoadingState message="Loading PDF RAG..." className="w-full max-w-md" />
    </main>
  );
}
