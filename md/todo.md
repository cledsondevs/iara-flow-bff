# TODO - Reorganização Estrutura Modular

## Problemas Identificados
- [x] Duplicação entre pastas `src/` e `app/`
- [x] Duas implementações diferentes do main.py
- [x] Imports conflitantes entre as duas estruturas
- [x] MemoryService duplicado em ambas as estruturas

## Ações a Realizar
- [x] Consolidar toda a estrutura na pasta `app/`
- [x] Remover pasta `src/` duplicada
- [x] Atualizar imports para usar apenas `app/`
- [x] Modularizar os chats e ajustar importsuncionando
- [ ] Atualizar arquivos de configuração (requirements.txt, etc.)
- [ ] Testar a aplicação
- [ ] Criar nova branch e fazer commit

## Estrutura Final Desejada
```
src/
├── main.py (arquivo principal)
├── services/
├── routes/
├── config/
├── utils/
└── static/
```

