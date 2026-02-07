"""
Main LCP Transformation Accelerator orchestrator
"""

from typing import Dict, Any, List, Optional
from datetime import datetime

from .state_manager import State, StateManager, StateType
from .sap_extractor import SAPConnection, SAPFactExtractor
from .normalization import NormalizationEngine
from .drift_complexity import DriftDetector, ComplexityAnalyzer
from .reasoning import ReasoningEngine, ChangeOption
from .alm_integration import ALMIntegration


class LCPTransformationAccelerator:
    """
    Main orchestrator for LCP Transformation Accelerator
    Coordinates all components to provide continuous architecture intelligence
    """
    
    def __init__(self, alm_system: str = "generic"):
        self.state_manager = StateManager()
        self.sap_extractor = SAPFactExtractor()
        self.normalization_engine = NormalizationEngine()
        self.drift_detector = DriftDetector()
        self.complexity_analyzer = ComplexityAnalyzer()
        self.reasoning_engine = ReasoningEngine()
        self.alm_integration = ALMIntegration(alm_system)
        
        self.execution_history: List[Dict[str, Any]] = []
    
    def extract_current_state(self, connection: Optional[SAPConnection] = None) -> State:
        """Extract current state from SAP systems"""
        if connection:
            self.sap_extractor.connection = connection
            if not connection.connected:
                connection.connect()
        
        # Extract all facts from SAP
        sap_facts = self.sap_extractor.extract_all_facts()
        
        # Normalize the facts
        normalized_data = self.normalization_engine.normalize_sap_facts(sap_facts)
        
        # Create current state
        current_state = State(StateType.CURRENT, normalized_data, {
            'source': 'sap_extraction',
            'extraction_time': datetime.utcnow().isoformat()
        })
        
        self.state_manager.set_state(current_state)
        self._record_execution('extract_current_state')
        
        return current_state
    
    def define_intended_state(self, intent_data: Dict[str, Any]) -> State:
        """Define intended state from intent specifications"""
        # Normalize the intent
        normalized_intent = self.normalization_engine.normalize_intent(intent_data)
        
        # Create intended state
        intended_state = State(StateType.INTENDED, normalized_intent, {
            'source': 'intent_specification',
            'defined_at': datetime.utcnow().isoformat()
        })
        
        self.state_manager.set_state(intended_state)
        self._record_execution('define_intended_state')
        
        return intended_state
    
    def define_reference_state(self, best_practices: Dict[str, Any]) -> State:
        """Define reference state from best practices"""
        # Normalize best practices
        normalized_practices = self.normalization_engine.normalize_best_practices(best_practices)
        
        # Create reference state
        reference_state = State(StateType.REFERENCE, normalized_practices, {
            'source': 'best_practices',
            'defined_at': datetime.utcnow().isoformat()
        })
        
        self.state_manager.set_state(reference_state)
        self._record_execution('define_reference_state')
        
        return reference_state
    
    def analyze_and_propose_changes(self) -> Dict[str, Any]:
        """
        Analyze all states, detect drift and complexity, and propose changes
        Returns a comprehensive analysis with proposed change options
        """
        analysis = {
            'analysis_time': datetime.utcnow().isoformat(),
            'states_analyzed': [],
            'drift_report': None,
            'complexity_report': None,
            'change_options': [],
            'summary': {}
        }
        
        # Get all states
        current = self.state_manager.get_state(StateType.CURRENT)
        intended = self.state_manager.get_state(StateType.INTENDED)
        reference = self.state_manager.get_state(StateType.REFERENCE)
        
        if not current:
            analysis['summary']['error'] = "Current state not defined"
            return analysis
        
        analysis['states_analyzed'].append(StateType.CURRENT)
        
        # Detect drift if intended state exists
        if intended:
            analysis['states_analyzed'].append(StateType.INTENDED)
            drift_report = self.drift_detector.detect_drift(
                current.data,
                intended.data
            )
            analysis['drift_report'] = drift_report
        else:
            drift_report = {'drift_items': [], 'severity': 'none', 'drift_score': 0.0}
        
        # Analyze complexity
        complexity_report = self.complexity_analyzer.analyze_complexity(current.data)
        analysis['complexity_report'] = complexity_report
        
        # Reason about changes
        if intended:
            change_options = self.reasoning_engine.reason_changes(
                current.data,
                intended.data,
                drift_report,
                complexity_report
            )
            analysis['change_options'] = [opt.to_dict() for opt in change_options]
        
        # Generate summary
        analysis['summary'] = {
            'drift_severity': drift_report.get('severity', 'none'),
            'complexity_level': complexity_report.get('overall_complexity', 'unknown'),
            'total_change_options': len(analysis['change_options']),
            'approved_options': sum(1 for opt in analysis['change_options'] 
                                   if opt['governance_status'] == 'approved'),
            'pending_options': sum(1 for opt in analysis['change_options'] 
                                  if opt['governance_status'] in ['pending', 'pending_review'])
        }
        
        self._record_execution('analyze_and_propose_changes')
        return analysis
    
    def create_delivery_plan(self) -> Dict[str, Any]:
        """Create delivery plan from approved change options"""
        approved_options = self.reasoning_engine.get_approved_options()
        
        if not approved_options:
            return {
                'error': 'No approved change options available',
                'message': 'Approve change options before creating delivery plan'
            }
        
        delivery_plan = self.alm_integration.create_delivery_plan(approved_options)
        
        # Create planned state
        planned_data = {
            'plan_id': delivery_plan['plan_id'],
            'tasks': delivery_plan['tasks'],
            'phases': delivery_plan['phases'],
            'total_effort': delivery_plan['total_effort'],
            'estimated_duration': delivery_plan['estimated_duration']
        }
        
        planned_state = State(StateType.PLANNED, planned_data, {
            'source': 'delivery_planning',
            'created_at': delivery_plan['created_at']
        })
        
        self.state_manager.set_state(planned_state)
        self._record_execution('create_delivery_plan')
        
        return delivery_plan
    
    def submit_to_alm(self) -> Dict[str, Any]:
        """Submit approved delivery plan to ALM system"""
        planned_state = self.state_manager.get_state(StateType.PLANNED)
        
        if not planned_state:
            return {
                'error': 'No planned state available',
                'message': 'Create delivery plan before submitting to ALM'
            }
        
        submission = self.alm_integration.submit_to_alm(planned_state.data)
        self._record_execution('submit_to_alm')
        
        return submission
    
    def synchronize_states(self) -> Dict[str, Any]:
        """Synchronize all states and detect drift"""
        sync_result = self.state_manager.synchronize()
        self._record_execution('synchronize_states')
        return sync_result
    
    def get_full_status(self) -> Dict[str, Any]:
        """Get comprehensive status of LCP TA system"""
        status = {
            'timestamp': datetime.utcnow().isoformat(),
            'states': {},
            'statistics': {},
            'history': {}
        }
        
        # Get all states
        all_states = self.state_manager.get_all_states()
        for state_type, state in all_states.items():
            status['states'][state_type] = {
                'timestamp': state.timestamp,
                'version': state.version
            }
        
        # Get statistics
        status['statistics'] = {
            'total_extractions': len(self.sap_extractor.get_extraction_history()),
            'total_normalizations': len(self.normalization_engine.get_normalization_history()),
            'total_drift_detections': len(self.drift_detector.get_detection_history()),
            'total_complexity_analyses': len(self.complexity_analyzer.get_analysis_history()),
            'total_reasoning_sessions': len(self.reasoning_engine.get_reasoning_history()),
            'total_deliveries': len(self.alm_integration.get_delivery_history())
        }
        
        # Get recent history
        status['history'] = {
            'executions': self.execution_history[-10:] if len(self.execution_history) > 10 else self.execution_history
        }
        
        return status
    
    def _record_execution(self, action: str) -> None:
        """Record execution in history"""
        self.execution_history.append({
            'timestamp': datetime.utcnow().isoformat(),
            'action': action
        })
    
    def get_execution_history(self) -> List[Dict[str, Any]]:
        """Get execution history"""
        return self.execution_history.copy()
