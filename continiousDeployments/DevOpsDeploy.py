from os import mkdir
import argparse
import Deployment
import Configmap
import HorizontalPodAutoScaler
import IngressExternal
import IngressInternal
import Kustomization
import Namespace
import Monitoring.Monitoring as Monitoring
import PodDisruptionBadget
import Service
import Secret

args = {}

def generate_manifests(deployment, metrics_path, healthcheck_path, service_port, global_configmap, configmap, secret, image_name, image_version, environment, ingress_type, outbox): 
  try:
    # Generar el manifiesto del deployment
    Deployment.make(deployment, metrics_path, healthcheck_path, service_port, global_configmap, configmap, image_name, image_version, secret, outbox, environment)

    # Generar el manifiesto del Service
    Service.make(deployment, service_port)
    
    # Generar el manifiesto del configmap
    if configmap:
      Configmap.make(deployment)
    
    # Generar el manifiesto del secret
    if secret:
      Secret.make(deployment, environment)
      
    # Generar el manifiesto del namespace
    Namespace.make(deployment)

    # Generar el manifiesto del bdb
    PodDisruptionBadget.make(deployment)
    
    # Generar el manifiesto kustomization
    Kustomization.make(deployment, configmap, ingress_type, secret)
    
    # Generar el manifiesto HPA
    HorizontalPodAutoScaler.make(deployment)
    
    if ingress_type == 'int':
      # Generar el manifiesto ingress int
      IngressInternal.make(deployment, healthcheck_path, service_port, environment)
    elif ingress_type == 'pub':
      # Generar el manifiesto ingress pub
      IngressExternal.make(deployment, healthcheck_path, service_port, environment)
    elif ingress_type == 'both':
      # Generar el manifiesto ingress puby int
      IngressExternal.make(deployment, healthcheck_path, service_port, environment)
      IngressInternal.make(deployment, healthcheck_path, service_port, environment)
      
    Monitoring.make()
    
    print("Manifiestos generados correctamente.")
  except Exception:
    print("Manifiestos generados incorrectamente.")
    print(Exception)

# def setArgs(self, args):
#   self.args = args

# def args(self):
#   return self.args

def main():
  # TODO Añadir bandera de autinstrumentación o no, añadir bandera de hpa, añadir bandera de ingress y tipo de ingress [int,pub,both]
    parser = argparse.ArgumentParser(description="Generar manifiestos de Kubernetes para un Deployment")
    parser.add_argument("-d", "--deployment", help="Nombre del deploy", required=True)
    parser.add_argument("-i", "--image-name", help="Nombre de la imagen", required=True)
    parser.add_argument("-v", "--image-version", help="Versión de la imagen", required=True)
    parser.add_argument("-p", "--service-port", help="Puerto del servicio", required=True, type=int)
    parser.add_argument("-e", "--environment", help="Entorno donde se desplegará [stg,pro]", choices=['stg', 'pro'], required=True)
    parser.add_argument("-gc", "--global-configmap", help="ConfigMap global", action="store_true")
    parser.add_argument("-m", "--metrics-path", help="Ruta de las métricas")
    parser.add_argument("-H", "--healthcheck-path", help="Ruta del healthcheck")
    parser.add_argument("-c", "--configmap", help="ConfigMap(application.properties)", action="store_true")
    parser.add_argument("-s", "--secret", help="External secret", action="store_true")
    parser.add_argument("-I", "--ingress", help="Tipo de ingress [int,pub,both]", choices=['int', 'pub', 'both'])
    parser.add_argument("-o", "--outbox", help="Si contiene outbox o no", action="store_true")
    parser.epilog = """Ejemplo de uso:
    
    python3 script.py -d my-image -i url/my-image -v 1.0 -p 8080 -e pro -gc -m /metrics -H /healthcheck -c -s -I both -o
    """
    args = parser.parse_args()
    #setArgs(args)
    # Generar carpeta
    try:
        mkdir(args.deployment)
        print(f"Directorio '{args.deployment}' creado exitosamente.")
        # Generar manifiestos
        generate_manifests(args.deployment, args.metrics_path, args.healthcheck_path, args.service_port, args.global_configmap, args.configmap, args.secret, args.image_name, args.image_version, args.environment, args.ingress, args.outbox)
    except FileExistsError:
        print(f"El directorio '{args.deployment}' ya existe.")
    except Exception as e:
        print(f"Error al crear el directorio '{args.deployment}': {e}")

if __name__ == "__main__":
    main()
