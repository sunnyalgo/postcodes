import pytest
from postcodes.uk import PostCodeUK


def test_postcodes_uk_uppercase_normalization():
    raw_postcode = 'aa9a 9aa'
    postcode = PostCodeUK(raw_postcode)
    assert postcode.raw_postcode == raw_postcode
    assert postcode.full_postcode == 'AA9A 9AA'


def test_postcodes_uk_outward_and_inward_validations():
    raw_postcode = 'AA9A 9AA'
    outward, inward = raw_postcode.split(' ')
    postcode = PostCodeUK(raw_postcode)
    assert postcode.outward == outward
    assert postcode.inward == inward


@pytest.mark.parametrize('raw_postcode, area, district, sector, unit', [['AA9A 9AA', 'AA', '9A', '9', 'AA'],
                                                                        ['A9A 9AA', 'A', '9A', '9', 'AA'],
                                                                        ['A9 9AA', 'A', '9', '9', 'AA'],
                                                                        ['A99 9AA', 'A', '99', '9', 'AA'],
                                                                        ['AA9 9AA', 'AA', '9', '9', 'AA'],
                                                                        ['AA99 9AA', 'AA', '99', '9', 'AA']])
def test_postcodes_uk_valid_formats(raw_postcode, area, district, sector, unit):
    postcode = PostCodeUK(raw_postcode)
    assert postcode.raw_postcode == raw_postcode
    assert postcode.full_postcode == raw_postcode
    assert postcode.area == area
    assert postcode.district == district
    assert postcode.sector == sector
    assert postcode.unit == unit
    assert postcode.is_valid is True


@pytest.mark.parametrize('raw_postcode', ['9 9AA', '9A 9AA', '99 9AA',
                                          'AAA9A 9AA', 'AAAA9A 9AA', 'AAAAA9A 9AA',
                                          'AAA99 9AA', 'AAAA99 9AA', 'AAAAA99 9AA', ])
def test_postcodes_uk_invalid_area(raw_postcode):
    postcode = PostCodeUK(raw_postcode)
    assert postcode.raw_postcode == raw_postcode
    assert postcode.full_postcode == raw_postcode
    assert postcode.is_valid is False
    assert postcode.errors == {'area': 'Invalid area format.'}


@pytest.mark.parametrize('raw_postcode', ['A 9AA', 'AA 9AA'])
def test_postcodes_uk_invalid_district(raw_postcode):
    postcode = PostCodeUK(raw_postcode)
    assert postcode.raw_postcode == raw_postcode
    assert postcode.full_postcode == raw_postcode
    assert postcode.is_valid is False
    assert postcode.errors == {'district': 'Invalid district format.'}


@pytest.mark.parametrize('raw_postcode', ['AA9A AA', 'A9A AA', 'A9 AA', 'A99 AA', 'AA9 AA', 'AA99 AA'])
def test_postcodes_uk_invalid_sector(raw_postcode):
    postcode = PostCodeUK(raw_postcode)
    assert postcode.raw_postcode == raw_postcode
    assert postcode.full_postcode == raw_postcode
    assert postcode.is_valid is False
    assert postcode.errors == {'sector': 'Invalid sector format.'}


@pytest.mark.parametrize('raw_postcode', ['AA9A 9', 'A9A 9', 'A9 9', 'A99 9', 'AA9 9', 'AA99 9',
                                          'AA9A 9AAA', 'A9A 9AAA', 'A9 9AAA', 'A99 9AAA', 'AA9 9AAA', 'AA99 9AAA',
                                          'AA9A 9AAAA', 'A9A 9AAAA', 'A9 9AAAA', 'A99 9AAAA', 'AA9 9AAAA',
                                          'AA99 9AAAA'])
def test_postcodes_uk_invalid_unit(raw_postcode):
    postcode = PostCodeUK(raw_postcode)
    assert postcode.raw_postcode == raw_postcode
    assert postcode.full_postcode == raw_postcode
    assert postcode.is_valid is False
    assert postcode.errors == {'unit': 'Invalid unit format.'}


def test_postcodes_uk_to_dict_with_valid_postcode():
    raw_postcode = 'AA9A 9AA'
    postcode = PostCodeUK(raw_postcode)
    assert postcode.is_valid is True
    assert postcode.to_dict() == {'postcode': 'AA9A 9AA',
                                  'is_valid': True,
                                  'attributes': {'area': 'AA', 'district': '9A', 'sector': '9', 'unit': 'AA'},
                                  'sides': {'outward': 'AA9A', 'inward': '9AA'},
                                  'errors': {}}


