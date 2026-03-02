# PluViewAPI

API de monitoramento de dados meteorologicos IoT, construida com NestJS e Prisma.

## Pre-requisitos

- Node.js 20+
- PostgreSQL 16+ (ou Docker)
- npm

## Setup Rapido

### 1. Instalar dependencias

```bash
npm install
```

### 2. Configurar variaveis de ambiente

```bash
# Copie o arquivo de exemplo
cp .env.example .env

# Edite o .env com suas configuracoes (se necessario)
```

### 3. Iniciar banco de dados

**Opcao A - Com Docker (recomendado):**
```bash
npm run docker:up
```

**Opcao B - PostgreSQL local:**
Certifique-se de que o PostgreSQL esta rodando e a DATABASE_URL esta correta no `.env`

### 4. Executar migrations

```bash
npm run db:migrate:deploy
```

### 5. Iniciar a aplicacao

```bash
# Desenvolvimento (com hot-reload)
npm run start:dev

# Producao
npm run build
npm run start:prod
```

A API estara disponivel em `http://localhost:3000`

## Scripts Disponiveis

| Script | Descricao |
|--------|-----------|
| `npm run start:dev` | Inicia em modo desenvolvimento (hot-reload) |
| `npm run start:debug` | Inicia em modo debug |
| `npm run start:prod` | Inicia em modo producao |
| `npm run build` | Compila o projeto |
| `npm run test` | Executa testes unitarios |
| `npm run test:watch` | Testes em modo watch |
| `npm run test:cov` | Testes com coverage |
| `npm run test:e2e` | Testes end-to-end |
| `npm run lint` | Executa ESLint |
| `npm run format` | Formata codigo com Prettier |
| `npm run db:migrate` | Cria nova migration |
| `npm run db:migrate:deploy` | Aplica migrations pendentes |
| `npm run db:push` | Push do schema (dev) |
| `npm run db:studio` | Abre Prisma Studio |
| `npm run docker:up` | Inicia containers Docker |
| `npm run docker:down` | Para containers Docker |

## Endpoints

### Stations
- `GET /station` - Listar estacoes
- `POST /station` - Criar estacao
- `GET /station/:id` - Obter estacao
- `PATCH /station/:id` - Atualizar estacao
- `DELETE /station/:id` - Deletar estacao

### Weather Data
- `GET /data` - Listar dados meteorologicos
- `POST /data` - Criar registro
- `GET /data/:id` - Obter registro
- `PATCH /data/:id` - Atualizar registro
- `DELETE /data/:id` - Deletar registro

### IoT (Leituras brutas)
- `GET /iot` - Listar leituras
- `POST /iot` - Criar leitura
- `GET /iot/:id` - Obter leitura
- `PATCH /iot/:id` - Atualizar leitura
- `DELETE /iot/:id` - Deletar leitura

## Docker

Para rodar tudo com Docker:

```bash
docker-compose up -d
```

Isso ira:
1. Iniciar PostgreSQL na porta 5432
2. Executar migrations automaticamente
3. Iniciar a API na porta 3000

## Deploy no Google Cloud Run

A API esta configurada para deploy automatico no Cloud Run via Cloud Build.

**URL de producao:** https://plueview-659121705045.europe-west1.run.app

### Configuracao inicial (uma vez)

1. **Criar repositorio no Artifact Registry:**
```bash
gcloud artifacts repositories create plueview \
  --repository-format=docker \
  --location=europe-west1
```

2. **Criar secret no Secret Manager:**
```bash
echo -n "postgresql://user:pass@host:5432/db" | \
  gcloud secrets create DATABASE_URL --data-file=-
```

3. **Dar permissao ao Cloud Build:**
```bash
# Obter numero do projeto
PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format='value(projectNumber)')

# Permissao para deploy no Cloud Run
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$PROJECT_NUMBER@cloudbuild.gserviceaccount.com" \
  --role="roles/run.admin"

# Permissao para acessar secrets
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$PROJECT_NUMBER@cloudbuild.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"

# Permissao para usar service account
gcloud iam service-accounts add-iam-policy-binding \
  $PROJECT_NUMBER-compute@developer.gserviceaccount.com \
  --member="serviceAccount:$PROJECT_NUMBER@cloudbuild.gserviceaccount.com" \
  --role="roles/iam.serviceAccountUser"
```

4. **Criar trigger no Cloud Build:**
   - Acesse: Console GCP > Cloud Build > Triggers
   - Conecte o repositorio GitHub
   - Crie trigger para branch `main`
   - Use o arquivo `cloudbuild.yaml`

### Deploy manual

```bash
gcloud run deploy plueview \
  --source . \
  --region europe-west1 \
  --allow-unauthenticated
```

## Estrutura do Projeto

```
src/
  main.ts           # Entry point
  app.module.ts     # Modulo raiz
  data/             # Modulo de dados meteorologicos
  iot/              # Modulo de leituras IoT
  station/          # Modulo de estacoes
  prisma/           # Modulo do Prisma ORM
prisma/
  schema.prisma     # Schema do banco de dados
  migrations/       # Historico de migrations
cloudbuild.yaml     # Config de CI/CD para Cloud Run
```
