# DESIGN.md — Nag Family Recipes

The look of recipes.nag.family as it is built today (2026-11-28), taken from `src/app/globals.css`, `src/app/layout.tsx`, the pages in `src/app/` and the components in `src/components/`. This file replaces the fleet's house design (`~/claude-computer/claude-global/DESIGN.md`) for this site. Anything it doesn't cover falls back to the house file.

## The idea

A cookbook page, NYT Cooking–style: cream paper, a serif display face for titles, a clean sans for everything you read while cooking, and one tomato-red accent for categories, the active filter and the step numbers. Photos carry the colour. The interface is quiet and the recipe is what you look at.

## Tokens

Defined in `@theme inline` in `src/app/globals.css`, used as Tailwind utilities (`bg-cream`, `text-warm-black`, `text-accent` and so on).

| Token | Value | For |
| --- | --- | --- |
| `--color-cream` | `#FAF9F6` | the page background (`body`) |
| `--color-warm-black` | `#1A1A1A` | text |
| `--color-accent` | `#C4372C` | categories, the active filter pill, step numbers, checked boxes, hover on titles and links, the search focus ring |
| `--color-accent-dark` | `#A12D24` | hover on accent-coloured links |
| `--color-light-gray` | `#E8E6E1` | borders, rules, image placeholders |
| `--color-mid-gray` | `#999` | meta, descriptions, labels, placeholder text |
| `--color-card-shadow` | `rgba(0,0,0,0.06)` | defined, unused (see Drift) |
| white (`bg-white`) | `#FFFFFF` | cards, the search input, the inactive pills, the Cook's Notes box |

- **Light only.** There's no dark theme and no `prefers-color-scheme` rule.
- **Shadow:** Tailwind's `shadow-sm` on recipe cards, `shadow-md` on hover. No other shadows.
- **Radius:** `rounded-lg` (8px) for cards, images, the video, the search input and the notes box; `rounded-full` for filter pills and step numbers; `rounded` (4px) for checkboxes and the Video badge.
- **Spacing:** Tailwind's 4px scale. Page gutter `px-4`, main `py-8`, grid gap `gap-6`, card padding `p-4`, `mb-8` between the filter row, the search and the grid.
- **Width:** `max-w-6xl` (1152px) centred for the header, main and footer; a recipe page narrows to `max-w-4xl` (896px).

Compared with the house system: the same warm-paper idea (cream `#FAF9F6` sits next to the house `--canvas` `#fbfaf7`), but its own accent, webfonts, a serif and no state colours.

## Type

Two Google webfonts, loaded in `layout.tsx` with `display=swap`:

- **Playfair Display** 400, 600, 700: `--font-serif`, falling back to Georgia and Times New Roman. Every `h1`–`h4` (set in `globals.css`), plus card titles via `font-serif`.
- **Inter** 400, 500, 600: `--font-sans`, falling back to the system sans. Body and everything else.

