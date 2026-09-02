import collections
import heapq
import os
import random

#10 UNIQUE MAP DESCRIPTIONS
# S = Start, G = Goal, # = Wall, . = Path (Cost 1), M = Mud (Cost 5)
RAW_MAPS = [
    [
        "S...#....G",
        ".##.#.##..",
        ".#..M..#..",
        ".#.MMM.#..",
        "...#......"
    ],
    [
        "SMMMMMMMM.",
        ".#######M.",
        ".#.....#M.",
        ".#.###.#M.",
        ".........G"
    ],
    [
        "S........#",
        "########.#",
        ".........#",
        ".#########",
        ".........G"
    ],
    [
        "SM.M.M.M.G",
        ".M.M.M.M..",
        ".M.M.M.M#.",
        ".M.M.M.M..",
        ".........."
    ],
    [
        "S..#...#..",
        "##.#.#.#.#",
        ".....#....",
        ".#########",
        "....MMM..G"
    ],
    [
        "S....#...G",
        "####.#.###",
        "MMMM.#....",
        "####.####.",
        ".........."
    ],
    [
        "S.#.#.#.#.",
        "..M.M.M...",
        "#.#.#.###.",
        "..M.M.M.M.",
        "#.#.###..G"
    ],
    [
        "SMM#...#MM",
        ".#M#.#.#M.",
        ".#MM.#.MM.",
        ".########.",
        ".........G"
    ],
    [
        "S..MMM....",
        "...MMM....",
        "...MMM....",
        "...MMM....",
        ".........G"
    ],
    [
        "S#.......G",
        ".#.#M#M#M#",
        ".#.#......",
        ".#.#####.#",
        ".........."
    ]
]

DIRECTIONS = {'w': (-1, 0), 's': (1, 0), 'a': (0, -1), 'd': (0, 1)}

def get_cost(cell):
    return 5 if cell == 'M' else 1

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

#  ALGORITHMS 
def get_neighbors(r, c, grid):
    neighbors = []
    for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]) and grid[nr][nc] != '#':
            neighbors.append((nr, nc))
    return neighbors

def bfs(grid, start, goal):
    queue = collections.deque([(start, [start], 0)])
    visited = {start}
    while queue:
        (r, c), path, cost = queue.popleft()
        if (r, c) == goal: return path, cost
        for nr, nc in get_neighbors(r, c, grid):
            if (nr, nc) not in visited:
                visited.add((nr, nc))
                queue.append(((nr, nc), path + [(nr, nc)], cost + get_cost(grid[nr][nc])))
    return [], 0

def dfs(grid, start, goal):
    stack = [(start, [start], 0)]
    visited = {start}
    while stack:
        (r, c), path, cost = stack.pop()
        if (r, c) == goal: return path, cost
        for nr, nc in get_neighbors(r, c, grid):
            if (nr, nc) not in visited:
                visited.add((nr, nc))
                stack.append(((nr, nc), path + [(nr, nc)], cost + get_cost(grid[nr][nc])))
    return [], 0

def ucs(grid, start, goal):
    pq = [(0, start, [start])]
    visited = {}
    while pq:
        cost, (r, c), path = heapq.heappop(pq)
        if (r, c) == goal: return path, cost
        if (r, c) in visited and visited[(r, c)] <= cost: continue
        visited[(r, c)] = cost
        
        for nr, nc in get_neighbors(r, c, grid):
            new_cost = cost + get_cost(grid[nr][nc])
            heapq.heappush(pq, (new_cost, (nr, nc), path + [(nr, nc)]))
    return [], 0

#  GAME LOOP 
def draw_map(maze, player_pos):
    print("=== MAZE RUNNER ===")
    print("Legend: @ = You, G = Goal, # = Wall, . = Path (Cost 1), M = Mud (Cost 5)\n")
    
    for r in range(len(maze)):
        row_str = ""
        for c in range(len(maze[0])):
            if (r, c) == player_pos:
                row_str += "@ "
            else:
                row_str += maze[r][c] + " "
        print(row_str)
    print("===================")

