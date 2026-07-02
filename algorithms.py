from collections import deque

def bfs(app):

    if app.start is None or app.finish is None:
        return False

    queue = deque([app.start])

    parents = {}

    visited = {app.start}

    found = False

    while queue:

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

        directions = [
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1)
        ]

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

    app.update_status()

    app.queue_box.delete(0, app.queue_box.size())

    app.search_running = False

    return found