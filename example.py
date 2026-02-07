#!/usr/bin/env python3
"""
Example usage of LCP Transformation Accelerator
Demonstrates the complete workflow from extraction to ALM delivery
"""

from lcp_ta.lcp_ta import LCPTransformationAccelerator
from lcp_ta.sap_extractor import SAPConnection
import json


def print_section(title):
    """Print a formatted section header"""
    print("\n" + "=" * 80)
    print(f" {title}")
    print("=" * 80)


def main():
    print("LCP Transformation Accelerator - Example Usage")
    print("=" * 80)
    
    # Initialize LCP TA
    print_section("1. Initialize LCP Transformation Accelerator")
    lcp_ta = LCPTransformationAccelerator(alm_system="jira")
    print("✓ LCP TA initialized with JIRA integration")
    
    # Extract Current State
    print_section("2. Extract Current State from SAP Systems")
    # In production, would connect to real SAP system
    # connection = SAPConnection("ERP_PRD", "sap-erp.example.com", "100")
    # connection.connect()
    current_state = lcp_ta.extract_current_state()
    print(f"✓ Current state extracted at {current_state.timestamp}")
    print(f"  Components: {len(current_state.data.get('components', {}))}")
    print(f"  Dependencies: {len(current_state.data.get('dependencies', []))}")
    
    # Define Intended State
    print_section("3. Define Intended State")
    intent_data = {
        'objectives': [
            {
                'id': 'obj1',
                'name': 'Reduce System Complexity',
                'description': 'Simplify architecture by consolidating components',
                'priority': 'high',
                'metrics': ['component_count', 'coupling_factor']
            },
            {
                'id': 'obj2',
                'name': 'Improve Integration',
                'description': 'Standardize all interfaces',
                'priority': 'medium',
                'metrics': ['interface_standardization']
            }
        ],
        'constraints': [
            {
                'id': 'const1',
                'name': 'Zero Downtime',
                'type': 'availability',
                'value': '99.9%',
                'mandatory': True
            }
        ],
        'target_architecture': {
            'components': [
                {'name': 'ERP_PRD', 'type': 'ERP'},
                {'name': 'BW_PRD', 'type': 'BW'}
            ],
            'layers': ['presentation', 'application', 'integration', 'data'],
            'patterns': ['microservices', 'event-driven']
        }
    }
    intended_state = lcp_ta.define_intended_state(intent_data)
    print(f"✓ Intended state defined at {intended_state.timestamp}")
    print(f"  Objectives: {len(intent_data['objectives'])}")
    print(f"  Constraints: {len(intent_data['constraints'])}")
    
    # Define Reference State (Best Practices)
    print_section("4. Define Reference State (Best Practices)")
    best_practices = {
        'practices': [
            {
                'id': 'bp1',
                'name': 'Loose Coupling',
                'category': 'architecture',
                'description': 'Components should be loosely coupled',
                'applicability': ['all']
            },
            {
                'id': 'bp2',
                'name': 'Interface Standardization',
                'category': 'integration',
                'description': 'Use standard protocols and formats',
                'applicability': ['integration']
            }
        ],
        'patterns': [
            {
                'id': 'pat1',
                'name': 'API Gateway',
                'type': 'integration',
                'structure': {'gateway': 'central', 'backends': 'multiple'},
                'benefits': ['centralized security', 'simplified client']
            }
        ],
        'antipatterns': [
            {
                'id': 'ap1',
                'name': 'Spaghetti Integration',
                'description': 'Point-to-point integrations everywhere',
                'impact': 'high',
                'remediation': 'Use integration hub or event bus'
            }
        ]
    }
    reference_state = lcp_ta.define_reference_state(best_practices)
    print(f"✓ Reference state defined at {reference_state.timestamp}")
    print(f"  Best Practices: {len(best_practices['practices'])}")
    print(f"  Patterns: {len(best_practices['patterns'])}")
    print(f"  Antipatterns: {len(best_practices['antipatterns'])}")
    
    # Analyze and Propose Changes
    print_section("5. Analyze States and Propose Changes")
    analysis = lcp_ta.analyze_and_propose_changes()
    print(f"✓ Analysis completed at {analysis['analysis_time']}")
    print(f"\nDrift Report:")
    if analysis['drift_report']:
        print(f"  Severity: {analysis['drift_report']['severity']}")
        print(f"  Drift Score: {analysis['drift_report']['drift_score']:.2f}")
        print(f"  Drift Items: {len(analysis['drift_report']['drift_items'])}")
    
    print(f"\nComplexity Report:")
    if analysis['complexity_report']:
        print(f"  Overall Complexity: {analysis['complexity_report']['overall_complexity']}")
        print(f"  Hotspots: {len(analysis['complexity_report']['hotspots'])}")
        for hotspot in analysis['complexity_report']['hotspots']:
            print(f"    - {hotspot['type']}: {hotspot['description']}")
    
    print(f"\nChange Options Proposed: {len(analysis['change_options'])}")
    for i, option in enumerate(analysis['change_options'][:5], 1):  # Show first 5
        print(f"  {i}. {option['title']} (Status: {option['governance_status']})")
    
    # Manually approve some options for demonstration
    print_section("6. Approve Change Options")
    approved_count = 0
    for option in analysis['change_options'][:3]:  # Approve first 3 for demo
        if lcp_ta.reasoning_engine.approve_option(option['option_id']):
            approved_count += 1
            print(f"✓ Approved: {option['title']}")
    print(f"\nTotal approved: {approved_count} options")
    
    # Create Delivery Plan
    print_section("7. Create Delivery Plan")
    delivery_plan = lcp_ta.create_delivery_plan()
    if 'error' not in delivery_plan:
        print(f"✓ Delivery plan created: {delivery_plan['plan_id']}")
        print(f"  Total Tasks: {len(delivery_plan['tasks'])}")
        print(f"  Phases: {len(delivery_plan['phases'])}")
        print(f"  Total Effort: {delivery_plan['total_effort']}")
        print(f"  Estimated Duration: {delivery_plan['estimated_duration']}")
        
        print("\nPhases:")
        for phase in delivery_plan['phases']:
            print(f"  Phase {phase['phase']}: {phase['name']} ({len(phase['task_ids'])} tasks)")
    
    # Submit to ALM
    print_section("8. Submit to ALM System")
    submission = lcp_ta.submit_to_alm()
    if 'error' not in submission:
        print(f"✓ Submitted to {submission['alm_system'].upper()}")
        print(f"  Submission ID: {submission['submission_id']}")
        print(f"  Status: {submission['status']}")
        print(f"  ALM References: {len(submission['alm_references'])}")
        
        print("\nCreated ALM Tickets:")
        for ref in submission['alm_references'][:5]:  # Show first 5
            print(f"  - {ref['alm_ticket']}: {ref['url']}")
    
    # Get Full Status
    print_section("9. System Status")
    status = lcp_ta.get_full_status()
    print(f"Timestamp: {status['timestamp']}")
    print(f"\nStates Present:")
    for state_type, state_info in status['states'].items():
        print(f"  - {state_type}: {state_info['timestamp']}")
    
    print(f"\nStatistics:")
    for key, value in status['statistics'].items():
        print(f"  - {key}: {value}")
    
    print_section("Complete!")
    print("LCP Transformation Accelerator has successfully:")
    print("  ✓ Extracted current state from SAP systems")
    print("  ✓ Normalized intent and best practices")
    print("  ✓ Detected drift and complexity")
    print("  ✓ Proposed governed, explainable change options")
    print("  ✓ Created delivery plan")
    print("  ✓ Submitted to ALM for execution")
    print("\nArchitecture insight has been turned into executable transformation!")


if __name__ == "__main__":
    main()
