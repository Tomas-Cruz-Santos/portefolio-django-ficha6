import json
import os
from django.conf import settings
from django.core.management.base import BaseCommand

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from portfolio.models import TFC


class Command(BaseCommand):
    help = 'Carrega TFCs do JSON'

    def handle(self, *args, **kwargs):
        path = os.path.join(settings.BASE_DIR, 'data', 'tfcs_2025.json')

        if not os.path.exists(path):
            self.stdout.write(self.style.ERROR('Ficheiro JSON não encontrado!'))
            return

        with open(path, encoding='utf-8') as f:
            dados = json.load(f)

        count = 0

        for item in dados:
            titulo = item.get('titulo')

            if not titulo:
                continue

            tfc, created = TFC.objects.get_or_create(
                titulo=titulo,
                defaults={
                    'autor': item.get('autor'),
                    'ano': item.get('ano'),
                    'descricao': item.get('descricao', ''),
                }
            )

            if created:
                count += 1
                self.stdout.write(self.style.SUCCESS(f"Criado: {titulo}"))
            else:
                self.stdout.write(self.style.WARNING(f"Já existe: {titulo}"))

        self.stdout.write(self.style.SUCCESS(f'\nTotal de novos TFCs: {count}'))