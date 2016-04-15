import re

def get_size_from_size_str(size_str):
    pattern = re.compile('(\d+\.*\d*)(.*)')
    match = pattern.match(size_str)
    if match:
        size = float(match.groups()[0])
        size_type = match.groups()[1]
        if 'm' in size_type or 'M' in size_type:
            size = size / 1000
        print size

if __name__ == '__main__':
    import sys
    size_str = sys.argv[1]
    get_size_from_size_str(size_str)
