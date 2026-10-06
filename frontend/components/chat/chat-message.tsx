import type { ChatResponse } from "@/lib/types/chat";

import { SourceCard } from "@/components/chat/source-card";

interface ChatMessageProps {
  response: ChatResponse;
}

export function ChatMessage({ response }: ChatMessageProps) {
  return (
    <div className="space-y-4">
      <div className="flex justify-end">
        <div className="max-w-3xl rounded-2xl rounded-br-md bg-white px-5 py-3 text-sm leading-6 text-slate-950">
          {response.question}
        </div>
      </div>

      <div className="flex justify-start">
        <div className="w-full max-w-4xl rounded-2xl rounded-bl-md border border-slate-800 bg-slate-900 p-5">
          <div className="flex items-center gap-2">
            <div className="flex h-7 w-7 items-center justify-center rounded-full bg-slate-700 text-sm">
              AI
            </div>

            <span className="text-sm font-medium text-slate-300">
              Assistant
            </span>
          </div>

          <div className="mt-4 whitespace-pre-wrap text-sm leading-7 text-slate-200">
            {response.answer}
          </div>

          {response.sources.length > 0 && (
            <div className="mt-6 border-t border-slate-800 pt-5">
              <h3 className="mb-3 text-sm font-semibold text-white">Sources</h3>

              <div className="space-y-3">
                {response.sources.map((source, index) => (
                  <SourceCard
                    key={`${source.page_number}-${source.chunk_index}-${index}`}
                    source={source}
                    index={index}
                  />
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
