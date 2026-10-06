import type { DocumentStatus } from "@/lib/types/document";

interface DocumentStatusProps {
  status: DocumentStatus;
}

const statusConfig: Record<
  DocumentStatus,
  {
    label: string;
    className: string;
  }
> = {
  ready: {
    label: "Ready",
    className: "bg-emerald-950 text-emerald-300",
  },
  processing: {
    label: "Processing",
    className: "bg-amber-950 text-amber-300",
  },
  failed: {
    label: "Failed",
    className: "bg-red-950 text-red-300",
  },
};

export function DocumentStatus({ status }: DocumentStatusProps) {
  const config = statusConfig[status];

  return (
    <span
      className={[
        "inline-flex items-center gap-2 rounded-full px-3 py-1",
        "text-xs font-medium",
        config.className,
      ].join(" ")}
    >
      {status === "processing" && (
        <span className="h-1.5 w-1.5 animate-pulse rounded-full bg-current" />
      )}

      {status === "ready" && "✓"}

      {status === "failed" && "!"}

      {config.label}
    </span>
  );
}
