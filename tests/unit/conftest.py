from pytest import fixture


@fixture
def test_header_field_bytes():
    return b'0       brux2                                                                                                                                                           04.02.0222.07.231536                                                100     1       5   '  # noqa: E501


@fixture
def channel_field_bytes():
    return b'Fp2-F4          F4-C4           C4-P4           P4-O2           F8-T4           EEG Fp2-F4                                                                      EEG F4-C4                                                                       EEG C4-P4                                                                       EEG P4-O2                                                                       EEG F8-T4                                                                       uV      uV      uV      uV      uV      -62.5   -62.5   -62.5   -62.5   -62.5   62.5    62.5    62.5    62.5    62.5    -2048   -2048   -2048   -2048   -2048   2047    2047    2047    2047    2047    LP:30.00Hz HP:0.30Hz NOTCH:50                                                   LP:30.00Hz HP:0.30Hz NOTCH:50                                                   LP:30.00Hz HP:0.30Hz NOTCH:50                                                   LP:30.00Hz HP:0.30Hz NOTCH:50                                                   LP:30.00Hz HP:0.30Hz NOTCH:50                                                   256     256     256     256     256                                                                                                                                                                     '  # noqa: E501


@fixture
def channel_field_content():
    return [
        {
            'label': 'Fp2-F4',
            'channel_type': 'EEG Fp2-F4',
            'physical_dimension': 'uV',
            'physical_minimum': -62.5,
            'physical_maximum': 62.5,
            'digital_minimum': -2048,
            'digital_maximum': 2047,
            'prefiltering': 'LP:30.00Hz HP:0.30Hz NOTCH:50',
            'num_samples_per_record': 256,
            'reserved': '',
        },
        {
            'label': 'F4-C4',
            'channel_type': 'EEG F4-C4',
            'physical_dimension': 'uV',
            'physical_minimum': -62.5,
            'physical_maximum': 62.5,
            'digital_minimum': -2048,
            'digital_maximum': 2047,
            'prefiltering': 'LP:30.00Hz HP:0.30Hz NOTCH:50',
            'num_samples_per_record': 256,
            'reserved': '',
        },
        {
            'label': 'C4-P4',
            'channel_type': 'EEG C4-P4',
            'physical_dimension': 'uV',
            'physical_minimum': -62.5,
            'physical_maximum': 62.5,
            'digital_minimum': -2048,
            'digital_maximum': 2047,
            'prefiltering': 'LP:30.00Hz HP:0.30Hz NOTCH:50',
            'num_samples_per_record': 256,
            'reserved': '',
        },
        {
            'label': 'P4-O2',
            'channel_type': 'EEG P4-O2',
            'physical_dimension': 'uV',
            'physical_minimum': -62.5,
            'physical_maximum': 62.5,
            'digital_minimum': -2048,
            'digital_maximum': 2047,
            'prefiltering': 'LP:30.00Hz HP:0.30Hz NOTCH:50',
            'num_samples_per_record': 256,
            'reserved': '',
        },
        {
            'label': 'F8-T4',
            'channel_type': 'EEG F8-T4',
            'physical_dimension': 'uV',
            'physical_minimum': -62.5,
            'physical_maximum': 62.5,
            'digital_minimum': -2048,
            'digital_maximum': 2047,
            'prefiltering': 'LP:30.00Hz HP:0.30Hz NOTCH:50',
            'num_samples_per_record': 256,
            'reserved': '',
        },
    ]
