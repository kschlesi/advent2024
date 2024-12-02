
def safety_check(report, dampen = False):
    '''determines whether a report (list of n integer levels) is safe (boolean True) or unsafe (False)
       if dampen = True, also checks each sub-report of length n-1 created by removing one level
    '''
    is_safe_full = is_safe(report)
    if dampen and not is_safe_full:
        return any([is_safe(report[:i]+report[i+1:]) for i in range(len(report))])
    return is_safe_full   


def is_safe(report):
    '''determines whether a report (list of integer levels) is safe (boolean True) or unsafe (False)
       To be safe, both of the following must be true:
       - The levels are either all increasing or all decreasing.
       - Any two adjacent levels differ by at least one and at most three.
    '''
    # calculate differences between levels
    differences = [level - report[i+1] for i, level in enumerate(report) if i+1 < len(report)]
    
    # check that all differences are the same sign
    sign_condition = [d == abs(d) for d in differences]
    if not len(list(set(sign_condition))) == 1:
        return False

    # check that all differences meet the size limits
    value_condition = [d for d in differences if not 0 < abs(d) < 4]
    if len(value_condition) > 0:
        return False
    
    return True


if __name__ == "__main__":
    
    # read data
    with open('input.txt','r') as f:
        reports = [[int(level) for level in row.split(' ')] for row in f]
        
    # determine safety
    print(sum([safety_check(report, True) for report in reports]))