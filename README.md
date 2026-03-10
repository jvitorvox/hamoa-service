# MCP File Server

Servidor MCP (Model Context Protocol) em Python que permite ao ChatGPT (ou qualquer cliente MCP) acessar arquivos armazenados na pasta `/data` do repositório.

---

## Como funciona

O servidor expõe duas ferramentas via protocolo MCP:

| Ferramenta | Descrição |
|---|---|
| `list_files` | Lista todos os arquivos disponíveis em `/data` |
| `read_file(filename)` | Retorna o conteúdo de um arquivo específico |

---

## Estrutura do projeto

```
mcp-server/
├── data/               ← Coloque seus arquivos aqui
│   ├── exemplo.sql
│   └── exemplo.json
├── server.py           ← Código do servidor MCP
├── requirements.txt    ← Dependências Python
├── render.yaml         ← Configuração de deploy no Render
├── .gitignore
└── README.md
```

---

## Como rodar localmente

**1. Clone o repositório**
```bash
git clone https://github.com/seu-usuario/mcp-server.git
cd mcp-server
```

**2. Crie um ambiente virtual**
```bash
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows
```

**3. Instale as dependências**
```bash
pip install -r requirements.txt
```

**4. Inicie o servidor**
```bash
python server.py
```

O servidor estará disponível em `http://localhost:8000/mcp`.

---

## Como fazer deploy no Render

1. Faça push do repositório para o GitHub
2. Acesse [render.com](https://render.com) e crie uma conta
3. Clique em **New > Web Service**
4. Conecte seu repositório GitHub
5. O Render detectará o `render.yaml` automaticamente e configurará o deploy
6. Clique em **Deploy** — o servidor ficará disponível em uma URL pública

> O deploy é automático a cada `git push` para a branch principal.

---

## Como adicionar novos arquivos

Basta colocar qualquer arquivo dentro da pasta `/data`:

```
data/
├── minha_query.sql
├── relatorio.csv
├── config.json
└── notas.txt
```

Formatos suportados: `.sql`, `.csv`, `.json`, `.txt`, `.md`, `.yaml`, e qualquer arquivo de texto.

Depois do `git push`, o Render fará o redeploy automaticamente com os novos arquivos disponíveis.

---

## Exemplo de uso

Após conectar o servidor ao ChatGPT ou outro cliente MCP:

```
# Listar arquivos disponíveis
list_files()

# Resultado:
Arquivos disponíveis:
- exemplo.json
- exemplo.sql

# Ler um arquivo específico
read_file("exemplo.sql")

# Resultado:
=== exemplo.sql ===

SELECT id, nome, email ...
```

---

## Variáveis de ambiente

| Variável | Padrão | Descrição |
|---|---|---|
| `PORT` | `8000` | Porta em que o servidor escuta |

---

## Dependências

- [mcp](https://pypi.org/project/mcp/) — biblioteca oficial do Model Context Protocol
- [requests](https://pypi.org/project/requests/) — utilitário HTTP (disponível para extensões futuras)
