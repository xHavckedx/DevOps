import Monitoring.Opentelemetry as Opentelemetry
import Monitoring.MongodbExporter as Mongodb
from os import mkdir

def GenerateMonitoringDir(deployment):
    try:
        mkdir(f"{deployment}/monitoring")
        print(f"Directorio 'monitoring' creado exitosamente.")
    except Exception:
        raise Exception
    
def init(deployment, env):
    GenerateMonitoringDir(deployment)    
    Mongodb.make(deployment, "<GENERIC-DATABASE-NULL>", env)
    Opentelemetry.make()
    print("make")