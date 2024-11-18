# Data Summary Report

## Objetivo do Uso dos Dados

Gerar modelo preditivo que consiga prever com base em dados históricos o número de atendimentos previsto para o próximo ano, bem como o custo previsto.

Desenvolver painel com análise acerca das regiões com potencial de investimento em infraestrutura de saúde, baseados no deslocamento dos cidadãos em busca de atendimento do SUS.

Indicar ao cidadão a localidade mais próxima com o melhor atendimento do SUS.

## Dados

### Base dos Dados (API)

#### Origem:

Base dos Dados:

Organização não-governamental sem fins lucrativos e open source. A Associação tem como missão universalizar o acesso a dados no Brasil, por meio da difusão de conhecimento e da criação de ferramentas, a fim de promover o desenvolvimento socioeconômico, o bem-estar social e políticas públicas baseadas em dados e evidências.

[Website Base dos Dados](basedosdados.org)

#### Dados Utilizados:

Sistema de Informações Hospitalares do SUS (SIH/SUS) - Ministério da Saúde

O SIH/SUS, ou Sistema de Informações Hospitalares do Sistema Único de Saúde, é um banco de dados que abrange todos os hospitais que utilizam o SUS, gerido pela Secretaria de Atenção Especializada à Saúde, do Ministério da Saúde. Esse sistema coleta informações sobre internações hospitalares, incluindo dados sobre o paciente, o diagnóstico, os procedimentos realizados e os valores pagos. O SIH/SUS é fundamental para o acompanhamento e gestão dos serviços hospitalares, além de ser uma importante ferramenta para a produção de estatísticas de saúde e a realização de pesquisas.

