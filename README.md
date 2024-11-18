# README

## Objetivo do Projeto

Subsidiar o planejamento de gestores dos Ministério da Saúde para o ano posterior, bem como indicar localidades nas quais há espaço para incremento/investimento em infraestrutura de saúde

## Instalação do Ambiente e Biblioteca

As dependências necessárias para a execução do projeto estão registradas no arquivo requirements.txt. 

As instruções para a instalação da biblioteca em python podem ser observadas no [link](https://basedosdados.github.io/mais/access_data_packages/).

Todavia, logo após a criação do virtual environment, deve ser realizada a instalação primeiro da biblioteca Base dos Dados. Isso porque, a referida biblioteca, além de ser necessária para se utilizar a API, irá instalar outras dependências como por exemplo o pandas.

Um ponto de atenção, é o fato da biblioteca Base dos Dados necessitar de **Python >=3.7.1, <3.11**.

Assim, recomenda-se que sejam seguidos os seguintes passos: 

``` shell
python3.10 -m venv .venv
source .venv/bin/activate
pip install basedosdados
```

Conforme registrado, durante a instalação da biblioteca base dos dados, diversas outras são instaladas, como por exemplo pandas e numpy. Ocorre que identificou-se uma incompatibilidade com a versão do numpy instalado, sendo necessária a correção das mesma por meio da instalação de uma versão mais antiga: 

``` shell
pip uninstall numpy
pip install numpy==1.24.0
```

Conforme instruções registradas no [link](https://basedosdados.github.io/mais/access_data_packages/), antes do perfeito funcionamento da API, há a necessidade de se criar um projeto na Google Cloud. Para isso podemos seguir os seguintes passos:

    Antes de começar: Crie o seu projeto no Google Cloud.
    
    Para criar um projeto no Google Cloud basta ter um email cadastrado no Google. É necessário ter um projeto seu, mesmo que vazio, para você fazer queries em nosso datalake público.
    
    1. Acesse o Google Cloud. Caso for a sua primeira vez, aceite o Termo de Serviços.
    
    2. Clique em Create Project/Criar Projeto . Escolha um nome bacana para o projeto.
    
    3. Clique em Create/Criar

Justificativa: 

A Google fornece 1 TB gratuito por mês de uso do BigQuery para cada projeto que você possui. Um projeto é necessário para ativar os serviços do Google Cloud, incluindo a permissão de uso do BigQuery. Pense no projeto como a "conta" na qual a Google vai contabilizar o quanto de processamento você já utilizou. Não é necessário adicionar nenhum cartão ou forma de pagamento - O BigQuery inicia automaticamente no modo Sandbox, que permite você utilizar seus recursos sem adicionar um modo de pagamento. Leia mais aqui.

Após a instalação da biblioteca Base dos dados, foi necessária a instalação do Streamlit e da biblioteca tabula-py, chegando assim ao requirements.txt atual.

## Endpoints do Projeto

O projeto disponibiliza 2 endpoints com 2 métodos POST de forma a permitir que as funcionalidades do aplicativo que são apresentadas em front-end via Streamlit também possam ser acessadas via APIs. 
Sendo assim, temos:

* /atendimento-proximo:  
    * Método: POST
    * Funcionalidade: retornar a cidade mais recomendada para o atendimento mais próximo, bem como o tempo de deslocamento
    * Body
     ```python
    {"origem": "Pacaraima", "raio": 300}
    ```
    * Exemplo:  
    ```python
    {"atendimento":"Pacaraima","tempo_viagem":"2 horas e 35 minutos"}
    ```

* /direcionador-investimento:

    * Método: GET
    * Funcionalidade: retornar lista das cidade mais recomendadas para investimentos na área de saúde
    * Exemplo:  

    ```python
    [{"Municipio":"Alto Alegre","Score de Investimento":10.0},{"Municipio":"Pacaraima","Score de Investimento":9.224423429851136},{"Municipio":"Canta","Score de Investimento":5.2985470231364244},{"Municipio":"Amajari","Score de Investimento":5.121742731501089}]
    ```

## Github do Projeto

[Link do Projeto](https://github.com/pedromvba/applied-ds-tp1)

## Dados do Projeto

Devido ao tamanho dos dados, a pasta data não foi replicada no Github. Os dados podem ser obtidos recriando-se o ambiente e executando os scripts conforme registrado no Data Summary Report, ou podem ser obtidos diretamente no seguinte [link](https://drive.google.com/file/d/1sNKzhx4-ATKZ2tqLI8mPeVx1YYeMMoiv/view?usp=share_link).

Caso opte pelo download, observe a necessidade de colocar o diretório data na raiz do projeto, juntamente com outras pastas como docs, notebooks e app.

## Links Úteis

[Github do Projeto](https://github.com/pedromvba/applied-ds-tp1)

[Dados do Projeto](https://drive.google.com/file/d/1sNKzhx4-ATKZ2tqLI8mPeVx1YYeMMoiv/view?usp=share_link).

[Base dos Dados Pypi](https://pypi.org/project/basedosdados/)

[Página do Dataset - Base dos Dados](https://basedosdados.org/dataset/ff933265-8b61-4458-877a-173b3f38102b?table=75db9d44-42be-42c5-9fbc-7591f4dc8d5f)

[Instalação da Biblioteca Base dos Dados](https://basedosdados.github.io/mais/access_data_packages/)

[Manual da Biblioteca Base dos Dados](https://basedosdados.github.io/mais/api_reference_python/)

[Manual Técnico do Sistema de Informação Hospitalar - 2007](https://bvsms.saude.gov.br/bvs/publicacoes/07_0066_M.pdf)

[Manual do Sistema de Informações Hospitalares do SUS (SIH/SUS) - 2004](https://giannaberetta.sistemasiga.net/static/salavirtual/arquivos/2126248621190918125950-lv.pdf)

[Conversor Códigos/Cidades - Datasus](http://tabnet.datasus.gov.br/cgi/deftohtm.exe?sih/cnv/spabr.def)

[Conversor Códigos/Procedimentos - Datasus](http://tabnet.datasus.gov.br/cgi/deftohtm.exe?sih/cnv/qiuf.def)

[Inspiração para o Projeto - Medium](https://medium.com/data-hackers/explorando-dados-do-sus-com-sql-e9c6cfc08cc2)

[Team Data Science Process - TDSP](https://learn.microsoft.com/pt-br/azure/architecture/data-science-process/overview)














