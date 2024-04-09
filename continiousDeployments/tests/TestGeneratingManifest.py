import unittest
from unittest.mock import patch
import sys
from io import StringIO
import os
import DevOpsDeploy

def mock_user_input(mock_input, expected_output):
    return lambda _: expected_output.pop(0)

class TestArgumentValidation(unittest.TestCase):

    def setUp(self):
        self.old_sys_argv = sys.argv.copy()

    def tearDown(self):
        sys.argv = self.old_sys_argv
        if os.path.exists('test_dir'):
            os.rmdir('test_dir')

    def test_invalid_ingress_flag(self):
        args = ['-d', 'test_dir', '-i', 'test_image', '-v', '1.0', '-p', '8080', '-e', 'pro', '-gc', '-I', 'invalid', '-o']
        with patch('builtins.input', side_effect=mock_user_input([], None)), \
             patch('sys.stdout', new=StringIO()) as mock_stdout:
            with self.assertRaises(SystemExit) as cm:
                DevOpsDeploy.main(args)
            self.assertEqual(cm.exception.code, 2)
            self.assertIn("invalid choice: 'invalid'", mock_stdout.getvalue())
    
    def test_invalid_environment_flag(self):
        args = ['-d', 'test_dir', '-i', 'test_image', '-v', '1.0', '-p', '8080', '-e', 'invalid', '-gc', '-I', 'both', '-o']
        with patch('builtins.input', side_effect=mock_user_input([], None)), \
                patch('sys.stdout', new=StringIO()) as mock_stdout:
            with self.assertRaises(SystemExit) as cm:
                DevOpsDeploy.main(args)
            self.assertEqual(cm.exception.code, 2)
            self.assertIn("invalid choice: 'invalid'", mock_stdout.getvalue())

    def test_invalid_service_port_flag(self):
        args = ['-d', 'test_dir', '-i', 'test_image', '-v', '1.0', '-p', 'abc', '-e', 'stg', '-gc', '-I', 'stg', '-o']
        with patch('builtins.input', side_effect=mock_user_input([], None)), \
             patch('sys.stdout', new=StringIO()) as mock_stdout:
            with self.assertRaises(SystemExit) as cm:
                DevOpsDeploy.main(args)
            self.assertEqual(cm.exception.code, 2)
            self.assertIn("argument -p/--service-port: invalid int value: 'abc'", mock_stdout.getvalue())

if __name__ == '__main__':
    unittest.main()
