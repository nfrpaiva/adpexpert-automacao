# Aprovação automática de apontamento de regras no ADP Expert
## Motivação
Durante o trabalho em home-office os colaboradores precisam marcar o ponto diariamente 
na ferramenta ADP Web.

Com esse script posso fazer a aprovação dos ajustes automáticamente desde que algumas condições sejam atendidas.
- O colaborador deve ter trabalhado no máximo 8:00 (+1:15 de almoço)
- Não pode ser um ajuste nos finais de semana.
## Instalação

### Requerimentos
- Python
- [Chromedrive](https://chromedriver.chromium.org/downloads) 
- [Selenium](https://www.selenium.dev/documentation/en/)

### Instalar dependências
```python
pip install -r requirements.txt
```

### Criar arquivo .env com credenciais de acesso
```bash
# Executar na pasta do projeto
echo "ADP_USER={SEU_USUÁRIO}" >> .env
echo "ADP_PASSWORD={SUA_SENHA}" >> .env
```

## Executar
```python
python3 aprovacao_automatica.py
```