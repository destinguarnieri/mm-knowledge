https://arxiv.org/abs/1105.3115

Noname manuscript No.
(will be inserted by the editor)
Dealing with the Inventory Risk
A solution to the market making problem
Olivier Gu´eant Charles-Albert Lehalle
Joaquin Fernandez-Tapia
arXiv:1105.3115v5 [q-fin.TR] 3 Aug 2012
This draft: July 2012
Abstract Market makers continuously set bid and ask quotes for the stocks
they have under consideration. Hence they face a complex optimization prob-
lem in which their return, based on the bid-ask spread they quote and the fre-
quency at which they indeed provide liquidity, is challenged by the price risk
they bear due to their inventory. In this paper, we consider a stochastic con-
trol problem similar to the one introduced by Ho and Stoll [17] and formalized
mathematically by Avellaneda and Stoikov [3]. The market is modeled using
a reference price St following a Brownian motion with standard deviation σ,
arrival rates of buy or sell liquidity-consuming orders depend on the distance
to the reference price St and a market maker maximizes the expected utility of
its P&L over a finite time horizon. We show that the Hamilton-Jacobi-Bellman
equations associated to the stochastic optimal control problem can be trans-
formed into a system of linear ordinary diﬀerential equations and we solve the
market making problem under inventory constraints. We also shed light on the
asymptotic behavior of the optimal quotes and propose closed-form approxi-
This research has been conducted within the Research Initiative “Microstructure des
March´es Financiers” under the aegis of the Europlace Institute of Finance.
Olivier Gu´eant
Universit´e Paris-Diderot, UFR de Math´ematiques, Laboratoire Jacques-Louis Lions. 175,
rue du Chevaleret, 75013 Paris, France.
E-mail: olivier.gueant@ann.jussieu.fr
Charles-Albert Lehalle
Head of Quantitative Research, Cr´edit Agricole Cheuvreux. 9, Quai du Pr´esident Paul
Doumer, 92400 Courbevoie, France.
E-mail: clehalle@cheuvreux.com
Joaquin Fernandez-Tapia
Universit´e Pierre et Marie Curie, LPMA. 4 place Jussieu, 75005 Paris, France.
2 Olivier Gu´eant et al.
mations based on a spectral characterization of the optimal quotes.
Keywords Stochastic optimal control· High-frequency Market Making·
Avellaneda-Stoikov problem
1 Introduction
From a quantitative viewpoint, market microstructure is a sequence of auc-
tion games between market participants. It implements the balance between
supply and demand, forming an equilibrium traded price to be used as refer-
ence for valuation. The rule of each auction game (fixing auction, continuous
auction, ...) is fixed by the firm operating each trading venue. Nevertheless,
most of all trading mechanisms on electronic markets rely on market partic-
ipants sending orders to a “queuing system” where their open interests are
consolidated as “liquidity provision” or form transactions [1]. The eﬃciency
of such a process relies on an adequate timing between buyers and sellers, to
avoid too many non-informative oscillations of the transaction price (for more
details and modeling, see for example [20]).
In practice, it is possible to provide liquidity to an impatient buyer (re-
spectively seller) and maintain an inventory until the arrival of the next im-
patient seller (respectively buyer). Market participants focused on this kind of
liquidity-providing activity are called “market makers”. On one hand they are
buying at the bid price and selling at the ask price they choose, making money
out of this “bid-ask spread”. On the other hand, their inventory is exposed to
price fluctuations mainly driven by the volatility of the market (see [2, 5, 10,
11, 18, 24]).
The recent evolution of both technology and market regulation reshaped
the nature of the interactions between market participants during continuous
electronic auctions, one consequence being the emergence of “high-frequency
market makers” who are said to be part of 70% of the electronic trades in
the US (40% in the EU and 35% in Japan) and have a massively passive
(i.e. liquidity-providing) behavior – a typical balance between passive and
aggressive orders for such market participants being around 80% of passive
interactions (see [22]).
From a mathematical modeling point of view, the market making problem
corresponds to the choice of optimal quotes (i.e. the bid and ask prices) that
such agents provide to other market participants, taking into account their in-
ventory limits and their risk constraints often represented by a utility function
(see [9, 16, 19, 21, 23, 25]).
Avellaneda and Stoikov proposed, in a widely cited paper [3], an innovative
framework for “market making in an order book”. In their approach, rooted to
Dealing with the Inventory Risk 3
an old paper by Ho and Stoll [17], the market is modeled using a reference price
or fair price St following a Brownian motion with standard deviation σ, and
the arrival of a buy or sell liquidity-consuming order at a distance δ from the
reference price St is described by a point process with intensity Aexp(−kδ),
A and k being two positive constants which characterize statistically the liq-
uidity of the stock.
We consider the same model as in [3] – adding inventory limits – and
we show, using a new change of variables, that the Hamilton-Jacobi-Bellman
equations associated to the problem boil down to a system of linear ordinary
diﬀerential equations. This new change of variables (i) simplifies the compu-
tation of a solution since numerical approximation of partial diﬀerential equa-
tions is now unnecessary, and (ii) allows to study the asymptotic behavior
of the optimal quotes. In addition to these two contributions, we use results
from spectral analysis to provide an approximation of the optimal quotes in
closed-form. Finally, we provide in the case of our model with inventory limits
a verification theorem that was absent from the original paper (the admissi-
bility of the quotes obtained in the original Avellaneda-Stoikov model appears
in fact to be an open problem!).
Since Avellaneda and Stoikov seminal paper, other authors have consid-
ered related market making models. Cartea, Jaimungal and Ricci [8] consider a
more sophisticated model inspired from the Avellaneda-Stoikov one1, including
richer dynamics of market orders, impact on the limit order book, adverse se-
lection eﬀects and predictable α. They obtained closed-form approximations of
the optimal quotes using a first-order Taylor expansion. Cartea and Jaimungal
[7] recently used a similar model to introduce risk measures for high-frequency
trading. Earlier, they used a model inspired from Avellaneda-Stoikov [6] in
which the mid-price is modeled by a Hidden Markov Model. Guilbaud and
Pham [14] also used a model inspired from the Avellaneda-Stoikov framework
but including market orders and limit orders at best (and next to best) bid
and ask together with stochastic spreads. Very recently, Guilbaud and Pham
[15] used another model inspired from the Avellanada-Stoikov one in a pro-
rata microstructure.
It is also noteworthy that the model we use to find the orders a market
maker should optimally send to the market has been used in a totally diﬀerent
domain of algorithmic trading: optimal execution. Bayraktar and Ludkovski
[4] and Gu´eant, Lehalle, Fernandez-Tapia [12] used indeed a similar model to
optimally liquidate a portfolio.
This paper starts in section 2 with the description of the model. Section 3 is
dedicated to the introduction of our change of variables and solves the control
problem in the presence of inventory limits. Section 4 focuses on the asymptotic
1 The objective function is diﬀerent.
4 Olivier Gu´eant et al.
behavior of the optimal quotes and characterizes the asymptotic value using
an eigenvalue problem that allows to propose a rather good approximation
in closed-form. Section 5 generalizes the model in two diﬀerent directions: (i)
the introduction of a drift in the price dynamics and (ii) the introduction
of market impact that may also be regarded as adverse selection. Section 6
carries out the comparative statics. Section 7 provides backtests of the model.
Adaptations of our results are in use at Cheuvreux.
2 Setup of the model
Let us fix a probability space (Ω,F ,P) equipped with a filtration (Ft)t≥0 satis-
fying the usual conditions. We assume that all random variables and stochastic
processes are defined on (Ω,F ,(Ft)t≥0,P).
We consider a high-frequency market maker operating on a single stock2
.
We suppose that the mid-price of this stock or more generally a reference
price3 of the stock moves as an arithmetic Brownian motion4:
dSt = σdWt
The market maker under consideration will continuously propose bid and
ask prices denoted respectively Sb
t and Sa
t and will hence buy and sell shares
according to the rate of arrival of market orders at the quoted prices. His
inventory q, that is the (signed) quantity of shares he holds, is given by
qt = Nb
t− Na
t
where Nb and Na are the point processes (independent of (Wt)t) giving the
number of shares the market maker respectively bought and sold (we assume
that transactions are of constant size, scaled5 to 1). Arrival rates obviously
depend on the prices Sb
t and Sa
t quoted by the market maker and we assume,
in accordance with the model proposed by Avellaneda and Stoikov [3], that
intensities λb and λa associated respectively to Nb and Na depend on the
diﬀerence between the quoted prices and the reference price (i.e. δb
t = St− Sb
t
and δa
t = Sa
t− St) and are of the following form6:
λb(δb) = Ae−kδb
= Aexp(−k(s−sb)) λa(δa) = Ae−kδa
= Aexp(−k(sa
−s))
2 We suppose that this high-frequency market maker does not “make” the price in the
sense that he has no market power. In other words, we assume that the size of his orders
is small enough to consider price dynamics exogenous. Market impact will be introduced in
section 5.
3 This reference price for the stock can be thought of as a smoothed mid-price for instance.
4 Since we will only consider short horizon problems, this assumption is almost equivalent
to the usual Black-Scholes one.
5 The only important hypothesis is the constant size of orders since we can easily replace
1 by any positive size ∆.
6 Some authors also used a linear form for the intensity functions – see [17] for instance.
Dealing with the Inventory Risk 5
where A and k are positive constants that characterize the liquidity of the
stock. In particular, this specification means – for positive δb and δa – that
the closer to the reference price an order is posted, the faster it will be executed.
As a consequence of his trades, the market maker has an amount of cash
evolving according to the following dynamics:
dXt = (St + δa
t )dNa
t− (St− δb
t )dNb
t
To this original setting introduced by Avellaneda and Stoikov (itself fol-
lowing partially Ho and Stoll [17]), we add a bound Q to the inventory that
a market maker is authorized to have. In other words, we assume that a mar-
ket maker with inventory Q (Q>0 depending in practice on risk limits) will
never set a bid quote and symmetrically that a market maker with inventory
−Q, that is a short position of Qshares in the stock under consideration, will
never set an ask quote. This realistic restriction may be read as a risk limit
and allows to solve rigorously the problem.
Now, coming to the objective function, the market maker has a time horizon
T and his goal is to optimize the expected utility of his P&L at time T. In
line with [3], we will focus on CARA utility functions and we suppose that the
market maker optimizes:
sup
E[− exp (−γ(XT + qT ST ))]
(δa
t )t ,(δb
t )t ∈A
where A is the set of predictable processes bounded from below, γ is the
absolute risk aversion coeﬃcient characterizing the market maker, XT is the
amount of cash at time T and qT ST is the evaluation of the (signed) remaining
quantity of shares in the inventory at time T (liquidation at the reference price
ST
7).
3 Characterization of the optimal quotes
The optimization problem set up in the preceding section can be solved using
the classical tools of stochastic optimal control. The first step of our reason-
ing is therefore to introduce the Hamilton-Jacobi-Bellman (HJB) equation
associated to the problem. More exactly, we introduce a system of Hamilton-
Jacobi-Bellman partial diﬀerential equations which consists of the following
equations indexed by q∈ {−Q,...,Q} for (t,s,x) ∈ [0,T] × R2:
7 Our results would be mutatis mutandis the same if we added a penalization term
−b(|qT|) for the shares remaining at time T . The rationale underlying this point is that
price risk prevents the trader from having important exposure to the stock. Hence, qt should
naturally mean-revert around 0.
6 Olivier Gu´eant et al.
For |q| <Q:
+ sup
δb
+ sup
δa
∂tu(t,x,q,s) + 1
σ2∂2
ssu(t,x,q,s)
2
λb(δb) u(t,x− s+ δb,q+ 1,s)− u(t,x,q,s)
λa(δa) [u(t,x+ s+ δa,q− 1,s)− u(t,x,q,s)] = 0
For q= Q:
+ sup
δa
∂tu(t,x,Q,s) + 1
σ2∂2
ssu(t,x,Q,s)
2
λa(δa) [u(t,x+ s+ δa,Q− 1,s)− u(t,x,Q,s)] = 0
For q=−Q:
∂tu(t,x,−Q,s) + 1
σ2∂2
ssu(t,x,−Q,s)
2
+ sup
δb
with the final condition:
λb(δb) u(t,x− s+ δb
,−Q+ 1,s)− u(t,x,−Q,s) = 0
∀q∈ {−Q,...,Q}, u(T,x,q,s) =− exp (−γ(x+ qs))
To solve these equations we will use a change of variables based on two
diﬀerent ideas. First, the choice of a CARA utility function allows to factor
out the Mark-to-Market value of the portfolio (x+ qs). Then, the exponential
decay for the intensity functions λb and λa allows to reduce the Hamilton-
Jacobi-Bellman (HJB) equations associated to our control problem to a linear
system of ordinary diﬀerential equations:
Proposition 1 (Change of variables for (HJB)) Let us consider a fam-
ily (vq )|q|≤Q of positive functions solution of:
∀q∈ {−Q+ 1,...,Q− 1},˙
vq (t) = αq2vq (t)− η(vq−1(t) + vq+1(t))
˙
vQ(t) = αQ2vQ(t)− ηvQ−1(t)
˙
v−Q(t) = αQ2v−Q(t)− ηv−Q+1(t)
with ∀q∈ {−Q,...,Q},vq(T) = 1, where α=
k
2γσ2 and η= A(1 + γ
k )−(1+k
γ )
γ
Then, u(t,x,q,s) =− exp(−γ(x+ qs))vq (t)−
k is solution of (HJB).
.
Then, the following proposition proves that there exists such a family of
positive functions:
Dealing with the Inventory Risk 7
Proposition 2 (Solution of the ordinary diﬀerential equations) Let us
introduce the matrix M defined by:
M=
.
            αQ2
  
