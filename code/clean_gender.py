import sys

def main():
    print "Starting...\n"
    infile = sys.argv[1]
    outfile = sys.argv[2]
    common_file = sys.argv[3]
    gender_in = sys.argv[4]
    common_names = {}
    
    with open(common_file, 'r') as f:
        for line in f:
            rows = line.split(',')
            common_names[rows[0]] = rows[1].strip()

    with open(infile, 'r') as f:
        for line in f:
            cleaned_name = line.lower()
            cleaned_name = cleaned_name.strip()
            g = common_names.get(cleaned_name, gender_in)
            if g == gender_in:
                with open(outfile, 'a') as f:
                    f.write(cleaned_name)
                    f.write("\n")
    print "Done cleaning"


if __name__ == '__main__':
    error_message = "Usage: python clean_gender.py <input_file> <output_file> \n"
    if len(sys.argv) != 5:
        print (error_message)
        exit()
    main()
