# Generar el manifiesto del hpa
def make(deployment):
    with open(f"./{deployment}/{deployment}-hpa.yaml", "w") as f:
          f.write(
    f"""---
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: {deployment}-hpa
spec:
  minReplicaCount: 2
  maxReplicaCount: 5
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: {deployment}
  pollingInterval:  30
  cooldownPeriod:   120
  triggers:
    - type: prometheus
      metadata:
        serverAddress: http://prometheus-operated.observability-peer.svc:9090
        metricName: {deployment}_request_per_pod
        threshold: '10'
        query: avg(sum(irate(nginx_ingress_controller_requests{{service="{deployment}"}}[120s])) by (pod)) or vector(0)

    - type: prometheus
      metricType: AverageValue # https://keda.sh/docs/2.9/concepts/scaling-deployments/#triggers (keda ya lo divide por el numero de pods)
      metadata:
        serverAddress: http://prometheus-operated.observability-peer.svc:9090
        metricName: kafka_consumergroup_level
        threshold: '1000'
        query: sum(kafka_consumergroup_lag{{consumergroup="{deployment}"}}) > 0 or vector(0)

    - type: cpu
      metadata:
        type: Utilization
        value: "60"
    
    - type: memory
      metadata:
        type: Utilization
        value: "80"
""")