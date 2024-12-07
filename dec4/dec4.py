import numpy as np

def search_array(input, target):
    target_length = len(target)
    input_length = len(input)
    # print(input_length)
    hits = [
        int(sum(input[i:i+target_length]==target)==target_length)
        for i, a in enumerate(input) 
        if i < input_length - target_length + 1
    ]
    # if any(hits):
    #    print(input)
    #    print([int(hit) for hit in hits])
    #    print([input[i:i+target_length] for i, hit in enumerate(hits) if hit])
    return hits

if __name__ == "__main__":
    # read data into array
    with open('input.txt','r') as f:
        rows = [[c for c in line.strip()] for line in f]
    word_search = np.array(rows)
    length, width = word_search.shape
    
    ## PART 1
    # define target subarray to find
    target = np.array(['X','M','A','S'])

    print(word_search.shape)
    # print(word_search)

    # search in each of 8 directions
    dir1 = [sum(search_array(row, target)) for row in word_search]
    dir2 = [sum(search_array(row[::-1], target)) for row in word_search]
    dir5 = [sum(search_array(word_search.diagonal(i), target)) for i in range(-1*length+1, length-1)]
    dir6 = [sum(search_array(word_search.diagonal(i)[::-1], target)) for i in range(-1*length+1, length-1)]
    
    word_search_transpose = word_search.T
    # print(word_search_transpose)
    dir3 = [sum(search_array(col, target)) for col in word_search_transpose]
    dir4 = [sum(search_array(col[::-1], target)) for col in word_search_transpose]

    word_search_flip = np.fliplr(word_search)
    # print(word_search_flip)
    dir7 = [sum(search_array(word_search_flip.diagonal(i), target)) for i in range(-1*width+1, width-1)]
    dir8 = [sum(search_array(word_search_flip.diagonal(i)[::-1], target)) for i in range(-1*width+1, width-1)]
    
    print(sum(dir1+dir2+dir3+dir4+dir5+dir6+dir7+dir8))

    ## PART 2
    target2 = np.array(['M','A','S'])
    finds = np.zeros((length, width))

    # search in first diagonal direction
    down_diags = [
        [0] + search_array(word_search.diagonal(i), target2)
        for i in range(-1*length+1, length-1)
    ]
    up_diags = [
        [0] + search_array(word_search.diagonal(i)[::-1], target2)
        for i in range(-1*length+1, length-1)
    ]
    diags = [
        (i, np.pad(down_diag, (0, length - abs(i) - len(down_diag))) 
            + np.pad(up_diag, (0, length - abs(i) - len(up_diag)))[::-1])
        for i, down_diag, up_diag in zip(range(-1*length+1, length-1), down_diags, up_diags)
    ]
    [np.fill_diagonal(finds[-1*i:,:length+i], diag) for i, diag in diags if i<0]
    [np.fill_diagonal(finds[:length-i,i:], diag) for i, diag in diags if i>=0]

    # search in second diagonal direction
    finds_flip = np.zeros((length, width))
    down_diags_flip = [
        [0] + search_array(word_search_flip.diagonal(i), target2)
        for i in range(-1*length+1, length-1)
    ]
    up_diags_flip = [
        [0] + search_array(word_search_flip.diagonal(i)[::-1], target2)
        for i in range(-1*length+1, length-1)
    ]
    diags_flip = [
        (i, np.pad(down_diag, (0, length - abs(i) - len(down_diag))) 
            + np.pad(up_diag, (0, length - abs(i) - len(up_diag)))[::-1])
        for i, down_diag, up_diag in zip(range(-1*length+1, length-1), down_diags_flip, up_diags_flip)
    ]
    [np.fill_diagonal(finds_flip[-1*i:,:length+i], diag) for i, diag in diags_flip if i<0]
    [np.fill_diagonal(finds_flip[:length-i,i:], diag) for i, diag in diags_flip if i>=0]

    # print(finds)
    # print(np.fliplr(finds_flip))
    # print((finds + np.fliplr(finds_flip))>1)
    print(sum(sum((finds + np.fliplr(finds_flip))>1)))
    