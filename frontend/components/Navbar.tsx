import Link from "next/link";

export default function Navbar() {
  return (
    <header className="border-b border-foreground/10">
      <nav className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        <Link
          href="/"
          className="text-xl font-bold tracking-widest uppercase hover:opacity-75 transition-opacity"
        >
          Open Hire
        </Link>

        <div className="flex items-center gap-4">
          <Link
            href="/accounts/register"
            className="px-4 py-2 rounded-md text-sm font-medium border border-foreground/20 hover:bg-foreground/5 transition-colors"
          >
            Register
          </Link>

          <button
            type="button"
            aria-label="Profile"
            className="w-9 h-9 rounded-full bg-foreground/10 hover:bg-foreground/20 transition-colors flex items-center justify-center"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
              fill="currentColor"
              className="w-5 h-5 text-foreground/70"
              aria-hidden="true"
            >
              <path
                fillRule="evenodd"
                d="M7.5 6a4.5 4.5 0 1 1 9 0 4.5 4.5 0 0 1-9 0ZM3.751 20.105a8.25 8.25 0 0 1 16.498 0 .75.75 0 0 1-.437.695A18.683 18.683 0 0 1 12 22.5c-2.786 0-5.433-.608-7.812-1.7a.75.75 0 0 1-.437-.695Z"
                clipRule="evenodd"
              />
            </svg>
          </button>
        </div>
      </nav>
    </header>
  );
}
