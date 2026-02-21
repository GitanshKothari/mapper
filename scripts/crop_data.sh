#!/bin/bash
set -e

echo "Starting data cropping pipeline..."

# Croping Ontario down to Toronto using the extracted GeoJSON boundary from Overpass Turbo
echo "Cropping to Toronto boundary..."
osmium extract -p data/interim/toronto-boundary.geojson data/raw/ontario-latest.osm.pbf -o data/interim/toronto-exact.osm.pbf --overwrite

echo "Data cropping complete! Output saved to data/interim/toronto-exact.osm.pbf"