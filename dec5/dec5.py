import math

def is_before(input1, input2, rules):
    before_string = str(input1) + '|' + str(input2)
    return rules[before_string] if before_string in rules.keys() else True

def reverse_rule(rule):
    return '|'.join(rule.split('|')[::-1])

def check_output(example, rules):
    if all([is_before(a, b, rules) for i, a in enumerate(example) for b in example[i + 1:]]):
        return int(example[math.floor(len(example)/2) + len(example)%2 - 1])
    return 0

def rules_sort(example, rules):
    return _sort(example, rules)

def _sort(input, rules):
    # recursive mergesort
    if len(input) <= 1:
        return input
    elif len(input) == 2:
        return (input if is_before(input[0], input[1], rules) else input[::-1])
    else:
        half = math.floor(len(input)/2) + len(input)%2 - 1
        return _merge(_sort(input[:half], rules), _sort(input[half:], rules), rules)

def _merge(input1, input2, rules):
    i1 = 0
    i2 = 0
    merged = []
    while i1 < len(input1) and i2 < len(input2):
        if is_before(input1[i1], input2[i2], rules):
            merged.append(input1[i1])
            i1 = i1+1
        else:
            merged.append(input2[i2])
            i2 = i2+1
    if i1 < len(input1):
        merged.extend(input1[i1:])
    if i2 < len(input2):
        merged.extend(input2[i2:])
    return merged        



if __name__ == "__main__":

    # read data
    rules = {}
    examples = []
    with open('input.txt','r') as f:
        for line in f:
            examples.append(line.strip().split(',')) if ',' in line else rules.update({line.strip(): True})
    
    # finalize rules: add reverse of each rule to rules
    reverse_rules = {}
    [reverse_rules.update({reverse_rule(rule): False}) for rule in rules]
    rules.update(reverse_rules)
    
    # check each example using rules
    output = [check_output(example, rules) for example in examples]
    print(output)
    print(sum(output))

    # sort each example
    sorts = [check_output(rules_sort(example, rules), rules) for example, check in zip(examples, output) if check == 0]
    print(sorts)
    print(sum(sorts))



        
        


    

            
    

    
    