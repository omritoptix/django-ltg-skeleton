web: python manage.py run_gunicorn -b "0.0.0.0:$PORT"
celerydpolling: python manage.py celeryd -B --loglevel=INFO -E
celerydprocessing: python manage.py celeryd --loglevel=INFO -Q closedeals -E