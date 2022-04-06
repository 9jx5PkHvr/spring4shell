import sys


def checkPipes(line):
    return (line.count("|") == 8)


def checkStatus(cveFields):
    validValues = ['', 'Vulnerable', 'Fix', 'Workaround', 'Not applicable', 'Not vulnerable',
                   'Under investigation', 'x']
    valid = True

    for field in cveFields:
        if field.strip() not in validValues:
            valid = False
    return valid


def checkLine(line):
    table = line.split("|")
    valid = True
    msg = []

    if not checkPipes(line):
        msg.append("Entry has not correct number of pipes. This will likely destroy the table.")
        valid = False
    if not checkStatus(table[3:4]):
        msg.append("Entry contains incorrect status value. Please check again.")
        valid = False
    return valid, msg


def parseDiff(difffile):
    errors = []

    with(open(difffile, "r")) as f:
        for line in f:
            if (line.startswith("+") and not line.startswith("+++")) or line.startswith(">"):
                valid, msg = checkLine(line)
                if not valid:
                    errors.append((line, msg))
        return errors


def main():
    valid = True

    for difffile in sys.argv[1:]:
        errors = parseDiff(difffile)

        if not errors:
            continue

        valid = False
        print("Error in", difffile)

        for (line, error) in errors:
            print(f"\t, {line}, \t\t, {error}")

    if not valid:
        exit(1)


if __name__ == '__main__':
    main()
