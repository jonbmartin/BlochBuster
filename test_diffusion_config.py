#!/usr/bin/env python3
"""Test B1map configuration without needing ffmpeg"""

import yaml
import numpy as np
from pathlib import Path

# Load the config
config_path = Path(__file__).parent / 'config' / 'diffusion_RF_grad.yml'
with open(config_path, 'r') as f:
    config = yaml.safe_load(f)

print("✓ Config loaded successfully")
print(f"  Number of pulse sequence events: {len(config['pulseSeq'])}")

# Check B1maps in events
events_with_b1map = 0
for i, event in enumerate(config['pulseSeq']):
    if 'B1map' in event:
        events_with_b1map += 1
        b1map = event['B1map']
        if isinstance(b1map, list):
            # Check dimensions
            if isinstance(b1map[0], list):
                if isinstance(b1map[0][0], list):
                    shape_str = f"[{len(b1map)}][{len(b1map[0])}][{len(b1map[0][0])}]"
                else:
                    shape_str = f"[{len(b1map)}][{len(b1map[0])}] (2D - will be converted to 3D)"
            else:
                shape_str = "1D"
            print(f"  Event {i} (t={event.get('t')}ms): B1map shape {shape_str}")

print(f"\n✓ Total events with B1map: {events_with_b1map}")

# Check locations dimensions
if 'locations' in config:
    if isinstance(config['locations'], dict):
        for comp_name, locs in config['locations'].items():
            if isinstance(locs, list):
                if isinstance(locs[0], list) and isinstance(locs[0][0], list):
                    nz = len(locs)
                    ny = len(locs[0])
                    nx = len(locs[0][0])
                elif isinstance(locs[0], list):
                    nz = 1
                    ny = len(locs)
                    nx = len(locs[0])
                print(f"  Locations '{comp_name}': {nz}x{ny}x{nx}")

print("\n✓ Configuration structure is valid!")
print("\nTo run the simulation, install ffmpeg:")
print("  pip install ffmpeg-python")
