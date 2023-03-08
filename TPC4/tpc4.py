import re
import json

def process_list(str):
    matches = re.findall(r"\d+", str)
    return [int(m) for m in matches]

def compute_aggregates(lst, type):
    if type == "media":
        return sum(lst) / len(lst)

def csv_to_json(src_file, dest_file):
    with open(src_file) as f:
        #Remove line terminators from strings
        csv = [s.strip() for s in f.readlines()]

    header = re.findall(r"(\w+(?:\{\d+(?:,\d+)?\}(?:::\w+)?)?)[,;]?", csv[0])
    lists = {}
    aggregates = {}

    for i in range(0, len(header)):
        if match := re.search(r"(\w+)\{(\d+)(?:,(\d+))?\}(?:::(\w+))?", header[i]):
            header[i] = match.group(1)

            if match.group(3) is None:
                lists[header[i]] = (int(match.group(2)), None)
            else:
                lists[header[i]] = (int(match.group(2)), int(match.group(3)))

            if match.group(4) is not None:
                aggregates[header[i]] = match.group(4)
    regex = ""
    last = False
    for item in header:
        if item in lists:
            last = True

            quantity = f"{{{str(lists[item][0])}{'' if lists[item][1] is None else ','+ str(lists[item][1])}}}"
            regex += f"(?P<{item}>([^,;]+[,;]?){quantity})"
        else:
            last = False
            regex += rf"(?P<{item}>[^,;]+)[,;]"

    # Remove last commas and add new line
    if not last:
        regex = regex[:-4]

    data = []
    for line in csv[1:]:
        matches = re.finditer(regex, line)

        for match in matches:
            data += [match.groupdict()]

    for i in range(0, len(data)):
        for k in data[i]:
            if k in lists:
                data[i][k] = process_list(data[i][k])
            if k in aggregates:
                data[i][k] = compute_aggregates(data[i][k], aggregates[k])
    for k in aggregates:
        for i in range(0, len(data)):
            data[i][f"{k}_{aggregates[k]}"] = data[i][k]
            del data[i][k]

    with open(dest_file, "w") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def main():
    csv_to_json("csv/alunos2.csv", "json/alunos2.json")

if __name__ != "main":
    main()