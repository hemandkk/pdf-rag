import type { ChatSource } from "@/lib/types/chat";

import { SourceCard } from "./source-card";

interface ChatMessageProps {
  question: string;
  answer: string;
  sources: ChatSource[];
  isStreaming?: boolean;
}

export function ChatMessage({
  question,
  answer,
  sources,
  isStreaming = false,
}: ChatMessageProps) {
  return (
    <div className="space-y-4">
      <div className="flex justify-end">
        <div className="max-w-[80%] rounded-2xl bg-primary px-4 py-3 text-sm text-primary-foreground">
          {question}
        </div>
      </div>

      <div className="flex justify-start">
        <div className="max-w-[90%] rounded-2xl border bg-card px-5 py-4">
          {answer ? (
            <div className="whitespace-pre-wrap text-sm leading-7">
              {answer}
              {isStreaming && (
                <span className="ml-1 inline-block animate-pulse">▋</span>
              )}
            </div>
          ) : (
            <div className="flex items-center gap-2 text-sm text-muted-foreground">
              <span className="animate-pulse">●</span>

              <span>Generating answer...</span>
            </div>
          )}

          {sources.length > 0 && !isStreaming && (
            <div className="mt-5 space-y-3 border-t pt-4">
              <h3 className="text-sm font-semibold">Sources</h3>

              {sources.map((source, index) => (
                <SourceCard
                  key={`${source.page_number}-${source.chunk_index}-${index}`}
                  source={source}
                  index={index}
                />
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
