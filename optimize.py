import argparse
from PatternReplace import parser

def main():
    """
	Given a file to optimize, apply combinations of different patterns replacement using parser.py. Create output files
	named after the pattern that was applied to the file, along with one file where all pattern types were applied.
	"""
    argparser = argparse.ArgumentParser(description='Enter file and optimization type desired')
    argparser.add_argument('f', type=str, help='file to optimize')
    args = argparser.parse_args()

    if args.f[:2] == ".\\":
        newFileName = "opti_" + args.f[2:]
    else:
        newFileName = "opti_" + args.f

    # list comp
    result0 = parser.parseFile(args.f, 0)
    tempFileName = 'comp_' + newFileName
    f = open(tempFileName, "w")
    f.write(result0)
    f.close()
    print("Successfully optimized with list comprehensions: ", tempFileName)

    # append to join
    result1 = parser.parseFile(args.f, 1)
    tempFileName = 'join_' + newFileName
    f = open(tempFileName, "w")
    f.write(result1)
    f.close()
    print("Successfully optimized with join: ", tempFileName)

    # attribute patterns
    result2 = parser.parseFile(args.f, 2)
    tempFileName = 'attr_' + newFileName
    f = open(tempFileName, "w")
    f.write(result2)
    f.close()
    print("Successfully optimized with attribute patterns: ", tempFileName)

    # all
    result3 = parser.parseFile(args.f, 0)
    tempFileName = 'all_' + newFileName
    f = open(tempFileName, "w")
    f.write(result3)
    f.close()
    result3 = parser.parseFile(tempFileName, 1)
    f = open(tempFileName, "w")
    f.write(result3)
    f.close()
    result3 = parser.parseFile(tempFileName, 2)
    f = open(tempFileName, "w")
    f.write(result3)
    f.close()
    print("Successfully optimized with all optimization patterns: ", tempFileName)


if __name__ == "__main__":
    main()
