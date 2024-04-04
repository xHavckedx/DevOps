# Generar el manifiesto del bdb
def make(deployment):
    with open(f"./{deployment}/{deployment}-bdb.yaml", "w") as f:
          f.write(
    f"""---
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: {deployment}-pdb
spec:
  minAvailable: 1
  selector:
    matchLabels:
      app.kubernetes.io/name: {deployment}
    """)