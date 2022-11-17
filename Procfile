release: python manage.py migrate
web: python manage.py collectstatic --no-input; gunicorn codebattle.wsgi --log-file - --log-level debug