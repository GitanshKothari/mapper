#!/bin/bash
SOURCE="data/processed/"
DEST="frontend/public/data/"

mkdir -p "$DEST"

echo "🔄 Syncing spatial assets to frontend using rsync..."

# Syncing json data with frontend public
rsync -av --include="*.json" --exclude="*" "$SOURCE" "$DEST"

echo "✅ Sync complete."
echo "Current frontend assets:"
ls -lh "$DEST"