# core/management/commands/atualizar_departamentos.py

from django.core.management.base import BaseCommand, CommandError
from core.scraping.departamentos import run_departamento_scraping
from selenium.webdriver.common.by import By 

class Command(BaseCommand):
    help = 'Executa o scraping de páginas de departamentos para extrair professores.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--urls', nargs='+', type=str, required=True,
            help='Uma ou mais URLs das páginas de departamento a serem scrapeadas.'
        )
        parser.add_argument(
            '--nomes', nargs='+', type=str,
            help='Nomes opcionais para os departamentos, na mesma ordem das URLs.'
        )
        parser.add_argument(
            '--layouts', nargs='+', type=str, required=True,
            help='Tipos de layout para cada URL (ex: eng_mecanica, matematica, fisica).'
        )
        parser.add_argument(
            '--selenium', action='store_true',
            help='Use Selenium para scraping (para sites com JavaScript).'
        )
        parser.add_argument(
            '--selenium_wait_selectors', nargs='+', type=str,
            help='Seletores para Selenium esperar (ex: "CSS:.container-professores"). Requer --selenium.'
        )

    def handle(self, *args, **kwargs):
        department_urls = kwargs['urls']
        department_names = kwargs['nomes'] if kwargs['nomes'] else []
        layout_types = kwargs['layouts']
        use_selenium = kwargs['selenium']
        selenium_wait_selectors_raw = kwargs['selenium_wait_selectors'] if kwargs['selenium_wait_selectors'] else []

        if len(layout_types) != len(department_urls):
            raise CommandError("O número de layouts deve corresponder ao número de URLs.")
        if len(department_names) > 0 and len(department_names) != len(department_urls):
            raise CommandError("O número de nomes de departamento deve corresponder ao número de URLs.")
        if use_selenium and len(selenium_wait_selectors_raw) > 0 and len(selenium_wait_selectors_raw) != len(department_urls):
             raise CommandError("O número de seletores de espera do Selenium deve corresponder ao número de URLs se fornecido.")
        if use_selenium and len(selenium_wait_selectors_raw) == 0:
             self.stdout.write(self.style.WARNING("Usando Selenium, mas nenhum seletor de espera foi fornecido. Pode causar TimeoutException."))
        
        by_map = {
            'ID': By.ID, 'NAME': By.NAME, 'XPATH': By.XPATH, 'LINK_TEXT': By.LINK_TEXT,
            'PARTIAL_LINK_TEXT': By.PARTIAL_LINK_TEXT, 'TAG_NAME': By.TAG_NAME,
            'CLASS_NAME': By.CLASS_NAME, 'CSS': By.CSS_SELECTOR
        }

        self.stdout.write(self.style.NOTICE(f"Iniciando atualização de professores de departamentos (Selenium: {use_selenium})."))

        for i, url in enumerate(department_urls):
            name = department_names[i] if i < len(department_names) else None
            layout = layout_types[i]
            
            selenium_wait_selector = None
            if use_selenium and i < len(selenium_wait_selectors_raw):
                parts = selenium_wait_selectors_raw[i].split(':', 1)
                if len(parts) == 2 and parts[0].upper() in by_map:
                    selector_type = by_map[parts[0].upper()]
                    selector_value = parts[1]
                    selenium_wait_selector = (selector_type, selector_value)
                else:
                    self.stdout.write(self.style.ERROR(f"Formato inválido para seletor de espera: '{selenium_wait_selectors_raw[i]}'. Ignorando para esta URL."))


            try:
                run_departamento_scraping(url, name, layout_type=layout, 
                                          use_selenium=use_selenium, 
                                          selenium_wait_selector=selenium_wait_selector)
                self.stdout.write(self.style.SUCCESS(f"Scraping de {url} (Layout {layout}) concluído!"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Erro ao scrapear {url} (Layout {layout}): {e}"))
                self.stdout.write(self.style.ERROR(f"  Detalhes do erro: {e}"))

        self.stdout.write(self.style.NOTICE("Scraping de departamentos finalizado."))