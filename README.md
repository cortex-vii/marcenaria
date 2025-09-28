# Django Base Project

Este é um projeto base Django configurado com Docker, PostgreSQL, Nginx e interface administrativa customizada com Django Unfold.

## 🚀 Características

- **Django 5.0.3** com interface administrativa moderna (django-unfold)
- **PostgreSQL 13** como banco de dados
- **Nginx** como proxy reverso e servidor de arquivos estáticos
- **Docker** e **Docker Compose** para containerização
- **SSL/HTTPS** suporte com certificados personalizados
- **CORS** configurado para APIs
- **Email** configurado para Zoho SMTP
- **Arquivos estáticos e media** servidos pelo Nginx

## 📋 Pré-requisitos

- Docker
- Docker Compose
- Git

## 🛠️ Estrutura do Projeto

```
django-testes/
├── djangoapp/                  # Aplicação Django principal
│   ├── project/               # Configurações do Django
│   ├── blog/                  # App de exemplo
│   ├── templates/             # Templates customizados
│   ├── manage.py
│   └── requirements.txt
├── nginx/                     # Configuração do Nginx
├── scripts/                   # Scripts de inicialização
├── dotenv_files/              # Arquivos de exemplo de variáveis
├── certs/                     # Certificados SSL (você deve criar)
├── docker-compose.yml
├── Dockerfile
└── README.md
```

## 🔧 Instalação e Configuração

### 1️⃣ Clone o repositório

```bash
git clone https://github.com/PantojaVII/django-base.git
cd django-base
```

### 2️⃣ Configure as variáveis de ambiente

```bash
# Copie o arquivo de exemplo
cp dotenv_files/.env-example .env

# Edite o arquivo .env com suas configurações
nano .env
```

**Variáveis importantes para alterar:**

```bash
SECRET_KEY="sua-chave-secreta-muito-segura"
DEBUG="0"  # 0 para produção, 1 para desenvolvimento
ALLOWED_HOSTS="seu-dominio.com,192.168.0.110"
POSTGRES_DB="nome_do_banco"
POSTGRES_USER="usuario_do_banco"
POSTGRES_PASSWORD="senha_do_banco"
```

### 3️⃣ Gere os certificados SSL (Opcional)

Se você quiser usar HTTPS:

```bash
# Crie o diretório para certificados
mkdir certs

# Gere certificados autoassinados para desenvolvimento
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout certs/key.pem -out certs/cert.pem
```

Para produção, substitua pelos certificados válidos (Let's Encrypt, Cloudflare, etc.)

### 4️⃣ Inicie o projeto

```bash
# Construa e inicie os containers
docker compose up --build

# Ou em background
docker compose up -d --build
```

## 🌐 Acessando a aplicação

- **Aplicação Django**: http://localhost:8800 (ou a porta configurada em `DJANGO_PORT_CONTAINER`)
- **Admin Django**: http://localhost:8800/admin/
  - **Usuário**: `root`
  - **Senha**: `231212`

## 📊 Comandos Úteis

### Gerenciamento de containers

```bash
# Ver logs
docker compose logs -f

# Parar containers
docker compose down

# Reconstruir containers
docker compose up --build

# Executar comandos Django
docker compose exec djangoservice python manage.py [comando]
```

### Comandos Django dentro do container

```bash
# Acessar shell do Django
docker compose exec djangoservice python manage.py shell

# Criar migrações
docker compose exec djangoservice python manage.py makemigrations

# Aplicar migrações
docker compose exec djangoservice python manage.py migrate

# Criar superusuário
docker compose exec djangoservice python manage.py createsuperuser

# Coletar arquivos estáticos
docker compose exec djangoservice python manage.py collectstatic
```

## 🗄️ Banco de Dados

O projeto usa PostgreSQL 13 em container. Os dados são persistidos em `./data/postgres/data/`.

**Conexão direta ao banco** (se necessário):
```bash
docker compose exec psqlservice psql -U [POSTGRES_USER] -d [POSTGRES_DB]
```

## 📁 Volumes e Persistência

- `./data/postgres/data/` - Dados do PostgreSQL
- `./data/web/static/` - Arquivos estáticos do Django
- `./data/web/media/` - Arquivos de mídia enviados pelos usuários

## 🎨 Interface Administrativa

O projeto usa o **Django Unfold** para uma interface administrativa moderna. Para customizar:

1. Edite `djangoapp/project/unfold_settings.py`
2. Modifique templates em `djangoapp/templates/admin/`

## 📧 Configuração de Email

O projeto está configurado para usar Zoho SMTP. Altere no arquivo `.env`:

```bash
EMAIL_HOST_USER="seu-email@zoho.com"
EMAIL_HOST_PASSWORD="sua-senha-de-app"
DEFAULT_FROM_EMAIL="seu-email@zoho.com"
```

## 🚀 Deploy em Produção

1. **Configure o ambiente**:
   - `DEBUG="0"`
   - Configure `ALLOWED_HOSTS` com seu domínio
   - Use certificados SSL válidos
   - Configure CORS adequadamente

2. **Segurança**:
   - Altere a senha padrão do superusuário
   - Use senhas fortes para o banco
   - Configure firewall adequadamente

3. **Performance**:
   - Configure Redis para cache (opcional)
   - Use Gunicorn em produção
   - Configure logs adequadamente

## 🤝 Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 🆘 Problemas Comuns

### Container não inicia
- Verifique se as portas não estão em uso
- Confirme se o arquivo `.env` está configurado corretamente

### Erro de permissão
- O projeto usa `su-exec` para gerenciar permissões
- Arquivos são automaticamente ajustados no entrypoint

### Banco não conecta
- Aguarde o PostgreSQL inicializar completamente
- Verifique as credenciais no arquivo `.env`

## 📞 Suporte

Para suporte, abra uma issue no GitHub ou entre em contato com a equipe de desenvolvimento.

---

**Desenvolvido por**: Estrutura Córtex  
**Maintainer**: PantojaVII


