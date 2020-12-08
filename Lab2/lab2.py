import cv2
import numpy as np
import argparse
from matplotlib import pyplot as plt
import glob


###
# Maior valor indica maior similaridade ( Correlacao e Interseccao)
# Menor valor indica maior similaridade ( Chi-Squared e Hellinger== Bhattacharyya )
###


def pegar_imagens(argm, hists, nome_img): # carrega todas as imagens de um formato presentes no diretorio e gera o histograma delas
    
    for imagem in glob.glob( argm["diretorio"] + "/*." + argm["formato"] ):
        nome = imagem[imagem.rfind("/")+1:]
        img = cv2.imread(imagem)
        nome_img[nome] = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # nome_img[nome] = img
        hist = cv2.calcHist( [img], [0,1,2], None, [256,256,256], [0,256,0,256,0,256])
        hist = cv2.normalize(hist, hist).flatten()
        hists[nome] = hist



def comparador(atual, hists, nome_img, metodos, acuracia, resultado_por_imagem):
    
    for ( nome_metodo, codigo_metodo ) in metodos: # nome no dicionario e o valor int correspondente no opencv do metodo
            descendente = False
            resultado = []

            for (k, hist) in hists.items():
                d = cv2.compareHist(hists[atual], hist, codigo_metodo)
                resultado.append( (d,k) )  
            
            if nome_metodo in ("Corelacao", "Intersecao"):
                descendente = True

            resultado = sorted( resultado, reverse= descendente )
            resultado_por_imagem[atual] = resultado
            
            if resultado[0][1][:-5] == resultado[1][1][:-5]:
                acuracia[nome_metodo] += 1


def main():

    flags = argparse.ArgumentParser()
    flags.add_argument("-d", "--diretorio", required=True, help= "Caminho para o diretorio das imagens")
    flags.add_argument("-f", "--formato", required=True, help=" Formato da imagem (png ou jpeg")
    argm = vars(flags.parse_args())
    
    hists = {}
    nome_img = {}
    pegar_imagens(argm, hists, nome_img)
    resultado_por_imagem = {}

    metodos = ( ("Corelacao", cv2.HISTCMP_CORREL), ("Chi-quadrado", cv2.HISTCMP_CHISQR), ("Intersecao", cv2.HISTCMP_INTERSECT), ( "Hellinger ( Bhattacharrya)", cv2.HISTCMP_BHATTACHARYYA)) 
    acuracia = { "Corelacao": 0, "Chi-quadrado": 0, "Intersecao": 0, "Hellinger ( Bhattacharrya)": 0 }
    comparados = 0
    
    for atual in nome_img:
        comparador(atual, hists, nome_img, metodos, acuracia, resultado_por_imagem)
        comparados+=1

    # print("\n resultado por imagem: \n", resultado_por_imagem)
    # for i in resultado_por_imagem:
    #     print("i: ", i, resultado_por_imagem[i])
    
    for j in acuracia:
        acuracia[j] =  round(  (acuracia[j]/comparados)*100, 5) 

    print("\n Imagens comparadas : ", comparados)
    print("\n Acuracia dos metodos: \n", acuracia)
    

if __name__ == '__main__':
    main()
