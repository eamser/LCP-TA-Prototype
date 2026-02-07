"""
ALM Delivery Integration Module
Integrates approved plans with ALM delivery systems
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import json


class DeliveryTask:
    """Represents a delivery task in ALM system"""
    
    def __init__(self, task_id: str, title: str, description: str):
        self.task_id = task_id
        self.title = title
        self.description = description
        self.status = "created"
        self.priority = "medium"
        self.assignee: Optional[str] = None
        self.created_at = datetime.utcnow().isoformat()
        self.updated_at = self.created_at
        self.subtasks: List[Dict[str, Any]] = []
    
    def add_subtask(self, subtask: Dict[str, Any]) -> None:
        """Add a subtask"""
        self.subtasks.append(subtask)
        self._update_timestamp()
    
    def assign(self, assignee: str) -> None:
        """Assign task to someone"""
        self.assignee = assignee
        self._update_timestamp()
    
    def set_priority(self, priority: str) -> None:
        """Set task priority"""
        self.priority = priority
        self._update_timestamp()
    
    def update_status(self, status: str) -> None:
        """Update task status"""
        self.status = status
        self._update_timestamp()
    
    def _update_timestamp(self) -> None:
        """Update the last modified timestamp"""
        self.updated_at = datetime.utcnow().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'task_id': self.task_id,
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'priority': self.priority,
            'assignee': self.assignee,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'subtasks': self.subtasks
        }


class ALMIntegration:
    """Integrates with ALM (Application Lifecycle Management) systems"""
    
    def __init__(self, alm_system: str = "generic"):
        self.alm_system = alm_system
        self.tasks: List[DeliveryTask] = []
        self.delivery_history: List[Dict[str, Any]] = []
    
    def create_delivery_plan(self, change_options: List[Any]) -> Dict[str, Any]:
        """Create delivery plan from approved change options"""
        plan = {
            'plan_id': f"plan_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
            'created_at': datetime.utcnow().isoformat(),
            'alm_system': self.alm_system,
            'tasks': [],
            'phases': [],
            'total_effort': 'unknown',
            'estimated_duration': 'unknown'
        }
        
        # Convert change options to delivery tasks
        for i, option in enumerate(change_options):
            task = self._convert_option_to_task(option, i + 1)
            self.tasks.append(task)
            plan['tasks'].append(task.to_dict())
        
        # Organize tasks into phases
        plan['phases'] = self._organize_into_phases(self.tasks)
        
        # Calculate effort and duration
        plan['total_effort'] = self._calculate_total_effort(self.tasks)
        plan['estimated_duration'] = self._estimate_duration(plan['phases'])
        
        self._record_delivery('plan_created', plan)
        return plan
    
    def _convert_option_to_task(self, option: Any, sequence: int) -> DeliveryTask:
        """Convert a change option to a delivery task"""
        option_dict = option.to_dict() if hasattr(option, 'to_dict') else option
        
        task_id = f"TASK-{sequence:04d}"
        task = DeliveryTask(
            task_id,
            option_dict.get('title', 'Untitled Task'),
            option_dict.get('description', '')
        )
        
        # Set priority based on impact
        impact = option_dict.get('impact', 'medium')
        priority_map = {
            'critical': 'critical',
            'high': 'high',
            'medium': 'medium',
            'low': 'low'
        }
        task.set_priority(priority_map.get(impact, 'medium'))
        
        # Add subtasks from benefits and risks
        for benefit in option_dict.get('benefits', []):
            task.add_subtask({
                'type': 'benefit',
                'description': benefit
            })
        
        for risk in option_dict.get('risks', []):
            task.add_subtask({
                'type': 'risk',
                'description': risk,
                'mitigation': 'To be defined'
            })
        
        return task
    
    def _organize_into_phases(self, tasks: List[DeliveryTask]) -> List[Dict[str, Any]]:
        """Organize tasks into delivery phases"""
        phases = []
        
        # Group by priority
        critical_tasks = [t for t in tasks if t.priority == 'critical']
        high_tasks = [t for t in tasks if t.priority == 'high']
        medium_tasks = [t for t in tasks if t.priority == 'medium']
        low_tasks = [t for t in tasks if t.priority == 'low']
        
        if critical_tasks:
            phases.append({
                'phase': 1,
                'name': 'Critical Changes',
                'task_ids': [t.task_id for t in critical_tasks]
            })
        
        if high_tasks:
            phases.append({
                'phase': len(phases) + 1,
                'name': 'High Priority Changes',
                'task_ids': [t.task_id for t in high_tasks]
            })
        
        if medium_tasks:
            phases.append({
                'phase': len(phases) + 1,
                'name': 'Medium Priority Changes',
                'task_ids': [t.task_id for t in medium_tasks]
            })
        
        if low_tasks:
            phases.append({
                'phase': len(phases) + 1,
                'name': 'Low Priority Changes',
                'task_ids': [t.task_id for t in low_tasks]
            })
        
        return phases
    
    def _calculate_total_effort(self, tasks: List[DeliveryTask]) -> str:
        """Calculate total effort estimate"""
        # This is a simplified calculation
        # In production, would use actual effort estimates
        effort_map = {
            'low': 1,
            'medium': 3,
            'high': 5,
            'critical': 8
        }
        
        total_points = sum(effort_map.get(task.priority, 3) for task in tasks)
        
        if total_points < 10:
            return 'small'
        elif total_points < 30:
            return 'medium'
        elif total_points < 50:
            return 'large'
        else:
            return 'extra_large'
    
    def _estimate_duration(self, phases: List[Dict[str, Any]]) -> str:
        """Estimate delivery duration"""
        phase_count = len(phases)
        
        if phase_count <= 1:
            return '1-2 months'
        elif phase_count <= 2:
            return '2-4 months'
        elif phase_count <= 3:
            return '4-6 months'
        else:
            return '6+ months'
    
    def submit_to_alm(self, delivery_plan: Dict[str, Any]) -> Dict[str, Any]:
        """Submit delivery plan to ALM system"""
        submission = {
            'submission_id': f"sub_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
            'plan_id': delivery_plan['plan_id'],
            'alm_system': self.alm_system,
            'submitted_at': datetime.utcnow().isoformat(),
            'status': 'submitted',
            'alm_references': []
        }
        
        # In production, this would actually integrate with ALM APIs
        # For now, simulate successful submission
        for task_dict in delivery_plan['tasks']:
            submission['alm_references'].append({
                'task_id': task_dict['task_id'],
                'alm_ticket': f"{self.alm_system.upper()}-{task_dict['task_id']}",
                'url': f"https://{self.alm_system}.example.com/ticket/{task_dict['task_id']}"
            })
        
        submission['status'] = 'completed'
        
        self._record_delivery('submitted_to_alm', submission)
        return submission
    
    def get_task_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get status of a specific task"""
        for task in self.tasks:
            if task.task_id == task_id:
                return task.to_dict()
        return None
    
    def update_task_status(self, task_id: str, status: str) -> bool:
        """Update task status"""
        for task in self.tasks:
            if task.task_id == task_id:
                task.update_status(status)
                self._record_delivery('task_status_updated', {
                    'task_id': task_id,
                    'new_status': status
                })
                return True
        return False
    
    def _record_delivery(self, action: str, data: Dict[str, Any]) -> None:
        """Record delivery action in history"""
        self.delivery_history.append({
            'timestamp': datetime.utcnow().isoformat(),
            'action': action,
            'data_summary': {
                k: v for k, v in data.items() 
                if k in ['plan_id', 'submission_id', 'task_id', 'status']
            }
        })
    
    def get_delivery_history(self) -> List[Dict[str, Any]]:
        """Get delivery history"""
        return self.delivery_history.copy()
