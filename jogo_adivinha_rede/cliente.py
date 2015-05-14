import socket
import sys

porta = int(sys.argv[1])

pacote=""
tentativas = ""

#inicia o socket
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect(("localhost", porta))

# Digita o nome
nome = raw_input("Digite o seu nome:")
cliente.send(nome)

# Aguarda o "OK" pra comecar a jogar
print "Aguardando Jogadores"
pacote = cliente.recv(1024)

print "====| comecou o jogo  |====="
while pacote != "acertou" and tentativas != '-1':
    num = raw_input("Digite o numero sorteado:")
    cliente.send(num)
    recebido = cliente.recv(1024)
    (pacote,tentativas) = recebido.split(":")
    print pacote

print "aguardando apuracao..."
resultado = cliente.recv(1024).split(":")
print "Vencedor foi %s. O seu numero sorteado %s" %(resultado[0],resultado[1])  

cliente.close()
raw_input("FIM DO JOGO")
