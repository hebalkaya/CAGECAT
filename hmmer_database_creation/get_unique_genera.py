from sys import argv

def write_unique_genera():
    with open(argv[1]) as inf:
        all_lines = inf.readlines()

    all_genera = []
    for line in all_lines:
        genus = line.strip().split()[0]

        if genus not in all_genera:
            all_genera.append(genus)

    print(f"{len(all_genera)} genera found")

    with open(argv[2], 'w') as outf:
        for g in all_genera:
            outf.write(f'{g}\n')

write_unique_genera()
