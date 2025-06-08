# more settings:
# https://drf-spectacular.readthedocs.io/en/latest/readme.html


SPECTACULAR_SETTINGS = {
    'TITLE': 'Flashcard API',
    'DESCRIPTION': 'Flashcard project',
    'VERSION': '0.1.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'SCHEMA_PATH_PREFIX': '/api/v[0-9]',
}
