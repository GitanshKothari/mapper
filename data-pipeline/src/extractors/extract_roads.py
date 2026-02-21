import osmium
import json
import os
from src.config import PROCESSED_DATA, TORONTO_PBF

class RoadExtractor(osmium.SimpleHandler):
    def __init__(self):
        super(RoadExtractor, self).__init__()
        self.roads = []

    def way(self, w):
        # 1. Filter: We only want drivable roads
        if 'highway' in w.tags:
            drivable_types = ['motorway', 'trunk', 'primary', 'secondary', 'tertiary', 'residential']
            highway_type = w.tags['highway']
            
            if highway_type in drivable_types:
                try:
                    # 2. Geometry: Map the Node IDs to their actual cached coordinates
                    # We store them as [lon, lat] pairs for easy JSON serialization
                    coords = [[n.location.lon, n.location.lat] for n in w.nodes]
                    
                    self.roads.append({
                        'id': w.id,
                        'name': w.tags.get('name', 'Unnamed Road'),
                        'type': highway_type,
                        'coordinates': coords
                    })
                except osmium.InvalidLocationError:
                    # A road might cross the Toronto border, meaning a node is missing 
                    # from our cropped file. We safely ignore these truncated segments.
                    pass

if __name__ == '__main__':
    output_file = os.path.join(PROCESSED_DATA, 'roads.json')
    os.makedirs(PROCESSED_DATA, exist_ok=True)

    print(f"Extracting road network from {TORONTO_PBF}...")
    print("This might take a few seconds because it has to cache millions of coordinates in RAM...")
    
    handler = RoadExtractor()
    
    # CRITICAL: locations=True tells Pyosmium to cache node coordinates in memory!
    handler.apply_file(TORONTO_PBF, locations=True)
    
    with open(output_file, 'w') as f:
        json.dump(handler.roads, f, indent=4)
        
    print(f"Success! Saved {len(handler.roads)} road segments to {output_file}")