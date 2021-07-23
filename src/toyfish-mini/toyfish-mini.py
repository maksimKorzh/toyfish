m={'P':'♙','N':'♘','B':'♗','R':'♖','Q':'♕','K':'♔','p':'♟','n':'♞','b':'♝','r':'♜','q':'♛','k':'♚','.':'·',' ':' '}
P,N,B,R,Q,K=2854580560,5279650638,2958146,345426,355285329,355283019;C=127
p,n,b,r,q,k=2854580720,5279650798,2958306,345586,355285489,355283179;S=120
w=lambda s:[32]+s+[32];z=lambda p:[p]*8;e=[32]+[46]*8+[32];o=[32]*10;f=range;
b=o*2+w([r,n,b,q,k,b,n,r])+w(z(p)+w(e*4)+z(P))+w([R,N,B,Q,K,B,N,R])+o*2+[0,0,0]
O=lambda: print(''.join([' '+m[chr(b[i]&C)] if i%10 else '\n' for i in f(S)]));O()
def X(x):
 if x==0:
  v=0
  for s in f(120):
   t=b[s]
   if chr(t&C) not in ' .':
    v+=((t>>8)&15)*100 * (1 if chr(t&C).isupper() else -1)
    if chr(t&C).isupper():v+=j[s]
    if chr(t&C).islower():v-=j[s]
  return -v if b[-1] else v
 u,g,l=-1,-1,-10000
 for s in f(S):
  t=b[s]
  if chr(t&C) not in ' .' and (t>>7)&1==b[-1]:
   d=[(t>>13),[]]
   for a in f(4 if (t>>12)&1 else 2):d[1].append(d[0]&31);d[0]>>=5
   n=[-d for d in d[1]]
   if t==P:d[1]=n
   elif t!=p:d[1]+=n 
   for a in d[1]:
     h=s
     while 1:
      h+=a;c=b[h]
      if c==32:break
      if c!=46 and (c>>7)&1==b[-1]:break
      if chr(t&C) in 'Pp' and a in [9,11,-9,-11] and c == 46:break
      if chr(t&C) in 'Pp' and a in [10,20,-10,-20] and c != 46:break
      if t==P and a==-20 and s not in f(81,89):break
      if t==P and a==-20 and b[s-10] != 46:break
      if t==p and a==20 and s not in f(31,39):break
      if t==p and a==20 and b[s+10] != 46:break
      if chr(c&C) in 'Kk': return 10000
      b[s]=46;b[h]=t;b[-1]^=1
      if t==P and s in f(31,39):b[h]=Q
      if t==p and s in f(81,89):b[h]=q
      v=-X(x-1);b[s]=t;b[h]=c;b[-1]^=1;b[-2]=s;b[-3]=h
      if v>l:l=v;u=s;g=h;
      if c!=46 and (c>>7)&1==b[-1]^1:break
      if chr(t&C) in 'PpNnKk': break
 b[-2]=u;b[-3]=g
 return l
j=[(3-abs(int(int(str(s)[0])-5.5)))**2+((3-abs(int(int(str(s)[1])-4.5))))**2 if b[s]!=32 else 0 for s in f(120)]
while 1:
 y=input(' Your move: ')
 u=(10-(ord(y[1])-ord('0')))*10+ord(y[0])-ord('a')+1
 g=(10-(ord(y[3])-ord('0')))*10+ord(y[2])-ord('a')+1
 b[g]=b[u];b[u]=46;
 if b[g]==P and u in f(31,39):b[g]=Q
 O();b[-1]^=1;s=X(3);b[b[-3]]=b[b[-2]];b[b[-2]]=46;
 if b[b[-3]]==p and b[-2] in f(81,89):b[b[-3]]=q
 O();b[-1]^=1
 if abs(s) == 10000: print(' Checkmate!'); break
