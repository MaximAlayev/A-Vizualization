import os
import pygame
import pygame.freetype
import time

#Our Grid of nodes
grid = []

#Grid that helps us determine which spots on the grid are traversable and whichs ones to color appropriately
visual_grid = []

#Finished Path calculated by A*
path = []


class Node():
    'Node Class knows its x and y values on the grid, \
     wether or not it is traversable territory, its H and\
     G cost, and its parent node'
    
    def __init__(self, x_position, y_position, walkable):
        self.x_position: int = x_position
        self.y_position: int = y_position
        self.walkable: bool = walkable
        self.g_cost: float = 0
        self.h_cost: float = 0
        self.parent: Node = None

    def set_g_cost(self, value) -> None:
        self.g_cost = value

    def set_h_cost(self, value) -> None:
        self.h_cost = value

    def set_parent(self, value) -> None:
        self.parent = value

    def set_walkable(self, value) -> None:
        self.walkable = value

    def get_f_cost(self) -> float:
        return (self.g_cost + self.h_cost)


def find_surrounding(node: Node) -> [Node]:
    'Returns a list of up to 8 nodes surrounding a particular node. List is \
    less than length of 8 in the case that the node is on a corner or edge'
    surrounding: [Node] = []
    for x in range (-1, 2):
        for y in range(-1, 2):
            if (x == 0 and y == 0):
                continue
            check_x = node.x_position + x
            check_y = node.y_position + y
            if (check_x >= 0 and check_x < 35 and check_y >= 0 and check_y < 35):
                surrounding.append(grid[check_x][check_y])
    return surrounding

def get_distance(node1: Node, node2: Node) -> float:
    'Gets distance between two nodes'
    x = abs(node1.x_position - node2.x_position)
    y = abs(node1.y_position - node2.y_position)
    if x > y:
        return 14*y + 10*(x-y)
    return 14*x + 10*(y-x)

def retrace(start: Node, end: Node) -> None:
    'Retraces the finished path of A* and assigns it to the 2d list named path'
    retraced_path = []
    current_node = end
    while (not current_node == start):
        retraced_path.append(current_node)
        current_node = current_node.parent
        visual_grid[current_node.x_position][current_node.y_position] = 3
    retraced_path.reverse()
    path = retraced_path

def draw_lines() -> None:
    'Draws the grid lines on the screen'
    for i in range (1, 35):
        pygame.draw.line(screen, (0,0,0), (0,  40 + i * 20), (660, i* 20 + 40), 1)
        pygame.draw.line(screen, (0,0,0), (i * 20, 60), (i* 20, 700), 1)


def setup() -> None:
    'Setup pygame, the screen and its size.'
    global screen
    global run
    global selected
    selected = False
    run = True
    screen = pygame.display.set_mode((660,700))
    screen.fill((255,255,255))
    pygame.display.set_caption("A* Visualizer")

#PyGame initializations:
pygame.font.init()
pygame.freetype.init()
myfont = pygame.freetype.Font("TNR.ttf", 20)
run = True


def setup_grid() -> None:
    'Fills Grid with Nodes'
    new = []
    for i in range (0, 35):
        for j in range (0, 35):
            new.append(0)
        grid.append(new)
        new = []
    for i in range (0, 35):
        for j in range (0, 35):
            grid[i][j] = Node(i , j, True)

def setup_visual_grid() -> None:
    'fills visual grid with traversable terrain (0)'
    new = []
    for i in range (0, 35):
        for j in range (0, 35):
            new.append(0)
        visual_grid.append(new)
        new = []
    visual_grid[0][0] = 6
    visual_grid[30][30] = 7

def color_grid() -> None:
    'Colors screen in according to visualGrid values'
    for i in range (0, 35):
        for j in range (0, 35):
            if (visual_grid[i][j] == 1): #Obstacle
                rect = pygame.Rect(i * 20, j * 20 + 60, 20, 20)
                screen.fill((0,0,0), rect)
            if (visual_grid[i][j] == 3): #Path
                rect = pygame.Rect(i * 20, j * 20 + 60, 20, 20)
                screen.fill((0,0, 255), rect)
            if (visual_grid[i][j] == 4): #Closed Set
                rect = pygame.Rect(i * 20, j * 20 + 60, 20, 20)
                screen.fill((255,0, 0), rect)
            if (visual_grid[i][j] == 5): #Open Set
                rect = pygame.Rect(i * 20, j * 20 + 60, 20, 20)
                screen.fill((0,255, 0), rect)
            if (visual_grid[i][j] == 6): #Yellow for startNode
                rect = pygame.Rect(i * 20, j * 20 + 60, 20, 20)
                screen.fill((255, 255, 0), rect)
            if (visual_grid[i][j] == 7): #Purple for targetNode
                rect = pygame.Rect(i * 20, j * 20 + 60, 20, 20)
                screen.fill((255, 0, 255), rect)
    rect = pygame.Rect(80, 20, 20, 20)
    screen.fill((255, 255, 0), rect)
    rect = pygame.Rect(280, 20, 20, 20)
    screen.fill((255, 0, 255), rect)

