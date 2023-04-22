# postcodes
Library to parse postal code format

This is the another one validation libraries of postcodes in the United Kingdom.

The main goal of this package and difference of the others is to show in exactly part of postcode is wrong and need to be fixup.

## Installation
Instaling with pip (from github)

```
pip install -e git://github.com/samukasmk/postcodes.git@v0.1.0#egg=postcodes.egg-info
```

On the future we will provides at pypi.org

## Using library for validations

### Validating a correct postcode in python

This example bellow validates a correct postcode from Facebook `'W1T 1FB'`

```python
>>> from postcodes.uk import PostCodeUK

>>> postcode = PostCodeUK('W1T 1FB')
>>> postcode.is_valid
True

>>> postcode.outward
"W1T"
>>> postcode.inward
"1FB"

>>> postcode.area
"W"
>>> postcode.district
"1T"
>>> postcode.sector
"1"
>>> postcode.unit
"FB"

>>> postcode.to_dict()
{'postcode': 'W1T 1FB',
 'is_valid': True,
 'attributes': {'area': 'W',
                'district': '1T',
                'sector': '1',
                'unit': 'FB'},
 'sides': {'outward': 'W1T',
           'inward': '1FB'},
 'errors': {}}
```

### Validating a invalid postcode in python

This example is it is similar to the previous using Facebook postcode but missing last 'B' from 'FB' area part

```python
>>> from postcodes.uk import PostCodeUK

>>> postcode = PostCodeUK('W1T 1F')
>>> postcode.is_valid
False

>>> postcode.errors
{'unit': 'Invalid unit format.'}

>>> postcode.outward
"W1T"
>>> postcode.inward
"1F"

>>> postcode.area
"W"
>>> postcode.district
"1T"
>>> postcode.sector
"1"
>>> postcode.unit
"F"

>>> postcode.to_dict()
{'postcode': 'W1T 1F',
 'is_valid': False,
 'attributes': {'area': 'W',
                'district': '1T',
                'sector': '1',
                'unit': 'F'},
 'sides': {'outward': 'W1T',
           'inward': '1F'},
 'errors': {'unit': 'Invalid unit format.'}}
```


### Validating a invalid postcode from Facebook but missing space
The space is very important to determine which part of postcode is wrong.
So it will no work without spaces because the lib will considerates all string with outward side.
The example of missing spaces bellow:


```python
>>> from postcodes.uk import PostCodeUK

>>> postcode = PostCodeUK('W1T1FB')
>>> postcode.is_valid
False

>>> postcode.errors
{'missing_space': 'Missing space in the postcode',
 'district': 'Invalid district format.',
 'sector': 'Invalid sector format.',
 'unit': 'Invalid unit format.'}

>>> postcode.outward
"W1T1FB"
>>> postcode.inward
None

>>> postcode.area
"W"
>>> postcode.district
"1T1FB"
>>> postcode.sector
None
>>> postcode.unit
None

>>> postcode.to_dict()
{'postcode': 'W1T1FB',
 'is_valid': False,
 'attributes': {'area': 'W',
                'district': '1T1FB',
                'sector': None,
                'unit': None},
 'sides': {'outward': 'W1T1FB',
           'inward': None},
 'errors': {'missing_space': 'Missing space in the postcode',
            'district': 'Invalid district format.',
            'sector': 'Invalid sector format.',
            'unit': 'Invalid unit format.'}}
```

## Using Command line script for validations

If you want a command line solution for consulting in your terminal
or integrate with bash scripts you can use command line created on
pip install process to validate postcodes

```
postcodes --help
usage: postcodes [-h] -p [POSTCODES ...] [-r REGION_FORMAT] [-o {json,text}]

A command line to parses postcodes.

optional arguments:
  -h, --help            show this help message and exit
  -p [POSTCODES ...], --postcodes [POSTCODES ...]
                        The post code to analise.
  -r REGION_FORMAT, --region-format REGION_FORMAT
                        The region format.
  -o {json,text}, --output-format {json,text}
                        The region format.
```

The command line provides two types of output `json` or `text` and many values for the argument `--postcodes`.

### Validating postcodes in command line on json output

This example bellow validates a correct postcode from Facebook `'W1T 1FB'` on the json output


```
$ postcodes --postcodes 'W1T 1FB' --output-format json
{
    "W1T 1FB": {
        "attributes": {
            "area": "W",
            "district": "1T",
            "sector": "1",
            "unit": "FB"
        },
        "errors": {},
        "is_valid": true,
        "postcode": "W1T 1FB",
        "sides": {
            "inward": "1FB",
            "outward": "W1T"
        }
    }
}
```

**Exit code: 0** (with success)

#### Validating two correct postcodes in command line on json output

