##script do scrapping professor microhorario
import requests
from bs4 import BeautifulSoup
import re

from core.models import Professor, Disciplina, Curso

def run_microhorario_scraping_for_course(course_url):
    """
    Executa o scraping de uma URL específica do MicroHorário (um curso já selecionado),
    extraindo professores, disciplinas e seus códigos, e salvando no banco de dados.
    """
    print(f"Iniciando scraping para: {course_url}")

    try:
        response = requests.get(course_url, timeout=30)
        response.raise_for_status() 
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar a URL {course_url}: {e}")
        return 

    soup = BeautifulSoup(response.content, 'html.parser')


    curso_obj = None
    curso_nome_element = soup.find('tr', class_='card-title') 
    if curso_nome_element:
        curso_nome = curso_nome_element.text.strip().split('-')[0].strip()
        curso_obj, created = Curso.objects.get_or_create(nome=curso_nome)
        if created:
            print(f"  [Curso] '{curso_nome}' criado.")
        else:
            print(f"  [Curso] '{curso_nome}' já existe.")
    else:
        print("  [AVISO] Não foi possível encontrar o nome do curso na página. Ignorando associação com Curso.")

    
    all_tr_elements = soup.find_all('tr')
    
    processed_entries_count = 0
    
    for tr in all_tr_elements:
        
        professor_td = tr.find('td', class_='col_Professor zw-rgrid-detail')
        
        if professor_td: 
            processed_entries_count += 1
            

            professor_nome = professor_td.text.strip()
            
            if professor_nome.lower() in ["a definir", "indefinido", "vazio", ""]:
                professor_nome = None 


            disciplina_codigo = None
            disciplina_nome = None
            
            
            disciplina_codigo_td = tr.find('td', {'data-th': 'Código'})
            disciplina_nome_td = tr.find('td', {'data-th': 'Disciplina'}) 

            if disciplina_codigo_td:
                disciplina_codigo = disciplina_codigo_td.text.strip()
            if disciplina_nome_td:
                disciplina_nome = disciplina_nome_td.text.strip()
            
            if not disciplina_codigo or not disciplina_nome:
                all_tds_in_tr = tr.find_all('td')
                
                
                if len(all_tds_in_tr) >= 2:
                    disciplina_codigo = all_tds_in_tr[0].text.strip() if not disciplina_codigo else disciplina_codigo
                    disciplina_nome = all_tds_in_tr[1].text.strip() if not disciplina_nome else disciplina_nome
                    
                    if not re.match(r'^[A-Z0-9]{3,7}$', disciplina_codigo):
                        disciplina_codigo = None

            
            professor_obj = None
            if professor_nome:
                professor_obj, created_prof = Professor.objects.get_or_create(nome=professor_nome)
                if created_prof:
                    print(f"    [Professor] '{professor_nome}' adicionado.")
                
            if disciplina_codigo and disciplina_nome:
                disciplina_obj, created_disc = Disciplina.objects.get_or_create(
                    codigo=disciplina_codigo,
                    defaults={'nome': disciplina_nome}
                )
                if created_disc:
                    print(f"    [Disciplina] '{disciplina_codigo} - {disciplina_nome}' criada.")
                elif disciplina_obj.nome != disciplina_nome:
                    
                    disciplina_obj.nome = disciplina_nome
                    disciplina_obj.save()
                    print(f"    [Disciplina] '{disciplina_codigo}' nome atualizado para '{disciplina_nome}'.")

                if professor_obj and disciplina_obj:
                    if not disciplina_obj.professores.filter(id=professor_obj.id).exists():
                        disciplina_obj.professores.add(professor_obj)
                        print(f"      [Associação] Professor '{professor_obj.nome}' associado à Disciplina '{disciplina_obj.nome}'.")
                
                if curso_obj and disciplina_obj:
                    if not curso_obj.disciplinas.filter(id=disciplina_obj.id).exists():
                        curso_obj.disciplinas.add(disciplina_obj)
                        print(f"      [Associação] Disciplina '{disciplina_obj.nome}' associada ao Curso '{curso_obj.nome}'.")
            
            else:
                print(f"  [AVISO] Dados incompletos para Disciplina (Código: {disciplina_codigo}, Nome: {disciplina_nome}). Pulando.")
        
    print(f"Scraping finalizado. {processed_entries_count} entradas de aula/professor processadas.")
    if processed_entries_count == 0:
        print("  [ALERTA CRÍTICO] Nenhuma <tr> de aula/professor foi encontrada com os seletores atuais.")
        print("  Por favor, verifique se a URL está correta e inspecione o HTML da página (F12) novamente.")
        print("  Ajuste 'all_tr_elements = soup.find_all('tr')' e os seletores dentro do loop.")