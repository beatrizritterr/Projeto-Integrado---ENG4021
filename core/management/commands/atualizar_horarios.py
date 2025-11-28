from django.core.management.base import BaseCommand, CommandError
from core.scraping.microhorario import run_microhorario_scraping_for_course 

class Command(BaseCommand):
    help = 'Executa o scraping (via Selenium) do MicroHorário e atualiza o banco.'

    def add_arguments(self, parser):
        parser.add_argument('--url', type=str, required=True, help='URL completa do curso.')

    def handle(self, *args, **kwargs):
        course_url = kwargs['url']
        if not course_url.startswith('http'):
            raise CommandError("A URL deve começar com http:// ou https://")
        
        self.stdout.write(self.style.NOTICE(f"Iniciando robô para: {course_url}"))
        try:
            run_microhorario_scraping_for_course(course_url)
            self.stdout.write(self.style.SUCCESS('Comando finalizado com sucesso!'))
        except Exception as e:
            raise CommandError(f"Erro fatal no comando: {e}")