from django.core.management.base import BaseCommand, CommandError
from core.scraping.microhorario import run_microhorario_scraping_for_course # Importa a função de scraping
from core.models import Professor, Disciplina, Curso # Para poder listar cursos, se quiser


class Command(BaseCommand):
    help = 'Executa o scraping do MicroHorário da PUC para um curso específico e atualiza o banco de dados.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--url',
            type=str,
            help='A URL completa da página do MicroHorário para o curso específico a ser scrapeado.',
            required=True
        )
        # Opcional: Adicionar um argumento para limpar o banco antes de scrapear
        parser.add_argument(
            '--clear-data',
            action='store_true',
            help='Limpa todos os Professores, Disciplinas e Cursos antes de rodar o scraping.',
        )

    def handle(self, *args, **kwargs):
        course_url = kwargs['url']
        clear_data = kwargs['clear_data']

        if not course_url.startswith('http'):
            raise CommandError("A URL fornecida deve ser uma URL completa (ex: 'https://...').")

        if clear_data:
            self.stdout.write(self.style.WARNING("Limpando dados existentes (Professores, Disciplinas, Cursos)..."))
            Professor.objects.all().delete()
            Disciplina.objects.all().delete()
            Curso.objects.all().delete()
            self.stdout.write(self.style.SUCCESS("Dados limpos com sucesso."))

        self.stdout.write(self.style.NOTICE(f"Iniciando atualização de horários para a URL: {course_url}"))

        try:
            run_microhorario_scraping_for_course(course_url) # Chama a função de scraping
            self.stdout.write(self.style.SUCCESS('Scraping concluído e banco de dados atualizado com sucesso!'))
        except Exception as e:
            raise CommandError(f"Ocorreu um erro durante o scraping: {e}")