def draw_text() -> None:
    'Draws Text'
    myfont.render_to(screen, (105, 23), "Start Node", (0, 0, 0))
    myfont.render_to(screen, (305, 23), "Target Node", (0, 0, 0))

def grid_walkable_update() -> None:
    'Updates which grid spots are walkable'
    for i in range (0, 35):
        for j in range (0, 35):
            if (visual_grid[i][j] == 1):
                grid[i][j].set_walkable(False)

def delete_last_start() -> None:
    'Deletes the start node'
    for i in range (0, 35):
        for j in range (0, 35):
            if (visual_grid[i][j] == 6):
                visual_grid[i][j] = 0

def delete_last_target() -> None:
    'Deletes the target node'
    for i in range (0, 35):
        for j in range (0, 35):
            if (visual_grid[i][j] == 7):
                visual_grid[i][j] = 0

def clear_screen() -> None:
    'Clears the entire grid and makes it empty again'
    screen.fill((255,255,255))
    for i in range (0, 35):
        for j in range (0, 35):
            grid[i][j] = Node(i, j, True)
            visual_grid[i][j] = 0
    color_grid()
    draw_lines()
    draw_text()
    pygame.display.update()
    

def find_path() -> None:
    'This is the A* pathfinding algorithm'
    clock = pygame.time.Clock()
    global start_node
    global target_node
    open_set = []
    closed_set = []
    open_set.append(start_node)
    while (len(open_set) > 0):
        clock.tick(60)
        node = open_set[0]
        for i in range (1, len(open_set)):
            if (open_set[i].get_f_cost() <= node.get_f_cost()):
                if (open_set[i].h_cost < node.h_cost):
                    node = open_set[i]

        open_set.remove(node)
        closed_set.append(node)
        visual_grid[node.x_position][node.y_position] = 4 #Red

        if (node.x_position == target_node.x_position \
            and node.y_position == target_node.y_position):
            retrace(start_node,node)
            return

        for surrounding_node in find_surrounding(node):
            if ((not surrounding_node.walkable) or surrounding_node \
                in closed_set):
                continue

            new_cost_to_surrounding_node = node.g_cost + \
                                           get_distance(node, surrounding_node)

            if (new_cost_to_surrounding_node < surrounding_node.g_cost or \
                not surrounding_node in open_set):
                surrounding_node.set_g_cost(new_cost_to_surrounding_node)
                surrounding_node.set_h_cost(get_distance(surrounding_node, target_node))
                surrounding_node.set_parent(node)
            if (not surrounding_node in open_set):
                open_set.append(surrounding_node)
                visual_grid[surrounding_node.x_position][surrounding_node.y_position] = 5 #Green
        pygame.display.update()
        screen.fill((255, 255, 255))
        draw_lines()
        color_grid()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

if __name__ == '__main__':
    setup()
    setup_grid()
    setup_visual_grid()
    next_click_start = False
    next_click_target = False
    skip_next_click_obst = False
    start_node = Node(0, 0, True)
    target_node = Node(30, 30, True)
    while run:
        pygame.display.update()
        screen.fill((255, 255, 255))
        draw_lines()
        color_grid()
        draw_text()
        if pygame.mouse.get_pressed()[0]:
            if (next_click_start):
                delete_last_start()
                mouse_x, mouse_y = pygame.mouse.get_pos()
                visual_grid[int(mouse_x/20)][int(mouse_y/20 - 3)] = 6
                start_node = Node(int(mouse_x/20), int(mouse_y/20 - 3), True)
                next_click_start = False
                skip_next_click_obst = True
                time.sleep(.3)
            elif (next_click_target):
                delete_last_target()
                mouse_x, mouse_y = pygame.mouse.get_pos()
                visual_grid[int(mouse_x/20)][int(mouse_y/20 - 3)] = 7
                target_node = Node(int(mouse_x/20), int(mouse_y/20 - 3), True)
                next_click_target = False
                skip_next_click_obst = True
                time.sleep(.3)
            elif (not skip_next_click_obst):
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if visual_grid[int(mouse_x/20)][int(mouse_y/20 - 3)] != 6 and \
                   visual_grid[int(mouse_x/20)][int(mouse_y/20 - 3)] != 7:
                    visual_grid[int(mouse_x/20)][int(mouse_y/20 - 3)] = 1
                    grid_walkable_update()
            #If startnode button clicked
            if (mouse_x > 80 and mouse_x < 100 and mouse_y > 20 and mouse_y < 40):
                next_click_start = True
            #if targetnode button clicked
            if (mouse_x > 280 and mouse_x < 300 and mouse_y > 20 and mouse_y < 40):
                next_click_target = True
            skip_next_click_obst = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    find_path()
                elif event.key == pygame.K_BACKSPACE:
                    clear_screen()
