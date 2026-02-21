import osmium
import json
import os
from src.config import TORONTO_PBF, PROCESSED_DATA

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

    os.makedirs(PROCESSED_DATA, exist_ok=True)
    output_file = os.path.join(PROCESSED_DATA, 'cafes.json')

    print(f"Scanning {TORONTO_PBF} for Coffee Shops...")
    
    handler = POIExtractor()
    handler.apply_file(TORONTO_PBF)

    with open(output_file, 'w') as f:
        json.dump(handler.cafes, f, indent=4)
        
    print(f"Success! Saved {len(handler.cafes)} cafes to {output_file}")