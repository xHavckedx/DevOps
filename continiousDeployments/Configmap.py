# Generar el ConfigMap
def make(deployment): 
    with open(f"./{deployment}/application.properties", "w") as f:
        f.write(
    f"""example.example=example
    # Agregar aquí los datos del ConfigMap global
    """)