| Role | Classes | Size / weight |
| --- | --- | --- |
| Site title (header) | `text-3xl md:text-4xl font-bold tracking-tight` | 30 → 36px, Playfair 700 |
| Recipe title | `text-4xl md:text-5xl font-bold leading-tight` | 36 → 48px, Playfair 700 |
| Section head (Ingredients, Instructions, a category's name) | `text-2xl font-semibold` | 24px, Playfair 600 |
| Card title | `text-lg font-semibold font-serif` | 18px, Playfair 600 |
| Cook's Notes head | `text-lg font-semibold` | 18px, Playfair 600 |
| Recipe description (lede) | `text-lg text-mid-gray` | 18px, Inter 400 |
| Body: ingredients, steps, card description | `text-sm leading-relaxed` | 14px / 1.625 |
| Category label, meta label | `text-xs font-medium uppercase tracking-wide` | 12px, Inter 500, 0.025em |
| Meta (time, servings, footer) | `text-xs` / `text-sm text-mid-gray` | 12–14px |
| Pills | `text-sm font-medium` | 14px, Inter 500 |

The body is antialiased. Headings take the serif; nothing else does, except card titles.

## Layout

- **Header:** centred site title with the strapline "A curated collection of family favorites" in small mid-gray Inter under it; a 1px `light-gray` rule below. The whole block links home.
- **Footer:** a 1px rule above, "Nag Family Recipes" centred in small mid-gray.
- **Home (`/`):** the category filter row, the search box, then the recipe grid (all recipes, or the search results with a "N recipes found" line).
- **Category (`/category/[category]`):** the filter row with that category active, its name as a section head, the grid.
- **Recipe (`/recipe/[slug]`):** a "← All Recipes" back link; the categories as red uppercase links; the title; the description; a meta strip (Total Time, Prep, Cook, Servings, By) between two `light-gray` rules, each a small uppercase label over its value; the YouTube video (16:9) if there is one, otherwise the photo (16:9); then two columns from `md` up, ingredients (1fr) and instructions (2fr); Cook's Notes in a white box; "View original source →".
- **Grid:** 1 column, 2 from `md`, 3 from `lg`.
- The page centres its header and footer text, unlike the house rule.

## Components

- **Recipe card** (`RecipeCard`): white, radius 8, `shadow-sm` → `shadow-md` on hover. A 4:3 image (scales to 105% on hover, .3s); no image shows a light-gray box with a thin plus icon. A YouTube recipe has a "Video" badge top right (`bg-red-600`, white 12px text). Under it: up to two categories in red uppercase, the serif title (red on hover), a two-line clamped description in mid-gray, then total time and "Serves N" in 12px mid-gray.
- **Category filter pill** (`CategoryFilter`): `rounded-full`, `px-4 py-1.5`, 14px medium. Active: accent fill, white text. Inactive: white, 1px `light-gray` border, `mid-gray` border on hover. "All" comes first.
- **Search box** (`SearchBar`): full width, white, 1px `light-gray`, radius 8, `py-3`, a search icon at the left (`pl-12`), a clear (×) button at the right once there's text. Focus: accent border and a 1px accent ring, no outline. Placeholder "Search recipes...". Client-side Fuse.js.
- **Ingredient checklist** (`IngredientList`): a 20px box, 2px `light-gray` border, radius 4; checked, it fills accent with a white tick and the text goes mid-gray and struck through. For ticking things off while cooking.
- **Step number** (`InstructionSteps`): a 32px accent circle with the number in white 14px semibold, the step text beside it; `space-y-6` between steps.
- **Video** (`YouTubeEmbed`): a 16:9 YouTube iframe, radius 8, warm-black behind it.
- **Icons:** inline SVG (Heroicons outline, 2px stroke; solid for the tick and the clear button) in `currentColor`, usually mid-gray. No emoji.
- **Motion:** `transition-colors` on links and pills, `transition-shadow` (.2s) and the image zoom (.3s) on cards. Nothing else moves.

## Imagery

- Photos are the recipe's YouTube thumbnail (the largest the API gives, `maxres` first), saved as JPEG to `public/images/recipes/` by `scripts/ingest_youtube.py`. 38 of the 51 recipes have one; the Apple Notes and hand-made ones mostly don't and get the placeholder.
- Cropped with `object-cover`: 4:3 on cards, 16:9 on the recipe page. No illustration, no stock photography.

## Words

- Warm, plain, family voice: "Nag Family Recipes", "A curated collection of family favorites", "Cook's Notes", "Serves 4".
- Labels in Title Case ("All Recipes", "Total Time", "Ingredients", "Instructions", "View original source"), unlike the house's sentence case.
- Recipe titles, ingredients and steps are cleaned by Claude (`make rewrite`) from the video's text; some titles keep their Hindi.
- Empty state: "No recipes found."

## Drift to decide

1. **The Video badge uses Tailwind's `bg-red-600` (`#DC2626`), not the accent `#C4372C`.** Two reds side by side on a card. Recommend: use `bg-accent`, or keep a YouTube red on purpose and say so here.
2. **`--color-card-shadow` is defined and never used;** cards use Tailwind's `shadow-sm` / `shadow-md`. Recommend: delete the token.
3. **Focus states are uneven.** The search box replaces the outline with an accent ring; pills, checkboxes, the clear button and cards keep the browser default. Recommend: one `:focus-visible` accent outline everywhere (2px, offset 2px).
4. **`mid-gray` `#999` on cream is about 2.7:1,** below 4.5:1, and it carries descriptions, meta, placeholders and checked ingredients. Recommend: darken to about `#6B6B6B` (around 5:1).
5. **Small hit targets for cooking with wet hands:** the 20px checkboxes and the bare clear button. Recommend: make the whole ingredient row the tap target, at least 44px tall on a phone.
6. **The search placeholder uses three dots ("Search recipes...")** where the house uses an ellipsis character. Recommend: "Search recipes…".
7. **No dark theme.** Recommend: leave it; a cookbook on cream is the brand. Revisit only if someone asks.
8. **Leftover Next.js starter files** in `public/` (`file.svg`, `globe.svg`, `next.svg`, `vercel.svg`, `window.svg`) aren't used. Recommend: delete them.
