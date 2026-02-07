"""
Drift and Complexity Detection Module
Detects drift between states and measures system complexity
"""

from typing import Dict, Any, List, Optional
from datetime import datetime


class DriftDetector:
    """Detects drift between architecture states"""
    
    def __init__(self):
        self.detection_history: List[Dict[str, Any]] = []
        self.thresholds = {
            'critical': 0.8,
            'high': 0.6,
            'medium': 0.4,
            'low': 0.2
        }
    
    def detect_drift(self, current_state: Dict[str, Any], target_state: Dict[str, Any]) -> Dict[str, Any]:
        """Detect drift between current and target states"""
        drift_report = {
            'detection_time': datetime.utcnow().isoformat(),
            'drift_items': [],
            'severity': 'none',
            'drift_score': 0.0,
            'summary': {}
        }
        
        # Compare components
        component_drift = self._detect_component_drift(
            current_state.get('components', {}),
            target_state.get('components', {})
        )
        drift_report['drift_items'].extend(component_drift)
        
        # Compare dependencies
        dependency_drift = self._detect_dependency_drift(
            current_state.get('dependencies', []),
            target_state.get('dependencies', [])
        )
        drift_report['drift_items'].extend(dependency_drift)
        
        # Compare metrics
        metric_drift = self._detect_metric_drift(
            current_state.get('metrics', {}),
            target_state.get('metrics', {})
        )
        drift_report['drift_items'].extend(metric_drift)
        
        # Calculate overall drift score
        drift_report['drift_score'] = self._calculate_drift_score(drift_report['drift_items'])
        drift_report['severity'] = self._determine_severity(drift_report['drift_score'])
        
        # Generate summary
        drift_report['summary'] = self._generate_drift_summary(drift_report['drift_items'])
        
        self._record_detection(drift_report)
        return drift_report
    
    def _detect_component_drift(self, current: Dict[str, Any], target: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Detect drift in components"""
        drift_items = []
        
        all_component_types = set(current.keys()) | set(target.keys())
        
        for comp_type in all_component_types:
            current_comps = current.get(comp_type, [])
            target_comps = target.get(comp_type, [])
            
            # Handle different data structures
            if isinstance(current_comps, dict):
                current_count = sum(len(v) if isinstance(v, list) else 1 for v in current_comps.values())
            else:
                current_count = len(current_comps) if isinstance(current_comps, list) else 0
            
            if isinstance(target_comps, dict):
                target_count = sum(len(v) if isinstance(v, list) else 1 for v in target_comps.values())
            else:
                target_count = len(target_comps) if isinstance(target_comps, list) else 0
            
            if current_count != target_count:
                drift_items.append({
                    'category': 'component',
                    'type': comp_type,
                    'drift_type': 'count_mismatch',
                    'current_value': current_count,
                    'target_value': target_count,
                    'impact': 'medium'
                })
        
        return drift_items
    
    def _detect_dependency_drift(self, current: List[Dict[str, Any]], target: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Detect drift in dependencies"""
        drift_items = []
        
        if len(current) != len(target):
            drift_items.append({
                'category': 'dependency',
                'type': 'count',
                'drift_type': 'count_mismatch',
                'current_value': len(current),
                'target_value': len(target),
                'impact': 'high'
            })
        
        # Compare individual dependencies
        current_deps = {f"{d.get('source', '')}->{d.get('target', '')}": d for d in current}
        target_deps = {f"{d.get('source', '')}->{d.get('target', '')}": d for d in target}
        
        # Find missing dependencies
        for dep_key in target_deps:
            if dep_key not in current_deps:
                drift_items.append({
                    'category': 'dependency',
                    'type': 'missing',
                    'drift_type': 'missing_dependency',
                    'dependency': dep_key,
                    'impact': 'high'
                })
        
        # Find extra dependencies
        for dep_key in current_deps:
            if dep_key not in target_deps:
                drift_items.append({
                    'category': 'dependency',
                    'type': 'extra',
                    'drift_type': 'extra_dependency',
                    'dependency': dep_key,
                    'impact': 'medium'
                })
        
        return drift_items
    
    def _detect_metric_drift(self, current: Dict[str, Any], target: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Detect drift in metrics"""
        drift_items = []
        
        all_metrics = set(current.keys()) | set(target.keys())
        
        for metric in all_metrics:
            current_value = current.get(metric, 0)
            target_value = target.get(metric, 0)
            
            if isinstance(current_value, (int, float)) and isinstance(target_value, (int, float)):
                if current_value != target_value:
                    variance = abs(current_value - target_value) / max(target_value, 1)
                    
                    drift_items.append({
                        'category': 'metric',
                        'type': metric,
                        'drift_type': 'value_change',
                        'current_value': current_value,
                        'target_value': target_value,
                        'variance': variance,
                        'impact': 'high' if variance > 0.5 else 'medium' if variance > 0.2 else 'low'
                    })
        
        return drift_items
    
    def _calculate_drift_score(self, drift_items: List[Dict[str, Any]]) -> float:
        """Calculate overall drift score"""
        if not drift_items:
            return 0.0
        
        impact_weights = {
            'critical': 1.0,
            'high': 0.7,
            'medium': 0.4,
            'low': 0.2
        }
        
        total_score = sum(impact_weights.get(item.get('impact', 'low'), 0.2) for item in drift_items)
        max_score = len(drift_items) * 1.0
        
        return total_score / max_score if max_score > 0 else 0.0
    
    def _determine_severity(self, drift_score: float) -> str:
        """Determine severity level based on drift score"""
        if drift_score >= self.thresholds['critical']:
            return 'critical'
        elif drift_score >= self.thresholds['high']:
            return 'high'
        elif drift_score >= self.thresholds['medium']:
            return 'medium'
        elif drift_score >= self.thresholds['low']:
            return 'low'
        else:
            return 'none'
    
    def _generate_drift_summary(self, drift_items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate summary of drift items"""
        summary = {
            'total_items': len(drift_items),
            'by_category': {},
            'by_impact': {}
        }
        
        for item in drift_items:
            category = item.get('category', 'unknown')
            impact = item.get('impact', 'low')
            
            summary['by_category'][category] = summary['by_category'].get(category, 0) + 1
            summary['by_impact'][impact] = summary['by_impact'].get(impact, 0) + 1
        
        return summary
    
    def _record_detection(self, drift_report: Dict[str, Any]) -> None:
        """Record drift detection in history"""
        self.detection_history.append({
            'timestamp': drift_report['detection_time'],
            'severity': drift_report['severity'],
            'drift_score': drift_report['drift_score'],
            'item_count': len(drift_report['drift_items'])
        })
    
    def get_detection_history(self) -> List[Dict[str, Any]]:
        """Get detection history"""
        return self.detection_history.copy()


class ComplexityAnalyzer:
    """Analyzes system complexity"""
    
    def __init__(self):
        self.analysis_history: List[Dict[str, Any]] = []
    
    def analyze_complexity(self, normalized_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze complexity of the system"""
        complexity_report = {
            'analysis_time': datetime.utcnow().isoformat(),
            'metrics': {},
            'hotspots': [],
            'recommendations': [],
            'overall_complexity': 'unknown'
        }
        
        # Calculate various complexity metrics
        complexity_report['metrics'] = self._calculate_complexity_metrics(normalized_data)
        
        # Identify complexity hotspots
        complexity_report['hotspots'] = self._identify_hotspots(normalized_data, complexity_report['metrics'])
        
        # Generate recommendations
        complexity_report['recommendations'] = self._generate_recommendations(
            complexity_report['metrics'],
            complexity_report['hotspots']
        )
        
        # Determine overall complexity level
        complexity_report['overall_complexity'] = self._determine_complexity_level(
            complexity_report['metrics']
        )
        
        self._record_analysis(complexity_report)
        return complexity_report
    
    def _calculate_complexity_metrics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate various complexity metrics"""
        metrics = {
            'component_count': 0,
            'dependency_count': 0,
            'coupling_factor': 0.0,
            'depth': 0,
            'cyclomatic_complexity': 0
        }
        
        # Count components
        components = data.get('components', {})
        for comp_type, comp_data in components.items():
            if isinstance(comp_data, list):
                metrics['component_count'] += len(comp_data)
            elif isinstance(comp_data, dict):
                metrics['component_count'] += sum(
                    len(v) if isinstance(v, list) else 1 
                    for v in comp_data.values()
                )
        
        # Count dependencies
        dependencies = data.get('dependencies', [])
        metrics['dependency_count'] = len(dependencies)
        
        # Calculate coupling factor
        if metrics['component_count'] > 1:
            max_dependencies = metrics['component_count'] * (metrics['component_count'] - 1)
            metrics['coupling_factor'] = metrics['dependency_count'] / max_dependencies if max_dependencies > 0 else 0
        
        # Use existing complexity score if available
        existing_metrics = data.get('metrics', {})
        if 'complexity_score' in existing_metrics:
            metrics['cyclomatic_complexity'] = existing_metrics['complexity_score']
        else:
            # Calculate a simple complexity score
            metrics['cyclomatic_complexity'] = (
                metrics['component_count'] * 1.0 +
                metrics['dependency_count'] * 1.5 +
                metrics['coupling_factor'] * 10
            )
        
        return metrics
    
    def _identify_hotspots(self, data: Dict[str, Any], metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify complexity hotspots"""
        hotspots = []
        
        # High coupling
        if metrics.get('coupling_factor', 0) > 0.3:
            hotspots.append({
                'type': 'high_coupling',
                'severity': 'high',
                'description': 'System exhibits high coupling between components',
                'metric_value': metrics['coupling_factor']
            })
        
        # Too many components
        if metrics.get('component_count', 0) > 50:
            hotspots.append({
                'type': 'component_proliferation',
                'severity': 'medium',
                'description': 'Large number of components may indicate over-engineering',
                'metric_value': metrics['component_count']
            })
        
        # High cyclomatic complexity
        if metrics.get('cyclomatic_complexity', 0) > 100:
            hotspots.append({
                'type': 'high_complexity',
                'severity': 'high',
                'description': 'Overall system complexity is very high',
                'metric_value': metrics['cyclomatic_complexity']
            })
        
        return hotspots
    
    def _generate_recommendations(self, metrics: Dict[str, Any], hotspots: List[Dict[str, Any]]) -> List[str]:
        """Generate recommendations based on complexity analysis"""
        recommendations = []
        
        for hotspot in hotspots:
            if hotspot['type'] == 'high_coupling':
                recommendations.append(
                    "Reduce coupling by introducing abstraction layers or event-driven patterns"
                )
            elif hotspot['type'] == 'component_proliferation':
                recommendations.append(
                    "Consider consolidating similar components or reviewing architecture boundaries"
                )
            elif hotspot['type'] == 'high_complexity':
                recommendations.append(
                    "Simplify architecture by removing unnecessary dependencies and components"
                )
        
        if not recommendations:
            recommendations.append("System complexity is within acceptable bounds")
        
        return recommendations
    
    def _determine_complexity_level(self, metrics: Dict[str, Any]) -> str:
        """Determine overall complexity level"""
        complexity_score = metrics.get('cyclomatic_complexity', 0)
        
        if complexity_score > 150:
            return 'very_high'
        elif complexity_score > 100:
            return 'high'
        elif complexity_score > 50:
            return 'medium'
        elif complexity_score > 20:
            return 'low'
        else:
            return 'very_low'
    
    def _record_analysis(self, complexity_report: Dict[str, Any]) -> None:
        """Record complexity analysis in history"""
        self.analysis_history.append({
            'timestamp': complexity_report['analysis_time'],
            'overall_complexity': complexity_report['overall_complexity'],
            'hotspot_count': len(complexity_report['hotspots'])
        })
    
    def get_analysis_history(self) -> List[Dict[str, Any]]:
        """Get analysis history"""
        return self.analysis_history.copy()