−η 0· · · · · · · · · 0
.
−η α(Q− 1)2
−η 0.
.
.
.
.
.
.
.
.
0.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
. 0
.
.
.
.
.
.
.
.
. 0−η α(Q− 1)2
−η
0· · · · · · · · · 0−η αQ2
              
where α=
k
2γσ2 and η= A(1 + γ
k )−(1+k
γ )
.
Let us define
v(t) = (v−Q(t),v−Q+1(t),...,v0(t),...,vQ−1(t),vQ(t))′
= exp(−M(T− t)) × (1,...,1)′
Then, (vq )|q|≤Q is a family of positive functions solution of the equations of
Proposition 1.
Using the above change of variables and a verification approach, we are
now able to solve the stochastic control problem, that is to find the value
function of the problem and the optimal quotes:
Theorem 1 (Solution of the control problem) Let consider (vq )|q|≤Q as
in Proposition 2.
Then u(t,x,q,s) =− exp(−γ(x+ qs))vq (t)−
γ
k is the value function of the
control problem.
Moreover, the optimal quotes are given by:
s− sb∗(t,q,s) = δb∗(t,q) = 1
kln vq (t)
vq+1(t) +
1
γ
ln 1 + γ
k , q̸= Q
sa∗(t,q,s)− s= δa∗(t,q) = 1
kln vq (t)
vq−1(t) +
1
γ
ln 1 + γ
k , q̸=−Q
and the resulting bid-ask spread quoted by the market maker is given by:
ψ∗(t,q) =−
1
kln vq+1(t)vq−1(t)
vq (t)2 +
2
γ
ln 1 + γ
k , |q| ̸= Q
8 Olivier Gu´eant et al.
4 Asymptotic behavior and approximation of the optimal quotes
To exemplify our findings and in order to motivate the asymptotic approxi-
mations we shall provide, we plotted on Figure 1 and Figure 2 the behavior
with time and inventory of the optimal quotes. The resulting bid-ask spread
quoted by the market maker is plotted on Figure 3.
We clearly see that the optimal quotes are almost independent of t, as
soon as tis far from the terminal time T. This observation is at odds with the
approximations proposed8 in Avellaneda and Stoikov [3] using an expansion
in q. It motivates however the study of the asymptotic behavior of the quotes.
s − sb [Tick]
5.5
5
4.5
4
3.5
3
2.5
2
1.5
1
600
500
400
30
300
20
200
10
100
−10
−20
Time [Sec]
0
−30
0
Inventory
Fig. 1 Behavior of the optimal bid quotes with time and inventory. σ = 0.3 A = 0.9 s 1
, k = 0.3 Tick 1
, γ = 0.01 Tick 1
, T = 600 s.
Tick· s 1/2
,
8 In [3], the approximations obtained by the authors using an expansion in q leads to the
following expressions:
δb
t ≃
δa
t ≃
1
γ
1
ln 1 + γ
k + 1 + 2q
2 γσ2(T− t)
ln 1 + γ
k +
1− 2q
2 γσ2(T− t)
γ
One can easily show, using the results of Theorem 1, that these approximations are nothing
but the Taylor expansions of the optimal quotes for t close to T.
Dealing with the Inventory Risk 9
s
a − s [Tick]
5.5
5
4.5
4
3.5
3
2.5
2
1.5
1
−30
600
500
−20
−10
200
0
10
Inventory
100
20
30 0
400
300
Time [Sec]
Fig. 2 Behavior of the optimal ask quotes with time and inventory. σ = 0.3 A = 0.9 s 1
, k = 0.3 Tick 1
, γ = 0.01 Tick 1
, T = 600 s.
Tick· s 1/2
,
ψ [Tick]
6.64
6.63
6.62
6.61
6.6
6.59
6.58
6.57
6.56
6.55
−30
600
500
−20
−10
200
0
10
Inventory
100
20
30 0
400
300
Time [Sec]
Fig. 3 Behavior of the resulting bid-ask spread with time and inventory. σ = 0.3 s 1/2
, A = 0.9 s 1
, k = 0.3 Tick 1
, γ = 0.01 Tick 1
, T = 600 s.
Tick·
10 Olivier Gu´eant et al.
Theorem 2 (Asymptotics for the optimal quotes) The optimal quotes
have asymptotic limits
lim
δb∗(0,q) = δb∗
∞(q)
T →+∞
lim
δa∗(0,q) = δa∗
∞ (q)
T →+∞
that can be expressed as:
δb∗
∞(q) = 1
γ
ln 1 + γ
k +
1
q
kln f0
f0
q+1
δa∗
∞ (q) = 1
γ
ln 1 + γ
k +
1
q
kln f0
f0
q−1
where f0 ∈ R2Q+1 is an eigenvector corresponding to the smallest eigenvalue
of the matrix M introduced in Proposition 2 and characterized (up to a mul-
tiplicative constant) by:
f0 ∈ argmin
f ∈ 2Q+1
,∥f ∥2=1
Q
q=−Q
αq2fq
2 + η
Q−1
q=−Q
(fq+1− fq )2 + ηfQ
2 + ηf−Q
2
The resulting bid-ask spread quoted by the market maker is asymptotically:
ψ∗
∞(q) =−
1
kln f0
q+1f0
q−1
f0
q
2 +
2
γ
ln 1 + γ
k
The above result, along with the example of Figure 1, Figure 2 and Figure
3, encourages to approximate the optimal quotes and the resulting bid-ask
spread by their asymptotic value. These asymptotic values depend on f0 and
we shall provide a closed-form approximation for f0
.
The above characterization of f0 corresponds to an eigenvalue problem in
R2Q+1 and we propose to replace it by a similar eigenvalue problem in L2(R)
for which a closed-form solution can be computed. More precisely we replace
the criterion
f0 ∈ argmin
f ∈ 2Q+1
,∥f ∥2=1
Q
q=−Q
αq2fq
2 + η
Q−1
q=−Q
(fq+1− fq )2 + ηfQ
2 + ηf−Q
2
by the following criterion for
˜
f0 ∈ L2(R):
˜
f0 ∈ argmin
∥˜
f ∥L2( )=1
+∞
−∞
αx2˜
˜
f(x)2 + η
f′(x)2 dx
The introduction of this new criterion is rooted to the following proposition
˜
that states (up to its sign) the expression for
f0 in closed form:
Dealing with the Inventory Risk Proposition 3 Let us consider
˜
f0 ∈ argmin
∥˜
f ∥L2( )=1
αx2˜
˜
f(x)2 + η
f′(x)2 dx
Then:
˜
f0(x) = ±
1
π
4
1
α
η
1
8
exp−
1
2
α
η
x2
11
From the above proposition, we expect f0
q to behave, up to a multiplicative
constant, as exp−
1
2
α
η q2 . This heuristic viewpoint induces an approxima-
tion of the optimal quotes and the resulting optimal bid-ask-spread:
δb∗
∞(q) ≃
≃
δa∗
∞ (q) ≃
≃
1
γ
1
γ
1
γ
1
γ
ln 1 + γ
k +
ln 1 + γ
k +
ln 1 + γ
k−
ln 1 + γ
k−
1
2k
α
η(2q+ 1)
2q+ 1
2
σ2γ
2kA 1 + γ
k
1
2k
α
η(2q− 1)
2q− 1
2
σ2γ
2kA 1 + γ
k
2
ψ∗
∞(q) ≃
γ
ln 1 + γ
k +
σ2γ
1+k
2kA 1 + γ
k
γ
1+k
γ
1+k
γ
s − sb [Tick]
10
8
6
4
2
0
−2
−4
s − sb [Tick]
7
6
5
4
3
2
1
0
−30 −20 −10 0 10 20 Inventory
30
−30 −20 −10 0 10 20 30
Inventory
Fig. 4 Asymptotic behavior of optimal bid quote (bold line). Approximation (dotted line).
Left: σ = 0.4 Tick· s 1/2
, A = 0.9 s 1
, k = 0.3 Tick 1
, γ = 0.01 Tick 1
, T=
600 s. Right: σ = 1.0 Tick· s 1/2
, A = 0.2 s 1
, k = 0.3 Tick 1
, γ = 0.01 Tick 1
,
T = 600 s.
We exhibit on Figure 4 and Figure 5 the values of the optimal quotes, along
with their associated approximations. Empirically, these approximations for
12 Olivier Gu´eant et al.
s
a − s [Tick]
10
8
6
4
2
0
−2
−4
s
a − s [Tick]
7
6
5
4
3
2
1
0
−30 −20 −10 0 10 20 Inventory
30
−30 −20 −10 0 10 20 30
Inventory
Fig. 5 Asymptotic behavior of optimal ask quote (bold line). Approximation (dotted line).
Left: σ = 0.4 Tick· s 1/2
, A = 0.9 s 1
, k = 0.3 Tick 1
, γ = 0.01 Tick 1
, T=
600 s. Right: σ = 1.0 Tick· s 1/2
, A = 0.2 s 1
, k = 0.3 Tick 1
, γ = 0.01 Tick 1
,
T = 600 s.
the quotes are satisfactory in most cases and are always very good for small
values of the inventory q. In fact, even though f0 appears to be well approxi-
mated by the gaussian approximation, we cannot expect a very good fit for the
quotes when q is large because we are approximating expressions that depend
on ratios of the form f 0
q
f 0
q
or
f 0
q+1
f 0
.
q−1
5 Extensions of the model
5.1 The case of a trend in the price dynamics
So far, the reference price was supposed to be a Brownian motion. In what
follows we extend the model to the case of a trend in the price dynamics:
dSt = µdt+ σdWt
In that case we have the following proposition (the proof is not repeated):
Proposition 4 (Solution with a drift) Let us consider a family of func-
tions (vq )|q|≤Q solution of the linear system of ODEs that follows:
∀q∈ {−Q+ 1,...,Q− 1},˙
vq (t) = (αq2
− βq)vq (t)− η(vq−1(t) + vq+1(t))
˙
vQ(t) = (αQ2
− βQ)vQ(t)− ηvQ−1(t)
˙
v−Q(t) = (αQ2 + βQ)v−Q(t)− ηv−Q+1(t)
with ∀q ∈ {−Q,...,Q},vq (T) = 1, where α =
k
2γσ2
, β= kµ and η=
A(1 + γ
k )−(1+k
γ )
.
Then, u(t,x,q,s) =− exp(−γ(x+ qs))vq (t)−
γ
k is the value function of the
control problem.
Dealing with the Inventory Risk 13
The optimal quotes are given by:
s− sb∗(t,q,s) = δb∗(t,q) = 1
kln vq (t)
vq+1(t) +
1
γ
ln 1 + γ
k
sa∗(t,q,s)− s= δa∗(t,q) = 1
kln vq (t)
vq−1(t) +
1
γ
ln 1 + γ
k
and the resulting bid-ask spread of the market maker is :
ψ∗(t,q) =−
1
kln vq+1(t)vq−1(t)
vq (t)2 +
2
γ
ln 1 + γ
k
Moreover,
lim
T →+∞
δb∗(0,q) = 1
γ
ln 1 + γ
k +
1
q
kln f0
f0
q+1
lim
T →+∞
δa∗(0,q) = 1
γ
lim
ψ∗(0,q) =−
T →+∞
ln 1 + γ
k +
1
q
kln f0
f0
q−1
1
kln f0
q+1f0
q−1
f0
q
2 +
2
γ
ln 1 + γ
k
where f0 is an eigenvector corresponding to the smallest eigenvalue of:
              
