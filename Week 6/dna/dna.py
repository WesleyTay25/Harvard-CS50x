import csv
import sys


def main():

    # TODO: Check for command-line usage
    if len(sys.argv) != 3:
        print("Please enter only 2 arguments!")
        sys.exit(1)
    else:
        csvfile = sys.argv[1]
        txtfile = sys.argv[2]
    # TODO: Read database file into a variable

    # CSV
    csvrows = []
    header = []
    with open(csvfile, "r") as csv_file:
        csvreader = csv.DictReader(csv_file)
        for row in csvreader:
            csvrows.append(row)  # list of dictionaries
        header.append(csvreader.fieldnames)
        del header[0][0]  # remove name column

    # make header 1D
    subsequences = []
    for row in header:
        for i in row:
            subsequences.append(i)  # one dimensional row

    # TODO: Read DNA sequence file into a variable
    # TXT
    with open(txtfile, "r") as txt_file:
        txtreader = csv.reader(txt_file)
        txtreader = list(txtreader)

    sequence = []
    for row in txtreader:
        for i in row:
            sequence.append(i)  # one dimensional row

    # TODO: Find longest match of each STR in DNA sequence
    number = []
    for i in range(len(subsequences)):
        max = longest_match(sequence[0], subsequences[i])
        number.append(max)

    # TODO: Check database for matching profiles
    for i in csvrows:  # iterate through dictionaries
        new = []
        match = 0

        for occurences in i.values():
            new.append(occurences)  # create new list of matches
        del new[0]  # get rid of name column

        for j in range(len(new)):
            if int(new[j]) == number[j]:  # compare matches
                match += 1
        if match == len(new):  # if all columns matches
            print(i["name"])
            break
    print("No match")
    return


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
