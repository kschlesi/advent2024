import re

def calculate_mul(input):
    matches = re.findall(r'mul\((\d+),(\d+)\)', input)
    return sum([int(a) * int(b) for (a,b) in matches])

if __name__ == "__main__":
    
    # read data
    with open('input.txt','r') as f:
        input = f.read()

    # print(calculate_mul(input))
    
    chunks = [on_chunk.split('don\'t()')[0] for on_chunk in input.split('do()')]

    print(sum([calculate_mul(chunk) for chunk in chunks]))
