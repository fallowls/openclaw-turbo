import importlib.util
print('psycopg', importlib.util.find_spec('psycopg'))
print('psycopg2', importlib.util.find_spec('psycopg2'))
