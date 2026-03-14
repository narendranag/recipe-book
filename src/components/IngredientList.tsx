"use client";

import { useState } from "react";

export default function IngredientList({
  ingredients,
}: {
  ingredients: string[];
}) {
  const [checked, setChecked] = useState<Set<number>>(new Set());

  const toggle = (index: number) => {
    setChecked((prev) => {
      const next = new Set(prev);
      if (next.has(index)) {
        next.delete(index);
      } else {
        next.add(index);
      }
      return next;
    });
  };

  return (
    <ul className="space-y-3">
      {ingredients.map((ingredient, i) => (
        <li key={i} className="flex items-start gap-3">
          <button
            onClick={() => toggle(i)}
            className={`mt-0.5 w-5 h-5 rounded border-2 flex-shrink-0 flex items-center justify-center transition-colors ${
              checked.has(i)
                ? "bg-accent border-accent text-white"
                : "border-light-gray hover:border-mid-gray"
            }`}
            aria-label={`Mark ${ingredient} as ${checked.has(i) ? "needed" : "done"}`}
          >
            {checked.has(i) && (
              <svg className="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                <path
                  fillRule="evenodd"
                  d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                  clipRule="evenodd"
                />
              </svg>
            )}
          </button>
          <span
            className={`text-sm leading-relaxed ${
              checked.has(i) ? "line-through text-mid-gray" : "text-warm-black"
            }`}
          >
            {ingredient}
          </span>
        </li>
      ))}
    </ul>
  );
}
