import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def obter_numero_telefone(empresa, cidade):
    # Inicializa o serviço do ChromeDriver
    service = Service('Caminho/para/chromedriver.exe')
    options = webdriver.ChromeOptions()
    options.add_argument('--headless') # Argumento para não abrir uma janela
    driver = webdriver.Chrome(service=service, options=options)
    
    # Pesquisa diretamente via url
    pesquisa = empresa + ' ' + cidade
    url = 'https://www.google.com/search?q='
    driver.get(url + pesquisa)   
    
    try: 
        WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.CLASS_NAME, 'LrzXr.zdqRlf.kno-fv'))) # Esperar até a classe desejada apareça
        elemento_resultado = driver.find_element(By.CLASS_NAME, 'LrzXr.zdqRlf.kno-fv')  # Essa é a classe específica para os telefones nos resultados do Google
        numero_telefone = elemento_resultado.text
    except:
        numero_telefone = 'NF'  # Se não encontrar o número, definir como "NF" (Número não encontrado)
    
    driver.quit()
    
    return numero_telefone 

# Ler dados da planilha Excel
dados = pd.read_excel('Caminho/para/planilha.xlsx')  # Caminho para o arquivo Excel
empresas = dados['COLUNA X'].tolist() # Selecionar coluna com os nomes de empresas
cidades = dados['COLUNA Y'].tolist()  # Selecionar coluna com os nomes das cidades

# Criar uma lista para armazenar os resultados
resultados = []

# Obter os números de telefone
for empresa, cidade in zip(empresas, cidades):
    numero_telefone = obter_numero_telefone(empresa, cidade)
    resultados.append({'Empresa': empresa, 'Cidade': cidade, 'Telefone 3': numero_telefone})

# Criar um DataFrame a partir dos resultados
df = pd.DataFrame(resultados)

# Salvar os dados em um arquivo Excel
df.to_excel('Caminho/para/resultados.xlsx', index=False)
