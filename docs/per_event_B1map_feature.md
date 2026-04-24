# Per-Event B1 Map Feature

## Overview

BlochBuster now supports specifying different B1 field maps for individual RF pulses in the pulse sequence. This allows you to simulate scenarios where different RF pulses experience different B1 field inhomogeneities, which can occur in various MRI applications such as:

- Multi-transmit systems with different coil configurations per pulse
- Simulating B1 changes due to subject motion between pulses  
- Different RF pulse types that interact differently with the transmit coil
- Studying the effects of B1 inhomogeneity on complex pulse sequences

## Usage

### Basic Syntax

You can specify a B1map for any RF pulse event in your pulse sequence by adding a `B1map` field to the event:

```yaml
pulseSeq:
  - t: 0
    FA: 90
    dur: 1
    B1map:
      - - [0.8, 0.9, 1.0]
        - [0.9, 1.0, 0.9]
        - [1.0, 0.9, 0.8]
```

### B1map Format

The B1map is specified as a 3D array with dimensions [nz][ny][nx], where each value represents a B1 scaling factor at that spatial location:

- Value of 1.0 = nominal B1 field strength
- Value < 1.0 = reduced B1 field  
- Value > 1.0 = increased B1 field

The B1map must match the spatial dimensions defined by your `locations` configuration.

### Complete Example

```yaml
title: Per-Event B1 Map Example
pulseSeq:
    # 90° excitation pulse with left-side B1 inhomogeneity
    - t: 0
      FA: 90
      dur: 1
      phase: 90
      B1map:
        - - [1.2, 1.0, 0.8]  # Stronger B1 on left, weaker on right
          - [1.2, 1.0, 0.8]
          - [1.2, 1.0, 0.8]
    
    # 180° refocusing pulse with right-side B1 inhomogeneity
    - t: 50
      FA: 180
      dur: 2
      phase: 0
      B1map:
        - - [0.7, 0.9, 1.3]  # Weaker B1 on left, stronger on right
          - [0.7, 0.9, 1.3]
          - [0.7, 0.9, 1.3]

TR: 100
B0: 3.0
nTR: 1

locations:
  - - [1.0, 1.0, 1.0]
    - [1.0, 1.0, 1.0]
    - [1.0, 1.0, 1.0]

components:
  - name: "tissue"
    T1: 1000.0
    T2: 100.0
    CS: 0.0

nIsochromats: 5
locSpacing: 0.02
```

### Backward Compatibility

The feature is fully backward compatible:

1. **Global B1map** (existing behavior): If you specify a top-level `B1map` in your config, it will be applied to all RF pulses that don't have their own B1map:

```yaml
B1map:  # Global B1map applies to all pulses
  - - [0.9, 1.0, 0.9]
    - [1.0, 1.1, 1.0]
    - [0.9, 1.0, 0.9]

pulseSeq:
  - t: 0
    FA: 90
    dur: 1
    # Uses global B1map
```

2. **Mixed usage**: You can use both global and per-event B1maps. Per-event B1maps override the global one:

```yaml
B1map:  # Global fallback
  - - [1.0, 1.0, 1.0]
    - [1.0, 1.0, 1.0]
    - [1.0, 1.0, 1.0]

pulseSeq:
  - t: 0
    FA: 90
    dur: 1
    # Uses global B1map
    
  - t: 50
    FA: 180
    dur: 2
    B1map:  # Overrides global B1map for this pulse only
      - - [0.8, 0.9, 1.1]
        - [0.9, 1.0, 0.9]
        - [1.1, 0.9, 0.8]
```

3. **No B1map**: If neither global nor per-event B1map is specified, uniform B1 field (all 1.0) is assumed.

## Implementation Details

- Per-event B1maps are interpolated to the exact spin position using trilinear interpolation
- The B1 scaling is applied multiplicatively to the RF pulse amplitude
- When events are split into sub-events (for array-valued pulses), the B1map is preserved across sub-events
- Spatial dimensions (nx, ny, nz) must be consistent across all B1maps in the configuration

## Example Configurations

See these demonstration files in the `config/` directory:
- `per_event_B1map_demo.yml` - Basic example with two pulses having different B1 maps
- `B1map_diffusion_demo.yml` - Example using global B1map (original behavior)

## Testing Your Configuration

To verify your configuration is valid before running a full simulation:

```bash
python -c "import yaml; config = yaml.safe_load(open('config/your_config.yml')); print('Valid!' if 'pulseSeq' in config else 'Invalid')"
```
