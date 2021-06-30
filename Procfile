
release: python manage.py migrate
web: daphne mysite.asgi:start_app --port $PORT --bind 0.0.0.0 -v2
worker: python manage.py runworker -v2