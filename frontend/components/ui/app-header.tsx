import Link from "next/link";

interface AppHeaderProps {
  title: string;
  description?: string;
  backHref?: string;
  backLabel?: string;
  rightContent?: React.ReactNode;
}

export function AppHeader({
  title,
  description,
  backHref,
  backLabel = "Back",
  rightContent,
}: AppHeaderProps) {
  return (
    <header className="border-b border-slate-800">
      <div className="mx-auto flex max-w-6xl items-center justify-between gap-6 px-6 py-5">
        <div className="min-w-0">
          {backHref && (
            <Link
              href={backHref}
              className="text-sm text-slate-500 transition hover:text-slate-300"
            >
              ← {backLabel}
            </Link>
          )}

          <h1
            className={[
              "font-bold text-white",
              backHref ? "mt-3 text-2xl" : "text-3xl",
            ].join(" ")}
          >
            {title}
          </h1>

          {description && (
            <p className="mt-1 text-sm text-slate-400">{description}</p>
          )}
        </div>

        {rightContent && <div className="shrink-0">{rightContent}</div>}
      </div>
    </header>
  );
}
