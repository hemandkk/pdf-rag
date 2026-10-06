import type { ChatSource } from "@/lib/types/chat";

interface SourceCardProps {
  source: ChatSource;
  index: number;
}

export function SourceCard({ source, index }: SourceCardProps) {
  const similarity = Math.round(source.similarity * 100);

  return (
    <div className="rounded-lg border border-slate-800 bg-slate-950 p-4">
      <div className="flex flex-wrap items-center justify-between gap-2">
        <div className="flex items-center gap-2">
          <span className="rounded-md bg-slate-800 px-2 py-1 text-xs font-medium text-slate-300">
            Source {index + 1}
          </span>

          <span className="text-sm font-medium text-white">
            Page {source.page_number}
          </span>
        </div>

        <span className="text-xs text-slate-500">{similarity}% similarity</span>
      </div>

      <p className="mt-3 whitespace-pre-wrap text-sm leading-6 text-slate-400">
        {source.text}
      </p>

      <p className="mt-3 text-xs text-slate-600">Chunk {source.chunk_index}</p>
    </div>
  );
}
