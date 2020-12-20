import sys, getopt

read_only = False
unattended =  False

try:
    opts, args = getopt.getopt(sys.argv[1:], "ru")
except getopt.GetoptError as err:
    print(err)
    sys.exit(2)

for o, a in opts:
    if o == '-r':
        read_only  = True
        print("Trabalhando em modo somente leitura")
    if o == '-u':
        unattended = True
        print("Trabalhando em modo automático de aprovação")

