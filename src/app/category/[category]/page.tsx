import { notFound } from "next/navigation";
import { getAllRecipes, getAllCategories } from "@/lib/recipes";
import RecipeGrid from "@/components/RecipeGrid";
import CategoryFilter from "@/components/CategoryFilter";

export async function generateStaticParams() {
  return getAllCategories().map((category) => ({
    category: encodeURIComponent(category),
  }));
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ category: string }>;
}) {
  const { category } = await params;
  const decoded = decodeURIComponent(category);
  return {
    title: `${decoded} Recipes | Nag Family Recipes`,
  };
}

export default async function CategoryPage({
  params,
}: {
  params: Promise<{ category: string }>;
}) {
  const { category } = await params;
  const decoded = decodeURIComponent(category);
  const allRecipes = getAllRecipes();
  const categories = getAllCategories();
  const filtered = allRecipes.filter((r) => r.category.includes(decoded));

  if (filtered.length === 0) notFound();

  return (
    <div>
      <CategoryFilter categories={categories} active={decoded} />
      <h2 className="text-2xl font-semibold mb-6">{decoded}</h2>
      <RecipeGrid recipes={filtered} />
    </div>
  );
}
