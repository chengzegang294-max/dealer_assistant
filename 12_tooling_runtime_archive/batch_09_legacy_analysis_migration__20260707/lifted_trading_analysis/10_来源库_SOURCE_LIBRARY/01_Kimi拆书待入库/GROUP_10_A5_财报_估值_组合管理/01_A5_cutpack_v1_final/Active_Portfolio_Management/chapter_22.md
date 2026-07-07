# Chapter 22: Summary

- **book_name**: Active Portfolio Management
- **main_source**: pdf
- **cross_check_source**: none
- **pdf_role**: main_text_source
- **split_scope**: pages 599-632

---

CHAPTER
22
Summary
In Active Portfolio Management, we have attempted to provide a
comprehensive treatment of the process of active management,
covering both basic principles and many practical details. In sum-
mary, we will review what we have covered, the major themes of
the book, and what is now left for the active manager to do.
WHAT WE HAVE COVERED
The book began by covering the foundations: the appropriate
framework for active management, and the basic portfolio theory
required to navigate in that framework. The active management
framework begins with a benchmark portfolio and defines excep-
tional returns relative to that benchmark. Active managers seek
exceptional returns, at the cost of assuming risk. Active managers
trade off their forecasts of exceptional return against this additional
risk. We measure value added as the risk-adjusted exceptional re-
turn. The key characteristic measuring a manager’s ability to add
value is the information ratio, the amount of additional exceptional
return he or she can generate for each additional unit of risk. The
information ratio is both a figure of merit and a budget constraint.
A manager’s ability to add value is constrained by her or his
information ratio.
Given this framework, portfolio theory connects exceptional
return forecasts—return forecasts which differ from consensus ex-
577
578
Implementation
pected returns—with portfolios that differ from the benchmark. If
a manager’s forecasts agree with the consensus, that manager will
hold the benchmark. To the extent that a manager’s forecasts differ
from the consensus, and to the extent that his or her information
ratio is positive, that manager will hold a portfolio that differs from
the consensus.
The information ratio arises repeatedly as the variable govern-
ing active management, and the fundamental law of active manage-
ment provides insight into its components. High information ratios
require both skill and breadth. Skill is captured by information
coefficients—correlations between a manager’s forecasts of excep-
tional return and their subsequent realization. Breadth measures
the manager’s available number of independent forecasts per year.
Breadth allows the manager to diversify his or her imperfect fore-
casts of the future. High information ratios may combine low skill
with large breadth, high skill with small breadth, or something
in between.
With the framework, basic theory, and insights in place, the
book went on to cover the process of active management. Day-to-
day active management begins with the processing of raw signals
into exceptional return forecasts and moves on to implementation:
portfolio construction, trading, and subsequent performance analy-
sis. The forecasting process may depend on a factor model (like
APT) or on individual stock valuation models. Forecasting includes
the processing of raw information into refined alpha forecasts.
Active management also requires research in order to find valuable
information. Once again, a process exists for analyzing the informa-
tion content of potential signals and refining them for use in ac-
tive management.
THEMES
We hope that several themes have strongly emerged from the text
and the equations. First, active management is a process. Active
management begins with raw information, refines it into forecasts,
and then optimally and efficiently constructs portfolios balancing
those forecasts of return against risk. Active management should
consist of more than merely buying a few stocks you think will go
up. The raw information may be the list of stocks you think will
Summary
579
go up, and it certainly need not be derived from a quantitative
model. But starting with this information, active management is a
disciplined approach to acting on that information, based on a
rigorous analysis of its content.
A second theme of the book is that active management is
forecasting, and a key to active manager performance is superior
information. In fact, most of this book describes the machinery
for processing this superior information into portfolios. If your
forecasts match the consensus, or if your forecasts differ from the
consensus but contain no information, this machinery will lead you
back to the benchmark. Only as you develop superior information
will your portfolio deviate from the benchmark.
The third strong theme of the book is that active managers
should forecast as often as possible. The fundamental law shows
that the information ratio depends on both skill and breadth, the
number of independent forecasts or bets per year. Given the realities
(and difficulties) of active management, the best hope for a large
information ratio is to develop a small edge and bet very often—e.g.,
forecast returns to 500 stocks every quarter. In this search for
breadth, we also advocate using multiple sources of information—
the more the better. In line with this theme of breadth, the reader
should also notice that we are not strong proponents of benchmark
timing. The fundamental law shows that benchmark timing is sel-
dom fruitful.
A fourth, and to some readers surprising, theme that we hope
has emerged is that mathematics cannot overcome ignorance. If
your raw information is valueless, no mathematical transformation
will help. In this book, we have presented the mathematics for
investing efficiently based on superior information from any source.
We have tried to avoid wherever possible the use of mathematics
to obscure lack of information.
WHAT’S LEFT?
We have described the process and machinery of active manage-
ment, starting from superior information. Much of this machinery
is available from vendors, or available to implement on your own,
if you wish. But clearly, the focus of the active manager, and what
580
Implementation
this book ultimately can’t help with, is the search for superior infor-
mation.
Seeking superior information in this zero-sum game is lonely.
Jack Treynor once described the process this way: If he identifies
a stock he thinks will go up, he talks to his wife about it. If she is
enthusiastic, he asks his barber. From there, he discusses the idea
with his accountant and his lawyer. If they all agree it’s a great
idea—he doesn’t buy the stock. If everyone agrees with him, the
price must already reflect his insight.
We have covered where to look for superior information, we
have discussed forecasting factor returns and forecasting asset spe-
cific returns, and we have described particular information sources
that have proven valuable in the past. These may still be valuable
now, but over time they must begin to inform the consensus ex-
pected returns. New, clever ideas will always help the active
manager.
Once you have found superior information, this book provides
the best path to success with active management.
APPENDIX
A
Standard Notation
This appendix covers standard notation used repeatedly through-
out the book. It does not cover notation introduced and used only
in one particular section.
In general, we represent vectors in lowercase bold letters and
matrices in uppercase bold letters. To refer to an element of a vector
or matrix, we use subscripts and do not use bold, e.g., r,, the
excess return to asset n, is the nth element of r, the vector of asset
excess returns.
REALIZED RETURNS
R
Ip
Re
pe
ae
0
b
u
total returns [(P,ew + dividend) / Pa)
risk-free rate of return
risk-free total return
excess returns
residual returns
factor returns
specific returns
EXPECTED RETURNS
expected excess returns
long-term expected excess returns
expected residual returns
expected exceptional returns
expected factor returns
total risk
residual risk
active risk
asset betas
portfolio beta (exposure to benchmark risk)
active portfolio beta
581
582
Appendix A
Vv
asset-by-asset covariance matrix
F
factor covariance matrix
A
specific variance matrix
PORTFOLIOS AND ASSETS
hp __ portfolio holdings
hpg _ residual portfolio holdings
hp,
active portfolio holdings
X
matrix of all assets’ exposures to factors
Xp
vector of portfolio P’s exposure to factors
PERFORMANCE AND VALUE ADDED
Ar
total risk aversion
Asr
benchmark timing risk aversion
Ae
residual risk aversion
ha
active risk aversion
INS
short-term risk aversion
SR
Sharpe ratio
IR
information ratio
IC
information coefficient
BR
breadth
PORTFOLIO NAMES
benchmark portfolio
market portfolio
fully invested portfolio with maximum Sharpe ratio
fully invested portfolio with minimum risk
v
minimum-risk portfolio with expected return = 1
minimum-risk portfolio with a = 1
portfolio with minimum expected {R}}
ies
GO)
Aes
1d
OTHER
e
vector of ls
~
APPENDIX
B
Glossary
This glossary defines some of the most commonly used terms in
the book.
Active management
The pursuit of investment returns in excess of a speci-
fied benchmark.
Active return
Return relative to a benchmark. If a portfolio’s return is 5 percent,
and the benchmark’s return is 3 percent, then the portfolio’s active return is
2 percent.
Active risk
The risk (annualized standard deviation) of the active return. This
is also called the tracking error.
Alpha
The expected residual return. Outside the pages of this book, alpha is
sometimes defined as the expected exceptional return and sometimes as the real-
ized residual or exceptional return.
Arbitrage To profit because a set of cash flows has different prices in different
markets.
Benchmark A reference portfolio for active management. The goal of the active
manager is to exceed the benchmark return.
Beta
The sensitivity of a portfolio (or asset) to a benchmark. For every 1 percent
return to the benchmark, we expect a B percent return to the portfolio.
Breadth
The number of independent forecasts available per year. A stock picker
forecasting returns to 100 stocks every quarter exhibits a breadth of 400 if each
forecast is independent (based on separate information).
Certainty equivalent return
The certain (zero-risk) return an investor would
trade for a given (larger) return with an associated risk. For example, a particular
investor might trade an expected 3 percent active return with 4 percent risk for
a certain active return of 1.4 percent.
Characteristic portfolio
A portfolio which efficiently represents a particular asset
characteristic. For a given characteristic, it is the minimum-risk portfolio with the
portfolio characteristic equal to 1. For example, the characteristic portfolio of asset
betas is the benchmark. It is the minimum-risk B = 1 portfolio.
Common factor
An element of return that influences many assets. According
to multiple-factor risk models, the common factors determine correlations between
asset returns. Common factors include industries and risk indices.
583
584
Appendix B
Descriptor A variable describing assets, used as an element of a risk index. For
example, a volatility risk index, distinguishing high-volatility assets from low-
volatility assets, could consist of several descriptors based on short-term volatility,
long-term volatility, systematic and residual volatility, etc.
Dividend discount model
A model of asset pricing, based on discounting the
future expected dividends.
Dividend yield
The dividend per share divided by the price per share. Also
known as the yield.
Earnings yield
The earnings per share divided by the price per share.
Efficient frontier
A set of portfolios, one for each level of expected return, with
minimum risk. We sometimes distinguish different efficient frontiers based on
additional constraints, e.g., the fully invested efficient frontier.
Exceptional return
Residual return plus benchmark timing return. For a given
asset with B = 1, if the residual return is 2 percent and the benchmark portfolio
exceeds its consensus expected returns by 1 percent, then the asset’s exceptional
return is 3 percent.
Excess return
Return relative to the risk-free return. If an asset’s return is 3
percent and the risk-free return is 0.5 percent, then the asset’s excess return is
2.5 percent.
Factor portfolio
The minimum-risk portfolio with unit exposure to the factor
and zero exposure to all other factors. The excess return to the factor portfolio is
the factor return.
Factor return
The return attributable to a particular common factor. We decom-
pose asset returns into a common factor component, based on the asset’s exposures
to common factors times the factor returns, and a specific return.
Information coefficient
The correlation of forecast returns with their subsequent
realizations. A measure of skill.
Information ratio
The ratio of annualized expected residual return to regidual
risk, a central measurement for active management. Value added is proportional
to the square of the information ratio.
Market
The portfolio of all assets. We typically replace this abstract construct
with a more concrete benchmark portfolio.
x
Normal A benchmark portfolio.
es ee
ee Se
Passive management
Managing a portfolio to match (not exceed) the return of
a benchmark.
Payout ratio
The ratio of dividends to earnings. The fraction of earnings paid
out as dividends.
Regression
A data analysis technique which optimally fits a model based on
the squared differences between data points and model fitted points. Typically,
regression chooses model coefficients to minimize the (possibly weighted) sum
of these squared differences.
Residual return
Return independent of the benchmark. The residual return is
the return relative to beta times the benchmark return. To be exact, an asset’s
residual return equals its excess return minus beta times the benchmark excess
return.
Residual risk
The risk (annualized standard deviation) of the residual return.
Risk-free return
The return achievable with absolute certainty. In the U.S. mar-
ket, short-maturity Treasury bills exhibit effectively risk-free returns. The risk-free
return is sometimes called the time premium, as distinct from the risk premium.
Risk index
A common factor typically defined by some continuous measure,
as opposed to a common industry membership factor defined as 0 or 1. Risk
index factors include size, volatility, value, and momentum.
Risk premium
The expected excess return to the benchmark.
R squared A statistic usually associated with regression analysis, where it de-
scribes the fraction of observed variation in data captured by the model. It varies
between 0 and 1.
Score
A normalized asset return forecast. An average score is 0, with roughly
two-thirds of the scores between —1 and 1. Only one-sixth of the scores lie above 1.
Security market line
The linear relationship between asset returns and betas
posited by the capital asset pricing model.
Sharpe ratio
The ratio of annualized excess returns to total risk.
Skill
The ability to accurately forecast returns. We measure skill using the infor-
mation coefficient.
Specific Return
The part of the excess return not explained by common factors.
The specific return is independent of (uncorrelated with) the common factors and
the specific returns to other assets. It is also called the idiosyncratic return.
Specific risk
The risk (annualized standard deviation) of the specific return.
Standard error
The standard deviation of the error in an estimate; a measure
of the statistical confidence in the estimate.
Systematic return
The part of the return dependent on the benchmark return.
We can break excess returns into two components: systematic and residual. The
systematic return is the beta times the benchmark excess return.
586
Appendix B
Systematic risk
The risk (annualized standard deviation) of the systematic
return.
t statistic
The ratio of an estimate to its standard error. The t statistic can help test
the hypothesis that the estimate differs from zero. With some standard statistical
assumptions, the probability that a variable with a true value of zero would exhibit
a t statistic greater than 2 in magnitude is less than 5 percent.
Tracking error
See active risk.
Value added
In the context of this book, the utility, or risk-adjusted return,
generated by an investment strategy: the return minus a risk aversion constant
times the variance. The value added depends on the performance of the manager
and the preferences of the owner of the funds.
Volatility
A loosely defined term for risk. In this book, we define volatility as
the annualized standard deviation of return.
Yield
See dividend yield.
APPENDIX
C
Return and
Statistics Basics
This appendix will very briefly cover the basics of returns, statistics,
and simple linear regression. We provide a list of basic references
at the end.
RETURNS
We define returns over a period t, of length At, which runs from
t tot + At. If the asset’s price at t is P(t) and at t + At is P(t + Af),
and the distributions’ over the period total d(t), then the asset’s
total return is
PEE AD eat)
iG
PO)
(C1)
The asset’s total rate of return is
rr(t) = R@) -—1
(G2)
We can also calculate a total return R,- and total rate of return i;
for the risk-free asset (e.g., a Treasury bill of maturity At). Then we
define the asset’s excess return as
rt)
RO)
BA)
(C.3)
or
r(t) = rr(t) — ip(t)
(C.4)
Throughout this book, we focus mainly on excess returns and
decompositions of excess returns. We occasionally use total returns,
and never explicitly use total rates of return.
Return calculations become more difficult where they involve
stock splits, stock dividends, and other corporate actions. We will
not explicitly treat those critical details here.
We label the distributions over the period d(t). If the period At is relatively long and a
cash distribution occurs in midperiod, we could assume reinvestment of the
distribution over the rest of the period at either the risk-free rate of return or the
asset rate of return.
587
588
Appendix C
STATISTICS
Here we will briefly define how to calculate means, standard devia-
tions, variances, covariances, and correlations, and briefly discuss
their standard errors. Let’s start with a set (a sample) of observed
excess returns to stock n, 1,(t), where t = 1,..., T. So we have
observed stock n for T months. The mean return over the period
(the sample mean) is 7,
7, = (t) ado
(C5)
The sample variance is
T
Vari{r,} zz (44
; > [r,,(t) = ile
(C.6)
t=1
and the sample standard deviation is
Std{r,} = V Vari{r,,}
(G7)
Note the use of T — 1 in the denominator of Eq. (C.6). We use
T — 1 instead of T to calculate an unbiased estimate of the variance,
on the assumption that we are estimating both the sample mean
and the sample variance. If we knew the mean with certainty,
independent of the sample mean, we would use T in the denomina-
tor of Eq. (C.6). We recommend limited use of statistics in very-
small-sample situations, where using T versus T — 1 can lead to
very different results.
To complete our discussion of basic statistical calculations,
consider the excess returns to another asset m, r,,(t), t = 1,.»., T.
The covariance of returns to assets n and m is
10
Comite a (4)
, >: [r,(t) > Fal : [n(t) ay fal
(C.8)
t=1
Note that
Cov{ratn} = Var{ra}
(C.9)
and
Cov{tin
tn} = CovttaS
mt
(C.10)
Return and Statistics Basics
589
Finally, the correlation of returns to assets n and m is
sen
Covinen)
Corrttitn} = SF dir) Staal
(C.11)
STANDARD ERRORS
The standard error of an estimate is the standard deviation of the
errors in its estimation, a basic measure of its accuracy. Assuming
that the errors in the estimate are normally distributed, the standard
error for the estimated mean is
_ Stdfr}
VT
The standard error of the estimated standard deviation is approxi-
mately
SE{r}
(C.12)
seta) ~ SU
and the standard error of the estimated variance is approximately
(G13)
SE{Var{r}} ~ Var{r} - 2
(C.14)
These approximations become more exact in the limit of large sam-
ple size, i-e., very large T.
SIMPLE LINEAR REGRESSION
Throughout the book, we make extensive use of regression analysis.
The simplest type of regression in the book estimates betas by
regressing excess returns against market returns:
r,(t) = QA, uw B,, j Tm t) at e,,(f)
(C.15)
Simple linear regression (OLS, or ordinarily least squares) estimates
a, and 8, by minimizing the sum of squared errors (ESS):
T
ESS = > €2(t)
(C.16)
t=1
590
Appendix C
The estimate of B,, is
Led Cov{n1 mit}
Bn =
Vartraucl
Sue)
and that of a, is
OQ, =f — Be: baat
(C.18)
These results use sample estimates of means, variances, and
covariances. In the book, we generally define betas using Eq. (C.17),
but with variances and covariances forecast using a covariance
matrix.
The R? of the regression is defined as
Var{e,,}
A
Gay
LS
Sp
Vari{r,,}
(
)
Another useful result of basic regression is that the errors ¢,(t)
are uncorrelated with the excess returns 1,(t):
Covir,,€,} = 0
(C.20)
More general regression analysis can involve more indepen-
dent variables and use weighted sums of squares, but the basic
idea is the same. The procedure estimates model parameters by
minimizing the (possibly weighted) sum of squared errors. The
resulting errors are uncorrelated with the returns. The definition
of R* remains the same. For a thorough introduction to regression
analysis, see the texts of Hoel, Port, and Stone; Hogg and Craig;
and Neter and Wasserman.
REFERENCES
Hoel, Paul G., Sidney C. Port, and Charles J. Stone. Introduction to Probability
Theory (Boston: Houghton Mifflin, 1971).
e
. Introduction to Statistical Theory (Boston: Houghton Mifflin, 1971).
Hogg, Robert V., and Allen T Craig. Introduction to Mathematical Statistics (New
York: Macmillan, 1970).
Neter, John, and William Wasserman. Applied Linear Statistical Models (Homewood
Ill.: Richard D. Irwin, 1974).
Pindyck, Robert S., and Daniel L. Rubinfeld. Econometric Models & Economic
Forecasts, 3d ed. (New York: McGraw-Hill, 1991).
“
IN DE X
Achievement, information ratio as measure
of, 112
Active management, 1-2
as dynamic problem, 574
as forecasting, 261
and information, 316-318
information ratio as key to, 125
objective of, 119-121
as process, 578-579
Active returns, 89, 102-103
Active risk, 50
After-tax investing, 575-576
Allocation (see Asset allocation)
Alpha(s), 91-92
benchmark-neutral, 384-385
characteristic portfolio of, 134
definition of, 111-112
and event studies, 331-332
extreme values, trimming, 382-383
and information horizon, 357-359
and information ratio, 127-129
and portfolio construction, 379-385,
411-413
risk-factor-neutral, 385
scaling, 311-312, 382
American Express, 20-21, 67
Arbitrage pricing theory (APT), 13, 26,
173-192
applications of, 187-190
assumptions of, 177-178
examples using, 178-181
and factor forecasting, 185-190,
194-197, 304
and Portfolio Q, 182-185
rationale of, 181-182
and returns-based analysis, 249
and valuation, 203-205, 207, 208,
218-220
and weaknesses of CAPM, 174-177
ARCH, 279-280
Asset allocation, 517-532
asset selection vs., 518
and construction of optimal portfolios,
525-532
and forecasting of returns, 520-525
Asset allocation (Cont.)
and international consensus expected
returns, 526-532
and liability, 575
out-of-sample portfolio performance,
532-533
technical aspects of, 536-539
as three-step process, 519-520
types of, 517
Asset valuation, 6-7
AT&T, 67
Attributed returns, cumulation of, 510-512
Attribution, performance, 498-503
Attribution of risk, 78, 81-83
Autocorrelation, 491
Aversion to total risk, 96
BARRA, 4, 51, 60, 63, 73, 184-186, 188, 252,
284, 435, 438, 449, 454, 500
Behavioral finance, 576
Benchmark risk, 100-101
Benchmark timing, 101-102, 491-493,
541-554
defining, 541-542
and forecasting frequency, 549-552
with futures, 543-544
and performance analysis, 552-554
technical aspects of, 555-558
and value added, 544-549
Benchmarks, 5, 88-90, 426-428
Beta, 13-16
forecasts of, 24
and information ratio, 125-127, 140
a priori estimates of, 493
Biased data, 450
Book-to-price ratios, 322, 323
Breadth, 6, 148
Capital asset pricing model (CAPM),
11-40, 487-489, 494, 496, 503, 560
assumptions of, 13-16, 27-28
characteristic portfolios in, 28-35
and efficient frontier, 35-37
and efficient markets theory, 17-18
example of analysis using, 20-21
and expected returns, 11, 18-19
591
592
Index
Capital asset pricing model (CAPM)
(Cont.)
and forecasting, 24
logic of, 16-17
mathematical notation in, 27
security market line in, 19-20
statement of, 16
as tool for active managers, 22-23
usefulness of, 22
and valuation, 203-205, 207, 208,
218-220
weaknesses of, 174-177
Cash flows:
certain, 200
uncertain, 200-201
Casinos, 150-151
Censored data, 450
Chaos theory, 280-281
Characteristic portfolios, 28-35
Commissions (see Transactions costs)
Comparative valuation, 244-248
Consensus expected returns, 11, 526-532
Constant-growth dividend discount
model, 231-232
Corporate finance, 226-228
Covariance, 206-207
Covariance matrices, 52, 64
Cross-sectional comparisons, 58, 296-302,
332-333, 484-487
Currency, 527-532
Data mining, 335-336
Descriptors, 63
Diaconis, Percy, 335
Dispersion, 402-408, 414-416
characterizing, 404
definition of, 402
example of, 403-404
managing, 404-408
Diversification, 184, 196-197
Dividend discount model(s), 7, 229-233,
242-244
beneficial side effects of, 244
certainty in, 229-230
constant-growth, 231-232
Golden Rule of, 235, 236
and returns, 242-244
three-stage, 239-242
uncertainty in, 230
“
Downside risk, 44-45
Duality theory of linear programming, 215
Efficient frontier, 35-37
Efficient markets theory, 17-18
Elementary risk models, 52-54
Event studies, 329-333, 343-345
Exceptional benchmark return, 91
Expectations, risk-adjusted, 203-206
Expected cash flows, 201
Expected return:
and CAPM, 11, 18-19
components of, 90-93
and value, 207-210
Expected utility, 96
Factor forecasts, 303-305
Factor models, 194-197
Factor portfolios, 74
Factor-mimicking portfolios, 74
Fama-MacBeth procedure, 72-73
Financial economics, 1
Financial value, 227
Forecast horizon, 274-275
Forecasts/forecasting, 7, 261-285, 295-313
active management as, 261, 579
advanced techniques for, 278-285
alpha scaling, testing, 311-312
with ARCH/GARCH, 279-280
and asset allocation, 520-525
basic formula for, 287-290
and chaos theory, 280-281
and cross-sectional scores, 296-302
examples of, 290-292
factor forecasts, 303-305
frequency of, 549-552, 579
with genetic algorithms, 284-285
and intuition, 267-268
with Kalman filters, 280
with multiple assets/multiple forecasts,
271-275, 296
multiple forecasts for each of n assets,
302-303, 311
+
naive, 262
with neural nets, 281-283
with one asset/one forecast, 264-268
with one asset/two forecasts, 268-271
one forecast for each of n assets,
309-310
raw, 262
refined, 262-265, 268-275
and risk, 275-277
rule of thumb for, 265-268
with time series analysis, 278-279
Index
593
Forecasts / forecasting (Cont.)
two forecasts for each of n assets,
310-311
and uncertain information coefficients,
305-308, 312-313
Fractiles, 273-274
Fundamental law of active management,
147-168, 225, 550
additivity of, 154-157
assumptions of, 157-160
attributes of, 148
derivation of, 163-168
examples using, 150-154
and investment style, 161
statement of, 148
and statistical law of large numbers, 160
tests of, 160-161
usefulness of, 149-150
Futures, 543-544
GARCH, 279-280
General Electric, 47-50, 60, 63
Generalized least squares (GLS)
regressions, 73, 246, 249
Genetic algorithms, 284-285
Gini coefficient, 428
GLS regressions (see Generalized least
squares regressions)
Golden Rule of the Dividend Discount
Model, 235, 236
Growth, 231-239
and constant-growth dividend discount
model, 231-232
implied rates of, 235-236
with multiple stocks, 233-235
unrealistic rates of, 236-239
Heterokedasticity, 491
Historical alpha, 111
Historical beta, 111
Humility principle, 225
IBM, 47-50, 67
ICs (see Inforrnation coefficients)
Implementation (see Portfolio construction)
Implied growth rates, 235-236
Implied transactions costs, 459-460
Industry factors, 60-62
Information analysis, 7, 315-338
and active management, 316-318
and event studies, 329-333, 343-345
Information analysis (Cont.)
flexibility of, 318
pitfalls of, 333-338
and portfolio creation, 319-321
and portfolio evaluation, 321-329
technical aspects of, 341-345
as two-step process, 318
Information coefficients (ICs), 148
and information horizon, 354-362
uncertain, 305-308, 312-313
Information horizon, 347-363
and gradual decline in value of
information, 359-363
macroanalysis of, 348-353
microanalysis of, 353-357
and realization of alpha, 357-359
return/signal correlations as function
of, 371-372
technical aspects of, 364-373
Information ratio (IR), 5-6, 109, 132,
135-139
and alpha, 111-112, 127-129
and beta, 125-127, 140
calculation/approximation of, 166-168
empirical results, 129-132
as key to active management, 125
and level of risk, 116
as measure of achievement, 112
as measure of opportunity, 113-117
negative, 112
and objective of active management,
119-121
and preferences vs. opportunities,
121-122
and residual frontier, 117-119
and residual risk aversion, 122-124
and time horizon, 116-117
and value-added, 124-125
See also Fundamental law of active
management
Information-efficient portfolios, 341-342
Inherent risk, 107
Intuition, 267-268
Inventory risk model, 450-451
Investment research, 336-338
Investment style, 161
IR (see Information ratio)
Kalman filters, 280
Liabilities, 575
594
Linear programming (LP), 395-396
Linear regression, 589-590
Long/short investing, 419-441
appeal of, 438-439
and benchmark distribution, 426-428
benefits of, 431-438
capitalization model for, 427-431
controversy surrounding, 421
empirical results, 439-440
long-only constraint, impact of, 421-426
LP (see Linear programming)
Luck, skill vs., 479-483
Magellan Fund, 43-44, 46
Major Market Index (MMI), 65-67,
235-236, 268, 488
Managers, 564-567
Marginal contribution for total risk, 78-81
factor marginal contributions, 79-80
sector marginal contributions, 80-81
Market microstructure studies, 447-448
Market volatility, 83-84
Market-dependent valuation, 207
Markowitz, Harry, 44
MIDCAP, 275-277
Mixture strategies, 365-369
MMI (see Major Market Index)
Modern portfolio theory, 3-4, 93
Modern theory of corporate finance,
226-228
Mosteller, Frederick, 335
Multiple-factor risk models, 57-60
cross-sectional comparisons in, 58
and current portfolio risk analysis,
64-67
external influences, responses to, 57-58
statistical factors in, 58-60
Naive forecasts, 262
Neural nets, 281-283
Neutralization, 383
Nixon, Richard, 357
Nonlinearities, 575
OLS (ordinary least squares) regressions,
246
Operational value, 227
Opportunity(-ies):
arbitrage, 214
“
information ratio as measure of, 113-117
preferences vs., 121-122
Index
Options pricing, 217-218
Ordinary least squares (OLS) regressions,
246
Out-of-sample portfolio performance,
532-533
Performance, 559-569
and manager population, 564-567
persistence of, 562-564
predictors of, 567-568
studies of, 560-562
Performance analysis, 477-507
and benchmark timing, 552-554
with cross-sectional comparisons,
484-487
and cumulation of attributed returns,
510-512
and definition of returns, 483-484
goal of, 477
portfolio-based, 497-506
returns-based, 487-497
risk estimates for, 512-513
and skill vs. luck, 479-483
usefulness of, 478
valuation-based approach to, 513-515
Persistence, performance, 562-564
Plan Sponsor Network (PSN), 484
Portfolio construction, 377-409
and alphas, 379-385, 411-413
and alternative risk measures, 400-402
and dispersion, 402-408, 414-416
inputs required for, 377-378
with linear programming, 395-396
practical details of, 387-389
with quadratic programming, 396-398
revisions, portfolio, 389-392
with screens, 393-394
with stratification, 394-395
technical aspects of, 410-418
techniques for, 392-398
y
testing methods of, 398-400
and transaction costs, 385-387
Portfolio-based performance analysis,
497-506
Predictors, 317
Preferences, 5-6, 121-122
Proust, Marcel, 336
PSN (Plan Sponsor Network), 484
Quadratic programming (QP), 396-398
Quantitative active management, 1, 3-4
Index
Rankings, 274
Raw forecasts, 262
Realized alpha, 111
Realized beta, 111
Refining forecasts, 262-265
and intuition, 267-268
with multiple assets /multiple forecasts,
271-275
with one asset/one forecast, 264-268
with one asset/two forecasts, 268-271
Regression analysis, 589-590
Residual frontier, 117-119
Residual returns, active vs., 102-103
Residual risk, 16-17, 50, 100-101, 122-124
Return forecasting, 7
Returns, 483-484, 587
Returns regression, 487-491
Returns-based analysis, 248-252
Returns-based performance analysis,
487-497
Revisions, portfolio, 389-392
Risk, 41-84
active, 50
and active vs. residual returns, 102-103
annualizing of, 49
attribution of, 78, 81-83
aversion to residual, 122-124
aversion to total, 96
benchmark, 100-101
definitions of, 41-46
downside, 44-45
elementary models of, 52-54
and forecasting, 275-277
indices of, 60, 62-63
and industry factors, 60-62
information ratio and level of, 116
inherent, 107
marginal impact on, 78-81
and market volatility, 83-84
and model estimation, 72-73
multiple-factor models of, 57-60, 73-75
over time, 575
residual, 16-17, 56, 100-101, 122-124
and semivariance, 44-45
as shortfall probability, 45-46
specific, 75-76
and standard deviation of return,
43-44, 47-52
structural models of, 55-56
total, 51
595
Risk (Cont.)
total risk and return, 93-99
and usefulness of risk models, 64-70
value at, 46
Risk analysis, 76-78
Risk estimates (for performance analysis),
512-513
Risk indices, 60, 62-63
Risk premium, 91
Risk-adjusted expectations, 203-206
Scheduling trades, 457-458
Science of investing, 1
Screens, 393-394
Security market line (in CAPM), 19-20
Semivariance, 44-45
Sharpe ratio (SR), 27, 32-33, 135-137, 487,
489-490
Shelf life (see Information horizon)
Shortfall probability, 45-46
Shrinkage factor, 433
Skill, luck vs., 479-483
S&P 500, 100, 275-277, 439, 445, 488, 505
Specific asset selection, 499
Specific risk, 75-76
Standard deviation, 43-44, 47-52
Standard errors, 589
Statistical law of large numbers, 160
Statistical risk factors, 58-60
Statistics, 588-589
Strategic asset allocation, 517
Strategy mixtures, 365-369
Stratification, 394-395
Structural risk models, 55-56
Style, investment, 161
t statistics, 325-327, 336-337
Tactical asset allocation, 517
Target portfolio, 464
Target semivariance, 45
Theory of Investment Value (John Burr
Williams), 229
Tick-by-tick data, 450
Time premium, 91
Time series analysis, 278-279
Timing, benchmark (see Benchmark
timing)
Total risk, 51, 96
Tracking error, 49
Trading, 447
implementation, strategy, 467-468
596
Index
Trading (Cont.)
optimization of, 473-475
as portfolio optimization problem,
463-467
Transactions costs, 385-387, 445-454,
458-459, 462-463, 574-575
analyzing /estimating, 448-454
implied, 459-460
and market microstructure,
447-448
See also Turnover
Treynor, Jack, 445, 580
Turnover, 446-447, 454-463
definition of, 456
and implied transactions costs,
459-460
and scheduling of trades, 457-458
and value added, 455-457, 471-472
Unrealistic growth rates, 236-239
Valuation, 109, 199-210, 225-257
and CAPM/APT, 218-220
comparative, 244-248
and dividend discount model, 229-233,
242-244
and expected return, 207-210
formula for, 202-203
Valuation (Cont.)
market-dependent, 207
and modeling of growth, 232-239
modern theory of, 199-201, 212-217
and modern theory of corporate
finance, 226-228
with nonlinear models/fractiles, 255-257
and options pricing, 217-218
of Portfolio S, 220-223
and returns-based analysis, 248-252
and risk-adjusted expectations, 203-206
and three-stage dividend discount
model, 239-242
Value added, 5-6, 99-101
and benchmark timing, 544-549
and information ratio, 124-125
objective for management of, 106-108
optimal, 139-140
and performance analysis, 493, 513-515
and turnover, 455-457
Value at risk, 46
Volatility:
cross-sectional, 302
market, 83-84
See also Risk
Volume-weighted average price (VWAP),
450
Wall Street Journal, 245
Williams, John Burr, 229
About
the
Authors
Richard C. Grinold, Ph.D., is Managing Director, Advanced Strategies and
Research at Barclays Global Investors. Dr. Grinold spent 14 years at BARRA,
where he served as Director of Research, Executive Vice President, and
President; and 20 years on the faculty at the School of Business Administration
at the University of California, Berkeley, where he served as the chairman of
the finance faculty, chairman of the management science faculty, and director
of the Berkeley Program in Finance.
Ronald N. Kahn, Ph.D., is Managing Director in the Advanced Active
Strategies Group at Barclays Global Investors. Dr. Kahn spent 11 years at
BARRA, including over seven years as Director of Research. He is on the
editorial advisory board of the Journal of Portfolio Management and the Journal of
Investment Consulting.
Both authors have published extensively, and are widely known in the
industry for their pioneering work on risk models, portfolio optimization, and
trading analysis, equity, fixed income, and international investing; and
quantitative approaches to active management.
ff
GRINOLD,
RICHARD C.
ACTIVE PORTFOLIO
MANAGEMENT
: QUANTITIVE
APPROACH FOR PROVIDING
HOUSTON PUBLIC LIBRARY
CENTRAL LIBRARY
(continued from front flap)
@ Methods to estimate transaction costs—
plus proven ways to reduce them
H Historical and empirical information on the
accuracy of risk models
@ Technical appendixes with more detailed
explanations of each chapter’s mathematics
@ Unique, real-world exercises to provide nuts-
and-bolts understanding of new concepts
Active Portfolio Management covers both the basic
principles and foundations, as well as the practical
details, of the process of active investment manage-
ment. It provides a proven approach to active
investment that is designed to beat not only unman-
aged indexes but also competing, less rigorous
management approaches.
About the Authors
Richard C. Grinold, Ph.D., is Managing Director,
Advanced Strategies and Research at Barclays
Global Investors. Dr. Grinold spent 14 years at
BARRA, where he served as Director of Research,
Executive Vice President, and President; and 20
years on the faculty at the School of Business
Administration at the University of California,
Berkeley, where he served as the chairman of the
finance faculty, chairman of the management
science faculty, and director of the Berkeley
Program in Finance.
Ronald N. Kahn, Ph.D., is Managing Director in
the Advanced Active Strategies Group at Barclays
Global Investors. Dr. Kahn spent 11 years at
BARRA, including over seven years as Director of
Research. He is on the editorial advisory board of
the Journal of Portfolio Management and the
Journal of Investment Consulting.
Both authors have published extensively, and are
widely known in the industry for their pioneering
work on risk models, portfolio optimization, and
trading analysis; equity, fixed income, and inter-
national investing; and quantitative approaches to
active management.
Cover Design: pinpoint design and advertising
Cover Illustration: tom white.images
and Finance
Se fislovatlye Approach to Portfolio Management—
Blending the Most Profitable
Angiytcal ane GuanGtanas Aspects
N PUBLIC LIBRARY
Professional aciaim "INIA
r*- Second iin
“Active Portfolio Managemen
ig the source of value-
added by
amoney manager.I
_
R O115b 6c4 b 3 ssional and academic
communities.”
ee:
—Professor William N. Goetzmann
Director, International Center for Finance
Yale University School of Management
“This new edition of Active Portfolio Management continues the standard of excellence estab-
lished in the first edition, with new and clear insights to help investment professionals.”
—William E. Jacques
Partner and Chief Investment Officer
Martingale Asset Management
“Active Portfolio Management offers investors an opportunity to better understand the balance
between manager skill and portfolio risk.”
—Scott Stewart
Portfolio Manager, Fidelity Select Equity® Discipline
Co-Manager, Fidelity Freedom® Funds
“This second edition will not remain on the shelf, but will be continually referenced by. both
novice and expert. There is a substantial expansion in both depth and breadth on the original.”
—Eric N. Remole
Managing Director, Head of Global Structured Equity
Credit Suisse Asset Management
“Active Portfolio Management, Second Edition, remains a readable yet theoretically and mathe-
matically rigorous book that one would expect from two such distinguished authors. I heartily
recommend this book.”
—Michael Even
Managing Director and Chief of Global Quantitative Analysis
Citibank Global Asset Management
“A more comprehensive examination of quantitative techniques for portfolio management
would be hard to find. Active Portfolio Management is an outstanding treatise on the methods
and techniques of measuring performance and risk control that is both rigorous and understand-
able.”
—Jon A. Christopherson
.
Research Fellow
Frank Russell Company
McGraw-Hill
S
A Division of The McGraw-Hill Companies
Visit us on the World Wide Web
at www.books.mcgraw-hill.com
|
39785"31661
x
|
90000
|
|
6
9"780070"248823
ISBN 0-07-02484
