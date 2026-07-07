# Chapter 17: Performance Analysis

- **book_name**: Active Portfolio Management
- **main_source**: pdf
- **cross_check_source**: none
- **pdf_role**: main_text_source
- **split_scope**: pages 499-538

---

CHAPTER
17
Performance Analysis
INTRODUCTION
Are you winning or losing? Why? Performance measurement will
answer the first question and can help to answer the second. A
sophisticated performance analysis system can provide valuable
feedback for an active manager. The manager can tie his or her
decisions to outcomes and identify success, failure, and possible
improvements.
Performance analysis has evolved from the days when the
performance goals were vague, if not primitive:
“Don’t steal any money!”
“Don’t lose any money!”
“Do a good job!”
“Do as well as I could at the bank!”
“Beat the market!”
“Justify your active management fee!”
The goal of performance analysis is to distinguish skilled from
unskilled investment managers. Simple cross-sectional compari-
sons of returns can distinguish winners from losers. Time series
analysis of the returns can start to separate skill from luck, by
measuring return and risk. Time series analysis of returns and port-
folio holdings can go the farthest toward analyzing where the
manager has skill: what bets have paid off and what bets haven't.
The manager’s skill ex post should lie along dimensions promised
ex ante.
477
478
Implementation
The drive for sophisticated performance analysis systems has
come from the owners of funds. Investment managers have, on
the whole, fought an unsuccessful rear-guard action against the
advance of performance analysis. This is understandable: The truly
poor managers are afraid, the unlucky managers will be unjustly
condemned, and the new managers have no track record. Only the
skilled (or lucky) managers are enthusiastic.
Of course, these owners of funds make several key assump-
tions in using performance analysis: that skillful active management
is possible; that skill is an inherent quality that persists over time;
that statistically abnormal returns are a measure of skill; and that
skillful managers identified in one period will show up as skillful
in the next period. The evidence here is mixed, as we will discuss
in this chapter and Chap. 20.
Performance analysis is useful not only for fund owners, but
also for investment managers, who can use performance analysis
to monitor and improve the investment process. The manager can
make sure that the active positions in the portfolio are compensated,
and that there have been no unnecessary risks in the portfolio.
Performance analysis can, ex post, help the manager avoid
two major pitfalls in implementing an active strategy. The first is
incidental risk: Managers may like growth stocks, for example, with-
out being aware that growth stocks are concentrated in certain
industry groups and concentrated in the group of stocks with higher
volatility. The second pitfall is incremental decision making. A portfo-
lio based on a sequence of individual asset decisions, each of them
wise on the surface, can soon become much more risky than the
portfolio manager intended. Risk analysis can diagnose these prob-
lems ex ante. Performance analysis can identify them ex post.
The lessons of this chapter are:
= The goal of performance analysis is to separate skill from
luck. Cross-sectional comparisons are not up to this job.
™ Returns-based performance analysis is the simplest
method for analyzing both return and risk, and
distinguishing skill from luck.
® Portfolio-based performance analysis is the most
sophisticated approach to distinguishing skill and luck
along many different dimensions.
Performance Analysis
479
® Performance analysis is most valuable to the sponsor
(client) when there is an ex ante agreement on the
manager’s goals and an indication of how the manager
intends to meet those goals.
™ Performance analysis is valuable to the manager in that it
lets the manager see which active management decisions
are compensated and which are not.
SKILL AND LUCK
The fundamental goal of performance analysis is to separate skill
from luck. But, how do you tell them apart? In a population of
1000 investment managers, about 5 percent, or 50, should have
exceptional performance by chance alone. None of the successful
managers will admit to being lucky; all of the unsuccessful manag-
ers will cite bad luck.
We present a facetious analysis of the market in Fig. 17.1. We
have divided the managers along the dimensions of skill and luck.
Those with both skill and luck are blessed. They deserve to thrive,
Luck
Insufferable
ik
Blessed
Doomed
Forlorn
Figure 17.1 Skill and luck.
480
Implementation
and they will. Those with neither skill nor luck are doomed. Natural
selection is cruel but just. But what about the two other categories?
Those managers with skill but no luck are forlorn. Their historical
performance will not reflect their true skill. And, finally, there is
the fourth category. These managers have luck without skill. We
call them the insufferable. Most managers can easily think of some-
one else they believe is in this category.
Fortunately or unfortunately, we observe only the combination
of skill and luck. Both the blessed and the insufferable will show
up with positive return histories. The challenge is to separate the
two groups.
The simple existence of positive returns does not prove skill.
Almost half of all roulette players achieve positive returns each spin
of the wheel, but over time they all lose. The existence of very large
positive returns also does not prove skill. How much risk was taken
on in generating that return? Performance analysis will involve com-
paring ex post returns to ex ante risk in a statistically rigorous way.
Chapter 12 included brief mentions of the standard error of
the information ratio. The approximate result is
1
SE{IR}
ar
(17.1)
where Y measures the number of years of observation.' The number
of years enters because we define the information ratio as an annu-
alized statistic. Equation (17.1) implies that to determine with 95
percent confidence (t statistic = 2) that a manager belongs in the
top quartile (IR = 0.5) will require 16 years of observations.’ It is
a fact of investment management life that proof of investment
prowess will remain elusive.
ke
ee
re
This assumes that all the error arises from the estimated mean residual return. If we
also account for the error arising from the estimated residual risk, we find
SEUR) = a 1+
where At is, e.g., 1/12 if we observe monthly returns. See Problem 3 for more details.
*See Problem 4 for a discussion of why changing the information ratio from an
annualized number to a monthly number does not improve our ability to
statistically verify investment performance.
IR? - At
2
Performance Analysis
481
We can view the basic predicament from another angle. What
if you are truly a top quartile manager, with an information ratio
of 0.5? What is the probability that your monthly, quarterly, annual
returns are positive? Figure 17.2 shows the result as the horizon
varies. Over one month, you have only a 56% chance of positive
realized alpha. Over a 5-year horizon, this rises to 87%. This implies
that over the standard 5-year horizon, 13% of skilled managers will
have negative realized alphas. Given the horizons for careers, and
for ideas in the investment business, luck will always play a role.
The efficient markets hypothesis suggests that active managers
have no skill. In its strong form, the hypothesis states that all
currently known information is already reflected in security prices.
Since all information is already in the prices, no additional informa-
tion is available to active managers to use in generating exceptional
returns. Active returns are completely random. The semistrong
version states that all publicly available information is already
reflected in security prices. Active management skill is really insider
trading! The weak form of the hypothesis claims only that all previ-
ous price-based information is contained in current prices. This
rules out technical analysis as skilled active management, but
would allow for skillful active management based on fundamental
and economic analysis.
There have also been many academic studies of active manag-
ers’ performance. These studies have focused on three related
questions:
= Does the average active manager outperform the
benchmark?
® Do the top managers have skill?
= Does positive performance persist from period to period?
Chapter 20 will review these questions in more detail. The initial
studies of mutual funds showed that the average manager under-
performed the benchmark, in proportion to fund expenses, and
that performance did not persist from period to period. Some recent
studies have shown that the average manager matches the bench-
mark net of fees, that top managers do have statistically significant
skill, and that positive performance may persist. Other studies have
found no evidence for persistence of performance. The conclusion
of all these conflicting studies is that even if performance does
OI
$182
X
Ul
UOZ1LIOP{
S
(C0 = Wy) soueusossed apysenb doy, ZZ] amsry
€
c
I
0
00°0
0c 0
0e'0
a0)
0s'0
S
oO
eudyy aaqisog Jo Ayiqeqoig
0L0
08°0
482
Performance Analysis
483
persist, it certainly doesn’t persist at any impressively high rate.
Do 52 percent or 57 percent of winners repeat, and is this statisti-
cally significant?
DEFINING RETURNS
We begin our in-depth discussion of performance analysis by defin-
ing returns—this may seem obvious, but there are several defini-
tions. Should we use compound returns or average returns, arith-
metic returns or logarithmic returns? Compound returns have the
benefit of providing an accurate measure of the value of the ending
portfolio.’ Arithmetic returns provide the benefit of using a linear
model of returns across periods. We can see these points with an
example. Let Rp(t) be the portfolio’s total return in period t, and
let Rp(t) and R;(t) be the total return on the benchmark and the risk-
free asset. The compound total return on portfolio P over periods 1
through T, Rp(1,T), is the product
IE
~Rp(1,T) = Ro(1) » Re(2) + Ro(3) +++ R(T) = T] Ret)
17.2)
t=1
The geometric average return for portfolio P, gp is the rate of return
per period that would give the same cumulative return:
He
(1 + gp)’ = [J Ro)
(17.3)
fi
Il
The average log return Zp is
T
ee T= |] Rpt)
(17.4)
t=1
1
T
or
Zp = (t) By In{Rp(t)}
CV Ae))
t=1
3This is true unless the portfolio has experienced cash inflows and outflows. Even in that
case, however, the industry standard approach to performance analysis is to
equally weight each period’s return, without accounting for differing portfolio
values in different periods.
484
Implementation
The geometric average return is compounded annually, while the
average log return is compounded continuously. Finally, the (arith-
metic) average return dp is
T
Ere (t) SRW)
(17.6)
t=1
It is always’ true that zp = gp = ap This does not necessarily say
that one measure is better to use than the others. It does indicate
that consistency is important, to make sure we are not comparing
apples and oranges.
These issues become even more important when we attribute
each period’s return to different sources, and then aggregate all
the sources over time. To cumulate returns, we need to account for
cross products. We discuss one approach to this in the technical
appendix.
CROSS-SECTIONAL COMPARISONS
The simplest type of performance analysis is a table that ranks
active managers by the total performance of their fund over some
period. Table 17.1 illustrates a typical table, showing median perfor-
mance, key percentiles, and the performance of a diversified and
widely followed index (the S&P 500), for a universe of institutional
equity portfolios covered by the Plan Sponsor Network (PSN) over
the period January 1988 through December 1992. These cross-
sectional comparisons can provide a useful feel for the range of
‘First, zp = In{1 + gp} < gp by the convexity of the logarithm function. We have a useful
approximation zp = In{1 + gp} ~ gp — 0.5 - gp. Again, by the convexity of the:
logarithm function,
T,
(*) -S) nfR} = Inf + 97)
ff
< in{() 2S) rao}
t=1
oe In{1 AF ap)
SO gp = ap. Finally, we have an approximation (exact for log normal) that 1 + ap ~
{1 + gp} - exp{0.5
- of}, where o} is the variance of In{R,(t)}. This reduces to ap ~
gp + 0.5 + op.
Performance Analysis
485
ee
ee ee
TABLE
17.1
SE
ee
ee ee
Percentile
Annualized Return, 1988-1992
5th
23.57%
25th
18.97%
Median
16.31%
75th
14.50%
95th
10.92%
S&P 500
15.80%
performance numbers over a period; however, they have four
drawbacks:
m They typically do not represent the complete population
of institutional investment managers. Table 17.1 includes
only those institutional equity portfolios that began no
later than 1983, still existed in 1993, and are covered in
the PSN database.
= These cross-sectional comparisons usually contain
survivorship bias, which is increasingly severe the longer
the horizon. Table 17.1 does not include firms that went
out of business between 1983 and 1993.
= These cross-sectional comparisons ignore the fact that
some of the reporting managers are managing $150
million portfolios, while others are managing $15 billion
portfolios. The rule is one man, one vote—not one dollar,
one vote.
= Cross-sectional comparisons do not adjust for risk. The
top performer may have taken large risks and been lucky.
We cannot untangle luck and skill in this comparison.
Figure 17.3 shows the impact of using a cross-sectional snap-
shot. Compare two managers, A and B. Over a 5-year period, Man-
ager A has achieved a cumulative return 16 percent above the bench-
mark, while Manager B has outperformed by. almost 20 percent.
Based on this rather limited set of information, most people would
prefer B to A, since B has clearly done better over the 5-year period.
OL
q
Joseuepy
—y—
V
Jaseuey,
—g—
yuo
‘uosteduiod uINyal BAQKRINUND EZ] any
%S-
%0
%S
Q
S
3
e
2
%O01
<
a
© =
a}
5
%S1
%OT
%ST
486
Performance Analysis
487
Figure 17.3, however, shows the time paths that A and B
followed over the 5-year period. After seeing Fig. 17.3, most observ-
ers prefer A to B, since A obviously incurred much less risk than
B in getting to the current position.’ If you had stopped the clock
at most earlier times in the 5-year period, A would have been ahead.
Performance analysis must account for both return and risk.
RETURNS-BASED PERFORMANCE
ANALYSIS: BASIC
The development of the CAPM and the notion of market efficiency
in the 1960s encouraged academics to consider the problems of
performance analysis. The CAPM maintained that consistent excep-
tional returns by one manager were unlikely. The academics devised
tests to see if their theories were true, and the by-products of these
tests are performance analysis techniques. These techniques analyze
time series of returns. One approach, first proposed by Jensen
(1968), separates returns into systematic and residual components,
and then analyzes the statistical significance of the residual compo-
nent. According to the CAPM, the residual return should be zero,
and positive deviations from zero signify positive performance.
The CAPM also states that the market portfolio has the highest
Sharpe ratio (ratio of excess return to risk), and Sharpe (1970)
proposed performance analysis based on comparing Sharpe ratios.
We will discuss the Jensen approach first, and then the Sharpe ap-
proach.
Returns Regression
Basic returns-based performance analysis according to Jensen in-
volves regressing the time series of portfolio excess returns against
benchmark excess returns, as discussed in Chap. 12.
SManager A has realized an information ratio of 1.0 over this period, while Manager B
has realized an information ratio of 0.7.
488
Implementation
wn
r=
few
8
vo
io
g +3
0%
-10%
4.
a
=
=
Alpha = 0.03%, t-alpha = 0.18
L
-10%
Beta = 0.92, t-beta = 23.01
-15%
S&P 500 Excess Returns
Figure 17.4 Returns regression.
Figure 17.4 shows the scatter diagram of excess returns to the
Major Market Index portfolio and the S&P 500, together with a
regression line, over the period from January 1988 through Decem-
ber 1992. The estimated coefficients in the regression are the portfo-
lio’s realized alpha and beta:
rp(t) =
(0.45 ote Bp C rp(t) = €p(t)
(77)
Alpha appears in the diagram as the intercept of the regression
line with the vertical axis. Beta is the slope of the regression line.
For the above example, ap = 0.03 percent per month and Bp =
0.92. The regression divides the portfolio’s excess return into the
benchmark component, Bp - rz(t), and the residual component,
Op(t) = ap + ep(t). Note that in this example, the residual return is
quite different from the active return, because the active beta is
—0.08. While the alpha is 3 basis points per month, the average
active return is —4 basis points per month.
The CAPM suggests that alpha should be zero. The regression
analysis provides us with confidence intervals for our estimates of
alpha and beta. The ¢ statistic for the alpha provides a rough test
Performance Analysis
489
of the alpha’s statistical significance. A rule of thumb is that a t
statistic of 2 or more indicates that the performance of the portfolio
is due to skill rather than luck. The probability of observing such
a large alpha by chance is only 5 percent, assuming normal distri-
butions.
The ¢ statistic for the alpha is approximately
tp ~ (2*) -/T
(17.8)
where ap and w» are not annualized and T is the number of observa-
tions (periods). The ¢ statistic measures whether ap differs signifi-
cantly from zero, and a significant t statistic requires a large ap
relative to its standard deviation, as well as many observations.
For the example above, the t statistic for the estimated ap is only
0.36, not statistically distinct from zero.
Chapter 12 has already discussed f statistics and their relation
to information ratios and information coefficients. The t statistic
measures the statistical significance of the return. The information
ratio measures the ratio of annual return to risk, and is related to
investment value added. Though closely related mathematically,
they are fundamentally different quantities. The ¢ statistic measures
statistical significance and skill. The information ratio measures
realized value added, whether it is statistically significant or not.
While Jensen focused on alphas and t statistics, information ratios,
given their relationship to value added, are also important for
performance analysis.
The basic alternative to the Jensen approach is to compare
Sharpe ratios for the portfolio and the benchmark. A portfolio with
fan is
(17.9)
where 7 denotes mean excess return over the period, has demon-
strated positive performance. Once again, we can analyze the statis-
tical significance of this relationship. Assuming that the standard
errors in our estimates of the mean returns 7p and 7, dominate the
errors in our estimates of op and oz, the standard error of each
Sharpe ratio is approximately 1/./N, where N is the number of
490
Implementation
observations. Hence a statistically significant (95 percent confidence
level) demonstration of skill occurs when®
eee
4/2
71
Dybvig and Ross (1985) have shown’ that superior perfor-
mance according to Sharpe implies positive Jensen alphas, but that
positive Jensen alphas do not imply positive performance according
to Sharpe.
RETURNS-BASED PERFORMANCE
ANALYSIS: ADVANCED
There are several refinements of the returns-only regression-based
performance analysis. Some are statistical in nature. They refine the
statistical tests. Examples of statistical refinements include Bayesian
corrections and adjustments for heteroskedasticity and autocorrela-
tions. Other refinements stem from financial theory. They attempt
to extract additional information from the time series of returns.
Examples of financial refinements include analyzing benchmark
timing, using a priori betas, analyzing value added, controlling for
public information, style analysis, and controlling for size and
value. The last three refinements are controversial, in that they all
argue that managers should receive credit only for returns beyond
those available through various levels of public information. These
proposals raise the bar on an already difficult enterprise.
Bayesian Correction
The first statistical refinement is a Bayesian correction. The Bayesian
correction allows us to use our prior knowledge about the distribu-
tion of alphas and betas across managers. For example, imagine
that we know that the prior distribution of monthly alphas has
‘If the standard error of each term is 1/\/N, and the errors are uncorrelated, then the
standard error of the difference is approximately \/2/N.
é
’They provide analytic results and do not deal with issues of statistical significance.
Performance Analysis
491
mean 0 and standard deviation of 12.5 basis points per month. We
then expect an alpha of 0, and would be “surprised” (a two-
standard-deviation event) if the alpha were more than +3.00 per-
cent per year (25 basis points per month). We can apply similar
logic to the observed betas. The Bayesian analysis allows one to
take this prior information into consideration in making judgments
about the “true” values of ap and Bp For more information about
this topic, see Vasicek (1973).
Heteroskedasticity
One of the assumptions underlying the regression model is that
the error terms €p(t) have the same standard deviation for each t.
We can employ various schemes to guard against failure of that
assumption. We call this heteroskedasticity in the regression game.
Autocorrelation
A third statistical problem is autocorrelation. We assume that the
error terms e€p(t) are uncorrelated. If there is significant autocorrela-
tion, then we can make an adjustment. This arises, for example, if
we examine returns on overlapping periods.
Benchmark Timing
One financially based refinement to the regression model is a bench-
mark timing component. The expanded model is
rp(t) = ap + Bp- rp(t) + yp ° Max{0,rg(t)} + €p(t)
71D)
We include the variable yp to determine whether the manager
has any benchmark timing skill. The model includes a “down-
market” beta, Bp and an “up-market” beta, Bp + yp. If yp is signifi-
cantly positive, then we say that there is evidence of timing skill;
benchmark exposure is significantly different in up and down cases.
Figure 17.5 indicates how Bp ap and 7p relate to performance.
In our example of the Major Market Index portfolio versus
the S&P 500 portfolio, not surprisingly, there is no evidence of
benchmark timing ability. Over the period from January 1988
®S1
uINnjJay YlewWYyUueg
%OI-
%S-
%O1
WS
TZ = eydye
ee
%S
2
Col
a
01
ta
SI] = B)9q JoyJeW-dn
HST
%
Ge
‘Sumy yreuryoueg ¢°ZT am8Lj
C80 = Blaq JaysJeW-UMOPp
%01-
%S1-
UINJ2Y O[0j710g
492
Performance Analysis
493
through December 1992, Bp = 0.95 and yp = —0.05. The coefficient yp
is not statistically distinct from zero, with a t statistic of only —0.41.
There is a longer discussion of the performance measurement
aspects of benchmark timing in Chap. 19. See also the paper by
Henriksson and Merton (1981).
A Priori Beta Estimates
Another embellishment of returns-based analysis is improved esti-
mation of the beta. This can take the form of using a beta that is
estimated before the fact. As we will discuss in Chap. 19, this can
help in avoiding spurious correlations between the portfolio returns
and benchmark returns. In the example of the Major Market Index
portfolio versus the S&P 500 from 1988 through 1992, this can make
_
a difference. While the realized beta was 0.92, the monthly forecast
beta over the period ranged from 0.98 to 1.03. Changing from
realized to forecast beta changes the portfolio’s alpha from 3 basis
points per month to —4 basis points per month.
Value Added
A different approach to analyzing the pattern of returns is to use
the concept of value added and ideas from the theory of valuation
(Chap. 8). The idea is to look at the pattern of portfolio excess
returns and market excess returns. Suppose we have T = 60 months
of returns, {rp(t), ra(t), r-(f)} for t = 1, 2,..., T. We can think of a
deal that says, “In the future the returns will equal {rp(t), rp(t),
re(t)} with probability 1/T.“ How much would you pay for the
opportunity to get the portfolio return under those conditions? You
would pay one unit to get the risk-free or market returns; i.e., they
are priced fairly. If the portfolio performs very well, you might be
willing to pay 1.027 to get the portfolio returns. In that case, we
say that the value added is 2.7 percent. If you were willing to pay
only 0.974, then there would be a loss in value of 2.6 percent. The
appendix shows how this analysis might be carried out.
Controlling for Public Information
Ferson and Schadt (1996) and Ferson and Warther (1996) have
argued that the standard regression [Eq. (17.7)] doesn’t properly
494
Implementation
condition for different market environments. They claim two things:
first, that public information on dividend yields and interest rates
can usefully predict market conditions, and second, that managers
earn their living through nonpublic information. As a result, they
adjust the basic CAPM regression to condition for public informa-
tion. For example, they suggest the regression
rp(t) = ap + B- rp(t) + B, - [ra(t) - yt — 1)]
(17.12)
st Bis [rp(t) - ip(t — 1)] + ep(t)
Equation (17.12) basically allows for beta varying with economic
conditions, as modeled linearly through the market dividend yield
y(t) and the risk-free rate i-(t). Many managers would argue, with
some justification, that Eq. (17.12) penalizes them by including ex
post insight into the relationship between yields, interest rates, and
market conditions.
Style Analysis
So far, all the advances discussed in returns-based performance
analysis still rely on a prespecified benchmark, typically a standard
index like the S&P 500. Sharpe (1992) proposed style analysis to
customize a benchmark for each manager’s returns, in order to
measure the manager’s contribution more exactly.
Style analysis attempts to extract as much information as possi-
ble from the time series of portfolio returns without requiring the
portfolio holdings. Like the factor model approach, style analysis
assumes that portfolio returns have the form
J
rp(t) = S) hp - 7)(t) + up(t)
(17.13)
j=l
:
where the {7,(¢)} are returns to J styles, the hp; measure the portfolio’s
holdings of those styles, and up(f) is the selection return, the portion
of the return which style cannot explain. Here the styles typically
allocate portfolio returns along the dimensions of value versus
growth, large versus small capitalization, domestic versus interna-
tional, and equities versus bonds. In addition to the returns to the
portfolio of interest, the estimation approach also requires returns
to portfolios that capture those styles.
Performance Analysis
495
We estimate holdings hp; via a quadratic program:
Min{Var{up(t)}}
(17.14)
J
subject to
De hp, = 1
(17.15)
j=1
This differs from regression in two key ways. First, the holdings
must be nonnegative and sum to 1. Second, the procedure mini-
ie
mizes the variance of the selection returns, not yy) up(t). The objective
t=1
does not penalize large mean selection returns—as_ regression
would do—but only variance about that mean.
Style analysis requires only the time series of portfolio returns
and the returns to a set of style indices. The result is a top-down
attribution of the portfolio returns to style and selection. According
to style analysis, the style holdings define the type of manager,
and the selection returns distinguish among managers. Managers
can demonstrate skill by producing large selection returns. We can
calculate manager information ratios using the mean and standard
deviation of the managers’ selection returns.
In general, we can use style analysis to (1) identify manager
style, (2) analyze performance, and (3) analyze risk. The first appli-
cation, identifying manager style, is controversial. Several research-
ers [e.g., Lobosco and DiBartolomeo (1997) and Christopherson
and Sabin (1998)] have pointed out the large standard errors associ-
ated with the estimated weights, driven in part by the significant
correlation between the style indices. But this application, by itself,
is of limited use. Identifying manager style usually requires no
fancy machinery. Managers publicize their styles, and a peek at
their portfolios can usually verify the claim.
Style-based performance analysis may also be inaccurate, al-
though it is usually an improvement over the basic returns-based
methodologies. It is an excellent tool for large studies of manager
performance. Inaccuracies tend to cancel out from one manager to
another in the large sample, and accurate and timely information
on portfolio holdings is unavailable.
496
Implementation
Risk analysis could use style analysis to identify portfolio
exposures to style indices. Risk prediction would follow from these
exposures, a style index covariance matrix, and an estimate of
selection risk (based on historical selection returns). We could as-
sume selection returns uncorrelated across managers. Once again,
this would improve on risk prediction based only on beta, but
would fall far short of the structural models we discussed in Chap. 3.
Controlling for Size and Value
Fama and French (1993) have proposed a performance analysis
methodology very similar in spirit to Sharpe’s style analysis. Their
approach to performance uses the regression
This looks like a standard CAPM regression with two additional
terms. The return SMB(t) (“small minus big”) is the return to a
portfolio long small-capitalization stocks and short large-capitaliza-
tion stocks. The return HML(t) (“high minus low”) is the return to
a portfolio long high-book-to-price stocks and short low-book-to-
price stocks. So Sharpe uses a quadratic programming approach
and indices split along size and value (book-to-price) dimensions.
Fama and French control along the same dimensions and use stan-
dard regression.
How do they build their two portfolio return series? First,
each June, they identify the median capitalization for New York
Stock Exchange (NYSE) stocks. They use that median to classify
all stocks (including AMEX and NASDAQ stocks) as S (for small)
or B (for big).
Second, using end-of-year data, they sort all stocks by book-
to-price ratios. They classify the bottom 30 percent as L (for tow),
the middle 40 percent as M (for medium), and the top 30 percent
as H (for high). These two splits lead to six portfolios:
S/L, S/M,
S/H; B/L, B/M, andsB/H:
They then calculate capitalization-weighted returns to each of
the six portfolios.
Finally, they define SMB(t) as the difference between the simple
average of S/L,S/M, and S/H and the simple average of B/L, B/M,
and B/H. Effectively, SMB(t) is the return on a net zero investment
Performance Analysis
497
portfolio that is long small-capitalization stocks and short large-
capitalization stocks, with long and short sides having roughly
equal book-to-price ratios.
Similarly, they define HML(t) as the difference between the
average of S/H and B/H
and the average of S/L and B/L. Once
again, this is the return on a net zero investment portfolio that is
long high-book-to-price stocks and short low-book-to-price stocks,
with long and short sides having roughly equal market capital-
izations.
Carhart (1997) has extended this approach by also controlling
for past 1-year momentum.
PORTFOLIO-BASED
PERFORMANCE ANALYSIS
Returns-based analysis is a top-down approach to attributing re-
turns to components, ex post, and statistically analyzing the manag-
er’s added value. At its simplest, the attribution is between system-
atic and residual returns, with managers given credit only for
achieved residual returns. Style analysis is similar in approach,
attributing returns to several style classes and giving managers
credit only for the remaining selection returns. Returns-based per-
formance analysis schemes typically allocate part of the returns to
systematic or style components and give managers credit only for
the remainder.
Portfolio-based performance analysis is a bottom-up ap-
proach, attributing returns to many components based on the ex
ante portfolio holdings and then giving managers credit for returns
along many of these components. This allows the analysis not only
of whether the manager has added value, but of whether he or she
has added value along dimensions agreed upon ex ante. Is he a
skillful value manager? Does her value added arise from stock
selection, beyond any bets on factors? Portfolio-based performance
analysis can reveal this. In contrast to returns-based performance
analysis, performance-based analysis schemes can attribute returns
to several components of possible manager skill.
The returns-only analysis works without the full information
available for performance analysis. We can say much more if we
look at the actual portfolios held by the managers. In fact, two
498
Implementation
nee
EEE Ean EEEEEEUEEE SSUES SSESEE ESSERE
additional items of information can help in the analysis of per-
formance:
® The portfolio holdings over time
= The goals and strategy of the manager
The analysis proceeds in two steps: performance attribution
and performance analysis. Performance attribution focuses on a
single period, attributing the return to several components. Perfor-
mance analysis then focuses on the time series of returns attributed
to each component. Based on statistical analysis, where (if any-
where) does the manager exhibit skill and add value?
Performance Attribution
Performance attribution looks at portfolio returns over a single
period and attributes them to factors. The underlying principle is
the multiple-factor model, first discussed in Chap. 3:
rp(t) = >) xp(t) - b(t) + ur(t)
(17.18)
i
Examining returns ex post, we know the portfolio’s exposures xp;(t)
at the beginning of the period, as well as the portfolio’s realized
return rp(t) and the estimated factor returns over the period. The
return attributed to factor / is
rpj(t) = Xpj(t) - b(t)
CUZ)
The portfolio’s specific return is up(t).
We are free to choose factors as described in Chap. 3, and in
fact we typically run performance attribution using the same risk-
model factors. However, we are not in principle limited to the same
factors as are in our risk model. In general, just as in the returns-
based analysis, we want to choose some factors for risk control
and others as sources of return. The risk control factors are typically
industry or market factors, although later we can analyze skill in
picking industries.
The return factors can include typical investment themes such
as value or momentum. In building risk models, we always use
ex ante factors: that is, those based on informatio known at the
beginning of the period. For return attribution, we could also con-
Performance Analysis
499
sider ex post factors: that is, those based on information known
only at the end of the period. For example, we could use a factor
based on IBES earnings forecasts available at the end of the period.
We could interpret returns attributed to this factor as evidence of
the manager’s skill in forecasting IBES earnings projections.
Beyond the manager’s returns attributed to factors will remain
the specific return to the portfolio.
A manager’s ability to pick
individual stocks, after controlling for the factors, will appear in
this term. We call this term specific asset selection.
We typically think of the specific return as the component
of return which cross-sectional factors cannot explain. That view
suggests that we simply lump the portfolio’s specific return all
together. But for an individual strategy, some attributions of specific
return may also make sense. If our strategy depends on analyst
information, we may want to group specific returns by analyst. We
think our auto industry analyst adds value. If this is true, we should
see a positive contribution from auto-stock specific asset selection.
Similarly, the specific returns can tell us if our strategy works better
in some sectors than in others. This term doesn’t tell us whether
we have successfully picked one sector over another, it tells us
whether we can pick stocks more accurately in one sector than
in another.
Note that we have many choices as to how to attribute returns.
We can choose the factors for attribution. We can attribute specific
returns. We can even attribute part of our returns to the constraints
in our portfolio construction process (e.g., we lost 32 basis points
of performance last year as a result of our optimizer constraints).*
Performance attribution is not a uniquely defined process. Com-
mercially available performance analysis products choose widely
applicable attribution schemes. Customized systems have no
such limitations.
5For example, with linear equality constraints, h’ - A = 0, and Lagrange multipliers —7,
the first-order conditions are
a=2-hy:V-hynt+a:-A=0
This effectively partitions the alpha between the portfolio and the constraints. For
more details, see Grinold and Easton (1998).
500
Implementation
We can apply performance attribution to total returns, active
returns, and even active residual returns. For active returns, the
analysis is exactly the same, but we work with active portfolio
holdings and returns:
reat) = >> xpaj(t) « bj(t) + ural)
(17.20)
J
To break down active returns into systematic and residual, remem-
ber that we can define residual exposures as
Xparj = Xpaj — Bra * XB;
(17:21)
where we simply subtract the active beta times the benchmark’s
exposure from the active exposure, and residual holdings simi-
larly as
Hearn = MpAn — Boa ° hen
(722)
Substituting these into Eq. (17.20), and remembering that up, =
Npan * Un, We find
reat) = Bra’ Ta(t) + DS) xpandt) - B(f) + ume(t)
(17.23)
]
Equation (17.23) will allow a very detailed analysis of the sources
of active returns relative to the benchmark.
As an example of performance attribution, consider the analy-
sis of the Major Market Index portfolio versus an S&P 500 bénch-
mark over the period January 1988 through December 1992. For
now, focus on the returns over January 1988. Using the BARRA
U.S. Equity model (version 2), the factor exposures are shown in
Table 17.2.
Table 17.2 illustrates the attributed active return. Table 17.3
summarizes the attribution between systematic and residual this
month. The active beta of the Major Market Index versus the
S&P 500 is only 0.02, and so the active residual component is very
Performance Analysis
501
TABLE
17.2
a
reenenmmmn
—
Factor
Active Exposure
Attributed Return
Variability in markets
SOE Ie)
—0.02%
Success
0.14
—0.47%
Size
0.69
0.10%
Trading activity
0.04
0.02%
Growth
—0.14
—0.10%
Earnings-to-price ratio
—0.07
—0.04%
Book-to-price ratio
SO),
—0.06%
Earnings variability
—0.23
0.10%
Financial leverage
—0.04
—0.03%
Foreign income
0.62
—0.02%
Labor intensity
0.06
0.02%
Yield
0.00
0.00%
Low capitalization
0.00
0.00%
Aluminum
—0.57%
0.02%
lron and steel
0.13%
0.01%
Precious metals
—0.31%
0.04%
Miscellaneous mining and metals
—0.61%
—0.03%
Coal and uranium
0.32%
—0.03%
International oil
2.53%
0.24%
Domestic petroleum reserves
0.92%
0.08%
Foreign petroleum reserves
0.00%
0.00%
Oil refining and distribution
—0.54%
—0.04%
Oil services
—0.91%
—0.09%
Forest products
0.42%
—0.01%
Paper
2.64%
—0.18%
Agriculture and food
—1.76%
—0.08%
Beverages
1.66%
—0.05%
Liquor
~0.52%
~0.01%
Tobacco
2.86%
0.19%
Construction
—0.01%
0.00%
Chemicals
5.59%
0.11%
Tire and rubber
—0.22%
0.00%
Containers
—0.22%
0.01%
Producer goods
—2.32%
—0.08%
Pollution control
—0.78%
—0.02%
502
Implementation
TABLE
17.2
(Continued)
Active Exposure
Attributed Return
Electronics
D276
0.04%
Aerospace
—1.96%
—0.08%
Business machines
1.59%
—0.01%
Soaps and housewares
4.19%
0.25%
Cosmetics
—0.55%
—0.038%
Apparel, textiles
—0.32%
—0.01%
Photographic, optical
2.76%
—0.12%
Consumer durables
—0.44%
—0.02%
Motor vehicles
1.70%
0.06%
Leisure, luxury
—0.37%
—0.01%
Health care
3.14%
0.11%
Drugs and medicine
10.45%
1.01%
Publishing
—2.21%
—0.01%
Media
—1.29%
—0.08%
Hotels and restaurants
—1.86%
—0.09%
Trucking, freight
—0.21%
—0.01%
Railroads, transit
—1.30%
—0.07%
Air transport
—0.69%
—0.01%
Transport by water
—0.06%
0.00%
Retail food
—0.72%
—0.03%
Other retail
—2.95%
—0.26%
Telephone, telegraph
—5.24%
—
—0.43%
Electric utilities
—4.39%
—0.34%
Gas utilities
—1.04%
—0.05%
Banks
—1.96%
—0.14%
Thrift institutions
—0.09%
—0.01%
Miscellaneous finance
1.19%
0.06%
Life insurance
—0.82%
—0.06%
Other insurance
= Weil
—0.06%
Real property
—0.22%
0.00%
Mortgage financing
0.00%
0.00%
Services
—2.09%
—0.04%
Miscellaneous
0.14%
0.01%
Total attributed active return
—0.84%
Performance Analysis
503
eee
eee
TABLE
17.3
a
en
Component
Attributed Return
Active systematic
0.06%
Active residual
—4.88%
Common factor
—0.75%
Specific
—4.13%
Active total
close to the active component. Comparing Tables 17.2 and 17.3, the
active common-factor component is —0.84 percent and the active
residual common-factor component is —0.75 percent.
Performance Analysis
Performance analysis begins with the attributed returns each pe-
riod, and looks at the statistical significance and value added of
the attributed return series. As before, this analysis will rely on t
statistics and information ratios to determine statistical significance
and value added.
For concreteness, consider the attribution defined in Eq.
(17.23), with active returns separated into systematic and residual,
and active residual returns further attributed to common factors
and specific returns.
Start with the time series of active systematic returns. Most
straightforward is a simple analysis of the mean return and its t
statistic. However, according to the CAPM, we expect a positive
return here if the active beta is positive on average. Hence, we will
go one additional step and separate this time series into three
components: one arising from the average active beta and the ex-
pected benchmark return, one arising from the average active beta
and the deviation of realized benchmark return from its expectation,
and the third from benchmark timing—deviations of the active
beta from its mean. The first component, based on the average
active beta and the expected benchmark return, is not a component
of active management.
504
Implementation
The total active systematic return over time is
Active systematic = >) Bra(t) + re(@)
(17.24)
= ) [Bos + S86] - [us + Gs — we) + r9(6)]
DL eS OT
12)
+ > dBralt) - Srs(t)
Expected active beta return = » Boa * ep
(17.25)
f
Active beta surprise = ») Bra - (7, — pp)
(17.26)
t
Active benchmark timing return = >> SBe,(t) - Srg(t)
(17.27)
t
In Egs. (17.24) through (17.27), Boa is the average active beta, 7s is
the average benchmark excess return over the period, and jg is
the long-run expected benchmark excess return.
The analysis of the time series of attributed factor returns and
specific returns is more straightforward.’ We can examine each
series for its mean, t statistic, and information ratio. For these, we
need not only the mean returns, but also the risk for each factor.
We can base risk on the realized standard deviation of the time series
or on the ex ante forecast risk. The technical appendix describes
an innovative approach which combines the two risk estimates,
weighting realized risk more heavily the more observations there
are in the analysis period.
Performance analysis, just like performance attribution, is not
uniquely defined. The scheme outlined here is simply a reasonable
approach to distinguishing the various sources of typical strategy
returns. It will sometimes prove useful to customize a performance
*Of course, we can apply the same time series analysis to the factor returns that we
applied to the systematic returns. In particular, we can separate each attributed
factor return into two components, one based on the average active exposure and
the other based on the timing of that exposure about its average.
Performance Analysis
505
TABLE
17.4
men
Annualized Active Contributions
Elements of Active Management
Return
Risk
IR
t statistic
Systematic active returns
Active beta surprise
0.02%
0.16%
0.23
0.51
Active benchmark timing
0.03%
0.19%
0.13
0.28
Total
0.06%
0.25%
0.24
0.54
Residual active returns
Industry factors
0.27%
1.88%
0.12
0.26
Risk index factors
—0.97%
2.25%
—0.:36
—0.81
Specific
0.12%
3.23%
0.01
0.02
Total
—0.58%
4.21%
—0.14
—0.30
Total active returns
—0.52%
4.22%
=0:12
=(0)/27/
analysis scheme to a particular strategy, in order to isolate more
precisely its sources of value added.
Table 17.4 summarizes this analysis for the example of the
Major Market Index portfolio versus the S&P 500 benchmark.”
Not surprisingly, given this example, Table 17.4 exhibits no strong
demonstrations of skill or value added.
Now that we have analyzed each source of risk in turn, we
can identify the best and worst policies followed by the manager:
those time series which have achieved the highest and lowest re-
turns on average. Here is where the manager’s predefined goals
and strategies should shine through. Stock pickers should see spe-
cific asset selection as one of their best strategies. Value managers
should see value factors as their best strategies. Ex ante strategies
that are inconsistent with best policy analysis can signal to the
owner of the funds that the active manager has deviated in strategy
and can signal to the manager that the strategy isn’t doing what
he or she expects it to do.
Table 17.5 displays the best and worst policies for the example
Major Market Index portfolio versus the S&P 500 benchmark. Previ-
“The technical appendix includes a discussion of how we calculate annualized active
contributions—in particular, how we deal with the issue of cumulating attributed
returns.
506
Implementation
TABLE
17.5
Policy
Annualized Active Return
Five best policies
Foreign income
0.44%
International oil
0.36%
Drugs, medicine
0.33%
Tobacco
0.22%
Health care (nondrug)
0.18%
Five worst policies
Size
—1.24%
Photographic, optical
—0.48%
Business machines
—0.40%
Paper
—0.37%
Telephone, telegraph
—0.32%
ous analysis showed that the example included no demonstration
of skill or value added, and comparing Table 17.5 to Table 17.2, we
can see that the best and worst policies simply correspond to the
largest-magnitude active exposures.
SUMMARY
The goal of performance analysis is to separate skill from luck. The
more information available, the better the analysis. Using a simple
cross section of returns to differentiate managers is insufficient. A
time series of returns to managers and benchmarks can separate
skill from luck. The most accurate performance analysis utilizes
information on portfolio holdings and returns over time, to not
only separate skill from luck, but also identify where the manager
has skill.
»
NOTES
The science of performance analysis began in the 1960s with the
seminal academic work of Sharpe (1966, 1970), Jensen (1968), and
Treynor (1965). They used the CAPM as a starting point for devel-
oping the returns-based methodology described in this chapter.
Their goal was to test market efficiency and analyze manager per-
formance, a topic we will cover in Chap. 20.
Performance Analysis
507
Since then, many other academics have developed perfor-
mance analysis methodologies, often motivated by the desire to
further test market efficiency and manager performance. Some ad-
vances have come from application of clever statistical insights
to the CAPM framework. Other refinements have followed new
developments in finance theory. For example, Fama and French
(1993) have proposed a new scheme which explicitly controls for
size and book-to-market effects.
Most often, the academic treatments have focused on returns-
based analysis, although Daniel, Grinblatt, Titman, and Wermers
(1997) control for size, book-to-price, and momentum at the asset
level (using quintile portfolios) and then aggregate specific returns
up to the portfolio level.
Most of these new academic developments are contained
within the practitioner-developed portfolio-based analysis method-
ology described in this chapter.
REFERENCES
Beckers, Stan. “Manager Skill and Investment Performance: How Strong Is the
Link?” Journal of Portfolio Management, vol. 23, no. 4, 1997, pp. 9-23.
Carhart, Mark M. “On Persistence in Mutual Fund Performance.” Journal of Finance,
vol. 52; no; 11997, pp. 57-82.
Christopherson, Jon A., and Frank C. Sabin. “How Effective Is the Effective Mix?”
Journal of Investment Consulting, vol. 1, no. 1, 1998, pp. 39-50.
Daniel, Kent, Mark Grinblatt, Sheridan Titman, and Russ Wermers. “Measuring
Mutual Fund Performance with Characteristic-based Benchmarks.” Journal
of Finance, vol. 52, no. 3, 1997, pp. 1035-1058.
;
DeBartolomeo, Dan, and Erik Witkowski. “Mutual Fund Misclassification: Evi-
dence Based on Style Analysis.” Financial Analysts Journal, vol. 53, no. 5,
1997,.pp. 32-43:
Dybvig, Philip H., and Stephen A. Ross. “The Analytics of Performance Measure-
ment Using a Security Market Line.” Journal of Finance, vol 40, no. 2, 1985,
pp. 401-416.
Fama, Eugene F,, and Kenneth R. French. “Common Risk Factors in the Returns
on Stocks and Bonds.” Journal of Financial Economics, vol. 33, no. 1, 1993,
pp: 3-56.
Ferson, Wayne E., and Rudi W. Schadt. “Measuring Fund Strategy and Perfor-
mance in Changing Economic Conditions.” Journal of Finance, vol. 51, no.
2, 1996, pp. 425-461.
Ferson, Wayne E., and Vincent A. Warther. “Evaluating Fund Performance in a
Dynamic Market.” Financial Analysts Journal, vol. 52, no. 6, 1996, pp. 20-28.
508
Implementation
Grinold, Richard C., and Kelly K. Easton. “Attribution of Performance and Hold-
ings.” In Worldwide Asset and Liability Modeling, edited by William T. Ziemba
and John M. Mulvey (Cambridge, England: Cambridge University Press,
1998), pp. 87-113.
Henriksson, Roy D., and Robert C. Merton. “On Market Timing and Investment
Performance II. Statistical Procedures for Evaluating Forecasting Skills.”
Journal of Business, vol 54, no. 4, 1981, pp. 513-533.
Ippolito, Richard A. “On Studies of Mutual Fund Performance 1962-1991,” Finan-
cial Analysts Journal, vol. 49, no. 1, 1993, pp. 42-50.
Jensen, Michael C. “The Performance of Mutual Funds in the Period 1945-1964.”
Journal of Finance, vol. 23, no. 2, 1968, pp. 389-416.
Jones, Frank J., and Ronald N. Kahn. “Stock Portfolio Attribution Analysis.” In
The Handbook of Portfolio Management, edited by Frank J. Fabozzi (New Hope,
PA: Frank J. Fabozzi Associates, 1998), pp. 695-707.
Lehmann, B., and D. Modest. “Mutual Fund Performance Evaluation:
A Compari-
son of Benchmarks and Benchmark Comparisons.” Journal of Finance, vol.
42, no. 2, 1987, pp. 233-265.
Lobosco, Angelo, and Dan DiBartolomeo. “Approximating the Confidence Inter-
vals for Sharpe Style Weights.” Financial Analysts Journal, vol. 53, no. 4, 1997,
pp. 80-85.
Modigliani, Franco, and Leah Modigliani. “Risk-Adjusted Performance.” Journal
of Portfolio Management, vol. 23, no. 2, 1997, pp. 45-54.
Rudd, Andrew, and Henry K. Clasing, Jr. Modern Portfolio Theory, 2nd ed. (Orinda,
Calif.: Andrew Rudd, 1988).
Sharpe, William F. “Mutual Fund Performance.” Journal of Business, vol 39, no. 1,
1966, pp. 119-138.
. Portfolio Theory and Capital Markets (New York: McGraw-Hill, 1970).
——. “Asset Allocation: Management Style and Performance Measurement.”
Journal of Portfolio Management, vol . 18, no. 2, 1992, pp. 7-19.
Treynor, Jack L. “How to Rate Management of Investment Funds.” Harvard Business
Review, vol. 43, no. 1, January-February 1965, pp. 63-75.
Treynor, Jack L., and Fischer Black. “Portfolio Selection Using Spectal Information
under the Assumptions of the Diagonal Model with Mean Variance Portfolio
Objectives and Without Constraints.” In Mathematical Models in Investment
and Finance edited by G. P. Szego and K. Shell (Amsterdam: North-Hol-
land 1972).
Vasicek, Oldrich A. “A Note on Using Cross-Sectional Information in Bayesian
Estimation of Security Betas.” Journal of Finance, vol. 28, no. 5, 1973, pp:
1233-1239;
PROBLEMS
1. Joe has been managing a portfolio over the past year.
Performance analysis shows that he has realized an
Performance Analysis
509
information ratio of 1 and a ¢ statistic of 1 over this
period. He argues that information ratios are what
matter for value added, and so who cares about t
statistics? Is he correct? What can you say about Joe’s
performance?
2. Jane has managed a portfolio for the past 25 years,
realizing a t¢ statistic of 2 and an information ratio of 0.4.
She argues that her ¢ statistic proves her skill. Compare
her skill and added value to Joe’s.
3. Prove the more exact result for the standard error of the
information ratio,
SE{IR} = - Ne (= at)
Assume that errors in the mean and standard deviation of
the residual returns are uncorrelated, and use the normal
distribution result:
0)
NZI)
for a sample standard deviation from N observations.
4. Show that changing the information ratio from an
annualized to a monthly statistic does not improve our
ability to measure investment performance. It will still
require a 16-year track record to demonstrate top-
quartile performance with 95 percent confidence. First
calculate the standard error of a monthly IR. Second,
convert a top-quartile IR of 0.5 to its monthly equivalent.
Finally, calculate the required time period to achieve a t
statistic of 2.
5. Using Table 17.2, identify the largest active risk index
and industry exposures and the largest risk index and
industry attributed returns for the Major Market Index
versus the S&P 500 from January 1988 to December 1992.
Must the largest attributed returns always correspond to
the largest active exposures?
SE[w] =
510
Implementation
6. Given portfolio returns of {5 percent, 10 percent, —10
percent} and benchmark returns of {1 percent, 5 percent,
10 percent}, what is the cumulative active return over
this period? What are the cumulative returns to the
portfolio and benchmark?
7. Why should portfolio-based performance analysis be
more accurate than returns-based performance
analysis?
8. How much statistical confidence would you have in an
information ratio of 1 measured over 1 year? How many
years of performance data would you need in order to
measure an information ratio of 1 with 95 percent
confidence?
9. Show that a portfolio Sharpe ratio above the benchmark
Sharpe ratio implies a positive alpha for the portfolio,
but that a positive alpha does not necessarily imply a
Sharpe ratio above the benchmark Sharpe ratio.
TECHNICAL APPENDIX
We will discuss three technical topics in this appendix: how to
cumulate attributed returns, how to combine forecast and realized
risk numbers for performance analysis, and a valuation-based ap-
proach to performance analysis.
Cumulating Attributed Returns
We will investigate two issues here: cumulating active returns and
cumulating more generally attributed returns. Let Rp(t) be the port-
folio’s total return in period t, and let R;(t) and R;,(t) be the total
return on the benchmark and the risk-free asset. The compound
total return on portfolio P over periods 1 through T, R,(1,T), is
the product
Tr
Rp(1,T) = Rp(1) + Rp(2) + Rp(3) -
+
+ Re(T) = If Rp(t)
(17A.1)
t=1
Performance Analysis
511
Similarly, we calculate the cumulative benchmark return as
IE
Rg(1,T) = Ra(1) « Ra(2) + Ra(3)
+
+ Ra(T) = |] Ra(t)
(17A.2)
t=1
Hence the active cumulative return must be
Rpa(1,T) = Rp(1,T) — R3(1,T)
(17A.3)
Note that we do not calculate active cumulative returns by some-
how cumulating the period-by-period active returns. For example,
Rpa(1, T)
(17A.4)
7 det Rol) — Re)) + [1 + Re) = RaQ)
11 + RaT) — RQ)
Now consider the more general problem of cumulating attrib-
uted returns, and just focus on the problem of cumulating the
portfolio returns (not active returns). For each period t,
Rp(t) = Re(t) +S) xp((t) « BCE) + uplt)
(17A.5)
j
and hence
Rp(1,T) = |ReQ) + >" xp(1) + BA) + up(1)
(17A.6)
j
oe e RAT) + SY xp(T) + B(T) + uplT)
j
Equation (17A.6) contains many cross-product terms. We would
like to write this as
Rp(1,T) = Re(1,T) + >) xp(1,T) - b(1,T) + up(A,T) + Ber,
(17A.7)
j
attributing the cumulative return linearly to factors plus a cross-
product correction dcp. There are two straightforward approaches
to defining the cumulative attributed returns, one based on a bot-
tom-up view and the other based on a top-down view. The bottom-
up view cumulates each attributed return in isolation:
x(1,T) « (1)
(174.8)
==) (1)
xpj(1) : b(1)] so) De) oat, xp(T) : b(T)] — R,(1,T)
The top-down view attributes cumulative returns by deleting each
512
Implementation
factor in turn from the cumulative total return and observing the
effect:
xp,(1,T) - 6((1,T)
(17A.9)
= Rp(1,T) — [Rp(1) — x91)» BQ) +
- « [Re(T) — xp(T) - B(T)]
We recommend the top-down approach [Equation (17A.9)], which
often leads to smaller cross-product correction terms Scp in Eq.
(17A.7). Given that the cross-product term is usually small, and
that intuition for it is limited, we often attribute the cross-product
term back to the factors, proportional to either the factor risk or
the factor return.
Risk Estimates for Performance Analysis
We observe returns over T periods t = 1,...,T and wish to analyze
performance. Prior to the period, the estimated risk of these returns
WaS Oprior(O). The realized risk for the returns is o,,.. Both risk
numbers are sample estimates of the “true” risk. What is the best
overall estimate of risk, given these two estimates?
According to Bayes, if we have two estimates, x, with standard
error o; and x, with standard error o,, and the estimation errors
are uncorrelated, then the best linear unbiased estimate, given these
two estimates, is
x= ("| ae (2)
(17A.10)
of? + of)
oi + 05 *2
:
Equation (17A.10) provides the overall estimate with minimum
standard error o.
We also know that the standard error of a sampled variance
is approximately
SE{variance} = variance - 2
(17A.11)
fh
where T is the number of observations in the sample-and we assume
that the distribution of the underlying variable is normal.
Performance Analysis
513
Combining Eqs. (17A.10) and (17A.11), our best risk estimate is
Th
thee oat
O? = Grios(0) °
+ oral
(17A.12)
mea
eel,
where T) measures the number of observations" used for the esti-
mate Of Opricr(0).
Valuation-based Approach to
Performance Analysis
The theory of valuation (Chap. 8) defined valuation multiples v
such that
_ EX(cf(T)} _ Ely + cf(T))
(Oa at a
(17A.13)
where p(0) is the current value of the asset based on its possible
future values cf(T) at time T. Defining total returns as
Seip)
= (0)
(17A.14)
we see that
Deg ite
ess,
ts +i
(17A.15)
One aspect of the valuation multiples, which is shown by Eq.
(17A.15), is that they fairly price all assets. Within the context of
the CAPM and APT, all returns are fairly priced with respect to
portfolio Q. A manifestation of this is that under this adjusted
measure, they all have the same value. Equation (17A.15) states
that the set of possible returns R should be worth $1.00 using the
valuation multiples u
In the valuation-based approach to performance analysis, the
benchmark plays the role of portfolio Q. We determine the valuation
multiples by the requirement that they fairly price the benchmark
and the risk-free asset. The observed set of benchmark returns and
"We can define Ty implicitly using SE{o>,i0(0)} = /2/To if we have an estimate of the
standard error of o%rio-(0).
514
Implementation
the observed set of risk-free returns will each be priced at $1.00.
How much will the observed portfolio returns be worth then?
How do we choose the valuation measure? We could use the
results from Chap. 8, that
This has certain problems, as discussed before; for instance, it isn’t
guaranteed to be positive. Alternatively, we can use a result from
continuous time option theory, that
— (In[Rp(t)/Re(t)] + 0? - At/2)
v(ra(t),ict)) = 8 > op|
Se GaeeR?
}
(17A.17)
where we use 8 here as a proportionality constant. Given Eq.
(17A.17), the valuation multiples are guaranteed to be positive, and
we can choose 6 and o by the requirement that they fairly price
the observed set of benchmark returns and risk-free returns:
v: R;(t) St
Dera
(17A.18)
uv: R(t) _
=
2 Pea
ops eS
(17A.19)
Once we have used Eqs. (17A.18) and (17A.19) to determine 8 and
o, we can calculate the value added of the portfolio as
v + Rp(t)
R-(t)
Value added = 5°
=a
(17A.20)
t
.
5)
We can apply Eq. (17A.20) to attributed returns, as well as to
the total portfolio returns, to calculate value added factor by
factor:
a
Ba
Value added = »;
€
RO
sol. wn (1 ZAG2))
Performance Analysis
515
Now, using Eq. (17A.19) and switching the summation order
leads to
£3
v + rp(t)
Value added = a 2 Ry
(17A.22)
]
Exercise
1. Over a 60-month period, the forecast market variance
was (17 percent)’, with a standard error of (5.1 percent)’,
and the realized (sample) variance was (12 percent)’.
What is the best estimate of market variance over this
period?
Applications Exercises
1. Compare the Major Market Portfolio to the S&P 500 over
the past 60 months. What were the best and worst
policies of this active portfolio?
2. What are the largest and smallest attributed returns in
the most recent month?
li
y,
pe
See TD
od FE, HO
1}
( yo vi
3
bead
ee RF
Tt
ph
Maret
ttn
qoheqiitions Semele Gi Bama,
—
:
ew sy
dal
ire
[Vere NS al
i @ ou
wiht
pw
aie,
A) Cate AE
awh
ts
Willi Bia repscint. Ot uk
vette
retire
iv AG
’
mmihiet? 48 ce
-
»
tel bt onisy
Ss
=
~~
~
a
@v
late"
_—
o 4 ted
o ~ ane
Vien “1 ry cae
iy
2deatn
Gh saps Se eden
,
‘tohed
Lets
@ Vitiiggienes cre B
“ts
;
ache ‘i
Vue
cities Sed
a epee
sys
"
sone
:
righ "7
™)
pate
* fis viary! Sua 9
w/;
