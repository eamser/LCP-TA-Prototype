"""
Test suite for LCP Transformation Accelerator
"""

import unittest
from lcp_ta.state_manager import State, StateManager, StateType
from lcp_ta.sap_extractor import SAPConnection, SAPFactExtractor
from lcp_ta.normalization import NormalizationEngine
from lcp_ta.drift_complexity import DriftDetector, ComplexityAnalyzer
from lcp_ta.reasoning import ReasoningEngine, ChangeOption
from lcp_ta.alm_integration import ALMIntegration
from lcp_ta.lcp_ta import LCPTransformationAccelerator


class TestStateManager(unittest.TestCase):
    """Test State Manager functionality"""
    
    def setUp(self):
        self.state_manager = StateManager()
    
    def test_create_state(self):
        """Test state creation"""
        state = State(StateType.CURRENT, {'test': 'data'})
        self.assertEqual(state.state_type, StateType.CURRENT)
        self.assertEqual(state.data, {'test': 'data'})
        self.assertIsNotNone(state.timestamp)
    
    def test_set_and_get_state(self):
        """Test setting and getting states"""
        state = State(StateType.CURRENT, {'test': 'data'})
        self.state_manager.set_state(state)
        
        retrieved = self.state_manager.get_state(StateType.CURRENT)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.state_type, StateType.CURRENT)
    
    def test_compare_states(self):
        """Test state comparison"""
        state1 = State(StateType.CURRENT, {'count': 10, 'name': 'test'})
        state2 = State(StateType.INTENDED, {'count': 15, 'name': 'test'})
        
        self.state_manager.set_state(state1)
        self.state_manager.set_state(state2)
        
        diff = self.state_manager.compare_states(StateType.CURRENT, StateType.INTENDED)
        self.assertIn('differences', diff)
        self.assertTrue(len(diff['differences']) > 0)


class TestSAPExtractor(unittest.TestCase):
    """Test SAP Fact Extractor functionality"""
    
    def setUp(self):
        self.extractor = SAPFactExtractor()
    
    def test_extract_system_landscape(self):
        """Test system landscape extraction"""
        landscape = self.extractor.extract_system_landscape()
        
        self.assertIn('systems', landscape)
        self.assertIn('connections', landscape)
        self.assertTrue(len(landscape['systems']) > 0)
    
    def test_extract_custom_code(self):
        """Test custom code extraction"""
        custom_code = self.extractor.extract_custom_code()
        
        self.assertIn('programs', custom_code)
        self.assertIn('function_modules', custom_code)
        self.assertIn('statistics', custom_code)
    
    def test_extract_all_facts(self):
        """Test complete fact extraction"""
        facts = self.extractor.extract_all_facts()
        
        self.assertIn('system_landscape', facts)
        self.assertIn('custom_code', facts)
        self.assertIn('interfaces', facts)
        self.assertIn('customizing', facts)


class TestNormalizationEngine(unittest.TestCase):
    """Test Normalization Engine functionality"""
    
    def setUp(self):
        self.engine = NormalizationEngine()
        self.extractor = SAPFactExtractor()
    
    def test_normalize_sap_facts(self):
        """Test SAP fact normalization"""
        facts = self.extractor.extract_all_facts()
        normalized = self.engine.normalize_sap_facts(facts)
        
        self.assertIn('components', normalized)
        self.assertIn('dependencies', normalized)
        self.assertIn('metrics', normalized)
    
    def test_normalize_intent(self):
        """Test intent normalization"""
        intent = {
            'objectives': [
                {'id': 'obj1', 'name': 'Test Objective'}
            ],
            'constraints': [
                {'id': 'const1', 'name': 'Test Constraint', 'type': 'time'}
            ]
        }
        
        normalized = self.engine.normalize_intent(intent)
        self.assertIn('objectives', normalized)
        self.assertIn('constraints', normalized)


class TestDriftDetector(unittest.TestCase):
    """Test Drift Detector functionality"""
    
    def setUp(self):
        self.detector = DriftDetector()
    
    def test_detect_drift(self):
        """Test drift detection"""
        current = {
            'components': {'systems': [1, 2, 3]},
            'dependencies': [],
            'metrics': {'component_count': 3}
        }
        
        target = {
            'components': {'systems': [1, 2]},
            'dependencies': [],
            'metrics': {'component_count': 2}
        }
        
        drift_report = self.detector.detect_drift(current, target)
        
        self.assertIn('drift_items', drift_report)
        self.assertIn('severity', drift_report)
        self.assertIn('drift_score', drift_report)
        self.assertTrue(len(drift_report['drift_items']) > 0)