[Website dos Dados Utilizados](https://basedosdados.org/dataset/ff933265-8b61-4458-877a-173b3f38102b?table=75db9d44-42be-42c5-9fbc-7591f4dc8d5f)

#### Tabela Utilizada

Serviços Profissionais

A Tabela de Serviços Profissionais do SIH/SUS é uma parte integrante do Sistema de Informações Hospitalares do Sistema Único de Saúde. Ela é utilizada para registrar os serviços e procedimentos realizados por profissionais de saúde dentro de hospitais que atendem pelo SUS. Esta tabela inclui informações sobre o tipo de serviço ou procedimento realizado, o código identificador desse serviço, e os valores de referência para o pagamento.
Os serviços são classificados em diferentes categorias, como assistência médica, serviços de diagnóstico e terapia, e outras áreas de atuação profissional. A tabela é atualizada periodicamente para refletir mudanças nos procedimentos, incorporações de novas tecnologias e práticas clínicas.

#### Importação dos dados

Os dados foram obtidos diretamente da API da Base dos Dados por meio do script data_import.py localizado em ./app/services. Os dados importados por esse script foram salvos em ./app/data/01_raw.

Os dados foram importados utilizando-se a query a seguir:

``` sql
SELECT  quantidade_procedimentos,
        mes,
        ano,
        sigla_uf,
        valor_ato_profissional,
        id_municipio_estabelecimento_aih,
        id_municipio_paciente,
        id_procedimento_principal                        
FROM    basedosdados.br_ms_sih.servicos_profissionais 
WHERE   ano BETWEEN 2020 AND 2023 AND sigla_uf='RR';
```
Ou seja, estão sendo utilizados os dados do SUS, para o Estado de Roraima, para os anos entre 2020 e 2023, incluídos.

Essa seleção se deu devido ao volume dos dados. 

* O estado de Roraima foi escolhido por dentre os estados brasileiros ser um dos menos populosos;
* A amplitude temporal considerou apenas 4 anos, todavia os dados na API da Base dos Dados estão disponíveis de forma gratuita para o período de 2008 até 2023.

Todavia, caso a infraestrutura do projeto suportasse maiores volumes de dados, poderíamos facilmente expandir a análise para períodos maiores, ou para o todo o Brasil ou ainda customiza-la para algum outro Estado específico.

___
### Nome dos Procedimentos

A tabela original da Base dos Dados traz os procedimentos (*id_procedimento_principal*) em formato de código. Para traduzi-los para os efetivos nomes, utilizamos o arquivo TABELA_NACIONAL_PROCEDIMENTOS.pdf, elaborado pela Prefeitura Municipal de Camaçari. A partir desse arquivo pdf, foi possível obter o arquivo procedure_names.csv, constante da pasta ./app/data/01_raw.

A criação do arquivo envolveu a execução do script procedure_names.py, em ./app/services cuja função foi realizar a leitura do arquivo TABELA_NACIONAL_PROCEDIMENTOS.pdf e convertê-lo em um arquivo csv que posteriormente foi utilizado para mapear o nome dos procedimentos no dataset importado via API.

### Nome das Cidades

Os dados obtidos pela API da Base dos Dados traziam, assim como para o caso do procedimento, os dados em formato de código (*id_municipio_estabelecimento_aih e id_municipio_paciente*). Para realizar a conversão dos códigos para o nome das cidades, foi criado manualmente o arquivo cities.json, localizado em ./app/data/01_raw. O script responsável pelo mapeamento do nome das cidades foi o data_processing.py localizado em ./app/services.

A criação do arquivo ocorreu utilizando o [site do datasus](http://tabnet.datasus.gov.br/cgi/deftohtm.exe?sih/cnv/spabr.def) no qual é possível realizar a conversão dos códigos pelo nome das cidades.


### Tempo de Deslocamento e Distância

Para o cálculo do tempo de deslocamento e da distância a ser percorrida, foi utilizada a API do Google - [Distance Matrix API](https://developers.google.com/maps/documentation/distance-matrix/overview?hl=pt-br). Essa API consegue nos retornar, dada uma origem e um destino, o tempo necessário para percorrer a rota, bem como a distância do melhor percurso.

### Cálculo da Melhor Rota

Para o cálculo da melhor rota e apresentação da mesma no aplicativo, foi utilizada a API do Google - [Maps Embed API](https://developers.google.com/maps/documentation/embed/get-started?hl=pt-br)

## Processamento e Amostra dos Dados Processados

### Processamento

Inicialmente, ocorreu o import dos dados utilizando o script data_import.py. Após a importação dos dados, foi necessário realizar alguns processamentos que constam em data_processing.py:

#### 1. Retirada do dígito da coluna *id_municipio_estabelecimento_aih*


#### 2. Filtragem das pessoas atendidas no Estado de Roraima cujo Estado de origem fosse somente Roraima e Amazonas.

Sobre esse ponto, é importante esclarecer que esse critério foi adotado em busca do alcance do objetivo do projeto. O objetivo do projeto é identificar localidades para as quais os cidadãos devam se deslocar de forma a receberem atendimento do SUS, muitas vezes do interior para alguma capital, localidade que normalmente possui recursos de saúde mais desenvolvidos e abundantes.

Durante a análise dos dados, observou-se que algumas pessoas atendidas no Estado de Roraima eram originárias de outros Estados, alguns muito distantes. Dessa forma é improvável, por exemplo, que uma pessoa tenha saído do Rio de Janeiro ou de Goiânia buscando atendimento do SUS em Boa Vista. O mais provável nesses casos é que o referido cidadão estivesse em Boa Vista por algum motivo principal e que secundariamente necessitou buscar atendimento do SUS.

Assim, de forma a manter a coerência do trabalho, bem como retirar esses outliers que apenas distorceriam os dados, foi utilizado o critério de considerar somente os cidadãos originários de municípios dos Estados de Roraima e Amazonas, ou seja, localidades geograficamente próximas ao Estado de Roraima. Consequentemente, os atendimentos de cidadãos originados em municípios de outros Estados foram excluídos com o entendimento de que caso o deslocamento se justificasse pela necessidade de atendimento pelo SUS, isso poderia ser feito em outra capital mais próxima.

Por fim, registra-se que esses outliers representavam 0,46% da amostra.


#### 3. Transformação dos Códigos de Cidades e Procedimentos em Nomes;

#### 4. Retiradas dos Dados Cujos Procedimentos Não Puderam Ser Identificados

Conforme registrado anteriormente neste documento, desejava-se traduzir os procedimentos de código para nome. Não identificamos base de dados do SUS que nos trouxesse essa informação. Assim, buscamos uma opção alternativa na internet, encontrando assim o arquivo TABELA_NACIONAL_PROCEDIMENTOS.pdf, que representava os procedimentos utilizados pela Prefeitura de Camaçari - BA em determinado ano.

Em que pese a maioria dos procedimentos constarem no documento, alguns não estavam, dessa forma, os registros para os quais os procedimentos não puderam ser identificados foram excluídos. Essa exclusão representou 11,8% da base de dados.

Assim, uma das melhorias que poderia ser adicionado a um futuro road map seria um acesso direto via API ou uma maior integração com os sistemas do SUS de forma a proceder essa tradução de forma integral.

De toda forma, considerando a dimensionalidade dos dados processados, 2.158.918 registros, entendemos que a exclusão desses dados não impacta o objetivo do projeto visto que ainda poderão ser identificados regiões com potencial de investimento em infraestrutura de saúde.


### Amostra

| Quantidade de Procedimentos | Mês | Ano  | Sigla UF | Valor Ato Profissional | Município Paciente | Município Atendimento | Procedimento Principal                                                |
|-----------------------------|-----|------|----------|------------------------|---------------------|-----------------------|-------------------------------------------------------------|
| 7                           | 2   | 2023 | RR       | 53.34                  | Amajari             | Boa Vista             | TRATAMENTO DE INFECCOES AGUDAS DAS VIAS AEREAS SUPERIORES   |
| 8                           | 2   | 2023 | RR       | 0.0                    | Amajari             | Boa Vista             | TRATAMENTO DE INFECCOES AGUDAS DAS VIAS AEREAS SUPERIORES   |
| 2                           | 2   | 2023 | RR       | 5.79                   | Amajari             | Boa Vista             | TRATAMENTO DE INFECCOES AGUDAS DAS VIAS AEREAS SUPERIORES   |
| 1                           | 2   | 2023 | RR       | 0.0                    | Pacaraima           | Boa Vista             | TRATAMENTO DE OUTRAS DOENÇAS BACTERIANAS                   |
| 1                           | 2   | 2023 | RR       | 0.0                    | Pacaraima           | Boa Vista             | TRATAMENTO DE OUTRAS DOENÇAS BACTERIANAS                   |
| 5                           | 2   | 2023 | RR       | 48.0                   | São Luiz            | Boa Vista             | TRATAMENTO DE OUTRAS INFECCOES AGUDAS DAS VIAS AEREAS INFERIORES |
| 0                           | 2   | 2023 | RR       | 15.9                   | São Luiz            | Boa Vista             | TRATAMENTO DE OUTRAS INFECCOES AGUDAS DAS VIAS AEREAS INFERIORES |
| 1                           | 2   | 2023 | RR       | 0.0                    | Iracema             | Boa Vista             | TRATAMENTO DE PNEUMONIAS OU INFLUENZA (GRIPE)              |
| 1                           | 2   | 2023 | RR       | 0.0                    | Iracema             | Boa Vista             | TRATAMENTO DE PNEUMONIAS OU INFLUENZA (GRIPE)              |
| 3                           | 2   | 2023 | RR       | 11.31                  | Caracaraí           | Boa Vista             | TRATAMENTO DE DESNUTRICAO                                   |
| 1                           | 2   | 2023 | RR       | 0.0                    | Caracaraí           | Boa Vista             | TRATAMENTO DE DESNUTRICAO                                   |
| 1                           | 2   | 2023 | RR       | 0.0                    | Caracaraí           | Boa Vista             | TRATAMENTO DE DESNUTRICAO                                   |
| 2                           | 2   | 2023 | RR       | 0.0                    | Caracaraí           | Boa Vista             | TRATAMENTO DE DOENÇAS INFECCIOSAS E INTESTINAIS             |

### Descrição dos Campos

Quantidade de Procedimentos: quantidade de procedimentos realizados no atendimento

Mês: mês de realização do atendimento

Ano: ano de realização do atendimento

Sigla UF : Estado no qual foi realizado o atendimento

Valor Ato Profissional: valor do procedimento realizado

Município Paciente: Município de domicílio do paciente

Município Atendimento: Município no qual o paciente foi atendido

Procedimento Principal: principal atendimento realizado


## Integração com LLM (Large Language Model) Local

A funcionalidade que utiliza o LLM local é a do indicador de localidade de atendimento baseado no procedimento desejado pelo cidadão. Por meio dessa funcionalidade o cidadão digitar o procedimento desejado que, utilizando embeddings o LLM retornará as localidades que realizam o procedimento desejado ou o que mais se aproxima do inserido pelo cidadão. Em caso de não ser possível identificar uma alta similaridade entre o procedimento desejado e o realizado pelo SUS, a aplicação indicará ao cidadão as localidades nas quais são realizado atendimentos de emergência em clínica geral, de forma que um médico possa analisar o caso. 

O modelo utilizado foi o [all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2), que é um sentence transformer com 384 dimensões. Esse modelo foi escolhido considerando os seguintes fatores: (i) acurácia, aonde apresentou resultados melhores do que outros modelos, como por exemplo, o [neuralmind/bert-base-portuguese-cased](https://huggingface.co/neuralmind/bert-base-portuguese-cased); (ii) tamanho, considerando a necessida de ser implantado localmente e a infraestrutura disponível e (iii) intenção do desenvolvedor muito similar a do projeto, ser um encoder de pequenas frases de forma a verificar similaridade entre textos.

