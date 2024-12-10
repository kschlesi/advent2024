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
        
        


    

            
    

    
    