class TestComplexityAnalyzer(unittest.TestCase):
    """Test Complexity Analyzer functionality"""
    
    def setUp(self):
        self.analyzer = ComplexityAnalyzer()
    
    def test_analyze_complexity(self):
        """Test complexity analysis"""
        data = {
            'components': {
                'systems': [1, 2, 3],
                'custom_code': {'total_artifacts': 5}
            },
            'dependencies': [1, 2, 3],
            'metrics': {}
        }
        
        report = self.analyzer.analyze_complexity(data)
        
        self.assertIn('metrics', report)
        self.assertIn('hotspots', report)
        self.assertIn('recommendations', report)
        self.assertIn('overall_complexity', report)


class TestReasoningEngine(unittest.TestCase):
    """Test Reasoning Engine functionality"""
    
    def setUp(self):
        self.engine = ReasoningEngine()
    
    def test_create_change_option(self):
        """Test change option creation"""
        option = ChangeOption('opt1', 'Test Option', 'Description')
        
        self.assertEqual(option.option_id, 'opt1')
        self.assertEqual(option.title, 'Test Option')
        self.assertEqual(option.governance_status, 'pending')
    
    def test_approve_option(self):
        """Test option approval"""
        option = ChangeOption('opt1', 'Test Option', 'Description')
        self.engine.change_options.append(option)
        
        result = self.engine.approve_option('opt1')
        self.assertTrue(result)
        self.assertEqual(option.governance_status, 'approved')
    
    def test_reason_changes(self):
        """Test change reasoning"""
        current = {'components': {}, 'dependencies': [], 'metrics': {}}
        intended = {'components': {}, 'dependencies': [], 'metrics': {}}
        drift_report = {
            'drift_items': [
                {'category': 'component', 'type': 'systems', 
                 'drift_type': 'count_mismatch', 'current_value': 5, 
                 'target_value': 3, 'impact': 'medium'}
            ]
        }
        complexity_report = {'hotspots': []}
        
        options = self.engine.reason_changes(current, intended, drift_report, complexity_report)
        self.assertTrue(len(options) > 0)


class TestALMIntegration(unittest.TestCase):
    """Test ALM Integration functionality"""
    
    def setUp(self):
        self.alm = ALMIntegration('jira')
    
    def test_create_delivery_plan(self):
        """Test delivery plan creation"""
        option = ChangeOption('opt1', 'Test Change', 'Description')
        option.set_impact('medium')
        option.approve()
        
        plan = self.alm.create_delivery_plan([option])
        
        self.assertIn('plan_id', plan)
        self.assertIn('tasks', plan)
        self.assertIn('phases', plan)
        self.assertTrue(len(plan['tasks']) > 0)


class TestLCPTransformationAccelerator(unittest.TestCase):
    """Test main LCP TA orchestrator"""
    
    def setUp(self):
        self.lcp_ta = LCPTransformationAccelerator()
    
    def test_extract_current_state(self):
        """Test current state extraction"""
        state = self.lcp_ta.extract_current_state()
        
        self.assertIsNotNone(state)
        self.assertEqual(state.state_type, StateType.CURRENT)
        self.assertIn('components', state.data)
    
    def test_define_intended_state(self):
        """Test intended state definition"""
        intent = {
            'objectives': [{'id': 'obj1', 'name': 'Test'}],
            'constraints': [],
            'target_architecture': {}
        }
        
        state = self.lcp_ta.define_intended_state(intent)
        
        self.assertIsNotNone(state)
        self.assertEqual(state.state_type, StateType.INTENDED)
    
    def test_full_workflow(self):
        """Test complete workflow"""
        # Extract current
        self.lcp_ta.extract_current_state()
        
        # Define intended
        intent = {
            'objectives': [{'id': 'obj1', 'name': 'Test'}],
            'constraints': [],
            'target_architecture': {'components': []}
        }
        self.lcp_ta.define_intended_state(intent)
        
        # Analyze
        analysis = self.lcp_ta.analyze_and_propose_changes()
        
        self.assertIn('drift_report', analysis)
        self.assertIn('complexity_report', analysis)
        self.assertIn('change_options', analysis)


if __name__ == '__main__':
    unittest.main()
