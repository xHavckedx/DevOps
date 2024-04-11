import sys
from io import StringIO
import os
import pytest
from unittest.mock import patch, MagicMock
import  DevOpsDeploy  

def mock_user_input(mock_input, expected_output):
    return lambda _: expected_output.pop(0)

@pytest.fixture
def clean_sys_argv():
    old_sys_argv = sys.argv.copy()
    yield
    sys.argv = old_sys_argv

@pytest.fixture
def clean_test_dir():
    if os.path.exists('test_dir'):
        os.rmdir('test_dir')

def test_invalid_ingress_flag():
    args = ['-d', 'test_dir', '-i', 'test_image', '-v', '1.0', '-p', '8080', '-e', 'pro', '-gc', '-I', 'invalid', '-o']
    with patch('sys.argv', args), patch('sys.stderr', new=StringIO()) as mock_stderr:
        with pytest.raises(SystemExit) as cm:
            DevOpsDeploy.main()
    mock_stderr.seek(0)  # Movemos el cursor al inicio del buffer StringIO
    error_output = mock_stderr.read()  # Leemos todo el contenido del buffer
    assert cm.value.code == 2
    assert "invalid choice: 'invalid'" in error_output



def test_invalid_environment_flag():
    args = ['-d', 'test_dir', '-i', 'test_image', '-v', '1.0', '-p', '8080', '-e', 'invalid', '-gc', '-I', 'both', '-o']
    with patch('sys.argv', args), \
            patch('sys.stderr', new=StringIO()) as mock_stderr:
        with pytest.raises(SystemExit) as cm:
            DevOpsDeploy.main()
        mock_stderr.seek(0)  # Movemos el cursor al inicio del buffer StringIO
        error_output = mock_stderr.read()  # Leemos todo el contenido del buffer
        assert cm.value.code == 2
        assert "invalid choice: 'invalid'" in error_output

def test_service_port_type_string():
    args = ['-d', 'test_dir', '-i', 'test_image', '-v', '1.0', '-p', 'invalid', '-e', 'pro']
    with patch('sys.argv', args), \
         patch('sys.stderr', new=StringIO()) as mock_stderr:
        with pytest.raises(SystemExit) as cm:
            DevOpsDeploy.main()
        mock_stderr.seek(0)  # Movemos el cursor al inicio del buffer StringIO
        error_output = mock_stderr.read()  # Leemos todo el contenido del buffer
        assert cm.value.code == 2
        assert "invalid int value: 'invalid'" in error_output
