import { getAllRecipes, getAllCategories } from "@/lib/recipes";
import SearchBar from "@/components/SearchBar";
import CategoryFilter from "@/components/CategoryFilter";

export default function Home() {
  const recipes = getAllRecipes();
  const categories = getAllCategories();

  return (
    <div>
      <CategoryFilter categories={categories} />
      <SearchBar recipes={recipes} />
    </div>
  );
}
