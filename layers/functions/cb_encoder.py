import json

with open('layers/database/postgres/data/mapping.json') as f:
    mapping = json.load(f)


def encode_table(table_name: str) -> str:
    encoded_table = [k for k, v in mapping['table'].items() if v == table_name.lower()]
    if not encoded_table:
        raise ValueError(f"Table name '{table_name}' not found in mapping.")
    return encoded_table[0]


def encode_group_subject(group_subject_name: str) -> str:
    encoded_group_subject = [k for k, v in mapping['group'].items() if v == group_subject_name.lower()]
    if not encoded_group_subject:
        raise ValueError(f"Group name '{group_subject_name}' not found in mapping.")
    return encoded_group_subject[0]


def encode_subject(subject_name: str) -> str:
    encoded_subject = [k for k, v in mapping['subject'].items() if v == subject_name.lower()]
    if not encoded_subject:
        raise ValueError(f"Subject name '{subject_name}' not found in mapping.")
    return encoded_subject[0]
