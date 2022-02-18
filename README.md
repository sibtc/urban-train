# ERP - Sistema de Gerenciamento de Gastos

# Instalação

> python -m venv .venv

Para acessar
- *Windows*:
> virtualenv .venv\Scripts\activate
- *Linux*:
> source .venv\bin\activate

Instalar as bibliotecas:

- Atualizando o pip:
> *python -m pip install --upgrade pip*

- *Windows*:
  > pip install -r requirements.txt
- *Linux*:
  - ATENÇÃO: no linux por padrão vem instalado a versão 2.7 do python,
   mas precisamos da versão 3.6+ então instale-a e rode:
  > pip3 install -r requirements.txt

- Rode o scripts abaixo:
  > python contrib\env_gen.py

Rode as migrations:
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

Como início de sua aplicação são esses os passos.

Qualquer dúvida/críticas/melhorias crie uma issues no github
ou envie pelo e-mail: *luciano.martins.developer@gmail.com*

That's all folks!
