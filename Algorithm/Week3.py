# 문제01
## 풀이01
n, m = map(lambda x: int(x), input().split())
numbers = list(map(lambda x: int(x), input().split()))

res = []
for number in numbers:
    if number > m:
        continue
    if len(res)==3:
        if res[0] < res[1]:
            res[0], res[1] = res[1], res[0]
        if res[1] < res[2]:
            res[1], res[2] = res[2], res[1]
            if res[0] < res[1]:
                res[0], res[1] = res[1], res[0]
                
        if number > res[-1]:
            res.pop()
            res.append(number)
        else:
            pass
    else:
        res.append(number)
print(sum(res))
# 풀이02
n, m = map(lambda x: int(x), input().split())
numbers = list(map(lambda x: int(x), input().split()))

res = [number for number in numbers if number<=m]
res = sorted(res)[-3:]

print(sum(res))

# 문제02
def combine(len_, lst=[]):
    """
    리스트에서 각 숫자의 위치(index)를 부여하는 함수
    가능한 모든 조합을 리스트 형태로 반환
    """
    if len(lst)==0:
        lst = [[i] for i in range(len_)]
        return combine(len_, lst)
    
    if len_!=len(lst[0]):
        for elem in lst:
            for i in range(len_):
                if i not in elem:
                    elem.append(i)
        return combine(len_, lst)
    else:
        for elem in lst:
            for i in range(len_):
                if i not in elem:
                    elem.append(i)
        return lst

numbers = ','.join(input()).split(',')
len_=len(numbers)

res = []
for combs in combine(len_):
    stopper = 0
    int_ = [-1]*len_
    for n, c in zip(numbers, combs):
        int_[c] = n
    num = int(''.join(int_))
    for i in range(2, num//2+1):
        if num%i == 0:
            stopper = 1
            break
    if stopper==0:
        res.append(num)

print(len(res))

# 문제03
m, n = map(lambda x: int(x), input().split())
mat = []
for _ in range(m):
    mat.append(input())

res = []
mats = []
for x_ in range(m-7):
    for y_ in range(n-7):
        # 8x8 크기 탐색
        mat_ = [row[y_:y_+8] for row in mat[x_:x_+8]]
        res_ = 0
        # RBRB/BRBR 순서 탐색
        for idx, row in enumerate(mat_):
            if idx%2==0:
                for idx_, str_ in enumerate(row):
                    if idx_%2==0 and str_!="R":
                        res_ += 1
                    elif idx_%2==1 and str_!="B":
                        res_ += 1
            if idx%2==1:
                for idx_, str_ in enumerate(row):
                    if idx_%2==0 and str_!="B":
                        res_ += 1
                    elif idx_%2==1 and str_!="R":
                        res_ += 1
        res.append(res_)
        
        # BRBR/RBRB 순서 탐색
        res_ = 0
        for idx, row in enumerate(mat_):
            if idx%2==0:
                for idx_, str_ in enumerate(row):
                    if idx_%2==0 and str_!="B":
                        res_ += 1
                    elif idx_%2==1 and str_!="R":
                        res_ += 1
            if idx%2==1:
                for idx_, str_ in enumerate(row):
                    if idx_%2==0 and str_!="R":
                        res_ += 1
                    elif idx_%2==1 and str_!="B":
                        res_ += 1
        res.append(res_)
print(min(res))

# 문제04
heights = [int(input()) for i in range(9)]

combs = []
for i in range(9):
    for j in range(9):
        if i<j:
            heights_ = heights.copy()
            heights_.pop(i)
            heights_.pop(j-1)
            if sum(heights_)==1000:
                print(*sorted(heights_), sep="\n")
                break

# 문제05
word = input()

len_ = len(word)
res = None
for i in range(len_):
    for j in range(len_):
        if i < j:
            # 글자 나누기
            words = [word[:i+1], word[i+1:j+1], word[j+1:]]
            # 뒤집기
            words = [word_[::-1] for word_ in words]
            # 합치기
            if not res:
                res = ''.join(words)
            if res > ''.join(words):
                res = ''.join(words)
print(res)