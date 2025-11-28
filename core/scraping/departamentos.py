# core/scraping/departamentos.py

import requests
from bs4 import BeautifulSoup
import re

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException


from core.models import Professor, Departamento

def _scrape_with_requests(url):
    """Função auxiliar para fazer requisição HTTP simples com requests."""
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status() 
        return BeautifulSoup(response.content, 'html.parser')
    except requests.exceptions.RequestException as e:
        print(f"  [ERRO Requests] Falha ao acessar {url}: {e}")
        return None

def _scrape_with_selenium(url, wait_selector_type, wait_selector_value, timeout=30):
    """Função auxiliar para fazer requisição com Selenium."""
    chrome_options = Options()
    chrome_options.add_argument("--headless") 
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--log-level=3")

    driver = None
    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        wait = WebDriverWait(driver, timeout)
        
        print(f"  [Selenium] Esperando por {wait_selector_type} = '{wait_selector_value}'...")
        wait.until(EC.presence_of_element_located((wait_selector_type, wait_selector_value)))
        
        print("  [Selenium] Dados carregados via JavaScript.")
        return BeautifulSoup(driver.page_source, 'html.parser')
    except TimeoutException:
        print(f"  [ERRO Selenium] Tempo limite ({timeout}s) esgotado ou seletor '{wait_selector_value}' não encontrado em {url}.")
        return None
    except WebDriverException as e:
        print(f"  [ERRO Selenium] WebDriver falhou para {url}: {e}")
        return None
    finally:
        if driver:
            driver.quit()

def _extract_valid_name(tag):
    """Extrai e valida um nome de professor de uma tag."""
    name = tag.text.strip()
    if len(name.split()) >= 2 and len(name) > 5 and not re.search(r'\d', name):
        return name
    return None


def _extract_layout_eng_mecanica(soup):
    professors_on_page = set()
    divs_prof = soup.find_all('div', class_=re.compile(r'col-sm-10', re.IGNORECASE))
    for div in divs_prof:
        link_tag = div.find('span').find('a') if div.find('span') else div.find('a')
        if link_tag:
            name = _extract_valid_name(link_tag)
            if name: professors_on_page.add(name)
    return list(professors_on_page)

def _extract_layout_matematica(soup):
    professors_on_page = set()
    h5_titles = soup.find_all('h5', class_='card-title')
    for h5 in h5_titles:
        link_tag = h5.find('a')
        if link_tag:
            name = _extract_valid_name(link_tag)
            if name: professors_on_page.add(name)
    return list(professors_on_page)

def _extract_layout_fisica(soup):
    professors_on_page = set()
    h4_headings = soup.find_all('h4', class_='media-heading')
    for h4 in h4_headings:
        link_tag = h4.find('a')
        if link_tag:
            name = _extract_valid_name(link_tag)
            if name: professors_on_page.add(name)
    return list(professors_on_page)

def _extract_layout_quimica(soup):
    professors_on_page = set()
    accordion_heads = soup.find_all('div', class_='accordion-head')
    for head in accordion_heads:
        p_tag = head.find('p')
        if p_tag:
            name = _extract_valid_name(p_tag)
            if name: professors_on_page.add(name)
    return list(professors_on_page)

def _extract_layout_informatica(soup):
    professors_on_page = set()
    h5_titles = soup.find_all('h5', class_='item-title')
    for h5 in h5_titles:
        link_tag = h5.find('a')
        if link_tag:
            name = _extract_valid_name(link_tag)
            if name: professors_on_page.add(name)
    return list(professors_on_page)

def _extract_layout_eng_civil_ambiental(soup):
    professors_on_page = set()
    divs = soup.find_all('div', class_=re.compile(r'fusion-text-\d+.*fusion-text-no-margin', re.IGNORECASE))
    for div in divs:
        p_tag = div.find('p')
        if p_tag:
            link_tag = p_tag.find('a')
            if link_tag:
                strong_tag = link_tag.find('strong')
                if strong_tag:
                    name = _extract_valid_name(strong_tag)
                    if name: professors_on_page.add(name)
    return list(professors_on_page)

