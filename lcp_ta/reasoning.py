"""
Reasoning Engine Module
Reasons across all states to propose governed, explainable change options
"""

from typing import Dict, Any, List, Optional
from datetime import datetime


class ChangeOption:
    """Represents a proposed change option"""
    
    def __init__(self, option_id: str, title: str, description: str):
        self.option_id = option_id
        self.title = title
        self.description = description
        self.rationale: List[str] = []
        self.benefits: List[str] = []
        self.risks: List[str] = []
        self.effort_estimate: str = "unknown"
        self.impact: str = "medium"
        self.governance_status: str = "pending"
        self.created_at = datetime.utcnow().isoformat()
    
    def add_rationale(self, rationale: str) -> None:
        """Add rationale for this change option"""
        self.rationale.append(rationale)
    
    def add_benefit(self, benefit: str) -> None:
        """Add benefit of this change option"""
        self.benefits.append(benefit)
    
    def add_risk(self, risk: str) -> None:
        """Add risk of this change option"""
        self.risks.append(risk)
    
    def set_effort_estimate(self, estimate: str) -> None:
        """Set effort estimate"""
        self.effort_estimate = estimate
    
    def set_impact(self, impact: str) -> None:
        """Set impact level"""
        self.impact = impact
    
    def approve(self) -> None:
        """Approve this change option"""
        self.governance_status = "approved"
    
    def reject(self) -> None:
        """Reject this change option"""
        self.governance_status = "rejected"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'option_id': self.option_id,
            'title': self.title,
            'description': self.description,
            'rationale': self.rationale,
            'benefits': self.benefits,
            'risks': self.risks,
            'effort_estimate': self.effort_estimate,
            'impact': self.impact,
            'governance_status': self.governance_status,
            'created_at': self.created_at
        }


