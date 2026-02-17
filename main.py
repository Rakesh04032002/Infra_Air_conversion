import json
import re
import os

# Regex pattern (case-insensitive)
FILE_PATTERN = re.compile(r'\b[\w./\\-]+\.(ksh|btq)\b', re.IGNORECASE)


# -------------------------------
# Normalize Path (for comparison only)
# -------------------------------
def normalize_path(path):
    path = path.replace("\\", "/")
    path = os.path.normpath(path)
    return path.lower()


# -------------------------------
# Extract from JSON
# -------------------------------
def extract_from_json(json_file):
    ksh_files = {}
    btq_files = {}

    with open(json_file, 'r') as f:
        data = json.load(f)

    def recursive_search(obj):
        if isinstance(obj, dict):
            for value in obj.values():
                recursive_search(value)
        elif isinstance(obj, list):
            for item in obj:
                recursive_search(item)
        elif isinstance(obj, str):
            for match in re.finditer(FILE_PATTERN, obj):
                original = match.group(0)
                normalized = normalize_path(original)

                if normalized.endswith(".ksh"):
                    ksh_files[normalized] = original
                elif normalized.endswith(".btq"):
                    btq_files[normalized] = original

    recursive_search(data)
    return ksh_files, btq_files


# -------------------------------
# Extract from PARAM
# -------------------------------
def extract_from_param(param_file):
    param_files = {}

    with open(param_file, 'r') as f:
        content = f.read()

        for match in re.finditer(FILE_PATTERN, content):
            original = match.group(0)
            normalized = normalize_path(original)
            param_files[normalized] = original

    return param_files


# -------------------------------
# Pretty Print Comparison
# -------------------------------
def compare_json_with_param(json_name, json_ksh, json_btq, param_files):

    json_all = {**json_ksh, **json_btq}
    param_all = param_files

    json_set = set(json_all.keys())
    param_set = set(param_all.keys())

    common = json_set & param_set
    only_json = json_set - param_set
    only_param = param_set - json_set

    print("\n===================================================")
    print(f"Comparing File: {json_name}")
    print("===================================================")

    # ----------- Print Extracted Files -----------
    print("\n--- All .ksh files in JSON ---")
    if json_ksh:
        for v in sorted(json_ksh.values()):
            print("  ", v)
    else:
        print("   No .ksh files found")

    print("\n--- All .btq files in JSON ---")
    if json_btq:
        for v in sorted(json_btq.values()):
            print("  ", v)
    else:
        print("   No .btq files found")

    # ----------- Comparison Section -----------
    print("\n---------------- Comparison Result ----------------")

    if common:
        print("\n✅ Common Dependencies:")
        for key in sorted(common):
            print("  JSON :", json_all[key])
            print("  PARAM:", param_all[key])
            print("  ---")
    else:
        print("\nNo Common Dependencies")

    if only_json:
        print("\n⚠ Dependencies Only in JSON:")
        for key in sorted(only_json):
            print("  ", json_all[key])

    if only_param:
        print("\n⚠ Dependencies Only in PARAM:")
        for key in sorted(only_param):
            print("  ", param_all[key])

    print("---------------------------------------------------\n")


# -------------------------------
# MAIN
# -------------------------------
if __name__ == "__main__":

    # You can give one or multiple JSON files here
    json_files = [
        "input.json",
        "inp.json"
        # "input2.json
        # ",
        # "input3.json"
    ]

    param_file = "input.param"

    # Extract param once
    param_dependencies = extract_from_param(param_file)

    # Process each JSON separately
    for json_file in json_files:
        ksh, btq = extract_from_json(json_file)
        compare_json_with_param(json_file, ksh, btq, param_dependencies)
