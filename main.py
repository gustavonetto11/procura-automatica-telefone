import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def obter_numero_telefone(empresa, cidade):
    # Inicializa o serviço do ChromeDriver
    service = Service('C:/Users/User/AppData/Local/Programs/Python/Python311/chromedriver.exe')
    options = webdriver.ChromeOptions()
    #options.add_argument('--headless') # Argumento para não abrir uma janela
    driver = webdriver.Chrome(service=service, options=options)

    pesquisa = empresa + ' ' + cidade

    url = 'https://www.google.com/search?q='
    driver.get(url + pesquisa)   
    
    try: 
        WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.CLASS_NAME, 'LrzXr.zdqRlf.kno-fv')))
        elemento_resultado = driver.find_element(By.CLASS_NAME, 'LrzXr.zdqRlf.kno-fv')  # Essa é a classe específica para os telefones nos resultados do Google
        numero_telefone = elemento_resultado.text
    except:
        numero_telefone = 'NF'  # Se não encontrar o número, definir como "NF" (Número não encontrado)
    
    driver.quit()
    
    return numero_telefone

# Ler dados da planilha Excel
dados = pd.read_excel('C:/Users/User/Desktop/AutoSearchPhone/ILHEUS_JUN23_Pt2.xlsx')  # Caminho para o arquivo Excel
empresas = dados['Nome Fantasia'].tolist()
cidades = dados['Município'].tolist()

# Criar uma lista para armazenar os resultados
resultados = []

# Obter os números de telefone
for empresa, cidade in zip(empresas, cidades):
    numero_telefone = obter_numero_telefone(empresa, cidade)
    resultados.append({'Empresa': empresa, 'Cidade': cidade, 'Telefone 3': numero_telefone})

# Criar um DataFrame a partir dos resultados
df = pd.DataFrame(resultados)

# Salvar os dados em um arquivo Excel
df.to_excel('C:/Users/User/Desktop/AutoSearchPhone/resultados_telefone.xlsx', index=False)