αQ2
− βQ−η 0· · · · · · · · · 0
−η α(Q− 1)2
− β(Q− 1)−η 0.
.
.
.
.
.
0.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
. 0
.
.
.
0· · · .
.
. 0−η α(Q− 1)2
· · · · · · 0−η − β(Q− 1)−η
αQ2
.
.
.
.
.
.
.
.
.
− βQ
              
In addition to this theoretical result, we can consider an approximation
similar to the approximation used for the initial model with no drift. We then
obtain the following approximations for the optimal quotes and the bid-ask
spread:
δb∗
∞(q) ≃
δa∗
∞ (q) ≃
1
γ
ln 1 + γ
k +−
µ
γσ2 +
2q+ 1
2
σ2γ
2kA 1 + γ
k
1
γ
ln 1 + γ
k + µ
γσ2−
2q− 1
2
σ2γ
2kA 1 + γ
k
ψ∗
∞(q) ≃
2
γ
ln 1 + γ
k +
σ2γ
2kA 1 + γ
k
1+k
γ
1+k
γ
1+k
γ
14 Olivier Gu´eant et al.
5.2 The case of market impact
Another extension of the model consists in introducing market impact. The
simplest way to proceed is to consider the following dynamics for the price:
dSt = σdWt + ξdNa
t− ξdNb
t , ξ >0
When a limit order on the bid side is filled, the reference price decreases. On
the contrary, when a limit order on the ask side is filled, the reference price in-
creases. This is in line with the classical modeling of market impact for market
orders, ξ being a constant since the limit orders posted by the market maker
are all supposed to be of the same size.
Adverse selection is another way to interpret the interaction we consider be-
tween the price process and the point processes modeling execution: trades on
the bid side are often followed by a price decrease and, conversely, trades on
the ask side are often followed by a price increase.
In this modified framework, the problem can be solved using a change of
variables that is slightly more involved than the one presented above but the
method is exactly the same and we have the following proposition (the proof
is not repeated):
Proposition 5 (Solution with market impact) Let us consider a family
of functions (vq )|q|≤Q solution of the linear system of ODEs that follows:
∀q∈ {−Q+ 1,...,Q− 1},˙
vq (t) = αq2vq (t)− ηe−
k
2 ξ (vq−1(t) + vq+1(t))
˙
vQ(t) = αQ2vQ(t)− ηe−
˙
v−Q(t) = αQ2v−Q(t)− ηe−
with ∀q ∈ {−Q,...,Q},vq (T) = exp(−
A(1 + γ
k )−(1+k
γ )
.
k
2 ξ vQ−1(t)
k
2 ξ v−Q+1(t)
1
2kξq2), where α =
k
2γσ2 and η=
Then, u(t,x,q,s) =− exp(−γ(x+ qs+ 1
2ξq2))vq (t)−
of the control problem.
γ
k is the value function
The optimal quotes are given by:
s− sb∗(t,q,s) = δb∗(t,q) = 1
kln vq (t)
vq+1(t) + ξ
2 +
1
γ
ln 1 + γ
k
sa∗(t,q,s)− s= δa∗(t,q) = 1
kln vq (t)
vq−1(t) + ξ
2 +
and the resulting bid-ask spread of the market maker is :
1
γ
ln 1 + γ
k
ψ∗(t,q) =−
1
kln vq+1(t)vq−1(t)
vq (t)2 + ξ+
2
γ
ln 1 + γ
k
Dealing with the Inventory Risk Moreover,
15
lim
T →+∞
δb∗(0,q) = 1
γ
ln 1 + γ
k + ξ
2 +
1
q
kln f0
f0
q+1
lim
T →+∞
δa∗(0,q) = 1
γ
ln 1 + γ
k + ξ
2 +
1
q
kln f0
f0
q−1
1
lim
ψ∗(0,q) =−
T →+∞
kln f0
q+1f0
q−1
f0
q
2 + ξ+
2
γ
ln 1 + γ
k
where f0 is an eigenvector corresponding to the smallest eigenvalue of:
               
