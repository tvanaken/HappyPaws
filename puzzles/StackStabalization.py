#PASSED
from typing import List
# Write any import statements here

def getMinimumDeflatedDiscCount(N: int, R: List[int]) -> int:
    # Write your code here
    
    deflates = 0

    for i in range(N - 1, 0, -1):
        lower = R[i]
        upper = R[i - 1]

        if upper >= lower:
            R[i - 1] = lower - 1

            if R[i-1] == 0:
                return -1
            
            deflates += 1

    return deflates

testList = [6,5,4,3]

print(getMinimumDeflatedDiscCount(4, testList))

