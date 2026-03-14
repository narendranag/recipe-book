"use client";

import { useState, useMemo } from "react";
import Fuse from "fuse.js";
import { Recipe } from "@/lib/types";
import RecipeGrid from "./RecipeGrid";

export default function SearchBar({ recipes }: { recipes: Recipe[] }) {
  const [query, setQuery] = useState("");

  const fuse = useMemo(
    () =>
      new Fuse(recipes, {
        keys: [
          { name: "title", weight: 2 },
          { name: "tags", weight: 1.5 },
          { name: "category", weight: 1.5 },
          { name: "cuisine", weight: 1 },
          { name: "ingredients", weight: 0.8 },
          { name: "description", weight: 0.5 },
        ],
        threshold: 0.3,
        includeScore: true,
      }),
    [recipes]
  );

  const results = query.trim()
    ? fuse.search(query).map((r) => r.item)
    : recipes;

  return (
    <div>
      <div className="relative mb-8">
        <svg
          className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-mid-gray"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
          />
        </svg>
        <input
          type="text"
          placeholder="Search recipes..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="w-full pl-12 pr-4 py-3 rounded-lg border border-light-gray bg-white text-warm-black placeholder:text-mid-gray focus:outline-none focus:border-accent focus:ring-1 focus:ring-accent transition-colors"
        />
        {query && (
          <button
            onClick={() => setQuery("")}
            className="absolute right-4 top-1/2 -translate-y-1/2 text-mid-gray hover:text-warm-black"
          >
            <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
              <path
                fillRule="evenodd"
                d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                clipRule="evenodd"
              />
            </svg>
          </button>
        )}
      </div>
      {query && (
        <p className="text-sm text-mid-gray mb-4">
          {results.length} {results.length === 1 ? "recipe" : "recipes"} found
        </p>
      )}
      <RecipeGrid recipes={results} />
    </div>
  );
}
