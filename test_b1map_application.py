#!/usr/bin/env python3
"""
Debug script to check if event-specific B1maps are being applied correctly during simulation
"""

import sys
import yaml
import numpy as np

# Add BlochBuster to path
sys.path.insert(0, 'BlochBuster')

# Patch FFMPEGwriter to avoid import issues
class DummyFFMPEGwriter:
    pass
sys.modules['FFMPEGwriter'] = type(sys)('FFMPEGwriter')
sys.modules['FFMPEGwriter'].FFMPEGwriter = DummyFFMPEGwriter

# Now import BlochBuster
from BlochBuster import checkConfig

# Load config
with open('config/diffusion_RF_grad_coregistered_1d.yml', 'r') as f:
    config = yaml.safe_load(f)

print("Processing configuration...\n")
checkConfig(config)

print("="*70)
print("CHECKING EVENT-SPECIFIC B1MAPS")
print("="*70)

# Check if events have B1maps
has_b1map_events = False
for i, event in enumerate(config['events']):
    if 'B1map' in event:
        has_b1map_events = True
        print(f"\nEvent {i}:")
        print(f"  Time: {event['t']} ms")
        if 'w1' in event:
            print(f"  Has RF pulse (w1 defined)")
        if 'B1map' in event:
            b1map = event['B1map']
            print(f"  B1map type: {type(b1map)}")
            print(f"  B1map shape: {np.array(b1map).shape}")
            print(f"  B1map values:")
            # Print the actual values flattened
            flat = np.array(b1map).flatten()
            print(f"    {flat}")

if not has_b1map_events:
    print("\n⚠️  WARNING: No events have B1map defined!")
    print("   This might be because they were lost during processing")

print("\n" + "="*70)
print("CHECKING GLOBAL CONFIG DIMENSIONS")
print("="*70)
print(f"  nx: {config.get('nx', 'NOT SET')}")
print(f"  ny: {config.get('ny', 'NOT SET')}")
print(f"  nz: {config.get('nz', 'NOT SET')}")

print("\n" + "="*70)
print("CHECKING ORIGINAL PULSE SEQUENCE B1MAPS")
print("="*70)
for i, event in enumerate(config['pulseSeq']):
    if 'B1map' in event:
        print(f"\nPulseSeq Event {i}:")
        print(f"  Time: {event['t']} ms")
        if 'FA' in event:
            print(f"  Flip Angle: {event['FA']}°")
        b1map = event['B1map']
        print(f"  B1map: {b1map}")

print("\n" + "="*70)
print("ANALYSIS")
print("="*70)

# Count how many RF events have B1maps
rf_events_with_b1map = 0
rf_events_total = 0
for event in config['events']:
    if 'w1' in event:
        rf_events_total += 1
        if 'B1map' in event:
            rf_events_with_b1map += 1

print(f"Total RF events: {rf_events_total}")
print(f"RF events with B1map: {rf_events_with_b1map}")

if rf_events_with_b1map < rf_events_total:
    print("\n⚠️  PROBLEM FOUND:")
    print(f"   Some RF events are missing their B1maps!")
    print(f"   {rf_events_with_b1map} out of {rf_events_total} RF events have B1maps")
else:
    print("\n✓ All RF events have B1maps")
    
    # Check if they're different
    b1maps = []
    for event in config['events']:
        if 'w1' in event and 'B1map' in event:
            b1maps.append(np.array(event['B1map']).flatten())
    
    if len(b1maps) >= 2:
        if np.array_equal(b1maps[0], b1maps[1]):
            print("⚠️  PROBLEM: All B1maps have identical values!")
            print(f"   All events use: {b1maps[0]}")
        else:
            print("✓ B1maps have different values (as expected)")
            for idx, b1 in enumerate(b1maps):
                print(f"   Event {idx}: {b1}")
