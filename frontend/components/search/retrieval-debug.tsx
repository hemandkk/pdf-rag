"use client";

import { FormEvent, useState } from "react";

import { useMutation } from "@tanstack/react-query";

import { searchDocument } from "@/lib/api/search";
import { ApiError } from "@/lib/api/client";
import type { SearchResponse } from "@/lib/types/search";

import { SearchResultCard } from "@/components/search/search-result-card";
import { Button } from "@/components/ui/button";

interface RetrievalDebugProps {
  documentId: string;
}

export function RetrievalDebug({ documentId }: RetrievalDebugProps) {
  const [query, setQuery] = useState("");
  const [topK, setTopK] = useState(5);
  const [result, setResult] = useState<SearchResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const searchMutation = useMutation({
    mutationFn: () =>
      searchDocument({
        document_id: documentId,
        query: query.trim(),
        top_k: topK,
      }),

    onSuccess: (response) => {
      setResult(response);
      setError(null);
    },

    onError: (searchError: unknown) => {
      if (searchError instanceof ApiError) {
        setError(searchError.message);
        return;
      }

      if (searchError instanceof Error) {
        setError(searchError.message);
        return;
      }

      setError("Retrieval failed.");
    },
  });

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    if (!query.trim()) {
      setError("Please enter a search query.");
      return;
    }

    setError(null);
    searchMutation.mutate();
  }

  const acceptedCount =
    result?.results.filter((item) => item.accepted).length ?? 0;

  const rejectedCount =
    result?.results.filter((item) => !item.accepted).length ?? 0;

  return (
    <div className="space-y-8">
      <section className="rounded-xl border border-slate-800 bg-slate-900 p-6">
        <div>
          <h2 className="text-lg font-semibold">Test Retrieval</h2>

          <p className="mt-1 text-sm text-slate-400">
            Search the vector database without calling the LLM.
          </p>
        </div>

        <form onSubmit={handleSubmit} className="mt-6 space-y-4">
          <div>
            <label
              htmlFor="retrieval-query"
              className="mb-2 block text-sm font-medium text-slate-300"
            >
              Query
            </label>

            <textarea
              id="retrieval-query"
              value={query}
              onChange={(event) => setQuery(event.target.value)}
              placeholder="What database does the system use?"
              rows={3}
              maxLength={2000}
              className="w-full resize-none rounded-lg border border-slate-700 bg-slate-950 px-4 py-3 text-sm text-white outline-none placeholder:text-slate-600 focus:border-slate-500"
            />
          </div>

          <div className="flex flex-col gap-4 sm:flex-row sm:items-end">
            <div>
              <label
                htmlFor="top-k"
                className="mb-2 block text-sm font-medium text-slate-300"
              >
                Top K
              </label>

              <select
                id="top-k"
                value={topK}
                onChange={(event) => setTopK(Number(event.target.value))}
                className="rounded-lg border border-slate-700 bg-slate-950 px-4 py-2.5 text-sm text-white outline-none focus:border-slate-500"
              >
                {[1, 3, 5, 10, 15, 20].map((value) => (
                  <option key={value} value={value}>
                    {value}
                  </option>
                ))}
              </select>
            </div>

            <Button
              type="submit"
              disabled={searchMutation.isPending || !query.trim()}
            >
              {searchMutation.isPending ? "Searching..." : "Run Retrieval"}
            </Button>
          </div>
        </form>

        {error && (
          <div className="mt-5 rounded-lg border border-red-800 bg-red-950/40 p-4">
            <p className="text-sm text-red-300">{error}</p>
          </div>
        )}
      </section>

      {result && (
        <>
          <section className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            <MetricCard label="Results" value={result.results.length} />

            <MetricCard label="Accepted" value={acceptedCount} />

            <MetricCard label="Rejected" value={rejectedCount} />

            <MetricCard label="Threshold" value={result.threshold.toFixed(2)} />
          </section>

          <section>
            <div className="mb-5">
              <h2 className="text-lg font-semibold">Retrieval Results</h2>

              <p className="mt-1 text-sm text-slate-500">
                Query: `&quot;`{result.query}`&quot;`
              </p>
            </div>

            {result.results.length === 0 ? (
              <div className="rounded-xl border border-dashed border-slate-700 bg-slate-900/50 p-8 text-center">
                <p className="text-sm text-slate-400">
                  No results passed the retrieval query.
                </p>
              </div>
            ) : (
              <div className="space-y-4">
                {result.results.map((item, index) => (
                  <SearchResultCard
                    key={`${item.page_number}-${item.chunk_index}-${index}`}
                    result={item}
                    index={index}
                  />
                ))}
              </div>
            )}
          </section>
        </>
      )}
    </div>
  );
}

interface MetricCardProps {
  label: string;
  value: number | string;
}

function MetricCard({ label, value }: MetricCardProps) {
  return (
    <div className="rounded-xl border border-slate-800 bg-slate-900 p-5">
      <p className="text-xs font-medium uppercase tracking-wide text-slate-500">
        {label}
      </p>

      <p className="mt-2 text-2xl font-bold text-white">{value}</p>
    </div>
  );
}
