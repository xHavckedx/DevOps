# Generar Secret
def make(deployment, environment):
    with open(f"./{deployment}/{deployment}-es.yaml", "w") as f:
        f.write(
    f"""---
apiVersion: kubernetes-client.io/v1
kind: ExternalSecret
metadata:
  name: {deployment}-secret
spec:
  backendType: secretsManager
  region: {"eu-central-1" if environment == 'pro' else "eu-west-1"}
  dataFrom: 
  - {"cloud-apps-01-pro" if environment == 'pro' else "staging-apps-01"}/{deployment}-service/secret
  template:
    metadata:
      annotations:
        created-by: external-secret 
""")