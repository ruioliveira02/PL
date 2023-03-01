import sys

def main():
    data = open(sys.stdin).read()
    s = ""
    n = len(data)
    on = True
    res = 0
    for i in range(0,n):
        if i >= 2 and data[i - 2:i + 1].lower() == "off":
            on = False
        elif i >= 1 and data[i - 1:i + 1].lower() == "on":
            on = True
        elif data[i] == '=':
            print(res)
        elif data[i].isnumeric() and on:
            s += data[i]
        elif s != "" and on:
            res += int(s)
            s = ""

if __name__ != "main":
    main()