import numpy as np

def next_direction(dir):
    directions = ['^','>','v','<']
    return directions[(directions.index(dir) + 1) % len(directions)]

def previous_direction(dir):
    directions = ['^','>','v','<']
    return directions[(directions.index(dir) - 1) % len(directions)]

class Map(np.ndarray):
    def __new__(cls, map_array):
        obj = np.asarray(map_array).view(cls)
        obj.length, obj.width = obj.shape
        obj.obstacle_list = np.argwhere(obj=='#')
        obj.obstacles = {'{}|{}'.format(int(loc[0]), int(loc[1])): True for loc in obj.obstacle_list}
        return obj
    
    def find_guard(self):
        directions = ['^','>','v','<']
        return [GuardState(dir, [int(loc[0]), int(loc[1])]) for dir in directions for loc in np.argwhere(self==dir)][0]
    
    def in_bounds(self, x, y):
        return 0 <= x < self.length and 0 <= y < self.width
    
    def patrol_step(self):
        guard = self.find_guard()

        # last step; finish
        if not self.in_bounds(guard.next_step().x, guard.next_step().y): 
            self[guard.x, guard.y] = 'X'
            return guard.next_step()
        
        # obstruction; turn
        elif self[guard.next_step().x, guard.next_step().y]=='#':   
            new_guard = guard.turn()
            self[guard.x, guard.y] = new_guard.dir

        # no obstruction; take a step
        else:
            new_guard = guard.next_step()
            self[guard.x, guard.y] = 'X'
            self[new_guard.x, new_guard.y] = new_guard.dir

        return new_guard
    
    def line_of_sight(self, location1, location2):
        if location1[0]==location2[0]:
            return len(np.argwhere(self[location1[0], location2[1]:location1[1]]=='#'))==0
        elif location1[1]==location2[1]:
            return len(np.argwhere(self[location2[0]:location1[0], location1[1]]=='#'))==0
        else:
            return False
    
    def trailing_loop_sites(self, guard):
        if guard.dir=='^':
            # find obstacles to the LEFT (y'=y-1) of current column, BELOW current row (x'>x)
            sites = [GuardState(previous_direction(guard.dir), [loc[0], guard.y])
                    for loc in self.obstacle_list if loc[0]>=guard.x and loc[1]==guard.y-1]
        elif guard.dir=='>':
            # find obstacles ABOVE (x'=x+1) of current column, to LEFT of current col (y'<=y)
            sites = [GuardState(previous_direction(guard.dir), [guard.x, loc[1]])
                    for loc in self.obstacle_list if loc[0]==guard.x-1 and loc[1]<=guard.y]
        elif guard.dir=='v':
            # find obstacles to the RIGHT (y'=y+1) of current column, ABOVE current row (x'<x)
            sites = [GuardState(previous_direction(guard.dir), [loc[0], guard.y])
                    for loc in self.obstacle_list if loc[0]<=guard.x and loc[1]==guard.y+1]
        elif guard.dir=='<':
            # find obstacles BELOW (x'=x-1) of current column, to RIGHT of current col (y'>=y)
            sites = [GuardState(previous_direction(guard.dir), [guard.x, loc[1]])
                    for loc in self.obstacle_list if loc[0]==guard.x+1 and loc[1]>=guard.y]
        else:
            sites = []
        
        return [site for site in sites if '{}|{}'.format(site.x, site.y) not in self.obstacles]
        
    def loop_opportunity_search(self, n, target_guard, guard_path, opps={}, searched={}):
        print(n, target_guard)
        if target_guard.__str__() in searched:
            # print('already searched')
            return opps, searched
        # print('searching...')
        [opps.update({'{}|{}'.format(guard_path[m].next_step().x, guard_path[m].next_step().y): True})
            for m in range(n+1, len(guard_path))
            if guard_path[m].turn().points_at(target_guard, aligned=True)
            and map.line_of_sight(target_guard.location, guard_path[m].location)
            and not '{}|{}'.format(guard_path[m].next_step().x, guard_path[m].next_step().y) in map.obstacles
            ]
        searched.update({target_guard.__str__(): True})
        [self.loop_opportunity_search(n, target_guard, guard_path, opps, searched) for target_guard in map.trailing_loop_sites(guard_path[n])]
        return opps, searched


class GuardState:
    def __init__(self, dir, location):
        self.dir = dir
        self.location = location
        self.x = location[0]
        self.y = location[1]

    def __str__(self):
        return '{} [{}, {}]'.format(self.dir, self.x, self.y)

    def next_step(self):
        '''returns a NEW guard state'''
        if self.dir=='^':
            new_location = [self.x-1, self.y]
        elif self.dir=='>':
            new_location = [self.x, self.y+1]
        elif self.dir=='v':
            new_location = [self.x+1, self.y]
        elif self.dir=='<':
            new_location = [self.x, self.y-1]
        else:
            new_location = self.location
        return GuardState(self.dir, new_location)        
    
    def turn(self):
        '''returns a NEW guard state'''
        return GuardState(next_direction(self.dir), self.location)
    
    def points_at(self, comp_state, aligned=False):
        '''boolean: whether current guard state points at provided comparison state'''
        if self.dir=='^':
            return (self.x >= comp_state.x and self.y == comp_state.y 
                    and (comp_state.dir=='^' if aligned else True))
        elif self.dir=='>':
            return (self.x == comp_state.x and self.y <= comp_state.y 
                    and (comp_state.dir=='>' if aligned else True))
        elif self.dir=='v':
            return (self.x <= comp_state.x and self.y == comp_state.y 
                    and (comp_state.dir=='v' if aligned else True))
        elif self.dir=='<':
            return (self.x == comp_state.x and self.y >= comp_state.y 
                    and (comp_state.dir=='<' if aligned else True))
        else:
            return False


if __name__ == "__main__":

    # read data into array
    with open('input.txt','r') as f:
        rows = [[c for c in line.strip()] for line in f]
    map = Map(rows)
    length, width = map.shape
    
    # simulate guard walk
    guard = map.find_guard()
    guard_path = [guard]
    while map.in_bounds(guard.x, guard.y):
        guard = map.patrol_step()
        guard_path.append(guard)

    # part 1
    # [print(guard) for guard in guard_path]
    print(len(np.argwhere(map=='X')))

    # part 2
    opps = {}
    for n, opp in enumerate(guard_path): 
        if n > 0 and n < len(guard_path)-1:
            print('{}/{}'.format(n, len(guard_path)-1))
            test_map = Map(rows)
            guard = test_map.find_guard()
            if opp.x==guard.x and opp.y==guard.y:
                print('initial position, skipping')
            else:
                test_map[opp.x, opp.y] = '#'        # place a single obstacle 
                visited = { guard.__str__(): True } # initiate list of locations visited
                while test_map.in_bounds(guard.x, guard.y):
                    guard = test_map.patrol_step()
                    if guard.__str__() in visited:  # loop!
                        print('loop detected!')
                        opps.update({'{}|{}'.format(opp.x, opp.y): True})
                        break
                    visited.update({ guard.__str__(): True })
                print('complete, no loop')

    print(len(opps)) # 1972 is the answer (1625 from last attempt)