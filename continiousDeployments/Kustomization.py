# Generar el kustomization.yaml
def make(deployment,configmap, ingress_type, secret): 
    with open(f"./{deployment}/kustomization.yaml", "w") as f:
        f.write(
    f"""---
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

namespace: {deployment}

# Monitoring
resources:
- {deployment}-namespace.yaml
- {deployment}-deployment.yaml
- {deployment}-service.yaml
- {deployment}-bdb.yaml
- {deployment}-hpa.yaml
{f"""- {deployment}-ingress-int.yaml{"\n" if (ingress_type == 'both' or secret) else ''}""" if (ingress_type == "int" or ingress_type ==  "both") else '' }{f"""- {deployment}-ingress-pub.yaml{"\n" if secret else ''}""" if (ingress_type == "pub" or ingress_type ==  "both") else ''}{f"""- {deployment}-es.yaml""" if secret else ''}
# TODO GENERAR ESTOS MANIFIESTOS
#- {deployment}-es-mongodb.yaml
#- {deployment}-es-kafka.yaml
#- {deployment}-config.yaml
#- monitoring

{f"""configMapGenerator:
- files:
  - application.properties
  name: {deployment}-service-properties""" if configmap else ""}
""")