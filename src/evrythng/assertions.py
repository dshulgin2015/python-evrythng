from evrythng.exceptions import (
    ExtraDataSubmittedException,
    InvalidDatatypeException,
    InvalidValueException,
    ReadOnlyFieldWrittenToException,
    RequiredFieldException,
)


def required(supplied_fields, required_fields):
    """Assert that all required fields are in the supplied_fields."""
    for field in required_fields:
        try:
            assert field in supplied_fields
        except AssertionError:
            raise RequiredFieldException(field)


def readonly(supplied_fields, readonly_fields):
    """Assert that a read only field wasn't supplied as a field/value."""
    for field in supplied_fields:
        try:
            assert field not in readonly_fields or supplied_fields[field] is None
        except AssertionError:
            raise ReadOnlyFieldWrittenToException(field, supplied_fields[field])


def no_extras(supplied_fields, possible_fields):
    """Assert that there are no extra fields in the supplied_fields."""
    for field in supplied_fields:
        try:
            assert field in possible_fields
        except AssertionError:
            raise ExtraDataSubmittedException(field, supplied_fields[field])


def datatype_str(field, value, spec):
    """Assert that the value is of type str."""
    try:
        assert isinstance(value, str)
    except AssertionError:
        raise InvalidDatatypeException(field, str, type(value))


def datatype_time(field, value, spec):
    """Assert that the value is of type int."""
    try:
        assert isinstance(value, int)
    except AssertionError:
        raise InvalidDatatypeException(field, int, type(value))


def datatype_dict(field, value, spec):
    """Assert that the value is of type dict."""
    try:
        assert isinstance(value, dict)
    except AssertionError:
        raise InvalidDatatypeException(field, dict, type(value))


def datatype_dict_of_str(field, value, spec):
    datatype_dict(field, value, spec)
    for k, v in value.iteritems():
        try:
            assert isinstance(k, str)
        except:
            raise InvalidDatatypeException(
                    '{}[{}]'.format(field, k), str, type(k))
        try:
            assert isinstance(v, str)
        except:
            raise InvalidDatatypeException(
                    '{}[{}].value'.format(field, k), str, type(v))


def datatype_list_of_str(field, value, spec):
    """Assert that the value is of type list containing str."""
    try:
        assert isinstance(value, (list, tuple))
        for i, val in enumerate(value):
            try:
                assert isinstance(value, str)
            except AssertionError:
                raise InvalidDatatypeException(
                    '{}[{}]'.format(field, i), str, type(value))
    except AssertionError:
        raise InvalidDatatypeException(field, (list, tuple), type(value))

    spec = spec.split('|')
    if len(spec) > 1:
        required_values = spec[1].split(',')
        if value not in required_values:
            raise InvalidValueException(
                field, value, ', '.join(required_values))


def datatype_list_of_social_networks(field, value, spec):
    # TODO: figure our how to serialize this.
    return ''


def datatype_birthday(field, value, spec):
    try:
        assert isinstance(value, dict)
    except AssertionError:
        raise InvalidDatatypeException(field, dict, type(value))

    required_keys = ('day', 'month', 'year')

    for key in value:
        if key not in required_keys:
            raise ValueError(
                'Invalid key of {} ... must be one of day|month|year.'.format(
                    key))

        try:
            assert isinstance(value[key], int)
        except AssertionError:
            raise InvalidDatatypeException(
                '{}[{}]'.format(field, key), int, type(value[key]))

        if key == 'month' and not (1 <= value <= 12):
            raise InvalidValueException(
                '{}[{}]'.format(field, key), value, '1-12')
        elif key == 'day' and not (1 <= value <= 31):
            raise InvalidValueException(
                '{}[{}]'.format(field, key), value, '1-31')
        elif key == 'year' and not (1800 <= value <= 2100):
            raise InvalidValueException(
                '{}[{}]'.format(field, key), value, '1800-2100')


def datatype_location(field, value, spec):
    datatype_dict(field, value, spec)
    try:
        assert 'position' in value
    except AssertionError:
        raise RequiredFieldException('position')

    try:
        assert 'type' in value['position']
    except AssertionError:
        raise RequiredFieldException('position[type]')

    try:
        assert value['position']['type'] == 'Point'
    except AssertionError:
        raise RequiredFieldException('position[type] != Point')

    try:
        assert 'coordinates' in value['position']
    except AssertionError:
        raise RequiredFieldException('position[coordinates]')

    coordinates = value['position']['coordinates']

    try:
        assert len(coordinates) == 2
    except AssertionError:
        raise ValueError('location[position][coordinates] must be an array of 2 floats: [float, float]')


def datatype_address(field, value, spec):
    valid_keys = (
        'extension',
        'street',
        'postalCode',
        'city',
        'county',
        'state',
        'country',
        'countryCode',
        'district',
        'buildingName',
        'buildingFloor',
        'buildingRoom',
        'buildingZone',
        'crossing1',
        'crossing2',
    )

    if not isinstance(value, dict):
        raise InvalidDatatypeException(field, dict, type(value))

    # Make sure the user didn't submit an unexpected key.
    for key in value:
        if key not in valid_keys:
            raise ExtraDataSubmittedException(field, key)

    # Make sure all values are str.
    for k, v in value.iteritems():
        if not isinstance(v, str):
            raise InvalidDatatypeException('{}[{}]'.format(field, v))


def datatype_geojson(field, value, spec):
    pass


def datatypes(supplied_fields, datatype_specs):
    """A helper for routing values to their type validators."""
    for field in supplied_fields:
        value = supplied_fields[field]
        if value is None:
            continue
        spec = datatype_specs[field]
        validator_name = spec.split('|')[0]
        validator = file_locals['datatype_{}'.format(validator_name)]
        validator(field, supplied_fields[field], spec)


file_locals = locals()