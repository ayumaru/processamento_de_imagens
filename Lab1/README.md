# Problema proposto
Implemente um programa que realize a redução da amostragem em uma imagem monocromática. O programa deve receber como parâmetros o nome da imagem, o percentual de redução e a técnica de quantização (média, mediana ou moda.) A saída do programa deve ser a imagem reamostrada. Utilize a imagem exemplo.png para testar o programa.


# Lab1 - Execução
O código deve ser rodado da seguinte forma:
> $> python3 lab1.py  **nome_da_imagem**  **proporção_de_saida**  **nome_da_tecnica**

As técnicas a serem passadas são escritas da seguinte forma: **media**, **mediana** , **moda**

exemplo:
> $> python3 lab1.py  **exemplo.png**  **90**  **media**

Nesse caso a imagem resultante vai possuir 90% do tamanho original.

# Bibliotecas utilizadas

- Numpy
	- Para utilização de arrays de forma mais eficiente.
- Math
	- Para utilização das funções de teto e chão. (math.ceil, math.floor)
- Opencv (cv2)
	- Para abrir a imagem e salvar a imagem resultante.
- Sys
	- Para poder pegar os argumentos passados via linha de execução pelo argv.
- Scipy 
	- Para poder utilizar a função pronta para calcular a moda de um vetor.

