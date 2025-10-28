
<h1 align="center">📌 Desafio Hubbi - Marketplace de Autopeças </h1>

<p align="center">
  <img src="http://img.shields.io/static/v1?label=License&message=CC%20BY-NC-SA%204.0&color=A20606&style=for-the-badge"/>
  <img src="http://img.shields.io/static/v1?label=Python&message=3.13%2B&color=A20606&style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/static/v1?label=Django&message=Framework&color=A20606&style=for-the-badge&logo=django"/>
</p>

---

Sistema de marketplace para compra e venda de autopeças, com tarefas assíncronas via **Celery**, **PostgreSQL** como banco de dados e **Redis** como broker/cache.  
Containerizado com **Docker Compose**, para rodar em ambiente local ou de produção.

---

## 🧭 Sumário

- [Características](#-características)
- [Tecnologias](#-tecnologias)
- [Pré-requisitos](#-pré-requisitos)
- [Instalação com Docker (recomendado)](#-instalação-com-docker-recomendado)
- [Configuração do Ambiente (.env)](#-configuração-do-ambiente-env)
- [Execução e Migrations](#-execução-e-migrations)
- [Acessando a Aplicação](#-acessando-a-aplicação)
- [Executando Tarefas Assíncronas](#-executando-tarefas-assíncronas)
- [Rodando Testes](#-rodando-testes)
- [Arquitetura do Projeto](#-arquitetura-do-projeto)
- [Licença](#-licença)
- [Autor](#-autor)

---

## 🚀 Características

- CRUD de peças (criação, listagem, edição, exclusão).
- Upload de arquivos **CSV** para cadastro em massa de produtos.
- Tarefas assíncronas com **Celery**:
  - Processamento de CSV.
  - Reposição automática de estoque.
- Autenticação com **JWT**.

---

## 🧰 Tecnologias

| Componente | Versão | Uso |
|-------------|--------|------|
| **Python** | 3.13 | Linguagem principal |
| **Django** | 5.2 | Framework backend |
| **Django REST Framework** | 3.x | Criação da API REST |
| **PostgreSQL** | 15 | Banco de dados relacional |
| **Redis** | 7 | Cache e broker Celery |
| **Celery** | 5 | Execução de tarefas assíncronas |
| **Docker Compose** | 3+ | Orquestração dos serviços |

---

## 🧱 Pré-requisitos

Antes de iniciar, instale em seu sistema:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- (Opcional) [Git](https://git-scm.com/) para clonar o repositório.


---

## 🐳 Instalação com Docker (recomendado)

### 1️⃣ Clonar o repositório

```bash
git clone https://github.com/kakanetwork/desafio-backend-hubbi.git
cd desafio-backend-hubbi
```

### 2️⃣ Criar o arquivo `.env`

```bash
cp .env.example .env
```

### 3️⃣ Subir os containers

```bash
docker compose up -d --build
```

Isso iniciará:
- `web` → servidor Django
- `db` → PostgreSQL
- `redis` → broker/cache
- `celery_worker` → worker de tarefas
- `celery_beat` → agendador de tarefas

### 4️⃣ Aplicar as migrations

```bash
docker compose exec web python manage.py migrate
```

### 5️⃣ Criar um superusuário

```bash
docker compose exec web python manage.py createsuperuser
```

---

## ⚙️ Configuração do Ambiente (.env)

Crie um arquivo `.env` na raiz do projeto com:

```env
# Banco de Dados
DB_NAME=marketplace
DB_USER=postgres
DB_PASSWORD=123456
DB_HOST=db
DB_PORT=5432

# Redis
REDIS_HOST=redis
REDIS_PORT=6379

# Django
SECRET_KEY=change-me-in-prod
DJANGO_SETTINGS_MODULE=marketplace.settings
DEBUG=True
```

> ⚠️ **oBs:** Dentro do Docker, use `db` e `redis` como hosts e não `localhost`, ou a rede de containers não será reconhecida.

---

## ▶️ Execução e Migrations

Após subir os containers e aplicar as migrations, o sistema estará pronto.

Para verificar os logs:

```bash
docker compose logs -f web
```

Para acessar o shell do Django:

```bash
docker compose exec web python manage.py shell
```

---

## 🌐 Acessando a Aplicação

- **API REST:** [`http://localhost:8000/api/`](http://localhost:8000/api/)
- **Painel Admin:** [`http://localhost:8000/admin/`](http://localhost:8000/admin/)

Autenticação via JWT:
```bash
POST /api/token/
{
  "username": "admin",
  "password": "senha"
}
```

Depois envie `Authorization: Bearer <token>` no header.

---

## ⏳ Executando Tarefas Assíncronas

O projeto usa **Celery + Redis**.

Os workers e beat são iniciados automaticamente via `docker`.

Para testar manualmente:
```bash
docker compose exec web celery -A marketplace worker -l info
docker compose exec web celery -A marketplace beat -l info
```

Tasks principais:
- `apps.estoque.tasks.celery_csv(csv_content)` — Processa CSV e atualiza peças.
- `apps.estoque.tasks.repor_estoque()` — Reforça peças com estoque baixo.

---

## 🧪 Rodando Testes

Execute dentro do container principal (`web`):

```bash
docker compose exec web pytest -q --disable-warnings
```



---

## 🧩 Arquitetura do Projeto

```
├── apps/
│   ├── estoque/        # Lógica de peças, tasks e CSV
│   └── usuarios/       # Autenticação e controle de usuários
├── marketplace/        # Configurações Django + Celery
├── manage.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## 📜 Licença

Licenciado sob **Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)**.  
Você pode compartilhar e adaptar para fins **não comerciais**, desde que cite a autoria original.

---

## 👨‍💻 Autor

<div align="left">
  <a href="https://github.com/kakanetwork">
    <img src="https://img.shields.io/badge/GitHub%20-%20KakaNetwork-4d080e?style=for-the-badge&logo=github&logoColor=white&color=A20606" alt="GitHub"/>
  </a>
  <a href="https://www.linkedin.com/in/kalvinklein/">
    <img src="https://img.shields.io/badge/LinkedIn%20-%20Kalvin%20Klein-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn"/>
  </a>
  <a href="mailto:kalvimklain@gmail.com">
    <img src="https://img.shields.io/badge/Email%20-%20Contato-D14836?style=for-the-badge&logo=gmail&logoColor=white" alt="Email"/>
  </a>
</div>

---
