"use client";
import Link from "next/link";

export default function LoginPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-neutral-900 p-4">
      <div className="max-w-md w-full space-y-8 bg-white dark:bg-neutral-800 rounded-lg shadow-md p-8">
        <div>
          <h2 className="text-center text-3xl font-bold tracking-tight text-gray-900 dark:text-gray-100">
            Sign in to your account
          </h2>
        </div>
        <form className="mt-8 space-y-6">
          <div className="space-y-4">
            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-700 dark:text-gray-200">
                Email address
              </label>
              <input
                id="email"
                name="email"
                type="email"
                required
                className="mt-1 block w-full rounded-md border-gray-300 dark:border-neutral-600 dark:bg-neutral-700 dark:text-gray-100 focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2"
              />
            </div>
            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-700 dark:text-gray-200">
                Password
              </label>
              <input
                id="password"
                name="password"
                type="password"
                required
                className="mt-1 block w-full rounded-md border-gray-300 dark:border-neutral-600 dark:bg-neutral-700 dark:text-gray-100 focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2"
              />
            </div>
          </div>

          <div>
            <button
              type="submit"
              className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
            >
              Sign in
            </button>
          </div>
        </form>
        <p className="mt-2 text-center text-sm text-gray-600 dark:text-gray-300">
          Not registered?{' '}
          <Link href="/register" className="font-medium text-indigo-600 hover:text-indigo-500">
            Sign up
          </Link>
        </p>
      </div>
    </div>
  );
}
