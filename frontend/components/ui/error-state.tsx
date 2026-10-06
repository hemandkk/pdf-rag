import { Button } from "@/components/ui/button";

interface ErrorStateProps {
  title?: string;
  message?: string;
  onRetry?: () => void;
}

export function ErrorState({
  title = "Something went wrong",
  message = "We couldn't complete the request.",
  onRetry,
}: ErrorStateProps) {
  return (
    <div className="rounded-xl border border-red-900 bg-red-950/30 p-8 text-center">
      <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-red-950 text-xl">
        !
      </div>

      <h3 className="mt-4 font-semibold text-red-200">{title}</h3>

      <p className="mx-auto mt-2 max-w-lg text-sm leading-6 text-red-300/80">
        {message}
      </p>

      {onRetry && (
        <Button
          type="button"
          variant="secondary"
          onClick={onRetry}
          className="mt-5"
        >
          Try again
        </Button>
      )}
    </div>
  );
}
