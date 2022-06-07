import timeit
import argparse

def main():
    """
	Given two files to compare, run them using the timit package n times, then report of the resulting average run time of
	each file, the time difference, and the time factor increase or decrease of file1_time/file2_time
    """

    argparser = argparse.ArgumentParser(description='Enter two filenames to compare time')
    argparser.add_argument('f1', type=str, help='file 1 to compare')
    argparser.add_argument('f2', type=str, help='file 2 to compare')
    argparser.add_argument('n', type=int, help='number of runs')
    args = argparser.parse_args()

    with open(args.f1, "r") as source:
        text1 = source.read()

    with open(args.f2, "r") as source:
        text2 = source.read()

    time1 = timeit.timeit(text1, number=args.n)
    time2 = timeit.timeit(text2, number=args.n)
    time1 /= args.n
    time2 /= args.n
    difference = abs(time1 - time2)
    factor_diff = '{:.20f}'.format(time1 / time2)
    time1 = '{:.20f}'.format(time1)
    time2 = '{:.20f}'.format(time2)
    difference = '{:.20f}'.format(difference)
    print("average time for", args.f1, ':', time1, 's')
    print("average time for", args.f2, ':', time2, 's')
    print("time difference between two files:", difference)
    print("time factor difference", factor_diff)


if __name__ == "__main__":
    main()
