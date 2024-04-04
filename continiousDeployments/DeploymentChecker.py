#TODO se descarga 
from DevOpsDeploy import generate_manifests, args
def checkContext():
    print("some code here")
    
def checkFiles():
    try:
        args = args()
        deployment = args.deployment
        
        if open(f"./{deployment}/{deployment}-deployment.yaml"): # Comprueba si existen los ficheros, si no existe, los crea.
            checkContext() #Comprueba que los ficheros estén en la versión actual.
        else:
            print("Generar los ficheros aquí.") 
            generate_manifests()
        return 0
    except Exception:
        raise Exception
        return 1