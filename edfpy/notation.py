from typing import Dict

channel_labels_by_type = dict(
    REF=[
        'A1', 'A2', 'M1', 'M2'
    ],
    EEG=[
        'C3', 'C4', 'CZ',
        'EEG',
        'F1', 'F2', 'F3', 'F4', 'F7', 'F8', 'FZ', 'Fp1', 'Fp2', 'FpZ',
        'O1', 'O2', 'OZ',
        'P3', 'P4', 'PZ',
        'T3', 'T4', 'T5', 'T6'
    ],

    ECG=[
        'ECG', 'ECG1', 'ECG2'
    ],

    EMG=[
        'EMG',
        'EMG1', 'EMG2',
        'EMG_x', 'EMG_y',
        'CHIN',
        'CHIN1', 'CHIN2',
        'Deltoide',
        'Submental1', 'Submental2', 'Submental3',
    ],

    EOG=[
        'EOG',
        'EOG_L', 'EOG_R',
        'E1-M2', 'E2-M2',
        'EOG_L-M2', 'EOG_R-M2',
    ],

    HR=[
        'HR'
    ],

    RESP=[
        'Pleth', 'Thorax', 'Abdomen', 'Flow', 'Cannula', 'THE'
    ],

    POS=[
        'Position'
    ],

    BLOODGAS=[
        'SpO2', 'STAT_SpO2'
    ],

    SNORE=[
        'MIC'
    ],

    LEG=[
        'Leg',
        'TIB_L', 'TIB_R',
        'TIB_L1', 'TIB_R1',
    ]
)


synonyms = {
    'LEOG-REF': 'EOG_L',
    'REOG-REF': 'EOG_R',
    'E1': 'EOG_L',
    'E2': 'EOG_R',
    'E1-M2': 'EOG_L-M2',
    'E2-M2': 'EOG_R-M2',
    'E1M2': 'EOG_L-M2',
    'E2M1': 'EOG_R-M1',
    'E2M2': 'EOG_R-M2',
    'EOGLOC-A2': 'EOG_L-A2',
    'EOGROC-A1': 'EOG_R-A1',
    'A1': 'M1',
    'A2': 'M2',
    'EEGF3-A2': 'F3-M2',
    'EEGF4-A1': 'F4-M1',
    'EEGC3-A2': 'C3-M2',
    'EEGC4-A1': 'C4-M1',
    'EEGO1-A2': 'O1-M2',
    'EEGO2-A1': 'O2-M1',
    'EEGA1-A2': 'A1-M2',
    'EEGA2-A1': 'A2-M1',
    'EOGLEFT': 'EOG_L-A2',
    'EOGRIGHT': 'EOG_R-A2',

    'F3A2': 'F3-M2',
    'F4A1': 'F4-M1',
    'C3A2': 'C3-M2',
    'C4A1': 'C4-M1',
    'O1A2': 'O1-M2',
    'O2A1': 'O2-M1',

    'F3-REF': 'F3',
    'F4-REF': 'F4',
    'C3-REF': 'C3',
    'C4-REF': 'C4',
    'O1-REF': 'O1',
    'O2-REF': 'O2',
    'M1-REF': 'M1',
    'M2-REF': 'M2',

    'F3M2': 'F3-M2',
    'F4M1': 'F4-M1',
    'C3M2': 'C3-M2',
    'C4M1': 'C4-M1',
    'O1M2': 'O1-M2',
    'O2M1': 'O2-M1',
    'FP1': 'Fp1',
    'FP2': 'Fp2',
    'FPZ': 'FpZ',
    'EKG': 'ECG',
    'EKG1': 'ECG1',
    'EKG2': 'ECG2',
    'EMG_X': 'EMG_x',
    'EMG_Y': 'EMG_y',
    'EMG-EMG': 'EMG_x-EMG_y',
    'MILO': 'CHIN',
    'DELTOIDE': 'Deltoide',
    'EOGSIN': 'EOG_L',
    'EOGDX': 'EOG_R',
    'EOG-L': 'EOG_L',
    'EOG-R': 'EOG_R',
    'LOC': 'EOG_L',
    'ROC': 'EOG_R',
    # 'E1-M2'             : 'EOG_L',
    # 'E2-M2'             : 'EOG_R',
    'LEFTELECTROOCUL': 'EOG_L',
    'RIGHTELECTROOCU': 'EOG_R',
    'HEARTRATEVARIA': 'HR',
    'PLETH': 'Pleth',
    'CHEST': 'Thorax',
    'THORAX': 'Thorax',
    'TORACE': 'Thorax',
    'TORACICO': 'Thorax',
    'ABDOMEN': 'Abdomen',
    'ADDDOME': 'Abdomen',
    'ADDOME': 'Abdomen',
    'ABDO': 'Abdomen',
    'FLOW': 'Flow',
    'FLUSSO': 'Flow',
    'CANNULA': 'Cannula',
    'CANULA': 'Cannula',
    'FLATTENING': 'Cannula',
    'TERMISTORE': 'THE',
    'THERMISTOR': 'THE',
    'POSITION': 'Position',
    'POSIZIONE': 'Position',
    'OXSTATUS': 'STAT_SpO2',
    'STAT': 'STAT_SpO2',
    'SAO2': 'SpO2',
    'SPO2': 'SpO2',
    'SOUND': 'MIC',
    'LEG': 'Leg',
    'SX1': 'TIB_L1',
    'SX2': 'TIB_L2',
    'TIBSX': 'TIB_L',
    'TIBSIN': 'TIB_L',
    'DX1': 'TIB_R1',
    'DX2': 'TIB_R2',
    'TIBDX': 'TIB_R',
}
synonyms.update(**{
    left.upper() + right.upper(): f"{left}-{right}"
    for left in channel_labels_by_type['EEG']
    for right in channel_labels_by_type['EEG']
})

channel_type_by_label: Dict[str, str] = {}
for channel_type, channels in channel_labels_by_type.items():
    channel_type_by_label.update({ch: channel_type for ch in channels})

_conversion_map = {
    'uVuV': 1.0,
    'mVmV': 1.0,
    'uVmV': 10**-3,
    'mVuV': 10**3
}


def convert_units(in_unit, out_unit):
    return _conversion_map[in_unit+out_unit]
