i = 0
file = open('setores.txt').read()
line = file.split('Bairros:')
totalBairros = 0
totalRegioes = len(line)
for i in range(1,totalRegioes):
	print("*************************************************")
	linha = line[i].split(',')
	print('Região',i,"Qtde de bairros =",len(linha))
	totalBairros += len(linha)
	for x in range(len(linha)):
		print("Bairros:",x+1,linha[x].lstrip())
print("Total de Regiões:",totalRegioes,"\nTotal de Bairros:",totalBairros)
