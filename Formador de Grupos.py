import pandas as pd
import sys

def distribuir(alunos, ordem=1):
    global estudantes
    estudantes = []

    #Pega os alunos da 3 serie
    dist(alunos, '3ª série')

    #Pega os alunos da 2 serie
    dist(alunos, '2ª série')

    #Pega os alunos da 1 serie
    dist(alunos, '1ª série')

    #Balencamento
    if ordem == -1: estudantes = list(reversed(estudantes))

    global g

    #Distribui os estudantes entre os grupos
    while len(estudantes) != 0:
        grupos[g].append((estudantes[0])) #Adiciona ao determinado grupo o nome do aluno e sua turma

        g += 1 #Cicla o grupo
        if g >= 10: g = 0
        estudantes.pop(0) #Remove o estudante adicionado  

def dist(alunos, serie):
    #Pega os alunos de determinada serie
    global estudantes
    nomes = []; series = []; areas = []

    a_nome = alunos.loc[alunos['Série'] == serie]['Nome completo sem abreviação']
    a_serie = alunos.loc[alunos['Série'] == serie]['Série']
    a_area = alunos.loc[alunos['Série'] == serie]['Área de conhecimento de maior afinidade']
    for n in a_nome: nomes.append(n)
    for s in a_serie: series.append(s)
    for a in a_area: areas.append(a)

    for pos, ser in enumerate(series): nomes.insert(2*pos + 1, ser)

    for pos, are in enumerate(areas):
        if are == 'Ciências da Natureza': A = 'CN'
        elif are == 'Matemática': A = 'MT'
        elif are == 'Linguagens e Códigos': A = 'LC'
        elif are == 'Ciências Humanas': A = 'CH'
        nomes.insert(3*pos + 2, A)

    while len(nomes) != 0:
        estudantes.append((nomes[0], nomes[1], nomes[2]))
        for contador in range(3): nomes.pop(0)


#Cria os grupos vazios
grupos = [[], [], [], [], [], [], [], [], [], []]

global g
g = 0

#Importa a tabela excel
try: dados_df = pd.read_excel(r"Equipes Aulão Enem.xlsx")
except: input('\nArquivo "Equipes Aulão Enem" não encontrado.\n\n\nPressione "Enter" para fechar.\n')

#Ciências da Natureza
CN = dados_df.loc[dados_df['Área de conhecimento de maior afinidade'] == 'Ciências da Natureza']
distribuir(CN)

#Matemática
M = dados_df.loc[dados_df['Área de conhecimento de maior afinidade'] == 'Matemática']
distribuir(M, -1)

#Ciências Humanas e Linguagens e Códigos
HL = dados_df.loc[(dados_df['Área de conhecimento de maior afinidade'] == 'Ciências Humanas') | (dados_df['Área de conhecimento de maior afinidade'] == 'Linguagens e Códigos')]
distribuir(HL)

#Organiza (3 -> 1)
for n, g in enumerate(grupos):
    grup = []
    for serie in range(3):
        for a in g:
            if a[1] == f'{3-serie}ª série':
                grup.append(a)

    grupos[n] = grup

#Nomes dos grupos
paises = ['Japão', 'Brasil', 'África do Sul', 'Alemanha', 'Austrália', 'Egito', 'Nova Zelândia', 'Grã-Bretanha', 'China', 'Estados Unidos']

#Salva os grupos
sys.stdout = open("Grupos.txt", "w")

for g, grupo in enumerate(grupos):
    print(f'{paises[g]}: ({len(grupo)})')

    for nome, turma, area in grupo:
        print(f'({turma}) {nome} - {area}')
    print('\n')

sys.stdout.close()
