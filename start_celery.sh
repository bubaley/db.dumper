export PYTHONPATH=$PYTHONPATH:.
celery -A app worker -B -E -n worker --loglevel=INFO --concurrency=3
