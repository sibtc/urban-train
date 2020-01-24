# Urban Train

Sistema de Gerenciamento de gastos

# Instalação
Recomenda-se criar uma virtualenv para evitar conflitos de versões das bibliotecas instaladas no seu computador
> virtualenv .venv

Para acessar
- *Windows*:
> virtualenv .venv\Scripts\activate
- *Linux*:
> source .venv\bin\activate

Instalar as bibliotecas:
- *Windows*:
  > pip install -r requirements.txt
- *Linux*:
  - ATENÇÃO: no linux por padrão vem instalado a versão 2.7 do python,
   mas precisamos da versão 3.6+ então instale-a e rode:
  > pip3 install -r requirements.txt

Crie 2 pastas, na raiz do projeto, para guardar infos sigilosas:
- *.envs* e dentro *.local*

Depois dentro da pasta .local crie o arquivo *.env* com o seguinte conteúdo:
```
DEBUG=True
APPEND_SLASH=False

DJANGO_SECRET_KEY='apjfqc9e8r-9eq3r3u49u4399r43-@#%^^^'
DJANGO_ALLOWED_HOSTS=localhost

#-------------------DATASBASE-------------------------
DATABASE_URL=postgres://<USER>:<PASSWORD>@localhost:5432/<DATABASE>
SQLITE_URL=sqlite:///db.sqlite3

RDS_DB_NAME=
RDS_USERNAME=
RDS_PASSWORD=
RDS_HOSTNAME=
RDS_PORT=5432

# AWS Settings
DJANGO_AWS_ACCESS_KEY_ID=
DJANGO_AWS_SECRET_ACCESS_KEY=
DJANGO_AWS_STORAGE_BUCKET_NAME=

# Used with email
DJANGO_MAILGUN_API_KEY=
DJANGO_SERVER_EMAIL=
MAILGUN_SENDER_DOMAIN=

# Security! Better to use DNS for this task, but you can use redirect
DJANGO_SECURE_SSL_REDIRECT=False

# django-allauth
DJANGO_ACCOUNT_ALLOW_REGISTRATION=False
```

Criar o banco e as tabelas:
- *Windows*:
  > python manage.py migrate
- *Linux*:
  > python3 manage.py migrate

Às vezes pode acontecer bugs e precisamos rodar o migrate para cada app, assim:
> python manage.py makemigrations accounts  

> python manage.py makemigrations website

> python manage.py migrate

Criar o usuário para poder logar no app:

- *Windows*:
  > python manage.py createsuperuser
- *Linux*:
  > python3 manage.py createsuperuser

Será criado o **user** principal do sistema

Como início de sua aplicação são esses os passos iniciais.

Qualquer dúvida/críticas/melhorias crie uma issues no github
ou envie pelo e-mail: *contato@luxu.com.br*

That's all folks!