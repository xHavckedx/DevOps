import argparse
import os
from modules import (Deployment, Configmap, HorizontalPodAutoScaler, IngressExternal, 
           IngressInternal, Kustomization, Namespace, PodDisruptionBadget, Service, Secret)
from modules.monitoring import Monitoring

class ManifestGenerator:
  def __init__(self, args):
    self.args = args

  def generate_manifests(self): 
    try:
      Deployment.make(self.args)
      Service.make(self.args)
      if self.args.configmap:
        Configmap.make(self.args)
      if self.args.secret:
        Secret.make(self.args)
      Namespace.make(self.args)
      PodDisruptionBadget.make(self.args)
      Kustomization.make(self.args)
      HorizontalPodAutoScaler.make(self.args)
      if self.args.ingress in ['int', 'both']:
        IngressInternal.make(self.args)
      if self.args.ingress in ['pub', 'both']:
        IngressExternal.make(self.args)
      Monitoring.init(self.args)
      print("Manifiestos generados correctamente.")
    except Exception as e:
      print(f"Manifiestos generados incorrectamente: {e}")

def main():
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
  args = parser.parse_args()

  try:
    os.mkdir(args.deployment)
    print(f"Directorio '{args.deployment}' creado exitosamente.")
    generator = ManifestGenerator(args)
    generator.generate_manifests()
  except FileExistsError:
    print(f"El directorio '{args.deployment}' ya existe.")
  except Exception as e:
    print(f"Error al crear el directorio '{args.deployment}': {e}")

if __name__ == "__main__":
  main()