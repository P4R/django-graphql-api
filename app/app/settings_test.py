# -*- coding: utf-8 -*-

import logging
import os

from graphene_django.utils.testing import GraphQLTestCase

from app.settings import *  # noqa
from app.settings import BASE_DIR

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3')
    }
}
logging.disable(logging.CRITICAL)
GraphQLTestCase.GRAPHQL_URL = '/api/graphql'
