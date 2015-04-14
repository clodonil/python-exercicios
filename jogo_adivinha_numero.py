'''
  O Jogo consiste em sorteador 2 numeros, um para cada jogador. Os jogadores tem 3 tentativas
   de acertar e quem acertar primeiro leva ou quem chegar mais perto do numero sorteado.
'''
   

import random


# Controle do while
controle=1

# Lista para guardar quem chegou mais perto
dif_jogador1=[]
dif_jogador2=[]

# garda o ganhador do jogo
ganhador=0

#lista com os jogadores e numero sorteado
jogador={}


# Le o nome dos 2 jogadores e sortea os numeros
jogador[raw_input("Digite o nome do 1 Jogador:")]=random.randrange(0,50)
jogador[raw_input("Digite o nome do 2 Jogador:")]=random.randrange(0,50)


#quem comeca primeiro?
quem_joga_primeiro = random.choice(jogador.keys())
quem_joga_segundo  = list((set(jogador.keys())-set([quem_joga_primeiro])))[0]

while controle < 4:

    # Jogada do jogador 1	
    jogada_1 = int(raw_input("JOGADA %d DO JOGADOR %s:" %(controle,quem_joga_primeiro)))

    # Verifica se a ganhador
    if jogador[quem_joga_primeiro] == jogada_1:
        ganhador = 	quem_joga_primeiro
        break	
    elif jogador[quem_joga_primeiro] > jogada_1:
        print "O Numero eh maior"	
    elif jogador[quem_joga_primeiro] < jogada_1:
        print "O Numero eh menor"

    # Guarda a distancia do numero sorteado    
    dif_jogador1.append(abs(jogador[quem_joga_primeiro] - jogada_1))

    # Jogada do jogador 2
    jogada_2 = int(raw_input("JOGADA %d DO JOGADOR %s:" %(controle,quem_joga_segundo)))

    # Verifica se a ganhador
    if jogador[quem_joga_segundo] == jogada_2:
       ganhador = quem_joga_segundo
       break
    elif jogador[quem_joga_segundo] > jogada_2:
       print "O Numero eh maior"	
    elif jogador[quem_joga_segundo] < jogada_2:
       print "O Numero eh menor"	
    # Guarda a distancia do numero sorteado      
    dif_jogador2.append(abs(jogador[quem_joga_segundo] - jogada_2))
       

    # Controle das jogadas
    controle += 1

# Verifica se ha ganhador
if ganhador != 0:
    print "O Vencedor eh %s" %(ganhador)
else:
	 # Verifica quem chegou mais perto
	 dif_jogador1.sort()
	 dif_jogador2.sort()

	 if dif_jogador1[0] < dif_jogador2[0]:
	 	print "O Vencedor eh %s,  sorteado: %d"	%(quem_joga_primeiro, jogador[quem_joga_primeiro])
	 elif dif_jogador2[0] < dif_jogador1[0]:
	 	print "O Vencedor eh %s,  sorteado: %d"	%(quem_joga_segundo, jogador[quem_joga_segundo])
	 else:
	    print "Empate...."	


raw_input("Pressione Enter")