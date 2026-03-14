import fs from "fs";
import path from "path";
import matter from "gray-matter";
import { Recipe } from "./types";

const recipesDirectory = path.join(process.cwd(), "content/recipes");

function getRecipeFiles(dir: string): string[] {
  if (!fs.existsSync(dir)) return [];
  const files: string[] = [];
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      files.push(...getRecipeFiles(fullPath));
    } else if (entry.name.endsWith(".mdx")) {
      files.push(fullPath);
    }
  }
  return files;
}

export function getAllRecipes(): Recipe[] {
  const files = getRecipeFiles(recipesDirectory);
  const recipes = files.map((filePath) => {
    const fileContents = fs.readFileSync(filePath, "utf8");
    const { data } = matter(fileContents);
    return {
      slug: data.slug || path.basename(filePath, ".mdx"),
      title: data.title || "Untitled Recipe",
      description: data.description || "",
      source: data.source || "manual",
      sourceUrl: data.sourceUrl,
      youtubeVideoId: data.youtubeVideoId,
      image: data.image,
      category: data.category || [],
      cuisine: data.cuisine,
      prepTime: data.prepTime,
      cookTime: data.cookTime,
      totalTime: data.totalTime,
      servings: data.servings,
      ingredients: data.ingredients || [],
      instructions: data.instructions || [],
      notes: data.notes,
      author: data.author,
      dateAdded: data.dateAdded || new Date().toISOString().split("T")[0],
      datePublished: data.datePublished,
      tags: data.tags || [],
    } as Recipe;
  });

  return recipes.sort(
    (a, b) => new Date(b.dateAdded).getTime() - new Date(a.dateAdded).getTime()
  );
}

export function getRecipeBySlug(slug: string): {
  recipe: Recipe;
  content: string;
} | null {
  const files = getRecipeFiles(recipesDirectory);
  for (const filePath of files) {
    const fileContents = fs.readFileSync(filePath, "utf8");
    const { data, content } = matter(fileContents);
    const fileSlug = data.slug || path.basename(filePath, ".mdx");
    if (fileSlug === slug) {
      return {
        recipe: {
          slug: fileSlug,
          title: data.title || "Untitled Recipe",
          description: data.description || "",
          source: data.source || "manual",
          sourceUrl: data.sourceUrl,
          youtubeVideoId: data.youtubeVideoId,
          image: data.image,
          category: data.category || [],
          cuisine: data.cuisine,
          prepTime: data.prepTime,
          cookTime: data.cookTime,
          totalTime: data.totalTime,
          servings: data.servings,
          ingredients: data.ingredients || [],
          instructions: data.instructions || [],
          notes: data.notes,
          author: data.author,
          dateAdded:
            data.dateAdded || new Date().toISOString().split("T")[0],
          datePublished: data.datePublished,
          tags: data.tags || [],
        } as Recipe,
        content,
      };
    }
  }
  return null;
}

export function getAllCategories(): string[] {
  const recipes = getAllRecipes();
  const categories = new Set<string>();
  recipes.forEach((r) => r.category.forEach((c) => categories.add(c)));
  return Array.from(categories).sort();
}

export function getAllSlugs(): string[] {
  return getAllRecipes().map((r) => r.slug);
}
