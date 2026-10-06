"use client";

import { useEffect } from "react";

import { Button } from "@/components/ui/button";

interface ErrorPageProps {
  error: Error & {
    digest?: string;
  };
  reset: () => void;
}

export default function ErrorPage({ error, reset }: ErrorPageProps) {
  useEffect(() => {
    console.error(error);
  }, [error]);

  return (
    <main className="flex min-h-screen items-center justify-center bg-slate-950 px-6 text-white">
      <div className="max-w-lg text-center">
        <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-full bg-red-950 text-2xl text-red-400">
          !
        </div>

        <h1 className="mt-6 text-2xl font-bold">Something went wrong</h1>

        <p className="mt-3 text-sm leading-6 text-slate-400">
          An unexpected error occurred while loading this page. You can try
          again.
        </p>

        <Button type="button" onClick={reset} className="mt-6">
          Try again
        </Button>
      </div>
    </main>
  );
}
