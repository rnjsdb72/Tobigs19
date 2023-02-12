# 문제01
n, m = map(lambda x: int(x), input().split())
mat = []
for _ in range(n):
    row = list(map(lambda x: int(x), input().split()))
    mat.append(row)

res = []
for row in mat:
    min_ = 10000
    for elem in row:
        if min_ > elem:
            min_ = elem
    res.append(min_)

ans = -1
for x in res:
    if ans < x:
        ans = x

print(ans)

# 문제02
n = int(input())
dir = input().split()

coor = [1,1]
for x in dir:
    if x == "L":
        if coor[1] != 1:
            coor[1] -= 1
    elif x == "R":
        if coor[1] != n:
            coor[1] += 1
    elif x == "U":
        if coor[0] != 1:
            coor[0] -= 1
    elif x == "D":
        if coor[0] != n:
            coor[0] += 1

print(' '.join(map(lambda x: str(x), coor)))

# 문제03
u, d, h = map(lambda x: int(x), input().split())
h = h-u # 올라가기만 했을 때, h에 도달할 수 있는 경우 고려
n = h//(u-d)

if h%(u-d)==0: # 나머지가 없으면 +1만 하여 출력
    print(n+1)
else: # 나머지가 있으면 +2 하여 출력
    print(n+2)
    
# 문제04
## (바뀌는 구간, 정답)
## (0 -> 0), (1 -> 1), (2 -> 1), (3 -> 2), (4 -> 2), (5 -> 3), (6 -> 3), (7 -> 4)
c = input()
ans = 0
before = c[0]
for after in c[1:]:
    if before != after:
        ans += 1
    before = after
if ans%2 == 0:
    print(ans//2)
else:
    print(ans//2+1)
    
# 문제05
while True:
    x = input()
    if x == "0":
        break
    if x == x[::-1]:
        print("yes")
    else:
        print("no")