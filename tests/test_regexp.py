from phones_scraper import scraper_manager


def test_parse_phone():
    samples = [
        ' 8(800)900-90-97 ',
        ' 8 (800) 900-90-97 ',
        '+7 (800)900-90-97 ',
        ' 8 800 9009097 ',
        'fsads +7 (800) 900-90-97 ',
        'sdfdsvd 88009009097 <dsfsdf>',
        '800-900-90-97 ',
        '(800)900-9097 ',
        '(800) 900-9097 '
    ]
    for s in samples:
        print(s)
        assert scraper_manager.parse_phones(s) == ['88009009097']


def test_parse_without_code():
    samples = [
        'sdf 900-90-97 dsf',
        'dsfds 900-9097 ',
        ' 9009097 dsfdsf'
    ]

    for s in samples:
        assert scraper_manager.parse_phones(s) == ['84959009097']
