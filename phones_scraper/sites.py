from collections import namedtuple

Site = namedtuple('Site', ['id', 'main', 'page_contacts'])
SITES = [
    Site(
        1,
        'https://hands.ru/',
        'https://hands.ru/company/about'
    ),
    Site(
        2,
        'https://repetitors.info',
        'https://repetitors.info/about.php'
    ),
    Site(
        4,
        'https://postgrespro.ru',
        'https://postgrespro.ru/contacts'
    ),
    Site(
        6,
        'https://skyeng.ru',
        'https://skyeng.ru/contacts'
    )
]


def get_sites():
    return SITES
