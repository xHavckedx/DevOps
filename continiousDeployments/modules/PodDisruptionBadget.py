def generate_pdb_manifest(deployment):
    return f"""---
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: {deployment}-pdb
spec:
  minAvailable: 1
  selector:
    matchLabels:
      app.kubernetes.io/name: {deployment}
    """

def make(args):
    deployment = args.deployment
    pdb_manifest = generate_pdb_manifest(deployment)
    with open(f"./{deployment}/{deployment}-bdb.yaml", "w") as f:
        f.write(pdb_manifest)