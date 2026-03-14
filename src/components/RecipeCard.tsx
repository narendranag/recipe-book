import Link from "next/link";
import { Recipe } from "@/lib/types";

export default function RecipeCard({ recipe }: { recipe: Recipe }) {
  return (
    <Link href={`/recipe/${recipe.slug}`} className="group block">
      <article className="bg-white rounded-lg overflow-hidden shadow-sm hover:shadow-md transition-shadow duration-200">
        <div className="aspect-[4/3] bg-light-gray relative overflow-hidden">
          {recipe.image ? (
            <img
              src={recipe.image}
              alt={recipe.title}
              className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
            />
          ) : (
            <div className="w-full h-full flex items-center justify-center text-mid-gray">
              <svg
                className="w-16 h-16"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={1}
                  d="M12 6v6m0 0v6m0-6h6m-6 0H6"
                />
              </svg>
            </div>
          )}
          {recipe.source === "youtube" && (
            <div className="absolute top-3 right-3 bg-red-600 text-white text-xs px-2 py-1 rounded">
              Video
            </div>
          )}
        </div>
        <div className="p-4">
          <div className="flex flex-wrap gap-1.5 mb-2">
            {recipe.category.slice(0, 2).map((cat) => (
              <span
                key={cat}
                className="text-xs font-medium text-accent uppercase tracking-wide"
              >
                {cat}
              </span>
            ))}
          </div>
          <h2 className="text-lg font-semibold text-warm-black group-hover:text-accent transition-colors font-serif">
            {recipe.title}
          </h2>
          <p className="text-sm text-mid-gray mt-1 line-clamp-2">
            {recipe.description}
          </p>
          <div className="flex items-center gap-3 mt-3 text-xs text-mid-gray">
            {recipe.totalTime && <span>{recipe.totalTime}</span>}
            {recipe.servings && <span>Serves {recipe.servings}</span>}
          </div>
        </div>
      </article>
    </Link>
  );
}
