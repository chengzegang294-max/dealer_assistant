# Chapter 16: Transactions Costs, Turnover, and Trading

- **book_name**: Active Portfolio Management
- **main_source**: pdf
- **cross_check_source**: none
- **pdf_role**: main_text_source
- **split_scope**: pages 467-498

---

CHAPTER
16
Transactions Costs,
Turnover,
and Trading
INTRODUCTION
Transactions costs, turnover, and trading are the details involved
in moving your current portfolio to your target portfolio.’ These
details are important. Studies show that, on average, active U.S.
equity managers underperform the S&P 500 by 1 to 2 percent per
year, and, as Jack Treynor has argued, that average underperfor-
mance can only be due to transactions costs. Given that typical
institutional managers seek to add only 2 to 3 percent active return
(and charge ~0.5 percent for the effort), this is a significant obstacle.
Transactions costs often appear to be unimportant. Who cares
about a 1 or 2 or even 5 percent cost if you expect the stock to
double? Unfortunately, expectations are often wrong. At the end
of the year, your performance is the net result of your winners and
losers. But winner or loser, you still pay transactions costs. They
can be the investment management version of death by a thousand
cuts. A top-quartile manager with an information ratio of 0.5 may
lose roughly half her returns because of transactions costs. They
are important.
In fact, they should influence your choice of target portfolio.
2A 1992 study by Lakonishok, Shleifer, and Vishny measured equal-weighted
underperformance of 1.3 percent and capitalization-weighted underperformance of
2.6 percent relative to the S&P 500 for 341 U.S. equity managers over the period
1983 through 1989. A 1995 study by Malkiel looked at active equity mutual funds
from 1982 to 1991. Interestingly, the naive analysis showed an average
underperformance relative to the S&P 500 of only 43 basis points, but after
accounting for survivorship bias (including funds which existed but disappeared
prior to 1991), the average underperformance increased to 1.83 percent.
445
446
Implementation
Chapter 14 dealt with transactions costs as an input to the
portfolio construction exercise.
Now we will deal with transactions
costs and turnover more broadly (how they arise), more concretely
(how to estimate them), and more strategically (how to reduce
these costs while preserving as much of the strategy’s value added
as possible). We will attack the strategic issue in two ways: reducing
transactions costs by reducing turnover while retaining as much
of the value added as possible, and reducing transactions costs
through optimal trading.
Basic insights we will cover in this chapter include the fol-
lowing:
® Transactions costs increase with trade size and the desire
for quick execution, which help to identify the manager
as an informed trader and require increased inventory
risk by the liquidity supplier.
= Transactions costs are difficult to measure. At the same
time, accurate estimates of transactions costs, especially
distinctions in transactions costs among different stock
trades, can significantly affect realized value added.
# Transactions costs lower value added, but you can often
achieve at least 75 percent of the value added with only
half the turnover (and half the transactions costs). You
can do better by distinguishing stocks by their
transactions costs.
® Trading is itself a portfolio optimization problem, distinct
from the portfolio construction problem. Optimal trading
can lower transactions costs, though at the expense of
additional short-term risk.
™ There are several options for trade implementation, with
rules of thumb on which to use when.
si
Turnover occurs whenever we construct or rebalance a portfo-
lio, motivated by new information (new alphas) or risk control.
Transactions costs are the penalty we pay for transacting. Transac-
tions costs have several components: commissions, the bid/ask
spread, market impact, and opportunity cost. Commissions are the
charge per share paid to the broker for executing the trade. These
tend to be the smallest component of the transactions costs, and
Transactions Costs, Turnover, and Trading
447
pe
ae en
8 Ss eee a
ee
ee
the easiest to measure. The bid/ask (or bid/offer) spread is the
difference between the highest bid and the lowest offer for the
stock; it measures the loss from buying a share of stock (at the
offer) and then immediately selling it (at the bid). The bid/ask
spread is approximately the cost of trading one share of stock.?
Market impact is the cost of trading additional shares of stock.‘
To buy one share of stock, you need only pay the offer price. To
buy 100,000 shares of stock, you may have to pay much more than
the offer price. The 100,000-share price must be discovered through
trading. It is not known a priori. Market impact is hard to measure
because it is the cost of trading many shares relative to the cost of
trading one share, and you cannot run a controlled experiment and
trade both many shares and one share under identical conditions.
Market impact is the financial analog of the Heisenberg uncertainty
principle. Every trade alters the market.
MARKET MICROSTRUCTURE
The field of market microstructure studies the details of how mar-
kets work and transactions occur, in order to understand transac-
tions costs, especially bid/ask spreads and market impact. This is
a field of current active research that as yet lacks a single complete
and widely accepted model. There is no CAPM or Black-Scholes
model of trading. However, there are at least two ideas from this
field that can illuminate the source of transactions costs.
When a portfolio manager trades, he or she must go to the
marketplace to find someone to trade with. That other person,
possibly a specialist on the New York Stock Exchange or a market
maker on
NASDAQ, will trade (“provide liquidity”), but for a price.
Often this liquidity supplier’s only business is providing short-term
liquidity, i.e., he or she is not a long-term investor in the market.
Several considerations determine what price the liquidity sup-
plier will charge (and can charge—after all, providing liquidity is
a competitive business). First, the liquidity supplier would like to
know why the manager is trading. In particular, does the manager
3You can never be certain of this cost until you actually trade.
4Some authors include the bid/ask spread in market impact, given that it is a market
phenomenon (as opposed to commissions and taxes).
448
Implementation
possess any unique nonpublic information that will soon change
the stock price? Is the manager an “informed trader’? If so, the
liquidity supplier would want to trade at the price the stock will
reach once the information is public. Typically, though, the liquidity
supplier can’t tell if the manager has valuable information, has
worthless information, or is trading only for risk control purposes.
He or she can only guess at the value of the manager’s information
by the volume and urgency of the proposed trade. The larger and
more urgent the trade, the more likely it is that the manager is
informed, and the higher the price concession the liquidity supplier
will demand. Market impact increases with trading volume.
A second consideration influencing transactions costs is inven-
tory risk. Even without informed traders, market impact would
still exist. Liquidity suppliers have no intention of holding positions
in inventory for long periods of time. When the liquidity supplier
trades, her or his goal is to hold the position in inventory only
until an opposing trade comes along. Every minute before that
opposing trade appears adds to the risk. The liquidity supplier has
a risk/return trade-off, and will demand a price concession (return)
to compensate for this inventory risk. The calculation of this risk
involves several factors, but certainly the larger the trade size, the
longer the period that the position is expected to remain in inven-
tory, and hence the larger the inventory risk and the larger the
market impact. Market impact increases with trading volume.
The theory of market microstructure can provide basic insights
into the sources of transactions costs. The details of how these
influences combine to produce the costs observed or inferred in
actual markets is still under investigation and is beyond the scope
of this book. However, we will utilize some of these basic insights
throughout the chapter.
ANALYZING AND ESTIMATING
TRANSACTIONS COSTS
Analyzing and estimating transactions costs is both difficult and
important. Market impact is especially difficult to estimate because,
as we have discussed, it is so difficult to measure.
Estimating transactions costs is important because accurate
estimates can significantly affect realized value added, by helping
Transactions Costs, Turnover, and Trading
449
the manager choose which stocks to trade when constraining turn-
over, and by helping him or her decide when to trade when schedul-
ing trades to limit market impact.
This endeavor is sufficiently important that analytics vendors
like BARRA and several broker/dealers now provide transactions
cost estimation services.
Ideally, we would like to estimate expected transactions costs
for each stock based on the manager’s style and possible range
of trade volumes. The theory of market microstructure says that
transactions costs can depend on manager style, principally because
of differences in trading speed. Managers who trade more aggres-
sively (more quickly) should experience higher transactions costs.
Wayne Wagner (1993) has documented this effect, and illus-
trated the connection between information and transactions costs,
by plotting transactions costs versus short-term return (gross of
transactions costs) for a set of 20 managers. The most aggressive
information trader was able to realize very large short-term returns,
but they were offset by very large transactions costs. The slowest
traders often even experienced negative short-term returns, but
with small or even negative transactions costs. (To achieve negative
transactions costs, they provided liquidity to others.)
Estimation of expected transactions costs requires measure-
ment and analysis of past transactions costs. The best place to start
is with the manager’s past record of transactions and the powerful
“implementation shortfall” approach to measuring the overall cost
of trading.” The idea is to compare the returns to a paper portfolio
with the returns to the actual portfolio. The paper portfolio is the
manager’s desired portfolio, executed as soon as he or she has
devised it, without any transactions costs. Differences in returns
to these two portfolios will arise as a result of commissions, the
bid/ask spread, and market impact, as well as the opportunity
costs of trades that were never executed. For example, some trades
never execute because the trader keeps waiting for a good price
while the stock keeps moving away. Wayne Wagner has estimated
that such opportunity costs often dominate all transactions costs.
‘Jack Treynor first suggested the approach, and Andre Perold later embellished it.
450
Implementation
Many services that currently provide ex post transactions cost
analysis do not use the implementation shortfall approach, because
it involves considerable record keeping. They use simpler methods,
such as comparing execution prices against the volume-weighted
average price (VWAP) over the day. Such an approach measures
market impact extremely crudely and misses opportunity costs
completely. The method simply ignores trade orders that don’t
execute. And, as a performance benchmark, traders can easily game
VWAP: They can arrange to look good by that measure.
The most difficult approach to transactions cost analysis is
to directly research market tick-by-tick data. Both the previously
described methods began with a particular manager’s trades. When
analyzing tick-by-tick data, we do not even know whether each
trade was buyer- or seller-initiated. We must use rules to infer
(inexactly) that information. For example, if a trade executes at the
offer price or above, we might assume that it is buyer-initiated.
The tick-by-tick data are also full of surprising events—very
large trades occurring with no price impact. But the record is never
complete. Did the price move before the trade, in anticipation of
its size? Did the trade of that size occur only because the trader
knew beforehand that existing limit orders contained the necessary
liquidity? Researchers refer to this as censored, or biased, data. The
tick-by-tick data show trades, not orders placed, and certainly not
orders not placed because the cost would be too high. Realized
costs will underestimate expected costs.
There are several other problems with tick-by-tick trade data.
The data set is enormous, generating significant data management
challenges. But in spite of all these data, we only rarely observe
some assets trading. These thinly traded assets are often the most
costly to trade. So this record is missing information about the
assets whose costs we often care about most.
.
Finally, tick-by-tick data are very noisy, because of discrete prices,
nonsynchronous reporting of trades and quotes, and data errors.
All of these challenges affect not only the estimation of market
impact but also the testing of models forecasting market impact.
Clearly, building an accurate, industrial-strength transactions cost
model is a very significant undertaking.
One approach to transactions costs which has proven fruitful,
models costs based on inventory risk. The inventory risk model
Transactions Costs, Turnover, and Trading
451
a
OS a
ee
estimates market impact based on a liquidity supplier’s risk of
facilitating the trade. Here heuristically is how that works. First,
given a proposed trade of size Vag, the estimated time before a
sufficient number of opposing trades appears in the market to clear
out the liquidity supplier’s net inventory in the stock is
4 ‘ade
Tetear % =
(16.1)
daily
where V
gay is the average daily volume (or forecast daily volume)
in the stock. Equation (16.1) states that if you want to trade one
day’s volume, the liquidity supplier’s estimated time to clear will
be on the order of one day, and so on.
This time to clear implies an inventory risk, based on the
stock’s volatility:
O inventory =i, 0
\/
Sih
(16.2)
where Eq. (16.2) converts the stock’s annual volatility o to a volatil-
ity over the appropriate horizon. Equation (16.2) assumes that we
measure Tear in days, and that a year contains 250 trading days.
The final step in the model assumes that the liquidity supplier
demands a return (price concession or market impact) proportional
to this inventory risk:
~
oni O inventory
(16.3)
where c is the risk/return trade-off, and we measure return rela-
tive to the bid price for a seller-initiated trade and relative to the
offer for a buyer-initiated trade. Since there exists some competi-
tion between liquidity suppliers, the market will help set the
constant c.
For a seller-initiated trade, the transactions cost will include
not only the price concession from the offer to the bid, but an
additional concession below the bid price, depending on the size
of the trade. The argument for the buyer-initiated trade is similar.
452
Implementation
Combining Eqs. (16.1) through (16.3), adding commissions,
and converting to units of return, leads to
d
V ade
Cost = commisson + (Ps
/ = apes
+ Ce" \ ae (16.4)
aily
price
where c,, includes the stock’s volatility, a risk/return trade-off, and
the conversion from annual to daily units.
In general, this approach and Eq. (16.4) are consistent with a
trading rule of thumb that it costs roughly one day’s volatility to
trade one day’s volume. This rule of thumb implies that c. ~
Ofa/\/250}.
One consequence of this inventory risk approach is that market
impact should increase as the square root of the amount traded. This
agrees remarkably well with the empirical work of Loeb (1983)].°
Because the total trading cost depends on the cost per share times
the number of shares traded, it increases as the 3/2 power of the
amount traded.
Loeb, a passive manager at Wells Fargo Investment Advisors,
collected bids on different size blocks of stock. Figure 16.1 displays
his results against a square root function. His observed dependence
of cost on trade size clearly follows the square root pattern (plus
fixed costs at low volume).
There are several ways to forecast transactions costs, starting
with Eq. (16.4). A simple approach is to choose c,, such that trades
of typical size experience about 2 percent round-trip transactions
costs, or to develop a better estimate based on analysis of the
manager’s past transactions. If your optimizer requires that transac-
tions costs be expressed as a piecewise linear or quadratic function
of trade size, then approximate Eq. (16.4) appropriately, HI the
region of expected trade sizes.
But the above approach leaves much on the table. This inven-
tory risk approach can support more elaborate structural models,
‘Researchers at BARRA, especially Nicolo Torre and Mark Ferrari, are responsible for
identifying the square root dependence of the Loeb data. They have also used
empirical methods to find the best-fitting exponent (square root corresponds to
1/2) in the dependence of market impact on trade volume. The square root
provides the best fit. See BARRA (1997) for details.
Transactions Costs, Turnover, and Trading
453
es
ee
4.50%
4.00%
One-way
Total
Cost
1.00%
8 One-way Total Cost
—— Square Root Fit
0
5
10
15
20
Des,
Order Size ($ millions)
Figure 16.1
which can provide more dynamic and accurate estimates.’ They
can also provide more industrial-strength estimates: As we have
seen, pure empirical approaches face many problems as a result of
poor data quality; poor coverage, especially of illiquid and new
assets; and poor timeliness. A structural attack can separate out
easier-to-measure elements, facilitate extensions to all assets, benefit
from cross-sectional estimation, impose reasonable behavior, and
generally limit problems.
The inventory risk approach suggests a certain structure. It
depends on a forecast of inventory risk and an estimate of the
liquidity supplier’s charge per unit of risk.
Chapter 3 presented structural models of risk. A structural
model of inventory risk involves an estimate of asset risk and also
estimates of the time to clear. To estimate both these quantities, the
7See BARRA (1997).
454
Implementation
market impact model developed by BARRA relies on submodels
to estimate asset volatility, trading volume and intensity (trade size
and trade frequency), and elasticity.
By separating out each component, the BARRA model can
apply appropriate insight and technology. We may have difficulty
discerning patterns within the tick-by-tick market impact data. But
we can apply our previous understanding of structural risk models
to estimate asset risk. We can apply insights into trading volume
and intensity which often hold across most stocks. For example,
all stock trading exhibits higher volume at the open and close, and
low volume in the vicinity of certain holidays.
Elasticity captures the dependence of buy versus sell orders
on price. Imagine that a liquidity supplier fills a large sell order
and demands a price concession. The trade price moves below the
bid, and the supplier’s inventory now has a positive position. But
the low price will attract other buyers. Elasticity measures how the
number of buyers versus sellers changes as we move away from
an equilibrium price.
The BARRA market impact model uses the distribution of
trade frequency, trade size, and elasticity to estimate time to clear,
given any particular desired trade size. This time to clear, combined
with estimated risk, leads to the inventory risk forecast. The final
step uses a liquidity supplier’s price of risk to convert inventory
risk into an expected price concession. The BARRA model estimates
this price of risk separately for buy orders and sell orders, and for
exchange-traded and over-the-counter stocks.
As well as developing their model, BARRA researchers have
also developed latent-variables methods for testing the accuracy
of such models, given the problems with tick-by-tick data. For
details, see BARRA (1997).
»
TURNOVER, TRANSACTIONS COSTS, AND
VALUE ADDED
We now wish to go beyond the simple observation that transactions
costs drag down performance, to see how much value added we can
retain if we limit a strategy’s turnover. We’ve all heard about the ex-
tremely promising strategy that unfortunately requires 80 percent
turnover per month. Don’t dismiss that policy out of hand. We may
Transactions Costs, Turnover, and Trading
455
a
a ne
cee er
ee
be able to add considerable value with the strategy if we restrict turn-
over to 40 percent, 20 percent, or even 10 percent per month.
We shall build a simple framework for analyzing the effects
of transactions costs and turnover to help us understand the trade-
off between value added and turnover. This framework will provide
a lower bound on the amount of value added achievable with
limited turnover, and also clarify the link between transactions
costs and turnover. It will also provide a powerful argument for
the importance of accurately distinguishing stocks based on their
transactions costs.
For any portfolio P, consider value added
VAp — Opes Na : We
(16.5)
where Wp is the portfolio’s active risk relative to the benchmark B.
The manager starts with an initial portfolio J that has value added
VA;. We will limit the portfolios that we can choose to a choice set*
CS. Portfolio Q is the portfolio in CS with the highest possible
value added. We will assume for now that portfolio I is also in CS,
but later relax that assumption. The increase in value added as we
move from portfolio I to portfolio Q is
Now let TOp represent the amount of turnover needed to
move from portfolio I to portfolio P. As a preliminary, let us define
turnover, since there are several possible choices. If hp is the initial
portfolio and hj is the revised portfolio, then the purchase turn-
over is
TOp = S) Max{0,Af, — hon}
(16.7)
n
and the sales turnover is
TOs = 5) Max(0,hp,, — hi}
(16.8)
n
These purchase and sales turnover statistics do not include changes
8We are allowing for constraints that limit our choices, such as full investment in risky
assets, portfolio beta equal to 1, no short sales, etc. The choice set CS is restricted
to be closed and convex. We will consider two cases explicitly: CS defined by
equality constraints and CS defined by inequality constraints.
456
Implementation
ee
ee
VAg
Value
Added
VA,
0
TO teers
TOg
Turmover
Figure 16.2
in cash position. One reasonable definition of turnover, which we
will adopt, is
TO = Min{TO,,TOs}
(16.9)
Turnover is the minimum of purchase and sales turnover. With no
change in cash position, purchase turnover will equal sales turn-
over. This turnover definition accommodates contributions and
withdrawals by not including them in the turnover formula.
The turnover required to move from portfolio I to portfolio
Q is TOg. If we restrict turnover to be less than TOg, we will be
giving up some value added in order to reduce cost. Let VA(TO)
be the maximum amount of value added if turnover is less than
or equal to TO. Figure 16.2 shows a typical situation. The frontier
VA(TO) increases from VA; to VAg. The concave’ shape of the curve
*The concavity of VA(TO) follows from the value added function’s being concave in the
holdings hp, the turnover function’s being convex in hp, and the choice set CS’s
being convex. The fact that VA(TO) is nondecreasing follows from common sense;
ie., a larger amount of turnover will let you do at least as well. The frontier will
be made up of quadratic segments (piecewise quadratic) when.the choice set is
described by linear inequalities.
Transactions Costs, Turnover, and Trading
457
Ee
a re
2
"4
indicates a decreasing marginal return for each additional amount
of turnover that we allow.
A Lower Bound
As the technical appendix will show in detail, when we assume
that CS is defined by linear equality constraints (e.g., constraining
the level of cash or the portfolio beta to equal specific targets) and
includes portfolio I, we can obtain a quadratic lower bound on
potential value added:
iv pic) : pe)
TOg
TOg
Underlying this result is a very simple strategy, prorating a fraction
TO/TOg of each trade needed to move from the initial portfolio I to
the optimal portfolio Q. This strategy leads toa portfolio that is in CS,
has turnover equal to TO, and meets the lower bound in Eq. (16.10).
We can express the sentiment of Eq. (16.10) in the value added/
turnover rule of thumb:
VA(TO) 2 VA; + AVAg :
(16.10)
You can achieve at least 75 percent of the (incremental) value added
with 50 percent of the turnover.
This result sounds even better in terms of an effective informa-
tion ratio, since the value added is proportional to the square of the
information ratio (at optimality). It implies that a strategy can retain
at least 87 percent of its information ratio with half the turnover."”
The Value of Scheduling Trades
We can exceed the lower bound in Eq. (16.10) by judicious schedul-
ing of trades, executing the most attractive opportunities first. For
example, suppose there are only four assets. As we move from
portfolio I to portfolio Q, we purchase 10 percent in assets 1 and
“The implication is loose for two reasons. First, we derived the relationship between
value added and information ratio at optimality, assuming no constraints (e.g., on
turnover). Second, in this chapter we have derived a relationship between
turnover and incremental value added.
458
Implementation
8
a
ee se
ee
Value
Added
0
CO seeserna
TO Q
Tumover
Figure 16.3
2 and sell 10 percent of our holdings in assets 3 and 4. Turnover
is 20 percent. Suppose the alphas for the four assets are 5 percent,
3 percent, —3 percent, and —5 percent, respectively. Then buying
1 and selling 4 has a bigger impact on alpha than swapping 2 for
3. If we have restricted turnover to 10 percent, we could make an
8 percent trade of stock 1 for stock 4 and a 2 percent trade of 2 for
3 rather than doing 5 percent in each trade.
Figure 16.3 illustrates the situation. The solid line shows the
frontier; the dotted line shows the lower bound. The maximum
opportunity for exceeding the bound occurs for turnover some-
where between 0 and 100 percent of TOp.
Transactions Costs
The simplest assumption we can make about transactions costs is
that round-trip costs are the same for all assets. Let TC be that level
of costs. We wish to choose a portfolio P in CS that will maximize
NAp eal
GuslO,
(16.11)
Figure 16.4 illustrates the solution to this problem. Let SLOPE(TO)
represent the slope of the value-added /turnover frontier when the
Transactions Costs, Turnover, and Trading
459
a
eee
ee
eee
<= > re)
Value
Added
VA |
iO aaa
gel:
To.
Turnover
Figure 16.4
level of turnover is TO. Since the frontier is increasing and concave,
SLOPE(TO) is positive and decreasing. The incremental gain from
each additional amount of turnover is decreasing, so the slope of
the frontier SLOPE(TO) will decrease to zero as TO increases to
TO g. SLOPE(TO) represents the marginal gain in value added from
additional transactions, and TC represents the marginal cost of
additional transactions. The optimal level of turnover will occur
where marginal cost equals marginal value added, i.e., where
SLOPE(TO*) = TC.
As long as the transactions cost is positive and less than
SLOPE(0), we
can
find
a level of turnover TO* such
that
SLOPE(TO*)
= TC. If TC > SLOPE(0), it is not worthwhile to
transact at all, and the best solution is to stick with portfolio I.
Implied Transactions Costs
The slope of the value-added/turnover frontier can be interpreted
as a transactions cost. We can reverse the logic and link any level
460
Implementation
of turnover to a transactions cost; e.g., a turnover level of 20 percent
corresponds to a round-trip transactions cost of 2.46 percent.
Transactions costs contain observable components, such as
commissions and spreads, as well as the unobservable market im-
pact. Because managers cannot be sure that they have a precise
measure of transactions costs, they will often seek to control those
costs by establishing an ad hoc policy such as “no more than 20
percent turnover per quarter.” The insight that relates the slope of
the value-added /turnover frontier to the level of transactions costs
provides an opportunity to analyze that cost control policy. One
can fix the level of turnover at the required level TOg and then
find the slope, SLOPE(TO,), of the frontier at TO. Our ad hoc
policy is consistent with an assumption that the general level of
round-trip transactions costs is equal to SLOPE(TO,). If we have
a notion that round-trip costs are around 2 percent, and we find
that SLOPE(TOx) is about 4.5 percent, then something is awry.
We can make three possible adjustments to get things back into
harmony. One, we can increase our estimate of the round-trip costs
from 2 percent. Two, we can increase the allowed level of turnover
TOg, since we are giving up more marginal value added (4.5 percent)
than it is costing us to trade (2.0 percent). Three, we can reduce
our estimates of our ability to add value by scaling our alphas back
toward zero. A combination of these adjustments—a little give from
all sides—would be fine as well. This type of analysis serves as a
reality check on our policy and the overall investment process.
An Example
Consider the following example, using the S&P 100 stocks asa starting
universe and the S&P 100 as the benchmark. We generated alphas"
for the 100 stocks, centering and scaling so that they were benchmark-
neutral, and also so that portfolio Q would have an alpha of 3.2 percent
and an active risk of 4 percent when we used \, = 0.1. The initial
portfolio contained 20 randomly chosen stocks, equal-weighted, with
an alpha of 0.07 percent and an active risk of 5.29 percent, typical of a
situation when a manager takes over an existing account.
"We produced 100 samples from the standard normal distribution.
Transactions Costs, Turnover, and Trading
461
A
A
a
ee
ee A
TABLE
16.1
SS SE
ee ee ee
a
ee ae ee
Value Added
Mi
a
I
Implied
Percentage
Lower
Perceniage
Transactions
of TO,
Bound
Excess
Total
of VAg
Cost
0.0
—2.73
0.00
S23
0.0%
10.0
OW
0.87
—1.03
39.2%
8.66%
20.0
etl dh
1.00
—0.18
59.0%
5.12%
30.0
\0ey2
0.88
0.36
71.4%
3.40%
40.0
0.04
0.70
0.74
80.2%
2.50%
50.0
0.52
0.51
1.03
86.8%
1.90%
60.0
0.91
0.34
1.24
91.8%
1.43%
70.0
eal
0.19
1.40
95.5%
1.02%
80.0
1.43
0.09
1.511
98.0%
0.67%
90.0
1.56
0.02
1.58
99.5%
0.33%
100.0
1.60
0.00
1.60
100.0%
0.00%
Table 16.1 displays the results, including the value added sepa-
rated into two parts: the lower bound and the excess above the
bound. The excess is the benefit we get from scheduling the best
trades first. Table 16.1 also displays the implied transactions costs.
We see that reasonable levels of round-trip costs (about 2 percent)
do not call for large amounts of turnover, and that very low or
high restrictions on turnover correspond to unrealistic levels of
transactions costs.
Note that the value of being able to pick off the best trades
(the difference between the lower bound and the actual fraction of
value added) is largest when turnover is 20 percent of the level
required to move to portfolio Q. In this case, the rule of thumb is
conservative: We achieve 87 percent of the value-added for 50
percent of the turnover.”
“Jt is possible to make up a two-stock example where the lower bound on the frontier
would be exact. Common sense indicates that with more stocks and a reasonable
distribution of alphas, there is considerable room to add value by plucking the
best opportunities.
462
Implementation
Generalizing the Result
We made three assumptions in deriving these results: (1) the initial
portfolio was in CS, (2) CS was described by linear equalities, and
(3) all round-trip transactions costs are the same. We will reconsider
these in turn.
If portfolio I is not in the choice set, then we can think of
the portfolio construction problem as being a two-step process. In
step 1, we find the portfolio J in the choice set such that the
turnover in moving from portfolio I to portfolio J is minimal. The
value added in moving’ from portfolio I to portfolio J is not a
consideration, so we may have VA; = VA, or VA; < VAj. The turn-
over required to move from I to J is TO). The lower bound in Eq.
(16.10) will still apply, although we start from portfolio J rather
than portfolio I.
This situation can demonstrate the costs of adding constraints.
What if portfolio I were not in CS, and we were limiting turnover
to 10 percent per month? If the first 4 percent of the turnover is
required to move the portfolio back into the choice set, then we
have only 6 percent to take advantage of our new alphas.
If the choice set CS is described by inequality constraints, such
as a restriction on short selling and upper limits on the individual
asset holdings, then the analysis becomes more complicated. How-
ever, the value-added /turnover frontier VA(TO) will have the same
increasing and concave slope that we see in Fig. 16.2. There will
be a quadratic lower bound on VA(TO); however, that lower bound"*
is not as strong as the lower bound we obtain in the case with only
equality constraints. You are not guaranteed three-quarters of the
value added for one-half the turnover. Nevertheless, in our experi-
ence, 75 percent is still a reasonable lower bound.
So far, we have made the assumption that all round-trip trans-
actions costs are the same. It is good news for the portfolio manager
if the transactions costs differ (and she or he can forecast the differ-
ence). Recall that the difference between the lower bound and
the value-added/turnover frontier stemmed from our ability to
"In a formal sense we are defining VAp = ap — Aq - Wh if P © CS and VAp = —~ if
PE
CS. This means that VA(TO) = — if TO < TO).
.
“See the appendix for justification.
Transactions Costs, Turnover, and Trading
463
adroitly schedule the most value-enhancing trades first. Our ability
to discriminate adds value. Differences in transactions costs further
enhance our ability to discriminate.
We have analyzed this effect in our example. We began with
the implied transactions costs at 1.90 percent for 50 percent of TOg.
We then set the transactions costs to 75 percent of that, or 1.42
percent, for half of the stocks, and raised the transactions costs for
the other stocks to 2.26 percent, so that transactions costs remained
constant at 50 percent of TOg. Taking into account these differing
costs when optimizing barely affected portfolio alphas or risk, but
did reduce transactions costs by about 30 percent.
Accurate forecasts of the cost of trading can generate significant
savings when used as part of the portfolio rebalancing process.
The better our model of transactions costs, the better our ability
to discriminate among stocks. In the example above, we distin-
guished stocks by their linear costs. More elaborate models can
distinguish them on the basis of more accurate, dynamic, and non-
linear costs.
Clearly we have seen promise in the approach of lowering
transactions costs by lowering turnover while retaining much of
the value added. Naive versions of this can preserve 75 percent of
the value added with 50 percent of the turnover, and clever versions,
utilizing differences in asset alphas and asset transactions costs,
can well exceed the naive result. We now move on to a second
approach to reducing transactions costs: optimal trading.
TRADING AS A PORTFOLIO
OPTIMIZATION PROBLEM
Trading is a portfolio optimization problem, but not the portfolio
construction problem we have discussed at length. Imagine that you
have already completed the portfolio construction (or rebalancing)
problem. You own a current portfolio, and you desire the output
from the portfolio construction problem. You trade to move from
your current portfolio to your desired portfolio. Scheduling these
trades—what stock to trade first, second, etc.—over an allowed
464
Implementation
trading period is a portfolio optimization problem. The goal is to
maximize trading utility:
Utility = (Chive Ns
Wenerr — MI
(16.12)
defined as short-term alpha minus a short-term risk adjustment,
minus market impact. This trading utility function swaps reduced
market impact for increased short-term risk. We distinguish short-
term alphas and risk from investment-horizon alphas and risk (dis-
cussed elsewhere in this book), because stock returns over hourly
or daily horizons often behave quite differently from stock returns
over monthly or quarterly horizons.
In portfolio construction, the goal is a target portfolio. In trad-
ing, the goal is a set of intermediate portfolios held at different
times, starting with the current portfolio now, and ending with the
target portfolio a short time later.
The benchmark for trading is immediate execution, and we
measure return and risk relative to that benchmark in Eq. (16.12).
The problem with quick execution, as discussed earlier, is that it
increases market impact. Market impact costs increase with trade
volume and speed.
What's the intuition about how risk, market impact, and alphas
will affect trade scheduling? Risk considerations should keep the
trade schedule close to the benchmark, i.e., push for quick execu-
tion. Market-impact considerations will tend to lead to even spacing
of trades. Alphas will push for early or late execution.
An Example
The details of how to implement this optimal trading process—for
example, how to model market impact as a function of how: fast
you trade—are beyond both the scope of this book and the state
of the art of the investment management industry. However, it’s
useful to present a very simple example of the idea. Even this
simple example, though, involves sophisticated mathematics that
is relegated to the technical appendix.
Consider the trading process at its most basic: You have cash,
and you want to buy one stock. You think the stock will go up.
You want to buy soon, before the stock rises. But to avoid market
Transactions Costs, Turnover, and Trading
465
es
Seg re
ee
impact, you are willing to be patient and assume some risk of
missing the stock rise. What is your optimal trading strategy?
Here are the details. Start with cash amount M. After T days,
you want to be fully invested in stock S, with expected return f
and risk o. The benchmark is immediate execution.
We need to quantify the return, risk, and transactions costs
for the implemented portfolio relative to the benchmark. For this
simple example, we can completely characterize the implemented
portfolio at time t by the fractional holding of the stock h(t). Assume
that you can trade at any time and at any speed, so long as you
are fully invested by day T. We then seek the optimal h(t) at each
time over the next T days. The cash position of the implemented
portfolio is simply 1 — h(t). The active portfolio stock position
relative to the benchmark is h(t) — 1, since the benchmark is fully
invested. The implemented portfolio will have h(0) = 0 and
h(T) = 1. Initially the portfolio is entirely cash, and at the end of
T days the portfolio is fully invested in stock S.
Over the next T days, the cumulative portfolio active return
will be -
ip
Qshort = [
ay. [h(t) — 1]}
(16.13)
0
This integrates (or sums up) the active return over each small period
dt to calculate the total active return over the period of T days.
Similarly, the cumulative active risk of the implemented port-
folio will be
T
Nee |
atte ACR a ho
(16.14)
0
Once again, this cumulative active risk integrates (or sums up)
active risk contributions over each period dt of the full T-day trading
period. This active risk involves the active portfolio position and
the stock return risk.
Finally, we must treat cumulative transactions costs. For the
example, we will focus specifically on market impact, the only
466
Implementation
interesting transactions costs in terms of influence on trading strat-
egy.'° We will model the cumulative active market impact as
T
MI = |
dt{c - h*()}
(16.15)
0
with
Ove a“
(16.16)
Equation (16.15) models market impact as simply proportional to
the square of the stock accumulation rate. The faster the portfolio
holding changes, the larger the market impact.
This simple model ignores any memory effects—a big assump-
tion, but only if trades are a significant fraction of daily volume.
According to this, the market doesn’t remember what you traded
yesterday, it just sees what you are trading this instant. Still, the
total market impact over the T-day trading period is the integral
(or sum) of the market impact over each subperiod df.
The technical appendix describes how to analytically solve for
the h(t) which maximizes Eq. (16.12). Here we will illustrate a
graphical solution for different parameter choices. Three different
elements influence the solution: return, risk, and market impact.
We are looking at short horizons, and typically the risk and market
impact components will dominate the expected returns compo-
nents.'° Assuming that the expected return is small, we still have
two distinct cases: risk aversion dominates market impact, and
market impact dominates risk. Figure 16.5 illustrates these two
cases, using T = 5 days. When market impact dominates risk aver-
sion, the optimal schedule is to evenly space trades, even though the
benchmark is immediate execution. When risk dominates market
impact, the optimal schedule will closely track the immediate execu-
tion benchmark. Within two days (40 percent of the period), the
portfolio’s stock position reaches 75 percent of its target.
We can include other transactions costs (commissions and taxes) in our forecasts of
stock returns, but they will not influence our trade schedule, since they are the
same, no matter what the schedule.
“Risk scales with the square root of time, while expected return scales linearly with time.
As the period shrinks, risk will increasingly dominate return.
Transactions Costs, Turnover, and Trading
467
a
hs
y
=
a
So
=x
ad
g
a
Market Impact Dominates
Risk Aversion Dominates
0
0.5
1
eS
2
eS
3
35
4
4.5
5
Time in Days
Figure 16.5
TRADE IMPLEMENTATION
After devising a trading strategy, either through the optimization
described above or through some more ad hoc approach, the next
step is actual trading. You can implement trades as market orders
or as limit orders.”
Market orders are orders to trade a certain volume at the
current market’s best price. Limit orders are orders to trade a certain
volume at a certain price. Limit orders trade off price impact against
certainty of execution. Market orders can significantly move prices,
but they will execute. Limit orders will execute at the limit price,
if they execute (they may not).
"The choices for trade implementation are actually much more numerous. They include
crossing networks, alternative stock exchanges, and principal bid transactions.
Treatment of these alternatives lies beyond the scope of this book.
468
Implementation
There is a current debate over the value of using limit orders
in trading. Many argue that placing limit orders provides free
options to the marketplace. For example, placing a limit order to
buy at a price P constitutes offering to buy the stock at P, even if
the stock is rapidly moving to 80 percent of P. Your only protection
is the ability to cancel the order as the price begins to move.
Trading portfolios of limit orders has additional problems. For
example, in a large market move, all the sell limit orders may
execute while none of the buy orders execute. This will add market
risk to the portfolio.
Given these concerns about limit orders, plus the typical port-
folio manager’s eagerness to complete the trades (implement the
new alphas), the general rule is to use limit orders sparingly, mainly
for the stocks with the highest anticipated market impact, and with
limit prices set very close to the existing market prices.
The opposite side of the debate is that limit orders let value
managers sell liquidity and earn the liquidity provider’s profit.
The appropriate order type may depend on the manager’s style.
SUMMARY
We have discussed transactions costs, turnover, and trading, with
a strategic focus on reducing the impact of transactions costs on
performance. After discussing the origins of transactions costs and
how they rise with trade volume and urgency, we focused on the
question of analyzing and estimating transactions costs. This is
difficult because measuring transactions costs is difficult, but it can
significantly affect realized value added, as the rest of the chapter
discussed. The most accurate analysis of transactions costs uses
the implementation shortfall: comparing the actual portfolio with
a paper portfolio implemented with no transactions costs.
4.
We discussed the inventory risk approach to modeling market
impact. This leads to behavior matching market observations, espe-
cially the dependence of price impact on the square root of volume
traded. It also leads to practical forecasts of market impact, ranging
from the fairly simple to the more complex structural market im-
pact models.
One approach to reducing transactions costs is to reduce turn-
over while retaining value added. We developed a lower bound
Transactions Costs, Turnover, and Trading
469
eee eae ie
ee ee Sue tO eS Sane re
ee
ee
on value added as a function of turnover, and verified the rule of
thumb that restricting turnover to one-half the level of turnover if
there is no restriction on turnover will result in at least three-
quarters of the value added. We can exceed that bound through
our ability to skim off the most valuable trades first, and by account-
ing for differences in transactions costs between stocks. We also
saw that the slope of the value-added/turnover frontier implies a
level of round-trip transactions costs.
We then looked at the trading process directly, to see that
trading itself is a portfolio optimization problem, distinct from
portfolio construction. Optimal trading can reduce transactions
costs, trading reduced market impact for additional short-term risk.
Choices for trade implementation include market orders and limit
orders. The disadvantages of limit orders make them most appro-
priate for the highest market impact stocks, with limit prices close
to market prices.
PROBLEMS
1. Imagine that you are a stock trader, and that a portfolio
manager plans to measure your trading prowess by
comparing your execution prices with volume-weighted
average prices. How would you attempt to look as good
as possible by this measure? Would this always coincide
with the best interests of the manager?
2. Why is it more difficult to beat the bound in Eq. (16.10)
with a portfolio of only 2 stocks than with a portfolio of
100 stocks?
3. A strategy can achieve 200 basis points of value added
with 200 percent annual turnover. How much value-
added should it achieve with 100 percent annual
turnover? How much turnover is required in order to
achieve 100 basis points of value added?
4. How would the presence of memory effects in market
impact change the trade optimization results displayed
in Fig. 16.5?
5. In Fig. 16.5, why does high risk aversion lead to quick
trading?
470
Implementation
REFERENCES
Angel, James J., Gary L. Gastineau, and Clifford J. Webber. “Reducing the Market
Impact of Large Stock Trades.” Journal of Portfolio Management, vol. 24, no.
1). 19977 pp: 69=/6:
Atkins, Allen B., and Edward A. Dyl. “Transactions Costs and Holding Periods
for Common Stocks.” Journal of Finance, vol. 52, no. 1, 1997, pp. 309-325.
BARRA, Market Impact Model Handbook (Berkeley, Calif.: BARRA, 1997).
Chan, Louis K. C., and Josef Lakonishok. “The Behavior of Stock Prices around
Institutional Trades.” Journal of Finance, vol. 50, no. 4, 1995, pp. 1147-1174.
. “Institutional Equity Trading Costs: NYSE versus NASDAQ.” Journal of
Finance, vol. 52, no. 2, 1997, pp. 713-735.
Ellis, Charles D. “The Loser’s Game.” Financial Analysts Journal, vol. 31, no. 4,
IO7OR Pp alI=20.
Grinold, Richard C., and Mark Stuckelman. “The Value-Added/Turnover Fron-
tier.” Journal of Portfolio Management, vol. 19, no. 4, 1993, pp. 8-17.
Handa, Puneet, and Robert A. Schwartz. “Limit Order Trading.” Journal of Finance,
vol. 51, no. 5, 1996; pp. 1835-1861.
Kahn, Ronald N. “How the Execution of Trades Is Best Operationalized.” In
Execution Techniques, True Trading Costs, and the Microstructure of Markets,
edited by Katrina F. Sherrerd (Charlottesville, Va.: AIMR 1993).
Keim, Donald B., and Ananth Madhavan. “The Cost of Institutional Equity
Trades.” Financial Analysts Journal, vol. 54, no. 4, 1998, pp. 50-69.
Lakonishok, Josef, Andre Shleifer, and Robert W. Vishny. “Study of U.S. Equity
Money Manager Performance.” Brookings Institute Study, 1992.
Loeb, Thomas F. “Trading Costs: The Critical Link between Investment Informa-
tion and Results.” Financial Analysts Journal, vol. 39, no. 3, 1983, pp. 39-44.
Malkiel, Burton. “Returns from Investing in Equity Mutual Funds 1971 to 1991.”
Journal of Finance, vol. 50, no. 2, 1995, pp. 549-572.
Modest, David. “What Have We Learned about Trading Costs? An Empirical
Retrospective.” Berkeley Program in Finance Seminar, March 1993.
Perold, Andre. “The Implementation Shortfall: Paper versus Reality.” Journal of
Portfolio Management, vol 14, no. 3, 1988, pp. 4-9.
Pogue, G. A. “An Extension of the Markowitz Portfolio Selection Model to Include
Variable Transactions Costs, Short Sales, Leverage Policies and Taxes.” Jour-
nal of Finance, vol. 45, no. 5, 1970, pp. 1005-1027.
Rudd, Andrew, and Barr Rosenberg.. “Realistic Portfolio Optimization.” In Pdrtfolio
Theory—Studies in Management Science, vol. 11, edited by E. J. Elton and M.
J. Gruber (Amsterdam: North Holland Press, 1979).
Schreiner, J. “Portfolio Revision: A Turnover-Constrained Approach.” Financial
Management, vol. 9, no. 1, 1980, pp. 67-75.
Treynor, Jack L. “The Only Game in Town.” Financial Analysts Journal, vol. 27, no.
ZAG, DP wlan:
. “Types and Motivations of Market Participants.” In Execution Techniques,
True Trading Costs, and the Microstructure of Markets, edited by Katrina F.
Sherrerd (Charlottesville, Va.: AIMR, 1993).
Transactions Costs, Turnover, and Trading
471
a
aaa a
a de
BE
ee ee ee
. “The Invisible Costs of Trading.” Journal of Portfolio Management, vol. 21,
no. 1, 1994, pp. 71-78.
Wagner, Wayne H. (Ed.). A Complete Guide to Securities Transactions: Controlling
Costs and Enhancing Performance (New York: Wiley, 1988).
. “Defining and Measuring Trading Costs.” In Execution Techniques, True
Trading Costs, and the Microstructure of Markets, edited by Katrina F. Sherrerd
(Charlottesville, Va.: AIMR, 1993).
Wagner, Wayne H., and Michael Banks. “Increasing Portfolio Effectiveness via
Transaction Cost Management.” Journal of Portfolio Management, vol. 19, no.
1, 1992, pp. 6-11.
Wagner, Wayne H., and Evan Schulman. “Passive Trading: Point and Counter-
point.” Journal of Portfolio Management, vol. 20, no. 3, 1994, pp. 25-29.
TECHNICAL APPENDIX
This technical appendix will cover two topics: the bound on value
added versus turnover, and the solution to the example trading
optimization problem.
We begin by proving the bound on value added versus turn-
over for the cases of linear inequality and equality constraints. Eq.
(16.10) corresponds exactly to the case of linear equality constraints.
Inequality Case, CS = {h|A: h < b}
Portfolio Q is optimal for the problem Max{VA;|hp € CS}. This
means that we can find nonnegative Lagrange multipliers m = 0
such that
a= 2° 4° Ve (ho —hy) — Al a =0
a=0
(16A.1)
and
A-hg=b-~
@w'-A-hg=a"-b
(16A.2)
Since h,; € CS, we have b —
A: h, = 0 and am 2 0, so
a-(b-A-:h)=kx2=0
or
w:A:h=7':-b-«
(16A.3)
If we premultiply Eq. (16A.1) by (h; — hg) and use Eqs. (16A.2)
and (16A.3), we find that
472
Implementation
Now consider the family of solutions as we move directly from
portfolio I to portfolio Q:
=h,— (1-8): hy
where we have introduced the trade portfolio hy These solutions
are all in CS as long as 0 = 8 = 1. The solutions have value added
VA{3} = ag + (1 — 8): (a — ag)
(16A.6)
Nai geo ie) ath
Weyer
ip ite CeO) re
where or is the risk of hz If we use Eq. (16A.4), then Eq. (16A.6)
simplifies to
VA{8} = VAg —.(1 = 8) + kK — Ay> 1 = 5)
07%. . (16A-7)
Since VA(0) = VA,;, VA(1) = VAg, and AVAy = VAg — VA; we have
k = AVAyg — Ay: 07 = 0
(16A.8)
Thus Eg. (16A.7) simplifies further to
VA{8} = VA, + AVAG? 2:34 ~ 9 = be 8°)
(16A.9)
where
A= Aa or t+ k/2 =
(16A.10)
Nac or tk”
and
eS eS
(16A.11)
Y one
FE
The slope of VA(8), Eq. (16A.9), is 2 - AVAg : (a — b - 8), which is
positive for 0 = 6 < 1 and decreases to x as 8 approaches 1.
Equality Case, CS = {hi|A- h = b}
The analysis is as before, except that m in Eq. (16A.1) is unrestricted
in sign. Therefore k = 0 and, from Eq. (16A.8), AVAg = 4° 0}.
Thus Eq. (16A.9) simplifies to
VA (=, VA;
WAVAS SID 5 eieeha
(164.12)
Transactions Costs, Turnover, and Trading
473
Trade Optimization
We will now describe how to solve analytically for the trading
strategy h(t) which maximizes utility in the simple example
Utility = Qshort
Xs . Wrrort — MI
(16A.13)
Schematically, we can represent the utility as
30
Ue i
dt - u(h,h)
(16A.14)
0
At the optimal ee the variation of this utility will be zero:
ou fa
1%
dh + afi
% sid =
0
(16A.15)
Integrating the second term by parts (and remembering that the
variation is zero at the utes endpoints of the integral),
du = Jo
\m-
5, < (%) hen
= 0
(16A.16)
Thus we can maximize U by choosing h(t) which satisfies
cae (%4 270
(16A.17)
Applying this to the particular utility function [Eq. (16A.13)], the
portfolio holding must satisfy the second-order ordinary differen-
tial equation
f-2-ds-o?-(h-1)+2-c-h=0
(16A.18)
plus the boundary conditions h(0) = 0 and A(T) = 1. Defining
relative parameters
om af
(164.19)
DOE
ua IN o
ga
(16A.20)
474
Implementation
and rearranging terms, Eq. (16A.18) becomes
h-¢g-h=-s-¢
(16A.21)
Applying standard mathematical techniques to Eq. (16A.21),
we find that the optimal solution h(f) is
oe: + (6/2) cosh)
Mee
sinh(g - T)
- sinh(g - £)(16A.22)
— (1
+5)
- [cosh(g
: t) — 1]
We can characterize various regimes for the solution h(t) by
looking at some dimensionless quantities which enter into the opti-
mal h(t):
2
Ns . co C tte
(Wed OE a eae
(16A.23)
R1. (g : T)’ >> 1. Risk aversion dominates over market
impact.
R2. (g - T)’ << 1. Market impact dominates over risk
aversion.
s+ T? =
(16A.24)
R3. s - T*? >> 1. Alpha is positive and dominant over
market impact.
R4.s
- T? << —1. Alpha is negative and dominant over
market impact.
Sch eo
Ce
D y Ns : o
RS. |s/g’| >> 1. Alpha (positive or negative) dominates risk
aversion.
R6. |s/g’| << 1. Risk aversion dominates over alpha.
(16A.25)
If we assume that the alpha is zero, so that the coefficient
s = 0 above, then it’s interesting to see the limiting behavior of Eq.
(16A.22) in regimes R1 and R2. When market impact dominates
Transactions Costs, Turnover, and Trading
475
over risk, h(t) follows a straight-line path from 0 to 1. The result
is uniform trading. If, on the other hand, risk dominates over market
impact, h(t) exponentially approaches 1:
hE)
1S Expl
=o
(16A.26)
Exercise
1. Assuming zero alpha, derive the limit of Eq. (16A.22)
when market impact dominates over risk. Also show
that in the limit that risk dominates over market impact,
the optimal trade schedule reduces to an exponential, as
in Eq. (16A.26).
Applications Exercises
Use alphas from a residual reversal model to build an optimal
portfolio of MMI stocks. The initial portfolio is the MMI, and the
benchmark is the CAPMMI. Use a risk aversion of 0.075 and the
typical institutional constraints: full investment, no short sales.
1. What is the value added of the MMI? What is the value
added of the optimal portfolio? What is the incremental
value added?
2. What is the turnover in moving from the MMI to the
optimal portfolio?
3. Now build a portfolio exactly halfway between the MMI
and the optimal portfolio:
hp =
hymn a Noptimal
2
What is the turnover in moving from the MMI to this in-
termediate portfolio? What is its value added? Compare
the incremental value added of this portfolio over the
MMI to that of the optimal portfolio over the MMI. Verify
Eg. (16.10).
iy
ij
ff
headend
Wii a)
isbern
Iereum §
= swaths
47
Ay! hs
(PAL
etl Galo
Va!
ou
gett oh
tk
is get pel lebanese net:
uf (ovO gatas ger , pea aj)" artic: geltisra al anit ae
ed aertegtyh didveneien:
ah it te als , he
is
:
7
OTR ee 9
)
4 Nat) +t 7
iii 43]
.
navel =
iv yi oyas.
«:
enaneu
Ee
wantin
CAL! Asie Gey wa hs ols Pugtrc hadi sik. -
sacutt
ed
vath
tote)
ears! jer xy Amt Jail "ree pat ni ‘piss
TMM Lees: eer ete
th pcre lt est
ih! tees) lemmtigo anit
Oh AEl fe af
Tes
ee
Vee
%
r tie alia a
a
eenioy 5x3 2 utente! , it
ie
ee ted) ya
liv
Betee
ONE odd
AF oe Ree pane I
Ya
Ad
ty
WAP ED | n en -* wen 6 oa A
#
oui al
il
ft
pid \ oF. al
eo
tea
7
Wha
red Gee ASTM
ent We sini onlay ans a nif
HRV
Vet “ary? 4 ae
kt RS a
oT
em
]
4
Ml adi mod
& vec Serene ota
; —
I
z. Tt)
£2
ae,
ie
ger
ine Vite.
wil. aye
eye
ie : oe ee wae
’ ra
‘
a
ia.
9
’
tag
veal panies Det
re)
isytta D> Sh on VOLOV ate t
m4
5
oe
@ oontont Soi
i - Gee, he ih spk aol
ee
ne ea ee
>
~,
Be rapes Cred Meee
