# Exercício ATS12 — Integração Contínua com GitHub Actions

Projeto de exemplo do exercício ATS12: API FastAPI, testes com Pytest, workflow de CI com matriz Python 3.10/3.11/3.12 e teste de integração usando `curl`.

## Estrutura

```text
ATS12_CI_GitHub_Actions/
├── .github/
│   └── workflows/
│       └── ci.yml
├── tests/
│   └── test_main.py
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

## 1. Executar localmente

Requer Python instalado. No terminal, dentro da pasta do projeto:

```bash
python -m venv .venv
```

Ative o ambiente virtual:

- Windows PowerShell: `.venv\\Scripts\\Activate.ps1`
- Windows CMD: `.venv\\Scripts\\activate.bat`
- Linux/macOS: `source .venv/bin/activate`

Instale as dependências e execute os testes:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
pytest -v
```

Inicie a API:

```bash
fastapi run main.py --port 8000
```

Em outro terminal, teste as rotas:

```bash
curl http://localhost:8000/
curl http://localhost:8000/somar/10/20
curl http://localhost:8000/multiplicar/2/2
```

Respostas esperadas:

- `/`: `{"mensagem":"API funcionando"}`
- `/somar/10/20`: `{"resultado":30}`
- `/multiplicar/2/2`: `{"resultado":4}`

## 2. Criar o repositório remoto e enviar o projeto

Crie um repositório vazio no GitHub. Depois, na pasta do projeto:

```bash
git init
git add .
git commit -m "Configura API e pipeline CI do ATS12"
git branch -M main
git remote add origin https://github.com/SEU-USUARIO/SEU-REPOSITORIO.git
git push -u origin main
```

Substitua a URL de exemplo pela URL real do seu repositório. Abra a aba **Actions** e confira as execuções. O workflow testa as três versões do Python.

## 3. Simular o erro de soma (Parte 2)

Faça essa alteração apenas para demonstrar a falha solicitada pelo PDF. Em `main.py`, troque temporariamente `a + b` por `a - b`:

```python
@app.get("/somar/{a}/{b}")
def somar(a: int, b: int):
    return {"resultado": a - b}
```

Envie a alteração para o GitHub:

```bash
git add main.py
git commit -m "Simula erro intencional na soma"
git push
```

Na aba **Actions**, abra a execução que falhou e expanda **Rodar Testes**. Para o teste `/somar/10/20`, o Pytest deve indicar uma falha de asserção: esperava `{"resultado": 30}`, mas recebeu `{"resultado": -10}`. A formatação exata do log pode variar conforme a versão do Pytest.

Depois da demonstração, restaure `return {"resultado": a + b}` e envie a correção.

## 4. Pull Request e proteção da branch main (Parte 3)

1. Confirme que a branch `main` está corrigida e que o CI passou.
2. No GitHub, abra **Settings → Branches** ou **Rulesets** e crie uma regra para `main`.
3. Exija Pull Request antes do merge e exija que o status check `verificar-api` passe.
4. Crie uma branch de funcionalidade:

   ```bash
   git checkout -b feature-multiplicacao
   ```

5. A rota `/multiplicar/{a}/{b}` e o teste correspondente já estão implementados neste projeto.
6. Para reproduzir a falha pedida pelo exercício, altere temporariamente em `tests/test_main.py` a expectativa de `4` para `5` no teste de multiplicação. Faça commit e push:

   ```bash
   git add tests/test_main.py
   git commit -m "Simula teste de multiplicação incorreto"
   git push -u origin feature-multiplicacao
   ```

7. Abra um Pull Request de `feature-multiplicacao` para `main`. O CI deverá falhar e, se as regras estiverem configuradas corretamente, bloquear o merge.
8. Corrija a expectativa para `4`, faça novo commit e push na mesma branch. Aguarde todos os checks ficarem verdes e então faça o merge.

**Importante:** não mantenha o teste propositalmente incorreto no código final. O projeto entregue está com o teste corrigido.

## 5. Matriz de versões Python (Parte 4)

O arquivo `.github/workflows/ci.yml` já contém:

```yaml
strategy:
  fail-fast: false
  matrix:
    python-version: ["3.10", "3.11", "3.12"]
```

A configuração `python-version: ${{ matrix.python-version }}` faz o GitHub Actions executar o job para cada versão da matriz, sem duplicar o workflow.

## 6. Teste de integração (Parte 5)

Depois do Pytest, o workflow inicia a API em segundo plano e usa `curl --fail` para verificar as rotas `/` e `/somar/10/20`. Se o servidor não iniciar ou uma requisição retornar status HTTP de erro, o passo falha. O processo é encerrado ao final do passo.

## Observações

- O nome do job é `verificar-api`, conforme solicitado no PDF. Ao configurar a proteção da branch, selecione o status check correspondente exibido pelo GitHub.
- A proteção de branch deve ser configurada nas configurações do repositório; ela não é ativada automaticamente pelo arquivo YAML.
- O workflow executa em cada `push` para `main` e branches com prefixo `feature-`, e em Pull Requests direcionados a `main`.
- As falhas intencionais são etapas de demonstração. O estado final entregue contém soma correta e testes aprovados.
