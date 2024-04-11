from modules.monitoring import(Opentelemetry, MongodbExporter)
from os import mkdir

def GenerateMonitoringDir(deployment):
    try:
        mkdir(f"{deployment}/monitoring")
        print(f"Directorio 'monitoring' creado exitosamente.")
    except Exception:
        raise Exception
    
def init(args):
    deployment = args.deployment
    env = args.environment
    GenerateMonitoringDir(deployment)    
    MongodbExporter.make(deployment, "<GENERIC-DATABASE-NULL>", env)
    Opentelemetry.make(deployment)
    print("make")