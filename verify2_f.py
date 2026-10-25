import random
from family import *
def A005044(n): return round(n*n/48) if n%2==0 else None
def alcuin(n):   # nearest integer to n^2/48 (n even) or (n+3)^2/48 (n odd), exact integer arithmetic
    m=n*n if n%2==0 else (n+3)**2
    return (2*m+48)//96           # floor(m/48+1/2)
assert [alcuin(n) for n in range(3,16)]==[1,0,1,1,2,1,3,2,4,3,5,4,7]
for s,(side,kind) in SEQ.items():
    prop=prop_sqfree if kind=='sqfree' else prop_coprime
    for n in range(1,301): assert a(s,n)==a_double(n,side,prop),(s,n)
print("T1 fast == O(n^2) definition for all 6 sequences, all n<=300",flush=True)
primes=[10**18+9,2**61-1,10**9+7,998244353,(1<<31)-1]
for p in primes:
    for s in ['A308202','A308209','mid-coprime']:
        assert a(s,p)==alcuin(p),(s,p)
print("T2 prime n (incl. 10^18+9, 2^61-1): coprime sequences equal Alcuin's A005044(n) exactly",flush=True)