class ReasoningEngine:
    """Reasons across all states to propose governed, explainable change options"""
    
    def __init__(self):
        self.change_options: List[ChangeOption] = []
        self.reasoning_history: List[Dict[str, Any]] = []
        self.governance_rules: List[Dict[str, Any]] = []
    
    def add_governance_rule(self, rule: Dict[str, Any]) -> None:
        """Add a governance rule"""
        self.governance_rules.append(rule)
    
    def reason_changes(
        self,
        current_state: Dict[str, Any],
        intended_state: Dict[str, Any],
        drift_report: Dict[str, Any],
        complexity_report: Dict[str, Any]
    ) -> List[ChangeOption]:
        """Reason across states to propose change options"""
        options = []
        
        # Analyze drift and propose changes
        for drift_item in drift_report.get('drift_items', []):
            option = self._create_drift_remediation_option(drift_item, current_state, intended_state)
            if option:
                options.append(option)
        
        # Analyze complexity and propose improvements
        for hotspot in complexity_report.get('hotspots', []):
            option = self._create_complexity_reduction_option(hotspot)
            if option:
                options.append(option)
        
        # Apply governance rules
        for option in options:
            self._apply_governance(option)
        
        self.change_options.extend(options)
        self._record_reasoning(len(options))
        
        return options
    
    def _create_drift_remediation_option(
        self,
        drift_item: Dict[str, Any],
        current_state: Dict[str, Any],
        intended_state: Dict[str, Any]
    ) -> Optional[ChangeOption]:
        """Create change option to remediate drift"""
        category = drift_item.get('category', 'unknown')
        drift_type = drift_item.get('drift_type', 'unknown')
        
        if category == 'component':
            option_id = f"drift_component_{drift_item.get('type', 'unknown')}"
            title = f"Align {drift_item.get('type', 'component')} count"
            description = f"Adjust {drift_item.get('type', 'component')} from {drift_item.get('current_value')} to {drift_item.get('target_value')}"
            
            option = ChangeOption(option_id, title, description)
            option.add_rationale(f"Current state has drift in {category}: {drift_type}")
            option.add_benefit("Brings system in line with intended architecture")
            option.set_impact(drift_item.get('impact', 'medium'))
            
            if drift_item.get('current_value', 0) > drift_item.get('target_value', 0):
                option.set_effort_estimate("medium")
                option.add_risk("Requires decommissioning existing components")
            else:
                option.set_effort_estimate("high")
                option.add_risk("Requires new component development")
            
            return option
        
        elif category == 'dependency':
            option_id = f"drift_dependency_{drift_type}"
            title = f"Fix dependency drift: {drift_type}"
            description = f"Address {drift_type} in system dependencies"
            
            option = ChangeOption(option_id, title, description)
            option.add_rationale(f"Dependency drift detected: {drift_type}")
            option.add_benefit("Ensures correct system integration")
            option.set_impact('high')
            option.set_effort_estimate('medium')
            option.add_risk("May affect system integration points")
            
            return option
        
        elif category == 'metric':
            option_id = f"drift_metric_{drift_item.get('type', 'unknown')}"
            title = f"Optimize {drift_item.get('type', 'metric')}"
            description = f"Adjust {drift_item.get('type', 'metric')} from {drift_item.get('current_value')} to {drift_item.get('target_value')}"
            
            option = ChangeOption(option_id, title, description)
            option.add_rationale(f"Metric deviation detected: {drift_item.get('variance', 0):.2f}")
            option.add_benefit("Improves system performance metrics")
            option.set_impact(drift_item.get('impact', 'medium'))
            option.set_effort_estimate('medium')
            
            return option
        
        return None
    
    def _create_complexity_reduction_option(self, hotspot: Dict[str, Any]) -> Optional[ChangeOption]:
        """Create change option to reduce complexity"""
        hotspot_type = hotspot.get('type', 'unknown')
        
        if hotspot_type == 'high_coupling':
            option = ChangeOption(
                'complexity_reduce_coupling',
                'Reduce system coupling',
                'Introduce abstraction layers to reduce coupling'
            )
            option.add_rationale(f"High coupling detected: {hotspot.get('metric_value', 0):.2f}")
            option.add_benefit("Improves maintainability and flexibility")
            option.add_benefit("Reduces ripple effects of changes")
            option.set_effort_estimate('high')
            option.set_impact('high')
            option.add_risk("Requires significant refactoring")
            
            return option
        
        elif hotspot_type == 'component_proliferation':
            option = ChangeOption(
                'complexity_consolidate_components',
                'Consolidate components',
                'Review and consolidate similar components'
            )
            option.add_rationale(f"Component proliferation detected: {hotspot.get('metric_value', 0)} components")
            option.add_benefit("Simplifies architecture")
            option.add_benefit("Reduces maintenance overhead")
            option.set_effort_estimate('medium')
            option.set_impact('medium')
            option.add_risk("May require component migration")
            
            return option
        
        elif hotspot_type == 'high_complexity':
            option = ChangeOption(
                'complexity_simplify_architecture',
                'Simplify architecture',
                'Reduce overall system complexity'
            )
            option.add_rationale(f"High complexity detected: {hotspot.get('metric_value', 0):.2f}")
            option.add_benefit("Improves system understandability")
            option.add_benefit("Reduces technical debt")
            option.set_effort_estimate('high')
            option.set_impact('high')
            option.add_risk("Requires comprehensive architecture review")
            
            return option
        
        return None
    
    def _apply_governance(self, option: ChangeOption) -> None:
        """Apply governance rules to a change option"""
        # Auto-approve low-impact changes
        if option.impact == 'low':
            option.approve()
            return
        
        # Check governance rules
        for rule in self.governance_rules:
            if self._matches_rule(option, rule):
                if rule.get('action') == 'approve':
                    option.approve()
                elif rule.get('action') == 'reject':
                    option.reject()
                return
        
        # Default: keep as pending for manual review
        option.governance_status = 'pending_review'
    
    def _matches_rule(self, option: ChangeOption, rule: Dict[str, Any]) -> bool:
        """Check if option matches a governance rule"""
        if 'impact' in rule and option.impact != rule['impact']:
            return False
        
        if 'option_id_pattern' in rule and not option.option_id.startswith(rule['option_id_pattern']):
            return False
        
        return True
    
    def get_approved_options(self) -> List[ChangeOption]:
        """Get all approved change options"""
        return [opt for opt in self.change_options if opt.governance_status == 'approved']
    
    def get_pending_options(self) -> List[ChangeOption]:
        """Get all pending change options"""
        return [opt for opt in self.change_options if opt.governance_status in ['pending', 'pending_review']]
    
    def approve_option(self, option_id: str) -> bool:
        """Manually approve a change option"""
        for option in self.change_options:
            if option.option_id == option_id:
                option.approve()
                return True
        return False
    
    def reject_option(self, option_id: str) -> bool:
        """Manually reject a change option"""
        for option in self.change_options:
            if option.option_id == option_id:
                option.reject()
                return True
        return False
    
    def _record_reasoning(self, option_count: int) -> None:
        """Record reasoning session in history"""
        self.reasoning_history.append({
            'timestamp': datetime.utcnow().isoformat(),
            'options_generated': option_count
        })
    
    def get_reasoning_history(self) -> List[Dict[str, Any]]:
        """Get reasoning history"""
        return self.reasoning_history.copy()
