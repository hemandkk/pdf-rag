import type { SearchResult } from "@/lib/types/search";

interface SearchResultCardProps {
  result: SearchResult;
  index: number;
}

export function SearchResultCard({ result, index }: SearchResultCardProps) {
  const similarity = Math.round(result.similarity * 100);

  return (
    <article
      className={[
        "rounded-xl border p-5",
        result.accepted
          ? "border-emerald-900 bg-emerald-950/20"
          : "border-slate-800 bg-slate-900",
      ].join(" ")}
    >
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div className="flex flex-wrap items-center gap-2">
          <span className="rounded-md bg-slate-800 px-2 py-1 text-xs font-medium text-slate-300">
            #{index + 1}
          </span>

          <span className="rounded-md bg-slate-800 px-2 py-1 text-xs font-medium text-white">
            Page {result.page_number}
          </span>

          <span className="rounded-md bg-slate-800 px-2 py-1 text-xs text-slate-400">
            Chunk {result.chunk_index}
          </span>
        </div>

        <div className="flex items-center gap-3">
          <span
            className={[
              "text-sm font-semibold",
              result.accepted ? "text-emerald-400" : "text-slate-500",
            ].join(" ")}
          >
            {similarity}%
          </span>

          <span
            className={[
              "rounded-full px-3 py-1 text-xs font-medium",
              result.accepted
                ? "bg-emerald-950 text-emerald-300"
                : "bg-slate-800 text-slate-500",
            ].join(" ")}
          >
            {result.accepted ? "Accepted" : "Rejected"}
          </span>
        </div>
      </div>

      <div className="mt-4 rounded-lg bg-slate-950 p-4">
        <p className="whitespace-pre-wrap text-sm leading-7 text-slate-300">
          {result.text}
        </p>
      </div>

      <div className="mt-4">
        <div className="mb-1 flex items-center justify-between text-xs text-slate-500">
          <span>Similarity</span>
          <span>{result.similarity.toFixed(4)}</span>
        </div>

        <div className="h-2 overflow-hidden rounded-full bg-slate-800">
          <div
            className={[
              "h-full rounded-full",
              result.accepted ? "bg-emerald-500" : "bg-slate-600",
            ].join(" ")}
            style={{
              width: `${Math.min(Math.max(similarity, 0), 100)}%`,
            }}
          />
        </div>
      </div>
    </article>
  );
}
