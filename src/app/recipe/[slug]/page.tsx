import { notFound } from "next/navigation";
import Link from "next/link";
import { getAllSlugs, getRecipeBySlug } from "@/lib/recipes";
import YouTubeEmbed from "@/components/YouTubeEmbed";
import IngredientList from "@/components/IngredientList";
import InstructionSteps from "@/components/InstructionSteps";

export async function generateStaticParams() {
  return getAllSlugs().map((slug) => ({ slug }));
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const result = getRecipeBySlug(slug);
  if (!result) return { title: "Recipe Not Found" };
  return {
    title: `${result.recipe.title} | Nag Family Recipes`,
    description: result.recipe.description,
  };
}

export default async function RecipePage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const result = getRecipeBySlug(slug);
  if (!result) notFound();

  const { recipe } = result;

  const jsonLd = {
    "@context": "https://schema.org",
    "@type": "Recipe",
    name: recipe.title,
    description: recipe.description,
    ...(recipe.image && { image: recipe.image }),
    ...(recipe.author && { author: { "@type": "Person", name: recipe.author } }),
    ...(recipe.prepTime && { prepTime: recipe.prepTime }),
    ...(recipe.cookTime && { cookTime: recipe.cookTime }),
    ...(recipe.totalTime && { totalTime: recipe.totalTime }),
    ...(recipe.servings && { recipeYield: recipe.servings }),
    ...(recipe.ingredients.length > 0 && { recipeIngredient: recipe.ingredients }),
    ...(recipe.instructions.length > 0 && {
      recipeInstructions: recipe.instructions.map((step, i) => ({
        "@type": "HowToStep",
        position: i + 1,
        text: step,
      })),
    }),
    ...(recipe.category.length > 0 && { recipeCategory: recipe.category[0] }),
    ...(recipe.cuisine && { recipeCuisine: recipe.cuisine }),
    ...(recipe.datePublished && { datePublished: recipe.datePublished }),
  };

  return (
    <article className="max-w-4xl mx-auto">
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />
      <Link
        href="/"
        className="inline-flex items-center gap-1 text-sm text-mid-gray hover:text-accent mb-6 transition-colors"
      >
        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
        </svg>
        All Recipes
      </Link>

      <header className="mb-8">
        <div className="flex flex-wrap gap-2 mb-3">
          {recipe.category.map((cat) => (
            <Link
              key={cat}
              href={`/category/${encodeURIComponent(cat)}`}
              className="text-xs font-medium text-accent uppercase tracking-wide hover:text-accent-dark"
            >
              {cat}
            </Link>
          ))}
        </div>
        <h1 className="text-4xl md:text-5xl font-bold text-warm-black leading-tight">
          {recipe.title}
        </h1>
        <p className="text-lg text-mid-gray mt-3">{recipe.description}</p>

        <div className="flex flex-wrap items-center gap-6 mt-6 py-4 border-y border-light-gray text-sm text-warm-black">
          {recipe.totalTime && (
            <div>
              <span className="text-mid-gray block text-xs uppercase tracking-wide">
                Total Time
              </span>
              {recipe.totalTime}
            </div>
          )}
          {recipe.prepTime && (
            <div>
              <span className="text-mid-gray block text-xs uppercase tracking-wide">
                Prep
              </span>
              {recipe.prepTime}
            </div>
          )}
          {recipe.cookTime && (
            <div>
              <span className="text-mid-gray block text-xs uppercase tracking-wide">
                Cook
              </span>
              {recipe.cookTime}
            </div>
          )}
          {recipe.servings && (
            <div>
              <span className="text-mid-gray block text-xs uppercase tracking-wide">
                Servings
              </span>
              {recipe.servings}
            </div>
          )}
          {recipe.author && (
            <div>
              <span className="text-mid-gray block text-xs uppercase tracking-wide">
                By
              </span>
              {recipe.author}
            </div>
          )}
        </div>
      </header>

      {recipe.youtubeVideoId && (
        <YouTubeEmbed videoId={recipe.youtubeVideoId} />
      )}

      {recipe.image && (
        <div className="aspect-[16/9] rounded-lg overflow-hidden mb-8 bg-light-gray">
          <img
            src={recipe.image}
            alt={recipe.title}
            className="w-full h-full object-cover"
          />
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-[1fr_2fr] gap-10 mt-8">
        <section>
          <h2 className="text-2xl font-semibold mb-4">Ingredients</h2>
          <IngredientList ingredients={recipe.ingredients} />
        </section>

        <section>
          <h2 className="text-2xl font-semibold mb-4">Instructions</h2>
          <InstructionSteps instructions={recipe.instructions} />
        </section>
      </div>

      {recipe.notes && (
        <section className="mt-10 p-6 bg-white rounded-lg border border-light-gray">
          <h3 className="text-lg font-semibold mb-2">Cook&apos;s Notes</h3>
          <p className="text-sm text-mid-gray leading-relaxed">
            {recipe.notes}
          </p>
        </section>
      )}

      {recipe.sourceUrl && (
        <div className="mt-6 text-sm text-mid-gray">
          <a
            href={recipe.sourceUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="hover:text-accent transition-colors"
          >
            View original source &rarr;
          </a>
        </div>
      )}
    </article>
  );
}