The another example of validating two correct postcodes of Buckingham Palace `'SW1A 1AA'` and Facebook `'W1T 1FB'` together

```
$ postcodes --postcodes 'SW1A 1AA' 'W1T 1FB' --output-format json
{
    "SW1A 1AA": {
        "attributes": {
            "area": "SW",
            "district": "1A",
            "sector": "1",
            "unit": "AA"
        },
        "errors": {},
        "is_valid": true,
        "postcode": "SW1A 1AA",
        "sides": {
            "inward": "1AA",
            "outward": "SW1A"
        }
    },
    "W1T 1FB": {
        "attributes": {
            "area": "W",
            "district": "1T",
            "sector": "1",
            "unit": "FB"
        },
        "errors": {},
        "is_valid": true,
        "postcode": "W1T 1FB",
        "sides": {
            "inward": "1FB",
            "outward": "W1T"
        }
    }
}
```

**Exit code: 0** (with success)


#### Validating two postcodes in command line on json format but one correct and another incorrect

The another example of validating together two postcodes of Buckingham Palace `'SW1A 1AA'` and wrong Facebook `'W1T 1F'` missing last `B`

```
$ postcodes --postcodes 'SW1A 1AA' 'W1T 1F' --output-format json
{
    "SW1A 1AA": {
        "attributes": {
            "area": "SW",
            "district": "1A",
            "sector": "1",
            "unit": "AA"
        },
        "errors": {},
        "is_valid": true,
        "postcode": "SW1A 1AA",
        "sides": {
            "inward": "1AA",
            "outward": "SW1A"
        }
    },
    "W1T 1F": {
        "attributes": {
            "area": "W",
            "district": "1T",
            "sector": "1",
            "unit": "F"
        },
        "errors": {
            "unit": "Invalid unit format."
        },
        "is_valid": false,
        "postcode": "W1T 1F",
        "sides": {
            "inward": "1F",
            "outward": "W1T"
        }
    }
}
```

**Exit code: 1** (with error because of the second the is incorrect)

### Validating postcodes in command line on text output

This example bellow validates a correct postcode from Facebook `'W1T 1FB'` on the text output

```
$ postcodes -p 'W1T 1FB'
Parsing postcode validations...

---
Postcode (W1T 1FB) format is: VALID
  Attributes:
    -> area: W
    -> district: 1T
    -> sector: 1
    -> unit: FB

---
Results:
  -> Valid postcodes: (W1T 1FB)
```

**Exit code: 0** (with success)

#### Validating two correct postcodes in command line on text output

The another example of validating two correct postcodes of Buckingham Palace `'SW1A 1AA'` and Facebook `'W1T 1FB'` together

```
$ postcodes -p 'SW1A 1AA' 'W1T 1FB'
Parsing postcode validations...

---
Postcode (SW1A 1AA) format is: VALID
  Attributes:
    -> area: SW
    -> district: 1A
    -> sector: 1
    -> unit: AA

---
Postcode (W1T 1FB) format is: VALID
  Attributes:
    -> area: W
    -> district: 1T
    -> sector: 1
    -> unit: FB

---
Results:
  -> Valid postcodes: (SW1A 1AA), (W1T 1FB)
```

**Exit code: 0** (with success)

#### Validating two postcodes in command line on text format but one correct and another incorrect

The another example of validating together two correct postcodes of (Buckingham Palace `'SW1A 1AA'`) and (National Savings `'DH99 1NS'`) and two **wrong postcodes** (Facebook `'W1T 1F'` missing last `B`) and (The Guardian `'N1 9G'` missing last `U`)

```
$ postcodes -p 'SW1A 1AA' 'DH99 1NS' 'W1T 1F' 'N1 9G'
Parsing postcode validations...

---
Postcode (SW1A 1AA) format is: VALID
  Attributes:
    -> area: SW
    -> district: 1A
    -> sector: 1
    -> unit: AA

---
Postcode (DH99 1NS) format is: VALID
  Attributes:
    -> area: DH
    -> district: 99
    -> sector: 1
    -> unit: NS

---
Postcode (W1T 1F) format is: INVALID
  Errors:
    -> Invalid unit format.
  Attributes:
    -> area: W
    -> district: 1T
    -> sector: 1
    -> unit: F(invalid format)

---
Postcode (N1 9G) format is: INVALID
  Errors:
    -> Invalid unit format.
  Attributes:
    -> area: N
    -> district: 1
    -> sector: 9
    -> unit: G(invalid format)

---
Results:
  -> Valid postcodes: (SW1A 1AA), (DH99 1NS)
  -> Invalid postcodes: (W1T 1F), (N1 9G)
```

**Exit code: 1** (with error because of the two incorrect postcodes)
