import json

table_1 = [
    {"name": "Miku", "voicebank": "VOCALOID2", "codename": "CV01", "number": "02"},
]

table_2 = [
    {"name": "Teto", "voicebank": "VOCALOID3", "codename": "CV02", "number": "none"},
]

table_3 = [
    {"name": "Nero", "voicebank": "VOCALOID4", "codename": "CV03", "number": "none"},
]

tables = {
    "Vocaloid1": table_1,
    "Vocaloid2": table_2,
    "Vocaloid3": table_3,
}
save_to_tables= ["Vocaloid1", "Vocaloid2", "Vocaloid3"]

for table_name in save_to_tables:
    if table_name in tables:
        with open(f"{table_name}.json", "w", encoding="utf-8") as f:
            json.dump(tables[table_name], f, ensure_ascii=False, indent=2)
