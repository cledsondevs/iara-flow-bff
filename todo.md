## Tarefas

### Fase 1: Analisar arquivos de scraping e sentimentos e planejar integração
- [x] Analisar `apple_store_scraping_real.py`
- [x] Analisar `google_play_scraping_real.py`
- [x] Analisar `sentiment_analysis_real.py`

### Fase 2: Criar estrutura de diretórios e mover arquivos para o novo módulo
- [x] Criar diretórios `app/modules/scraping` e `app/modules/sentiment`
- [x] Mover `apple_store_scraping_real.py` para `app/modules/scraping/apple_store.py`
- [x] Mover `google_play_scraping_real.py` para `app/modules/scraping/google_play.py`
- [x] Mover `sentiment_analysis_real.py` para `app/modules/sentiment/analysis.py`
- [x] Criar arquivos `__init__.py` nos novos diretórios

### Fase 3: Adaptar e integrar o código de scraping e análise de sentimentos
- [x] Atualizar `app/modules/sentiment/analysis.py` para usar a chave Gemini e importar `genai`
- [x] Instalar dependências (`google-generativeai`, `google-play-scraper`)
- [x] Atualizar `requirements.txt`

### Fase 4: Criar novas rotas de API para scraping e análise de sentimentos
- [x] Criar blueprint para rotas de scraping
- [x] Implementar rota POST /api/scraping/google-play/{id}
- [x] Implementar rota POST /api/scraping/apple-store/{id}
- [x] Criar blueprint para rotas de análise de sentimentos
- [x] Implementar rota POST /api/sentiment/analyze

### Fase 5: Remover a chamada externa e atualizar serviços existentes
- [x] Identificar e remover chamadas para `https://bff-analyse.vercel.app/api/` em `review_collector_service.py`
- [x] Atualizar `review_collector_service.py` para usar os novos módulos internos de scraping
- [x] Atualizar `review_agent_service.py` para usar o novo módulo interno de análise de sentimentos
- [x] Adicionar a chave do Gemini nas configurações (`app/config/settings.py`)

### Fase 6: Testar as novas funcionalidades da API
- [ ] Criar/atualizar script de teste para as novas rotas de scraping
- [ ] Criar/atualizar script de teste para a nova rota de análise de sentimentos
- [ ] Executar os testes

### Fase 7: Atualizar o repositório Git
- [ ] Adicionar e commitar as alterações
- [ ] Subir para o GitHub


