.PHONY: dev build sync-youtube sync-notes sync-all rewrite

UV_RUN = uv run --with pyyaml --with beautifulsoup4 --with html2text --with requests --with httpx

dev:
	npm run dev

build:
	npm run build

sync-youtube:
	cd scripts && $(UV_RUN) python ingest_youtube.py

sync-notes:
	osascript scripts/export_notes.applescript
	cd scripts && $(UV_RUN) python ingest_notes.py

rewrite:
	cd scripts && $(UV_RUN) python rewrite_recipes.py

sync-all: sync-youtube sync-notes rewrite
