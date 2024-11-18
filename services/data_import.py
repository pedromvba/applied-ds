'''
Script for importing the data from the base dos dados api.
'''

import basedosdados as bd

# data collection

# data reading
df_with_procedures = bd.read_sql(query=''' 
                            
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
                  ''',
billing_project_id='projeto-dados-saude',
reauth=True
)

# data saving
df_with_procedures.to_csv('./data/01_raw/roraima_with_procedures.csv',index=False)

print('Data Collection Done!')


