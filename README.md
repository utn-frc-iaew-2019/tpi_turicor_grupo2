# Setup (Linux) on virtualenv

> sudo apt-get install libxml2-dev libxslt1-dev python3.5 python3.5-dev

> virtualenv -p {python path} venv

En linux, python se encuentra en /usr/bin/python3.5 se pueden usar las versiones 3.5, 3.6 o 3.7.

> source venv/bin/activate

> pip install -r requirements.txt

> cd iaew

> python manage.py makemigrations

> python manage.py migrate

# Setup (Linux)

Install [Python 3.6](https://www.python.org/downloads/release/python-360/)

Abrir una consola y ubicarse en el directorio principal.

> python -m pip install -r requirements.txt

> cd iaew

> python manage.py makemigrations

> python manage.py migrate

# Run

> python manage.py runserver

Abrir [localhost:8000/](localhost:8000/)
