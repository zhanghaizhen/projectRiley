import os
import sys
import random
import shutil


def list_files(path):
    '''
    returns a list of names (with extension, without full path) of all files in folder path
    '''
    files = []
    for name in os.listdir(path):
        if os.path.isfile(os.path.join(path, name)):
            files.append(os.path.join(path, name))
    return files


def copy_files(input_f, output_f, num):
    '''
    INPUT: input folder path (str)
           output folder path (str)
           num: number of sample files (int)
    OUTPUT: None

    Copies a sample set of files from input_folder to output_folder
    '''
    files = list_files(input_f)

    rands = random.sample(xrange(len(files)), num)
    for r in rands:
        print "Copying File:{0}".format(files[r])
        shutil.copy2(files[r], output_f)

    print "Done copying {0} files to {1}".format(num, output_f)


def main():
    '''
    Takes 3 command line arguments:
    input_directory_path
    output_directory_path
    number_of_samples
    '''
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    num_samples = int(sys.argv[3])

    copy_files(input_dir, output_dir, num_samples)


if __name__ == '__main__':
    main()
