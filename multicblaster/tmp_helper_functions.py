def create_empty_dict_of_labels(filename):
    new = {}

    with open(filename) as inf:
        labels = [line.strip() for line in inf.readlines()]

    for l in labels:
        new[l] = {"title": "TODO",
                  "text": "TODO"}

    return new