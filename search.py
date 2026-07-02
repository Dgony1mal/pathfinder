from collections import deque
import heapq

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def restore_path(parents, start, finish):

    path = [finish]

    current = finish

    while current != start:
        current = parents[current]
        path.append(current)

    path.reverse()

    return path

def bfs(grid, start, finish):

    queue = deque([start])

    parents = {}

    visited = {start}

    while queue:

        current = queue.popleft()

        if current == finish:

            return {
                "found": True,
                "path": restore_path(
                    parents,
                    start,
                    finish
                ),
                "visited": visited
            }

        row, col = current

        for dr, dc in [
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1)
        ]:

            nr = row + dr
            nc = col + dc

            if not (0 <= nr < len(grid) and 0 <= nc < len(grid[0])):
                continue

            if grid[nr][nc] == 1:
                continue

            neighbor = (nr, nc)

            if neighbor in visited:
                continue

            visited.add(neighbor)

            parents[neighbor] = current

            queue.append(neighbor)

    return {
        "found": False,
        "path": [],
        "visited": visited
    }

def dfs(grid, start, finish):

    stack = [start]

    parents = {}

    visited = {start}

    while stack:

        current = stack.pop()

        if current == finish:

            return {
                "found": True,
                "path": restore_path(
                    parents,
                    start,
                    finish
                ),
                "visited": visited
            }

        row, col = current

        for dr, dc in [
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1)
        ]:

            nr = row + dr
            nc = col + dc

            if not (0 <= nr < len(grid) and 0 <= nc < len(grid[0])):
                continue

            if grid[nr][nc] == 1:
                continue

            neighbor = (nr, nc)

            if neighbor in visited:
                continue

            visited.add(neighbor)

            parents[neighbor] = current

            stack.append(neighbor)

    return {
        "found": False,
        "path": [],
        "visited": visited
    }

def astar(grid, start, finish):

    open_set = []

    heapq.heappush(open_set, (0, start))

    parents = {}

    g_score = {start: 0}

    visited = set()

    while open_set:

        _, current = heapq.heappop(open_set)

        if current in visited:
            continue

        visited.add(current)

        if current == finish:

            return {
                "found": True,
                "path": restore_path(
                    parents,
                    start,
                    finish
                ),
                "visited": visited
            }

        row, col = current

        for dr, dc in [
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1)
        ]:

            nr = row + dr
            nc = col + dc

            if not (0 <= nr < len(grid) and 0 <= nc < len(grid[0])):
                continue

            if grid[nr][nc] == 1:
                continue

            neighbor = (nr, nc)

            new_cost = g_score[current] + 1

            if neighbor not in g_score or new_cost < g_score[neighbor]:

                g_score[neighbor] = new_cost

                priority = new_cost + heuristic(neighbor, finish)

                heapq.heappush(open_set, (priority, neighbor))

                parents[neighbor] = current

    return {
        "found": False,
        "path": [],
        "visited": visited
    }