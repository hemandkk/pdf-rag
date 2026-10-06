export function DocumentListSkeleton() {
  return (
    <div className="space-y-4" aria-label="Loading documents">
      {Array.from({ length: 3 }).map((_, index) => (
        <div
          key={index}
          className="animate-pulse rounded-xl border border-slate-800 bg-slate-900 p-5"
        >
          <div className="flex items-center gap-4">
            <div className="h-12 w-12 shrink-0 rounded-lg bg-slate-800" />

            <div className="flex-1">
              <div className="h-4 w-1/3 rounded bg-slate-800" />

              <div className="mt-3 h-3 w-1/4 rounded bg-slate-800" />

              <div className="mt-3 h-3 w-1/5 rounded bg-slate-800" />
            </div>

            <div className="h-9 w-20 rounded-lg bg-slate-800" />
          </div>
        </div>
      ))}
    </div>
  );
}
