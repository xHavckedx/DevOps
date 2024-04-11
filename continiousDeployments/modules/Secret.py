def generate_external_secret_manifest(deployment, environment):
    region = "eu-central-1" if environment == 'pro' else "eu-west-1"
    data_from = "cloud-apps-01-pro" if environment == 'pro' else "staging-apps-01"
    return f"""---
apiVersion: kubernetes-client.io/v1
kind: ExternalSecret
metadata:
  name: {deployment}-secret
spec:
  backendType: secretsManager
  region: {region}
  dataFrom: 
  - {data_from}/{deployment}-service/secret
  template:
    metadata:
      annotations:
        created-by: external-secret 
"""

def make(args):
    deployment = args.deployment
    environment = args.environment
    external_secret_manifest = generate_external_secret_manifest(deployment, environment)
    with open(f"./{deployment}/{deployment}-es.yaml", "w") as f:
        f.write(external_secret_manifest)