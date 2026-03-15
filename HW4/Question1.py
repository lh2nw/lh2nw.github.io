import math
from itertools import combinations

points = [(2, 3), (5, 7), (1, 8), (2, 3), (9, 1), (5, 7)]

# 1. Removes duplicate points
# Converting a list to a set automatically removes duplicates
unique_points = list(set(points))

max_distance = -1
farthest_pair = (None, None)

# 2. Computes the Euclidean distance between every pair
# combinations(list, 2) creates every unique pair without repeats (A,B is same as B,A)
for p1, p2 in combinations(unique_points, 2):
    # Euclidean distance formula: sqrt((x2-x1)^2 + (y2-y1)^2)
    distance = math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)

    # 3. Finds the two points that are farthest apart
    if distance > max_distance:
        max_distance = distance
        farthest_pair = (p1, p2)

# 4. Returns the result as a tuple: (pointA, pointB, distance)
result = (farthest_pair[0], farthest_pair[1], max_distance)

print(f"Farthest Points: {result[0]} and {result[1]}")
print(f"Distance: {result[2]:.2f}")
print(f"Final Tuple: {result}")