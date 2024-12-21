import sys
from function.dir_blast import parse_arguments, run_blast

def main():
    print("--------------------------------------------------------------")
    print("|      _   _                  _       _                 _    |")
    print("|   __| | (_)  _ __          | |__   | |   __ _   ___  | |   |")
    print("|  / _` | | | | '__|  _____  | '_ \  | |  / _` | / __| | __| |")
    print("| | (_| | | | | |    |_____| | |_) | | | | (_| | \__ \ | |_  |")
    print("|  \__,_| |_| |_|            |_.__/  |_|  \__,_| |___/  \__| |")
    print("--------------------------------------------------------------")
    
    if len(sys.argv) == 1:
        sys.argv.append('-h')
    
    args = parse_arguments()
    run_blast(args.url, args.wordlist, args.threads)

if __name__ == "__main__":
    main()