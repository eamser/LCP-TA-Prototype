"""
State Management Module
Manages Current, Intended, Reference, and Planned states
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import json


class StateType:
    """Enumeration of state types"""
    CURRENT = "current"
    INTENDED = "intended"
    REFERENCE = "reference"
    PLANNED = "planned"


class State:
    """Represents a single state snapshot"""
    
    def __init__(self, state_type: str, data: Dict[str, Any], metadata: Optional[Dict[str, Any]] = None):
        self.state_type = state_type
        self.data = data
        self.metadata = metadata or {}
        self.timestamp = datetime.utcnow().isoformat()
        self.version = self.metadata.get('version', '1.0')
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert state to dictionary"""
        return {
            'state_type': self.state_type,
            'data': self.data,
            'metadata': self.metadata,
            'timestamp': self.timestamp,
            'version': self.version
        }
    
    def to_json(self) -> str:
        """Convert state to JSON string"""
        return json.dumps(self.to_dict(), indent=2)
    
    @classmethod
    def from_dict(cls, state_dict: Dict[str, Any]) -> 'State':
        """Create state from dictionary"""
        state = cls(
            state_type=state_dict['state_type'],
            data=state_dict['data'],
            metadata=state_dict.get('metadata', {})
        )
        if 'timestamp' in state_dict:
            state.timestamp = state_dict['timestamp']
        if 'version' in state_dict:
            state.version = state_dict['version']
        return state


class StateManager:
    """Manages all architecture states and keeps them synchronized"""
    
    def __init__(self):
        self.states: Dict[str, State] = {}
        self.history: List[Dict[str, Any]] = []
    
    def set_state(self, state: State) -> None:
        """Set or update a state"""
        self.states[state.state_type] = state
        self._record_change(f"Set {state.state_type} state")
    
    def get_state(self, state_type: str) -> Optional[State]:
        """Get a specific state"""
        return self.states.get(state_type)
    
    def get_all_states(self) -> Dict[str, State]:
        """Get all states"""
        return self.states.copy()
    
    def compare_states(self, state_type1: str, state_type2: str) -> Dict[str, Any]:
        """Compare two states and return differences"""
        state1 = self.get_state(state_type1)
        state2 = self.get_state(state_type2)
        
        if not state1 or not state2:
            return {
                'error': f"One or both states not found: {state_type1}, {state_type2}",
                'differences': []
            }
        
        differences = self._find_differences(state1.data, state2.data)
        
        return {
            'state1': state_type1,
            'state2': state_type2,
            'timestamp': datetime.utcnow().isoformat(),
            'differences': differences
        }
    
    def _find_differences(self, data1: Any, data2: Any, path: str = "") -> List[Dict[str, Any]]:
        """Recursively find differences between two data structures"""
        differences = []
        
        if type(data1) != type(data2):
            differences.append({
                'path': path,
                'type': 'type_mismatch',
                'value1': str(data1),
                'value2': str(data2)
            })
            return differences
        
        if isinstance(data1, dict):
            all_keys = set(data1.keys()) | set(data2.keys())
            for key in all_keys:
                new_path = f"{path}.{key}" if path else key
                
                if key not in data1:
                    differences.append({
                        'path': new_path,
                        'type': 'added',
                        'value': data2[key]
                    })
                elif key not in data2:
                    differences.append({
                        'path': new_path,
                        'type': 'removed',
                        'value': data1[key]
                    })
                else:
                    differences.extend(self._find_differences(data1[key], data2[key], new_path))
        
        elif isinstance(data1, list):
            if len(data1) != len(data2):
                differences.append({
                    'path': path,
                    'type': 'length_changed',
                    'value1': len(data1),
                    'value2': len(data2)
                })
            
            for i in range(min(len(data1), len(data2))):
                new_path = f"{path}[{i}]"
                differences.extend(self._find_differences(data1[i], data2[i], new_path))
        
        elif data1 != data2:
            differences.append({
                'path': path,
                'type': 'value_changed',
                'value1': data1,
                'value2': data2
            })
        
        return differences
    
    def synchronize(self) -> Dict[str, Any]:
        """Synchronize all states and detect drift"""
        sync_result = {
            'timestamp': datetime.utcnow().isoformat(),
            'states_present': list(self.states.keys()),
            'drift_detected': [],
            'recommendations': []
        }
        
        # Compare current vs intended
        if StateType.CURRENT in self.states and StateType.INTENDED in self.states:
            current_intended_diff = self.compare_states(StateType.CURRENT, StateType.INTENDED)
            if current_intended_diff['differences']:
                sync_result['drift_detected'].append({
                    'type': 'current_vs_intended',
                    'differences': current_intended_diff['differences']
                })
                sync_result['recommendations'].append(
                    "Align current state with intended state"
                )
        
        # Compare current vs reference
        if StateType.CURRENT in self.states and StateType.REFERENCE in self.states:
            current_reference_diff = self.compare_states(StateType.CURRENT, StateType.REFERENCE)
            if current_reference_diff['differences']:
                sync_result['drift_detected'].append({
                    'type': 'current_vs_reference',
                    'differences': current_reference_diff['differences']
                })
                sync_result['recommendations'].append(
                    "Review deviations from reference architecture"
                )
        
        self._record_change("Performed state synchronization")
        return sync_result
    
    def _record_change(self, action: str) -> None:
        """Record a change in history"""
        self.history.append({
            'timestamp': datetime.utcnow().isoformat(),
            'action': action
        })
    
    def get_history(self) -> List[Dict[str, Any]]:
        """Get change history"""
        return self.history.copy()
