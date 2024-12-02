if __name__ == "__main__":
    
    # read data
    with open('input.txt','r') as f:
        data = [row.split('   ') for row in f]
        
    # process and sort the two lists
    list1 = sorted([int(pair[0]) for pair in data])
    list2 = sorted([int(pair[1]) for pair in data])
    
    # calculate sum of lengths
    lengths = [abs(int(pair[0]) - int(pair[1])) for pair in zip(list1, list2)]
    print(sum(lengths))

    # calculate the simlarity score
    sims = [entry * list2.count(entry) for entry in list1]
    print(sum(sims))