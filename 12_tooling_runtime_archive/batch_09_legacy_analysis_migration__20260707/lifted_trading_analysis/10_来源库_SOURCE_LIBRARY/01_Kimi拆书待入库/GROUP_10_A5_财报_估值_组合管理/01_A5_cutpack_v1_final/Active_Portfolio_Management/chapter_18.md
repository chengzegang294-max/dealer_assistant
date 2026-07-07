# Chapter 18: Asset Allocation

- **book_name**: Active Portfolio Management
- **main_source**: pdf
- **cross_check_source**: none
- **pdf_role**: main_text_source
- **split_scope**: pages 539-562

---

CHAPTER
18
Asset Allocation
INTRODUCTION
In Chap. 4 we developed a utility function for active management
which separated benchmark timing from asset selection. The in-
tervening chapters have focused on asset selection, postponing
treatment of benchmark timing to Chap. 19. Before moving on to
that treatment, we want to focus separately on a style of invest-
ment—asset allocation—which lies somewhere between asset selec-
tion and benchmark timing.
Asset allocation comes in several varieties: strategic versus
tactical, and domestic versus global. The process of selecting a target
asset allocation is called strategic asset allocation. The variation in asset
allocation around that target is called tactical asset allocation. There
is an analogy between strategic asset allocation and the choice of
a benchmark in a single equity market, and between tactical asset
allocation and active management within the equity market. We
do not address the important question of strategic asset allocation
in this book.' We assume that we have simply been presented with
the benchmark.
This chapter explicitly addresses tactical asset allocation. Do-
mestic tactical asset allocation typically involves actively choosing
allocations to at least three asset classes—stocks, bonds, and cash—
‘For a discussion of strategic asset allocation issues, see Ambachtsheer (1987) or Sharpe
(1987).
517
518
Implementation
and possibly more. Global asset allocation involves actively choos-
ing allocations to typically 20 or so global equity and bond markets.
The principles for actively managing asset selection in one
market apply to tactical asset allocation. The main difference is in
the number of assets. There are typically from 3 to 20 in tactical
asset allocation and from 100 to several thousand for portfolio
management in a single market. Given this important difference,
the fundamental law of active management implies that tactical
asset allocation will have to surmount a high skill hurdle to compete
with asset selection.
Asset allocation differs from asset selection in other ways as
well. Asset allocation strategies often involve time series, rather
than cross-sectional analysis, and rely on different types and sources
of information. Currencies are more central to global asset allocation
than even to international asset selection. Finally, traditional asset
allocation managers have eschewed the explicit acknowledgement
of a benchmark in portfolio construction.
Given the relatively small number of bets, why pursue asset
allocation? These strategies have several desirable features: new
opportunities for enhanced returns, often beyond national bound-
aries; the possibility of increased diversification; and the control of
the major determinant of total returns. The asset allocation decision
incurs large risks and offers large potential returns. Global asset
allocation is the largest source of differences in performance among
global portfolios.’
This chapter will present a practical framework for researching
global asset allocation strategies, and will include examples of
global asset allocation to clarify the discussion. Major points will
include the following:
® Researching asset allocation strategies is a three-step ,.
process: forecasting returns, building portfolios, and
analyzing out-of-sample performance.
= The procedure for forecasting returns for asset allocation
differs from that for asset selection in its focus on time
series instead of cross-sectional analysis. In spite of this,
See Solnik (1993b).
Asset Allocation
519
a
ee ee ke
Se
asset allocation, like asset selection, adds value through
identifying relative performance.
= Traditional asset allocation ignores any explicit
benchmark, simply trading off expected excess return
against total risk. This causes substantial problems. We
will implicitly include a benchmark in the expected
returns, a procedure complicated by the presence of
currencies.
THE THREE-STEP PROCESS
Researching asset allocation strategies for institutional investors is
a three-step process: forecasting asset-class expected returns, build-
ing optimal portfolios, and testing their out-of-sample performance.
The forecasts may come from a quantitative model, a qualita-
tive model, or a combination of the two. We will demonstrate a
quantitative model of expected returns.
The quantitative framework will differ somewhat from that
for individual security selection in that it will build a separate time
series model for each asset class, as opposed to a cross-sectional
model of differences between individual securities.
There are two related reasons to focus on separate time series
models rather than a cross-sectional model. First, to the extent that
these asset classes exhibit low correlations as compared to asset
returns (which usually include a strong market factor), a time series
approach makes better sense. Second, the typical explanatory vari-
ables for asset-class returns focus on the individual time series
rather than on cross-sectional comparisons, and aren’t always com-
parable across countries and asset classes. There may still be a place
for cross-sectional models, especially focusing on a smaller set of
correlated asset classes (e.g., European equities), but we will not
deal with such models here.
Even though asset allocation forecasting uses time series analy-
sis, asset allocation strategies add value by identifying relative
_ performance. They bet on the relative performance of asset class A
versus asset class B this month, not on the performance of asset
class A this month versus last month. Underlying the reliance on
time series models is the idea that accurate time series forecasts
provide accurate relative valuations.
520
Implementation
Given the expected excess return forecasts, step 2 is to build
optimal mean/variance portfolios. A problem with traditional asset
allocation is its trade-off of expected excess returns against total risk,
without regard to any benchmark. The resulting optimal portfolio
weights are extremely sensitive to small changes in expected re-
turns, and often vary widely from benchmark weights. A Bayesian
approach (following the principles discussed in Chap. 10 and de-
pendent on a benchmark) can control this problem.
The final step is out-of-sample performance analysis on our
optimal portfolios. We must test these strategies out-of-sample to
determine the information content of the expected return models.
Out-of-sample testing is always critical for researching invest-
ment strategies. For time series—based approaches, even the in-
sample period must include explicit testing of forecasting ability.
Let’s say we fit a time series model over a period from T, to T).
The model’s estimates for times t < T, will then generally include
information from times all the way through T>. In particular, the
estimated regression coefficients will depend on all the data through
T>. Hence the in-sample testing must include estimating the model
from T; to T, and looking at its forecasting ability beyond T,. We
will measure forecasting ability using the information coefficient
(IC), the correlation of forecasts and realizations. After an in-sample
look at forecasting ability to choose appropriate explanatory vari-
ables, out-of-sample testing will validate the performance of the
model.
Step 1: Forecasting Returns
We will illustrate step 1 by building a model to forecast monthly
excess returns for the German, Japanese, U.K., and U.S. aquity
markets using data from January 1985 through December 1992. In
this example, we will build a linear, regression-based model
r(t) = >) x(t) - b + elt)
(18.1)
j
where we attempt to explain asset-class excess monthly returns r(t)
using a set of explanatory variables {x,(t)}. The information used
to forecast r(t), the explanatory variables {x;(t)}, are available at
Asset Allocation
521
the beginning of period t. We estimate coefficients b; to relate the
explanatory variables to the returns.
As described before, we will estimate model coefficients over
part of the in-sample data, and then test forecasting ability through
the remainder of the in-sample period. In fact, our initial regression
will use the first 30 months of data to forecast returns over the 31st
month. Our next regression will use the first 31 months of data to
forecast returns over the 32nd month. We will expand our regression
window until we reach 60 months of data, after which we will
always use the past 60 months of data to forecast returns over the
next month.
In this example, our 8 years of in-sample data will allow us
to estimate information coefficients using 5.5 years of in-sample
forecasts. These in-sample information coefficients help us choose
appropriate explanatory variables.
Later on, we will test model performance in an out-of-sample
period, looking at the performance of portfolios built using the
model. Building portfolios will require the information coefficient
for each country, which we will estimate using the available history
of forecasts and realizations (which start in month 31).
We will use the same five explanatory variables for each mar-
ket.’ These explanatory variables are the predicted dividend yield
for the market, the short-term interest rate in the market, the differ-
ence between that short rate and the U.S. short-term interest rate,
the exchange rate to U.S. dollars, and a January dummy variable.
Two of these variables drop out for the U.S. model.
Table 18.1 displays the statistical results for the markets, based
on model estimation as of January 1993, the beginning of our out-
of-sample period. Table 18.1 displays the coefficients bj and their t
statistics, as well as the adjusted R? statistics for each market. We
can first make some overall observations about the performance
of the model, and then focus in on some details to compare it
to intuition.
Overall, the explanatory power of the model varies widely
from country to country over this mainly in-sample period. The
3See the references of Solnik (1993b), Emanuelli and Pearson (1994), and Ferson and
Harvey (1992) for more details.
PO.
rl
8"
9L-
00°0
9S'0-
Ov
80'0-
sajels peyun
8°0
St =
g'z-
om
Le
6°0-
Z0'0
OL L-
26°} —
9'0
69
OL'0-
wop6ury peyun
v'0-
60
Ze-
eT
oz
Li-
Loo
OL'92
8z'z—
€0'2
Lye
Lv'0-
ueder
Zk
g'Z—
gL
ate
Ov
vl
7z'0
€0'0
8S'0—
96'0—
zS'2
L61
vz'0-
Auewas
pasenbs y
Asenuer
a}ey
ayey wous
ajey
PISIA
3da019}uU]
Ayunog
paisnipy
aBueyox3
aAe|9Y
uous
puepirig
Pst
3718
VL
B22
Asset Allocation
523
average adjusted R* is roughly 9 percent, ranging from close to
zero for the United States to over 20 percent for Germany. For a
model of returns, these results are on average good.
Looking at the estimated coefficients, we can first see that the
coefficients for dividend yield are always positive. Higher dividend
yields imply higher expected returns. In the United States, for
example, the coefficient is 4.0. Each 1 percent increase in predicted
dividend yield in the United States raises our expected monthly
U.S. equity market excess return by 4.0 percent.
The coefficients for the short interest rate are sometimes posi-
tive and sometimes negative. Looking again at the example of the
United States, each 1 percent increase in the short rate lowers the
expected monthly market excess return by 0.56 percent.
The coefficients for the difference between short interest rates
in the local market and in the United States are negative. In the
United Kingdom, a 1 percent rise in this differential implies a
decrease of 1.92 percent in the expected monthly market excess
return.
The intuition here is perhaps that both higher short rates and
higher rate differentials to the United States should lower expected
equity market returns. Our results for the short-rate effect do not
entirely agree with this intuition. However a more detailed analysis
of this model shows a high correlation between these two variables
in some countries for the 60 months ending January 1993. Given
this high correlation of exposures, coupled very often with coeffi-
cients of differing signs, the net result may well be that higher short
rates do indeed imply lower market returns. If we were interested
in pursuing this model further, the natural solution would be to
delete one of these explanatory variables, given its high correlation
with other explanatory variables.
The coefficients for the local exchange rate (U.S. dollars per
unit of local currency) is negative for Germany and the United
Kingdom, and positive for Japan. Only the result in Germany is
statistically significant. The negative coefficient means that as the
local currency depreciates relative to the dollar (as the dollars per
unit of local currency increases), the expected return increases. For
example, if the dollars per deutsche mark decreases from $0.59 to
$0.58, the expected monthly excess return to the German market
will increase by —0.58
- ($0.58 — $0.59) = .0058 = 0.58 percent.
524
Implementation
The January effect is positive for Germany and the United
Kingdom. The coefficient for Germany implies that the expected
monthly excess return is higher by 2.89 percent in January than in
the other months.
In our implementation of this example, we have used the raw
values for all the explanatory variables. This can lead to estimated
coefficients of widely differing magnitudes. It is only xb; that has
the units and magnitude of returns. If the dollar value of a U.K.
pound has a very different magnitude from the U.K. short interest
rate, then the estimated coefficients associated with these explana-
tory variables will have compensatingly different magnitudes. This
can obscure our insight into the relative importance of these effects
(although the t statistics will help). A variant of our implementation
is to linearly rescale the explanatory variables—subtract the sample
mean and divide by the sample standard deviation—to put all the
variables on an equal footing. This linear transformation will have
no effect on explanatory power. However, after the transformation,
the magnitude of the estimated coefficients will identify which
variables explain most of the monthly variation in asset-class
returns.
This example is quantitative, yet it also provides qualitative
insight and intuition into market behavior. It explicitly connects
economic variables to expected returns. These connections should
be intuitive. It can identify which economic variables are relatively
more important for market returns, and help in predicting mar-
ket direction.
The above discussion shows that this simple model exhibits
reasonable explanatory power, with coefficients that generally con-
form to our intuition. The next step is to implement these forecasts
in optimal mean/variance portfolios. Before doing that, however,
we should briefly discuss alternatives for maximizing the explana-
tory power of these models.
Our simple model constrained the explanatory variables to be
the same in each market. An obvious extension would be to allow
different variables in different markets based on how well they
forecast returns in those markets (and accounting for colinearities
in some markets). We could extend the explanatory variables to
include macroeconomic variables and previous or lagged monthly
returns (to capture mean reversion or trends). We could add ana-
Asset Allocation
525
lysts’ forecasts or even forecasts of political risks. We can combine
the forecasts from a quantitative model with forecasts from the more
qualitative sources that are traditional in global asset allocation. We
can even use the insights of the model into the size and sign of these
coefficients to help the traditional analyst make better-informed
qualitative forecasts. And, of course, we can extend the analysis to
include bond markets as well as equity markets.
Step 2: Building Optimal Portfolios
Our estimated model [Eq. (18.1)] provides monthly expected excess
returns to a set of equity markets. But mean/variance optimal
portfolios that trade off expected excess return and total risk are
extremely sensitive to these expected returns. Whereas active or
residual asset returns exhibit relatively low correlations, asset-class
excess returns exhibit high correlations.
We could handle this problem by using expected active or
residual returns relative to an asset allocation benchmark. This is
the approach of the rest of the book. Instead, for this chapter,
we will stick to the traditional asset allocation methodology, and
describe how to avoid the sensitivity problem. To do this, we will
effectively sneak the benchmark into our expected excess return
forecasts.*
Our approach will be the methodology we developed in Chap.
10, refining these “raw” expected returns 7. The basic forecasting
formula is
Ein7} = bint Coviri}
Varun
(7 = Etr})
(18.2)
where E{r|7} is the refined expected return conditional on the fore-
cast ?. This simplifies to the forecasting rule of thumb
E{r|?}, = E{r} + IC - STD{r}
- Score
(18.3)
When we implement our simple model, each market will have
its own information coefficient, which may vary over time de-
pending on the model’s forecasting ability in that market. Only for
‘Note that the problem involving the trade-off between active or residual return and risk
differs from the standard global asset allocation methodology in that it involves
the aversion to active or residual risk, not to total risk.
526
Implementation
markets with significant information coefficients will our forecast
returns differ from consensus expectations.
To use Eq. (18.3) in our example model, we must analyze one
further detail: Where do we find the consensus expected excess
returns? Here is where we will sneak a benchmark into the problem:
We will use the consensus returns implied by our benchmark port-
folio. Given a benchmark, then, as we saw in Chap. 2, the consensus
expected excess returns are just
Etr) = B- fs
(18.4)
where 8 is the beta of the asset class relative to the benchmark and
fg is the consensus expected return to the benchmark.
This approach is more complex with multiple currencies, espe-
cially if we want consensus expected excess returns that are reason-
able from many different currency perspectives.°
INTERNATIONAL CONSENSUS
EXPECTED RETURNS
So what is the problem with backing out consensus expected returns
in the international context? If we aren’t careful, the results will
look very different from different perspectives. Part of the problem
is the home bias. If we start by assuming, for example, that the
standard asset allocation of a U.S. pension fund, with at most about
20 percent invested outside the United States, is optimal, Eq. (18.4)
leads to artificially low expected excess returns for foreign assets.
Perhaps more surprising, we can’t solve the problem by simply
reweighting the assets in the presumed efficient portfolio so that,
for example, 60 percent of the holdings are outside the United
States and 40 percent are within the United States, more in line
with global capital market weights. At this level, Eq. (18.4) implies
consensus expected excess returns for foreign assets that are too
large.° But this domestic view is only part of the problem.
“If your focus is solely on asset allocation for investors from a single country, and their
benchmark is imposed externally, then you may not require “sensible” expected
returns. You can use the expected returns consistent with the imposed benchmark,
whether they appear sensible or not. In that case, the discussion in the next
section is just a cultural diversion.
:
See Grinold (1996) for details.
Asset Allocation
527
An Aside: Currency Semantics
We should be aware of a semantic pitfall. Currency has a double
meaning: It can be either a numeraire of perspective or an asset.
It is this double nature that gives a theological aspect to that old
conundrum: “Is currency an asset?” We will maintain that short-
term, default-free, interest-bearing bills held in foreign countries
are indeed assets. The return on such a bill is known in its home
country; the only uncertainty in its return for a foreign investor is
the exchange rate risk. Thus, when we speak loosely of currency
as an asset, we actually mean a short-term, default-free, discount
bill in that particular country.
On the other hand, we use the notion of currency to indicate
an investment perspective—i.e., how we keep score. Phrases like
“for the yen-based investor” or “this is not as attractive from a
sterling perspective” indicate that we are using the currency as
a numeraire.
We will use currency in both its meanings. We start with
an example of consensus expected returns viewed from several
numeraire perspectives. We will examine stocks and bonds in the
four major countries treated in our expected return model: Ger-
many, Japan, the United Kingdom, and the United States. Our
presumed efficient portfolio is 60 percent stocks and 40 percent
bonds in each country. The country weights are Germany, 10 per-
cent; Japan, 30 percent; the United Kingdom, 20 percent; and the
United States, 40 percent. We estimate risk from historical data for
1970 through 1995.
Table 18.2 shows the consensus expected returns from each
of the four different currency perspectives.
The wide range of expected excess returns suggests a major
inconsistency. For example, a Frankfurt-based investor holding dol-
lars will expect 4.80 percent excess return, while a
New York-based
investor holding deutsche marks (or Euros, post 1999) will expect
a 1.93 percent excess return. While win/win is a laudable concept,
this seems to carry the notion too far. In fact, as we show below,
it is not possible to have numbers this high in a consistent scheme.
This example suggests two questions. First, how do we consis-
tently transform expected excess returns from one currency per-
spective to another? If we know the expected excess returns for a
528
Implementation
TABLE
18.2
Numeraire Perspective
Asset
Germany
Japan
United Kingdom
United States
German stocks
5.10%
5.18%
5.48%
6.27%
Japan stocks
9.70%
5.36%
7.27%
7.54%
U.K. stocks
10.76%
7.41%
6.49%
7.63%
U.S. stocks
10.62%
6.62%
7.49%
5.54%
German bonds
0.46%
1.05%
1.56%
2.73%
Japan bonds
4.15%
0.36%
2.36%
2.08%
U.K. bonds
4.64%
2.18%
0.91%
2.97%
U.S. bonds
5.96%
2.44%
3.40%
1.87%
Deutsche marks
0.00%
0.47%
0.75%
1.93%
Yen
3.80%
0.00%
1.75%
1.30%
Sterling
3.31%
0.97%
0.00%
1.48%
Dollars
4.80%
0.83%
1.78%
0.00%
London-based investor, how do we deduce the expected excess
returns for a New York- or Tokyo-based investor? Second, how do
we determine a “reasonable” ex ante efficient portfolio? In particu-
lar, what role will currency play in that portfolio?
The first question has a definite answer, as discussed in Black
(1990) [also Black (1989)]. International returns, by their nature,
involve products of the return in the local market and changes in
the level of exchange rates. This type of relationship will hold
between any two countries and for any asset. We illustrate using
U.S. and U.K. investors and the Australian stock BHP:
[($/£)(t)]
[($/£)(0)]
where Rgup(US|0,t) refers to the cumulative total return’ to BHP
over the period from 0 to t from the U.S. dollar perspective, and
we represent a 3.5 percent return as 1.035. Suppose a British investor
observes a 3.5 percent return to BHP between 0 and tf. Furthermore,
the exchange rate at time 0 is $1.50 per pound, and the exchange
Reup(U.S.|0,t) =
- Reur(U.K.|0,£)
(18.5)
-
&
’We are assuming
reinvestment of any
cash flows.
y
Asset Allocation
529
rate at time t is $1.52 per pound. Then the U.S. investor will observe
a 4.88 percent return over the interval.
From that simple relationship, we can derive a rule linking
excess rates of return in different locales. We always measure re-
turns in excess of the investor’s risk-free alternative; i.e., the excess
return on BHP for a U.S. investor is relative to the risk-free return
in the U.S. market:
rpup(U.S.) = rpyp(U.K.) = r3(U.K.) SF Opupe(U.S.)
(18.6)
So the excess return to BHP from the U.S. perspective equals the
excess return to BHP from the U.K. perspective, less the excess
return to U.S. Treasury bills from the U.K. perspective, plus the
covariance between BHP and U.K. Treasury bills from the U.S.
perspective (see Appendix C for details).
Equation (18.6) deals with realized returns. We can also take
expectations to derive a link between the expected returns:
E{rsyp(U.S.)} = E{rgyp(U-K.)} — Ef{rg(U.K.)} + opype(U.S.)
(18.7)
This result answers our first question about moving expected
excess returns from one locale to another. It requires both expected
return and risk forecasts.
The second question, concerning a reasonable presumed effi-
cient portfolio, has no totally acceptable answer in the domestic
case. It will only get harder in the global case. We will have to be
satisfied with a reasonable way to treat currency in the global
context. Here is the procedure from Grinold (1996).
How can we get rid of the exchange rates? One way is to
envision a world with a single currency. Suppose we had a compos-
ite country that we will call COM. The currency for COM is a
mixture of the currencies of all the countries, a composite currency.
A portfolio called BSK (for basket) determines the makeup of the
composite currency. For example, the basket could be 40 percent
dollars, 30 percent yen, 20 percent sterling, and 10 percent deutsche
marks. Recall the double nature of currency. The currency portfolio,
BSK, defines the composite currency numeraire, COM. It is also
an asset. It serves as the risk-free asset from the COM perspective,
and German, Japanese, U.K., and U.S. investors can hold BSK.
We can rewrite Eq. (18.7) using this new currency asset and
numeraire:
530
Implementation
E{rgyp(U.S.)} = E{rgup(COM)} — E{rs(COM)} + opupssx(U.S.)
(18.8)
Now, we can’t expect the consensus expected returns procedure to
work perfectly from the COM perspective, since it doesn’t work
perfectly in a pure domestic setting. We are striving for a relative
measure of satisfaction rather than an absolute measure. The best
way to judge is to look at the improvement we get over using the
naive procedure. To do that, we will observe the improvement in
our example. But first, we will trace the presumed efficient portfolio
as we move from one locale to the other. We'll see that the presumed
efficient portfolio changes.
Let’s start from the COM currency perspective and presume
that portfolio Q is efficient.
Now, from the COM perspective, portfo-
lio Q explains all expected excess returns. For example,
E{rsup(COM)} = Bsxp(COM)
- fo(COM)
(18.9)
and for a U.S. risk-free instrument from the COM currency per-
spective,
E{rs(;COM)} = Bs(COM) - fo(COM)
(18.10)
We can use Egg. (18.9) and (18.10) for the expectations in Eq. (18.8).
Furthermore, we can use this approach to calculate an effective
efficient portfolio from other perspectives. The idea is to transform
the betas from the COM perspective to the dollar perspective. Then
we can solve for the portfolio, Qus, that explains excess returns from
the U.S. perspective. The technical appendix contains the details.
We find that the only change required in order to move from
Q to Qus, or from Qys, to Qyx, comes in the currency position. For
example, to move from Q to Qus, we partially hedge against
changes in the value of the currency basket. Portfolio Quys, will be
long dollars and short the basket currency, relative to portfolio Q.
As the technical appendix will show, to move from Q to Qys, we
subtract a fraction [1 — (¢g/SRg)] of the portfolio that is long the
basket currency (e.g., 40 percent dollars, 30 percent yen, 20 percent
deutsche marks, 10 percent pounds) and short (—100 percent) dol-
lars. That fraction is roughly 65 percent, assuming>a Sharpe ratio
Asset Allocation
531
of about 0.35 and a volatility of about 12 percent for the global
asset allocation portfolio Q.°
Our presumed efficient portfolio from the COM perspective
will have 60 percent stock and 40 percent bond allocations in each
country, with country weights 40 percent in the United States, 30
percent in Japan, 20 percent in the United Kingdom, and 10 percent
in Germany. It contains no explicit currency positions.
Table 18.3 displays the consensus expected returns from vary-
ing perspectives, including the composite currency. Notice the very
low expected excess returns for holding currency.
The forecasts of expected excess returns for the currencies are
more reasonable and the expected excess returns for stocks and
bonds more consistent across countries than in Table 18.2. In partic-
ular, let’s look at the German investor holding U.S. T-bills and
the U.S. investor holding German T-bills. Using Eq. (18.7), and
TABLE
183
Numeraire Perspective
United
United
Asset
Germany
Japan
Kingdom
States
Composite
German stocks
4.72%
4.59%
4.68%
4.96%
4.51%
Japan stocks
6.81%
5.70%
6.15%
6.32%
5.89%
U.K. stocks
7.51%
6.62%
6.45%
6.80%
6.49%
U.S. stocks
6.79%
5.76%
5.98%
5.65%
5.60%
German bonds
0.65%
0.64%
0.77%
1.14%
0.61%
Japan bonds
1.52%
0.53%
1.00%
1.04%
0.67%
U.K. bonds
2.14%
1.45%
1.19%
1.75%
1.33%
U.S. bonds
2.64%
1.71%
1.95%
1.71%
1.60%
Deutsche marks
0.00%
—0.04%
0.05%
0.41%
—0.09%
Yen
0.99%
0.00%
0.41%
0.42%
0.09%
Sterling
0.85%
0.19%
0.00%
0.43%
0.06%
Dollars
1.08%
0.06%
0.29%
0.00%
—0.07%
8In other chapters, we discussed portfolio Q volatilities in the range of 15 to 20 percent.
Those numbers assume only equity investments. The lower volatility quoted here
reflects the significant exposure to fixed income.
532
Implementation
remembering that the excess return for a German investor on Ger-
man T-bills is, by definition, zero,
E{rpw(U.S.)} + E{rs(GER)} = o}m(U.S.)
(18.11)
In Table 18.3, the 0.41 percent return for a U.S. investor holding
German bills and 1.08 percent for a German investor holding U.S.
bills are consistent with a 12.2 percent exchange rate volatility. By
contrast, the expectations in Table 18.2—a large 1.93 percent for a
U.S. investor holding German bills and an enormous 4.80 percent
for a German investor holding U.S. bills—are consistent with a
huge exchange rate volatility of 25.9 percent. The realized volatility
of this exchange rate over any sizable period in the last 20 years
has consistently been in the 11 to 13 percent range.
Step 3: Analyzing Out-of-Sample Portfolio
Performance
The last step in our methodology involves analyzing the out-of-
sample performance of our optimized portfolios. Remember that
a fair test of these time series models requires this out-of-sample
testing. Focusing on excess returns to the strategy, we can examine
the cumulative return plots and compare portfolio performance to
benchmark performance. We can calculate the Sharpe ratios for the
portfolio and the benchmark.
We can also look at the portfolio’s active returns. We can
examine the cumulative active returns, the information ratio, and
the t¢ statistics.
A more detailed performance analysis would also
look at turnover, performance in up markets versus down markets
(defined by the benchmark or the numeraire market), the number
of up and down months, and which particular markets contributed
the most to the outperformance. Performance dominated by one
particular market would be a worrisome sign.
The goal of this out-of-sample performance analysis step is to
fairly measure the value added of the strategy, and possibly identify
research directions for model improvement. Note that this final
step of analysis of asset allocation performance measures how well
we identify relative value among asset classes, since we overweight
some and underweight others. Our return forecasts use time series
Asset Allocation
533
models. To add value, those time series models must forecast cross-
sectional returns.
SUMMARY
We have discussed a three-step procedure for researching practical
asset allocation strategies. These steps include forecasting expected
asset class returns, building optimal portfolios, and analyzing the
out-of-sample performance of those portfolios.
We saw that asset allocation strategies, unlike asset selection
strategies, rely on time series analysis to forecast returns. We dis-
cussed how traditional asset allocation trades off expected excess
returns against total risk in building portfolios. We showed how
to retain that traditional approach, but avoid its problems, by refin-
ing the expected excess returns based on a benchmark. This process
is complicated for global investors by the presence of currencies.
This framework has importance far beyond quantitative strate-
gies for global asset allocation. It can provide intuition and control
for quantitative or qualitative approaches to this critical element
of global investing.
NOTES
There are two distinct strands of research concerning asset alloca-
tion. One involves building models to forecast expected returns for
different asset classes. The other focuses on appropriate methods
for constructing portfolios.
Let’s start with the research on international expected returns.
Solnik has worked extensively on modeling expected returns to
international equity and bond markets. In his 1993 Journal of Empiri-
cal Finance paper, he models expected returns to nine equity and
nine bond markets using three fundamental variables—dividend
yield, the short interest rate, and the long interest rate—plus a
January dummy variable. Solnik’s 1993 monograph, Predictable
Time-Varying Components of International Asset Returns, extends his
model by including the spread between short interest rates and
the U.S. short interest rate and lagged market returns as additional
explanatory variables. Emanuelli and Pearson (1994) also use IBES
earnings forecast data to help explain market returns. In particular,
534
Implementation
they define an earnings forecast revision ratio based on the number
of up and down earnings forecast revisions in the market as a
predictor of future market returns. Ferson and Harvey (1992) have
also built models of expected returns to 18 different international
equity markets. The review paper by Solnik includes an extensive
bibliography of these and other efforts to build models of ex-
pected returns.
Black and Litterman’s work on portfolio construction for
global asset allocation focuses on an entirely different challenge
of global investing. Starting with the traditional mean/variance
framework, they discuss a well-known problem for global asset
allocation: The optimal portfolio weights can be extremely sensitive
to small changes in expected returns. The underlying cause is the
high correlation of many asset classes. To an optimizer, they appear
as reasonable substitutes.
Because of this, optimized portfolios can often exhibit weights
that vary greatly from global benchmarks. Exposures may be re-
stricted to only a very few assets. Black and Litterman describe a
Bayesian approach to portfolio construction. Instead of using raw
expected returns and mean/variance optimization, they back out
the consensus expected returns which will lead exactly to bench-
mark portfolio weights, and then move away from those consensus
forecasts toward the raw expected forecasts in proportion to the
information content of the model. Grinold (1996) also covers this
territory, describing how to back out consistent and reasonable
expected excess returns for multiple currency perspectives. This is
especially important for institutional portfolios, which require not
only an optimal return/risk trade-off, but also low risk relative to
a benchmark.
PROBLEMS
1. You are researching an asset allocation strategy among
global equity markets using price/earnings and price/
book ratios. What difficulties might you encounter in
trying to implement this with cross-sectional analysis?
2. Why might you expect to see differing January effects
across countries?
Asset Allocation
535
3. Suppose a U.K. investor observes a BHP return of 3.5
percent, but the pound depreciates relative to the dollar
by 3.5 percent over the period (e.g., from $1.50 to
$1.4475). Does a U.S. investor observe a net BHP return
of zero? Why or why not?
4. Evidently (from examining Table 18.3), the sample data
have produced a Q(GER) for Germany that has a high
correlation with currencies and a Q(JPN) for Japan that
has a low correlation with currencies. How would you
explain the lack of symmetry between the Japanese
relationship with other currencies and the German
relationship with other currencies?
REFERENCES
Ambachtscheer, Keith P. “Pension Fund Asset Allocation: In Defense of a 60/40
Equity/Debt Asset Mix.” Financial Analysts Journal, vol. 43, no. 5, 1987,
pp. 14-24.
Black, Fischer. “Capital Market Equilibrium with Restricted Borrowing.” Journal
of Business, vol. 45, 1972, pp. 444-455.
. “Universal Hedging: Optimizing Currency Risk and Reward in Interna-
tional Equity Portfolios.” Financial Analysts Journal, vol. 45, no. 4, 1989,
pp. 16-22.
. “Equilibrium Exchange Rate Hedging.” Journal of Finance, vol. 65, no. 3,
1990, pp. 899-907.
Black, Fischer, and Robert Litterman. “Asset Allocation: Combining Investor Views
with Market Equilibrium.” Goldman Sachs Fixed Income Research Publica-
tion, September 1990.
. “Global Asset Allocation with Equities, Bonds, and Currencies.” Goldman
Sachs Fixed Income Research Publication, October 1991.
Emanuelli, Joseph F., and Randal G. Pearson. “Using Earnings Estimates for Global
Asset Allocation.” Financial Analysts Journal, vol. 50, no. 2, 1994, pp. 60-72.
Ferson, Wayne E., and Campbell R. Harvey. “The Risk and Predictability of Interna-
tional Equity Returns,” Review of Financial Studies, vol. 6, no. 3, 1992, pp.
527-566.
Grinold, Richard C. “Alpha Is Volatility Times IC Times Score.” Journal of Portfolio
Management, vol. 20, no. 4, 1994, pp. 9-16.
. “Domestic Grapes from Imported Wine.” Journal of Portfolio Management,
Special Issue December 1996, pp. 29-40.
Kahn, Ronald N., Jacques Roulet, and Shahram Tajbakhsh. “Three Steps to Global
Asset Allocation.” Journal of Portfolio Management, vol. 23, no. 1, 1996, pp.
23-32.
Sharpe, William F. “Capital Asset Prices: A Theory of Market Equilibrium under
Conditions of Risk.” Journal of Finance, vol. 19, no. 3, 1964, pp. 425-442.
536
Implementation
. “Integrated Asset Allocation.” Financial Analysts Journal, vol. 43, no. 5,
1987, pp. 25-32.
Singer, Brian D., Kevin Terhaar, and John Zerolis. “Maintaining Consistent Global
Asset Views (with a Little Help from Euclid).” Financial Analysts Journal,
vol. 54, no. 1, 1998, pp. 63-71.
Solnik, Bruno. “The Performance of International Asset Allocation Strategies Using
Conditioning Information.” Journal of Empirical Finance, vol. 1, 1993a, pp.
33-55.
Solnik, Bruno. Predictable Time-Varying Components of International Asset Returns.
(Charlottesville, Va.: Research Foundation of Institute of Chartered Financial
Analysts, 1993b).
TECHNICAL APPENDIX
In this appendix, we will derive the link between excess returns
from different perspectives [Eq. (18.6)], and also the transformation
of portfolio Q from the COM perspective to other perspectives.
To derive the result connecting excess returns from different
perspectives, we will continue the tradition of this chapter and focus
on BHP from the U.K. and U.S. perspectives. The generalization of
the approach is obvious, and by using a specific example, we avoid
having to remember which subscript or superscript refers to numer-
aire versus local market, etc. Let’s begin this treatment with Eq.
(18.5) from the main text:
[($/£)(t)]
[($/£)(0)]
Just to understand the logic of this starting point, imagine taking
$1 at time 0 and converting it to U.K. pounds. You will have 1/
[($/£)(0)] pounds. Invest that amount in BHP from t = 0 to t. You
then have 1/[($/£)(0)] -
Rgyp(U.K.|0,t) pounds. Converting back to
dollars leads to Eq. (18A.1).
v:
To account for the multiplicative relationship between local
returns and currency returns, we will use a slightly unusual defini-
tion of cumulative excess return:
Regup(U.S.|0,t)
R,(U.S.|0,t)
where R,(U.S.|0,t) is the value at time ¢ of a U.S. money market
account starting with $1 at t = 0. We can similarly define excess
Rpup(U.S.,excess|0,t) =
(18A.2)
Asset Allocation
537
returns to BHP from the U.K. perspective, and excess returns to
U.K. pounds from the U.S. perspective. In fact,
Rpup(U.K.,excess|0,t)
Rpyp(U.S.,excess|0,t) = “R,(U.K.excess|0,f)_
(18A.3)
Now we want to look at instantaneous excess returns /:
dR(excess | 0,t)
sl R(excess | 0,t)
(18A.4)
The calculation of this from Eq. (18A.3) is complicated by the ratio
of two stochastic terms. We can apply Ito’s lemma, to show that,
in general, for
x
Y
(18A.5)
we find
4F _dX_ dY
dY\ _
dX dY
(18A.6)
E
X
Y + Var Y
Cov XY
Ito’s lemma effectively tells us to expand dF in a Taylor series and
keep all terms up to second order. Applying this to Eq. (18A.3),
we find
rpyp(U.S.,t) — rsup(U.K..,t) = r3(U.K.,t)
(18A.7)
+ Var{r;(U.K.,t)} — Cov{rgup(U.K.,t),rs(U.K.,f)}
We will need one more step to derive the result in the main text.
In general, for any asset n,
Covites (US:), 1 (U0 S.)}
(18A.8)
=" COvVifsa( UK) — fA Kar.) = 7(0.K)}
If we set n = U.K. pounds, we can simplify this because the excess
return to U.K. pounds from the U.K. perspective is zero:
Cov{rgup(U'S.), r.(U.S.)}
(18A.9)
= ‘Covifer(U-K) — 1(U-K.), = 7.(U.K)}
= Covirsr(U.K.), — 7(U-K.)} + Varir,(U.K.)}
538
Implementation
Substituting this into Eq. (18A.7) leads to
Tpyp(U.S.) a Tgyp(U.K.) ar r3(U.K.) te Cov{rgup(U:S.), r(U.S.)}
(18A.10)
This is Eq. (18.6) in the main text.
Transforming Portfolio Q
We saw in the main text that
E{rpyp(U.S.)} = E{rgyp(COM)} — E{rs(COM)} + opupssx(U.S.)
(18A.11)
We also saw that
E{r,(COM)} = B,(COM) - fo(COM)
(18A.12)
= 4 * On0(COM)
where
— 1e6COM)
(18A.13)
a@(COM)
Here we are using Q to refer to the efficient portfolio from the
COM perspective. We are seeking a portfolio we will call Quys. If
we apply standard (not international) CAPM analysis to this portfo-
lio from the U.S. perspective, we will find the same consensus
expected excess returns as if we had used Q in the full interna-
tional context.
First, we will use Eq. (18A.8) to convert the necessary covari-
ances from Eqs. (18A.12) and (18A.11) to the U.S. perspective:
= OpupQ(U.S.) aa Opex,Q(U.S.) —Opuppsk(U.S.) ale o%ox(U.S.)
and
0s9(COM) = —OpexQ(U.S.) Li Orex( US.)
(18A.15)
Substituting Eqs. (18A.12), (18A.14), and (18A.15) into Eq.
(18A.11) leads to
E{rgyp(U.S.)} = a - [opupg(U.S.) a Opuppsk(U.S.)] tj Opuppsk(U.S.)
(18A.16)
Asset Allocation
539
If we define Qys such that
Elran(U.S.)} = a - [surg US.)]
(18A.17)
1
then OpuPg,,,(U-S.) = Opupg(U.S.) = (
aa? ‘)
y Opuppsx(U.S.) (18A.18)
Hence, we can define Qys as
1
lig. — ho eA (1
— 1)
. (hgsx = hs)
(18A.19)
We can freely add or subtract hs without influencing the covari-
ances. We have used this property to preserve the investment level
(e.g., fully invested) of Q. Note that the only adjustment in moving
from Q to Qus, involves a shift in currency exposure. We are low-
ering our exposure to the currency basket, i.e., hedging our interna-
tional currency exposure.
——
Jwad) (oes ats anti
;
.
'
¥
_
‘
i
y
Dp
tu
>»?
f
~
;
=
she
2)
i
a
(jan
7
‘y
‘
f
ry
tie
Wy tit is eOomas tiga ‘S iv
=
;
fle ous
7
(edt
;
1?) Pde
tring Po a usaf
¥v re
=
Re
ae
‘ia?
Gow! Qiu eave Cs
I
( oF
WJ
¥
AL
;
(
i
sere
7
a) uf
“
*
A
SUC
SHY ech
aptly 7nd gaan
6
arte
ise cartehie ra Aner
:
eh
s
1
¥ ah t J Te
me
:
a
:
>
;
S
Py
>. i
\ 7 lire oH ro 4
eo
wl
al ae
ay
ie ‘yy
:
‘1 Ogi
:
wo RA
=e
=
j
!
|
oy
e
i?
6
