# Rio Jequitinhonha: Variações dos Aspectos Naturais e de Usos Humanos

Este repositório é um auxílio ao uso da ferramenta criada para o estudo de dados sobre os atributos do Rio Jequitinhonha providos pela Agência Nacional de Águas.

A ferramenta faz parte do Trabalho de Conclusão de Curso intitulado 'Rio Jequitinhonha Variações dos Aspectos Naturais e de Usos Humanos' e foi projetada para tornar mais simples a análise gráfica e numérica dos dados da ANA.

É escrita na linguagem de programação python e utiliza as bibliotecas pandas, matplotlib, seaborn e os distribuídas pela plataforma Anaconda 3, compiladas no IDE Spyder (python 3.7.3).

> Este é um exemplo de gráfico de linhas criado com a função systemLineplot. Ela mostra valores dos arquivos encontrados do caminho 'cotas', utilizando o atributo 'Media' no eixo y. Nesse caso mostra apenas valores entre 0 e 1000, entre os anos de 1950 e 1990.

```
systemLineplot(cotas, 'Media', 0, 1000, '1950', '1990')
```

![githubexample](https://user-images.githubusercontent.com/52804741/66139985-b80b7a00-e5d7-11e9-9d6f-73edce052e3f.png)

> O Caminho e o atributo são parâmetros obrigatóŕios, enquanto que os valores máximo e minimo bem como o intervalo de anos são opcionais com o padrão 'False'. A sintaxe da função é:

```
systemLineplot(caminho, variável, minimo, máximo, ano de início, ano final)
```
> Se desejar usar apenas um dos atributos deve definir os precedentes como falsos e respeitar sua ordem. A função a seguir por exemplo, mostra todos os registros no caminhos 'cotas' até o ano de 1980 (já que os valores maximo e mínimo, bem como ano de início foram definidos como 'False').

```
systemLineplot(cotas, 'Media', False, False, False, '1980')
```

![githubexample2](https://user-images.githubusercontent.com/52804741/66140889-446a6c80-e5d9-11e9-9dcf-8cee5e1ad893.png)

> Foi implementada também com a mesma sintaxe a função systemBoxplot, que no exemplo a seguir plota valores entre 0 e 500, entre os anos de 1950 e 2010.

```
systemBoxplot(cotas, 'Media' , 0 , 500, '1950', '2010')
```

![githubexample3](https://user-images.githubusercontent.com/52804741/66141589-4680fb00-e5da-11e9-852e-05e4cc3f7958.png)

> Nesse caso a função utiliza o código das estações no eixo horizontal e utiliza as datas das coletas dos dados para fazer a análise estatística (média e quartis).
