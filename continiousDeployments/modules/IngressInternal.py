def generate_ingress_internal_manifest(deployment, healthcheck_path, environment, service_port):
    host = "cloud-apps-01-int.cttexpress.com" if environment == 'pro' else "staging-apps-01-int.cttexpress.com"
    return f"""---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: {deployment}-ingress-int
  namespace: {deployment}
  annotations:
    prometheus.io/scrape: "true"
    prometheus.io/scheme: "https"
    prometheus.io/path: /{deployment}{healthcheck_path}
    nginx.ingress.kubernetes.io/proxy-body-size: 10m
    nginx.ingress.kubernetes.io/use-regex: "true"
    nginx.ingress.kubernetes.io/rewrite-target: /$1
    nginx.ingress.kubernetes.io/service-upstream: "true" # Required for linkerd
spec:
  ingressClassName: nginx-int
rules:
- host: {host}
  http:
  paths:
  - path: /{deployment}/(.*)
    pathType: Prefix
    backend:
      service:
        name: {deployment}-service
        port:
        number: {service_port}
"""

def make(args):
    deployment = args.deployment
    healthcheck_path = args.healthcheck_path
    environment = args.environment
    service_port = args.service_port
    ingress_internal_manifest = generate_ingress_internal_manifest(deployment, healthcheck_path, environment, service_port)
    with open(f"./{deployment}/{deployment}-ingress-int.yaml", "w") as f:
        f.write(ingress_internal_manifest)