def test_postcodes_uk_to_dict_with_invalid_area():
    raw_postcode = '9A 9AA'
    postcode = PostCodeUK(raw_postcode)
    assert postcode.is_valid is False
    assert postcode.to_dict() == {'attributes': {'area': '', 'district': '9A', 'sector': '9', 'unit': 'AA'},
                                  'errors': {'area': 'Invalid area format.'},
                                  'is_valid': False,
                                  'postcode': '9A 9AA',
                                  'sides': {'inward': '9AA', 'outward': '9A'}}

def test_postcodes_uk_to_dict_with_invalid_district():
    raw_postcode = 'AA 9AA'
    postcode = PostCodeUK(raw_postcode)
    assert postcode.is_valid is False
    assert postcode.to_dict() == {'attributes': {'area': 'AA', 'district': None, 'sector': '9', 'unit': 'AA'},
                                  'errors': {'district': 'Invalid district format.'},
                                  'is_valid': False,
                                  'postcode': 'AA 9AA',
                                  'sides': {'inward': '9AA', 'outward': 'AA'}}

def test_postcodes_uk_to_dict_with_invalid_sector():
    raw_postcode = 'AA9A AA'
    postcode = PostCodeUK(raw_postcode)
    assert postcode.is_valid is False
    assert postcode.to_dict() == {'attributes': {'area': 'AA', 'district': '9A', 'sector': '', 'unit': 'AA'},
                                  'errors': {'sector': 'Invalid sector format.'},
                                  'is_valid': False,
                                  'postcode': 'AA9A AA',
                                  'sides': {'inward': 'AA', 'outward': 'AA9A'}}

def test_postcodes_uk_to_dict_with_invalid_unit():
    raw_postcode = 'AA9A 9'
    postcode = PostCodeUK(raw_postcode)
    assert postcode.is_valid is False
    assert postcode.to_dict() == {'attributes': {'area': 'AA', 'district': '9A', 'sector': '9', 'unit': ''},
                                  'errors': {'unit': 'Invalid unit format.'},
                                  'is_valid': False,
                                  'postcode': 'AA9A 9',
                                  'sides': {'inward': '9', 'outward': 'AA9A'}}


def test_postcodes_uk_to_dict_with_invalid_combined_area_and_unit():
    raw_postcode = '9A 9'
    postcode = PostCodeUK(raw_postcode)
    assert postcode.is_valid is False
    assert postcode.to_dict() == {'attributes': {'area': '', 'district': '9A', 'sector': '9', 'unit': ''},
                                  'errors': {'area': 'Invalid area format.', 'unit': 'Invalid unit format.'},
                                  'is_valid': False,
                                  'postcode': '9A 9',
                                  'sides': {'inward': '9', 'outward': '9A'}}


def test_postcodes_uk_to_dict_with_invalid_combined_district_and_sector():
    raw_postcode = 'AA AA'
    postcode = PostCodeUK(raw_postcode)
    assert postcode.is_valid is False
    assert postcode.to_dict() == {'attributes': {'area': 'AA', 'district': None, 'sector': '', 'unit': 'AA'},
                                  'errors': {'district': 'Invalid district format.',
                                             'sector': 'Invalid sector format.'},
                                  'is_valid': False,
                                  'postcode': 'AA AA',
                                  'sides': {'inward': 'AA', 'outward': 'AA'}}


def test_postcodes_uk_to_dict_with_missing_space_letter():
    raw_postcode = 'AAAA'
    postcode = PostCodeUK(raw_postcode)
    assert postcode.is_valid is False
    assert postcode.to_dict() == {'attributes': {'area': 'AAAA', 'district': None, 'sector': None, 'unit': None},
                                  'errors': {'area': 'Invalid area format.',
                                             'district': 'Invalid district format.',
                                             'missing_space': 'Missing space in the postcode',
                                             'sector': 'Invalid sector format.',
                                             'unit': 'Invalid unit format.'},
                                  'is_valid': False,
                                  'postcode': 'AAAA',
                                  'sides': {'inward': None, 'outward': 'AAAA'}}

def test_postcodes_uk_to_dict_with_missing_space_digit():
    raw_postcode = '9'
    postcode = PostCodeUK(raw_postcode)
    assert postcode.is_valid is False
    assert postcode.to_dict() == {'attributes': {'area': '', 'district': '9', 'sector': None, 'unit': None},
                                  'errors': {'area': 'Invalid area format.',
                                             'missing_space': 'Missing space in the postcode',
                                             'sector': 'Invalid sector format.',
                                             'unit': 'Invalid unit format.'},
                                  'is_valid': False,
                                  'postcode': '9',
                                  'sides': {'inward': None, 'outward': '9'}}
