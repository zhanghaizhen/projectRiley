input_file = 'result.txt'
count = 0

with open(input_file) as infile:
    copy = False
    for line in infile:
        if line.strip() == "content:start:":
            count += 1
            outfile = 'output'+ str(count)+'.html'
            copy = True
        elif line.strip() == "content:end:":
            copy = False
        elif copy:
            with open(outfile, 'a') as out:
                out.write(line)
