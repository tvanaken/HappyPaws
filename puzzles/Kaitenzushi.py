#PASSED
from typing import List
# Write any import statements here

def getMaximumEatenDishCount(N: int, D: List[int], K: int) -> int:
  # Write your code here
  eatenMap = {}
  eaten = 0
  #eatenLst = list(set(D[0:K]))

  for dish in D:
    
    touched = eatenMap.get(dish)
    
    if touched is None or eaten - touched >= K:
      eaten += 1
      eatenMap[dish] = eaten
  
  return eaten

print(getMaximumEatenDishCount(9, [1,1,2,2,3,3,3,2,1], 1))