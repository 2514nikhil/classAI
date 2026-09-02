#FIFO
def bfs(graph, start):
    
    #keep track of visited nodes to avoid cycles and infinite loops
    visited = set()
    
    #Initialize queue with start node and mark it as visited
    queue = deque([start])
    visited.add(start)
    
    bfs_order = []

    while queue:
        #Dequeue the node from the front of the line
        current_node = queue.popleft()
        bfs_order.append(current_node)
        #neighbors of the current node are added to the queue if they haven't been visited yet
        for neighbor in graph[current_node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return bfs_order

if __name__ == "__main__":
    from collections import deque

    # Example graph represented as an adjacency list
    graph = {
        'A': ['B', 'C'],
        'B': ['A', 'D', 'E'],
        'C': ['A', 'F'],
        'D': ['B'],
        'E': ['B', 'F'],
        'F': ['C', 'E']
    }

    start_node = 'A'
    bfs_result = bfs(graph, start_node)
    print(f"BFS Traversal starting from node {start_node}: {bfs_result}")