"use client";

import { FormEvent, useState } from "react";

import { Button } from "@/components/ui/button";

interface ChatInputProps {
  onSubmit: (question: string) => void;
  disabled?: boolean;
}

export function ChatInput({ onSubmit, disabled = false }: ChatInputProps) {
  const [question, setQuestion] = useState("");

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    const trimmedQuestion = question.trim();

    if (!trimmedQuestion || disabled) {
      return;
    }

    onSubmit(trimmedQuestion);
    setQuestion("");
  }

  return (
    <form
      onSubmit={handleSubmit}
      className="border-t border-slate-800 bg-slate-950/95 p-4 backdrop-blur"
    >
      <div className="mx-auto flex max-w-4xl gap-3">
        <textarea
          value={question}
          onChange={(event) => setQuestion(event.target.value)}
          onKeyDown={(event) => {
            if (event.key === "Enter" && !event.shiftKey) {
              event.preventDefault();

              const trimmedQuestion = question.trim();

              if (trimmedQuestion && !disabled) {
                onSubmit(trimmedQuestion);
                setQuestion("");
              }
            }
          }}
          placeholder="Ask a question about this document..."
          disabled={disabled}
          rows={2}
          maxLength={2000}
          className="min-h-12 flex-1 resize-none rounded-xl border border-slate-700 bg-slate-900 px-4 py-3 text-sm text-white outline-none placeholder:text-slate-500 focus:border-slate-500 disabled:opacity-50"
        />

        <Button
          type="submit"
          disabled={disabled || !question.trim()}
          className="self-end"
        >
          {disabled ? "Thinking..." : "Ask"}
        </Button>
      </div>

      <p className="mx-auto mt-2 max-w-4xl text-xs text-slate-600">
        Enter to send · Shift + Enter for a new line
      </p>
    </form>
  );
}
