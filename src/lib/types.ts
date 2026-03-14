export interface Recipe {
  slug: string;
  title: string;
  description: string;
  source: "youtube" | "notes" | "manual" | "instagram";
  sourceUrl?: string;
  youtubeVideoId?: string;
  image?: string;
  category: string[];
  cuisine?: string;
  prepTime?: string;
  cookTime?: string;
  totalTime?: string;
  servings?: string;
  ingredients: string[];
  instructions: string[];
  notes?: string;
  author?: string;
  dateAdded: string;
  datePublished?: string;
  tags: string[];
}
