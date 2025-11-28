# Arquivo: core/management/commands/importar_disciplinas.py (Final)

from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from core.models import Disciplina 
import requests
from bs4 import BeautifulSoup
import re 

# --------------------------------------------------------------------------
# 🎯 PONTO DE ENTRADA: LISTA DE URLS DIRETAS FORNECIDAS PELO USUÁRIO
# --------------------------------------------------------------------------
DISCIPLINA_URLS = [
    'https://www.puc-rio.br/ensinopesq/ccg/administracao.html#curso',
    'https://www.puc-rio.br/ensinopesq/ccg/arquitetura.html#curso',
    'https://www.puc-rio.br/ensinopesq/ccg/artes_cenicas.html#curso',
    'https://www.puc-rio.br/ensinopesq/ccg/ciencia_computacao.html#curso',
    'https://www.puc-rio.br/ensinopesq/ccg/ciencias_biologicas_bacharelado.html',
    'https://www.puc-rio.br/ensinopesq/ccg/economia.html#curso',
    'https://www.puc-rio.br/ensinopesq/ccg/ciencias_sociais_bacharelado.html',
    'https://www.puc-rio.br/ensinopesq/ccg/comunicacao.html#curso',
    'https://www.puc-rio.br/ensinopesq/ccg/design.html#curso',
    'https://www.puc-rio.br/ensinopesq/ccg/direito.html#curso',
    'https://www.puc-rio.br/ensinopesq/ccg/eng_ambiental.html#curso',
    'https://www.puc-rio.br/ensinopesq/ccg/eng_civil.html#curso',
    'https://www.puc-rio.br/ensinopesq/ccg/eng_computacao.html#curso',
    'https://www.puc-rio.br/ensinopesq/ccg/eng_automacao.html#curso',
    'https://www.puc-rio.br/ensinopesq/ccg/eng_eletrica.html#curso',
    'https://www.puc-rio.br/ensinopesq/ccg/eng_nanotecnologia.html#periodo_2023',
    'https://www.puc-rio.br/ensinopesq/ccg/eng_mecanica.html#curso',
    'https://www.puc-rio.br/ensinopesq/ccg/eng_producao.html#curso',
    'https://www.puc-rio.br/ensinopesq/ccg/eng_quimica.html#curso',
    'https://www.puc-rio.br/ensinopesq/ccg/estudos_de_midia.html#periodo_1',
    'https://www.puc-rio.br/ensinopesq/ccg/filosofia_bacharelado.html',
    'https://www.puc-rio.br/ensinopesq/ccg/filosofia_bacharelado.html', # Duplicada, mas OK
    'https://www.puc-rio.br/ensinopesq/ccg/fisica.html#curso',
    'https://www.puc-rio.br/ensinopesq/ccg/historia_bacharelado.html',
    'https://www.puc-rio.br/ensinopesq/ccg/geografia_bacharelado.html',
    'https://www.puc-rio.br/ensinopesq/ccg/comunicacao_jornalismo2.html#periodo_1',
    'https://www.puc-rio.br/ensinopesq/ccg/letras_port-ing.html#periodo_2012',
    'https://www.puc-rio.br/ensinopesq/ccg/matematica.html#periodo_2025',
    'https://www.puc-rio.br/ensinopesq/ccg/neurociencias.html#curso',
    'https://www.puc-rio.br/ensinopesq/ccg/matematica.html#periodo_2023',
    'https://www.puc-rio.br/ensinopesq/ccg/nutricao.html#curso',
    'https://www.puc-rio.br/ensinopesq/ccg/pedagogia.html#curso',
    'https://www.puc-rio.br/ensinopesq/ccg/psicologia.html#curso',
    'https://www.puc-rio.br/ensinopesq/ccg/quimica.html#curso',
    'https://www.puc-rio.br/ensinopesq/ccg/rel_internacionais.html#curso',
    'https://www.puc-rio.br/ensinopesq/ccg/servico_social.html#curso',
    'https://www.puc-rio.br/ensinopesq/ccg/sistemas_informacao.html#curso',
    'https://www.puc-rio.br/ensinopesq/ccg/teologia.html#curso'
]
# --------------------------------------------------------------------------


class Command(BaseCommand):
    help = 'Importa disciplinas de uma lista de URLs fixas (Scraping Direto de Tabelas).'

    def handle(self, *args, **options):
        self.stdout.write("Iniciando scraping direto das grades curriculares...")
        
        disciplinas_criadas = 0
        
        for url_disciplinas in DISCIPLINA_URLS:
            self.stdout.write(f"\n-> Processando URL: {url_disciplinas}")
            
            try:
                # NÍVEL 3: ACESSAR E EXTRAIR A TABELA DE DISCIPLINAS
                response_disciplinas = requests.get(url_disciplinas)
                response_disciplinas.raise_for_status()
                soup_disciplinas = BeautifulSoup(response_disciplinas.content, 'html.parser')
                
                # Seleciona TODAS as linhas de tabela (TR) dentro do bloco principal (#conteudo)
                # Esta é a lógica de extração da Imagem 3 que funciona para a tabela.
                disciplina_elements = soup_disciplinas.select('#conteudo table tr')
                
                # Pular a primeira linha (cabeçalho da tabela)
                disciplina_data_rows = disciplina_elements[1:] 

                if not disciplina_data_rows:
                    self.stdout.write(self.style.WARNING(f"  [AVISO] Nenhuma linha de dados encontrada na tabela. Pulando URL."))
                    continue


                for row in disciplina_data_rows:
                    cells = row.find_all('td')
                    
                    # Garante que a linha tem dados suficientes (Código e Nome)
                    if len(cells) >= 2:
                        
                        # Extração da Célula 1 (Código, ex: ARQ1101)
                        codigo_raw = cells[0].text.strip()
                        
                        # Extração da Célula 2 (Nome da Disciplina)
                        nome_disciplina = cells[1].text.strip()
                        
                        # Validação: Garante que o código é válido (letras+números)
                        if len(codigo_raw) >= 5 and codigo_raw[0].isalpha():
                            codigo = codigo_raw.replace(' ', '') 
                            
                            # Salvar no Model
                            try:
                                obj, created = Disciplina.objects.get_or_create(
                                    nome=nome_disciplina,
                                    defaults={'codigo': codigo}
                                )
                                
                                if created:
                                    disciplinas_criadas += 1
                                    self.stdout.write(self.style.SUCCESS(f'     [OK] {codigo} - {nome_disciplina}'))
                            except IntegrityError:
                                # Captura o erro UNIQUE constraint failed
                                self.stdout.write(self.style.WARNING(f'     [AVISO] {codigo} já existe. Ignorando.'))
                                continue
                    
            except requests.exceptions.RequestException as e:
                self.stdout.write(self.style.ERROR(f'Erro de conexão/HTTP ao acessar {url_disciplinas}: {e}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Ocorreu um erro na extração de {url_disciplinas}: {e}'))
                
        self.stdout.write(f"\n--- Processo Concluído ---")
        self.stdout.write(self.style.SUCCESS(f'{disciplinas_criadas} novas disciplinas importadas com sucesso!'))