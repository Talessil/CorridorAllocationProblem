#!/usr/bin/python

from gurobipy import *
import random
from random import shuffle
from collections import defaultdict
import time


#FUNCAO GERADORA DE INSTANCIAS - GERA 2 ARQUIVOS, UM CONTENDO TAMANHO DE CADA SALA, OUTRO CONTENDO A RELACAO DE TRAFEGO ENTRE SALAS
def gera_instancia(tam,val):
	
	f= open("tamanho.txt","w+")
	for i in range(tam):
    		f.write("%d\n" %random.randint(2,15))
	f.close() 

	g= open("trafego.txt","w+")
	for i in range(val):
    		g.write("%d\n" %random.randint(5,21))
	g.close() 

	return 0
	
#FUNCAO QUE CALCULA POSICAO DE CADA PORTA DAS ALOCACOES EXISTENTES
def calcula_posicao_porta(alocs,tamanho):

	new_dict = nested_dict(2, float)
	
	#--------------- CALCULAR A POSICAO DA PORTA DE CADA ALOCACAO ------------------#
	
		#define posicoes das portas de aloc1
	for j in range(len(alocs)):
		soma = 0
		k = 0
		aux = alocs[j]
		for i in range(len(aux)): #range(len(aux))*****
			new_dict[j,aux[i]] = float(soma) + float(tamanho[aux[i]])/2
			soma += float(tamanho[aux[i]])


	return new_dict

#FUNCAO DICTIONARY (COMO SE FOSSE UMA MATRIZ)
def nested_dict(n, type):
    if n == 1:
        return defaultdict(type)
    else:
        return defaultdict(lambda: nested_dict(n-1, type))
			

#CONSTRUTIVO, CADA VEZ QUE EH CHAMADO GERA 100 ALOCACOES
def construtivo(tam,mat,tamanho,aloc_qnt):

	#--------------- DECLARACAO DE VARIAVEIS ------------------#

		#controle de salas alocadas e inicializacao com valor 0
	alocados = [] 
	for i in range(tam):
 		alocados.append(0)
	
	aloc1 = []   #alocacao 1 (fila 1)
	aloc2 = []   #alocacao 2 (fila 2)

		#controle de indice das alocacoes
	indice1 = 0
        indice2 = 0 	
		#soma dos tamanhos das alocacoes
	soma1 = 0
	soma2 = 0

	#joga sala 0 para alocacao 1, sala 1 para alocacao 2
	val = (int)(random.random() * tam-1)
	val2 = (int)(random.random() * tam-1)
	while(val == val2):
		val2 = (int)(random.random() * tam-1)

	#print val
	#print val2
	aloc1.append(val)
	indice1 += 1
	alocados[val] = 1
	soma1 += tamanho[val]
	aloc2.append(val2)
	indice2 += 1	
	alocados[val2] = 1
	soma2 += tamanho[val2]
	
	#print alocados
	#--------------- CONSTRUTIVO ------------------#
	for i in range(2,tam):
		maior = 0
		if(soma1 > soma2):
			for j in range(tam):
				if mat[j,aloc2[indice2-1]] >= 0:
					if alocados[j]==0 and float( mat[j,aloc2[indice2-1]]/((tamanho[j]+tamanho[aloc2[indice2-1]])/2) ) >= maior:
						maior = float( mat[j,aloc2[indice2-1]] / ((tamanho[j]+tamanho[aloc2[indice2-1]])/2) )
						sala = j
				else: 
					if alocados[j]==0 and float( mat[aloc2[indice2-1],j]/((tamanho[j]+tamanho[aloc2[indice2-1]])/2) ) >= maior:
						maior = float( mat[aloc2[indice2-1],j] / ((tamanho[j]+tamanho[aloc2[indice2-1]])/2) )
			    			sala = j

			aloc2.append(sala)
			indice2 += 1
	   		alocados[sala] = 1
	    		soma2 += tamanho[sala]
		else:
			for j in range(tam):
				if mat[j,aloc1[indice1-1]] >= 0:
					if alocados[j]==0 and float( mat[j,aloc1[indice1-1]]/((tamanho[j]+tamanho[aloc1[indice1-1]])/2) ) >= maior:
						maior = float( mat[j,aloc1[indice1-1]] / ((tamanho[j]+tamanho[aloc1[indice1-1]])/2) )
		    				sala = j
				else:
					if alocados[j]==0 and float( mat[aloc1[indice1-1],j]/((tamanho[j]+tamanho[aloc1[indice1-1]])/2) ) >= maior:
						maior = float( mat[aloc1[indice1-1],j]/((tamanho[j]+tamanho[aloc1[indice1-1]])/2) )
		    				sala = j

			aloc1.append(sala)
			indice1 += 1
	    		alocados[sala] = 1
	    		soma1 += tamanho[sala]
				
	#print "aloc1"
	#for r in range(indice1):
	#	print aloc1[r]
	#print "aloc2"
	#for r in range(indice2):
	#	print aloc2[r]	

	#print alocados

	#----------------- GERAR VARIAS CONFIGURACOES ----------------------#	
	
	alocs = []
	i = 0
	#EMBARALHA CADA LADO SEPARADAMENTE
	while(i < aloc_qnt): #esse valor dividido por 2
		#unir as 2 primeiras alocacoes
		random.shuffle(aloc1)
		random.shuffle(aloc2)
		linha = []
		for l in range(indice1):
			linha.append(aloc1[l])
		for l in range(indice2):
			linha.append(aloc2[l])
 		if i == 0:
			alocs.append(0)
			alocs[i] = aloc1
			i+=1
		elif i == 1:
			alocs.append(0)
			alocs[i] = aloc2
			i+=1
		else:
			alocs.append(0)
			alocs[i] = []
			for j in range(indice1):
				alocs[i].append(linha[j])
			i+=1
			alocs.append(0)
			alocs[i] = []
			for k in range(j+1,tam):
				alocs[i].append(linha[k])
			i+=1

	#print alocs
	return alocs

