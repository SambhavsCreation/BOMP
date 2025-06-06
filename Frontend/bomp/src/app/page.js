"use client";
import Link from "next/link";
import { motion } from "framer-motion";

export default function Home() {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
      className="flex flex-col items-center justify-center min-h-screen bg-gray-50 dark:bg-neutral-900 p-4 gap-6"
    >
      <motion.h1
        initial={{ y: -20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ delay: 0.2 }}
        className="text-4xl font-bold text-gray-900 dark:text-gray-100"
      >
        Welcome to BOMP
      </motion.h1>

      <p className="text-gray-600 dark:text-gray-300 text-center max-w-md">
        This is a demo project. Use the buttons below to sign in or create a new
        account.
      </p>

      <div className="flex gap-4">
        <motion.div whileHover={{ scale: 1.05 }}>
          <Link
            href="/login"
            className="px-6 py-2 rounded-md bg-indigo-600 text-white hover:bg-indigo-700 transition-colors"
          >
            Login
          </Link>
        </motion.div>
        <motion.div whileHover={{ scale: 1.05 }}>
          <Link
            href="/register"
            className="px-6 py-2 rounded-md bg-gray-200 text-gray-900 hover:bg-gray-300 dark:bg-neutral-800 dark:text-gray-100 dark:hover:bg-neutral-700 transition-colors"
          >
            Register
          </Link>
        </motion.div>
      </div>
    </motion.div>
  );
}