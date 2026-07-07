# Chapter 8: Valuation in Theory

- **book_name**: Active Portfolio Management
- **main_source**: pdf
- **cross_check_source**: none
- **pdf_role**: main_text_source
- **split_scope**: pages 221-246

---

CHAPTER
8
Valuation in Theory
INTRODUCTION
Valuation is the central concept of active management. Active man-
agers must believe that their assessment of value is better than the
market or consensus assessment. In this chapter, we describe a
basic theory of valuation. The following chapters will illustrate
practical valuation procedures and any links that these might have
with theory.
This chapter contains three important messages:
= The modern theory of valuation connects stock values to
risk-adjusted expected cash flows.
= The theory is closely related to the theory of option
pricing, and is consistent with the CAPM and the APT.
® Valuation (and misvaluation) is connected to expected
returns.
THE MODERN THEORY OF VALUATION
The modern theory of asset valuation is general, esoteric, and worth
studying. The theory provides a framework for judging more ad
hoc and practical valuation methods.
We start with the important premise that a stock’s value is
derived from the cash flows an investor can obtain from owning
the stock. These cash flows arise as dividends or as the future value
199
200
Expected Returns and Valuation
of the stock realized by selling the stock.’ The key to the theory
will be discounting these uncertain cash flows back to the present.
This is the same task required for option pricing, and readers famil-
iar with option pricing theory will recognize the similarities (which
we will make more explicit in the technical appendix).
Certain Cash Flows
In the simplest case, the investor will obtain a certain cash flow
cf(t) at future time t. To make it even simpler, we assume a constant
risk-free interest rate that applies over all maturities. Let ip be the
(annual) return on a risk-free investment. When interest rates are
6 percent annually, then i; = 0.06. The present value of a promised
$1.00 in 1 year is 1/(1 + i). The promise of $1.00 in ft years is 1/
(1 + i;)' and the present value of cf(f) dollars in ¢ years is
acl)
(1 + ip)
Equation (8.1) is the basis for valuing fixed-income instruments
with certain cash flows. Given a stream of cash flows, e.g., cf(1) in
1 year, cf(2) in 2 years, etc., the valuation formula becomes
i
f
eo
(8.2)
(8.1)
(Pie)
For example, if we have a promise of 6 dollars in 1 year and 10
dollars in 3 years and i; = 0.06, we find
ean06 te C0Gy = 14.06
(8.3)
Uncertain Cash Flows
‘
Equation (8.1) fails when the cash flows are uncertain. Uncertainty
means that there is more than one possible value for the future
'If the stock is fairly valued, it doesn’t matter whether we consider a sale in five years or
six months. In practice, it may matter, since the key to using the valuation scheme
is to find some future time when the stock will be fairly valued, and work
backward toward a current fair value.
‘
Valuation in Theory
201
cash flows. We need a way to describe those possibilities. We do
this by listing the possible outcomes at time t and determining the
probability of each outcome. This is easier said than done in prac-
tice, but remember, this is the theory chapter. Let’s push on bravely
and ask what we would do next if we could define both the possible
future cash flows and the probability of each outcome.
We can index the possible outcomes at time ft by s (for states).
Let m(t,s) be the probability of outcome s at time t, and let cf(t,s)
be the uncertain cash flow at time t in state s. The probabilities are
nonnegative and sum to 1; i.e., > m(t,s) = 1 for every t.
As an example, consider a 1-month period, t = 1/12, and a
stock currently valued at 50. In 1 month its value (sale price
plus any dividend paid in the month) will be either cf(t,1) = 49 or
cf(t,2) = 53. The outcomes are equally likely; m(t,1) = m(t,2) = 0.5.
The risk-free interest over the year is 6 percent. The expected cash
flow is 51, and the standard deviation is 2.
Given this information, how should we value these uncertain
cash flows? The simplest and most tempting way is to generalize
Eq. (8.1), replacing certain cash flows with expected cash flows:
E{cf(t)} = S‘a(t,s) - cf(t,s)
(8.4)
Unfortunately, this doesn’t work. Expectations generally overesti-
mate the stock’s value. When the cash flows are uncertain, we
usually find
E{cf(t)} z 2m(t,s) ChE
eS)
ie
(ena?
(1 + i,)
In our example, the discounted expected cash flows lead to a value
of 50.75, but the current price is 50. The problem is that expected
cash flows do not take account of risk. An instrument with an
expected but uncertain cash flow of 51 should not have the same
price as an instrument with a certain cash flow of 51. The two have
the same expected cash flows, but one is certain and one is not.
We must dig deeper to find a valuation formula.
202
Expected Returns and Valuation
THE VALUATION FORMULA
Before we present a valuation formula, we can list the properties
that a reasonable formula should display. There are several.’
1. If all future cash flows are nonnegative, the value is
nonnegative.
2. If we double (or triple or halve) the cash flows, the value
should change in the same proportion.
3. If we add two sets of cash flows, the value of the total
cash flow should be the sum of the values of each
separately.
4. The valuation formula should reduce to Eq. (8.1) in the
case of certain cash flows.
5. The formula should agree with the market value of
securities.
Property 1 is certainly sensible; if we can’t lose and we might
gain, the opportunity should be worth something. Property 2 says
that the price of six shares is six times the price of one share.
Property 3 combined with property 2 says that our valuation rule
works for portfolios. We can value each stock in the portfolio and
know that the portfolio’s value is simply the weighted sum of the
values for each stock separately. Property 3 not only lets us combine
stocks into portfolios, but also allows us to value each cash flow
in a stream of cash flows separately. Thus we could value next
quarter’s dividend separately from the dividend the quarter follow-
ing. The cash flows for the 3-month and 6-month dividends may
be highly correlated, but that doesn’t matter; the valuation formula
should still get each right.
Property 3 also lets us see the flexibility of this valuation
notion. Suppose we have a stock that pays a quarterly dividend
and the next dividend occurs in 3 months. Rather than consider
an indefinite sequence of dividends, we can always consider the
stock as the promise of the next four dividends plus the price of
*We omit from this list the technical stipulation that if m(t,s*) = 0 for some state s* and
cf(t,s*) = 1, but cf(t,s) = 0 for s ¥ s*, the value of the cash flow must be zero. We
attach no value to promised cash flows for outcomes that can’tshappen, e.g., a put
option with an exercise price of —10.
Valuation in Theory
203
the stock in 1 year. The price in 1 year is the final cash flow that
we receive. The 1 year was arbitrary. We could have used the price
in 1 month, before the first dividend, or in 2 years, after eight
dividends. The valuation formula should give us the same answer
no matter how we represent the cash flows!
Property 4 says that we can value a certain cash flow of any
maturity. This is clearly a prerequisite to valuing uncertain cash
flows of any maturity. Equation (8.1) is based on a constant interest
rate. We can easily generalize it to allow for risk-free rates that
depend on maturity.
Property 5 says that the valuation formula works. This is where
the active manager and the economist part company. The active
manager is interested in using the concept to find stocks for which
the formula is not working. In practice, property 5 can be used to
say that the valuation is correct on average or within certain groups.
The active manager is free to look within those groups for under-
and overpriced stocks.
We know the properties that we want. How do we get them?
RISK-ADJUSTED EXPECTATIONS
There are two ways to modify the right side of Eq. (8.5) in order
to get a straightforward relationship like Eq. (8.1). One possibility
is to introduce a risk-adjusted interest rate. Then we could dis-
count the expected cash flows at the higher (one presumes) rate
of interest and therefore lower their value. This seems like a good
idea, and, as we’ll see in the next chapter, it is used in practice.
It is just a straightforward extension of the CAPM and the APT,
which state
AO =1+i+ 8° fo
(8.6)
where cf(t) is the stock value in 1 year, and so
____Elcf)}
P
T+
+B: fo
Here the risk-adjusted interest rate is based on the asset’s beta and
(8.7)
204
Expected Returns and Valuation
the expected excess return to portfolio Q. The term ip + B ° fg is
sometimes called the equity cost of capital.
While this risk-adjusted interest rate is simple and easy to
understand, this valuation approach can break down. In particular,
imagine a coin-toss security worth $100,000 (if heads) or —$100,000
(if tails). The expected cash flow is zero. Any attempt to value this
by adjusting the discount rate will still get zero.’
The modern theory of valuation employs the alternative modi-
fication of Eq. (8.5): risk-adjusted expectations E*{cf(t)}. As we will
see, this approach will go far beyond Eq. (8.7) in providing insight
into valuation and unifying concepts from the CAPM, the APT, and
options pricing. By introducing a unique risk-adjusted probability
distribution, we will be able to consistently discount all adjusted
expected cash flows at the same risk-free rate.
We obtain the risk adjustment by introducing value multiples’
vu(t,s), so the modified expectation can be written as
E*{cf(t)} = Efv(t) - cf(t)} = Dy) - u(t,s) > cf(t,s)
(8.8)
where v(t,s) is
# Positive
# With expected value 1
® A function of the return to portfolio Q and
proportional to the total return on a portfolio S, the
portfolio with minimum second moment of total return
(see appendix)
In the technical appendix, we will show that these valuation
multiples exist as long as there are no arbitrage opportunities in
the valuation scheme. Arbitrage can occur if we can start with a
nonpositive amount of money at t = 0 and have all outcomes
nonnegative with at least one outcome positive.
‘In Eq. (8.7), this situation leads to both the numerator and the denominator approaching
zero. See Problem 3 for more. details.
‘Technically, v(t,s) is a Radon-Nikodyn derivative, and 1*(t,s) = v(t,s) > m(t,s) is a
Martingale equivalent measure.
Valuation in Theory
205
With this definition of the risk-adjusted expectations, we ob-
tain our valuation formula:
Eich}
a
CF)
e
All modern valuation theories, including option theory, the CAPM,
and the APT, use valuation formulas that have the form of Eq.
(8.9). The technical appendix will discuss this in more detail.
Let’s check that Eq. (8.9) has the required valuation properties.
Since v(t) is positive, property 1 will hold: Nonnegative cash flows
will lead to nonnegative risk-adjusted expectations E*{cf(t)} and,
by Eq. (8.9), nonnegative values.
The valuation rule is linear, so properties 2 and 3 have to hold.
That means that Eq. (8.9) has the portfolio property. If stock n has
uncertain cash flows cf,(t), and the weight of stock n in portfolio
P is hp,, then the portfolio’s cash flow is cfp(t) = Dhp, « cf,(t), and
the value of portfolio P is
:
fp(t)}
p= py EGE Shee Pr
(8.10)
where
E* {cf At)}
= 2+ in
aw il
(8.11)
is the value of stock n valued in isolation.
If the cash flow cf(f) is certain, then
E*{cf,,(t)} = Efv(t) - cf(t)} = cf(t) - Efv(t)} = cf(t)
(8.12)
The first equality follows from the definition of E*, the second
equality because cf(t) is certain, and the third equality because v(t)
has expected value of 1. This means that property 4 is true: Eq.
(8.9) will agree with Eq. (8.1) when the cash flows are certain.
We hope that property 5 holds, at least on average. If property
5 held for all stocks, the active manager would not find any opportu-
nities in the marketplace.
206
Expected Returns and Valuation
INTERPRETATIONS
The value multiples v(t,s) help define a new set of probabilities
w*(t,s) = t(t,s)
- v(t,s). The risk-adjusted expectation E* uses the
modified set of probabilities.
In the simple example used previously, the outcomes cf(f,1) =
49 and cf(t,2) = 53 are equally likely, m(t,1) = a(t,2) = 0.5, and
the risk-free interest over the year is 6 percent, ir = 0.06. We find
(see the appendix) that v(t,1) =
1.38 and v(t,2) = 0.62. This is
consistent with properties 1 through 5. The altered probabilities
are m*(t,1) = 0.5 - 1.38 = 0.69 and m*(t,2) = 0.5 - 0.62 = 0.31. The
valuation for the risky stock works out correctly:
_ (0.69 - 49 + 0.31 - 53)
50 =
(1.06)!/2
(8.13)
The Role of Covariance
The definition of covariance and the fact that Ef{v(t)} = 1, can be
used to link the true and risk-adjusted expectations of cf(t):
E*{cf(t)} = Covi{cf(f),u(f)} + E{cf(t)}
(8.14)
Equations (8.5) and (8.9) imply that the covariance term will, in
general, be negative; in our example, we have E*{cf(t)} = 50.24 and
E{cf(t)} = 51, and so the covariance term is —0.76. This is the explicit
penalty for the risk. Its present value is —0.756.
An alternative interpretation of the valuation formula is that
the value multiples modify the cash flows. The value multiples
u(t,s) change the cash flows by amplifying some, if v(t,s) > 1, and
reducing others, if u(t,s) < 1. Since the value multiples have expected
value equal to 1, they are on average unbiased. For our example,
the rescaled cash flows are 67.62 = 1.38 - 49 and 32.86 = 0.62 - 53.
Suppose that cfy(t) is proportional to the total return on the
market portfolio. Then, the negative covariance indicates that v(t,s)
will tend to be less than 1 when the market is doing better than
its average (good times) and v(t,s) will tend to be larger than 1.0
when the market is below its average. The expectations E* makes
the risk adjustment by placing a lower value on good-time cash
flows as compared to bad-time cash flows. There is no great surprise
Valuation in Theory
207
a
I
a
ee
here. This means that the marginal amount of cash flow is worth
more when cash flow in general is scarce.
MARKET-DEPENDENT VALUATION
According to the modern theory of valuation, the key elements of
Eq. (8.9), both the risk-free rate of interest and the value multipliers
u(t,s), are market-dependent and not stock-dependent. The only
stock information needed is the potential cash flows cf(t,s). We use
the same v(t,s) and the same ir for all instruments: for IBM stock,
for GM puts, or for the S&P 500 portfolio. This critical property
arises in all modern asset valuation theories, including the CAPM
and the APT, which assert that only systematic risks are priced.
The APT frames this issue in the context of arbitrage-free
pricing: that assets with identical exposures to nondiversifiable
risks should have identical returns. This notion of arbitrage-free
pricing is critical to proving that the value multiples cannot depend
on individual stock returns, but only on portfolio Q returns.
We have discovered a simple formula for the value of a stock
providing a sequence of uncertain cash flows. The formula uses
adjusted expectations of the cash flows and discounts those ad-
justed expectations at market rates of interest to obtain a present
value for the stock. In some cases, such as option valuation and
variants of the CAPM, explicit formulas allow us to calculate the
modified cash flows. In other cases, such as the APT, these modified
expectations exist, although we don’t have specific information for
calculating them.’ The appendix includes examples of these appli-
cations.
VALUE AND EXPECTED RETURN
We can now link formulas for expected return, i.e., the CAPM and
the APT, and the valuation formula just described. Consider a stock
currently priced at p(0), paying a dividend d at the end of 1 year,
and with an uncertain price p(1) at the end of the year. Assume
5If we knew the true APT factors, so that we could calculate portfolio Q or portfolio S,
then we could calculate the modified cash flows.
208
Expected Returns and Valuation
ON EEE
ee ee
that the stock is fairly valued now and will be fairly valued at the
end of the year. If we sell the stock at the end of the year, the cash
flow will be the dividend plus the sale price: cf(1) = d + p(1). The
valuation formula over one period is
_ E*{d + p()} _ Ef): [d= pay)
sn
(cats pe ene
arias)
Shy
If p(0) ¥ 0, then we can convert Eq. (8.15) to an expected return
equation. Define total return R = [d + p(1)]/p(0). Divide Eq. (8.15)
by p(0), and multiply by 1 + i; Then recall that E{v(1)} = 1. The
net result is
E{R} = (1. + iz) — Cov{yR}
(8.16)
and
E* {R} = (1 + i;) = Efv: R}
(8.17)
Equation (8.16) says that the expected excess return on all stocks
is determined by their covariance with u This result is suspiciously
close to the CAPM and the APT results, that the expected excess
return on every stock is determined by its covariance with portfolio
Q (which for the CAPM is the market). The technical appendix
will show, in fact, that v is a function of the return to portfolio Q and
proportional to the return to a portfolio S, which is a combination of
the risk-free asset and portfolio Q. So we will relate Eq. (8.16) to
the CAPM and the APT. And, not only can we derive Eq. (8.16)
from Eq. (8.15), we can also derive Eq. (8.15) from Eq. (8.16). Our
previously derived expected return formulas imply valuation as
in Eq. (8.15).
Equation (8.17) also demonstrates that under the modified
probabilities, the expected return on the risky investment is equal
to the return on the risk-free investment. In fact, under the modified
expectations, all stocks have (modified) expected returns equal to
the risk-free return.
What if the market price and the model price don’t agree?
Suppose we start with an asset that has a market value p(0,mkt)
that is not equal to zero and is not properly valued:
E* {cf}
plO,mkt) #
= p(0,mdl)
~
(8.18)
Valuation in Theory
209
Define « and y such that
_
p,mdl) —
p(0,mkt)
‘
p(0,mkt)
(8.19)
and
ft p(1,mdl) — p(1,mkt)
ep mebeed
oe
The parameter k measures the extent of misvaluation of the stock;
it is the percentage difference between the fitted and market prices
at time 0. The parameter y measures the persistence of the misvalua-
tion: how long it will take for the market to learn what we know.
Presumably 0 = y = 1. If this is a “slow idea,” then y will be close
to 1.0; much of the mispricing will remain. If this is a “fast idea,”
then y will be close to 0. We can think of —0.69/In{y} as the half-
life of the misvaluation, the number of years it will take for half
the misvaluation to disappear.
Equations (8.16), (8.19), and (8.20) yield®
E{R} = 1 + ip — Cov{yR} + a
(8.21)
where a is
2
yo eo ay)
a = (1+ i,)
staat
(8.22)
Equation (8.22) breaks the expected return into what we would
expect if the stock were fairly valued and a second term that cor-
rects for the market’s incorrect valuation of the stock. Notice that
a = 0 if either k = 0 or y = 1; it is no good if the world never
learns that this stock is improperly valued. Also, if y = 0, then
a = (1 + i) - k; we realize the full benefit, plus interest, over
the period.
Table 8.1 shows the alphas we get for different levels of k and
y. It assumes a 6 percent annual interest rate.
’Define R* as the return to the fairly priced asset, and show that R is proportional to R*.
Equation (8.21) then follows directly from Eq. (8.16).
210
Expected Returns and Valuation
pe
er
ee
ee
TABLE
8&1
0.0
1.06%
0.63%
5.30%
3.12%
10.60%
6.12%
26.50%
14.45%
53.00%
26.50%
SUMMARY
The modern theory of valuation prices uncertain future cash flows
by risk-adjusting the expected cash flows and discounting them to
the present using the risk-free rate. This theory is consistent with
the CAPM and APT models, which forecast expected returns; and
in fact the risk-adjusting procedure is related to portfolio Q.
If the market doesn’t currently price the asset fairly, then the
asset’s expected return comprises two components: the return ex-
pected if the asset were fairly priced, and a correction term based
on the market price’s approaching fair value.
PROBLEMS
1. In the simple stock example described in the text, value
a European call option on the stock with a strike price
of 50, maturing at the end of the 1-month period. The
option cash flows at the end of the period are
%
Max{0,p(t,s) — 50}, where p(t,s) is the stock price
at time ¢ in state s.
2. Compare Eq. (8.16) to the CAPM result for expected
returns, to relate v to rg. Impose the requirement that
E{v} = 1 to determine v exactly as a function of ro.
3. Using the simple stock example in the text, price an
instrument which pays $1 in state 1 [cf(t,1).= 1] and $—-1
in state 2 [cf(t,2) = —1]. What is the expected return to
Valuation in Theory
211
this asset? What is its beta with respect to the stock?
How does this relate to the breakdown of Eq. (8.7)?
4. You believe that stock X is 25 percent undervalued, and
that it will take 3.1 years for half of this misvaluation to
disappear. What is your forecast for the alpha of stock X
over the next year?
REFERENCES
Arrow, Kenneth J. Essays in the Theory of Risk-Bearing (Chicago: Markham Publish-
ing Company, 1971).
Bar-Yosef, Sasson, and Hayne Leland. Risk Adjusted Discounting. University
of California, Berkeley Research Program in Finance working paper #134,
December 1982.
Black, Fischer, and Myron Scholes. “The Pricing of Options and Corporate Liabili-
ties.” Journal of Political Economy, vol. 81, no. 3, 1973, pp. 637-654.
Chamberlain, Gary, and M. Rothschild. “Arbitrage, Factor Structure and Mean-
Variance Analysis on Large Asset Markets.” Econometrica, vol 51, no. 5, 1983,
pp. 1281-1304.
Cox, John C., and Mark Rubinstein. Options Markets (Englewood Cliffs, N.J.:
Prentice-Hall, 1985).
Debreu, Gerard. Theory of Value (New York: John Wiley & Sons, 1959).
Garman, Mark B. “A General Theory of Asset Valuation under Diffusion State
Processes.” University of California, Berkeley Research Program in Finance
working paper #50, 1976.
Garman, Mark B. “Towards a Semigroup Pricing Theory.” Journal of Finance, vol.
40, no. 3, 1985, pp. 847-861.
Grinold, Richard C. “The Valuation of Dependent Securities in a Diffusion Pro-
cess,” University of California, Berkeley Research Program in Finance work-
ing paper #59, April 1977.
. “Market Value Maximization and Markov Dynamic Programming.” Man-
agement Science, vol. 29 no. 5, 1983, pp. 583-594.
. “Ex-Ante Characterization of an Efficient Portfolio.” University of Califor-
nia, Berkeley Research Program in Finance working paper #59, Septem-
ber 1987.
Harrison, Michael J., and David M. Kreps. “Martingales and Arbitrage in Multi-
period Securities Markets.” Journal of Economic Theory, vol 20, 1979, pp.
381-408.
Hull, John. Options,
Futures, and Other Derivative Securities (Englewood Cliffs, N.J.:
Prentice-Hall, 1989).
Ohlson, James A. “A Synthesis of Security Valuation Theory and the Role of
Dividends, Cash Flows, and Earnings.” Columbia University working paper,
April 1989.
Ross, Stephen. “Return, Risk, and Arbitrage.” In Risk and Return in Finance, edited
by I. Friend and J. Bicksler (Cambridge, Mass.: Ballinger, 1976).
212
Expected Returns and Valuation
Rubinstein, Mark. “The Valuation of Uncertain Income Streams and the Pricing
of Options.” Bell Journal of Economics, vol 7, 1976, pp. 407-425.
Sharpe, William F. “Capital Asset Prices:
A Theory of Market Equilibrium under
Conditions of Risk.” Journal of Finance, vol. 19, no. 3, 1964, pp. 425-442.
Williams, John Burr. The Theory of Investment Value (Amsterdam: North-Holland
Publishing Company, 1964).
Technical Appendix
This appendix derives some of the results used in the text. In par-
ticular,
m We derive the basic valuation result in the case of a finite
number of outcomes.
® We illustrate the basic valuation result using option
pricing.
m We apply the CAPM (or really mean/variance theory) to
valuation.
® We introduce portfolio S as a more general portfolio
approach to valuation.
Theory of Valuation
Consider a finite number of assets indexed by n = 0,1,...,N over
a finite number of periods T. Start at time t = 0, and observe the prices
of the assets at times t = 1, 2,..., T. The prices evolve along paths.
The collection of paths determines the possible outcomes. At time
t = T, we will know what path we have followed. At time t = 0, we
know only the set of possible paths. At intermediate times, 0 < t <
T, we have partial knowledge of the eventual path we will follow.
Specifying the state of knowledge at each intermediate point
in time determines the system. Knowledge is refined throughstime,
as the collection of possible paths shrinks. At time t, we can be in
one of S(t) states, where a state indicates a collection of possible
paths we might be following. As time moves on, this set of possible
paths is reduced, until at time T we know what path we have been
following. Figure 8A.1 illustrates a case in which there are 3 time
periods and 11 possible paths.
We can make this more precise. At time tf = J in state s, we
will know the unique time ft — 1 state that preceded state s; the
Valuation in Theory
213
Figure 8A.1
predecessor is denoted ¢(s,t). We will also know the possible succes-
sors to (s,t) at time t + 1. That collection of possible successors is
denoted (X(s,t). For every possible successor z € ((s,t), we must
have (s,t) as a predecessor; i.e., if z € ((s,t), then (z,t+1) = s.
Similarly, if z ¢ O(s,t), then (z,t+1) # s. The set of all possible
states at time t is denoted P(t).
We have probabilities m{s,t} of being in state s at time t. We
require only that these probabilities be positive.
Asset prices are given by p,(s,t), the price of asset n if state s
occurs at time ft. Since there is only one state at time t = 0, we have
pn(1,0) as the initial prices.
One of the assets, call it asset n = 0, is risk-free. At time t in state
S, a positive risk-free rate of interest i;(s,t) will prevail from time t
until time t + 1. We start with p,(1,0) = 1. At time t + 1, we have
polzt + 1) = [1 + if(s,t)] - pols,t)
(8A.1)
for every z € (Xs,t). This assumption allows future rates of interest
to be uncertain, although we will always know what rate of interest
obtains over the next period.
To make life simple, we will ignore dividends. This means
that we can assume either that all dividends are paid at time T or
that p,(s,t) includes accumulated dividends.
214
Expected Returns and Valuation
An investment strategy is determined by the N+1-element
vector NS(s,t) = {NS,(s,t),NS,(s,t), .
.
., NSy(s,t)} for each state, time,
and asset. It describes the number of shares of that asset in the
portfolio at that state and held from time ft to time t + 1. The value
of the portfolio at time ¢ in state s using strategy NS is denoted
W(s,t). The value W(s,t) is
N
W(s,t) = >) NS,(s,t) + puls,t)
(8A.2)
n=0
To conserve value, we impose a self-financing condition: The value
of the portfolio at the end of period t-1 must exactly match the
value of the portfolio at the start of period t. Mathematically, for
t=1lands E(t),
N
N
W(s,t) = > NS,(s,t) > pils,t)
= SY NS,[o(,t),t — 1] - p,(s,t)
n=0
n=0
(8A.3)
The value of the portfolio before it is revised is the same as the
value of the portfolio after it is revised.
An arbitrage opportunity is available if we can find an invest-
ment strategy that starts with a nonpositive amount of money,
W(1,0) = 0; is guaranteed not to lose money, W(s,t) = 0 for sE®(T);
and makes money in at least one outcome,
> W(s,T) > 0.
sEW(T)
Proposition 1
If there are no arbitrage opportunities, we can find positive valua-
tion multiples v(s,t) > 0 such that for any asset n = 0,1, 2,..,N
and any time ¢ = 1, 2,..,
T,
a
j aan
Pni1,0)
paps v(s,t) eee
(8A.4)
Proof
Consider the following linear program:
Max} ») wr}
.
(8A.5)
sE G(T)
Valuation in Theory
215
subject to
N
> NS,(1,0) - p,(1,0) < 0
(8A.6)
n=0
N
N
— SNS, (s,£) - pils,t) + >) NS,[o(s,t),t — 11+ p,ls,t) = 0 (8A.7)
n=0
n=0
for every 1 = t < T and s€@(t), and
(8A.8)
N
— 3S NS,(s,T) « pils,T) + W(s,T) = 0
n=0
W(s,T) = 0
(8A.9)
for sE®(T).
The linear program maximizes the sum of the end-period
wealths across the possible states, subject to the constraints of initial
wealth nonpositive [Eq. (8A.6)], self-financing strategies [Eq. (8A.7)],
end-period wealth definition [Eq. (8A.8)], and nonnegative end-
period wealth in each possible state [Eq. (8A.9)].
Given the constraints of initial wealth nonpositive and final
wealth nonnegative, this linear program has a feasible solution:
NS,(s,t) = 0 for all n, s, and t. By the no-arbitrage condition, this
is an optimal solution as well; i.e., no solution will exhibit positive
value for the objective.
The duality theorem of linear programming then implies that
there will be an optimal solution q(s,t) to the dual problem. The
dual problem is
tf
Min) SS) (st)
(8A.10)
t=0 sEW(t)
subject to
—q(s,t)- pr(st) + > q@t+1)-pztt+1)=0
(8A.11)
zE((s,t)
216
Expected Returns and Valuation
for all n =0,425.N;
VSit-< TF seO@7and
q(1,0) = 0
(8A.12)
Gs
(8A.13)
for all sE®(T).
Let q(s,t) be an optimal dual solution. Equation (8A.13) guaran-
tees that q(s,T) are positive, and in fact greater than 1. We can
further show, by successive applications of Eq. (8A.11), that each
q(s,t) is positive, using the risk-free asset:
q(s,t) = (1 + i(s,t)}- >) (zt + 1)
(8A.14)
zE(\s,t)
Define the conditional probabilities m*(z,t + 1 | s,t) by
1+ ip(s,t)
’
5
a*(z,t Ti |
s,t) =
q(s,t)
q(z,t Ar 1)
if zZE(XVs,t)
0
if zZQ(s,t)
(8A.15)
This definition, along with Eq. (8A.11), leads to the intertemporal
valuation formula
{PASO S area +15 fet
*
Dl ware
zEQ(s,t)
This formula requires probabilities in states (z,t+1) conditional on
predecessor states (s,t). We would like to rewrite these in terms
of unconditional probabilities, which we can derive starting with
m*(1,0) = 1. Then, using the laws of probability and the fact that
state s at time t+1 has a unique predecessor ¢(s,t+1) at time t,
w*(s,t + 1) = w*[s,t + 1| d(s,t + 1),t] - w*[b(s,t + 1),t]
(8A.17)
The valuation multipliers are then
ar*(s,t)
v(s,t) = Pe)
i
(8A.18)
Valuation in Theory
217
Repeated application of Eqs. (8A.16) through (8A.18) will demon-
strate Proposition 1, Eq. (8A.4).”8
Options Pricing
The most familiar context for the modern theory of valuation is in
options pricing. Here is an example, which we also used in the
main text of the chapter. Consider a single stock and a single
1-month period with two equally likely outcomes. The stock can
go either up, the UP event, or down, the DN event. The risk-free
asset increases in value from 1.00 to Rp = (1 + i;)!/" = 1.00487,
corresponding to an annual interest rate of 6 percent. The stock’s
initial price is p = 50, and its final value is equally likely to be
’This proof demonstrates the existence but not the uniqueness of the valuation
mulipliers. Only if we have a complete market will we have unique valuation
multipliers. In a complete market, for any t, we will be able to devise a self-
financing strategy that pays off 1 in state s and 0 in states uES(t), u # s. Not only
that, we will be able to determine the minimum initial input, V*(s,t), into a self-
financing strategy necessary to produce W(s,t) = 1, W(u,t) = 0 for uES(t), u A s.
The term V%*(s,t) will be positive because of the no-arbitrage condition, and
a(s,t)
plier V* (s,t) + po(s,t)
’Proposition 1 required the absence of arbitrage opportunities. In practice, e.g., if we
generate prices via Monte Carlo, the process may not be exactly arbitrage-free.
However, we can trick the process into being arbitrage-free by assuming that the
original probabilities are the Martingale probabilities and adjusting the original
prices appropriately. To be exact, define 5,(s,t) and adjusted prices py(s,t):
8,(5,) =
{1 + ix(s,t)) »
pi(s,t)
Set +1| st) > pzt + 1)
zES(t)
with
px(1,0) = p,(1,0)
and
pr(z,t + 1) = 8,(s,t) - p,(z,t + 1)
for z€M(s,t).
With these adjusted prices, Eq. (8A.16) will hold using the original probabilities.
Variations of this idea are used sometimes in options pricing theory.
218
Expected Returns and Valuation
end
ee ee ee
ee
ee ee
eee
Pup = 53 OF Pon = 49. The outcomes UP and DN are equally likely:
Typ = Tpn = 0.5.
Now let’s calculate the valuation measure in the UP and DN
states. Following Eq. (8A.11), the dual linear program in this simple
case is
go — {qup * Re + Gon: Re} = 0
(8A.19)
qo * 50 — {qup - 53 + gon * 49} = 0
(8A.20)
with go = 0 and qup gon = 1. Solving for vyp = {--} Upn =
fo * Tup
‘ett. we find 0.62 and 1.38, respectively.
4o * TDN
We can check that these valuation multiples correctly value
both the risk-free asset and the stock. These multiples will be non-
negative’ as long as {Pep
co a{L tage. {Pex and their expected
value will always be 1.0.
Of course, options pricing theory was developed to price op-
tions, and given these valuation multiples, we can price any claim
contingent on the stock price. For this simple case in particular, we
can price options maturing at the end of the period, with payouts
dependent on the ending stock value. The payout for a call option
would have the form Max[0, S(T) — K], where K is the strike price.
We can easily expand this framework to multiple periods. For
a more substantial treatment, see the texts by Cox and Rubinstein
and by Hull.
Connection with the CAPM and APT
The main body of the chapter discussed the connection betweefi val-
uation and expected returns. We revisit that topic here. Let p,, be the
initial value of stock n, d,, the dividends paid on the stock (at the end
of the month), and p¥ the final value. Let R,,, R; and Rg be the total
returns on the stock, the risk-free asset, and portfolio Q. The excess
returns are r, and rg. In the CAPM, portfolio Q is the market.
~
"If these conditions do not hold, then arbitrage opportunities exist.
Valuation in Theory
219
Proposition 2
The valuation function v depends only on the return to portfolio
Q, according to
v(s) =1-k- {ro(s) — fol
(8A.21)
with
Pe fo
(8A.22)
re)
Proof
Define the return on asset n with outcome s as
Sor
R,(s) = B® : a
(8.23)
Since portfolio Q defines expected excess returns,
E{R,} = Rp + x + Cov{r,,r9}
(8A.24)
The definition of covariance implies
Cov{r,1g} = Cov{R,,
rg} = E{Rn + (tg — Efrg})}
(8 A.25)
Now, Eq. (8A.25), in combination with Eqs. (8A.24) and (8A.21),
leads to
E{v(s) - [p%(s) + d,(s)]}
(8A.26)
:
(baerh
This is the desired result.
Notice that v depends only on portfolio Q’s return. The ex-
pected value of v is 1 and, since k > 0, v decreases as the market
return increases. Reasonable estimates of k are between 1.5 and
2.00; as an example, we'll choose 1.75. Hence v is negative if rg >
fo + 0.57. If the expected annual excess return to the market was
approximately 6 percent, this would be a 63 percent excess market
return: more than a three standard deviation event. In fact, the
largest two annual S&P 500 returns since 1926 have been a 54
percent return in 1933 and a 53 percent return in 1954.
Proposition 2 relates the valuation multipliers v to the excess
return to portfolio Q. Alternatively, we can introduce a new portfo-
lio, portfolio S, which also explains excess returns and whose total
220
Expected Returns and Valuation
a
returns are directly proportional to the valuation multipliers. For
the purpose of this technical appendix, portfolio S provides simply
another view of excess returns and valuation. We introduce portfo-
lio S because (although we will not make use of this property) it
is also a more robust approach to excess returns and valuation than
portfolio Q. We require very few assumptions to determine that
portfolio S exists and explains excess returns. For example, while
we require that the expected excess return to portfolio C be positive
for the existence of portfolio Q, portfolio S exists and explains
expected excess returns even without that assumption.
Portfolio S
We define a portfolio S as the portfolio containing both risky and
riskless assets with the minimum second moment of total return. We
will investigate the properties of portfolio S, including its relation to
excess returns, portfolio Q, and the valuation multipliers.
The total return for any portfolio P is given by Rp = 1 +
ip + rp. Portfolio S solves the problem
Min{E{R3}}
(8A.27)
where portfolio P contains both risky and risk-free assets. The risk-
free portfolio would give us second moment Rj. Portfolio S has
even less.
Proposition 3'°
For any portfolio P, we have
E{rp} = b - Cov{rp,rs}
(8A.28)
“This proposition is actually true much more generally. We can let Rs and Rp be the
returns to strategies involving rebalancing, option replication, etc. Given a
stochastic risk-free rate, and R; the return to the strategy that rolls over the risk-
free investment, we find
E{Rp = Rr} = Re re b G Cov{Rp ae Rz,Rs}
where
=i
E{Rs}
b=
as in the main text of the appendix.
Valuation in Theory
221
where
3.
b = iE
(8A.29)
Proof
Consider a portfolio P(w) with fraction (1 — w) invested
in portfolio S and fraction w invested in portfolio P. The total return
on this mixture will be
R,(w) = Rs =p (6b)
{Rp 3 Rs}
(8A.30)
Define gp(w) as the expected second moment of the return on the
mixture:
gp(w) = E{R3(w)} = E{R3} + 2+ w- E{Rs - (Rp
(8A.31)
— Rs)} ar w : E{(Rp aay R;)*}
Since Rg; is the portfolio that has minimum second moment, the
derivative of gp(w) at w = 0 must be zero. Hence
E{Rs; - (Rp — Rs)} = 0
(8A.32)
for any portfolio P. We can expand this to
Cov{rp,rs} te E{Rp} < E{Rs} = E{R3}
(8A.33)
Equation (8A.33) holds for any portfolio P, including the risk-free
portfolio F, and so
E{R;} - E{Rs} = E{R3}
(8A.34)
Combining Eqs. (8A.33) and (8A.34) leads to Proposition 3, Eq.
(8A.28).
Proposition 3 demonstrated the connection between portfolio
S and expected returns. We also know the connection between
portfolio Q and expected returns. And so, there is a link between
portfolio S and portfolio Q.
Proposition 4
If
= Portfolio S solves Eq. (8A.27)
222
Expected Returns and Valuation
ROG eS eS ee
ee
eee
® Portfolio Q is the fully invested portfolio with maximum
Sharpe ratio”
then portfolio S is a mixture of portfolio F and portfolio Q:
Rs = Rp ae Wo . {Ro a R;}
(8A.35)
where
_ —SRo«
{1 + ish
(8A.36)
og: {1 + SRB
Proof
Given an arbitrary starting fully invested portfolio P, con-
sider a portfolio P(w) composed of a fraction w invested in portfolio
P and a fraction (1 — w) invested in portfolio F. Its total return is
Now choose w to minimize
the expected second moment,
E{Ré(wp)}, of the return. The optimal w is
— ~SRp
+ {1 + is}
Wp = cp
{1 + SR)
(8A.38)
with associated optimal expected second moment
(1 + i)?
2
=
E{Rp(wp)}
1 + SR
(8A.39)
As long as SRp is not zero, we can do better than just the risk-free
portfolio. In fact, the larger SRp is in absolute value, the better we
can do. We achieve the minimum second moment over all portfolios
(risky plus risk-free) by choosing the fully invested portfolio R that
maximizes SR}: portfolio Q. This proves Proposition 4, Eq. (8A.35).
Our final task is to express the valuation multiples in terms
of portfolio S.
"We are making the familiar assumption that portfolio C has positive expected excess
return, and so portfolio Q—the fully invested portfolio that explains expected
excess returns—exists.
Valuation in Theory
223
Proposition 5
The valuation multiples are
Rs
E{Rs}
(8A.40)
Vv =
Proof Combining Proposition 3 [Eq. (8A.28)], which explains
expected excess returns using portfolio S, and Proposition 2
[Eq. (8A.21)], which expresses the valuation multiples in terms of
portfolio Q, we can derive
Jak ae a
(8A.41)
where
y=
Oe (RK, —E(R,)})
(8A.42)
Since
= —1/E{Rs}, this simplifies to Proposition 5, Eq. (8A.40).
Exercises
1. Using the definitions from the technical appendix to
Chap. 2, what is the characteristic associated with
portfolio S?
2. Show that the portfolio S holdings in risky assets satisfy
V -h; = —E{Rs} - f
3. Show that portfolio S exists even if fo < 0, and that if
fc = 0, then portfolio S will consist of 100 percent cash
plus offsetting long and short positions in risky assets.
4. Prove the portfolio S analog of Proposition 1 in the
technical appendix of Chap. 7, i.e., that the factor model
(X, E, A) explains expected excess returns if and only if
portfolio S is diversified with respect to (X, F, A).
Applications Exercises
1. If portfolio Q is the MMI and pg = 6 percent, what is
portfolio S? Use Proposition 4 of the technical appendix,
which expresses portfolio S in terms of portfolio Q.
224
Expected Returns and Valuation
2. Using the result from the first applications exercise, what
is the valuation multiple in the state defined by rg = 5
percent? Use Proposition 5 of the technical appendix. If
interest rates are 6 percent, what is the value of an
option which pays $1 in 1 year only in the state defined
by ro = 5 percent? Assume that the probability of that
state occurring is 50 percent.
