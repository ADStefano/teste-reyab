# Teste Dev JR Reyab

O objetivo do teste prático é automatizar o desafio [RPAChallange](https://rpachallenge.com/), realizando:
* Download do arquivo inicial.
* Leitura e tratamento dos dados da planilha excel.
* Preenchimento automático do formulário.
* Captura do tempo total de execução.

## Tecnologias utilizadas:

![Python Version](https://img.shields.io/badge/Python-3.14-blue)
![Selenium](https://img.shields.io/badge/Selenium-4.38.0-green)
![Pandas](https://img.shields.io/badge/Pandas-2.3.3-yellow)
![Pytest](https://img.shields.io/badge/Pytest-9.0.1-blueviolet)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen)
![OpenPyXL](https://img.shields.io/badge/openpyxl-3.1.5-blue)



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
Utilizei o Conda para gerenciar o ambiente. Caso não tenha instaldo, siga as intruções [aqui](https://docs.conda.io/projects/conda/en/latest/user-guide/install/).

Para criar o ambiente:
``` 
conda create -n web_automation python=3.14
```

Para ativar o ambiente:
``` 
conda activate web_automation 
```

### Instalando as dependências do projeto:
O Projeto utiliza o [Selenium](https://www.selenium.dev/pt-br/documentation/), [Pandas](https://pandas.pydata.org/) junto do [Openpyxl](https://pypi.org/project/openpyxl/) e [Pytest](https://docs.pytest.org/en/stable/). Para instalar as dependências utilize o comando: 
```
 pip install -r requirements.txt
 ```

## Rodando o projeto

Para rodar o projeto vá até a pasta em que ele foi extraido, e na raiz rode o comando no terminal:
```
python main.py
```
O script abrirá o navegador, realizará a automação completa e exibirá o tempo total no console.

## Considerações
Abaixo explico as principais decisões técnicas adotadas ao longo do desenvolvimento e os desafios encontrados.

### 1. Seleção dos elementos:
Tive dificuldade inicial para localizar os campos do formulário, porque os IDs eram dinâmicos.
Para tornar o código mais legível e evitar soluções improvisadas, utilizei o XPATH com os atributos para os campos do formulário:
```
ng-reflect-name='labelFirstName'
```
Eles são consistentes e deixam o código mais claro do que mapear os elementos via variáveis, ini ou outras gambiarras.

### 2. Download do arquivo:
No inicío havia risco de apagar pastas erradas ao trabalhar com ```absolute()``` e ```.parent```.
A solução definitiva foi utilizar:
```
tempfile.mkdtemp(prefix="rpa_challange")
```
Isso cria uma pasta temporária com um prefixo atrelado a um hash aleátorio, facilitando a criação, remoção e prevenindo acidentes ao remover o diretório.

### 3. Estrutura do projeto e modularização:
Optei por separar o código em uma pasta web_automation/ por motivos de organização e aderência a princípios como responsabilidade única.
O main.py é o ponto de inicio da automação, permitindo rodar múltiplas automações no futuro, aproveitar a estrutura modular e facilitar teste unitários.
Também utilizei o factory para instanciar o WebDriver com as suas dependências, deixando a classe principal mais facilde testar.

### 4. Otimização:
O tempo médio da execução da automação ficou: 4894,7.
Tentei reduzir o tempo total da automação com o uso do ```itertuples``` no lugar do ```iterrows``` que diminui cerca de 0.003s o tempo de execução.
E depois tentei diminuir o máximo possível o a espera na função ```download_wait```, deixando fixo em 0.5 segundos, o que reduziu o tempo sem comprometer a confiabilidade.

### 5. Testes:
Não consegui identificar uma forma eficiente de testar automaticamente os métodos que interagem diretamente com Selenium. Porém, consegui testar:
* A função que lê a planilha com Pandas
* A normalização dos nomes das colunas
* A validação de erro quando o arquivo não existe
* A extração do tempo via expressão regular (_get_time)

Para rodar os teste basta rodar o seguinte comando no terminal:
```
pytest -v
```

### 6. Loggin:
Não tinha certeza se deveria manter logs detalhados ou somente o tempo final.Por isso removi os logs, o log de tempo final foi substituido por um ```print()```. O logging continua configurado corretamente caso precise no futuro.




