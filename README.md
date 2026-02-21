# Mapper 🗺️

## Motivation

Most "Full Stack" map applications rely on abstraction layers like Leaflet, Mapbox, or Google Maps APIs. While these tools are excellent for rapid development, they hide the underlying systems engineering and spatial mathematics required to make a map actually work.

The goal of this project is to peel back those layers and build a functional, scaled-down routing engine from scratch. By refusing to use pre-built mapping libraries, this project focuses on the raw data engineering, graph theory (A\* pathfinding), and geometry needed to parse raw geographic data and render a navigable network on a custom canvas. It is a deep dive into how routing systems operate under the hood.

## Architecture

- **Data Ingestion:** C++ `osmium-tool` for high-performance spatial cropping of raw Protocolbuffer Binary Format (.pbf) files.
- **Extraction:** Python (`pyosmium`) to parse OpenStreetMap Nodes and Ways, resolving coordinate dependencies in memory.
- **Graph Engine:** (In Progress) A\* routing utilizing `networkx` to calculate the shortest path across physical road segments using the Haversine formula.
- **Renderer:** (In Progress) Custom Web Mercator projection to translate spherical geographic coordinates to a 2D HTML5 `<canvas>` / WebGL context.

## Setup & Data Acquisition

To make the routing engine lightweight and performant, the massive OpenStreetMap planet dataset was cropped down exclusively to the Greater Toronto Area.

### 1. Acquiring the Raw Data

1. **Regional Extract:** Downloaded the latest `ontario-latest.osm.pbf` file from the [Geofabrik Download Server](https://download.geofabrik.de/north-america/canada/ontario.html) and save it in `data/raw/`.
2. **Municipal Boundary:** To avoid routing through Lake Ontario or neighboring cities, the exact municipal boundary polygon for Toronto was extracted.
   - This was done using **Overpass Turbo** (`overpass-turbo.eu`) with the query `rel(324211); out geom;`. `324211` is the code for Toronto.
   - The boundary was exported and saved as `toronto-boundary.geojson` in `data/interim/`.

### 2. Preprocessing the Dataset

With the Ontario `.pbf` file and the Toronto `.geojson` boundary in hand, the dataset was cropped using the C++ `osmium-tool`.
Run the automated bash script to generate the localized dataset:

```bash
bash scripts/crop_data.sh
```

This command outputs a lightweight `toronto-exact.osm.pbf` file to the `data/interim/` directory.

### 3. Running the Extractors

Install the Python dependencies:

```bash
pip3 install -r requirements.txt
```

Run the extraction scripts to parse the binary data into flat JSON files for the routing graph:

```bash
python3 src/extractors/extract_pois.py
```

## Project Structure

This repository is structured as follows:

```text
toronto-routing-engine/
│
├── data/ # (Ignored by Git)
│ ├── raw/ # Contains 'ontario-latest.osm.pbf'
│ ├── interim/ # Contains the cropped 'toronto-exact.osm.pbf' and the GeoJSON boundary
│ └── processed/ # Extracted JSON files (cafes.json) ready for routing
│
├── src/
│ ├── extractors/ # Python scripts for parsing raw OSM Nodes and Ways
│ │ ├── extract_pois.py
│ │
│ │
│ ├── graph/ # (Coming Soon) NetworkX A\* routing logic
│ │
│ └── api/ # (Coming Soon) Backend server to serve map tiles and routes
│
├── scripts/ # Bash scripts for automated data processing
│ └── crop_data.sh
│
├── .gitignore # Prevents tracking of massive .pbf and .json files
├── requirements.txt # Python dependencies
└── README.md
```
