import numpy as np

class Map(np.ndarray):
    def __new__(cls, map_array):
        obj = np.asarray(map_array).view(cls)
        obj.length, obj.width = map_array.shape
        # obj.guard_state = obj.find_guard()
        return obj
    
    def find_guard(self):
        guard_directions = ['^','>','v','<']
        return [(dir, x) for dir in guard_directions for x in np.argwhere(self==dir)][0]
    
    
    






class guard_state():




def next_direction(dir):
    directions = ['^','>','v','<']
    return directions[(directions.index(dir) + 1) % len(directions)]

def previous_direction(dir):
    directions = ['^','>','v','<']
    return directions[(directions.index(dir) - 1) % len(directions)]

def take_step()
    


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
    map = Map(rows)
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
    # for all steps with dir '<' and guard location [x, y]:
    # find subsequent steps with direction 'v' and location [x, y'>=y]
    path_length = len(guard_path)
    print(path_length)
    opps = [ (i, guard_path[i][0], [guard_path[i][1][0], guard_path[i][1][1]], j, guard_path[j][0], [guard_path[j][1][0], guard_path[j][1][1]]) 
                for i in range(path_length) 
                for j in range(i+1, path_length) 
                if (
                    (guard_path[i][0]=='<' and guard_path[j][0]=='v' and guard_path[i][1][0]==guard_path[j][1][0] and guard_path[i][1][1]<=guard_path[j][1][1] 
                     and not '#' in (list(map[guard_path[j][1][0]+1, guard_path[j][1][1]]) + list(map[guard_path[j][1][0], guard_path[i][1][1]:guard_path[j][1][1]])) 
                    ) or
                    (guard_path[i][0]=='>' and guard_path[j][0]=='^' and guard_path[i][1][0]==guard_path[j][1][0] and guard_path[i][1][1]>=guard_path[j][1][1]
                    ) or
                    (guard_path[i][0]=='v' and guard_path[j][0]=='>' and guard_path[i][1][0]>=guard_path[j][1][0] and guard_path[i][1][1]==guard_path[j][1][1]
                    ) or
                    (guard_path[i][0]=='^' and guard_path[j][0]=='<' and guard_path[i][1][0]<=guard_path[j][1][0] and guard_path[i][1][1]==guard_path[j][1][1]
                    )
                )       
            ]
    print(len(opps))
    print(len(list(set(['{}|{}|{}'.format(opp[4], opp[5][0], opp[5][1]) for opp in opps])))) # 800 the old way

    # print(len(list(set(opps))))
    print(opps[:10])

    # .....OR it can be one turn away from that spot Dx
    # for all steps with guard location [x, y]:
    #     if direction '>': 
    #         find subsequent steps with direction '^' and location [x, y'<=y]. these are candidates
    #         for all existing obstacles at locations [x''=x-1, y''<=y]: treat as a new step with direction '^' and location [x, y'']. repeat search.
    #  


    def search(stepN):
        find all stepM such that:
            - M > N
            - turn(M) pointsAt N (without blocks!)
            - step(M) != '#'
        for each '#' along the trailing line of stepN:
            - construct stepP
            - search(stepP) 


    


        
        


    

            
    

    
    