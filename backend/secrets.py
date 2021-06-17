SECRET_KEY = 'mscm*pgd)ezuy#^u+9*aw1@@@io#_sg+1)t=w!95t#ndd0az^+'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'game-web-site',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': '192.168.178.85',
        'PORT': '5432'
    }
}

igdb_data = {
        'client_id': '31wxrza5qcb3h0kn1s5ep6cq1vqtwj',
        'client_secret': '1lmsfzd2fkl0jfg78lq8kija2w1uhm',
        'grant_type': 'client_credentials'
}

twitter_data = {
    'url': 'https://api.twitter.com/2',
    'api-key': 'AZPDM9aI4xwF16gPwqGCGxHdM',
    'api-secret': 'lxhj1uzpprVrRiapBiGMD7p8pCMMQVlCIeHKfmZfS5teTZw6Q3',
    'bearer': 'AAAAAAAAAAAAAAAAAAAAADtlNgEAAAAAtoygdnuL07x2YIVxhuoerfw5yxI%3DLjA7km6aqmjLhK8I2qEBrQxpZ9LQw0gA2I4Y0GWByJbVXSsStl'
}
