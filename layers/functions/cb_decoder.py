import json

with open('layers/database/postgres/data/mapping.json') as f:
    mapping = json.load(f)


def decode_table(encoded_table: str) -> str:
    decoded_table = mapping['table'].get(encoded_table)
    if not decoded_table:
        raise ValueError(f"encoded_table :'{encoded_table}' not found in mapping.")
    return decoded_table


def decode_group_subject(encoded_group_subject: str) -> str:
    decoded_group_subject = mapping['group'].get(encoded_group_subject)
    if not decoded_group_subject:
        raise ValueError(f"encoded_group :'{encoded_group_subject}' not found in mapping.")
    return decoded_group_subject


def decode_subject(encoded_subject: str) -> str:
    decoded_subject = mapping['subject'].get(encoded_subject)
    if not decoded_subject:
        raise ValueError(f"encoded_subject :'{encoded_subject}' not found in mapping.")
    return decoded_subject
