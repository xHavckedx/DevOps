def generate_service_manifest(deployment, service_port):
  return f"""---
apiVersion: v1
kind: Service
metadata:
  name: {deployment}-service
  namespace: {deployment}
  labels:
    app: {deployment}-service
    project: {deployment}
    developer: leo
spec:
  selector:
    app.kubernetes.io/name: {deployment}
  ports:
  - protocol: TCP
    port: {service_port}
    targetPort: app
"""

def make(args):
  deployment = args.deployment
  service_port = args.service_port 
  service_manifest = generate_service_manifest(deployment, service_port)
  with open(f"./{deployment}/{deployment}-service.yaml", "w") as f:
      f.write(service_manifest)