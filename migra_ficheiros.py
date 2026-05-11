import os
import django
from django.core.files import File
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings') 
django.setup()

from portfolio.models import Docente, Tecnologia, Projeto, TFC, MakingOf

MEDIA_ROOT = settings.BASE_DIR

modelos_para_migrar = [
    (Docente, 'foto'),
    (Tecnologia, 'logo'),
    (Projeto, 'foto'),
    (TFC, 'imagem'),
    (MakingOf, 'fotos'),
]

for modelo, campo in modelos_para_migrar:
    print(f"--- Migrando {modelo.__name__} ---")
    
    for obj in modelo.objects.all():
       
        ficheiro_campo = getattr(obj, campo)
        
        if ficheiro_campo and ficheiro_campo.name:
            
            local_path = os.path.join(MEDIA_ROOT, ficheiro_campo.name)
            
            if os.path.exists(local_path):
                with open(local_path, 'rb') as f:
                    ficheiro_campo.save(
                        os.path.basename(local_path),
                        File(f),
                        save=True
                    )
                print(f"Migrado {modelo.__name__}: {obj}")
            else:
                print(f"Ficheiro não encontrado: {local_path}")