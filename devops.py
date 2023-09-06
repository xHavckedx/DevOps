import sys
import os
import argparse

parser = argparse.ArgumentParser(prog="DevOps")
#parser.add_argument("-o", "--opcion", dest = "opcion", help="restart o mail", required=True)
parser.add_argument("opcion")
parser.add_argument("-d", "--destinatario", dest = "receiverEmail", help = "Nombre del destinatario")
parser.add_argument("-s", "--subject", dest = "subject", help = "Cuerpo del subject")
parser.add_argument("-f", "--file", dest = "html", help = "Archivo html con el cuerpo del mensaje")
parser.add_argument("-e", "--env", dest = "entorno", help = "entorno")
parser.add_argument("-a", "--account-service", dest = "account", help = "account service")
parser.add_argument("-t", "--topics", dest = "topics", help = "topics")
parser.add_argument("-o", "--operations", dest = "operations", help = "operations")
args = parser.parse_args()
arg1 = sys.argv[1]
if arg1 == 'restart': #args.opcion == 'restart':
  if len(sys.argv) >= 2:
    if args.entorno in  ['stg', 'pro', 'mstg', 'mpro']:
      os.system(f"restart {args.entorno}")
    else:
      print(f"Agrega -e [stg | pro | mstg | mpro]")
elif arg1 == 'mail': #args.opcion  == 'mail':
  if len(sys.argv) >= 4:
    os.system(f"python3 ~/DevOps/tools/senderEmail.py -d {args.receiverEmail} -s \"{args.subject}\" -f \"{args.html}\"")
  else:
    print("Agrega -d \"DESTINATARIO\" -s \"SUBJECT\" -f \"FILE\"")
elif arg1 == 'confluent':
  if len(sys.argv) >= 2:
    topics = args.topics.split(',')
    print(f'Imprimiendo la lista de topicos: {topics}')
    os.system(f"confluent login --save")
    os.system(f"confluent environment use env-gq128r")
    for t in topics:
      os.system(f"confluent kafka acl create --allow --service-account {args.account} --operations {args.operations} --prefix --topic {t}")
      print(f"confluent kafka acl create --allow --service-account {args.account} --operations {args.operations} --prefix --topic {t}")
exit()