#FUNCAO QUE GERA A SOLUCAO INICIAL DE FORMA CONSTRUTIVA
def funcao_chamadora(tam,val,alocs,n):

	#--------------- LEITURA DOS ARQUIVOS ------------------#
	
	tamanho = [] #vetor com tamanhos das salas
	trafego = [] #vetor com trafegos entre as salas

		#Leitura dos tamanhos das salas
	f=open("tamanho.txt", "r")
	f1 = f.readlines()
	for x in f1:
		tamanho.append(int(x))

		#Leitura dos trafegos entre as salas
	f=open("trafego.txt", "r")
	f2 = f.readlines()
	for x in f2:
		trafego.append(int(x))
	

	#----------------- INICIALIZA MATRIZ DE TRAFEGO ----------------------#	
	mat = {}
	k = 0
	for i in range(tam):
		for j in range(tam):
			if j>i :
				mat[i,j] = int(trafego[k])
				k+=1
			else:
				mat[i,j] = -1
	
	#----------------- CHAMA O CONSTRUTIVO 'N' VEZES ----------------------#	
	alocs = []
	for i in range(n):
		alocs = alocs + construtivo(tam,mat,tamanho,200)
	
	
	#----------------- CALCULAR POSICAO DAS PORTAS DAS ALOCACOES ----------------------#
	
	new_dict = nested_dict(2, float)
	new_dict = calcula_posicao_porta(alocs,tamanho)

	#----------------- RESOLVEDOR ----------------------# 
	resolvedor(tam,alocs,new_dict,mat)
	
	#print new_dict
	
	return 0
	

def resolvedor(tam,alocs,new_dict,mat):

	allocations = range(len(alocs))

	############################## MODEL ##################################
	#Create Empty Model
	m = Model()

	#VARIABLE - ALLOCATION
	selectedAloc = {}
	for i in allocations:
		selectedAloc[i] = m.addVar(vtype=GRB.BINARY,obj=0,name="allocation"+ str(i))

	#VARIABLE - ROOM (DOOR) POSITION (FOR EACH ROOM)
	p_room = {}
	for i in range(tam):
		p_room[i] = m.addVar(vtype=GRB.CONTINUOUS,obj=0,name="p_"+ str(i))

	#VARIABLE - ROOM DISTANCE FROM BEGGIN OF ALLOCATION (each room to another)
	dist = {}
	for i in range(tam):
		for j in range(i+1,tam):
			dist[i,j] = m.addVar(vtype=GRB.CONTINUOUS,obj=1,name="d_"+ str(i)+ str(j))

	#OBJECTIVE
	m.setObjective(quicksum(mat[i,j]*dist[i,j] for i,j in dist), GRB.MINIMIZE) 

	#CONSTRAINT 1 {set 2 to selected allocations}
	total = 0
        for i in selectedAloc:
		total+=selectedAloc[i]
	c1 = m.addConstr(total == 2)

	#CONSTRAINT 2 {Not select 2 aloc with same room i}
	c2 = {} #room_const
	for i in range(tam):
	      	soma = 0
		for j in allocations:  #para cada alocacao 'k'
			for k in alocs[j]:   #para cada sala na alocacao 'k'
				if(k==i):
					soma+=selectedAloc[j]
		c2[i] = m.addConstr(soma ==  1,"room")

	#CONSTRAINT 3
	c3 = {} 
        for i in range(tam):
		total = 0
		for j in selectedAloc:
			#total+= dist_de_i_ate_inicio_na_alocacao_j * selectedAloc[j]
			if i in alocs[j]:
				total+= new_dict[j,i] * selectedAloc[j]
		c3[i] = m.addConstr(total - p_room[i] == 0,"c3")

	#CONSTRAINT 4 and 5
        c4 = {}
        c5 = {} 
        for j in range(tam):
		for k in range(j+1,tam):
			c4[j,k] = m.addConstr(p_room[j] - p_room[k] - dist[j,k] <= 0,"distjk")
			c5[j,k] = m.addConstr(p_room[k] - p_room[j] - dist[j,k] <= 0,"distkj")


   
	m.write('trabalho.lp')

	# Optimize
	m.optimize()
	status = m.status
	if status == GRB.Status.OPTIMAL:
	    print('The optimal objective is %g' % m.objVal)
	
	# PRINT SOLUTION
	for k in range(len(alocs)): 
		if selectedAloc[k].getAttr("x") == 1:
			print alocs[k]
	


def main():	
	start = time.time()

	tam = input('Digite o numero de salas: ')
	val = ((tam*tam)-tam)/2
	aloc_qnt = input('Digite a quantidade de configuracoes desejada (o default eh 50): ')
	alocs = []
	val = funcao_chamadora(tam,val,alocs,aloc_qnt*2)

	end = time.time()
	print('tempo: %f' % (end - start))

if __name__ == "__main__":
    main()
