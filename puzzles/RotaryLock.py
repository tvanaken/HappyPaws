#PASSED
from typing import List
# Write any import statements here

def getMinCodeEntryTime(N: int, M: int, C: List[int]) -> int:
  # Write your code here
  current = 1
  total = 0
  
  for i in range(0, M):
    if C[i] == current:
      continue
    
    if current < C[i]:
        left = (current + abs(C[i] - N))
        right = abs(C[i] - current)
    else:
        left = (current - C[i])
        right = (N - current) + C[i]
    
    if left >= right:
      total += right
    else:
      total += left
      
    current = C[i]
    
    
  return total

print(getMinCodeEntryTime(15, 4, [9, 4, 4, 8]))