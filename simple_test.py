import yaml

# Simple test to verify config YAML is valid
with open('config/per_event_B1map_demo.yml', 'r') as f:
    config = yaml.safe_load(f)

print('✓ Config loaded successfully!')
print(f'✓ Number of pulse sequence events: {len(config["pulseSeq"])}')
events_with_b1map = sum(1 for e in config['pulseSeq'] if 'B1map' in e)
print(f'✓ Events with B1map: {events_with_b1map}')

if events_with_b1map > 0:
    print('\n✓ Per-event B1map feature configuration is valid!')
    for i, event in enumerate(config['pulseSeq']):
        if 'B1map' in event:
            b1map = event['B1map']
            print(f'  Event {i+1}: B1map with shape [{len(b1map)}][{len(b1map[0])}][{len(b1map[0][0])}]')
