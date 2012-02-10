from string import split

if __name__ == "__main__":
    
    word_counts = {}

    # Prompt for file

    filename = str(raw_input("Enter filename: "))

    # Open file, tally word occurrences

    f = open(filename)
    for line in f:
        for token in split(line):
            if word_counts.has_key(token):
                word_counts[token] += 1
            else:
                word_counts[token] = 1
    f.close()

    # Sort by word

    for (k, v) in sorted(word_counts.iteritems()):
        print("{0} {1}").format(k, v)

    print("There are {0} words in this file").format(len(word_counts))