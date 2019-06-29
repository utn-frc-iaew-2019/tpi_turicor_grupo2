# Setup (Linux)

> sudo apt-get install libxml2-dev libxslt1-dev python3.5 python3.5-dev

> virtualenv -p {python path} venv

En linux, python se encuentra en /usr/bin/python3.5 se pueden usar las versiones 3.5, 3.6 o 3.7.

> source venv/bin/activate

> pip install -r requirements.txt

> python manage.py makemigrations

> python manage.py migrate

# Run

> python manage.py runserver

Navigate to [localhost:8000/](localhost:8000/)
