#python3 senderEmail.py -d correoDestinatario -s subject -f html
import smtplib, ssl, argparse
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--destinatario", dest = "receiverEmail", help = "Nombre del destinatario", required=True)
parser.add_argument("-s", "--subject", dest = "subject", help = "Cuerpo del subject", required=True)
parser.add_argument("-f", "--file", dest = "html", help = "Archivo html con el cuerpo del mensaje", required=True)
args = parser.parse_args()

if args.receiverEmail is not None:
  sender_email = "francescgc2010@gmail.com"
  receiver_email = args.receiverEmail
  password = input("Escribe tu contraseña aquí: ")
  
  message = MIMEMultipart("alternative")
  message["Subject"] = args.subject
  message["From"] = sender_email
  message["To"] = receiver_email
  html = args.html
  
  # Create the plain-text and HTML version of your message
  text = """\
  Hi,
  How are you?
  Real Python has many great tutorials:
  www.realpython.com"""
  
  # Turn these into plain/html MIMEText objects
  part1 = MIMEText(text, "plain")
  part2 = MIMEText(html, "html")
  
  # Add HTML/plain-text parts to MIMEMultipart message
  # The email client will try to render the last part first
  message.attach(part1)
  message.attach(part2)
  
  # Create secure connection with server and send email
  context = ssl.create_default_context()
  with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
      server.login(sender_email, password)
      server.sendmail(
          sender_email, receiver_email, message.as_string()
      )
else:
  print("Utiliza --help para saber como funciona el comando")
