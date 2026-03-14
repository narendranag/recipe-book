.PHONY: dev build sync-youtube sync-notes sync-all

dev:
	npm run dev

build:
	npm run build

sync-youtube:
	cd scripts && python3 ingest_youtube.py

sync-notes:
	osascript scripts/export_notes.applescript
	cd scripts && python3 ingest_notes.py

sync-all: sync-youtube sync-notes

install-scripts:
	pip3 install -r scripts/requirements.txt
