import json
import re

# Case-insensitive pattern
FILE_PATTERN = re.compile(r'\b[\w./\\-]+\.(ksh|btq)\b', re.IGNORECASE)


# -------------------------------
# Extract from JSON
# -------------------------------
def find_files_in_json(json_file):
    found_files = {}  # key = lowercase, value = original

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
                found_files[original.lower()] = original

    recursive_search(data)

    if not found_files:
        print("No .ksh or .btq files present in JSON")
    else:
        print("\nFiles found in JSON:")
        for file in sorted(found_files.values()):
            print(file)

    return set(found_files.keys())  # return lowercase for comparison


# -----------------------------------
# Extract from PARAM file
# -----------------------------------
def find_files_in_param(param_file):
    found_files = {}

    with open(param_file, 'r') as f:
        content = f.read()

        for match in re.finditer(FILE_PATTERN, content):
            original = match.group(0)
            found_files[original.lower()] = original

    if not found_files:
        print("No .ksh or .btq files present in Param file")
    else:
        print("\nFiles found in Param file:")
        for file in sorted(found_files.values()):
            print(file)

    return set(found_files.keys())


# -----------------------------------
# Compare Dependencies
# -----------------------------------
def compare_dependencies(json_file, param_file):
    json_files = find_files_in_json(json_file)
    param_files = find_files_in_param(param_file)

    if not json_files and not param_files:
        print("\nNo .ksh or .btq files present in both files")
        return

    common = json_files.intersection(param_files)
    only_json = json_files - param_files
    only_param = param_files - json_files

    print("\n--- Comparison Result ---")

    if common:
        print("\nCommon dependencies:")
        for file in sorted(common):
            print(file)
    else:
        print("\nNo common dependencies found")

    if only_json:
        print("\nDependencies only in JSON:")
        for file in sorted(only_json):
            print(file)

    if only_param:
        print("\nDependencies only in Param file:")
        for file in sorted(only_param):
            print(file)


# -----------------------------------
# Main
# -----------------------------------
if __name__ == "__main__":
    json_path = "input.json"
    param_path = "input.param"

    compare_dependencies(json_path, param_path)
