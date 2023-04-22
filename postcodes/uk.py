import re
from typing import Tuple, Optional

REGEX_AREA_VALIDATION = re.compile(r'^[A-Z]{1,2}$')
REGEX_DISTRICT_VALIDATION = re.compile(r'^[0-9][A-Z0-9]?$')
REGEX_SECTOR_VALIDATION = re.compile(r'^[0-9]$')
REGEX_UNIT_VALIDATION = re.compile(r'^[A-Z]{2}$')
REGEX_DIGITS = re.compile(r'([0-9]+)')
REGEX_SPACES = re.compile(r' +')

POSTCODE_VALIDATIONS = {'area': REGEX_AREA_VALIDATION,
                        'district': REGEX_DISTRICT_VALIDATION,
                        'sector': REGEX_SECTOR_VALIDATION,
                        'unit': REGEX_UNIT_VALIDATION}


class PostCodeUK:
    """Object to parse postal code to UK format."""

    def __init__(self, postcode: str):
        # define internal attributes
        self.__raw_postcode = postcode
        self.__full_postcode = postcode.upper()
        self.__errors = {}
        self.__outward = None
        self.__inward = None
        self.__area = None
        self.__district = None
        self.__sector = None
        self.__unit = None
        self.__attributes = ('area', 'district', 'sector', 'unit')

        # parses postcode format
        self.__outward, self.__inward = self.__get_outward_and_inward()
        self.__area, self.__district = self.__get_area_and_district()
        self.__sector, self.__unit = self.__get_sector_and_unit()
        self.__errors.update(self.__validate_postcode_attributes_format())

    @property
    def raw_postcode(self):
        """Raw postcode text"""
        return self.__raw_postcode

    @property
    def full_postcode(self):
        """Full postcode text normalized"""
        return self.__full_postcode

    @property
    def errors(self):
        """Errors dict with exact postcode attribute that is incorrectly formatted"""
        return self.__errors

    @property
    def outward(self):
        """Outward side"""
        return self.__outward

    @property
    def inward(self):
        """Inward side"""
        return self.__inward

    @property
    def attributes(self):
        """Postcode attributes"""
        return self.__attributes

    @property
    def area(self):
        """Area postcode attribute"""
        return self.__area

    @property
    def district(self):
        """District postcode attribute"""
        return self.__district

    @property
    def sector(self):
        """Sector postcode attribute"""
        return self.__sector

    @property
    def unit(self):
        """Unit postcode attribute"""
        return self.__unit

    @property
    def is_valid(self):
        """Validation status"""
        return not self.__errors

    def to_dict(self):
        """Formating result in dict object"""
        return {'postcode': self.full_postcode,
                'is_valid': self.is_valid,
                'attributes': {attr: getattr(self, attr) for attr in self.attributes},
                'sides': {'outward': self.outward, 'inward': self.inward},
                'errors': self.errors}

    def __get_outward_and_inward(self):
        """Splits full postcode string in outward and inward sides"""
        if not REGEX_SPACES.search(self.full_postcode):
            self.__errors['missing_space'] = 'Missing space in the postcode'
        return self.__split_sides_by_spaces(self.full_postcode)

    def __get_area_and_district(self):
        """Splits outward string in area and district sides"""
        if not self.outward:
            return None, None

        outward_to_split = self.__insert_space_before_digits(self.outward)
        return self.__split_sides_by_spaces(outward_to_split)

    def __get_sector_and_unit(self):
        """Splits inward string in sector and unit sides"""
        if not self.inward:
            return None, None

        if self.inward[0].isdigit():
            inward_to_split = self.__insert_space_after_digits(self.inward)
        else:
            inward_to_split = self.__insert_space_at_beginning(self.inward)

        return self.__split_sides_by_spaces(inward_to_split)

    def __validate_postcode_attributes_format(self):
        """Parses postcode format in separated pieces
           The purpose of validating separate pieces is to obtain depth of
           understanding on the exact attribute of the p that is incorrect"""
        errors = {}
        for name in self.attributes:
            regex_pattern = POSTCODE_VALIDATIONS[name]
            value = getattr(self, name)
            if not value or not regex_pattern.match(value):
                errors[name] = f'Invalid {name} format.'
        return errors

    @staticmethod
    def __insert_space_before_digits(text_to_insert: str) -> str:
        """Formats string to split inserting spaces before digits"""
        return REGEX_DIGITS.sub(r' \1', text_to_insert)

    @staticmethod
    def __insert_space_after_digits(text_to_insert: str) -> str:
        """Formats string to split inserting spaces after digits"""
        return REGEX_DIGITS.sub(r'\1 ', text_to_insert)

    @staticmethod
    def __insert_space_at_beginning(text_to_insert: str) -> str:
        """Formats string to split inserting spaces at the string begging"""
        return ' ' + text_to_insert

    @staticmethod
    def __split_sides_by_spaces(text_to_split: str) -> Tuple[Optional[str], Optional[str]]:
        """Splits string into two pieces
           First piece is the first element found and second piece is the rest of matches"""
        left_side = None
        right_side = None
        splited_sides = REGEX_SPACES.split(text_to_split)
        if splited_sides:
            left_side = splited_sides[0]
            if len(splited_sides) > 1:
                right_side = ''.join(splited_sides[1:])
        return left_side, right_side
