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

    # --- 1. Acessa a URL e faz o parse do HTML ---
    try:
        response = requests.get(course_url, timeout=30) # Aumentei o timeout por segurança
        response.raise_for_status() # Levanta um erro para respostas HTTP de status ruim (4xx ou 5xx)
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar a URL {course_url}: {e}")
        return # Sai da função se houver erro na requisição

    soup = BeautifulSoup(response.content, 'html.parser')

    # --- 2. Extrai o nome do Curso (se disponível na página) ---
    # Inspecione o HTML para encontrar o elemento que contém o nome do curso.
    # Exemplo comum: um h4 ou h5 dentro de um painel/card
    curso_obj = None
    curso_nome_element = soup.find('tr', class_='card-title') # OU <h3 class="panel-title">, etc.
    if curso_nome_element:
        # Tenta pegar só o nome do curso, removendo o código ou outras informações
        curso_nome = curso_nome_element.text.strip().split('-')[0].strip()
        curso_obj, created = Curso.objects.get_or_create(nome=curso_nome)
        if created:
            print(f"  [Curso] '{curso_nome}' criado.")
        else:
            print(f"  [Curso] '{curso_nome}' já existe.")
    else:
        print("  [AVISO] Não foi possível encontrar o nome do curso na página. Ignorando associação com Curso.")

    # --- 3. Itera sobre cada linha (<tr>) que representa uma aula/disciplina ---
    # Seu inspetor de elementos confirmou que <tr> é o separador.
    # Vamos encontrar todas as <tr> que contêm dados relevantes.
    # Pode ser que a tabela tenha uma classe específica, ou que as <tr>s interessantes
    # estejam dentro de um <tbody> ou <div> com ID/classe.
    
    # Exemplo: Procurar por todas as <tr> dentro de uma <tbody> principal
    # Você PODE precisar ser mais específico:
    # Por exemplo: `soup.find('table', id='horariosTabela').find('tbody').find_all('tr')`
    all_tr_elements = soup.find_all('tr')
    
    processed_entries_count = 0
    
    for tr in all_tr_elements:
        # Verifica se esta <tr> contém as colunas que nos interessam
        # (pelo menos a coluna do professor, que é a mais fácil de identificar)
        professor_td = tr.find('td', class_='col_Professor zw-rgrid-detail')
        
        if professor_td: # Se encontrou a célula do professor, esta <tr> é relevante
            processed_entries_count += 1
            
            professor_nome = professor_td.text.strip()
            
            # Evitar "A Definir", "Vazio" ou outros placeholders
            if professor_nome.lower() in ["a definir", "indefinido", "vazio", ""]:
                professor_nome = None # Não consideramos como um professor real

            # --- Extrai a Disciplina e o Código ---
            # Aqui é mais complexo, pois os seletores para disciplina/código podem variar.
            # Geralmente, em sites de grade, o código e nome da disciplina
            # estão em <td>s vizinhas na mesma <tr>.

            disciplina_codigo = None
            disciplina_nome = None
            
            # Vamos tentar encontrar outras <td> na mesma <tr>.
            # Exemplo: col_DisciplinaCodigo, col_DisciplinaNome
            # Inspecione a página para achar classes como 'col_Codigo', 'col_Disciplina'
            
            # Tentativa 1: Procurar td com 'data-th' como 'Disciplina' ou 'Código'
            disciplina_codigo_td = tr.find('td', {'data-th': 'Código'}) # Ou class_='col_Codigo'
            disciplina_nome_td = tr.find('td', {'data-th': 'Disciplina'}) # Ou class_='col_Disciplina'

            if disciplina_codigo_td:
                disciplina_codigo = disciplina_codigo_td.text.strip()
            if disciplina_nome_td:
                disciplina_nome = disciplina_nome_td.text.strip()
            
            # Se não encontrou por data-th, pode estar em uma coluna genérica
            if not disciplina_codigo or not disciplina_nome:
                # Vamos tentar pegar todas as TDs e inferir
                all_tds_in_tr = tr.find_all('td')
                
                # CHUTE: Disciplina e Código podem estar na primeira ou segunda TD
                # Se o nome e o código estiverem em TDs adjacentes, você precisará
                # ajustar os índices abaixo com base na sua inspeção (F12).
                if len(all_tds_in_tr) >= 2:
                    # Exemplo: <td> Código </td> <td> Nome da Disciplina </td>
                    disciplina_codigo = all_tds_in_tr[0].text.strip() if not disciplina_codigo else disciplina_codigo
                    disciplina_nome = all_tds_in_tr[1].text.strip() if not disciplina_nome else disciplina_nome
                    
                    # Regex para garantir que o que pegamos parece um código
                    if not re.match(r'^[A-Z0-9]{3,7}$', disciplina_codigo):
                        disciplina_codigo = None # Não parece um código válido

            # --- 4. Salva (ou atualiza) os dados no banco de dados ---
            
            # 4.1. Salva o Professor (se encontrado)
            professor_obj = None
            if professor_nome:
                professor_obj, created_prof = Professor.objects.get_or_create(nome=professor_nome)
                if created_prof:
                    print(f"    [Professor] '{professor_nome}' adicionado.")
                # else: print(f"    [Professor] '{professor_nome}' já existe.")

            # 4.2. Salva a Disciplina (se encontrado código e nome) e associa
            if disciplina_codigo and disciplina_nome:
                disciplina_obj, created_disc = Disciplina.objects.get_or_create(
                    codigo=disciplina_codigo,
                    defaults={'nome': disciplina_nome}
                )
                if created_disc:
                    print(f"    [Disciplina] '{disciplina_codigo} - {disciplina_nome}' criada.")
                elif disciplina_obj.nome != disciplina_nome:
                    # Se a disciplina já existe, mas o nome é diferente (pode ser um erro ou atualização)
                    # Você decide se quer atualizar o nome ou manter o original
                    disciplina_obj.nome = disciplina_nome
                    disciplina_obj.save()
                    print(f"    [Disciplina] '{disciplina_codigo}' nome atualizado para '{disciplina_nome}'.")
                # else: print(f"    [Disciplina] '{disciplina_codigo}' já existe.")

                # 4.3. Associa Professor à Disciplina (se ambos existem)
                if professor_obj and disciplina_obj:
                    if not disciplina_obj.professores.filter(id=professor_obj.id).exists():
                        disciplina_obj.professores.add(professor_obj)
                        print(f"      [Associação] Professor '{professor_obj.nome}' associado à Disciplina '{disciplina_obj.nome}'.")
                
                # 4.4. Associa Disciplina ao Curso (se ambos existem)
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