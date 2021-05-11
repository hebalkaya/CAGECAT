def create_empty_dict_of_labels(filename):
    new = {}

    with open(filename) as inf:
        labels = [line.strip() for line in inf.readlines()]

    for l in labels:
        new[l] = {"title": "TODO",
                  "module": "TODO",
                  "text": "TODO"}
        # TODO: potentially more at text
    print(new)
    return new

create_empty_dict_of_labels('not_registered_helps.txt')