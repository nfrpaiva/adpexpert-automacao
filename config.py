import sys
import os
import getopt
from dotenv import load_dotenv

load_dotenv()

adp_username = os.getenv('ADP_USER')
adp_password = os.getenv('ADP_PASSWORD')

url = os.getenv("URL")

db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_database = os.getenv('DB_DATABASE')

read_only = False
unattended = False

try:
    opts, args = getopt.getopt(sys.argv[1:], "ru")
except getopt.GetoptError as err:
    print(err)
    sys.exit(2)

for o, a in opts:
    if o == '-r':
        read_only = True
        print("Trabalhando em modo somente leitura")
    if o == '-u':
        unattended = True
        print("Trabalhando em modo automático de aprovação")
