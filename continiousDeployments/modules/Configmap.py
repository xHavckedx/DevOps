def generate_configmap_content():
    return """example.example=example
    # Agregar aquí los datos del ConfigMap
    """
def make(args):
    deployment = args.deployment 
    configmap_content = generate_configmap_content()
    with open(f"./{deployment}/application.properties", "w") as f:
        f.write(configmap_content)