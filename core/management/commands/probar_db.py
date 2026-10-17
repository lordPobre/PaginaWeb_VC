"""Verifica la conexión a la base de datos y muestra su estado.

Uso:  python manage.py probar_db
"""
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import connection
from django.db.migrations.executor import MigrationExecutor


class Command(BaseCommand):
    help = 'Prueba la conexión a Postgres y lista migraciones pendientes.'

    def handle(self, *args, **opts):
        db = settings.DATABASES['default']
        motor = db['ENGINE'].rsplit('.', 1)[-1]
        self.stdout.write(f"Motor: {motor}")
        if motor == 'sqlite3':
            self.stdout.write(self.style.WARNING('Estás usando SQLite (no hay DATABASE_URL). Define DATABASE_URL para conectar a Postgres.'))
        else:
            self.stdout.write(f"Host: {db.get('HOST')}  ·  Base: {db.get('NAME')}  ·  Usuario: {db.get('USER')}")

        try:
            with connection.cursor() as cur:
                if motor == 'postgresql':
                    cur.execute('SELECT version(), current_database(), now()')
                    version, base, ahora = cur.fetchone()
                    self.stdout.write(self.style.SUCCESS(f'✓ Conectado a "{base}"'))
                    self.stdout.write(f'  {version.split(",")[0]}')
                    self.stdout.write(f'  Hora del servidor: {ahora}')
                else:
                    cur.execute('SELECT 1')
                    self.stdout.write(self.style.SUCCESS('✓ Conexión OK'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ No se pudo conectar: {e}'))
            self.stdout.write('  Revisa DATABASE_URL, que termine en ?sslmode=require y que la IP no esté bloqueada.')
            return

        ex = MigrationExecutor(connection)
        pendientes = ex.migration_plan(ex.loader.graph.leaf_nodes())
        if pendientes:
            self.stdout.write(self.style.WARNING(f'Hay {len(pendientes)} migraciones pendientes → ejecuta: python manage.py migrate'))
        else:
            self.stdout.write(self.style.SUCCESS('✓ Base de datos al día con las migraciones'))
