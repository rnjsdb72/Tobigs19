n, m = map(lambda x: int(x), input().split())
# 문제01
numbers = list(map(lambda x: int(x), input().split()))

res = 0
for i in range(len(numbers)-2):
    for j in range(i+1,len(numbers)-1):
        for k in range(j+1, len(numbers)):
            sum_ = numbers[i]+numbers[j]+numbers[k]
            if (sum_ <= m) and (sum_ > res):
                res = sum_
print(res)

# 문제02
def permutation(numbers, n):
    """
    숫자의 순열을 계산하는 함수

    Args:
        numbers: 숫자 리스트
        n: 선택할 숫자 개수

    Returns:
        res: 해당 숫자의 모든 순열의 경우의 수가 담긴 리스트
    """
    res = []
    if n>len(numbers):
        return res
    if n == 1:
        for i in numbers:
            res.append([i])
    elif n > 1:
        for i in range(len(numbers)):
            ans = [i for i in numbers]
            ans.remove(numbers[i])
            for rest in permutation(ans, n-1):
                res.append([numbers[i]]+rest)
    return res

def count_prime(numbers):
    """
    소수 개수 파악하는 함수

    Args:
        numbers: 숫자 조합 리스트

    Returns:
        res: 숫자 조합 중 소수 개수
    """
    res = []
    for number in numbers:
        num = int("".join(number))
        if num == 2:
            res.append(num)
            
        stopper=0
        for i in range(2, num//2+1):
            if num%i == 0:
                stopper = 1
                break
        if stopper==0 and num not in [0,1]:
            res.append(num)
    return res

numbers = ','.join(input()).split(',')

res = []
comb_nums = []
for n_ in range(1, len(numbers)+1):
    comb_nums += permutation(numbers, n_)

res = count_prime(comb_nums)
res = set(res)
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
stopper = 0
for i in range(8):
    for j in range(i+1, 9):
        heights_ = heights.copy()
        heights_.pop(j)
        heights_.pop(i)
        if sum(heights_)==1000:
            print(*sorted(heights_), sep="\n")
            stopper=1
            break
    if stopper==1:
        break

# 문제05
word = input()

len_ = len(word)
res = None
for i in range(1, len_-1):
    for j in range(i+1, len_):
        # 글자 나누기
        words = [word[:i], word[i:j], word[j:]]
        # 뒤집기
        words = [word_[::-1] for word_ in words]
        # 합치기
        if not res:
            res = ''.join(words)
        if res > ''.join(words):
            res = ''.join(words)
print(res)