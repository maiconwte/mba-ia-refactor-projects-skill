# code-smells-project

API de E-commerce em Python/Flask (estrutura MVC) usada como entrada do desafio `refactor-arch`.

## Como rodar

```bash
pip install -r requirements.txt
python app.py
```

Variáveis de ambiente opcionais: `SECRET_KEY`, `DEBUG`, `ADMIN_TOKEN` (padrão `dev-admin-token`), `DB_PATH`.

A aplicação sobe em `http://localhost:5000`. O banco SQLite (`loja.db`) é criado automaticamente no primeiro boot, já com produtos e usuários de exemplo (senhas armazenadas com hash SHA-256).
