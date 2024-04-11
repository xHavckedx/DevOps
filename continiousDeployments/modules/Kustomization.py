def generate_kustomization_content(deployment, ingress_type, secret, configmap):
  resources = [
    f"{deployment}-namespace.yaml",
    f"{deployment}-deployment.yaml",
    f"{deployment}-service.yaml",
    f"{deployment}-bdb.yaml",
    f"{deployment}-hpa.yaml",
  ]

  if ingress_type in ["int", "both"]:
    resources.append(f"{deployment}-ingress-int.yaml")
  if ingress_type in ["pub", "both"]:
    resources.append(f"{deployment}-ingress-pub.yaml")
  if secret:
    resources.append(f"{deployment}-es.yaml")

  resources_str = "\n- ".join(resources)

  configmap_str = ""
  if configmap:
    configmap_str = f"""configMapGenerator:
- files:
  - application.properties
  name: {deployment}-service-properties"""

  return f"""---
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

namespace: {deployment}

# Monitoring
resources:
- {resources_str}

# TODO GENERAR ESTOS MANIFIESTOS
#- {deployment}-es-mongodb.yaml
#- {deployment}-es-kafka.yaml
#- {deployment}-config.yaml
#- monitoring

{configmap_str}
"""

def make(args): 
  deployment = args.deployment
  ingress_type = args.ingress
  secret = args.secret
  configmap = args.configmap
  kustomization_content = generate_kustomization_content(deployment, ingress_type, secret, configmap)
  with open(f"./{deployment}/kustomization.yaml", "w") as f:
    f.write(kustomization_content)