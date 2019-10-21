# Rio Jequitinhonha: Variações dos Aspectos Naturais e de Usos Humanos

Este repositório é um auxílio ao uso da ferramenta batizada de 'ANAbranch' criada para o estudo de dados sobre os atributos do Rio Jequitinhonha providos pela ANA. 'Anabranching' é um tipo de canal que se desassocia do canal principal e o encontra novamente em outro ponto do rio. ANA é a agência nacional de águas.

A ferramenta faz parte do Trabalho de Conclusão de Curso intitulado 'Rio Jequitinhonha Variações dos Aspectos Naturais e de Usos Humanos' entregue ao Instituto do Mar da UNIFESP como pré-requisito para graduação e foi projetada para tornar mais simples a análise gráfica e numérica dos dados da ANA.

É escrita na linguagem de programação python e utiliza as bibliotecas os, pandas e seaborn distribuídas pela plataforma Anaconda 3, compiladas no IDE Spyder (python 3.7.3).

```
arquivo = 'c:\\Users\\User\\Downloads\\Dados\\arquivo.csv''
data = stationData(arquivo)
```

O exemplo de código acima lê os dados de um arquivo csv retirado da ANA e o transforma em um pandas.DataFrame

![Captura de tela de 2019-10-20 23-34-21](https://user-images.githubusercontent.com/52804741/67172566-36b33600-f392-11e9-9eab-efd94a188917.png)

Podemos agora utilizar funções da biblioteca anabranch para transformar os dados em uma série temporal e plotá-los.

```
import anabranch as ab
data = ab.stationData(sample) # na forma de dataframe
data = ab.dailyOccurences(data) # apenas as ocorrencias diárias
data = ab.dailySeries(data) # no formato de série temporal
data = ab.datetimeSorted(data) # em ordem cronológica
data = ab.targetVar(data,'value') # apenas a variável alvo
```

Todas as funções acima estão disponíveis em anabranch e trabalham com o dataframe da forma indicada. Mais alguns tratamentos permitem que os dados sejam graficados:

```
data = data[data['Data'] > '1975'] # entre 1975
data = data.set_index('Data') # usando as satas como índice
data = data['value'].resample('MS').mean() # média mensal
data.dropna(inplace=True) # excluindo ocorrências nulas
data.plot(figsize=(15, 6)) # figura de 15'' por 6''
plt.show(sns) # gráfico usando seaborn
```
Finalmente:

![estocasticmean](https://user-images.githubusercontent.com/52804741/67172410-9eb54c80-f391-11e9-99bb-f183e364f913.png)

> Abaixo vemos o exemplo de gráfico de linhas criado com a função ab.systemLineplot. Ela mostra valores dos arquivos encontrados do caminho 'cotas', utilizando o atributo 'Media' no eixo y. Nesse caso mostra apenas valores entre 0 e 1000, entre os anos de 1950 e 1990.

```
cotas = 'c:\\Users\\User\\Downloads\\Dados\\cotas'
ab.systemLineplot(cotas, 'Media', '1950', '1990', 0, 1000)
```

![githubexample](https://user-images.githubusercontent.com/52804741/66139985-b80b7a00-e5d7-11e9-9d6f-73edce052e3f.png)

> O Caminho e o atributo são parâmetros obrigatóŕios, enquanto que os valores máximo e minimo bem como o intervalo de anos são opcionais com o padrão 'False'. A sintaxe da função é:

```
ab.systemLineplot(caminho, variável, ano de início, ano final, minimo, máximo)
```
> Se desejar usar apenas um dos atributos deve definir os precedentes como falsos e respeitar sua ordem. A função a seguir por exemplo, mostra todos os registros no caminhos 'cotas' até o ano de 1980 (já que os valores maximo e mínimo, bem como ano de início foram definidos como 'False').

```
ab.systemLineplot(cotas, 'Media', False, '1980')
```

![githubexample2](https://user-images.githubusercontent.com/52804741/66140889-446a6c80-e5d9-11e9-9dcf-8cee5e1ad893.png)
