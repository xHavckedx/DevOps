# Generar el manifiesto del namespace
def make(deployment):                
    with open(f"./{deployment}/{deployment}-namespace.yaml", "w") as f:
        f.write(
    f"""---
apiVersion: v1
kind: Namespace
metadata:
    name: {deployment}
# Agregar aquí los datos del namespace
    """)
    