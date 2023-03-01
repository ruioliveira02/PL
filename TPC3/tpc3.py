import re
import json

def split_name(name):
    first_name = re.match(r"\w+\b", name).group()
    last_name = re.search(r"\b\w+$", name).group()

    return first_name, last_name

def parse(path):
    with open(path) as f:
        lines = f.readlines()
        regex_str = r"(?P<processes>\d+)::(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})::(?P<name1>[a-zA-Z ]+)::(?P<name2>[a-zA-Z ]+)::(?P<name3>[a-zA-Z ]+)::(?P<extra>[^:]*)::"
        res = []
        regex = re.compile(regex_str)

        for line in lines:
            if match := regex.finditer(line):
                res = res + [m.groupdict() for m in match]

    return res


def frequency_per_year(data):
    ans = {}
    for entry in data:
        if entry["year"] not in ans:
            ans[entry["year"]] = 0

        ans[entry["year"]] += 1

    return ans

def name_frequency(data, century, idx, cutoff=5):
    names = {}

    for entry in data:
        if (int(entry["year"]) - 1) // 100 + 1 != century:
            continue
        for i in range(1,4):
            name = split_name(entry["name" + str(i)])
            if name[idx] not in names:
                names[name[idx]] = 0

            names[name[idx]] += 1

    sorted_names = sorted(names.items(), key=lambda x:x[1])
    print(sorted_names)
    return sorted_names[:cutoff]

def names_per_century(data,cutoff=5):
    first_names = {}
    last_names = {}
    for i in range(1,22):
        first_names[i] = name_frequency(data, i, 0,cutoff)
        last_names[i] = name_frequency(data, i, 0,cutoff)

    return first_names, last_names

def relationship_frequency(data):
    ans = {
        "pai": 0,
        "mae": 0,
        "tio": 0,
        "tia": 0,
        "irmao": 0,
        "irma": 0,
        "avo": 0,
        "primo": 0,
        "prima": 0
    }
    regex = re.compile(r"\b(?:pai|mae|tio|tia|irmao|irma|avo|primo|prima)\b", flags=re.IGNORECASE)

    for entry in data:
        if match := regex.search(entry["extra"]):
            ans[match.group().lower()] += 1

    return ans

def convert_to_json(data, file, number=20):
    with open(file, "w") as f:
        content = json.dump(data, f)

def main():
    data = parse("dados.txt")
    print(frequency_per_year(data))
    print(names_per_century(data))
    print(relationship_frequency(data))
    convert_to_json(data, "resultado.json")

if __name__ != "main":
    main()