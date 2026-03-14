"use client";

import Link from "next/link";

export default function CategoryFilter({
  categories,
  active,
}: {
  categories: string[];
  active?: string;
}) {
  return (
    <div className="flex flex-wrap gap-2 mb-8">
      <Link
        href="/"
        className={`px-4 py-1.5 rounded-full text-sm font-medium transition-colors ${
          !active
            ? "bg-accent text-white"
            : "bg-white text-warm-black border border-light-gray hover:border-mid-gray"
        }`}
      >
        All
      </Link>
      {categories.map((cat) => (
        <Link
          key={cat}
          href={`/category/${encodeURIComponent(cat)}`}
          className={`px-4 py-1.5 rounded-full text-sm font-medium transition-colors ${
            active === cat
              ? "bg-accent text-white"
              : "bg-white text-warm-black border border-light-gray hover:border-mid-gray"
          }`}
        >
          {cat}
        </Link>
      ))}
    </div>
  );
}
