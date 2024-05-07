import pytest
from unittest.mock import call, patch, MagicMock
from DevOpsDeploy import main

@patch('os.mkdir')
@patch('builtins.print')
@patch('argparse.ArgumentParser.parse_args')
def test_main_success(mock_args, mock_print, mock_mkdir):
    mock_args.return_value = MagicMock(deployment='test')
    main()
    mock_mkdir.assert_called_once_with('test')
    mock_print.assert_has_calls([
        call("Directorio 'test' creado exitosamente."),
    ])

@patch('os.mkdir')
@patch('builtins.print')
@patch('argparse.ArgumentParser.parse_args')
def test_main_directory_exists(mock_args, mock_print, mock_mkdir):
    mock_args.return_value = MagicMock(deployment='test')
    mock_mkdir.side_effect = FileExistsError
    main()
    mock_print.assert_called_once_with("El directorio 'test' ya existe.")

@patch('os.mkdir')
@patch('builtins.print')
@patch('argparse.ArgumentParser.parse_args')
def test_main_error(mock_args, mock_print, mock_mkdir):
    mock_args.return_value = MagicMock(deployment='test')
    mock_mkdir.side_effect = Exception('Some error')
    main()
    mock_print.assert_called_once_with("Error al crear el directorio 'test': Some error")

@patch('DevOpsDeploy.Deployment.make')
@patch('DevOpsDeploy.Service.make')
@patch('DevOpsDeploy.Configmap.make')
@patch('DevOpsDeploy.Secret.make')
@patch('DevOpsDeploy.Namespace.make')
@patch('DevOpsDeploy.PodDisruptionBadget.make')
@patch('DevOpsDeploy.Kustomization.make')
@patch('DevOpsDeploy.HorizontalPodAutoScaler.make')
@patch('DevOpsDeploy.IngressInternal.make')
@patch('DevOpsDeploy.IngressExternal.make')
@patch('DevOpsDeploy.Monitoring.init')
@patch('builtins.print')
@patch('argparse.ArgumentParser.parse_args')
def test_generate_manifests_success(mock_args, mock_print, mock_monitoring_init, mock_ingress_external_make,
                                   mock_ingress_internal_make, mock_horizontal_pod_auto_scaler_make,
                                   mock_kustomization_make, mock_pod_disruption_badget_make, mock_namespace_make,
                                   mock_secret_make, mock_configmap_make, mock_service_make, mock_deployment_make):
    mock_args.return_value = MagicMopopck(deployment='test', configmap=True, secret=True, ingress='both')
    main()
    mock_deployment_make.assert_called_once_with(mock_args)
    mock_service_make.assert_called_once_with(mock_args)
    mock_configmap_make.assert_called_once_with(mock_args)
    mock_secret_make.assert_called_once_with(mock_args)
    mock_namespace_make.assert_called_once_with(mock_args)
    mock_pod_disruption_badget_make.assert_called_once_with(mock_args)
    mock_kustomization_make.assert_called_once_with(mock_args)
    mock_horizontal_pod_auto_scaler_make.assert_called_once_with(mock_args)
    mock_ingress_internal_make.assert_called_once_with(mock_args)
    mock_ingress_external_make.assert_called_once_with(mock_args)
    mock_monitoring_init.assert_called_once_with(mock_args)
    mock_print.assert_called_once_with("Manifiestos generados correctamente.")

@patch('DevOpsDeploy.Deployment.make')
@patch('DevOpsDeploy.Service.make')
@patch('DevOpsDeploy.Configmap.make')
@patch('DevOpsDeploy.Secret.make')
@patch('DevOpsDeploy.Namespace.make')
@patch('DevOpsDeploy.PodDisruptionBadget.make')
@patch('DevOpsDeploy.Kustomization.make')
@patch('DevOpsDeploy.HorizontalPodAutoScaler.make')
@patch('DevOpsDeploy.IngressInternal.make')
@patch('DevOpsDeploy.IngressExternal.make')
@patch('DevOpsDeploy.Monitoring.init')
@patch('builtins.print')
@patch('argparse.ArgumentParser.parse_args')
def test_generate_manifests_error(mock_args, mock_print, mock_monitoring_init, mock_ingress_external_make,
                                 mock_ingress_internal_make, mock_horizontal_pod_auto_scaler_make,
                                 mock_kustomization_make, mock_pod_disruption_badget_make, mock_namespace_make,
                                 mock_secret_make, mock_configmap_make, mock_service_make, mock_deployment_make):
    mock_args.return_value = MagicMock(deployment='test', configmap=True, secret=True, ingress='both')
    mock_deployment_make.side_effect = Exception('Some error')
    main()
    mock_deployment_make.assert_called_once_with(mock_args)
    mock_service_make.assert_called_once_with(mock_args)
    mock_configmap_make.assert_called_once_with(mock_args)
    mock_secret_make.assert_called_once_with(mock_args)
    mock_namespace_make.assert_called_once_with(mock_args)
    mock_pod_disruption_badget_make.assert_called_once_with(mock_args)
    mock_kustomization_make.assert_called_once_with(mock_args)
    mock_horizontal_pod_auto_scaler_make.assert_called_once_with(mock_args)
    mock_ingress_internal_make.assert_called_once_with(mock_args)
    mock_ingress_external_make.assert_called_once_with(mock_args)
    mock_monitoring_init.assert_called_once_with(mock_args)
    mock_print.assert_called_once_with("Manifiestos generados incorrectamente: Some error")