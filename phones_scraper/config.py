import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(object):
    """Base configuration."""

    NAME = 'BaseConfig'
    TESTING = False
    DEV = False
    TIMEOUT = 5
    FILE_DONE = f'{BASEDIR}/site_done.log'

    RE_RULE = r'|'.join([
        r'[\(][-\.\s]??\d{3}[-\.\s]??[\)][-\.\s]??\d{3}[-\.\s]??\d{2}[-\.\s]??\d{2}[\s\<\(а-яА-Яa-zA-Z]',
        r'\d{3}[-\.\s]??\d{3}[-\.\s]??\d{2}[-\.\s]??\d{2}[\s\<\(а-яА-Яa-zA-Z]',
        r'\d{3}[-\.\s]??\d{2}[-\.\s]??\d{2}[\s\<\(а-яА-Яa-zA-Z]'
    ])
    DEFAULT_AREA_CODE = 495


class DevelopConfig(BaseConfig):
    NAME = 'DevelopConfig'
    DEV = True
    TESTING = False


class ProdConfig(BaseConfig):
    NAME = 'ProdConfig'


class TestConfig(BaseConfig):
    NAME = 'TestConfig'
    TESTING = False


def get_config():
    mappings = dict(
        dev=DevelopConfig,
        prod=ProdConfig,
        test=TestConfig,
    )
    profile = os.environ.get('ENV', 'dev')
    return mappings[profile]
