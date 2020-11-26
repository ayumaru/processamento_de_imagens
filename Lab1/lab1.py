import numpy as np 
import math
import cv2
import sys
from scipy import stats

def moda(val):
    a = stats.mode(val) #pega a moda do vetor
    return np.uint8(a[0])

def mediana(val):    
    if len(val)%2 == 0: #eh par, entao pega os 2 elementos centrais, soma e divide por 2
        b = int(len(val)/2)
        a = np.uint8( ( int(val[b-1])+int(val[b]))/2 )
    elif len(val)%2 == 1: #eh impar
        a = math.floor(np.uint8(len(val)/2))
        a = val[a] #pega o elemento na posicao de a
    return np.uint8(a)


def media(val):
    a = np.median(val)
    return np.uint8(a) 



def carregar_img():
    img = cv2.imread(sys.argv[1],0)
    largura,altura = img.shape
    return img,largura,altura



def quantizacao(img, j_val_anterior,  j_val_prox, i_val_anterior, i_val_prox, tecnica):
    i_dim = abs(i_val_prox - i_val_anterior) 
    j_dim = abs(j_val_prox - j_val_anterior )
    cores = np.zeros( [i_dim*j_dim ], dtype=np.uint8)
    n = 0
    for ii in range(i_val_anterior, i_val_prox):
        for jj in range(j_val_anterior, j_val_prox):
            cores[n] = img[ii][jj]
            n+=1
    
    if tecnica == "media":
        return  media(cores)
    elif tecnica == "mediana":
       return mediana( np.sort(cores) ) #envia o vetor ja ordenado
    elif tecnica == "moda":
       return moda(cores)    
    

def reducao(img, esc_l, esc_a, na, nl, res_img, tecnica, lar, alt):
    
    parar = 0
    i_val_prox = 0
    i_val_anterior=0
    for i in range(nl-1): 
        
        if ( (1+int((i-1)/esc_l) ) > 1 ):
            i_val_anterior = int(((1+i/esc_l) - (1+(i-1)/esc_l))/2 )
            i_val_anterior = 1+int(i/esc_l) - i_val_anterior
        if ( (1+int( (i+1)/esc_l)) < lar):
            i_val_prox = math.ceil(((1+ (i+1)/esc_l ) - (1 + i/esc_l))/2 )
            i_val_prox += 1+int(i/esc_l)
        else:
            i_val_prox = lar        

        j_val_prox = 0
        j_val_anterior = 0    
        
        for j in range(na-1): 
            
            if ( (1+int((j-1)/esc_a) ) > 1 ):
                
                j_val_anterior = int(((1 + j/esc_a) - ( 1+ (j-1)/esc_a))/2 )
                j_val_anterior = 1+int(j/esc_a) - j_val_anterior   
            if ( (1+ int((j+1)/esc_a)) < alt):
                
                j_val_prox = math.ceil(((1+ (j+1)/esc_a ) - (1 + j/esc_a))/2 )
                j_val_prox += 1+int(j/esc_a) 
            else:
                j_val_prox = alt
            a = quantizacao(img, j_val_anterior,  j_val_prox, i_val_anterior, i_val_prox, tecnica)
            res_img[i+1, j+1] = a

    #arrumar a borda da direita e superior que não possuem pixels, copiando os vizinhos do lado. Aplicar quantizacao talvez?
    for i in range(0,nl):
        res_img[i][0] = res_img[i][1]
    for j in range(0,na):
        res_img[0][j] = res_img[1][j]

    return res_img

def main():
    t_reducao = float(sys.argv[2])
    tecnica = sys.argv[3]
    img, lar, alt = carregar_img() 

    na = int(alt*(t_reducao/100)) #dimensoes de saida para imagem nova 
    nl = int(lar*(t_reducao/100))
    esc_a = na/(alt-1) #nova escala de imagem
    esc_l = nl/(lar-1) 

 
    
    res_img = np.ones( (nl, na, 1), np.uint8) # matriz resultante    
    
    res_img = reducao(img, esc_l, esc_a, na, nl, res_img, tecnica, lar, alt)# reducao, quantizacao
    cv2.imwrite('./resultado_'+tecnica+'_'+str(t_reducao)+'.png', res_img)

if __name__ == "__main__":
    main()
