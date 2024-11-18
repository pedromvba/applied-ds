'''
Python Script responsable for retrieving the names of the procedures from the procedures codes.
The procedures names originate from a pdf found in the internet, made by the Prefeitura Municipal de Camaçari.
'''

import tabula
import pandas as pd

#Prefeitura Municipal file path
pdf_path = 'data/01_raw/TABELA_NACIONAL_PROCEDIMENTOS.pdf'

#Reading pdf tables
tables = tabula.read_pdf(pdf_path, pages='all', multiple_tables=False, relative_columns=True)

#concatenating tables and selecting interested columns
concat_table = pd.concat(tables, ignore_index=True)
concat_table = concat_table[['CÓDIGO', 'PROCEDIMENTO']]

#saving csv file
concat_table.to_csv('data/01_raw/procedure_names.csv',index=False)
