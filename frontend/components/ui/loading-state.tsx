interface LoadingStateProps {
  message?: string;
  className?: string;
}

export function LoadingState({
  message = "Loading...",
  className = "",
}: LoadingStateProps) {
  return (
    <div
      className={[
        "flex flex-col items-center justify-center rounded-xl",
        "border border-slate-800 bg-slate-900 p-10 text-center",
        className,
      ].join(" ")}
    >
      <div className="h-8 w-8 animate-spin rounded-full border-2 border-slate-700 border-t-white" />

      <p className="mt-4 text-sm text-slate-400">{message}</p>
    </div>
  );
}
