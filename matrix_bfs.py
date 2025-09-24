from collections import deque
from typing import List, Tuple, Optional, Set


class Matrix:
    
    def __init__(self, rows: int, cols: int, data: Optional[List[List[int]]] = None):
        self.rows = rows
        self.cols = cols
        
        if data is not None:
            self.matrix = [row[:] for row in data]
        else:
            self.matrix = [[0 for _ in range(cols)] for _ in range(rows)]
    
    def set_cell(self, row: int, col: int, value: int) -> None:
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.matrix[row][col] = value
        else:
            raise IndexError("Cell coordinates out of bounds")
    
    def get_cell(self, row: int, col: int) -> int:
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.matrix[row][col]
        else:
            raise IndexError("Cell coordinates out of bounds")
    
    def is_valid_cell(self, row: int, col: int) -> bool:
        return (0 <= row < self.rows and 
                0 <= col < self.cols and 
                self.matrix[row][col] == 0)
    
    def __str__(self) -> str:
        return '\n'.join([' '.join(map(str, row)) for row in self.matrix])


class BFS:
    
    def __init__(self, matrix: Matrix):
        self.matrix = matrix
        # 8-directional movement: up, down, left, right, and 4 diagonals
        self.directions = [(-1, 0), (1, 0), (0, -1), (0, 1),  # cardinal directions
                          (-1, -1), (-1, 1), (1, -1), (1, 1)]  # diagonal directions
    
    def find_shortest_path(self, start: Tuple[int, int], end: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
        if not self.matrix.is_valid_cell(start[0], start[1]):
            raise ValueError("Start position is not valid")
        if not self.matrix.is_valid_cell(end[0], end[1]):
            raise ValueError("End position is not valid")
        
        queue = deque([(start[0], start[1], [start])])
        visited: Set[Tuple[int, int]] = {start}
        
        while queue:
            row, col, path = queue.popleft()
            
            if (row, col) == end:
                return path
            
            for dr, dc in self.directions:
                new_row, new_col = row + dr, col + dc
                
                if (self.matrix.is_valid_cell(new_row, new_col) and 
                    (new_row, new_col) not in visited):
                    
                    visited.add((new_row, new_col))
                    new_path = path + [(new_row, new_col)]
                    queue.append((new_row, new_col, new_path))
        
        return None
    
    def get_path_length(self, start: Tuple[int, int], end: Tuple[int, int]) -> int:
        if not self.matrix.is_valid_cell(start[0], start[1]):
            raise ValueError("Start position is not valid")
        if not self.matrix.is_valid_cell(end[0], end[1]):
            raise ValueError("End position is not valid")
        
        queue = deque([(start[0], start[1], 0)])
        visited: Set[Tuple[int, int]] = {start}
        
        while queue:
            row, col, distance = queue.popleft()
            
            if (row, col) == end:
                return distance
            
            for dr, dc in self.directions:
                new_row, new_col = row + dr, col + dc
                
                if (self.matrix.is_valid_cell(new_row, new_col) and 
                    (new_row, new_col) not in visited):
                    
                    visited.add((new_row, new_col))
                    queue.append((new_row, new_col, distance + 1))
        
        return -1


def create_sample_matrix() -> Matrix:
    sample_data = [
        [0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
        [0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0],
        [0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0],
        [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1],
        [0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
        [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0]
    ]
    return Matrix(len(sample_data), len(sample_data[0]), sample_data)


def visualize_path(matrix: Matrix, path: List[Tuple[int, int]]) -> str:
    visual = [row[:] for row in matrix.matrix]
    
    for i, (row, col) in enumerate(path):
        if i == 0:
            visual[row][col] = 'S'
        elif i == len(path) - 1:
            visual[row][col] = 'E'
        else:
            visual[row][col] = 'P'
    
    return '\n'.join([' '.join(map(str, row)) for row in visual])


if __name__ == "__main__":
    matrix = create_sample_matrix()
    print("Original Matrix:")
    print(matrix)
    print()
    
    bfs = BFS(matrix)
    
    start = (0, 0)
    end = (9, 11)
    
    print(f"Finding shortest path from {start} to {end}")
    
    path = bfs.find_shortest_path(start, end)
    
    if path:
        print(f"Shortest path found with {len(path) - 1} steps:")
        print("Path coordinates:", path)
        print()
        print("Visual representation:")
        print(visualize_path(matrix, path))
        print()
        print(f"Path length: {bfs.get_path_length(start, end)}")
    else:
        print("No path found between the given points")