αQ2
k
−ηe−
2 ξ 0· · · · · · · · · 0
k
−ηe−
2 ξ α(Q− 1)2
k
−ηe−
2 ξ 0.
.
.
.
.
.
.
.
.
.
0.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
. 0
.
.
.
k
.
.
.
.
.
. 0−ηe−
2 ξ α(Q− 1)2
k
−ηe−
2 ξ
k
0· · · · · · · · · 0−ηe−
2 ξ αQ2
               
In addition to this theoretical result, we can consider an approximation
similar to the approximation used for the initial model. We then obtain the
following approximations for the optimal quotes and the bid-ask spread:
δb∗
∞(q) ≃
1
γ
ln 1 + γ
k + ξ
2 +
2q+ 1
2
e
k
4 ξ σ2γ
2kA 1 + γ
k
1+k
γ
δa∗
∞ (q) ≃
1
γ
ln 1 + γ
k + ξ
2−
2q− 1
2
e
k
4 ξ σ2γ
2kA 1 + γ
k
1+k
γ
ψ∗
∞(q) ≃
2
γ
ln 1 + γ
k + ξ+ e
k
4 ξ σ2γ
1+k
2kA 1 + γ
k
γ
6 Comparative statics
We argued in section 4 that the value of the optimal quotes was almost inde-
pendent of tfor tsuﬃciently far from the terminal time T and we characterized,
using spectral arguments, the asymptotic value of the optimal quotes. In or-
der to obtain closed-form formulae, we also provided approximations for the
asymptotic value of the optimal quotes. Although these closed-form formu-
lae are only approximations, they provide a rather good intuition about the
influence of the diﬀerent parameters on the optimal quotes.
16 Olivier Gu´eant et al.
6.1 Dependence on σ2
The dependence of optimal quotes on σ2 depends on the sign of the inventory.
More precisely, we observe numerically, in accordance with the approximations,
that:
    
∂δb∗
∞
∂σ2 <0,
∂δb∗
∞
∂σ2 >0,
∂δb∗
∞
∂σ2 >0,
∂δa∗
∞
∂σ2 >0,if q<0
∂δa∗
∞
∂σ2 >0,if q= 0
∂δa∗
∞
∂σ2 <0,if q>0
For the bid-ask spread, we obtain:
∂ψ∗
∞
∂σ2 >0
The rationale behind this is that an increase in σ2 increases inventory risk.
Hence, to reduce this risk, a market maker that has a long position will try
to reduce his exposure and hence ask less for his stocks (to get rid of some
of them) and accept to buy at a lower price (to avoid buying new stocks).
Similarly, a market maker with a short position tries to buy stocks, and hence
increases its bid quote, while avoiding short selling new stocks, and he increases
its ask quote to that purpose. Overall, due to the increase in price risk, the
bid-ask spread widens as it is well instanced in the case of a market maker with
a flat position (this one wants indeed to earn more per trade to compensate
the increase in inventory risk).
6.2 Dependence on µ
The dependence of optimal quotes on the drift µis straightforward and corre-
sponds to the intuition. If the agent expect the price to increase (resp. decrease)
he will post orders with higher (resp. lower) prices. Hence we have:
∂δb∗
∞
∂µ <0,
∂δa∗
∞
∂µ >0
6.3 Dependence on A
Because of the form of the system of equations that defines v, the dependence
on A must be the exact opposite of the dependence on σ2:
    
