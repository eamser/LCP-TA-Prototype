"""
SAP Fact Extractor Module
Extracts facts from live SAP systems
"""

from typing import Dict, Any, List, Optional
from datetime import datetime


class SAPConnection:
    """Represents a connection to an SAP system"""
    
    def __init__(self, system_id: str, host: str, client: str):
        self.system_id = system_id
        self.host = host
        self.client = client
        self.connected = False
    
    def connect(self) -> bool:
        """Connect to SAP system (simulated)"""
        # In production, this would establish actual SAP RFC connection
        self.connected = True
        return True
    
    def disconnect(self) -> None:
        """Disconnect from SAP system"""
        self.connected = False


class SAPFactExtractor:
    """Extracts architectural facts from SAP systems"""
    
    def __init__(self, connection: Optional[SAPConnection] = None):
        self.connection = connection
        self.extraction_history: List[Dict[str, Any]] = []
    
    def extract_system_landscape(self) -> Dict[str, Any]:
        """Extract SAP system landscape information"""
        landscape = {
            'extraction_time': datetime.utcnow().isoformat(),
            'systems': [],
            'connections': [],
            'metadata': {}
        }
        
        if self.connection and self.connection.connected:
            # Simulate extraction from real SAP system
            landscape['systems'].append({
                'system_id': self.connection.system_id,
                'host': self.connection.host,
                'client': self.connection.client,
                'status': 'active'
            })
        else:
            # Return example data when not connected
            landscape['systems'] = [
                {
                    'system_id': 'ERP_PRD',
                    'host': 'sap-erp-prod.example.com',
                    'client': '100',
                    'status': 'active',
                    'type': 'ERP',
                    'version': 'S/4HANA 2021'
                },
                {
                    'system_id': 'BW_PRD',
                    'host': 'sap-bw-prod.example.com',
                    'client': '100',
                    'status': 'active',
                    'type': 'BW',
                    'version': 'BW/4HANA 2.0'
                }
            ]
            
            landscape['connections'] = [
                {
                    'source': 'ERP_PRD',
                    'target': 'BW_PRD',
                    'type': 'RFC',
                    'protocol': 'SAP RFC'
                }
            ]
        
        self._record_extraction('system_landscape', landscape)
        return landscape
    
    def extract_custom_code(self) -> Dict[str, Any]:
        """Extract custom code artifacts"""
        custom_code = {
            'extraction_time': datetime.utcnow().isoformat(),
            'programs': [],
            'function_modules': [],
            'classes': [],
            'statistics': {}
        }
        
        # Simulate custom code extraction
        custom_code['programs'] = [
            {
                'name': 'Z_CUSTOM_REPORT',
                'type': 'REPORT',
                'author': 'DEVELOPER1',
                'lines_of_code': 450,
                'last_changed': '2024-01-15'
            }
        ]
        
        custom_code['function_modules'] = [
            {
                'name': 'Z_CUSTOM_FUNCTION',
                'function_group': 'ZCUSTOM',
                'complexity': 'medium'
            }
        ]
        
        custom_code['statistics'] = {
            'total_programs': len(custom_code['programs']),
            'total_function_modules': len(custom_code['function_modules']),
            'total_classes': len(custom_code['classes'])
        }
        
        self._record_extraction('custom_code', custom_code)
        return custom_code
    
    def extract_interfaces(self) -> Dict[str, Any]:
        """Extract interface configurations"""
        interfaces = {
            'extraction_time': datetime.utcnow().isoformat(),
            'rfc_destinations': [],
            'idocs': [],
            'web_services': []
        }
        
        # Simulate interface extraction
        interfaces['rfc_destinations'] = [
            {
                'name': 'BW_RFC_DEST',
                'target_system': 'BW_PRD',
                'connection_type': 'RFC',
                'status': 'active'
            }
        ]
        
        interfaces['idocs'] = [
            {
                'message_type': 'ORDERS05',
                'direction': 'outbound',
                'partner': 'VENDOR_001'
            }
        ]
        
        self._record_extraction('interfaces', interfaces)
        return interfaces
    
    def extract_customizing(self) -> Dict[str, Any]:
        """Extract system customizing/configuration"""
        customizing = {
            'extraction_time': datetime.utcnow().isoformat(),
            'company_codes': [],
            'plants': [],
            'sales_organizations': []
        }
        
        # Simulate customizing extraction
        customizing['company_codes'] = [
            {
                'code': '1000',
                'name': 'Company Code 1000',
                'country': 'US',
                'currency': 'USD'
            }
        ]
        
        customizing['plants'] = [
            {
                'plant': '1010',
                'name': 'Plant Houston',
                'company_code': '1000'
            }
        ]
        
        self._record_extraction('customizing', customizing)
        return customizing
    
    def extract_all_facts(self) -> Dict[str, Any]:
        """Extract all available facts from SAP system"""
        all_facts = {
            'extraction_time': datetime.utcnow().isoformat(),
            'system_landscape': self.extract_system_landscape(),
            'custom_code': self.extract_custom_code(),
            'interfaces': self.extract_interfaces(),
            'customizing': self.extract_customizing()
        }
        
        return all_facts
    
    def _record_extraction(self, extraction_type: str, data: Dict[str, Any]) -> None:
        """Record extraction in history"""
        self.extraction_history.append({
            'timestamp': datetime.utcnow().isoformat(),
            'type': extraction_type,
            'record_count': len(data) if isinstance(data, list) else sum(
                len(v) if isinstance(v, list) else 0 
                for v in data.values() if isinstance(v, list)
            )
        })
    
    def get_extraction_history(self) -> List[Dict[str, Any]]:
        """Get extraction history"""
        return self.extraction_history.copy()
