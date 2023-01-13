import pandas as pd
import requests

def main():
  # url do arquivo com a lista de links a serem baixados em formato .json
  url = 'https://raw.githubusercontent.com/gabrielmacedoanac/flat-data-anac/main/regulamentos-url-json.csv' 
  
  # transformar o arquivo em formato de lista
  urls = requests.get(url).text.split() 
  
  # cria dataframe vazio
  df = pd.DataFrame() 
  
  # percorre a lista de url dos arquivos e cria um dataframe com o conteúdo de todos os arquivos ignorando os índices individuais
  for item in urls:
    df = pd.read_json(item).append(df, ignore_index=True)
  
  # Criar uma cópia do dataframe
  df_o = df.copy()
  
  # Remover linhas vazias e duplicadas do dataframe criado, mantendo a última ocorrência das linhas duplicadas
  df.dropna(how='all')
  df.drop_duplicates(keep='last', inplace=True)
  
  # Remover espaços vazios e quebras de linhas antes e depois dos textos nas colunas
  df['ementa'] = df['ementa'].str.strip()
  df['norma'] = df['norma'].str.strip()
  df['tornada_sem_efeito'] = df['tornada_sem_efeito'].str.strip()
  df['alterada'] = df['alterada'].str.strip()
  df['data'] = df['data'].str.strip()
  df['outros'] = df['outros'].str.strip()
  df['tipo_normatico'] = df['tipo_normatico'].str.strip()
  df['publicacao'] = df['publicacao'].str.strip()
  df['revogada'] = df['revogada'].str.strip()
  df['em_vigor'] = df['em_vigor'].str.strip()
  df['anexos'] = df['anexos'].str.strip()
  
  # Corrigir os dados incorretos publicados pela ANAC. Série de regras de substituição de caracteres
  # corrige links errados na coluna anexos
  df['anexos']=df['anexos'].str.replace('portalhomolog2', 'www')
  df['anexos']=df['anexos'].str.replace('@@download/', '/@@display-file/')
  
  # Extrair e criar metadados
  
  # Importar biblioteca de expressões regulares
  import re
  
  # Criar colunas de dados_nao_estruturados para gerar as tags
  df['dados_nao_estruturados']=df[['ementa','norma']].agg(' | '.join, axis=1)
  
  # Gerar tags ignorando capitalização (maiúsculas e minúsculas) a partir da
  df['tags']=df['dados_nao_estruturados'].str.lower().str.findall('([0-9]{1,13}\.[0-9]{1,15}|rbac|rbha|lei|decret\w+|decis\w+|crm|cnpj|cpf|portari\w+|isen\w+|cumpriment\w+ alternativ\w+|n[i|í]v\w+ equivalent\w+ d\w+ seguran\w+|diretri\w+ d\w+ aeronavegabilidade|certificad\w+ suplementar\w+ de tip\w+|embraer|alter\w+|modific\w+)', flags=re.IGNORECASE)
  
  # Gerar valores únicos para as tags e unir com "|" 
  df['tags']=df['tags'].apply(set).str.join("|")
  
  # Classificar os valores em ordem alfabética
  df['tags']=df['tags'].map(lambda x: '|'.join(sorted(x.split('|')))) 
  
  # Substituir valores (texto) das tags para valores desejados
  df['tags']=df['tags'].str.replace(r'certificad\w+ suplementar\w+ de tip\w+', 'cst', regex=True)
  
  # Remover coluna dados_nao_estruturados
  df.drop(columns=["dados_nao_estruturados"],inplace=True)
  
  # Converter valores das tags para uma lista
  df['tags'] = df['tags'].str.replace("|", ", ", regex=False).str.split(', ').tolist()
  
  # Ordenar a lista de forma alfabética
  df['tags'] = df['tags'].apply(sorted)
  
  # CSV - indicar local onde o arquivo será salvo
  path = './regulamentos-anac-tags.csv'

  # salvar arquivo em formato .csv com codificação utf-8
  with open(path, 'w', encoding = 'utf-8-sig') as f:
    df.to_csv(f, index=False)
  
  # TSV - indicar local onde o arquivo será salvo 
  path = './regulamentos-anac-tags.tsv'
  # salvar arquivo em formato .csv com codificação utf-8
  with open(path, 'w', encoding = 'utf-8-sig') as f:
    df.to_csv(f, sep="\t", index=False)
  
  # JSON - indicar local onde o arquivo será salvo
#  path = './regulamentos-anac-tags.json'
  # salvar arquivo em formato .json
#  with open(path, 'w') as f:
#    df.to_json(f, orient="records")

  df.to_json('./regulamentos-anac-tags.json', force_ascii=False, orient="records")
  
if __name__ == '__main__':
  main()

  
  

