def generate_namespace_manifest(deployment):
    return f"""---
apiVersion: v1
kind: Namespace
metadata:
    name: {deployment}
# Agregar aquí los datos del namespace
"""

def make(args):
    deployment = args.deployment
    namespace_manifest = generate_namespace_manifest(deployment)
    with open(f"./{deployment}/{deployment}-namespace.yaml", "w") as f:
        f.write(namespace_manifest)