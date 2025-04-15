import heapq
from collections import defaultdict
from constants import UP, DOWN, LEFT, RIGHT, STOP


def manhattan_distance(pos1, pos2, ghost_pos=None):
    base_dist = abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
    if ghost_pos:
        ghost_dist = abs(pos1[0] - ghost_pos[0]) + abs(pos1[1] - ghost_pos[1])
        if ghost_dist < 5:
            base_dist += (5 - ghost_dist) * 60
    return base_dist


class Pathfinder:
    def __init__(self, nodeGroup):
        self.nodeGroup = nodeGroup
        self.metrics = {}
        self.total_metrics = {
            'astar': {"nodes_expanded": 0, "path_length": 0, "calls": 0},
            'greedy': {"nodes_expanded": 0, "path_length": 0, "calls": 0},
            'bfs': {"nodes_expanded": 0, "path_length": 0, "calls": 0},
            'dfs': {"nodes_expanded": 0, "path_length": 0, "calls": 0},
            'ucs': {"nodes_expanded": 0, "path_length": 0, "calls": 0}
        }

    def update_total_metrics(self, algorithm, nodes_expanded, path_length):
        self.total_metrics[algorithm]["calls"] += 1
        self.total_metrics[algorithm]["nodes_expanded"] += nodes_expanded
        self.total_metrics[algorithm]["path_length"] += path_length

    def compute_target_path(self, start, pellet, search_method):
        search_method = search_method.strip().lower()
        if search_method == "a*":
            search_method = "astar"

        search_func = {
            'astar': self.astar_search,
            'bfs': self.bfs_search,
            'dfs': self.dfs_search,
            'greedy': self.greedy_search,
            # 'ucs': self.uniform_cost_search
        }.get(search_method, self.greedy_search)
        target_node = self.nodeGroup.getNodeFromPixels(pellet.position.x, pellet.position.y)
        if target_node is None:
            return None, []
        path = search_func(start, target_node)
        return target_node, path

    def astar_search(self, start, goal):
        open_set = []
        counter = 0
        heapq.heappush(open_set, (0, counter, start))
        parent = {start: None}
        g_score = {start: 0}
        nodes_expanded = 0
        ghost_node = self.nodeGroup.ghost.node if self.nodeGroup.ghost else None
        ghost_pos = ghost_node.position.asTuple() if ghost_node else None

        while open_set:
            _, _, current = heapq.heappop(open_set)
            nodes_expanded += 1
            if current == goal:
                path = self.reconstruct_path(parent, current)
                self.metrics['astar'] = {"nodes_expanded": nodes_expanded, "path_length": len(path)}
                self.update_total_metrics('astar', nodes_expanded, len(path))
                print(f"A*: Nodes Expanded = {nodes_expanded}, Path Length = {len(path)}")
                return path
            for child in [n for n in current.neighbors.values() if n is not None]:
                tentative_g = g_score[current] + 1
                if child not in g_score or tentative_g < g_score[child]:
                    parent[child] = current
                    g_score[child] = tentative_g
                    f_score = tentative_g + manhattan_distance(child.position.asTuple(), goal.position.asTuple(), ghost_pos)
                    counter += 1
                    heapq.heappush(open_set, (f_score, counter, child))
        self.metrics['astar'] = {"nodes_expanded": nodes_expanded, "path_length": 0}
        self.update_total_metrics('astar', nodes_expanded, 0)
        print(f"A*: Nodes Expanded = {nodes_expanded}")
        return []

    def bfs_search(self, start, goal):
        open_list = [start]
        parent = {start: None}
        nodes_expanded = 0
        ghost_node = self.nodeGroup.ghost.node if self.nodeGroup.ghost else None
        ghost_pos = ghost_node.position.asTuple() if ghost_node else None

        while open_list:
            open_list.sort(key=lambda n: manhattan_distance(n.position.asTuple(), goal.position.asTuple(), ghost_pos))
            current = open_list.pop(0)
            nodes_expanded += 1
            if current == goal:
                path = self.reconstruct_path(parent, current)
                self.metrics['bfs'] = {"nodes_expanded": nodes_expanded, "path_length": len(path)}
                self.update_total_metrics('bfs', nodes_expanded, len(path))
                print(f"BFS: Nodes Expanded = {nodes_expanded}, Path Length = {len(path)}")
                return path
            for child in [n for n in current.neighbors.values() if n is not None]:
                if child not in parent:
                    parent[child] = current
                    open_list.append(child)
        self.metrics['bfs'] = {"nodes_expanded": nodes_expanded, "path_length": 0}
        self.update_total_metrics('bfs', nodes_expanded, 0)
        print(f"BFS: Nodes Expanded = {nodes_expanded}")
        return []

    def dfs_search(self, start, goal):
        open_list = [start]
        parent = {start: None}
        nodes_expanded = 0
        ghost_node = self.nodeGroup.ghost.node if self.nodeGroup.ghost else None
        ghost_pos = ghost_node.position.asTuple() if ghost_node else None

        while open_list:
            open_list.sort(key=lambda n: -manhattan_distance(n.position.asTuple(), goal.position.asTuple(), ghost_pos))
            current = open_list.pop()
            nodes_expanded += 1
            if current == goal:
                path = self.reconstruct_path(parent, current)
                self.metrics['dfs'] = {"nodes_expanded": nodes_expanded, "path_length": len(path)}
                self.update_total_metrics('dfs', nodes_expanded, len(path))
                print(f"DFS: Nodes Expanded = {nodes_expanded}, Path Length = {len(path)}")
                return path
            for child in [n for n in current.neighbors.values() if n is not None]:
                if child not in parent:
                    parent[child] = current
                    open_list.append(child)
        self.metrics['dfs'] = {"nodes_expanded": nodes_expanded, "path_length": 0}
        self.update_total_metrics('dfs', nodes_expanded, 0)
        print(f"DFS: Nodes Expanded = {nodes_expanded}")
        return []

    def greedy_search(self, start, goal):
        open_list = [start]
        parent = {start: None}
        nodes_expanded = 0
        ghost_node = self.nodeGroup.ghost.node if self.nodeGroup.ghost else None
        ghost_pos = ghost_node.position.asTuple() if ghost_node else None

        while open_list:
            open_list.sort(key=lambda node: manhattan_distance(node.position.asTuple(), goal.position.asTuple(), ghost_pos))
            current = open_list.pop(0)
            nodes_expanded += 1
            if current == goal:
                path = self.reconstruct_path(parent, current)
                self.metrics['greedy'] = {"nodes_expanded": nodes_expanded, "path_length": len(path)}
                self.update_total_metrics('greedy', nodes_expanded, len(path))
                print(f"Greedy: Nodes Expanded = {nodes_expanded}, Path Length = {len(path)}")
                return path
            for child in [n for n in current.neighbors.values() if n is not None]:
                if child not in parent:
                    parent[child] = current
                    open_list.append(child)
        self.metrics['greedy'] = {"nodes_expanded": nodes_expanded, "path_length": 0}
        self.update_total_metrics('greedy', nodes_expanded, 0)
        print(f"Greedy: Nodes Expanded = {nodes_expanded}")
        return []

    def uniform_cost_search(self, start, goal):
        open_list = []
        counter = 0
        heapq.heappush(open_list, (0, counter, start))
        parent = {start: None}
        cost_so_far = {start: 0}
        nodes_expanded = 0
        ghost_node = self.nodeGroup.ghost.node if self.nodeGroup.ghost else None
        ghost_pos = ghost_node.position.asTuple() if ghost_node else None

        while open_list:
            current_cost, _, current = heapq.heappop(open_list)
            nodes_expanded += 1
            if current == goal:
                path = self.reconstruct_path(parent, current)
                self.metrics['ucs'] = {"nodes_expanded": nodes_expanded, "path_length": len(path)}
                self.update_total_metrics('ucs', nodes_expanded, len(path))
                print(f"UCS: Nodes Expanded = {nodes_expanded}, Path Length = {len(path)}")
                return path
            for child in [n for n in current.neighbors.values() if n is not None]:
                new_cost = cost_so_far[current] + 1
                if child not in cost_so_far or new_cost < cost_so_far[child]:
                    cost_so_far[child] = new_cost
                    parent[child] = current
                    counter += 1
                    priority = new_cost + manhattan_distance(child.position.asTuple(), goal.position.asTuple(), ghost_pos)
                    heapq.heappush(open_list, (priority, counter, child))
        self.metrics['ucs'] = {"nodes_expanded": nodes_expanded, "path_length": 0}
        self.update_total_metrics('ucs', nodes_expanded, 0)
        print(f"UCS: Nodes Expanded = {nodes_expanded}")
        return []

    def reconstruct_path(self, parent, current):
        path = []
        while current:
            path.append(current)
            current = parent[current]
        return list(reversed(path))

    def get_next_direction(self, path, current_node):
        if len(path) < 2:
            return STOP
        next_node = path[1]
        for direction, neighbor in current_node.neighbors.items():
            if neighbor == next_node:
                return direction
        return STOP
