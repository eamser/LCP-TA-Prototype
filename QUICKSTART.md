# Quick Start Guide - LCP Transformation Accelerator

## Installation

```bash
# Clone the repository
git clone https://github.com/eamser/LCP-TA-Prototype.git
cd LCP-TA-Prototype

# Install dependencies
pip install -r requirements.txt

# Or install as package
pip install -e .
```

## 5-Minute Quick Start

### 1. Run the Example

```bash
python example.py
```

This demonstrates the complete workflow from SAP extraction to ALM delivery.

### 2. Basic Usage

```python
from lcp_ta.lcp_ta import LCPTransformationAccelerator

# Initialize
lcp_ta = LCPTransformationAccelerator(alm_system="jira")

# Extract current state
current = lcp_ta.extract_current_state()
print(f"Extracted {len(current.data.get('components', {}))} components")

# Define intended state
intent = {
    'objectives': [
        {
            'id': 'obj1',
            'name': 'Reduce Complexity',
            'description': 'Simplify architecture',
            'priority': 'high'
        }
    ],
    'constraints': [],
    'target_architecture': {
        'components': [],
        'layers': ['presentation', 'business', 'data']
    }
}
intended = lcp_ta.define_intended_state(intent)

# Analyze and get recommendations
analysis = lcp_ta.analyze_and_propose_changes()
print(f"Detected {analysis['summary']['drift_severity']} drift")
print(f"Found {len(analysis['change_options'])} change options")

# Approve some options
for option in analysis['change_options'][:3]:
    lcp_ta.reasoning_engine.approve_option(option['option_id'])
    print(f"Approved: {option['title']}")

# Create delivery plan
plan = lcp_ta.create_delivery_plan()
print(f"Created plan with {len(plan['tasks'])} tasks")

# Submit to ALM
submission = lcp_ta.submit_to_alm()
print(f"Submitted to {submission['alm_system']}")
```

## Common Use Cases

### Use Case 1: Check Current Architecture Compliance

```python
from lcp_ta.lcp_ta import LCPTransformationAccelerator

lcp_ta = LCPTransformationAccelerator()

# Extract current
current = lcp_ta.extract_current_state()

# Define reference architecture
reference_arch = {
    'practices': [
        {
            'id': 'bp1',
            'name': 'Microservices',
            'category': 'architecture',
            'description': 'Use microservices pattern'
        }
    ]
}
reference = lcp_ta.define_reference_state(reference_arch)

# Check compliance
sync = lcp_ta.synchronize_states()
if sync['drift_detected']:
    print("⚠️ Drift from reference architecture detected!")
    for drift in sync['drift_detected']:
        print(f"  - {drift['type']}")
```

### Use Case 2: Plan S/4HANA Migration

```python
from lcp_ta.lcp_ta import LCPTransformationAccelerator

lcp_ta = LCPTransformationAccelerator(alm_system="jira")

# 1. Baseline current ECC system
current = lcp_ta.extract_current_state()

# 2. Define S/4HANA target
s4hana_target = {
    'objectives': [
        {
            'id': 'migrate_s4',
            'name': 'Migrate to S/4HANA',
            'priority': 'critical'
        }
    ],
    'target_architecture': {
        'components': [
            {'name': 'S4HANA', 'type': 'ERP', 'version': '2023'}
        ]
    }
}
intended = lcp_ta.define_intended_state(s4hana_target)

# 3. Analyze migration path
analysis = lcp_ta.analyze_and_propose_changes()

# 4. Create migration plan
# (Review and approve options manually)
plan = lcp_ta.create_delivery_plan()
submission = lcp_ta.submit_to_alm()

print(f"Migration plan created with {len(plan['phases'])} phases")
print(f"Estimated duration: {plan['estimated_duration']}")
```

### Use Case 3: Continuous Architecture Monitoring

```python
from lcp_ta.lcp_ta import LCPTransformationAccelerator
import schedule
import time

lcp_ta = LCPTransformationAccelerator()

def monitor_architecture():
    """Run daily architecture check"""
    # Extract current state
    current = lcp_ta.extract_current_state()
    
    # Check synchronization
    sync = lcp_ta.synchronize_states()
    
    # Alert if critical drift
    if sync.get('drift_detected'):
        for drift in sync['drift_detected']:
            if drift.get('type') == 'current_vs_intended':
                print("🔔 Architecture drift detected!")
                # Send alert to team
                
    # Analyze complexity
    analysis = lcp_ta.analyze_and_propose_changes()
    complexity = analysis.get('complexity_report', {})
    
    if complexity.get('overall_complexity') in ['high', 'very_high']:
        print("⚠️ High complexity detected!")
        # Create remediation plan

# Schedule daily monitoring
schedule.every().day.at("02:00").do(monitor_architecture)

while True:
    schedule.run_pending()
    time.sleep(3600)  # Check every hour
```

## Running Tests

```bash
# Run all tests
python -m unittest tests.test_lcp_ta -v

# Run specific test class
python -m unittest tests.test_lcp_ta.TestStateManager -v

# Run with coverage (if pytest-cov installed)
pytest tests/ --cov=lcp_ta --cov-report=html
```

## Configuration

Copy and customize the example configuration:

```bash
cp config_example.py config.py
# Edit config.py with your settings
```

Key configuration areas:
- SAP connections
- ALM integration
- Governance rules
- Drift/complexity thresholds
- Best practices

## Troubleshooting

### Issue: "No module named 'lcp_ta'"

**Solution**: Install the package or add to PYTHONPATH
```bash
pip install -e .
# or
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### Issue: SAP connection fails

**Solution**: Check network connectivity and credentials
```python
from lcp_ta.sap_extractor import SAPConnection
conn = SAPConnection("SID", "host", "client")
success = conn.connect()
print(f"Connected: {success}")
```

### Issue: No change options generated

**Solution**: Ensure both current and intended states are defined
```python
# Must have both states
lcp_ta.extract_current_state()
lcp_ta.define_intended_state(intent_data)

# Then analyze
analysis = lcp_ta.analyze_and_propose_changes()
```

## Next Steps

1. **Explore the Example**: Run `python example.py` to see the full workflow
2. **Read Documentation**: Check `ARCHITECTURE.md` for detailed design
3. **Customize Configuration**: Adapt `config_example.py` to your needs
4. **Integrate with Your Systems**: Connect to real SAP and ALM systems
5. **Extend**: Add custom extractors, rules, and analyzers

## Getting Help

- **Documentation**: See `README.md` and `ARCHITECTURE.md`
- **Examples**: Check `example.py` for usage patterns
- **Tests**: Review `tests/test_lcp_ta.py` for API examples
- **Issues**: Report issues on GitHub

## Resources

- **GitHub**: https://github.com/eamser/LCP-TA-Prototype
- **Documentation**: See `ARCHITECTURE.md`
- **Examples**: See `example.py`

Happy architecting! 🚀
