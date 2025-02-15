import os
import re

pattern = re.compile(r"^(.*) \((\d+)\)(\..+)$")

for filename in os.listdir():
    print(filename)
    match = pattern.match(filename)
    if match:
        base_name, number, extension = match.groups()
        new_name = f"{base_name}({number}){extension}"

        os.rename(filename, new_name)
        print(f"Renamed: {filename} → {new_name}")

print("✅ Renaming complete!")