def _extract_layout_eng_eletrica(soup):
    professors_on_page = set()
    divs = soup.find_all('div', class_='wpb_wrapper')
    for div in divs:
        p_tag = div.find('p')
        if p_tag:
            span_tag = p_tag.find('span')
            if span_tag:
                name = _extract_valid_name(span_tag)
                if name: professors_on_page.add(name)
    return list(professors_on_page)

def _extract_layout_eng_quimica_materiais(soup):
    professors_on_page = set()
    divs = soup.find_all('div', class_=re.compile(r'fusion-text-\d+', re.IGNORECASE))
    for div in divs:
        p_tag = div.find('p')
        if p_tag:
            strong_tag = p_tag.find('strong')
            if strong_tag:
                link_tag = strong_tag.find('a')
                if link_tag:
                    name = _extract_valid_name(link_tag)
                    if name: professors_on_page.add(name)
    return list(professors_on_page)

def _extract_layout_eng_industrial(soup):
    professors_on_page = set()
    h4_titles = soup.find_all('h4', class_='title')
    for h4 in h4_titles:
        link_tag = h4.find('a')
        if link_tag:
            name = _extract_valid_name(link_tag)
            if name: professors_on_page.add(name)
    return list(professors_on_page)


def run_departamento_scraping(departamento_url, departamento_nome=None, layout_type='default', use_selenium=False, selenium_wait_selector=None):
    """
    Executa o scraping de uma URL de página de departamento usando o layout especificado.
    Pode usar Requests (padrão) ou Selenium.
    """
    print(f"Iniciando scraping para {departamento_nome if departamento_nome else departamento_url} (Layout: {layout_type})...")

    soup_data = None 
    if use_selenium:
        if not selenium_wait_selector or not isinstance(selenium_wait_selector, tuple) or len(selenium_wait_selector) != 2:
            print("  [ERRO] Para usar Selenium, 'selenium_wait_selector' deve ser uma tupla (By.TIPO, 'seletor').")
            return [] 
        
        soup_data = _scrape_with_selenium(departamento_url, selenium_wait_selector[0], selenium_wait_selector[1])
    else:
        soup_data = _scrape_with_requests(departamento_url)
    
    if not soup_data: 
        return []

    professors_found = []
    
    if layout_type == 'eng_mecanica':
        professors_found = _extract_layout_eng_mecanica(soup_data)
    elif layout_type == 'matematica':
        professors_found = _extract_layout_matematica(soup_data)
    elif layout_type == 'fisica':
        professors_found = _extract_layout_fisica(soup_data)
    elif layout_type == 'quimica':
        professors_found = _extract_layout_quimica(soup_data)
    elif layout_type == 'informatica':
        professors_found = _extract_layout_informatica(soup_data)
    elif layout_type == 'eng_civil_ambiental':
        professors_found = _extract_layout_eng_civil_ambiental(soup_data)
    elif layout_type == 'eng_eletrica':
        professors_found = _extract_layout_eng_eletrica(soup_data)
    elif layout_type == 'eng_quimica_materiais':
        professors_found = _extract_layout_eng_quimica_materiais(soup_data)
    elif layout_type == 'eng_industrial':
        professors_found = _extract_layout_eng_industrial(soup_data)
    else:
        print(f"  [ERRO] Tipo de layout desconhecido: '{layout_type}'. Nenhum professor extraído.")
        return []

    saved_count = 0
    departamento_obj = None
    if departamento_nome:
        departamento_obj, _ = Departamento.objects.get_or_create(nome=departamento_nome)

    for prof_name in sorted(list(professors_found)):
        professor_obj, created = Professor.objects.get_or_create(nome=prof_name)
        if created:
            print(f"    [Professor Adicionado] '{prof_name}'")
        
        if departamento_obj:
            departamento_obj.professores.add(professor_obj)
        saved_count += 1

    print(f"Scraping finalizado para {departamento_nome}. {saved_count} professores encontrados e salvos.")
    if saved_count == 0:
        print("  [ALERTA] Nenhum professor encontrado com os seletores deste layout.")
        print("  Verifique o seletor CSS e/ou se o site precisa de JavaScript (use '--selenium').")
    
    return professors_found