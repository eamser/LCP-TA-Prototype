"""
Configuration example for LCP Transformation Accelerator
"""

# SAP Connection Configuration
SAP_CONNECTIONS = {
    'production': {
        'system_id': 'ERP_PRD',
        'host': 'sap-erp-prod.example.com',
        'client': '100'
    },
    'quality': {
        'system_id': 'ERP_QAS',
        'host': 'sap-erp-qa.example.com',
        'client': '200'
    }
}

# ALM Integration Configuration
ALM_CONFIG = {
    'system': 'jira',  # Options: jira, azure_devops, servicenow
    'base_url': 'https://jira.example.com',
    'project_key': 'ARCH',
    'default_assignee': 'architecture_team'
}

# Governance Rules
GOVERNANCE_RULES = [
    {
        'name': 'Auto-approve low impact',
        'impact': 'low',
        'action': 'approve'
    },
    {
        'name': 'Require review for high impact',
        'impact': 'high',
        'action': 'pending_review'
    },
    {
        'name': 'Auto-approve drift remediation',
        'option_id_pattern': 'drift_',
        'impact': 'medium',
        'action': 'approve'
    }
]

# Drift Detection Thresholds
DRIFT_THRESHOLDS = {
    'critical': 0.8,
    'high': 0.6,
    'medium': 0.4,
    'low': 0.2
}

# Complexity Thresholds
COMPLEXITY_THRESHOLDS = {
    'coupling_factor': {
        'high': 0.3,
        'medium': 0.2
    },
    'component_count': {
        'high': 50,
        'medium': 30
    },
    'cyclomatic_complexity': {
        'very_high': 150,
        'high': 100,
        'medium': 50
    }
}

# Reference Architecture Best Practices
BEST_PRACTICES = {
    'practices': [
        {
            'id': 'bp_loose_coupling',
            'name': 'Loose Coupling',
            'category': 'architecture',
            'description': 'Components should be loosely coupled to enable independent evolution',
            'applicability': ['all']
        },
        {
            'id': 'bp_api_first',
            'name': 'API-First Design',
            'category': 'integration',
            'description': 'Design APIs before implementation',
            'applicability': ['integration', 'services']
        },
        {
            'id': 'bp_observability',
            'name': 'Built-in Observability',
            'category': 'operations',
            'description': 'Include logging, monitoring, and tracing from the start',
            'applicability': ['all']
        }
    ],
    'patterns': [
        {
            'id': 'pat_api_gateway',
            'name': 'API Gateway',
            'type': 'integration',
            'structure': {
                'gateway': 'central',
                'backends': 'multiple'
            },
            'benefits': [
                'Centralized security',
                'Rate limiting',
                'Simplified client integration'
            ]
        },
        {
            'id': 'pat_event_bus',
            'name': 'Event Bus',
            'type': 'integration',
            'structure': {
                'publishers': 'multiple',
                'subscribers': 'multiple',
                'bus': 'central'
            },
            'benefits': [
                'Loose coupling',
                'Scalability',
                'Event-driven architecture'
            ]
        }
    ],
    'antipatterns': [
        {
            'id': 'ap_spaghetti',
            'name': 'Spaghetti Integration',
            'description': 'Point-to-point integrations everywhere',
            'impact': 'high',
            'remediation': 'Introduce integration hub or event bus'
        },
        {
            'id': 'ap_god_object',
            'name': 'God Object',
            'description': 'Single component doing too many things',
            'impact': 'high',
            'remediation': 'Split into focused components with single responsibility'
        }
    ]
}

# Normalization Rules
NORMALIZATION_RULES = {
    'component_naming': {
        'prefix_removal': ['Z_', 'Y_'],
        'case': 'upper'
    },
    'dependency_types': {
        'RFC': 'remote_function_call',
        'HTTP': 'http_api',
        'IDOC': 'intermediate_document'
    }
}

# Extraction Schedule
EXTRACTION_SCHEDULE = {
    'enabled': True,
    'frequency': 'daily',  # Options: hourly, daily, weekly
    'time': '02:00',  # 2 AM
    'systems': ['production']
}

# Notification Configuration
NOTIFICATION_CONFIG = {
    'enabled': True,
    'channels': ['email', 'slack'],
    'recipients': ['architecture@example.com'],
    'events': [
        'drift_detected_high',
        'drift_detected_critical',
        'complexity_threshold_exceeded',
        'delivery_plan_created',
        'delivery_plan_submitted'
    ]
}
