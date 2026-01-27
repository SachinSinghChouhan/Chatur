
import unittest
from unittest.mock import MagicMock, patch
from chatur.handlers.tasks import GoogleTasksHandler
from chatur.models.intent import Intent, IntentType

class TestTasksHandler(unittest.TestCase):
    def setUp(self):
        # Patch Credentials
        self.creds_patcher = patch('chatur.handlers.tasks.Credentials')
        self.mock_creds = self.creds_patcher.start()
        
        # Patch build
        self.build_patcher = patch('chatur.handlers.tasks.build')
        self.mock_build = self.build_patcher.start()
        self.mock_service = MagicMock()
        self.mock_build.return_value = self.mock_service
        
        # Patch Path.exists specifically for the module
        self.path_patcher = patch('chatur.handlers.tasks.Path.exists')
        self.mock_exists = self.path_patcher.start()
        self.mock_exists.return_value = True

        try:
            self.handler = GoogleTasksHandler()
        except Exception as e:
            print(f"Handler init failed: {e}")
            raise e

    def tearDown(self):
        self.creds_patcher.stop()
        self.build_patcher.stop()
        self.path_patcher.stop()

    def test_add_task(self):
        intent = Intent(
            type=IntentType.TASK,
            language='en',
            parameters={'action': 'add', 'title': 'Buy milk'},
            response_language='en'
        )
        
        # Setup mock return
        self.mock_service.tasks().insert.return_value.execute.return_value = {
            'id': '123', 'title': 'Buy milk'
        }
        
        response = self.handler.handle(intent)
        
        self.assertIn("Added 'Buy milk'", response)
        self.mock_service.tasks().insert.assert_called_once()

    def test_list_tasks(self):
        intent = Intent(
            type=IntentType.TASK,
            language='en',
            parameters={'action': 'list'},
            response_language='en'
        )
        
        # Setup mock return
        self.mock_service.tasks().list.return_value.execute.return_value = {
            'items': [
                {'title': 'Task 1'},
                {'title': 'Task 2'}
            ]
        }
        
        response = self.handler.handle(intent)
        
        self.assertIn("Here are your tasks", response)
        self.assertIn("Task 1", response)
        self.assertIn("Task 2", response)

    def test_complete_task(self):
        intent = Intent(
            type=IntentType.TASK,
            language='en',
            parameters={'action': 'complete', 'title': 'Task 1'},
            response_language='en'
        )
        
        # Setup mock return for list
        self.mock_service.tasks().list.return_value.execute.return_value = {
            'items': [
                {'id': '1', 'title': 'Task 1'},
                {'id': '2', 'title': 'Task 2'}
            ]
        }
        
        # Setup mock return for update
        self.mock_service.tasks().update.return_value.execute.return_value = {
            'id': '1', 'title': 'Task 1', 'status': 'completed'
        }
        
        response = self.handler.handle(intent)
        
        self.assertIn("Completed task: Task 1", response)
        self.mock_service.tasks().list.assert_called()
        self.mock_service.tasks().update.assert_called()

if __name__ == '__main__':
    unittest.main()
