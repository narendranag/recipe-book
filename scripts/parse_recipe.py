"""
Shared recipe parser: extracts structured recipe data from unstructured text.
Uses heuristic pattern matching to find ingredients, instructions, and metadata.
"""

import re


def parse_recipe_text(raw_text: str, title: str = "") -> dict:
    """
    Parse unstructured recipe text and extract structured components.

    Returns dict with keys:
        ingredients, instructions, prepTime, cookTime, totalTime,
        servings, tags, category, description
    """
    lines = [line.strip() for line in raw_text.strip().split("\n")]

    ingredients = []
    instructions = []
    description_lines = []
    current_section = None

    # Patterns for section headers
    ingredient_headers = re.compile(
        r"^(ingredients?|what you.?ll need|you.?ll need|shopping list)\s*:?\s*$",
        re.IGNORECASE,
    )
    instruction_headers = re.compile(
        r"^(instructions?|method|directions?|steps?|how to make|preparation|procedure)\s*:?\s*$",
        re.IGNORECASE,
    )
    notes_headers = re.compile(
        r"^(notes?|tips?|cook.?s? notes?)\s*:?\s*$", re.IGNORECASE
    )

    # Patterns for ingredient lines
    quantity_pattern = re.compile(
        r"^[\d½¼¾⅓⅔⅛]|^a (pinch|dash|handful|bunch)|^one |^two |^three ",
        re.IGNORECASE,
    )
    bullet_pattern = re.compile(r"^[-•*]\s+")

    for line in lines:
        if not line:
            continue

        # Detect section headers
        if ingredient_headers.match(line):
            current_section = "ingredients"
            continue
        elif instruction_headers.match(line):
            current_section = "instructions"
            continue
        elif notes_headers.match(line):
            current_section = "notes"
            continue

        # Parse based on current section
        if current_section == "ingredients":
            cleaned = bullet_pattern.sub("", line)
            if cleaned:
                ingredients.append(cleaned)
        elif current_section == "instructions":
            # Remove step numbers
            cleaned = re.sub(r"^\d+[\.\)]\s*", "", line)
            cleaned = bullet_pattern.sub("", cleaned)
            if cleaned:
                instructions.append(cleaned)
        elif current_section is None:
            # Before any section header, treat as description
            # But check if it looks like an ingredient
            cleaned = bullet_pattern.sub("", line)
            if quantity_pattern.match(cleaned):
                current_section = "ingredients"
                ingredients.append(cleaned)
            elif re.match(r"^\d+[\.\)]\s+", line):
                current_section = "instructions"
                cleaned = re.sub(r"^\d+[\.\)]\s*", "", line)
                instructions.append(cleaned)
            else:
                description_lines.append(line)

    # Extract metadata from text
    metadata = extract_metadata(raw_text)

    return {
        "ingredients": ingredients,
        "instructions": instructions,
        "description": " ".join(description_lines[:3]) if description_lines else "",
        **metadata,
    }


def extract_metadata(text: str) -> dict:
    """Extract time, servings, and other metadata from recipe text."""
    metadata = {}

    # Time patterns
    time_pattern = re.compile(
        r"(prep|cook|total)\s*(?:time)?\s*:?\s*(\d+\s*(?:min(?:ute)?s?|hr?s?|hours?))",
        re.IGNORECASE,
    )
    for match in time_pattern.finditer(text):
        key = match.group(1).lower()
        value = match.group(2).strip()
        if key == "prep":
            metadata["prepTime"] = value
        elif key == "cook":
            metadata["cookTime"] = value
        elif key == "total":
            metadata["totalTime"] = value

    # Servings
    servings_match = re.search(
        r"(?:serves?|servings?|yield|makes?)\s*:?\s*(\d+)", text, re.IGNORECASE
    )
    if servings_match:
        metadata["servings"] = servings_match.group(1)

    return metadata


def slugify(text: str) -> str:
    """Convert text to a URL-safe slug."""
    slug = text.lower().strip()
    slug = re.sub(r"[^\w\s-]", "", slug)
    slug = re.sub(r"[\s_]+", "-", slug)
    slug = re.sub(r"-+", "-", slug)
    return slug.strip("-")


if __name__ == "__main__":
    # Test with sample text
    sample = """
    Butter Chicken Recipe

    This is a delicious creamy chicken curry.

    Prep time: 20 minutes
    Cook time: 40 minutes
    Serves: 4

    Ingredients:
    - 500g chicken thighs
    - 1 cup yogurt
    - 2 tbsp butter

    Instructions:
    1. Marinate the chicken in yogurt and spices.
    2. Cook in a pan until golden.
    3. Add tomato sauce and simmer.
    """
    result = parse_recipe_text(sample, "Butter Chicken")
    import json
    print(json.dumps(result, indent=2))
