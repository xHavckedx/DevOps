# Generar el manifiesto del ingress público
def make(deployment, healthcheck_path, service_port,environment):
    with open(f"./{deployment}/{deployment}-ingress-pub.yaml", "w") as f:
        f.write(
    f"""---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: {deployment}-ingress-pub
  namespace: {deployment}
  annotations:
    # Do not scrape (auth is required) we use manifest-file-ingress-int to monitor it
    prometheus.io/scrape: "true"
    prometheus.io/scheme: "https"
    prometheus.io/path: /{deployment}{healthcheck_path}
    nginx.ingress.kubernetes.io/proxy-body-size: 10m
    nginx.ingress.kubernetes.io/use-regex: "true"
    nginx.ingress.kubernetes.io/rewrite-target: /$1
    # nginx.ingress.kubernetes.io/auth-type: basic
    # nginx.ingress.kubernetes.io/auth-secret: manifest-file-basic-auth
    # nginx.ingress.kubernetes.io/auth-secret-type: auth-map
    # nginx.ingress.kubernetes.io/auth-realm: "Enter your credentials"
  spec:
    ingressClassName: nginx-pub
    rules:
    - host: {"cloud" if environment == 'pro' else "staging"}-apps-01-pub.cttexpress.com
      http:
      paths:
      - path: /{deployment}/(.*)
        pathType: Prefix
        backend:
          service:
            name: {deployment}-service
            port:
            number: {service_port}
""")