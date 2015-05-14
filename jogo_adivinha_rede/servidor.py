import socket
import thread
import random
import time
import sys


class Jogar():    
    # Class do Jogo
    def __init__(self,num_max=50):
         self.num_max = num_max            
         self.semafaro=0
         self.jogadores = {}
         self.jogadas = {}
         self.filewrite()

    def  sorteia(self):
        return random.randrange(0,self.num_max)

    def fileread(self):                
        while True:           
           if self.semafaro == 0:
                self.jogadores={}
                self.jogadas={}    
                self.semafaro = 1
                try:
                    fconfig = open("jogo.config")
                    for linha in fconfig.readlines():                      
                        linha = linha.replace(' ','')
                        if len(linha) != 1:
                           (index,valor) = linha.split(":")
                           valor = valor.replace('\n','')                           
                           if index in self.jogadores:
                               self.jogadas[index] = valor
                           else: 
                               self.jogadores[index]=valor

                    fconfig.close()     
                except:
                    print("Nao foi possivel abrir o arquivo de configuracao")
                    sys.exit(1)                        
                self.semafaro = 0
                break
        
        
    def filewrite(self):        
        while True:
            if self.semafaro == 0:
                self.semafaro = 1
                try:
                    fconfig = open("jogo.config","w")
                    for linha in self.jogadores.keys():
                       params = "%s:%s\n" %(linha,self.jogadores[linha])                
                       fconfig.write(params)

                    for linha in self.jogadas.keys():
                      params = "%s:%s\n" %(linha,self.jogadas[linha])                
                      fconfig.write(params)
                    fconfig.close()
                except:
                    print("Nao foi possivel abrir o arquivo de configuracao")
                    sys.exit(1)
                self.semafaro = 0
                break          


    def num_jogador(self):
        self.fileread()        
        return len(self.jogadores)   

    def  add_jogador(self,nome,num):
        self.fileread()
        if not nome in self.jogadores:
            self.jogadores[nome] = 0
        else:
            self.jogadores[nome] = num                   
        self.filewrite()

    def vencedor(self):
        # Verifica se existe vencedor no jogo        
        vencedor_temp={}
        nome=""
        

        # Lei os dados gravados no banco
        self.fileread()

        # verifica se alguem acertou e qual rodada
        # varre as todas as jogas
        for jogador in self.jogadas.keys():
            # se o numero sorteado foi jogado
            temp = self.jogadas[jogador].split("+")            
            if self.jogadores[jogador] in temp:
                vencedor_temp[jogador] = temp.index(self.jogadores[jogador])

        
        if vencedor_temp:            
           nome=min(vencedor_temp.iterkeys(), key=lambda k: vencedor_temp[k])
           

        # ninguem acertou, verificar quem chegou mais perto
        if not nome:            
            for jogador in self.jogadas.keys():                
                temp = self.jogadas[jogador].split("+")                
                temp.remove('-1')                
                # transforma os valores para inteiro
                temp = [int(i) for i in temp]
                temp.sort()                
                
                menor= max(temp) + 10
                for item in temp:
                    if abs(item - int(self.jogadores[jogador])) <  menor:
                       menor = abs(item - int(self.jogadores[jogador]))
                
                vencedor_temp[jogador] = menor
            
            nome=min(vencedor_temp.iterkeys(), key=lambda k: vencedor_temp[k])                
            
        return nome        

    def gravar_jogada(self,nome,jogada):
        self.fileread()
        if not nome in self.jogadas:
            self.jogadas[nome] = jogada
        else:
            self.jogadas[nome] = self.jogadas[nome] + '+' + jogada                         
        self.filewrite()
        


    def fim_das_jogadas(self):
         self.fileread()
         finalizou=0
         for jogador in self.jogadas.keys():
             if "-1" in self.jogadas[jogador]:
                finalizou = finalizou + 1         
         return ( True if (finalizou > 1) else False)

    def verifica(self,nome,num):
        result=0
        if int(self.jogadores[nome]) > int(num):
            result = "maior"
        elif int(self.jogadores[nome]) < int(num):
            result = "menor"
        else:
            result = "acertou"        
        return result

    def run(self,cliente_socket,addr):
    
        # Recebe o nome do jogador                
        nome_jogador = cliente_socket.recv(1024)        

        # adiciona o jogador no banco de dados
        self.add_jogador(nome_jogador,0)

                # aguarda os outros jogadores
        while self.num_jogador() < 2:
            time.sleep(2)
            
                    
        # Sorteia os numeros     
        sorteado = str(self.sorteia())
        

        # Envia o numero pela rede
        cliente_socket.send("OK")
        
        # Adiciona o numero no banco de dados
        self.add_jogador(nome_jogador,sorteado)

        jogada = ""
        tentativas = 0
        while True:
            # recebe a jogada
            num = cliente_socket.recv(1024)
            
            # verifica se maior, menor ou vencedor            
            ganhador = self.verifica(nome_jogador,num)

            #grava a jogada                  
            self.gravar_jogada(nome_jogador,num)

            # Verifica se o numero de jogas acabou o seu acertou
            if tentativas == 2 or ganhador == 'acertou':
                cliente_socket.send(ganhador+":"+"-1")
                self.gravar_jogada(nome_jogador,"-1")
                break                          
            else:
                cliente_socket.send(ganhador+":"+str(tentativas))    
            
            tentativas = tentativas +  1    
        
        # aguardando os jogos
        time.sleep(3)
        while not self.fim_das_jogadas():
            time.sleep(5)


        # verifica se existe vencedor
        vencedor=self.vencedor()
        cliente_socket.send(vencedor+":"+str(self.jogadores[nome_jogador]))
        cliente_socket.close()
 
        time.sleep(3)        

        # finalizando o jogo
        # limpa os nomes dos jogadores
        self.jogadores={}
        self.jogadas={}
        # grava no banco de dados
        self.filewrite()     


if __name__=='__main__':
   porta = int(sys.argv[1])
   sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   sock.bind(('localhost',porta))
   sock.listen(5)

   novo_jogo = Jogar(50)
   while True:                             
        cliente_socket,addr = sock.accept()
        thread.start_new_thread(novo_jogo.run,(cliente_socket,addr))
       


