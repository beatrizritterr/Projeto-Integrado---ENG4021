import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from core.models import Professor, Disciplina, Curso

def run_microhorario_scraping_for_course(course_url):
    """
    Versão SELENIUM: Executa o scraping em sites com JavaScript.
    Abre um navegador, espera os dados carregarem e extrai as informações.
    """
    print(f"Iniciando scraping (via Selenium) para: {course_url}")

    chrome_options = Options()
   
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--log-level=3")

    driver = webdriver.Chrome(options=chrome_options)
    html_content = None

    try:
        print("Navegador aberto. Acessando URL e aguardando dados...")
        driver.get(course_url)

       
        wait = WebDriverWait(driver, 30)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "col_Professor.zw-rgrid-detail")))
        
        print("Dados carregados na página! Extraindo o HTML...")
        html_content = driver.page_source

    except TimeoutException:
        print("\n[ERRO] Tempo limite esgotado.")
        print("O site demorou mais de 30s para carregar ou a classe 'col_Professor' não foi encontrada.")
        print("Dica: Verifique a URL e se o seletor CSS ainda é válido.")
    except Exception as e:
        print(f"\n[ERRO] Ocorreu um erro inesperado no Selenium: {e}")
    finally:
        driver.quit() 

    if not html_content:
        return 

    
    soup = BeautifulSoup(html_content, 'html.parser')

    curso_obj = None
    curso_nome_element = soup.find(['h3', 'h4', 'span'], class_=lambda x: x and ('titulo' in x or 'curso' in x))
    if not curso_nome_element:
         curso_nome_element = soup.find('span', id=lambda x: x and 'NomeCurso' in x)

    if curso_nome_element and curso_nome_element.text.strip():
        curso_nome = curso_nome_element.text.strip().split('-')[0].strip()
        curso_obj, created = Curso.objects.get_or_create(nome=curso_nome)
        if created: print(f"  [Curso] '{curso_nome}' criado.")
    
    all_tr_elements = soup.find_all('tr')
    processed_count = 0
    print(f"Analisando {len(all_tr_elements)} linhas de tabela...")

    for tr in all_tr_elements:
        professor_td = tr.find('td', class_=lambda x: x and 'col_Professor.zw-rgrid-detail' in x)
        
        if professor_td:
            professor_nome = professor_td.text.strip()
            if not professor_nome or professor_nome.lower() in ["a definir", "", "&nbsp;", "sem professor"]:
                continue

            processed_count += 1

            disciplina_codigo = None
            disciplina_nome = None
            
            all_tds = tr.find_all('td')
            
            if len(all_tds) >= 2:
                disciplina_codigo = all_tds[0].text.strip()
                disciplina_nome = all_tds[1].text.strip()

            
            professor_obj, _ = Professor.objects.get_or_create(nome=professor_nome)
            
           
            if disciplina_codigo and disciplina_nome:
                disciplina_obj, _ = Disciplina.objects.get_or_create(
                    codigo=disciplina_codigo, defaults={'nome': disciplina_nome}
                )
                disciplina_obj.professores.add(professor_obj)
                if curso_obj:
                    curso_obj.disciplinas.add(disciplina_obj)
                

    print("-" * 30)
    print(f"Scraping finalizado. {processed_count} entradas processadas e salvas.")