# Teste Dev JR Reylab

Teste para a empresa Reylab para desenvolvedor Júnior, o teste consiste em completar o desafio do site [RPAChallange](https://rpachallenge.com/), automatizando o download, preenchimento de formulário e buscando o tempo de execução.

## Tecnologias utilizadas:
* Python 3.14
* Selenium 4.38.0
* Pandas 2.3.3
* Openpyxl 3.1.5

## Setup

### Instalando o Python:
Para rodar o projeto será necessário ter o Python instalado na sua máquina. Os sistemas Linux recentes já possuem o Python instalado mas caso queira ter certeza, pode rodar o seguinte comando para verificar:
```
which python3
```
e o comando para validar a versão:
```
python3 --version
```
Caso não tenha o python instalado pode ver como instalar o Python clicando [aqui](https://www.python.org/downloads/).

### Criando o ambiente:
Utilizei o conda para lidar com o ambiente deste projeto, para instalar o conda clique [aqui](https://docs.conda.io/projects/conda/en/latest/user-guide/install/).

Após instalado utilizar o seguinte comando para criar um abiente com o Python 3.11 instalado:
``` 
conda create -n web_automation python=3.14
```

Depois rode para ativar o ambiente:
``` 
conda activate web_automation 
```

### Instalando as dependências do projeto:
O Projeto utiliza o [Selenium](https://www.selenium.dev/pt-br/documentation/), e o [Pandas](https://pandas.pydata.org/) junto do [Openpyxl](https://pypi.org/project/openpyxl/). Para instalar as dependências utilize o comando: 
```
 pip install -r requirements.txt
 ```

## Rodando o projeto

Para rodar o projeto vá até a pasta em que ele foi extraido, e na raiz rode o comando no terminal:
```
python main.py
```

## Considerações
Esse foram os dois pontos com os quais tive problema de inicío:
Encontrar os elementos corretamente e ajustar o local do download do arquivo.
para lidar com o problema dos ids, procurei no elemento algo que fosse mais legivel e encontrei o ng-reflect-name, que tem um valor mais legivel, ex: 'labelFirstName.Assim fica melhor de entender o código do que colocar os ids em uma variável de ambiente no arquivo ini ou fazer alguma outra gambiarra.
Para lidar com o problema do download fui pesquisar e descobri o tempfile.mkdtemp, que cria uma pasta temporária e faz um append no prefixo com um hash aleatório, assim fica mais facil de criar e deletar a pasta, sem correr o risco de pagar algo mais importante igual estava antes com o absolute() e o .parent
Fora esses pontos não encontrei nenhuma outra dificuldade em fazer o script funcionar, minha preocupação se voltou para deixar o código mais modular e tentar o máximo possível otimizar o tempo do desafio, para isso meu primeiro ponto foi testar iterar pelo dataframe utilizando itertuples no lugar do iterrows, o itertuples foi 0.003s mais rápido. O próximo passo foi diminuir o tempo de espera na função ``` _download_wait ```, de 1 segundo para 0.5, testei com valores menores mas o ganho não foi grande o sufciente para justificar a eventual chance de erro.

Decidi fazer o script da automação em outra pasta em vez de em um arquivo só por questões de organização, caso precise rodar mais de alguma automação junta ou algum outro processo isso seria feito através do arquivo main.py, dessa forma sigo o padrão SOLID.

Tentei separar bem as funções e deixar elas simples de serem lidas para facilitar o entendimento e facilitar futuros testes, também utilizei o factory por causa disso e já tenho alguma experiência utilizando esse modelo

Não tinha certeza se deveria deixar os logs ou só a parte com o tempo então deixei a maioria dos logs comentados, apenas aparecendo os de erro mas ainda utilizei o logger q eu criei para mostrar o tempo.


