"""
Normalization Engine Module
Normalizes intent and best practices into diff-able models
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import json


class NormalizationRule:
    """Represents a normalization rule"""
    
    def __init__(self, rule_id: str, name: str, description: str, rule_type: str):
        self.rule_id = rule_id
        self.name = name
        self.description = description
        self.rule_type = rule_type
    
    def apply(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Apply normalization rule to data"""
        # To be implemented by specific rule types
        return data


class NormalizationEngine:
    """Normalizes diverse data sources into consistent, diff-able models"""
    
    def __init__(self):
        self.rules: List[NormalizationRule] = []
        self.normalization_history: List[Dict[str, Any]] = []
    
    def add_rule(self, rule: NormalizationRule) -> None:
        """Add a normalization rule"""
        self.rules.append(rule)
    
    def normalize_sap_facts(self, sap_facts: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize SAP facts into standard model"""
        normalized = {
            'normalization_time': datetime.utcnow().isoformat(),
            'source': 'sap_facts',
            'model_version': '1.0',
            'components': {},
            'dependencies': [],
            'metrics': {}
        }
        
        # Normalize system landscape
        if 'system_landscape' in sap_facts:
            normalized['components']['systems'] = self._normalize_systems(
                sap_facts['system_landscape'].get('systems', [])
            )
            normalized['dependencies'] = self._normalize_connections(
                sap_facts['system_landscape'].get('connections', [])
            )
        
        # Normalize custom code
        if 'custom_code' in sap_facts:
            normalized['components']['custom_code'] = self._normalize_custom_code(
                sap_facts['custom_code']
            )
        
        # Normalize interfaces
        if 'interfaces' in sap_facts:
            normalized['components']['interfaces'] = self._normalize_interfaces(
                sap_facts['interfaces']
            )
        
        # Calculate metrics
        normalized['metrics'] = self._calculate_metrics(normalized)
        
        self._record_normalization('sap_facts', normalized)
        return normalized
    
    def normalize_intent(self, intent_data: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize intent specifications into standard model"""
        normalized = {
            'normalization_time': datetime.utcnow().isoformat(),
            'source': 'intent',
            'model_version': '1.0',
            'objectives': [],
            'constraints': [],
            'target_architecture': {}
        }
        
        # Extract and normalize objectives
        if 'objectives' in intent_data:
            normalized['objectives'] = [
                self._normalize_objective(obj) 
                for obj in intent_data['objectives']
            ]
        
        # Extract and normalize constraints
        if 'constraints' in intent_data:
            normalized['constraints'] = [
                self._normalize_constraint(cons) 
                for cons in intent_data['constraints']
            ]
        
        # Normalize target architecture
        if 'target_architecture' in intent_data:
            normalized['target_architecture'] = self._normalize_architecture(
                intent_data['target_architecture']
            )
        
        self._record_normalization('intent', normalized)
        return normalized
    
    def normalize_best_practices(self, best_practices: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize best practices into standard model"""
        normalized = {
            'normalization_time': datetime.utcnow().isoformat(),
            'source': 'best_practices',
            'model_version': '1.0',
            'practices': [],
            'patterns': [],
            'antipatterns': []
        }
        
        # Normalize practices
        if 'practices' in best_practices:
            normalized['practices'] = [
                self._normalize_practice(practice) 
                for practice in best_practices['practices']
            ]
        
        # Normalize patterns
        if 'patterns' in best_practices:
            normalized['patterns'] = [
                self._normalize_pattern(pattern) 
                for pattern in best_practices['patterns']
            ]
        
        # Normalize antipatterns
        if 'antipatterns' in best_practices:
            normalized['antipatterns'] = [
                self._normalize_antipattern(ap) 
                for ap in best_practices['antipatterns']
            ]
        
        self._record_normalization('best_practices', normalized)
        return normalized
    
    def _normalize_systems(self, systems: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Normalize system definitions"""
        return [
            {
                'id': sys.get('system_id', ''),
                'name': sys.get('system_id', ''),
                'type': sys.get('type', 'unknown'),
                'host': sys.get('host', ''),
                'status': sys.get('status', 'unknown'),
                'version': sys.get('version', 'unknown')
            }
            for sys in systems
        ]
    
    def _normalize_connections(self, connections: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Normalize connection/dependency definitions"""
        return [
            {
                'source': conn.get('source', ''),
                'target': conn.get('target', ''),
                'type': conn.get('type', 'unknown'),
                'protocol': conn.get('protocol', '')
            }
            for conn in connections
        ]
    
    def _normalize_custom_code(self, custom_code: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize custom code artifacts"""
        return {
            'programs': custom_code.get('programs', []),
            'function_modules': custom_code.get('function_modules', []),
            'classes': custom_code.get('classes', []),
            'total_artifacts': (
                len(custom_code.get('programs', [])) +
                len(custom_code.get('function_modules', [])) +
                len(custom_code.get('classes', []))
            )
        }
    
    def _normalize_interfaces(self, interfaces: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize interface configurations"""
        return {
            'rfc': interfaces.get('rfc_destinations', []),
            'idocs': interfaces.get('idocs', []),
            'web_services': interfaces.get('web_services', []),
            'total_interfaces': (
                len(interfaces.get('rfc_destinations', [])) +
                len(interfaces.get('idocs', [])) +
                len(interfaces.get('web_services', []))
            )
        }
    
    def _normalize_objective(self, objective: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize a single objective"""
        return {
            'id': objective.get('id', ''),
            'name': objective.get('name', ''),
            'description': objective.get('description', ''),
            'priority': objective.get('priority', 'medium'),
            'metrics': objective.get('metrics', [])
        }
    
    def _normalize_constraint(self, constraint: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize a single constraint"""
        return {
            'id': constraint.get('id', ''),
            'name': constraint.get('name', ''),
            'type': constraint.get('type', ''),
            'value': constraint.get('value', ''),
            'mandatory': constraint.get('mandatory', True)
        }
    
    def _normalize_architecture(self, architecture: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize architecture definition"""
        return {
            'components': architecture.get('components', []),
            'layers': architecture.get('layers', []),
            'patterns': architecture.get('patterns', [])
        }
    
    def _normalize_practice(self, practice: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize a best practice"""
        return {
            'id': practice.get('id', ''),
            'name': practice.get('name', ''),
            'category': practice.get('category', ''),
            'description': practice.get('description', ''),
            'applicability': practice.get('applicability', [])
        }
    
    def _normalize_pattern(self, pattern: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize an architecture pattern"""
        return {
            'id': pattern.get('id', ''),
            'name': pattern.get('name', ''),
            'type': pattern.get('type', ''),
            'structure': pattern.get('structure', {}),
            'benefits': pattern.get('benefits', [])
        }
    
    def _normalize_antipattern(self, antipattern: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize an antipattern"""
        return {
            'id': antipattern.get('id', ''),
            'name': antipattern.get('name', ''),
            'description': antipattern.get('description', ''),
            'impact': antipattern.get('impact', 'unknown'),
            'remediation': antipattern.get('remediation', '')
        }
    
    def _calculate_metrics(self, normalized_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate metrics from normalized data"""
        metrics = {
            'component_count': 0,
            'dependency_count': len(normalized_data.get('dependencies', [])),
            'complexity_score': 0
        }
        
        components = normalized_data.get('components', {})
        
        if 'systems' in components:
            metrics['component_count'] += len(components['systems'])
        
        if 'custom_code' in components:
            metrics['component_count'] += components['custom_code'].get('total_artifacts', 0)
        
        # Simple complexity calculation
        metrics['complexity_score'] = (
            metrics['component_count'] * 1.0 +
            metrics['dependency_count'] * 1.5
        )
        
        return metrics
    
    def _record_normalization(self, source: str, data: Dict[str, Any]) -> None:
        """Record normalization in history"""
        self.normalization_history.append({
            'timestamp': datetime.utcnow().isoformat(),
            'source': source,
            'model_version': data.get('model_version', 'unknown')
        })
    
    def get_normalization_history(self) -> List[Dict[str, Any]]:
        """Get normalization history"""
        return self.normalization_history.copy()
