web: gunicorn mysite.wsgi --log-file -
web: daphne mysite.asgi:application --port $PORT --bind 0.0.0.0 -v2