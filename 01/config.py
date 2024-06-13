import os

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:root@localhost/apitest')

