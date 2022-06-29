import pandas as pd
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import base64, MySQLdb, os

#Funcion que servira para nombrar los meses
def numToMon(posicion):
    mes=["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
    posicion-=1
    return mes[posicion]

#Lectura del archivo
df=pd.read_csv('data.csv')

#Calculo del balance total
total_balance=df['Transactions'].sum()

#Calculo de transacciones por mes
num_trans_mon={}
for fecha in df['Date']:
    fecha=datetime.strptime(fecha, '%m/%d')
    mes=numToMon(fecha.month)
    if num_trans_mon.get(mes):
        trans_total=num_trans_mon.get(mes)
        trans_total+=1
        num_trans_mon.update({mes:trans_total})
    else:
        num_trans_mon.update({mes:1})

#Calculo del promedio de debito y credito
debit=df['Transactions'].where(df['Transactions']<0).fillna(0)
debit=[ x for x in debit if x!=0 ]
average_debit=sum(debit)/len(debit)
credit=df['Transactions'].where(df['Transactions']>=0).fillna(0)
credit=[ x for x in credit if x!=0 ]
average_credit=sum(credit)/len(credit)

#Impresion de resultado
num_trans_string=''
print(f'El balance total es {total_balance}')
for month in num_trans_mon.keys():
    num_trans_string+=f'Numero de transacciones en {month}: {num_trans_mon.get(month)}, '
print(num_trans_string)
print(f'Importe promedio de debito {average_debit}')
print(f'Importe promedio de credito {average_credit}')

#Creacion del correo a enviar
message=f'El balance total es {total_balance}. {num_trans_string}. Importe promedio de debito {average_debit}. Importe promedio de credito {average_credit}'
mimeMessage = MIMEMultipart()
mimeMessage["to"] = 'juansicloud@gmail.com'
mimeMessage["subject"] = "Resumen de tus transacciones"
mimeMessage.attach(MIMEText(message, "plain"))
file = open("storiLogo.jpg", "rb")
attach_image = MIMEImage(file.read())
attach_image.add_header('Content-Disposition', 'attachment; filename = "Logo"')
mimeMessage.attach(attach_image)
raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()

#Validacion de tabla e inserción a base de datos
if os.environ.get('MYSQL_DATABASE'):
    bd=os.environ.get('MYSQL_DATABASE')
    print(os.environ.get('MYSQL_HOST'), os.environ.get('MYSQL_USER'), os.environ.get('MYSQL_PASSWORD'), os.environ.get('MYSQL_DATABASE'))
    miConexion = MySQLdb.connect(host=os.environ.get('MYSQL_HOST'), user=os.environ.get('MYSQL_USER'), passwd=os.environ.get('MYSQL_PASSWORD'), db=os.environ.get('MYSQL_DATABASE'))
    cur = miConexion.cursor()
    cur.execute(f'CREATE TABLE IF NOT EXISTS {bd}.transactions(Id INT AUTO_INCREMENT PRIMARY KEY,Date DATETIME NOT NULL,Transactions VARCHAR(255) NOT NULL);')
    valores=[]
    for i in df.index:
        fecha=datetime.strptime(df["Date"][i], '%m/%d')
        valores.append((fecha, df["Transactions"][i]))
    print(valores)
    string_query="""INSERT INTO transactions (Date, Transactions) VALUES (%s, %s);"""
    cur.executemany(string_query, valores)
    miConexion.commit()
    miConexion.close()
    print('Almacenado en BBDD...')

print("Proceso finalizado")