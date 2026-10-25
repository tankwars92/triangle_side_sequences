import random
from family import *
from refined import *
random.seed(5)
ns=list(range(3,500))+[random.randint(500,200000) for _ in range(60)]
for s,(side,kind) in SEQ.items():
    for n in ns:
        orc=Sqfree(n) if kind=='sqfree' else Coprime(n)
        assert S_refined(side,n,orc)==a(s,n),(s,n)
print("R1 refined closed form (Theorem 2) == fast method: 6 cases, n=3..499 and 60 random n<=2e5")
# explicit closed form for the middle side (Corollary 2), property f=mu^2
def Qt(o,x): return o.pref(x,0)[0]+o.pref(x,1)[0]
def Mt(o,x): return o.pref(x,0)[1]+o.pref(x,1)[1]
def mid_explicit(n):
    o=Sqfree(n); H=(n-1)//2; l=-(-(n-H)//2); be=-(-n//3); b1=min(be-1,H); b2=max(l,be); t=0
    if l<=b1: t+=(H-n+1)*(Qt(o,b1)-Qt(o,l-1))+2*(Mt(o,b1)-Mt(o,l-1))
    if b2<=H: t+=(H+1)*(Qt(o,H)-Qt(o,b2-1))-(Mt(o,H)-Mt(o,b2-1))
    return t
assert all(mid_explicit(n)==a('A308455',n) for n in ns)
print("R2 explicit formula for A308455 (Corollary 3) == fast method on the same n")
# parity reduction (Lemma): Q1(x)=sum (-1)^i Q(floor(x/2^i)), M1(x)=sum (-2)^i M(floor(x/2^i))
o=Sqfree(10**6)
for x in [1,2,3,10,999,12345,250000]:
    q=sum((-1)**i*Qt(o,x>>i) for i in range(x.bit_length()+1)); m=sum((-2)**i*Mt(o,x>>i) for i in range(x.bit_length()+1))
    assert q==o.pref(x,1)[0] and m==o.pref(x,1)[1]
print("R3 parity reduction identities hold for Q1 and M1 (squarefree), several x")
