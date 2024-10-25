celery -A app worker -B -E -n worker --loglevel=INFO --pool=threads --concurrency=4
