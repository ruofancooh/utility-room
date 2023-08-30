import primesieve


def is_prime(num: int) -> bool:
    
    if isinstance(num, int) is not True or num <= 1:
        return False
    if len(primesieve.primes(num,num))==1:
        return True
    else:
        return False



def decompose_prime_factors(num: int) -> list:
    
    if isinstance(num, int) is not True or num <= 1:
        raise TypeError('The number must be an integer greater than 1')
    
    prime_factor = []
    it = primesieve.Iterator()
    prime = it.next_prime()  #2
    sqrt_num=num**0.5

    while prime <= sqrt_num:
        print(prime_factor,prime)
        if is_prime(num):
            prime_factor.append(num)
            return prime_factor
        elif num % prime == 0:
            prime_factor.append(prime)
            num = num//prime
        else:
            prime = it.next_prime()
            
    return prime_factor+[num]



num = 2**61-5
print(f'{num}分解质因数为{decompose_prime_factors(num)}')
print(f'{num}{"是质数" if is_prime(num)is True else "不是质数"}')

'''
set1=set()
set2=set()
count=primesieve.count_primes(1000)
for i in range(2,1000):
    if is_prime(i):
        set1.add(i)
    if decompose_prime_factors(i)[0]==i:
        set2.add(i)

print(len(set1))
print(len(set2))
print(count)
'''
#print(is_prime(2**31))