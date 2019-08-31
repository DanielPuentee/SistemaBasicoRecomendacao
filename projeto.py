from recomendacoes import baseDadosUsuarios, baseDadosFilmes
from math import sqrt
import os

def euclidiana(baseDados, usuario1, usuario2):
    # essa função calcula a similaridade através da distância euclidiana entre dois usuários
    si = {}
    
    # verificando os filmes em comum
    for item in baseDados[usuario1]:
        if item in baseDados[usuario2]:
            si[item] = 1
    # caso não tenham filmes em comum, retorne 0        
    if len(si) == 0:
        return 0

    # calculando a distania euclidiana entre os usuarios
    soma = sum([pow(baseDados[usuario1][item] - baseDados[usuario2][item], 2)   
                for item in baseDados[usuario1] if item in baseDados[usuario2]])

    # retornando a distancia euclidiana em porcentagem
    return 1/(1 + sqrt(soma))

def getSimilares(baseDados, usuario):
    # essa função calcula a similaridade entre um usuário e outros presentes no banco de dados

    # calculamos a distancia euclidiana entre o usuario e os outros e guardamos em um vetor
    similaridade = [(euclidiana(baseDados, usuario, outro), outro)
                    for outro in baseDados if outro != usuario]
    
    # ordenamos os resultados em forma crescente
    similaridade.sort()

    # ordenamos os resultados em forma decrescente
    similaridade.reverse()

    # retornamos os resultados
    return similaridade[0:30]
    
def getRecomendacoes(baseDados, usuario):
    # essa função fornece as indicações para filmes não vistos pelo usuário e sim pelos outros
    
    # totais é o resultado da similaridade em relação ao outro x a nota que o outro deu
    totais = {}

    # somaSimilaridade é a soma da similaridade de todos os outros usuarios que viram o filme
    somaSimilaridade = {}

    # percorre os usuarios
    for outro in baseDados:
        # caso outro igual ao usuario que estamos analisando pule o for
        if outro == usuario: continue
        
        # chamando a função similaridade
        similaridade = euclidiana(baseDados, usuario,outro)

        # caso retorno seja 0, ou seja, não há similaridade pule o for
        if similaridade <= 0: continue
        
        # calculamos os totais e soma para cada filme
        for item in baseDados[outro]:
            if item not in baseDados[usuario]:
                totais.setdefault(item, 0)
                totais[item] += baseDados[outro][item] * similaridade
                somaSimilaridade.setdefault(item, 0)
                somaSimilaridade[item] += similaridade

    # Retorna o calculo final
    rankings = [(total / somaSimilaridade[item], item) for item, total in totais.items()]

    rankings.sort()

    rankings.reverse()

    return rankings[0:30]

def carregaBaseDadosMovieLens():
    #Nessa função lemos os dados presentes no banco de dados de filmes e de avaliadores

    filmes = {}
    for linha in open('u.item'):
        (id, titulo) = linha.split('|')[0:2]
        filmes[id] = titulo

    base = {}
    for linha in open('u.data'):
        (usuario, idfilme,nota,tempo) = linha.split('\t')
        base.setdefault(usuario, {})
        base[usuario][filmes[idfilme]] = float(nota)
    return base

base = carregaBaseDadosMovieLens()

print(getRecomendacoes(base, '1'))