def setup_game(raw_map):
    maze = [list(row) for row in raw_map]
    start = (0, 0)
    goal = (0, 0)
    
    # Dynamically find Start and Goal positions
    for r in range(len(maze)):
        for c in range(len(maze[0])):
            if maze[r][c] == 'S':
                start = (r, c)
            elif maze[r][c] == 'G':
                goal = (r, c)
                
    return maze, start, goal

def play_game():
    # 1. Create our "deck" of maps and shuffle them
    map_deck = list(RAW_MAPS)
    random.shuffle(map_deck)
    
    maps_played = 0

    while True:
        # 2. Check if we need to reshuffle the deck
        if not map_deck:
            print("\n[!] You have played all 10 maps! Reshuffling the deck...")
            map_deck = list(RAW_MAPS)
            random.shuffle(map_deck)
            input("Press Enter to continue to the next round...")
            
        # 3. Draw a map from the deck
        current_raw_map = map_deck.pop()
        maze, start_pos, goal_pos = setup_game(current_raw_map)
        
        player_r, player_c = start_pos
        steps = 0
        total_cost = 0
        maps_played += 1

        # Run the current level
        while (player_r, player_c) != goal_pos:
            clear_screen()
            print(f"--- LEVEL {maps_played} ---")
            draw_map(maze, (player_r, player_c))
            print(f"\nStats -> Steps: {steps} | Energy Cost: {total_cost}")
            
            move = input("Move (W=Up, A=Left, S=Down, D=Right) | Q=Quit: ").lower()
            
            if move == 'q':
                print("\nQuitting game... Thanks for playing!")
                return # Exits the program entirely
                
            if move in DIRECTIONS:
                dr, dc = DIRECTIONS[move]
                nr, nc = player_r + dr, player_c + dc
                
                # Check boundaries and walls
                if 0 <= nr < len(maze) and 0 <= nc < len(maze[0]) and maze[nr][nc] != '#':
                    player_r, player_c = nr, nc
                    steps += 1
                    total_cost += get_cost(maze[nr][nc])
                else:
                    print("\n[!] Ouch! You hit a wall.")
                    input("Press Enter to continue...")
            else:
                print("\n[!] Invalid move. Use W, A, S, or D.")
                input("Press Enter to continue...")

        # Player wins the current map
        clear_screen()
        draw_map(maze, (player_r, player_c))
        print(f"\n CONGRATULATIONS!!!!  YOU BEAT LEVEL, {maps_played}!")
        print(f"Your Final Stats -> Steps: {steps} | Energy Cost: {total_cost}")
        print("\nLet's see how the AI algorithms would have done...")
        input("Press Enter to calculate AI paths...")
        
        # Calculate AI
        bfs_path, bfs_cost = bfs(maze, start_pos, goal_pos)
        dfs_path, dfs_cost = dfs(maze, start_pos, goal_pos)
        ucs_path, ucs_cost = ucs(maze, start_pos, goal_pos)
        
        print("\n--- RESULTS BOARD ---")
        print(f"YOU (Human Player)  -> Steps: {steps} | Cost: {total_cost}")
        print(f"BFS (Fewest Steps)  -> Steps: {len(bfs_path)-1} | Cost: {bfs_cost}")
        print(f"UCS (Lowest Cost)   -> Steps: {len(ucs_path)-1} | Cost: {ucs_cost}")
        print(f"DFS (Blind Search)  -> Steps: {len(dfs_path)-1} | Cost: {dfs_cost}")
        
        replay = input("\nDo you want to play the next map? (Y/N): ").lower()
        if replay != 'y':
            print(f"\nThanks for playing! You beat {maps_played} levels.")
            break 

if __name__ == "__main__":
    play_game()