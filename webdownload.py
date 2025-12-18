#!/usr/bin/env python
# coding: utf-8

# In[88]:


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
import time
import os
import pandas as pd
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import shutil
from datetime import datetime
from dotenv import load_dotenv
from selenium.webdriver.chrome.service import Service


# In[89]:


download_dir = os.path.join(os.getcwd(), "downloads")
os.makedirs(download_dir, exist_ok=True)

#chrome_options.add_experimental_option("prefs", {
#    "download.default_directory": download_dir,
#    "download.prompt_for_download": False,
#    "download.directory_upgrade": True,
#    "safebrowsing.enabled": True
#})

# Configurações do Chrome
chrome_options = Options()
chrome_options.add_experimental_option("prefs", {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True  # evita bloqueios de segurança
})
# Adiciona o modo headless
chrome_options.add_argument("--headless=new")  # Use --headless se estiver usando uma versão mais antiga do Chrome
chrome_options.add_argument("--window-size=1920,1080")  # Evita problemas com redimensionamento de elementos
chrome_options.add_argument("--disable-gpu")  # Recomendado para evitar bugs em alguns sistemas
chrome_options.add_argument("--no-sandbox")  # Útil em ambientes Linux
# Inicia o Chrome com as opções configuradas
#driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
#driver = webdriver.Chrome(executable_path='/usr/bin/chromedriver', options=chrome_options)

service = Service('/usr/bin/chromedriver')
driver = webdriver.Chrome(service=service, options=chrome_options)

# In[90]:


#chrome_options = Options()
#chrome_options.add_experimental_option("prefs", {
#    "download.default_directory": download_dir,
#    "download.prompt_for_download": False,
#    "download.directory_upgrade": True,
#    "safebrowsing.enabled": True
#})


# In[91]:


#driver = webdriver.Chrome(options=chrome_options)


# In[92]:


driver.get("https://academico.ifms.edu.br/administrativo/")


# In[93]:


usuario = driver.find_element(By.ID, "UsuarioLogin")
senha = driver.find_element(By.ID, "UsuarioSenha")
#botao_login = driver.find_element(By.Value, "Entrar")
botao_login= driver.find_element(By.XPATH,'//*[@value="Entrar"]')

#load_dotenv()

usuario_login = os.environ["USUARIO_LOGIN"]
usuario_senha = os.environ["USUARIO_SENHA"]


usuario.send_keys(usuario_login)
senha.send_keys(usuario_senha)
botao_login.click()


# In[94]:


driver.get("https://academico.ifms.edu.br/administrativo/relatorios/retidos_semestre")
escolha = driver.find_element(By.ID, "CursoId_chosen")
escolha.click()

driver.find_element(By.XPATH, '//li[@data-option-array-index="4"]').click()

escolha = driver.find_element(By.ID, "CursoId_chosen")
escolha.click()
driver.find_element(By.XPATH, '//li[@data-option-array-index="18"]').click()

escolha = driver.find_element(By.ID, "CursoId_chosen")
escolha.click()
driver.find_element(By.XPATH, '//li[@data-option-array-index="8"]').click()

escolha = driver.find_element(By.ID, "CursoId_chosen")
escolha.click()
driver.find_element(By.XPATH, '//li[@data-option-array-index="10"]').click()

escolha = driver.find_element(By.ID, "CursoId_chosen")
escolha.click()
driver.find_element(By.XPATH, '//li[@data-option-array-index="12"]').click()

escolha = driver.find_element(By.ID, "CursoId_chosen")
escolha.click()
driver.find_element(By.XPATH, '//li[@data-option-array-index="14"]').click()

escolha = driver.find_element(By.ID, "RelatorioSemestre")
escolha.click()

#select_element = driver.find_element(By.ID, "RelatorioSemestre")
seletor = Select(escolha)
seletor.select_by_value("12")



#escolha = driver.find_element(By.ID, "RelatorioCargaHoraria")
campo_carga = driver.find_element(By.ID, "RelatorioCargaHoraria")
campo_carga.clear()            # limpa o campo, se tiver algo já
campo_carga.send_keys("0")   

#botao_baixar= driver.find_element(By.VALUE,'xls')
#botao_baixar.click()

botao_xls = driver.find_element(By.XPATH, '//button[@value="xls"]')
botao_xls.click()


# In[95]:


#time.sleep(60)

caminho_xls = os.path.join(download_dir, "relatorio_retidos.xls")
caminho_csv = os.path.join(os.getcwd(), "trypa5.csv")

# Remove o .xls antigo se existir
if os.path.exists(caminho_xls):
    os.remove(caminho_xls)
    print("Arquivo .xls antigo removido.")

# Aguarda até o novo .xls ser baixado
print("Aguardando o download do novo .xls...")
timeout = 120  # segundos
inicio = time.time()
while not os.path.exists(caminho_xls):
    if time.time() - inicio > timeout:
        raise TimeoutError("Tempo excedido aguardando o download do arquivo .xls.")
    time.sleep(1)

# Converte o .xls para DataFrame
tabelas = pd.read_html(caminho_xls)
df = tabelas[0]

# Salva o CSV mais recente (sobrescreve trypa5.csv)
df.to_csv(caminho_csv, index=False)
print(f"Arquivo principal atualizado: {caminho_csv}")

# Cria uma cópia com timestamp como backup
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
caminho_backup = os.path.join(download_dir, f"backup_trypa5_{timestamp}.csv")
shutil.copy(caminho_csv, caminho_backup)