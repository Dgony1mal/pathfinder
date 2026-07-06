from collections import deque
import heapq
import time   # ДОБАВЛЕНО: для замера времени

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def bfs(app):
    if app.start is None or app.finish is None:
        return False

    start_time = time.time()   # ДОБАВЛЕНО: начало замера

    queue = deque([app.start])
    parents = {}
    visited = {app.start}
    found = False

    while queue:
        if not app.search_running:
            return False

        current = queue.popleft()
        row, col = current

        if app.grid[row][col] == 0:
            app.grid[row][col] = 4

        app.draw_grid()
        app.update_queue(queue)
        app.root.update()
        app.root.after(20)

        if current == app.finish:
            found = True
            break

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dr, dc in directions:
            nr = row + dr
            nc = col + dc

            if not (0 <= nr < 30 and 0 <= nc < 30):
                continue
            if app.grid[nr][nc] == 1:
                continue

            neighbor = (nr, nc)
            if neighbor in visited:
                continue

            visited.add(neighbor)
            parents[neighbor] = current
            queue.append(neighbor)

    app.visited = len(visited)

    if found:
        app.restore_path(parents)

    # Замер времени после выполнения
    execution_time = time.time() - start_time
    app.execution_time = execution_time

    # Сохраняем результат в словарь сравнения
    app.results["BFS"]["path"] = app.path_length if found else "-"
    app.results["BFS"]["time"] = f"{execution_time:.3f}" if found else "-"

    app.update_status()
    app.update_compare()

    app.queue_box.delete(0, app.queue_box.size())
    app.search_running = False

    return found

def dfs(app):
    if app.start is None or app.finish is None:
        return False

    start_time = time.time()   # ДОБАВЛЕНО

    stack = [app.start]
    parents = {}
    visited = {app.start}
    found = False

    while stack:
        if not app.search_running:
            return False

        current = stack.pop()
        row, col = current

        if app.grid[row][col] == 0:
            app.grid[row][col] = 4

        app.draw_grid()
        app.update_queue(stack)
        app.root.update()
        app.root.after(20)

        if current == app.finish:
            found = True
            break

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dr, dc in directions:
            nr = row + dr
            nc = col + dc

            if not (0 <= nr < 30 and 0 <= nc < 30):
                continue
            if app.grid[nr][nc] == 1:
                continue

            neighbor = (nr, nc)
            if neighbor in visited:
                continue

            visited.add(neighbor)
            parents[neighbor] = current
            stack.append(neighbor)

    app.visited = len(visited)

    if found:
        app.restore_path(parents)

    execution_time = time.time() - start_time
    app.execution_time = execution_time

    app.results["DFS"]["path"] = app.path_length if found else "-"
    app.results["DFS"]["time"] = f"{execution_time:.3f}" if found else "-"

    app.update_status()
    app.update_compare()

    app.queue_box.delete(0, app.queue_box.size())
    app.search_running = False

    return found

def astar(app):
    if app.start is None or app.finish is None:
        return False

    start_time = time.time()   # ДОБАВЛЕНО

    open_set = []
    heapq.heappush(open_set, (0, app.start))
    parents = {}
    g_score = {app.start: 0}
    visited = set()
    found = False

    while open_set:
        if not app.search_running:
            return False

        _, current = heapq.heappop(open_set)
        if current in visited:
            continue

        visited.add(current)
        row, col = current

        if app.grid[row][col] == 0:
            app.grid[row][col] = 4

        app.draw_grid()
        app.update_queue([cell for _, cell in open_set])
        app.root.update()
        app.root.after(20)

        if current == app.finish:
            found = True
            break

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dr, dc in directions:
            nr = row + dr
            nc = col + dc

            if not (0 <= nr < 30 and 0 <= nc < 30):
                continue
            if app.grid[nr][nc] == 1:
                continue

            neighbor = (nr, nc)
            new_cost = g_score[current] + 1

            if neighbor not in g_score or new_cost < g_score[neighbor]:
                g_score[neighbor] = new_cost
                priority = new_cost + heuristic(neighbor, app.finish)
                heapq.heappush(open_set, (priority, neighbor))
                parents[neighbor] = current

    app.visited = len(visited)

    if found:
        app.restore_path(parents)

    execution_time = time.time() - start_time
    app.execution_time = execution_time

    app.results["A*"]["path"] = app.path_length if found else "-"
    app.results["A*"]["time"] = f"{execution_time:.3f}" if found else "-"

    app.update_status()
    app.update_compare()

    app.queue_box.delete(0, app.queue_box.size())
    app.search_running = False

    return found