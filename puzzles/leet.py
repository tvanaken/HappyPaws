from typing import List


def validPath(n: int, edges: List[List[int]], source: int, destination: int) -> bool:
        
        currentNode = [source]

        for edge in edges:
              if currentNode in edge:
                    

        return False

def checkPath(edges: List[List[int]], source: int, destination: int) -> list:
     
    path = []

    for edge in edges:
            if source in edge:
                if destination in edge:
                     return True
                if edge[0] == source:
                     path.append(edge[1])
                     edges2.remove(edge)
                else:
                     path.append(edge[0])
                     edges2.remove(edge)
    return path
        

    

print(validPath(3, [[0,1],[1,2],[2,0]], 0, 2))
print(validPath(6, [[0,1],[0,2],[3,5],[5,4],[4,3]], 0, 5))