∂δb∗
∞
∂A >0,
∂δb∗
∞
∂A <0,
∂δb∗
∞
∂A <0,
∂δa∗
∞
∂A <0,if q<0;
∂δa∗
∞
∂A <0,if q= 0
∂δa∗
∞
∂A >0,if q>0
Dealing with the Inventory Risk 17
For the bid-ask spread, we obtain:
∂ψ∗
∞
∂A <0
The rationale behind these results is that an increase in A reduces the
inventory risk. An increase in A indeed increases the frequency of trades and
hence reduces the risk of being stuck with a large inventory (in absolute value).
For this reason, an increase in A should have the same eﬀect as a decrease in
σ2
.
6.4 Dependence on γ
Using the closed-form approximations, we see that the dependence on γ is
ambiguous. The market maker faces indeed two diﬀerent risks that contribute
to inventory risk: (i) trades occur at random times and (ii) the reference price
is stochastic. But if risk aversion increases, the market maker will mitigate
the two risks: (i) he may set his quotes closer to one another to reduce the
randomness in execution and (ii) he may widen his spread to reduce price
risk. The tension between these two roles played by γ explains the diﬀerent
behaviors we may observe, as on Figure 6 and Figure 7 for the bid-ask spread
resulting from the asymptotic optimal quotes:
Spread [Tick]
7
6.5
6
5.5
5
4.5
4
30
0
0.1
0.2
20
0.3
10
0
0.4
−10
−20
−30
0.5
γ
Inventory
Fig. 6 Bid-ask spread resulting from the asymptotic optimal quotes for diﬀerent inventories
and diﬀerent values for the risk aversion parameter γ. σ = 0.3 Tick· s 1/2
, A = 0.9 s 1
,
k = 0.3 Tick 1
, T = 600 s.
18 Olivier Gu´eant et al.
Spread [Tick]
2.5
2.4
2.3
2.2
2.1
2
1.9
1.8
30
0
0.1
0.2
20
0.3
10
0
0.4
−10
−20
−30
0.5
γ
Inventory
Fig. 7 Bid-ask spread resulting from the asymptotic optimal quotes for diﬀerent inventories
and diﬀerent values for the risk aversion parameter γ. σ = 0.6 Tick· s 1/2
, A = 0.9 s 1
,
k = 0.9 Tick 1
, T = 600 s.
6.5 Dependence on k
From the closed-form approximations, we expect δb∗
∞ to be decreasing in k for
q greater than some negative threshold. Below this threshold, we expect it to
be increasing. Similarly we expect δa∗
∞ to be decreasing in k for q smaller than
some positive threshold. Above this threshold we expect it to be increasing.
Eventually, as far as the bid-ask spread is concerned, the closed-form ap-
proximations indicate that the resulting bid-ask spread should be a decreasing
function of k.
∂ψ∗
∞
∂k <0
In fact several eﬀects are in interaction. On one hand, there is a “no-volatility”
eﬀect that is completely orthogonal to any reasoning on the inventory risk:
when k increases, in a situation where δb and δa are positive, trades occur
closer to the reference price St. For this reason, and in absence of inventory
risk, the optimal bid-ask spread has to shrink. However, an increase in k also
aﬀects the inventory risk since it decreases the probability to be executed (for
δb,δa > 0). Hence, an increase in k is also, in some aspects, similar to a de-
crease in A. These two eﬀects explain the expected behavior.
Dealing with the Inventory Risk 19
s sb [Tick]
10
8
6
4
2
0
−2
2
30
20
1.5
10
1
k [Tick ]
0.5
0
−30
−20
0
−10
Inventory
Fig. 8 Asymptotic optimal bid quotes for diﬀerent inventories and diﬀerent values of k.
σ = 0.3 Tick· s 1/2
, A = 0.9 s 1
, γ = 0.01 Tick 1
, T = 600 s.
Numerically, we observed that the “no-volatility” eﬀect dominated for the
values of the inventory under consideration (see Figure 8 for the case of the
bid quote9).
6.6 Dependence on the market impact ξ
The market impact introduced in 5.2 has two eﬀects on the optimal quotes. In
the absence of price risk, given the functional form of the execution intensities,
the direct eﬀect of ξ is approximately to add ξ
2 the each optimal quote: the
market maker approximately maintains his profit per round trip on the market
but the probability of occurrence of a trade is reduced. This adverse selection
eﬀect has a side-eﬀect linked to inventory risk: since adverse selection gives
the market maker an incentive to post orders deeper in the book, it increases
the risk of being stuck with a large inventory for a market maker holding
such an inventory. As a consequence, for a trader holding a positive (resp.
negative) inventory, there is a second eﬀect inciting to buy and sell at lower
(resp. higher) prices. These two eﬀects are clearly highlighted by the closed-
form approximations exhibited in the previous section:
1
δb∗
∞(q) ≃
γ
ln 1 + γ
k + ξ
2
adverse selection
+
9 The case of the ask quote is obviously similar.
2q+ 1
2
k
e
4 ξ
side−ef f ect
σ2γ
2kA 1 + γ
k
1+k
γ
20 Olivier Gu´eant et al.
δa∗
∞ (q) ≃
1
γ
ln 1 + γ
k + ξ
2
adverse selection
−
2q− 1
2
k
e
4 ξ
side−ef f ect
σ2γ
1+k
2kA 1 + γ
k
γ
7 Backtests
Before using the above model on historical data, we need to discuss some fea-
tures of the model that need to be adapted before any backtest is possible.
First of all, the model is continuous in both time and space while the real
control problem is intrinsically discrete in space, because of the tick size, and
in time, because orders have a certain priority and changing position too often
reduces the actual chance to be reached by a market order. Hence, the model
has to be reinterpreted in a discrete way. In terms of prices, quotes must not
be between two ticks and we decided to round the optimal quotes to the near-
est tick. In terms of time, an order of size ATS10 is sent to the market and is
not canceled nor modified for a given period of time ∆t, unless a trade occurs
and, though perhaps partially, fills the order. Now, when a trade occurs and
changes the inventory or when an order stayed in the order book for longer
than ∆t, then the optimal quote is updated and, if necessary, a new order is
inserted.
Concerning the parameters, σ, Aand kcan be calibrated on trade-by-trade
limit order book data while γ has to be chosen. However, it is well known by
practitioners that A and k have to depend at least on the actual market bid-
ask spread. Since we do not explicitly take into account the underlying market,
there is no market bid-ask spread in the model. For the backtest example we
present below, A and k have been chosen independent of the spread but, in
practice, the value of A and k are function of the market bid-ask spread. As
far as γ is concerned, we decided in our backtests to assign γ an arbitrary
value for which the inventory stayed between -10 and 10 during the day we
considered (the unit being the ATS).
Turning to the backtests, they were carried out with trade-by-trade data
and we assumed that our orders were entirely filled when a trade occurred at
or above the ask price quoted by the agent. Our goal here is just to exemplify
the use of the model11 and we considered the case of the French stock France
Telecom on March 15th 2012.
10 ATS is the average trade size.
11 We, voluntarily, do not give full details about the algorithm based on the model.
Dealing with the Inventory Risk 21
We first plot the price of the stock France Telecom on March 15th 2012
on Figure 9, the evolution of the inventory12 on Figure 10 and the associated
P&L (the stocks in the portfolio are evaluated at mid-price) on Figure 11.
Price
11.29
11.28
11.27
11.26
11.25
11.24
11.23
11.22
11.21
11.2
10:00 11:00 12:00 13:00 14:00 15:00 16:00
Time
Fig. 9 Price of the stock France Telecom on 15/03/2012, from 10:00 to 16:00.
8
6
4
2
Inventory
0
−2
−4
−6
−8
10:00 11:00 12:00 13:00 14:00 15:00 16:00
Time
Fig. 10 Inventory (in ATS) when the strategy is used on France Telecom (15/03/2012)
from 10:00 to 16:00.
12 The ATS is 1105 for the day we considered.
22 Olivier Gu´eant et al.
1400
1200
1000
PnL [in EUR]
800
600
400
200
0
10:00 11:00 12:00 13:00 14:00 15:00 16:00
Time
Fig. 11 P&L when the strategy is used on France Telecom (15/03/2012) from 10:00 to
16:00.
This P&L can be compared to the P&L of a naive trader (Figure 12) who
only posts orders at the first limit of the book on each side, whenever he is
asked to post orders – that is when one of his orders has been executed or
after a period of time ∆t with no execution.
800
600
400
PnL [in EUR]
200
0
−200
−400
−600
10:00 11:00 12:00 13:00 14:00 15:00 16:00
Time
Fig. 12 P&L of a naive market maker on France Telecom (15/03/2012) from 10:00 to 16:00.
Now, to better understand the details of the strategy, we focused on a
subperiod of 1 hour and we plotted the state of the market along with the
Dealing with the Inventory Risk 23
quotes of the market maker (Figure 13). Trades occurrences involving the
market maker are signalled by a dot.
11.24
11.23
Price
11.22
11.21
11.2
12:00 12:10 12:20 12:30 12:40 12:50 13:00
Time
Fig. 13 Details for the quotes and trades when the strategy is used on France Telecom
(15/03/2012). Thin lines represent the market while bold lines represent the quotes of the
market maker. Dotted lines are associated to the bid side while plain lines are associated to
the ask side. Black points represent trades in which the market maker is involved.
Conclusion
In this paper we present a model for the optimal quotes of a market maker.
Starting from a model in line with Avellaneda and Stoikov [3] and rooted to
Ho and Stoll [17], we introduce a change of variables that allows to trans-
form the HJB equation into a system of linear ordinary diﬀerential equations.
This transformation allows to find the optimal quotes and to characterize
their asymptotic behavior. Closed-form approximations are also obtained us-
ing spectral analysis.
The change of variables introduced in this paper can also be used to solve
the initial equations of Avellaneda and Stoikov [3] and we provide a complete
mathematical proof in [13]. However, in the absence of inventory limits, no
proof of optimality is available for the quotes claimed to be optimal in [3] and
their admissibility appears to be an open problem.
An important topic for future research consists in generalizing the model to
any intensity function. This is particularly important because the exponential
form of the intensity is only suited to liquid stocks with a small bid-ask spread.
Another important topic consists in introducing “passive market impact” (i.e.
24 Olivier Gu´eant et al.
the perturbations of the price formation process by liquidity provision). This
is a real modeling challenge since no quantitative model for this type of impact
has been proposed in the literature.
Acknowledgements The authors wish to acknowledge the helpful conversations with Yves
Achdou (Universit´e Paris-Diderot), Vincent Fardeau (London School of Economics), Thierry
Foucault (HEC), Jean-Michel Lasry (Universit´e Paris-Dauphine), Antoine Lemenant (Uni-
versit´e Paris-Diderot), Pierre-Louis Lions (Coll`ege de France), Albert Menkveld (VU Uni-
versity Amsterdam), Vincent Millot (Universit´e Paris-Diderot) and Nizar Touzi (Ecole Poly-
technique). The authors also would like to thank two anonymous referees for their sugges-
tions.
References
1. Amihud, Y., Mendelson, H.: Dealership Market. Market-Making with Inventory. Journal
of Financial Economics 8, 31–53 (1980)
2. Amihud, Y., Mendelson, H.: Asset pricing and the bid-ask spread. Journal of Financial
Economics 17(2), 223–249 (1986)
3. Avellaneda, M., Stoikov, S.: High-frequency trading in a limit order book. Quantitative
Finance 8(3), 217–224 (2008).
4. Bayraktar, E., Ludkovski, M.: Liquidation in limit order books with controlled intensity.
Arxiv preprint arXiv:1105.0247 (2011)
5. Benston Robert, L., George, J.: Determinants of bid-asked spreads in the over-the-counter
market. Journal of Financial Economics 1(4), 353–364 (1974)
´
6.
A. Cartea and S. Jaimungal. Modeling asset prices for algorithmic and high frequency
trading. 2010.
´
7.
A. Cartea and S. Jaimungal. Risk measures and fine tuning of high frequency trading
strategies. 2012.
´
8. Cartea,
A., Jaimungal, S., Ricci, J.: Buy low sell high: A high frequency trading perspec-
tive (2011)
9. Cohen, K.J., Maier, S.F., Schwartz, R.A., Whitcomb, D.K.: Market makers and the mar-
ket spread: A review of recent literature. Journal of Financial and Quantitative Analysis
14(04), 813–835 (1979)
10. Cohen, K.J., Maier, S.F., Schwartz, R.A., Whitcomb, D.K.: Transaction Costs, Order
Placement Strategy, and Existence of the Bid-Ask Spread. The Journal of Political Econ-
omy 89(2), 287–305 (1981).
11. Garman, M.B.: Market microstructure. Journal of Financial Economics 3(3), 257–275
(1976)
12. Gu´eant, O., Lehalle, C.A., Fernandez-Tapia, J.: Optimal Execution with Limit Orders.
Working paper (2011)
13. Gu´eant, O., Lehalle, C.A.: Existence and Uniqueness for the Avellaneda-Stoikov PDE.
Working paper (2012)
14. Guilbaud, F., Pham, H.: Optimal high frequency trading with limit and market orders
(2011)
15. F. Guilbaud and H. Pham. Optimal high frequency trading in a pro-rata microstructure
with predictive information. Arxiv preprint arXiv:1205.3051, 2012.
16. Hendershott, T., Menkveld, A.: Price pressures. Manuscript, VU University Amsterdam
(2009)
17. Ho, T., Stoll, H.R.: Optimal dealer pricing under transactions and return uncertainty.
Journal of Financial Economics 9(1), 47–73 (1981).
18. Ho, T.S.Y., Macris, R.G.: Dealer bid-ask quotes and transaction prices: An empirical
study of some AMEX options. Journal of Finance pp. 23–45 (1984)
19. Ho, T.S.Y., Stoll, H.R.: The dynamics of dealer markets under competition. Journal of
Finance 38(4), 1053–1074 (1983)
Dealing with the Inventory Risk 25
20. Lehalle, C.A., Gu´eant, O., Razafinimanana, J.: High Frequency Simulations of an Order
Book: a Two-Scales Approach. In: F. Abergel, B.K. Chakrabarti, A. Chakraborti, M. Mitra
(eds.) Econophysics of Order-Driven Markets, New Economic Windows. Springer (2010)
21. Madhavan, A., Smidt, S.: An analysis of changes in specialist inventories and quotations.
The Journal of Finance 48(5), 1595–1628 (1993)
22. Menkveld, A.J.: High Frequency Trading and The New-Market Makers. Social Science
Research Network Working Paper Series (2010).
23. Mildenstein, E., Schleef, H.: The optimal pricing policy of a monopolistic marketmaker
in the equity market. Journal of Finance pp. 218–231 (1983)
24. O’Hara, M., Oldfield, G.S.: The microeconomics of market making. Journal of Financial
and Quantitative Analysis 21(04), 361–376 (1986)
25. Roll, R.: A simple implicit measure of the eﬀective bid-ask spread in an eﬃcient market.
Journal of Finance 39(4), 1127–1139 (1984)
Appendix: Proofs of the results
Proof of Proposition 1, Proposition 2 and Theorem 1:
Let us consider a family (vq )|q|≤Q of positive functions solution of the
system of ODEs introduced in Proposition 1 and let us define u(t,x,q,s) =
− exp (−γ(x+ qs)) vq (t)−
γ
k
.
Then:
1
∂tu+
σ2∂2
ssu=−
2
γ
k
˙
vq (t)
vq (t) u+ γ2σ2
2 q2u
Now, concerning the hamiltonian parts, we have for the bid part (q̸= Q):
sup
δb
λb(δb) u(t,x− s+ δb,q+ 1,s)− u(t,x,q,s)
= sup
Ae−kδb
δb
u(t,x,q,s) exp(−γδb) vq+1(t)
γ
vq (t)
−
k
− 1
The first order condition of this problem corresponds to a maximum (be-
cause u is negative) and writes:
γ
(k+ γ) exp(−γδb∗) vq+1(t)
vq (t)
−
k
= k
Hence:
δb∗
=
1
kln vq (t)
vq+1(t) +
1
γ
ln 1 + γ
k
and
sup
δb
λb(δb) u(t,x− s+ δb,q+ 1,s)− u(t,x,q,s)
=−
γ
Aexp(−kδb∗)u(t,x,q,s)k+ γ
26 Olivier Gu´eant et al.
γA
k
=−
k+ γ
1 + γ
k
−
γ vq+1(t)
vq (t) u(t,x,q,s)
Similarly, the maximizer for the ask part (for q̸=−Q) is:
δa∗
=
1
kln vq (t)
vq−1(t) +
1
γ
ln 1 + γ
k
and
=−
sup
δa
λa(δa) [u(t,x+ s+ δa,q− 1,s)− u(t,x,q,s)]
γ
=−
Aexp(−kδa∗)u(t,x,q,s)
k+ γ
γA
k
=−
k+ γ
1 + γ
k
−
γ vq−1(t)
vq (t) u(t,x,q,s)
Hence, putting the terms altogether we get for |q| <Q:
∂tu(t,x,q,s) + 1
σ2∂2
ssu(t,x,q,s)
2
+ sup
δb
λb(δb) u(t,x− s+ δb,q+ 1,s)− u(t,x,q,s)
+ sup
λa(δa) [u(t,x+ s+ δa,q− 1,s)− u(t,x,q,s)]
δa
˙
=−
γ
k
vq (t)
vq (t) u+ γ2σ2
2 q2u−
γA
k+ γ
1 + γ
k
γ
k
u
vq (t)
˙
kγσ2
vq (t)−
2 q2vq (t) + A 1 + γ
k
k
γ vq+1(t)
vq−1(t)
vq (t) +
vq (t) u
−(1+k
γ ) (vq+1(t) + vq−1(t)) = 0
For q=−Q we have:
∂tu(t,x,q,s) + 1
σ2∂2
ssu(t,x,q,s)
2
+ sup
δb
λb(δb) u(t,x− s+ δb,q+ 1,s)− u(t,x,q,s)
=−
γ
k
γ
=−
k
u
vq (t)
˙
vq (t)−
Similarly, for q= Q we have:
˙
vq (t)
vq (t) u+ γ2σ2
2 q2u−
γA
k+ γ
1 + γ
k
kγσ2
2 q2vq (t) + A 1 + γ
k
k
γ vq+1(t)
vq (t) u
−(1+k
γ )
vq+1(t) = 0
∂tu(t,x,q,s) + 1
σ2∂2
ssu(t,x,q,s)
2
+ sup
δa
λa(δa) [u(t,x− s+ δa,q+ 1,s)− u(t,x,q,s)]
Dealing with the Inventory Risk 27
˙
γ
vq (t)
=−
k
vq (t) u+ γ2σ2
γA
k
2 q2u−
k+ γ
1 + γ
k
γ vq−1(t)
vq (t) u
γ
u
=−
k
vq (t)
˙
kγσ2
vq (t)−
2 q2vq (t) + A 1 + γ
k
−(1+k
γ )
vq−1(t) = 0
Now, noticing that the terminal condition for vq is consistent with the ter-
minal condition for u, we get that uverifies (HJB) and this proves Proposition
1.
The positivity of the functions (vq )|q|≤Q was essential in the definition of
u. Hence we need to prove that the solution to the above linear system of ordi-
nary diﬀerential equations, namely v(t) = exp(−M(T− t)) × (1,...,1)′ (where
M is given in Proposition 2), defines a family (vq )|q|≤Q of positive functions.
In fact, we are going to prove that:
∀t∈ [0,T],∀q∈ {−Q,...,Q}, vq (t) ≥ e−(αQ2
−η)(T−t)
If this was not true then there would exist ǫ>0 such that:
min
t∈[0,T ],|q|≤Q
e−2η(T−t) vq (t)− e−(αQ2
−η)(T−t) + ǫ(T− t) <0
But this minimum is achieved at some point (t∗,q∗) with t∗ <T and hence:
d
dt e−2η(T−t) vq∗ (t)− e−(αQ2
−η)(T−t)
t=t∗
≥ ǫ
This gives:
2ηe−2η(T−t∗) vq∗ (t∗)− e−(αQ2
−η)(T−t∗ )
+e−2η(T−t∗) v′
q∗ (t∗)− (αQ2
− η)e−(αQ2
−η)(T−t∗ ) ≥ ǫ
Hence:
2ηvq∗ (t∗) + v′
q∗ (t∗)− (η+ αQ2)e−(αQ2
−η)(T−t∗ ) ≥ ǫe2η(T−t∗)
Now, if |q∗| <Q, this gives:
αq∗2
vq∗ (t∗)− η(vq∗ +1(t∗)− 2vq∗ (t∗) + vq∗
−1(t∗))
−(η+ αQ2)e−(αQ2
−η)(T−t∗ ) ≥ ǫe2η(T−t∗ )
Thus:
αq∗2
vq∗ (t∗)− e−(αQ2
−η)(T−t∗ ) − η(vq∗ +1(t∗)− 2vq∗ (t∗) + vq∗
−1(t∗))
−(η+ α(Q2
− q∗2))e−(αQ2
−η)(T−t∗ ) ≥ ǫe2η(T−t∗ )
28 Olivier Gu´eant et al.
All the terms on the left hand side are nonpositive by definition of (t∗,q∗)
and this gives a contradiction.
If q∗
= Q, we have:
(αQ2 + η)vQ (t∗)− η(vQ−1(t∗)− vQ(t∗))
−(η+ αQ2)e−(αQ2
−η)(T−t∗ ) ≥ ǫe2η(T−t∗ )
Thus:
−η(vQ−1(t∗)− vQ(t∗)) + (η+ αQ2) vQ(t∗)− e−(αQ2
−η)(T−t∗ ) ≥ ǫe2η(T−t∗ )
All the terms on the left hand side are nonpositive by definition of (t∗,q∗) =
(t∗,Q) and this gives a contradiction.
Similarly, if q∗
=−Q, we have:
(αQ2 + η)v−Q(t∗)− η(v−Q+1(t∗)− vQ(t∗))
−(η+ αQ2)e−(αQ2
−η)(T−t∗ ) ≥ ǫe2η(T−t∗ )
−η(v−Q+1(t∗)−v−Q(t∗))+(η+αQ2) v−Q(t∗)− e−(αQ2
−η)(T−t∗ ) ≥ ǫe2η(T−t∗)
All the terms on the left hand side are nonpositive by definition of (t∗,q∗) =
(t∗
,−Q) and this gives a contradiction.
As a consequence, vq (t) ≥ e−(αQ2
−η)(T−t) >0 and this completes the proof
of Proposition 2.
Combining the above results, we see that u, as defined in Theorem 1, is a
solution of (HJB). Then, we are going to use a verification argument to prove
that uis the value function of the optimal control problem under consideration
and prove subsequently that the optimal controls are as given in Theorem 1.
Let us consider processes (νb) and (νa) ∈ A. Let t ∈ [0,T) and let us
consider the following processes for τ ∈ [t,T]:
dSt,s
τ
= σdWτ , St,s
t = s
dXt,x,ν
τ = (Sτ + νa
τ )dNa
τ− (Sτ− νb
τ )dNb
τ , Xt,x,ν
t = x
dqt,q,ν
= dNb
τ
τ− dNa
τ , qt,q,ν
t = q
where the point process Nb has intensity (λb
τ )τ with λb
τ
where the point process Na has intensity (λa
τ )τ with λa
τ
= Ae−kνb
τ 1qτ− <Q and
= Ae−kνa
τ 1qτ− >−Q 13
.
13 These intensities are bounded since νb and νa are bounded from below.
Dealing with the Inventory Risk 29
Now, since u is smooth, let us write Itˆo’s formula for u, between t and tn
where tn = T ∧ inf{τ > t,|Sτ− s| ≥ nor |Na
τ− Na
t | ≥ nor |Nb
τ− Nb
t | ≥ n}
(n∈ N):
u(tn,Xt,x,ν
tn− ,qt,q,ν
tn− ,St,s
tn ) = u(t,x,q,s)
+
tn
t
∂τ u(τ,Xt,x,ν
τ− ,qt,q,ν
τ− ,St,s
τ ) + σ2
2 ∂2
ssu(τ,Xt,x,ν
τ− ,qt,q,ν
τ− ,St,s
τ ) dτ
+
tn
t
u(τ,Xt,x,ν
τ− + St,s
τ + νa
τ ,qt,q,ν
τ−
− 1,St,s
τ )− u(τ,Xt,x,ν
τ− ,qt,q,ν
τ− ,St,s
τ ) λa
τ dτ
+
tn
t
u(τ,Xt,x,ν
τ−
− St,s
τ + νb
τ ,qt,q,ν
τ− + 1,St,s
τ )− u(τ,Xt,x,ν
τ− ,qt,q,ν
τ− ,St,s
τ ) λb
τ dτ
+
t
tn
σ∂su(τ,Xt,x,ν
τ− ,qt,q,ν
τ− ,St,s
τ )dWτ
+
tn
t
u(τ,Xt,x,ν
τ− + St,s
τ + νa
τ ,qt,q,ν
τ−
− 1,St,s
τ )− u(τ,Xt,x,ν
τ− ,qt,q,ν
τ− ,St,s
τ ) dMa
τ
+
tn
t
u(τ,Xt,x,ν
τ−
− St,s
τ + νb
τ ,qt,q,ν
τ− + 1,St,s
τ )− u(τ,Xt,x,ν
τ− ,qt,q,ν
τ− ,St,s
τ ) dMb
τ
where Mb and Ma are the compensated processes associated respectively to
Nb and Na for the intensity processes (λb
τ )τ and (λa
τ )τ.
Now, because each vq is continuous and positive on a compact set, it has a
positive lower bound and vqτ (τ)−
γ
k is bounded along the trajectory, indepen-
dently of the trajectory. Also, because νb and νa are bounded from below, and
because of the definition of tn, all the terms in the above stochastic integrals
are bounded and, local martingales being in fact martingales, we have:
E u(tn,Xt,x,ν
tn− ,qt,q,ν
tn− ,St,s
tn ) = u(t,x,q,s)
+E
tn
t
∂τ u(τ,Xt,x,ν
τ− ,qt,q,ν
τ− ,St,s
τ ) + σ2
2 ∂2
ssu(τ,Xt,x,ν
τ− ,qt,q,ν
τ− ,St,s
τ ) dτ
+
tn
t
u(τ,Xt,x,ν
τ− + St,s
τ + νa
τ ,qt,q,ν
τ−
− 1,St,s
τ )− u(τ,Xt,x,ν
τ− ,qt,q,ν
τ− ,St,s
τ ) λa
τ dτ
+
tn
t
u(τ,Xt,x,ν
τ−
− St,s
τ + νb
τ ,qt,q,ν
τ− + 1,St,s
τ )− u(τ,Xt,x,ν
τ− ,qt,q,ν
τ− ,St,s
τ ) λb
τ dτ
Using the fact that u solves (HJB), we then have that
E u(tn,Xt,x,ν
tn− ,qt,q,ν
tn− ,St,s
tn ) ≤ u(t,x,q,s)
with equality when the controls are taken equal the maximizers of the hamil-
tonians (these controls being in A because v is bounded and has a positive
30 Olivier Gu´eant et al.
lower bounded).
Now, if we prove that
lim
E u(tn,Xt,x,ν
tn− ,qt,q,ν
tn− ,St,s
tn ) = E u(T,Xt,x,ν
T ,qt,q,ν
T ,St,s
T )
n→∞
we will have that for all controls in A:
E− exp−γ(Xt,x,ν
T + qt,q,ν
T St,s
T ) = E u(T,Xt,x,ν
T ,qt,q,ν
T ,St,s
T ) ≤ u(t,x,q,s)
with equality for νb
t = δb∗(t,qt−) and νa
t = δa∗(t,qt−). Hence:
sup
(νa
t )t ,(νb
t )t ∈A
and this will give the result.
E− exp−γ(Xt,x,ν
T + qt,q,ν
T St,s
T ) = u(t,x,q,s)
= E− exp−γ(Xt,x,δ∗
T + qt,q,δ∗
T St,s
T )
It remains to prove that
lim
E u(tn,Xt,x,ν
tn− ,qt,q,ν
tn− ,St,s
tn ) = E u(T,Xt,x,ν
T ,qt,q,ν
T ,St,s
T )
n→∞
First, we have, almost surely, that u(tn,Xt,x,ν
tn− ,qt,q,ν
tn− ,St,s
tn ) tends towards
u(T,Xt,x,ν
T− ,qt,q,ν
T− ,St,s
T ). Then, in order to prove that the sequence is uniformly
integrable we will bound it in L2. However, because of the uniform lower bound
on v already used early, it is suﬃcient to bound exp(−γ(Xt,x,ν
tn− + qt,q,ν
St,s
tn−
tn ))
in L2
.
But,
Xt,x,ν
tn− + qt,q,ν
St,s
tn−
tn
=
t
tn
νa
τ dNa
τ +
tn
νb
τ dNb
t
τ + σ
tn
t
≥ −∥νa
−∥∞Na
T − ∥νb
−∥∞Nb
T + σ
tn
t
qt,q,ν
τ dWτ
qt,q,ν
τ dWτ
Hence
E exp(−2γ(Xt,x,ν
tn− + qt,q,ν
St,s
tn−
tn ))
≤ E exp 2γ∥νa
−∥∞Na
T exp 2γ∥νa
−∥∞Nb
T exp−2γσ
tn
t
1
1
≤ E exp 6γ∥νa
−∥∞Na
T
3 E exp 6γ∥νb
−∥∞Nb
T
3
×E exp−6γσ
tn
1
3
qt,q,ν
t
τ dWτ
qt,q,ν
τ dWτ
Dealing with the Inventory Risk 31
Now, since the intensity of each point process is bounded, the point pro-
cesses have a Laplace transform and the first two terms of the product are
finite (and independent of n). Concerning the third term, because |qt,q,ν
τ | is
bounded by Q, we know (for instance applying Girsanov’s theorem) that:
E exp−6γσ
tn
t
1
qt,q,ν
τ dWτ
3
≤ E exp 3γ2σ2(tn− t)Q2
1
3
≤ exp γ2σ2Q2T
Hence, the sequence is bounded in L2, then uniformly integrable and we
have:
lim
E u(tn,Xt,x,ν
tn− ,qt,q,ν
tn− ,St,s
tn ) = E u(T,Xt,x,ν
T− ,qt,q,ν
T− ,St,s
T )
n→∞
= E u(T,Xt,x,ν
T ,qt,q,ν
T ,St,s
T )
We have proved that u is the value function and that δb∗ and δa∗ are
optimal controls.
⊓⊔
Proof of Theorem 2:
Let us first consider the matrix M+2ηI. This matrix is a symmetric matrix
and it is therefore diagonalizable. Its smallest eigenvalue λis characterized by:
x′(M + 2ηI)x
λ= inf
x∈ 2Q+1\{0}
x′x
and the associated eigenvectors x̸= 0 are characterized by:
λ=
x′(M + 2ηI)x
x′x
It is straightforward to see that:
x′(M + 2ηI)x=
Q
q=−Q
αq2xq
2 + η
Q−1
q=−Q
(xq+1− xq )2 + ηxQ
2 + ηx−Q
2
Hence, if x is an eigenvector of M + 2ηI associated to λ:
λ≤ |x|′(M + 2ηI)|x|
|x|′|x|
=
1
|x|′|x|
 Q
q=−Q
αq2|xq |2 + η
Q−1
q=−Q
(|xq+1| − |xq |)2 + η|xQ|2 + η|x−Q|2 
32 Olivier Gu´eant et al.
≤
1
|x|′|x|
 Q
αq2|xq |2 + η
Q−1
q=−Q
q=−Q
(xq+1− xq )2 + η|xQ|2 + η|x−Q|2 = λ
This proves that |x| is also an eigenvector and that necessarily xq+1 and
xq are of the same sign (i.e. xq xq+1 ≥ 0).
Now, let x≥ 0 be an eigenvector of M + 2ηI associated to λ.
If for some q with |q| <Q we have xq = 0 then:
0 = λxq = αq2xq− η(xq+1− 2xq + xq−1) =−η(xq+1 + xq−1) ≤ 0
Hence, because x ≥ 0, both xq+1 and xq−1 are equal to 0. By immediate
induction x= 0 and this is a contradiction.
Now, if xQ = 0, then 0 = λxQ= αQ2xQ− η(−2xQ + xQ−1) =−ηxQ−1 ≤ 0
and hence xQ−1 = 0. Then, by the preceding reasoning we obtain a contradic-
tion.
Similarly if x−Q = 0, then 0 = λx−Q= αQ2x−Q− η(x−Q+1− 2x−Q) =
−ηx−Q+1 ≤ 0 and hence x−Q+1 = 0. Then, as above, we obtain a contradic-
tion.
This proves that any eigenvector x≥ 0 of M+ 2ηI associated to λverifies
in fact x>0.
Now, if the eigenvalue λwas not simple, there would exist two eigenvectors
x and y of M + 2ηI associated to λ such that |x|′y = 0. Hence, y must have
positive coordinates and negative coordinates and since yq yq+1 ≥ 0, we know
that there must exist q such that yq = 0. However, this contradicts our pre-
ceding point since |y| ≥ 0 should also be an eigenvector of M+ 2ηI associated
to λ and it cannot have therefore coordinates equal to 0.
As a conclusion, the eigenspace of M + 2ηI associated to λ is spanned by
a vector f0 >0 and we scaled its R2Q+1-norm to 1.
Now, because M is a symmetric matrix, we can write v(0) = exp(−MT) ×
(1,...,1)′ as:
vq (0) =
2Q
exp(−λiT)⟨gi
,(1,...,1)′⟩gi
q , ∀q∈ {−Q,...,Q}
i=0
where λ0 ≤ λ1 ≤... ≤ λ2Q are the eigenvalues of M (in increasing order
and repeated if necessary) and (gi)i an associated orthonormal basis of eigen-
vectors. Clearly, we can take g0 = f0. Then, both f0
q and ⟨f0
,(1,...,1)′⟩ are
positive and hence diﬀerent from zero. As a consequence:
Dealing with the Inventory Risk 33
vq (0)∼T →+∞ exp(−λ0T)⟨f0
,(1,...,1)′⟩f0
q , ∀q∈ {−Q,...,Q}
Then, using the expressions for the optimal quotes, we get:
lim
T →+∞
δb∗(0,q) = 1
γ
ln 1 + γ
k +
1
q
kln f0
f0
q+1
lim
T →+∞
δa∗(0,q) = 1
γ
ln 1 + γ
k +
1
q
kln f0
f0
q−1
Turning to the characterization of f0 stated in Theorem 2, we just need to
write the Rayleigh ratio associated to the smallest eigenvalue of M + 2ηI:
f0 ∈ argmin
f′(M + 2ηI)f
f ∈ 2Q+1
,∥f ∥2=1
Equivalently:
f0 ∈ argmin
f ∈ 2Q+1
,∥f ∥2=1
Q
q=−Q
αq2fq
2 + η
Q−1
q=−Q
(fq+1− fq )2 + ηfQ
2 + ηf−Q
2
⊓⊔
Proof of Proposition 3:
Let us first introduce H= {u ∈ L1
loc(R)/x → xu(x) ∈ L2(R) and u′ ∈
L2(R)}.
space.
H equipped with the norm ∥u∥H = (αx2u(x)2 + ηu′(x)2) dxis an Hilbert
Step 1: H ⊂ L2(R) with continuous injection.
Let us consider u∈ H and ǫ>0.
We have:
u(x)2dx≤
\[−ǫ,ǫ]
1
ǫ2 \[−ǫ,ǫ]
x2u(x)2dx<+∞
Hence because u′ ∈ L2(R), we have u ∈ H1(R \ [−ǫ,ǫ]) with a constant Cǫ
independent of u such that ∥u∥H1( \[−ǫ,ǫ]) ≤ Cǫ∥u∥H . In particular u is con-
tinuous on R∗
.
Now, if ǫ = 1, ∀x ∈ (0,1),u(x) = u(1)−
1
x
|u(1)| + √1− x∥u′∥L2((0,1)).
u′(t)dt and then |u(x)| ≤
34 Olivier Gu´eant et al.
Because the injection of H1((1,+∞)) in C([1,+∞)) is continuous, we
know that there exists a constant C independent of u such that |u(1)| ≤
C∥u∥H1((1,+∞)). Hence, there exists a constant C′ such that |u(1)| ≤ C′∥u∥H
and eventually a constant C′′ such that ∥u∥L∞((0,1)) ≤ C′′∥u∥H . Similarly, we
obtain ∥u∥L∞((−1,0)) ≤ C′′∥u∥H.
Combining the above inequalities we obtain a new constant K so that
∥u∥L2( ) ≤ K∥u∥H.
⊓⊔
A consequence of this first step is that H ⊂ H1(R) ⊂ C(R).
Step 2: The injection H ֒→ L2(R) is compact.
Let us consider a sequence (un)n of functions in Hwith supn ∥un∥H <+∞.
Because H ⊂ H1(R), ∀m ∈ N∗, we can extract from (un)n a sequence
that converges in L2((−m,m)). Using then a diagonal extraction, there exists
a subsequence of (un)n, still denoted (un)n, and a function u∈ L2
loc(R) such
that un(x) → u(x) for almost every x∈ R and un → u in the L2
loc(R) sense.
Now, by Fatou’s lemma:
x2u(x)2dx≤ lim inf
n→∞
x2un(x)2dx≤ supn ∥un∥2
H
α
Hence, there exists a constant C such that ∀m∈ N∗:
|u(x)−un(x)|2dx≤
m
1
|u(x)−un(x)|2dx+
−m
m2 \[−m,m]
x2|u(x)−un(x)|2dx
≤
m
−m
|u(x)− un(x)|2dx+
C
m2
Hence lim supn→∞ |u(x)− un(x)|2dx≤ C
m2.
Sending m to +∞ we get:
lim sup
n→∞
|u(x)− un(x)|2dx= 0
Hence (un)n converges towards u in the L2(R) sense.
⊓⊔
Now, we consider the equation−ηu′′(x) + αx2u(x) = f(x) for f ∈ L2(R)
and we define u= Lf the weak solution of this equation, i.e.:
∀v∈ H, αx2u(x)v(x) + ηu′(x)v′(x) dx= f(x)v(x)dx
Dealing with the Inventory Risk 35
Step 3: L : L2(R) → L2(R) is a well defined linear operator, compact,
positive and self-adjoint.
For f ∈ L2(R), v ∈ H → f(x)v(x)dx is a continuous linear form on H
because the injection H ֒→ L2(R) is continuous. Hence, by Lax-Milgram or
Riesz’s representation theorem, there exists a unique u∈ H weak solution of
the above equation and L is a well defined linear operator.
Now, ∥Lf∥2
H = ⟨f,Lf⟩ ≤ ∥f∥L2( )∥Lf∥L2( ). Hence, since the injection
H ֒→ L2(R) is continuous, there exists a constant C such that ∥Lf∥2
H ≤
C∥f∥L2( )∥Lf∥H , which in turn gives ∥Lf∥H ≤ C∥f∥L2( ). Since the injec-
tion H ֒→ L2(R) is compact, we obtain that L is a compact operator.
L is a positive operator because ⟨f,Lf⟩= ∥Lf∥2
H ≥ 0.
Eventually, L is self-adjoint because ∀f,g∈ L2(R):
⟨f,Lg⟩= αx2Lf(x)Lg(x) + η(Lf)′(x)(Lg)′(x) dx
= αx2Lg(x)Lf(x) + η(Lg)′(x)(Lf)′(x) dx= ⟨g,Lf⟩
⊓⊔
Now, using the spectral decomposition of Land classical results on Rayleigh
ratios we know that the eigenfunctions f corresponding to the largest eigen-
value λ0 of L satisfy:
1
λ0
=
∥f∥H
∥f∥L2( )
= inf
g∈H\{0}
∥g∥H
∥g∥L2( )
Hence, our problem boils down to proving that the largest eigenvalue of L
is simple and that g: x→ exp−
1
2
α
η
x2 is an eigenfunction corresponding
to this eigenvalue (it is straightforward that g∈ H).
Step 4: Any positive eigenfunction corresponds to the largest eigenvalue of
L.
By definition of ∥ · ∥H , ∀f ∈ H, ∥|f |∥H
= ∥f ∥H
. Hence, if f is an
∥|f |∥L2( )
∥f ∥L2( )
eigenfunction of L corresponding to the eigenvalue λ0, then |f| is also an
˜
eigenfunction of L corresponding to the eigenvalue λ0. Now, if
f is an eigen-
˜
˜
function of Lcorresponding to an eigenvalue λ̸= λ0
, ⟨|f|,
f⟩ = 0. Therefore
f
cannot be positive.
⊓⊔
Step 5: gspans the eigenspace corresponding to the largest eigenvalue of L.
36 Olivier Gu´eant et al.
Diﬀerentiating g twice, we get g′′(x) =−
α
η g(x) +α
x2g(x).
η
Hence−ηg′′(x) + αx2g(x) = √αηg(x) and g is a positive eigenfunction, nec-
essarily associated to the eigenvalue λ0 that is therefore equal to 1
√αη.
Now, if we look for an eigenfunction f ∈ C∞(R) ∩ H – because any eigen-
function of L is in C∞(R) – we can look for f of the form f= gh. This
gives:
0 =−ηf′′(x) + αx2f(x)− √αηf(x)
=−η(g′′(x)h(x) + 2g′(x)h′(x) + g(x)h′′(x)) + αx2g(x)h(x)− √αηg(x)h(x)
Hence:
0 = 2g′(x)h′(x) + g(x)h′′(x) =−2x
α
g(x)h′(x) + g(x)h′′(x)
η
⇒ h′′(x) = 2x
α
h′(x)
η
⇒ ∃K1, h′(x) = K1 exp
α
η
x2
⇒ ∃K1,K2, h(x) = K1
x
0
⇒ ∃K1,K2, f(x) = K1g(x)
x
0
exp
α
η
exp
t2 dt+ K2
α
η
t2 dt+ K2g(x)
Now,
g(x)
0
x
exp
α
η
t2 dt≥ exp−
≥ x 1−
1
2
α
η
x2
x
x
√2
exp
α
η
t2 dt
1
√2
Hence, for f to be in H, we must have K1 = 0. Thus, gspans the eigenspace
corresponding to the largest eigenvalue of L and Proposition 3 is proved.
⊓⊔