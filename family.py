"""Triangles with perimeter n and an arithmetic property of ONE side (smallest/middle/largest):
   a(n) = sum_k f(k) * w_n(k),  w_n piecewise linear (with parity) -> prefix sums of f.
   f = squarefree indicator (A308453/4/5) or [gcd(k,n)=1] (A308202/A308209)."""
from fractions import Fraction
from math import isqrt, gcd
import random
def weight(side,n):
    H=(n-1)//2
    if side=='min': return lambda k:(n-k)//2-max(k,n-k-H)+1
    if side=='mid': return lambda b:H-max(b,n-2*b)+1
    if side=='max': return lambda c:c-(n-c+1)//2+1
def pieces(side,n):
    H=(n-1)//2; ce=lambda a,b:-(-a//b)
    if side=='min':
        top=n//3; k0=ce(n-H,2); P=[(1,min(k0-1,top))]
        if k0<=top: P.append((max(k0,1),top))
        return P
    if side=='mid':
        lo=ce(n-H,2); br=ce(n,3); return [(lo,min(br-1,H)),(max(br,lo),H)]
    if side=='max': return [(ce(n,3),H)]

def is_sqfree(k):
    d=2
    while d*d<=k:
        if k%(d*d)==0: return False
        d+=1
    return True
def prop_sqfree(n): return lambda k:is_sqfree(k)
def prop_coprime(n): return lambda k:gcd(k,n)==1
def a_double(n,side,prop):
    f=prop(n); t=0
    for a in range(1,n//3+1):
        for b in range(a,(n-a)//2+1):
            c=n-a-b
            if a+b>c: t+=f({'min':a,'mid':b,'max':c}[side])
    return t
def a_linear(n,side,prop):
    f=prop(n); w=weight(side,n); t=0
    for L,R in pieces(side,n):
        for k in range(L,R+1):
            if f(k): t+=w(k)
    return t
class Sqfree:
    def __init__(self,n):
        self.lim=isqrt(n//2)+2; N=self.lim
        mu=[1]*(N+1); isp=[True]*(N+1); mu[0]=0
        for i in range(2,N+1):
            if isp[i]:
                for j in range(i,N+1,i):
                    if j>i: isp[j]=False
                    mu[j]=-mu[j]
                for j in range(i*i,N+1,i*i): mu[j]=0
        self.ds=[(d,mu[d]) for d in range(1,N+1,2) if mu[d]]
    def odd(self,x):
        Q=S=0
        for d,m in self.ds:
            d2=d*d
            if d2>x: break
            t=(x//d2+1)//2; Q+=m*t; S+=m*d2*t*t
        return Q,S
    def pref(self,x,p):
        if x<=0: return 0,0
        if p==1: return self.odd(x)
        Q,S=self.odd(x//2); return Q,2*S
def factor(n):
    ps=[]; 
    for p in (2,3,5,7,11,13,17,19,23,29,31,37):
        if n%p==0:
            ps.append(p)
            while n%p==0: n//=p
    if n==1: return ps
    def mr(m):
        if m<2: return False
        for p in (2,3,5,7,11,13,17,19,23,29,31,37):
            if m%p==0: return m==p
        d=m-1; s=0
        while d%2==0: d//=2; s+=1
        for a in (2,3,5,7,11,13,17,19,23,29,31,37):
            x=pow(a,d,m)
            if x in (1,m-1): continue
            for _ in range(s-1):
                x=x*x%m
                if x==m-1: break
            else: return False
        return True
    def rho(m):
        if m%2==0: return 2
        while True:
            c=random.randrange(1,m); x=y=random.randrange(m); d=1
            while d==1:
                x=(x*x+c)%m; y=(y*y+c)%m; y=(y*y+c)%m; d=gcd(abs(x-y),m)
            if d!=m: return d
    st=[n]
    while st:
        m=st.pop()
        if m==1: continue
        if mr(m): ps.append(m); continue
        d=rho(m); st+= [d,m//d]
    return sorted(set(ps))
class Coprime:
    def __init__(self,n):
        ps=factor(n); self.ds=[(1,1)]
        for p in ps: self.ds+=[(d*p,-m) for d,m in self.ds]
    def pref(self,x,p):
        if x<=0: return 0,0
        Q=S=0
        for d,m in self.ds:
            J=x//d
            if d%2==1:
                if p==1: t=(J+1)//2; c=t; s=t*t
                else: u=J//2; c=u; s=u*(u+1)
                Q+=m*c; S+=m*d*s
            elif p==0: Q+=m*J; S+=m*d*J*(J+1)//2
        return Q,S
def a_fast(n,side,oracle):
    if n<3: return 0
    w=weight(side,n); tot=Fraction(0)
    for L,R in pieces(side,n):
        if L>R: continue
        for p in (0,1):
            k1=L+((p-L)%2)
            if k1>R: continue
            Q1,S1=oracle.pref(R,p); Q0,S0=oracle.pref(k1-2,p)
            q=Q1-Q0; s=S1-S0
            if k1+2>R: tot+=w(k1)*q
            else:
                sl=Fraction(w(k1+2)-w(k1),2); ic=w(k1)-sl*k1
                tot+=ic*q+sl*s
    assert tot.denominator==1
    return int(tot)
SEQ={'A308453':('min','sqfree'),'A308455':('mid','sqfree'),'A308454':('max','sqfree'),
     'A308202':('min','coprime'),'A308209':('max','coprime'),'mid-coprime':('mid','coprime')}
def a(seq,n):
    side,kind=SEQ[seq]
    return a_fast(n,side,Sqfree(n) if kind=='sqfree' else Coprime(n))
