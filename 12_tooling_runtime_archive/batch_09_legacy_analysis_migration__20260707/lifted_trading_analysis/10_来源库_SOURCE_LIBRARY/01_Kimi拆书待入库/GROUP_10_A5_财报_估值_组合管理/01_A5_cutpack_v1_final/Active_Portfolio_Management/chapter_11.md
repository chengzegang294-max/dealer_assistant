# Chapter 11: Advanced Forecasting

- **book_name**: Active Portfolio Management
- **main_source**: pdf
- **cross_check_source**: none
- **pdf_role**: main_text_source
- **split_scope**: pages 317-336

---

CHAPTER
11
Advanced Forecasting
INTRODUCTION
Chapter 10 covered forecasting basics, especially the insight that
refined alphas control for volatility, skill, and expectations. In the
context of a single asset, Chapter 10 also examined how to combine
multiple signals, and even briefly presented some choices of ad-
vanced and nonlinear methodologies.
Chapter 10 has provided much of the insight into forecasting.
But it hasn’t covered the standard case facing institutional manag-
ers: multiple assets. This chapter will mainly focus on that im-
portant practical topic. It will also cover the particular case of factor
forecasts, and some ideas about dealing with uncertain informa-
tion coefficients.
Highlights will include the following:
= The single-asset methodology also applies to multiple
assets.
= A complication occurs when we have cross-sectional and
not time series scores. In many cases, we need not
multiply cross-sectional scores by volatility.
= If you have information and you forecast some factor
returns, do not set other factor forecasts to zero.
® Uncertainty in the IC will lead to shrinkage in the alpha.
We begin with the discussion of multiple assets.
295
296
Information Processing
MULTIPLE ASSETS
The standard situation for an institutional manager involves multi-
ple assets: choosing a portfolio that will outperform the benchmark.
The chapters in Part 1, “Foundations,” discussed exactly this case.
First, we must point out that the basic forecasting formula,
Eq. (10.1), applies in the case of multiple assets and multiple signals:
E{r|g} = E{r} + Cov{rg} - Var {g} - (g — Etg})
(11.1)
In Eq. (11.1), we can treat both r and g as vectors of length N and
K, respectively, where K/N measures the number of signals per
asset. In the case of one signal per asset, the technical appendix
will show that the forecasting rule of thumb still applies for each
asset n:
UAgssunye Geese)
G12)
We are assuming that the signal has the same information coefficient
across all assets.
We have also introduced the subscript “TS” to explicitly label
the score as a time series score. The time series of scores for asset
nN, Z75n, has mean O and standard deviation 1. This is the definition
of score that we discussed in Chap. 10. We will contrast these scores
with cross-sectional scores, Z¢sn-
Unfortunately, Eq. (11.2) doesn’t describe the typical situation
facing a manager: a numerical forecast for each stock at a given
time. We do not have N time series scores; rather, we can calcu-
late one set of cross-sectional scores. Cross-sectional scores have
mean 0 and standard deviation 1 across N stocks at one time. We
want time series scores. We have cross-sectional scores. How do
we proceed?
CROSS-SECTIONAL SCORES
»
The time series score 27s, depends not only on the current signal,
g,(t), but also on the time series average and the standard deviation
of gn:
Zsn(t)
Stdrs{¢,}
(11.3)
But if we can calculate only a cross-sectional set of {g,} (ie, g,
Advanced Forecasting
297
for n = 1, 2,... N at one time ft), we can calculate only cross-
sectional scores:
EE, g(t) cm Ecs{ Gay,
Zcsn(t)
Stdclg,(t)]
(11.4)
How can we move from the cross-sectional scores we can easily
observe to the time series scores required for Eq. (11.2)?
For simplicity, let’s assume that the mean forecast over time
is 0 for each stock, and that the IC for each stock is the same and
that forecasts are uncorrected across stocks. We will then analyze
two cases. In Case 1, the time series standard deviation of the signal
is the same for each asset. In Case 2, the time series standard
deviations of the signals are proportional to stock volatility. For
example, if stock A is twice as volatile as stock B, its raw signal
gat) will be twice as volatile as g,(t).
Case 1: Identical Time Series Signal Volatilities
In case 1, we are assuming that
Stdrs{gn} = c1
(11.5)
where c; is independent of n. In this case, we can estimate c, via time
series or cross-sectional analysis. We can estimate c, froma time series
of scores chosen from a distribution with standard deviation c,. Alter-
natively, we can estimate c, by choosing cross-sectionally from a set
of distributions, each with mean 0 and standard deviation c). In other
words, if the time series standard deviations are identical, then time
series scores equal cross-sectional scores:
es Seer ere a &n I as On ee
1
2180 =
Stdrelg,]
Cy
Stdesgu]
ae
(Cee (eo [es ZCS.n
Te)
Case 2: Time Series Signal Volatilities
Proportional! to Asset Volatilities
In case 2, we assume that time series standard deviations depend
on asset volatilities:
Stdrslgn} = Co + Wn
(11.8)
298
Information Processing
Once again, we assume that all time series means are 0. But starting
with Eq. (11.8), we can estimate the constant c, by observing that
= Stdrs {|
(11.9)
By assumption, the coefficient c, is independent of n. But in that
case, we can equivalently estimate it from time series or cross-
sectional data, assuming forecasts are uncorrelated across assets:
cde {|
(11.10)
With this cross-sectional estimate of c, and with Eq. (11.8), we can
restate the basic result, Eq. (11.2), as
le
eer
aig etm
ob, = On *
IC (©, ]
(LAI)
eee |
(11.12)
Stdos |S}
To rewrite this explicitly in terms of cross-sectional scores,
Stdcs {|
CStsn
But the second term on the right-hand side of Eq. (11.13) is just a
number, independent of n. We will call it c,. Hence
»
o, = IC i Cy ; ZCS,n
(11.14)
So if the time series signal volatilities are proportional to asset
volatilities, then the refined forecasts are proportional to cross-
sectional scores and neshenent of volatility. In case 2, forecasts
still equal volatility -
score, but this is proportional to IC -
cross-sectional score. “ine constant of etal ecto
9)
Cy, Can vary
by signal.
Advanced Forecasting
299
Empirical Evidence
It appears that the question of how to refine cross-sectional signals
depends critically on how time series signal volatilities vary from
stock to stock. In the previous section, we analyzed two extremes:
independent of stock volatility and proportional to stock volatility.
Here we will examine several specific signais along two partic-
ular dimensions. First, we will simply observe how the time series
signal volatilities depend on asset volatilities. Second, we will com-
pare the performance of the alphas refined according to Eqs. (11.7)
and (11.14). We hope to find empirical results consistent with our
analysis. (For another approach to empirically testing alpha scaling,
see the technical appendix.)
We will examine six U.S. equity signals commercially available
from BARRA:
Dividend discount model (DDM)
Estimate change
Estimate revision
Relative strength
Residual reversal
Sector momentum
The dividend discount model provides internal rates of return
from a three-stage model, as outlined in Chap. 9. The estimate
change signal is the 1-month change in consensus estimated annual
earnings,’ divided by current price. The estimate revision signal
combines the 1-month change in consensus estimated annual earn-
ings with the 1-month stock return (to help account for stocks
whose prices have already reacted to the change in consensus).
The relative strength signal combines each stock’s return over the
past 13 months with its return over the past month [i.e., it attempts
to capture momentum over roughly the past year, and it controls
for short-term (1-month) reversal effects]. The residual reversal
signal uses 1-month returns, residual to industry and risk index
'This is based on a weighted combination of estimated earnings in fiscal years 1 and
2. The weights depend on where the current date stands in the fiscal year. At
the beginning of fiscal year 1, all the weight is on fiscal year 1. As the year
progresses, the model places more and more weight on fiscal year 2.
300
Information Processing
effects. The sector momentum signal is the 1-month return to
capitalization-weighted sector portfolios. Each stock in the sector
receives the same signal.
BARRA provides these signals as monthly cross-sectional
scores. The sector momentum signal stands out in this group as
the only signal on which many assets receive the same score.
In the first empirical test, we simply calculated 60-month time
series signal volatilities for roughly the largest 1200 U.S. stocks (the
BARRA HICAP universe) as of December 1994. We then ran the
following cross-sectional regression:
Stdis{g,} =a + b-w, + &,
CPs)
This regression will test whether the time series signal volatilities
vary from stock to stock by residual volatility. Most importantly,
we want to know the R’ statistic for the regression, and also the t
statistic for the estimated coefficient b. We find the results given
in Table 11.1.
For all the signals except sector momentum, we see a very
strong positive linear relationship between time series signal volatil-
ities and asset residual volatilities. This implies that we need not
rescale these cross-sectional scores by volatility when estimating
expected exceptional return.
We tested this idea by calculating expected exceptional returns
using both Eq. 11.7 and Eq. 11.14. We will describe the test methodol-
ogy in detail in Chap. 12. For each method, we built optimal portfo-
TABLE
11.1
Model
t statistic (b)
DDM
0.37
19.3
Estimate change
0.34
18.0
Estimate revision
0.31
17.0
Relative strength
0.72
54.3
Residual reversal
0.77
62.2
Sector momentum
=H}
Advanced Forecasting
301
a
ee
TA BLE
11.2
Information Ratio
Model
@,° IC - Zs
DDM
1.19
Estimate change
1.87
Estimate revision
3.32
Relative strength
1.93
Residual reversal
2.18
Sector momentum
eO)
lios based on the refined signal, and looked at information ratios
from backtests.* Table 11.2 contains the results.
The evidence in Table 11.2 is completely consistent with the
evidence from Table 11.1. Five of the models (all but sector momen-
tum) exhibit a strong relationship between signal volatility and
asset residual volatility. And in each case, the cross-sectional scores
[the correct refined signals according to Eq. (11.14)] match or outper-
form those scores multiplied by residual volatility.
In the one case in which signal volatilities did not vary with
asset volatilities, sector momentum, the cross-sectional
scores
multiplied by volatility [the correct refined signals according to Eq.
(11.7)] outperformed the cross-sectional scores alone.
The empirical evidence supports the previous analysis. Given
cross-sectional scores, the critical question is whether signal volatili-
ties vary with asset volatilities. The refining process always multi-
plies time series scores by volatility. This does not always imply
multiplying cross-sectional scores by volatility.
Forecasts have the form volatility
- IC - score. Sometimes this is
simply proportional to IC - cross-sectional score.
In this test, we industry-neutralized all but the sector momentum signal. Hence each
signal is defined relative to its industry. Industry-neutralizing sector momentum
would set it to zero.
302
Information Processing
WHY NOT FORECAST CROSS-SECTIONAL
ALPHAS DIRECTLY?
We built up our entire forecasting methodology in Chap.10 from
time series analysis. We have now spent considerable effort adapt-
ing that methodology to the more standard application involving
cross-sectional scores. Why don’t we just apply the forecasting
methodology directly to the cross-sectional information? Can’t we
simply discard all the time series machinery and focus directly on
cross-sectional behavior?
In the simple case where we have N asset returns and N
signals, all at one time, Eq. (11.1) reduces to
b, a KC ‘ Stdcs{8,,}
, ZCS,n
(11.16)
where Stdc{0,,} is the cross-sectional volatility of the residual returns.
For any given time f, it is just a constant. For all practical purposes,
Eq. (11.16) is equivalent to Eq. (11.14).
That result may be reassuring, but the analysis is overly sim-
plistic. Estimating expected exceptional returns from only one cross-
sectional panel of data is fraught with problems. In one month,
industries will probably explain much of the cross-sectional varia-
tion in returns. The next month, the same will be true, but the
industries will be different. This month, Internet stocks. Next
month, health care. The following month, banks. The refining pro-
cess must, of necessity, analyze both time series and cross-sectional
information. We need to know what we can consistently forecast
over time.
In general, we must use both time series and cross-sectional
data in Eq. (11.1). We have chosen to attack the time series problem
first, and then add the complexity of cross-sectional data. As we
will see, the fully general case is too complex to handle exactly.
We must apply structure to tackle it.
MULTIPLE FORECASTS FOR EACH OF N
STOCKS
In Chap. 10, we explicitly handled the case of two forecasts for one
asset, and also described mathematically how to handle multiple
forecasts for an asset.
Advanced Forecasting
303
With some simplifying assumptions, the results from Chap. 10
apply in the case of multiple assets, asset by asset. The simplifying
assumptions are fairly restrictive. Each information source j has an
information coefficient vector IC;. The elements of IC; describe the
information coefficient asset by asset. For each information source,
a correlation matrix p; describes the signal correlations across assets.
The simplifying assumptions state that
(OG =e
(11.17)
p; =
(11.18)
Information source j exhibits the same information coefficient for
all assets, and the correlation of its signal across assets matches the
correlation of every other information source’s signal across assets.
Furthermore, we must assume that the correlation between every
Bin ANd gj, is just pj, a constant describing the correlation between
signals i and j. With these simplifying assumptions, we can apply
the results of Chap. 10, asset by asset. We still must remember that
the Chap. 10 results depend on time series scores and not cross-
sectional scores.
The technical appendix provides some further insight into
handling the general case of multiple forecasts for multiple assets.
If we are unwilling to accept the assumptions above, we need to
supply an alternative structure.
FACTOR FORECASTS
One standard way to apply structure to the case of multiple assets
is through a factor model. In particular, the arbitrage pricing theory
(APT) states that all return forecasts must assume the form
E{r} =X-m
(11.19)
where
r= Xb tu
(11.20)
and
m = E{b}
(11.20)
Typically, the problem of forecasting hundreds, if not thousands,
of asset returns reduces to a problem of forecasting a handful of
304
Information Processing
factor returns. Many institutional managers apply just such meth-
ods, as we saw in Chap 7.
In the typical case, some of the APT factors immediately
suggest factor forecasts. For example, some factors may generate
consistent returns month after month. We always want portfolios
that tilt toward these factors. Other factors may require timing,
i.e., their returns vary from positive to negative, with no implied
tilt direction.
We have observed many investment managers, therefore, face
the following problem: They can forecast one or a few factors, but
they have no information (in their opinion) about the other factors.
Should they set the other factor forecasts to zero?
We can apply the basic forecasting formula to solve this prob-
lem. Let’s assume that we have a signal g, to forecast b;. We know
how to refine g, to forecast b;. What should we expect for the
other factors?
Using the basic forecasting formula,
E{bj|¢1} = Et) + Cov{b,g,}
« Var Hei} - (g, — Efg})
(11.22)
How do we calculate the covariance and correlation of b; and gj?
Let’s begin by assuming that g; contains some information about
b,, plus noise:
g =IC’-b,
+ IC: 162
SOr
(11.23)
where Z has mean 0 and standard deviation 1 and is uncorrelated
with b, (and all other b;). Using Eq. (11.22), we can calculate
Cov{bj,g;} = IC? - Cov{b;,b;}
(11.24)
NG pee,
‘i
Substituting this back into Eq. (11.22), and assuming that E{b;} = 0
we find
J
E{bi\g,} = IC Py O° (eran
(11.25)
=IC-
py +z
According to Eq. (11.25), if we forecast E{b,1g,} 4 0, We should not
set E{bj1g,} = 0.
Advanced Forecasting
305
TABLE
113
We have empirically tested Eq. (11.25) in the following case.
We used the BARRA U.S. Equity model (version 2), and assumed
that we had explicit information only for the book-to-price (B/P)
factor. We then looked at three variants of a B/P
strategy:
A. Bet only on B/P.
B. Use the information about B/P
to also bet on other risk
indices.
C. Use B/P information to bet only on other factors.
Case C is rather perverse, but an interesting empirical test of the
idea. Using data for the 5-year period from May 1990 through April
1995, we found the results in Table 11.3.
We can observe from Table 11.3 that using the information
about b,; to bet on b; improves the performance of the signal. We
can also observe that even perverse strategy C, using information
about b, to bet on factors other than b,, exhibits a high information
ratio. We would also expect the squared information ratio for strat-
egy B to roughly match the sum of the squared information ratios
for strategies A and C. This is true.
UNCERTAIN INFORMATION COEFFICIENTS
This and the previous chapter have discussed how to refine raw
signals based on expectations, volatility, and skill, with skill mea-
sured by the information coefficient. We have also discussed how
to combine signals with differing information coefficients.
A common practical problem, however, involves uncertainty
in the information coefficients themselves, and how this should
influence the refined signals. For example, how should we combine
two signals with equal estimated IC if one has much higher estima-
306
Information Processing
tion errors? We would expect to weight the signal with the more
certain IC more heavily. None of our machinery so far implies that
answer, however. In fact, it isn’t obvious how to account for IC
estimation errors in our framework.
This is because our methodology so far has explicitly ignored
this problem. Achieving algebraic results requires assuming that
we know something. In our analysis so far, we have assumed that
we know the ICs.
Fortunately, some modest tweaking of our Bayesian methodol-
ogy can handle the case of uncertain ICs. We will explicitly handle
the case of one signal, but will discuss the more general result.
We will use regression methodology to analyze the problem.
We are attempting to forecast residual returns @(t) with signal
g(t). We will refine the signal via regression:
O(t)
=a + b> ot) + E(t)
(11.26)
For this analysis, we will assume that 0(t) and g(t) both have mean
0. Hence
a= 0
(11.27)
T
aa
>) 0
+ eb
= Cov{6,
wi
VaR f=) —_____
(11.28)
Uy
> 20
pil
We will handle uncertainty in the estimated IC by adding a prior,
b, to the regression, Eq. (11.26). We now have
6(1)
gQ1)
€9(1)
adi
eet
PEE
fo uolbe.
11.29
0(T)
g(T)
€9(T)
Cae
b
1
Ep
where we will weight the observations of @(t) by 1/w}, and the
prior by 1/w;, where w, is the standard deviation of €,(t) and o, is
the standard deviation of ¢,.
?
Equation (11.29) displays a useful mathematical trick. We can
Advanced Forecasting
307
add a prior as an additional “observation” in the standard regres-
sion. With the above weights, this corresponds to a maximum
likelihood analysis, with the likelihood of each residual return ob-
servation being combined with the likelihood of the observed coeffi-
cient, given the prior.
Solving this regression for the adjusted coefficient b’ leads to
T
(1/«3) - SY 0() - gt) + (6/03)
bo =
4
______
(11.30)
(1/03)
- S* 9(t) + (/ef)
f= 1
We will use a prior of b = 0. The technical appendix will show
[following Connor (1997)] that Eq. (11.30) then reduces to
At
o  |\T+ G/T EIR
RO 0
(11.31)
which involves the expected R’ statistic from the (no prior) regres-
sion. Since this R’ statistic should equal IC’, and hence be quite
small, we can approximate Eq. (11.31) as
b' = pay See 0
(11°32)
1
asic)
Equation (11.32) describes a shrinkage of the original estimate b
to account for uncertainty. With a large number of observations
T or a high information coefficient, we remain close to the naive
estimate b. But with fewer periods, or with lower information
coefficients, we shrink closer to zero. Table 11.4 shows the shrink-
age as a function of IC and months of observation T. The shrinkage
is quite significant even for very good signals observed over long
periods of time. For poor signals, the adjusted coefficient shrinks
to zero (the prior).
Note that Eq (11.31) applies the Bayesian shrinkage to the
regression coefficient b, not directly to the IC. As we will show in
the technical appendix, uncertainty in the IC will typically dominate
overall uncertainty in the regression coefficient.
ie
308
Information Processing
Seen ee ee ee eee eee eee eee ee eee
eal
TABLE
11.4
Information Coefficient
Months
H
0.05
36
0.08
60
0.13
90
0.18
0.23
0.38
What about the case of multiple signals? The same Bayesian
shrinkage applies, but with the marginal R’ statistics replacing the
total R’ statistic in Eq. (11.31). With multiple signals, these marginal
R’ statistics attribute the total R’ to the signals. Each signal’s mar-
ginal R* equals the total R* minus the R’ achieved with that coeffi-
cient set to zero. These marginal R’ statistics sum to the total R’
statistic. This methodology places a premium on parsimony. A
new signal with small marginal explanatory power will experience
substantial shrinkage.
SUMMARY
This chapter began with the foundations built in Chap. 10—how
to refine forecasts for one asset—and grappled with the typical and
more complicated cases of multiple assets and uncertainties in
estimated ICs. The basic forecasting formula applies to multiple
assets, but typically requires so many separate estimates that it
demands additional structure. Investment managers often rely on
cross-sectional scores. In many cases, refined exceptional returns
are directly proportional to cross-sectional scores.
When forecasting factor returns (e.g., in APT models), use
your available information
to forecast all the factors.
The greater the uncertainty in our estimated IG the more we
will shrink the IC toward zero.
Advanced Forecasting
309
PROBLEMS
1. Signal 1 and signal 2 have equal IC, and both exhibit
signal volatilities proportional to asset volatilities. Do
the two signals receive equal weight in the forecast
exceptional return?
2. What IR would you naively expect if you combined
strategies A and C in Table 11.3? Why might the
observed answer differ from the naive result?
3. How much should you shrink coefficient b, connecting
raw signals and realized returns, estimated with R* =
0.05 after 120 months?
REFERENCES
Black, Fisher, and Robert Litterman. “Global Asset Allocation with Equities, Bonds,
and Currencies.” Fixed Income Research, Goldman, Sachs & Co., New York,
October 1991.
Connor, Gregory. “Sensible Return Forecasting for Portfolio Management.” Finan-
cial Analysts Journal, vol. 53, no. 5, 1997, pp. 44-51.
Grinold, Richard C. “Alpha Is Volatility Times IC Times Score, or Real Alphas
Don’t Get Eaten.” Journal of Portfolio Management, vol. 20, no. 4, 1994, pp. 9-16.
Kahn, Ronald. “Alpha Analytics.” BARRA Equity Research Seminar, Pebble Beach,
Calif., June 1995.
TECHNICAL APPENDIX
In this appendix, we examine in more detail the analysis of forecasts
for multiple assets, discuss an alternative method for testing volatil-
ity scaling, and treat in more detail the case of uncertain informa-
tion coefficients.
One Forecast for Each of N Assets
Consider the case with K = N forecasts, one forecast g, for each
asset return r,. We will make the assumption that the IC is the
same for each forecast:
Cov{rn8n} = IC - w, + Stdrslg,}
(11A.1)
310
Information Processing
What about the covariance of r,, with g,,? We will assume that r,, is
correlated with g,, only through g,, 1.e.,
Cov {tin} = IC + On * Pum * Stdrsl Sm}
(11A.2)
where p,,,, measures the correlation of g,, and g,,. In matrix notation,
Covirg} = IC-w-p-
Std
(11A.3)
Var{g} = Std - p- Std
(11A.4)
where @ and Std are diagonal matrices with {w,} and {Stdlg,]},
respectively, on the diagonal. Substituting this into the basic fore-
casting formula [Eq. (11.1)], we find
b =IC-w-:
Std" - (g — E{g})
CAS)
Hence, each forecast takes on the form
atari
(er: ay
h, = IC:
w, (
Sida
(11A.6)
Two Forecasts for Each of N Assets
Next, consider the case where K = 2N. Now g = {g;,g)}, with two raw
forecasts for each stock. We will make the simplifying assumptions
P
PRP). Sta
(11A.7)
Var{g} = Std -
Pi2° P
p
Covirg}
= -[IC,-I
IC): 1- ’ i
Std
(11.8)
Thus the correlation matrix for the g, is identical to the correlation
matrix for the g,. The correlation between every g;, and g>, ig de-
scribed by the scalar constant p,. The correlation between every
gin and 1, is described by the scalar constant IC,, and the correlation
between every >, and r, is described by the scalar constant IC).
We can substitute Eqs. (11A.7) and (11A.8) into the basic fore-
casting formula, to find
,
IG = pv: )
)
(S
= (vie® i)
ry) (Satu JG I
iene
-I
:
(11A.9)
b=
+e
0)
Std
igs Fie]
Advanced Forecasting
311
Once again the refined exceptional forecast takes on the form vola-
tility - IC - score. In this case, we adjust the information coefficients
based on the correlation between the forecasts g, and gp.
Multiple Forecasts for Each of N Assets
The general case is easier to understand if we transform the raw
forecasts g into a set of uncorrelated (orthogonal) forecasts y. We
can always write
Var{g} = H’: H
(114.10)
y = (H’)’- [g — E{g}]
(11A.11)
where the y are standardized and uncorrelated raw forecasts:
E{y} = 0, Var{y} = I. We can also show that
Covirg} = Coviry}
-H
(11A.12)
and so
& = w - Corr{ry} - y
(11A.13)
Thus the general result, that the refined forecast has the form volatil-
ity - IC - score, still holds, although in the general case it involves
transformed scores y and an IC matrix Corr{r,y}. To go beyond this
result, we need to impose more structure on this correlation matrix.
Testing Alpha Scaling
A separate approach to testing whether we have appropriately
scaled alphas by volatility is to look at the amount of risk we take
per asset. Assuming uncorrrelated residual risks,
Ay
CRE
(11A.14)
R
n
hg,(n) =
Here is an alternative empirical procedure for combining K forecasts for each of N
assets. First estimate K factor portfolio returns, one for each forecast for the N
assets. Each factor portfolio should control exposure to the other K — 1 factors.
Then choose an optimal set of K weights to maximize the information ratio of the
portfolio of factor portfolios. Use these to determine the weights on the K
forecasts for each of the N assets.
312
Information Processing
Using the forecasting rule of thumb,
IGez,
hg,(n) = EAGT
(11A.15)
and the portfolio risk becomes
ea
2 =
.
2
ws
(; | > Ze
(11A.16)
Equation (11A.16) implies that we expect equal risk contributions
from each asset, since E{z’} = 1 for each asset. So, for example, we
could define buckets of equal numbers of assets, based on volatility,
and calculate the contribution to residual variance from each
bucket. Each bucket should contain a sufficient number of assets
to control the sampling error around E{z’}.
If different buckets exhibit different contributions to risk, then
either the volatility scaling is incorrect or we have imposed different
information coefficients for different buckets.
This method also applies to buckets defined on the basis of
other attributes.
Uncertain ICs
The main text of the chapter analyzed how to shrink estimated ICs
based on their estimation error. The technique actually focused on
the regression coefficient b:
(ft)
=a +b- g(t) + elt)
(114.17)
where
p — Covieg} _ IC +
(11A.18)
Var{g}
— Std{g}
and not directly on the IC. However, we will show that the estima-
tion error in the IC dominates the overall estimation error in b.
Hence it is reasonable to assume that we are applying the Bayesian
shrinkage to the IC.
Advanced Forecasting
313
Given Eq. (11A.18), how do estimation errors influence our
estimate of b? Using A to denote uncertainties in the variables,
GS
IC: aw
Ab = AIC: Sale) fae Ceecea aie arte) AStd{g}
(11A.19)
Ab_ AIC | Aw _ AStd{g}
yen
ee a sido}
So
Hence
Var t =
Var MG
+ Var oo
(11A.21)
b
yen
ron)
+ Var Res + covariances
We can analyze Eq. (11A.21) in more detail if we assume that
1. The errors are uncorrelated (so the covariance terms
disappear).
2. We have large sample sizes.
3. All errors are normally distributed.
We can then use the results for standard error variances for sample
standard deviations and correlations:
2
a
(11A.22)
(i =2p7)?
N
Var{Ac} =
Var{Ap} =
(11A.23)
Substituting these results in Eq. (11A.21), assuming IC << 1, and
simplifying leads to
.
Ab
1
1
vary 2
7 i ie T Bee
T
(11A.24)
where T measures the number of months of observations. The first
term on the right-hand side of Eq. (11A.24) is the contribution from
uncertainty in the IC. The second term is the contribution from
uncertainty in w and Std{g}. Since IC << 1, the error in the IC
dominates the error in the regression coefficient.
314
Information Processing
Exercises
. We are following N assets but have a forecast only for
asset 1 (N assets, K = 1). Should we set all other
forecasts equal to their consensus values (, = 0,1 =
2,..., N)? How should the N forecasts differ from their
consensus values based on this one forecast?
. Compare the result from Exercise 1 to the CAPM result
for a forecast of exceptional market return. Black and
Litterman have pursued these ideas in the context of
international asset allocation in their international CAPM
model.
. How could you connect the best linear unbiased estimate
combining K forecasts for each of N assets to an
approach estimating factor portfolios for each of the K
forecasts and then optimally combining those factor
portfolios to maximize the overall information ratio?
Application Exercise
. Compute the coefficient c, for at least two signals. This
requires a cross-sectional set of signals and residual
volatilities. If the signals had equal ICs, what does this
imply about their relative weighting?
