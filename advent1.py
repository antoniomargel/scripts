def parse_line(file):
    password = list()
    for line in open(file):
        line = line.strip()
        password.append([line[0], line[1:]])
    return password

def dial(password):
    pos = 50
    count = 0
    for i in password:
        if i[0] == "L":
            pos = (pos - int(i[1])) % 100
            if pos == 0:
                count += 1
        if i[0] == "R":
            pos = (pos + int(i[1])) % 100
            if pos == 0:
                count += 1
    return count
            
def newdial(password):
    pos = 50
    count = 0
    for i in password:
        if i[0] == "L":
            for j in range(int(i[1])):
                pos = (pos - 1) % 100
                if pos == 0:
                    count += 1
        if i[0] == "R":
            for j in range(int(i[1])):
                pos = (pos + 1) % 100
                if pos == 0:
                    count += 1
    return count

def main():
    password = parse_line("day1.txt")
    print(newdial(password))

if __name__ == "__main__":
    main()