import numpy as np

def find_guard(map):
    guard_directions = ['^','>','v','<']
    return [(dir, x) for dir in guard_directions for x in np.argwhere(map==dir)][0]

def patrol_step(map):
    dir, guard = find_guard(map)
    new_dir = dir
    new_guard = guard.copy()

    # evaluate next action based on current direction
    if dir=='^':
        if guard[0] == 0:                       # last step; finish
            map[guard[0], guard[1]] = 'X'
            new_guard[0] = guard[0]-1
            return new_dir, new_guard, map
        elif map[guard[0]-1,guard[1]] == '#':   # obstruction; turn
            new_dir = '>'
        else:                                   # take a step
            new_guard[0] = guard[0]-1
    elif dir=='>':
        if guard[1]+1 == width:                 # last step; finish
            map[guard[0], guard[1]] = 'X'
            new_guard[1] = guard[1]+1
            return new_dir, new_guard, map
        elif map[guard[0],guard[1]+1] == '#':   # obstruction; turn
            new_dir = 'v'
        else:                                   # take a step
            new_guard[1] = guard[1]+1
    elif dir=='v':
        if guard[0]+1 == length:                # last step; finish
            map[guard[0], guard[1]] = 'X'
            new_guard[0] = guard[0]+1
            return new_dir, new_guard, map
        elif map[guard[0]+1,guard[1]] == '#':   # obstruction; turn
            new_dir = '<'
        else:                                   # take a step
            new_guard[0] = guard[0]+1
    elif dir=='<':
        if guard[1] == 0:                       # last step; finish
            map[guard[0], guard[1]] = 'X'
            new_guard[1] = guard[1]-1
            return new_dir, new_guard, map
        if map[guard[0],guard[1]-1] == '#':     # obstruction; turn
            new_dir = '^'
        else:                                   # take a step
            new_guard[1] = guard[1]-1
    
    # if a step was taken, leave an X behind and put guard in new position
    if new_dir==dir:
        map[new_guard[0], new_guard[1]] = dir
        map[guard[0], guard[1]] = 'X'
    
    # if a turn was made, update the guard's direction
    else:
        map[guard[0], guard[1]] = new_dir
    
    # return updated direction, guard position, and map
    return new_dir, new_guard, map


if __name__ == "__main__":

    # read data into array
    with open('input.txt','r') as f:
        rows = [[c for c in line.strip()] for line in f]
    map = np.array(rows)
    length, width = map.shape
    print(map)
    print(map.shape)
    
    # simulate guard walk
    dir, guard = find_guard(map)
    guard_path = [(dir, guard)]
    while 0 <= guard[0] < length and 0 <= int(guard[1]) < width:
        dir, guard, map = patrol_step(map)
        guard_path.append((dir, guard))
        # print(dir, guard)

    print(len(np.argwhere(map=='X')))

    # in order to create a loop, the path must repeat.
    # this means the guard is in the same cell they were in earlier and facing the same direction.
    # opportunites to create this with a single obstruction occur when:
    # (1) guard is in the same row or column they were in at earlier step N
    # (2) guard's current direction + 90 degrees is the same as the direction they were facing at earlier step N
    # (3) guard's current column or row is ahead or behind of that at earlier step N, as appropriate
    
    # FINDING REPEAT OPPORTUNITIES:
    # for all steps with dir '^' and guard location [x, y]:
    # find previous steps with direction '>' and location [x, y'>=y]
    opps = [ (j, dirj, guardj, i, diri, guardi) 
                for j, (dirj, guardj) in enumerate(guard_path) 
                for i, (diri, guardi) in enumerate(guard_path) 
                 if i<j and (
                    (dirj=='^' and diri=='>' and guardi[0]==guardj[0] and guardi[1]>=guardj[1]) or
                    (dirj=='>' and diri=='v' and guardi[0]>=guardj[0] and guardi[1]==guardj[1]) or
                    (dirj=='v' and diri=='<' and guardi[0]==guardj[0] and guardi[1]<=guardj[1]) or
                    (dirj=='<' and diri=='^' and guardi[0]<=guardj[0] and guardi[1]==guardj[1])
                )       
            ]
    print(len(opps))

    # for all steps with dir '>' and guard location [x, y]:
    # find previous steps with direction 'v' and location [x'>=x, y]
    # oppsE = [ j for j, (dirj, guardj) in enumerate(guard_path) for i, (diri, guardi) in enumerate(guard_path) if i<j and dirj=='>' and diri=='v' and guardi[0]>=guardj[0] and guardi[1]==guardj[1] ]
    # print(len(oppsE))

    # for all steps with dir 'v' and guard location [x, y]:
    # find previous steps with direction '<' and location [x, y'<=y]
    # oppsS = [ j for j, (dirj, guardj) in enumerate(guard_path) for i, (diri, guardi) in enumerate(guard_path) if i<j and dirj=='v' and diri=='<' and guardi[0]==guardj[0] and guardi[1]<=guardj[1] ]
    # print(len(oppsS))

    # for all steps with dir '<' and guard location [x, y]:
    # find previous steps with direction '^' and location [x'<=x, y]
    # oppsW = [ j for j, (dirj, guardj) in enumerate(guard_path) for i, (diri, guardi) in enumerate(guard_path) if i<j and dirj=='<' and diri=='^' and guardi[0]<=guardj[0] and guardi[1]==guardj[1] ]
    # print(len(oppsW))

    # print(len(list(set(opps))))
    print(opps[:10])

    # .....OR it can be one turn away from that spot Dx
    # for all steps with guard location [x, y]:
    #     if direction '>': 
    #         find subsequent steps with direction '^' and location [x, y'<=y]. these are candidates
    #         for all existing obstacles at locations [x''=x-1, y''<=y]: treat as a new step with direction '^' and location [x, y'']. repeat search.
    #  



    


        
        


    

            
    

    
    