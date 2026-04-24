#!/usr/bin/env python3
"""
Test to demonstrate the bug BEFORE the fix
"""

import yaml

# Read the config file
with open('config/diffusion_RF_grad_coregistered_1d.yml', 'r') as f:
    config = yaml.safe_load(f)

print("Demonstrating the ORIGINAL BUG (without the fix):\n")
print("="*60)

def arrangeLocations_BUGGY(slices, config, key='locations'):
    '''Original buggy version - doesn't restore nx, ny, nz'''
    if not isinstance(slices, list):
        raise Exception('Expected list in config "{}", not {}'.format(key, type(slices)))
    if not isinstance(slices[0], list):
        slices = [slices]
    if not isinstance(slices[0][0], list):
        slices = [slices]
    
    if 'nz' not in config:
        config['nz'] = len(slices)
    elif len(slices)!=config['nz']:
        raise Exception('Config "{}": number of slices do not match. Expected nz={}, got {}'.format(key, config['nz'], len(slices)))
    if 'ny' not in config:
        config['ny'] = len(slices[0])
    elif len(slices[0])!=config['ny']:
        raise Exception('Config "{}": number of rows do not match. Expected ny={}, got {}'.format(key, config['ny'], len(slices[0])))
    if 'nx' not in config:
        config['nx'] = len(slices[0][0])
    elif len(slices[0][0])!=config['nx']:
        raise Exception('Config "{}": number of elements do not match. Expected nx={}, got {}'.format(key, config['nx'], len(slices[0][0])))
    return slices

test_config = {'TR': 80}

# First event B1map
b1map1 = [[1.75, 1.50, 1.25, 1, .75, .50, 0.25]]
print("Processing Event 1 B1map (90° pulse):")
print(f"  Input: {b1map1}")

# This is what the BUGGY code does - stores but doesn't restore
temp_nx = test_config.get('nx')
temp_ny = test_config.get('ny')
temp_nz = test_config.get('nz')
print(f"  Stored temp values: nx={temp_nx}, ny={temp_ny}, nz={temp_nz}")

arranged1 = arrangeLocations_BUGGY(b1map1, test_config, 'B1map')
print(f"  After arranging: nx={test_config['nx']}, ny={test_config['ny']}, nz={test_config['nz']}")
print(f"  ⚠️  BUG: temp values are NOT restored! Global config now has Event 1's dimensions")

# Second event B1map - this would fail or use Event 1's dimensions
b1map2 = [[1, 1, 1, 1, 1, 1, 1]]
print("\nProcessing Event 2 B1map (180° pulse):")
print(f"  Input: {b1map2}")

temp_nx = test_config.get('nx')
temp_ny = test_config.get('ny')
temp_nz = test_config.get('nz')
print(f"  Stored temp values: nx={temp_nx}, ny={temp_ny}, nz={temp_nz}")
print(f"  ⚠️  BUG: Event 1's dimensions are still in config!")

try:
    arranged2 = arrangeLocations_BUGGY(b1map2, test_config, 'B1map')
    print(f"  After arranging: nx={test_config['nx']}, ny={test_config['ny']}, nz={test_config['nz']}")
    print(f"  ⚠️  BUG: Both events forced to use the SAME dimensions (7x1x1)")
    print(f"  ⚠️  This means Event 2's B1map cannot be truly independent!")
except Exception as e:
    print(f"  ✗ ERROR: {e}")

print("\n" + "="*60)
print("\nSUMMARY OF THE BUG:")
print("  • First event's B1map dimensions (7x1x1) were stored in global config")
print("  • When processing second event's B1map, it checks against these global dims")  
print("  • Both B1maps are forced to match the same nx, ny, nz")
print("  • This prevents truly independent B1 profiles per event")
print("\nTHE FIX:")
print("  • Temporarily REMOVE nx, ny, nz from config before processing each event")
print("  • Let arrangeLocations set new dimensions for that event")
print("  • RESTORE original nx, ny, nz values after processing")
print("  • This allows each event to have its own independent B1map dimensions")
