import Link from "next/link";

export default function Home() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-50 dark:bg-neutral-900 p-4 gap-6">
      <h1 className="text-4xl font-bold text-gray-900 dark:text-gray-100">Welcome to BOMP</h1>
      <p className="text-gray-600 dark:text-gray-300 text-center max-w-md">
        This is a demo project. Use the buttons below to sign in or create a new account.
      </p>
      <div className="flex gap-4">
        <Link
          href="/login"
          className="px-6 py-2 rounded-md bg-indigo-600 text-white hover:bg-indigo-700 transition-colors"
        >
          Login
        </Link>
        <Link
          href="/register"
          className="px-6 py-2 rounded-md bg-gray-200 text-gray-900 hover:bg-gray-300 dark:bg-neutral-800 dark:text-gray-100 dark:hover:bg-neutral-700 transition-colors"
        >
          Register
        </Link>
      </div>
    </div>
  );
}
