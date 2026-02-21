import osmium
import json
import os

class POIExtractor(osmium.SimpleHandler):
    def __init__(self):
        super(POIExtractor, self).__init__()
        self.cafes = []

    def node(self, n):
        if n.tags.get('amenity') == 'cafe':
            self.cafes.append({
                'name': n.tags.get('name', 'Unknown Cafe'),
                'lon': n.location.lon,
                'lat': n.location.lat
            })

if __name__ == '__main__':
    # Define paths based on our new project structure
    input_file = '../../data/interim/toronto-exact.osm.pbf'
    output_dir = '../../data/processed'
    output_file = os.path.join(output_dir, 'cafes.json')

    print(f"Scanning {input_file} for Coffee Shops...")
    
    handler = POIExtractor()
    handler.apply_file(input_file)
    
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Save the data to a JSON file
    with open(output_file, 'w') as f:
        json.dump(handler.cafes, f, indent=4)
        
    print(f"Success! Saved {len(handler.cafes)} cafes to {output_file}")