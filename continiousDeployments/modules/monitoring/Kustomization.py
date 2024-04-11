def make(deployment, database, env):
    with open(f"./monitoring/kustomization.yaml", "w") as f:
        f.write(f"""
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

configMapGenerator:
- name: grafana-dashboards

  files:
  - dashboards/manifest-file-dashboard.json

generatorOptions:
  disableNameSuffixHash: true
  labels:
    grafana_dashboard: "1"
  annotations:
    k8s-sidecar-target-directory: /tmp/dashboards/100 - Application - Manifests File

resources:
- manifest-file-prometheusrules.yaml
- mongodb-database-exporter-deployment.yaml          
""")