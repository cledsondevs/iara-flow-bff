import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.main import create_app

app = create_app()

print('Rotas registradas:')
for rule in app.url_map.iter_rules():
    if 'v2' in rule.rule or 'gemini' in rule.rule:
        print(f'{rule.methods} {rule.rule}')


