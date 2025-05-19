# convert_utf16_to_utf8.py
with open("db.json", "r", encoding="utf-16") as f_in:
    data = f_in.read()

with open("db_utf8.json", "w", encoding="utf-8") as f_out:
    f_out.write(data)
