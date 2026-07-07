# Chapter 10: Forecasting Basics

- **book_name**: Active Portfolio Management
- **main_source**: pdf
- **cross_check_source**: none
- **pdf_role**: main_text_source
- **split_scope**: pages 283-316

---

CHAPTER
10
Forecasting Basics
INTRODUCTION
We have completed our discussion of expected returns and valua-
tion. We now move on to the third major section of the book:
information processing. We now assume some source of alpha
information. In this section, we tackle a critical problem: how to
efficiently analyze and process that information. We will spend two
chapters looking forward: describing how to turn information into
alphas. We will then look backward, with a chapter on information
analysis. The last chapter in this section will look forward and
backward, covering the information horizon.
Active management is forecasting. The consensus forecasts of
expected returns, efficiently implemented, lead to the market or
benchmark portfolio. Active managers earn their title by investing
in portfolios that differ from their benchmark. As long as they claim
to be efficiently investing based on their information, they are at
least implicitly forecasting expected returns.
Forecasting is too large a topic to deal with adequately in this
book. Instead, we will give the reader some insight into how forecast-
ing techniques can refine raw information and turn it into alphas and
forecasts of exceptional return. Earnings estimates, measures of price
momentum, and brokers’ buy recommendations are pieces of raw
information. This chapter and the next will discuss how to turn such
raw information into forecasts of exceptional return.
These two chapters on forecasting and the following chapters
on information analysis and the information horizon are all closely
261
262
Information Processing
linked. In this chapter, we will try to deal with terminology and
gather some insights. In the next chapter, “Advanced Forecasting,”
we will apply those insights to some standard real-world issues
faced by most active institutional investment managers. In Chap.
12, “Information Analysis,” we will show how we can evaluate the
ability of a variable or a combination of variables to predict returns.
In Chap. 13, “The Information Horizon,” we will focus specifically
on the critical time component of information, using the tools devel-
oped in the previous chapters.
The main insights gained in this chapter are the following:
= Active management is forecasting.
# The unconditional or naive forecast is the consensus
expected return. The conditional or informed forecast is
dependent on the information source. Historical averages
make poor unconditional forecasts.
# A basic forecasting formula connects the naive and
informed forecasts, and handles single and multiple
sources of information.
® The refined forecast has the form volatility - IC - score.
® Forecasts of return have negligible effect on forecasts of
risk.
NAIVE, RAW, AND REFINED FORECASTS
Here we will introduce several types of forecasts, and establish a
link between our forecasts and returns via the basic forecasting
formula. The naive forecast is the consensus expected return. It is
the informationless (or uninformed) forecast. The naive forecast
leads to the benchmark holdings.
v
The raw forecast contains the active manager’s information in
raw form: an earnings estimate, a buy or sell recommendation, etc.
The raw forecast can come in a variety of units and scales, and is
not directly a forecast of exceptional return.
The basic forecasting formula transforms raw forecasts into
refined forecasts. The outputs of the formula are forecasts in the
form (and units) of exceptional returns, adjusted for the information
Forecasting Basics
263
content of the raw forecast. The formula (which we derive in the
appendix) is!
E{r\g} = E{r} + Cov{r,g} - Var“{g} - (g — E{g})
(10.1)
where r = excess return vector (N assets)
= raw forecast vector (K forecasts)
E{r} = naive (consensus) forecast
E{g} = expected forecast
E{r | g} = informed expected return: the expected return
conditional on g
At its core, Eq. (10.1) relates forecasts that differ from their expected
levels to forecasts of returns that differ from their expected levels.
In fact, we will define the refined forecast as the change in expected
return due to observing g:
o = E{r | g} — E{r} = Covirg} - Var“ {g} - (g — E{g})
(10.2)
This is the exceptional return referred to in previous chapters.
It can include both residual return forecasts and benchmark timing.
And, given a benchmark portfolio B, the naive (consensus) forecast is
E(t} = B- pes
:
(10.3)
where we define betas relative to the benchmark and p, is the
consensus expected excess return of the benchmark. Historical aver-
age returns are a poor alternative to these consensus expected
returns for the active manager. As discussed in Chap. 2, historical
average returns have very large sample errors, and are inappropri-
ate for new or changing stocks. More importantly, Eq. (10.3) pro-
vides consensus returns leading to the benchmark.
An equivalent way to think about the basic forecasting formula
is to apply it directly to the residual returns 0. Then, instead of Eq.
(10.3), we have the equivalent result
E{0} = 0
(10.4)
'We are using the notation for conditional expectation E{r\g} somewhat loosely.
264
Information Processing
the consensus expected residual returns are 0, and
a = Cov{6,g} - Var'{g} - (g — E{g})
(10.5)
In the next sections we will explore the meaning and use of
the basic forecasting formula.
REFINING RAW INFORMATION: ONE ASSET
AND ONE FORECAST
Let’s start with the simplest case—one asset and one forecast—and
look at it in two ways. First, we will use the pedagogical tool of
the binary model, which we introduced in Chap. 6. Here we will
see exactly the processes generating returns and forecasts. Second,
we will use regression analysis, where we will not see the underly-
ing processes. Fortunately, these two approaches to the same prob-
lem lead us to roughly the same conclusion. This mutual confirma-
tion will reinforce our trust in the formula for refining information.
As a side benefit, we will extract a forecasting rule of thumb that
will prove useful in countless situations.
In the binary model, we presume that we understand the
processes generating returns and forecasts. Suppose we are forecast-
ing return over one quarter; the expected excess return over the
quarter is E{r} = 1.5 percent, and the quarterly volatility is 9 percent.
That is equivalent to an annual expected excess return of 6 percent
and an annual volatility of 18 percent.
We can write the return we are forecasting as
r=15+0,+ 0,+--- + 05,
(10.6)
where 1.5 is the certain expected return, and the 81 random elements
0; capture the uncertain component of the return. The 6; are indepen-
dent and equally likely to achieve +1 or —1; thus, each 0; has
expectation 0 and variance 1. The variance of r is 81, corresponding
to the desired 9 percent per quarter volatility. We can think of the
variables 6; through 6s; as unit bundles of uncertainty. The random
component in the return is the sum of these 81 simple components.
We cannot observe the values of the individual 0; we can only
observe the sum, f.
We observe the return at the end of an investment period, but
we must forecast at the beginning of the period. Invour example,
Forecasting Basics
265
the forecast, g, has an expected value of 2 percent and a standard
deviation of 4 percent. We can model the forecast in a manner
similar to the return:
C20 Pos
es + 03 tat Mp
Tis
(10.7)
The variables 6, through 0; are elements of the return r. The fore-
caster actually knows something about part of the return, and
knows it at the beginning of the period. The components ,; through
N13 are additional bundles of uncertainty in the forecast. They have
nothing to do with the return. The forecast is a combination of
useful and useless information. The y; are independent of each
other and independent of the @;. Each nj can achieve +1 or —1 with
equal probability. We can think of the 6; as bits of signal and the
7m; as bits of noise. The forecaster gets 16 unit bundles of information;
3 are signal, 13 are noise. Alas, the forecaster sees only the sum
and cannot sort out the signal from the noise.
The covariance of g and r is simply the number of elements
of return that they have in common. In this case, Cov{r,g} = 3 (0,
through 63). The correlation between g and r is the skill level or IC:
ah
SEOUL Ret See
~ Std{r}
- Std {g}
9-4
We obtain the best linear estimate of the return conditional on
knowledge of g by using Eq. (10.1). Focusing now on the refined
forecast, for the case of a single asset and a single forecast, we can
express this as
IC = Corr{r,g}
= 0.0833
(10.8)
me,
ob = Std{r} - Corr{r,g} - bere
(10.9)
In this particular case, we have
b = 9 - 0.0833 - (22)
(10.10)
THE FORECASTING RULE OF THUMB
In the case of one asset and one forecast, we refine the forecast by
= Standardizing the raw forecast by subtracting the
expected forecast and dividing by the standard deviation
266
Information Processing
of the forecasts. We call that standardized version of the
raw forecast a score or Z score.
= Scaling the score to account for the skill level of the
forecaster (the IC) and the volatility of the return we are
attempting to forecast.
Equation (10.9) leads to the forecasting rule of thumb:
Refined forecast = volatility - IC - score
(10.11)
With this rule of thumb, we can gain insight into the forecasting
process and derive refined forecasts in unstructured situations. In
our example, we have a (quarterly) volatility of 9 percent and an
IC of 0.0833. The refined forecast will be 0.75 = 0.0833
- 9 times
the score (the standardized raw forecast). If the scores are normally
distributed, then our refined forecast will be between —0.75 and
+0.75 percent two quarters out of three. The refined forecast will
be outside the range {—1.50 percent, +1.50 percent} one quarter
in twenty.
The forecasting rule of thumb [Eq. (10.11)] also shows the
correct behavior in the limiting case of no forecasting skill. If the
IC = 0, then the refined forecasts are all zero, as they should be
in this case.
We will find the same rule of thumb if we use regression
analysis instead of the binary model. In the binary model, we
presumed that we knew the structure generating the returns and
the forecasts. In reality, we are in the dark and must make inferences
from available data, or guess based on experience and intuition.
Given the data, we will refine the raw forecasts using regression
analysis.
Consider a time series of forecasts g(t) and subsequent returns
r(t) over a sample of T periods. Let m, and m, be the sample averages
for r and g, and let Vartr}, Var{g}, and Cov{r,g} be the sample
variances and covariances. We will use the time series regression
r(t) = cy + cy - g(t) + eff)
(10.12)
as our refining tool. The least-squares estimates of c, and cp are
n Covir,g} a Std{r} - Corrtr,g}
Cy
Varig]
Stdigl
(10.13)
Ch
MN,
Cy
ttt
‘
(10.14)
Forecasting Basics
267
Defining the score as
_ git) — m,
z(t)
Std{g)
(10.15)
and using the regression results and the definition of refined fore-
cast, we find
b= Stiri
Comigg). = Zl. 1)
(10.16)
= volatility - IC - score
This is identical to the result in the binary model, except that we are
now using the sample history to estimate the IC and the volatility of
r and to standardize the raw forecast.’
So both the binary model and the regression analysis lead to
the same forecasting rule of thumb: The refined forecast of excep-
tional return has the form volatility - IC - score. For a given signal,
the volatility and IC components will be constant, and the score
will distinguish this forecast for the asset from previous forecasts
for the asset.
Forecasts have the form volatility
- IC - score.
Intuition
This refinement process—converting raw forecasts into refined
forecasts—controls for three factors: expectations, skill, and volatil-
ity. The score calculation controls for expectations by the subtraction
of the unconditional expected raw forecast. We can illustrate the
intuition here with an example: earnings surprise. An earnings
surprise model forecasts alphas based on how reported earnings
compare to prior expectations. When earnings just match expecta-
tions, the stock price doesn’t move. More generally, we expect ex-
ceptional price movement only when the raw information doesn’t
match consensus expectations.
2As we have noted earlier, our estimates of the means of the returns m, generally
contain a great deal of sample error. The sample errors affect the parameter cy =
m, — C, * My. If we have a strong prior reason to believe that the unconditional
expected return is equal to m, then we can replace the estimate of the coefficient
Cy by cf = m — c, : m,. A Bayesian analysis would start with a prior that the mean
is m + d and then mix in the sample evidence.
268
Information Processing
The refinement process controls for skill through the IC term.
If IC = 0, the raw forecast contains no useful information, and we
set the refined forecast of exceptional return to zero.
Finally, the refinement process controls for volatility. Note first
that in the volatility - IC - score construction, the IC and score terms
are dimensionless. The volatility term provides the dimensions of
return. Also note that given a skill level and two stocks with the
same score, the higher-volatility stock receives the higher alpha.
Perhaps a utility stock and an Internet stock both appear on a
broker’s buy list. We expect both stocks to rise. The Internet stock
(presumably the more volatile) should rise more.
As we will discuss in the next chapter, the forecasting rule of
thumb can also hold for a cross-sectional forecast of exceptional
returns, so the score is what distinguishes one stock from another.
The average and standard deviation of the time series of scores for
a particular stock over time should be close to 0 and 1, respectively.
The average and standard deviation of the scores over many stocks
at one point in time should also be close to 0 and 1, respectively.
Table 10.1 illustrates the rule of thumb for the Major Market
Index as of December 1992. We have used an IC level of 0.09 and
used a random number generator to sample the scores from a
standard normal distribution.
REFINING FORECASTS: ONE ASSET AND
TWO FORECASTS
Let’s go back to the binary model and assume we are forecasting
the same excess return r with the forecast g from before and a new
raw forecast 9’:
gy = 0.5 +03 + O, + 05 + O06 + Ho tH te
(10.17)
+ Neo
of
Forecasts g and g’ share one element of signal (83) and four elements
of noise (N10, Nu, Nz, ANd 13). Forecast g’ has 25 units of uncertainty;
thus Var{g’} = 25. Forecast g’ contains four elements of signal
(03, 04, 05, 9); thus Cov{r,g’}
= 4. The correlation of r and g’ (IC,
is Corr{r,g'}
= 4/(9 - 5) = 0.089. Forecast g’ has five bits of informa-
tion in Coma with forecast g (83, Yio, Nn, Thy and ma), and thus
Covig,g’}
=
Forecasting Basics
269
TABLE
10.1
MMI Stock
Residual Volatility
American Express
23.26%
AT&T
15.89%
Chevron
20.44%
Coca-Cola
18.92%
Disney
19.17%
Dow Chemical
16.93%
DuPont
17.29%
Exxon
21.13%
General Electric
14.42%
General Motors
23.46%
IBM
30.32%
International Paper
19.83%
Johnson & Johnson
18.97%
Kodak
19.20%
McDonalds
20.54%
Merck
20.43%
3M
:
13.41%
Procter & Gamble
16.29%
Philip Morris
20.17%
Sears
22.33%
We now have enough information to use Eq. (10.1). If we were
using only g’ in this example, we would find
b = 9 - (0.089) - (525) = (0.16) -(g’ — 0.5)
(10.18)
but combining g and g’, we find
w= 10.1467)" {= 2.0) + (01307) > 0:5)"
(10.19)
with an IC for the refined combined forecast of 0.1090.
In the case of one asset and two forecasts, we can actually
calculate an explicit general result (and rule of thumb):
= Std{r}
- IC* + z, + Std{r} - IC¥ + zy
(10.20)
The revised skill levels IC} and IC} take into account the correlation
270
Information Processing
between the forecasts. If p,, is the correlation between forecasts g
and g’, then:
1Gharp
ree i
(10.21)
ICy =
peer IC
(artes
MU
Ee
(10.22)
1 — peg
If the forecasts are uncorrelated, the combined forecast reduces
to the sum of the refined forecasts for g and g’. If the forecasts are
completely correlated (p,.. = 1), then Eqs. (10.21) and (10.22) break
down (remember that IC, = IC, in that case). The second forecast
adds nothing.
We could equivalently repackage the scores instead of the ICs.
The idea would be to create orthogonal linear combinations of the
original scores. In the two-signal example here,
pamela
feet
(10.23)
V2 dal
Lieks Des)
and
i
(10.24)
‘
V y ° (1 4 Pee’)
They would exhibit revised ICs
V2
pay
and
Ic#* = 1G 1G
(10.26)
‘i
V Be
7 @ a Peg’)
Since the repackaged scores are uncorrelated, combining them re-
duces to simple addition.
We can also show that in the two-signal case the IC ofthe
combined forecast is
Ce
Ch
es Oe el
rele
1 — py
(10.27)
(@arned =
If the forecasts are uncorrelated, the square of the combined IC is
the sum of the squares of the two component ICs.
>
Forecasting Basics
271
We can repeat the two-forecast, one-asset example with regres-
sion analysis. The time series regression is now
rif) = cy + ce, et) + c,* 9’) + eff)
(10.28)
and our refined forecast will be
Pe eye te l= Wises Le eb)
my]
(10.29)
In our example, with a sufficiently long history (T is very large),
we would estimate c, close to 0.1467 and c, close to 0.1307.
The case of one asset and more than two signals involves more
complicated algebra (see the appendix for details). But we can
provide some suggestion of what the refinement process does in
those cases. Imagine, for example, three signals, each with the same
IC. What if the first two signals are highly correlated, but are
uncorrelated with the third signal? If all three signals were uncorre-
lated, we would equal-weight them (simply add the separately
refined forecasts). But the refinement process will account for the
correlations by halving the ICs of the two correlated signals. Effec-
tively, we will count the uncorrelated signal equally with the sum of
the two correlated signals. The general mathematical result captures
this intuitive idea, while accounting for all possible intercorre-
lations.
REFINING FORECASTS: MULTIPLE ASSETS
AND MULTIPLE FORECASTS
With multiple assets and multiple forecasts, it is more difficult to
apply the basic forecast rule. This is because we lack sufficient data
and insight to uncover the required structure. With two forecasts
g and g’ on each of 500 stocks, the covariance matrix of g and g’
is 1000 by 1000, and the covariance of the returns and g and g’ is
a 500 by 1000 matrix. We will treat this topic in the next chapter,
although this chapter includes some simple examples.
EXAMPLES
Now we will consider several practical and less structured exam-
ples that rely heavily on our volatility - IC - score rule of thumb
for producing a refined forecast of exceptional return. We are assum-
272
Information Processing
ing that estimates of residual volatility are available. In the absence
of sufficient historical information to decide on the IC of the raw
forecasts, use these vague but tested guidelines: A good forecaster
has IC = 0.05, a great forecaster has IC = 0.10, and a world-class
forecaster has IC = 0.15. An IC higher than 0.20 usually signals a
faulty backtest or imminent investigation for insider dealing.
A Tip
Consider that most ad hoc of all situations, the stock tip.’ Let’s say
the stock in question has typical residual volatility of 20 percent.
To change the subjective stock tip into a forecast of residual return,
we need the IC and the score. For the IC, look to the track record
of the source: If the source is great, set IC = 0.1; if the source is
good, IC = 0.05; and if the source is a waste of time, then IC = 0.
For the score, we can give a run-of-the-mill tip (very positive) a
1.0 and a very, very positive tip a 2.0. Table 10.2 shows the spectrum
of possibilities and the ability to transform some unstructured quali-
tative information into a more useful quantitative form.
Up/Down Forecast
In a major investment firm, the most notorious and accurate fore-
caster was a fellow named Charlie. For years, as portfolio managers
filed into work, Charlie greeted them with the enthusiastic words:
“Market's going up today!” Charlie was right two-thirds of the
TABLE
10.2
Very, Very Positive
Ic
Very Positive (Score = 1)
(Score = 2)
Great 0.10
2.0%
4.0%
Good 0.05
1.0%
2.0%
No information 0.00
0.0%
0.0%
~
*Andrew Rudd suggested this example.
Forecasting Basics
273
time. Of course, Charlie’s forecasts weren’t very valuable, since
the market should on average go up, and two-thirds is about the
historical average. The value in the forecast comes from separating
up days from down days.
Suppose the expected annual market return is 6 percent with
annual risk of 18 percent, corresponding to an expected monthly
return of 0.50 percent with a monthly standard deviation of 5.20
percent. We
can
represent monthly up/down
forecasts
as
Raw(t) = +1 for up and Raw(t) = —1 for down. If the raw forecasts
are consistent with the returns, i.e., two-thirds are +1, then the
mean and standard deviation of the raw scores will be 1/3 and
0.9428, respectively. The standardized scores are 0.707 and —1.414.
Given an IC (correlating the forecasts with the returns), we find
that Refined = 0.50 + (5.20)
- IC - (0.707) for an up forecast and
Refined = 0.50 — (5.20)
- IC - (1.414) for a down forecast. With
moderate skill (IC = 0.075), the forecasts are 0.78 percent for an
up market and —0.05 percent for a down market. The asymmetry
follows because, in the absence of any information, we expect an
up market with a 0.50 percent return.
Buy and Sell Recommendations
A more structured example involves a buy and sell list. In this
case, we give a score of +1.0 to the buys and a score of —1.0 to
the sells. If we apply this to the Major Market Index stocks, with
a random choice of buy and sell and an IC of 0.09, we see the
alphas shown in Table 10.3. The rule gives higher alphas to the
more volatile stocks. If we ignored the rule and gave an alpha of
+1 percent to the buy stocks and an alpha of —1 percent to the
sell stocks, then an optimizer would select those buy stocks with
the lowest residual risk.
Fractiles
Some managers group their assets into deciles or quintiles or
quartiles. This is a refinement of the buy/sell idea, which partitions
the assets into two groups. If assets have a raw score of 1 through
10 depending on their decile membership, we can turn these into
standardized scores by subtracting the average (perhaps value-
274
Information Processing
TABLE
103
Residual
MMI Stock
Volatility
Score
American Express
23.26%
AT&T
15.89%
Chevron
20.44%
Coca-Cola
18.92%
Disney
19.17%
Dow Chemical
16.93%
DuPont
17.92%
Exxon
21.13%
General Electric
14.42%
General Motors
23.46%
IBM
30.32%
International Paper
19.83%
Johnson & Johnson
18.97%
Kodak
19.20%
McDonalds
20.54%
Merck
20.43%
3M
13.41%
Procter & Gamble
16.29%
Philip Morris
20.17%
Sears
22.33%
weighted) raw score and dividing by the standard deviation of the
raw scores.
Rankings
A ranking is similar to a fractile grouping except that there is only
one asset in each group. We can look at the rankings, say 1 throtigh
762, as raw scores. First, check to see if the asset ranked 1 is the best
or the worst! Then we can, using various degrees of sophistication,
transform those rankings into standardized scores.
The Forecast Horizon: New and Old Forecasts
Suppose that we generate a raw forecast each month and that these
forecasts are useful in predicting returns for the next 2 months. In
Forecasting Basics
275
this case, the forecast frequency (how often the forecasts arrive) is
1 month and the forecast horizon (the horizon over which the
forecasts have predictive power) is 2 months. How do we operate
in this situation? As we will show in Chap. 13, the answer is to
treat the old forecast as a separate source of information and apply
the basic forecasting formula.
FORECASTING AND RISK
Suppose the correlation between the S&P 500 and the MIDCAP
has been 0.95 over the past 10 years, but new information leads to
a forecast that the S&P 500 will do poorly in the next quarter and
the MIDCAP will do well. The temptation is to replace the historical
correlation, 0.95, with a negative correlation, since we believe that
S&P 500 and MIDCAP returns will move in opposite directions.
This temptation is incorrect. This line of thought confounds
the notion of conditional means (i.e., the expected return on the
S&P 500 taking into consideration the research) and the notion
of conditional covariance (i.e., how the research should influence
forecasts of variance and covariance).
It is surprising to note that forecasts of returns have negligible
effect on forecasts of volatility and correlation. It is even more
surprising to note that what little effect there is has nothing to do
with the forecast and everything to do with the skill of the forecaster.
Thus, in our example, we would adjust the risk forecast in the same
way even if the forecast were for the S&P 500 to do well and the
MIDCAP to do poorly! This welcome news makes life easier. We
can concentrate on the expected return part of the problem and
not worry about the risk part.
This result arises because risk measures uncertainty in the
return. A skillful forecaster can reduce the amount of uncertainty
in the return, and a perfect forecaster reduces the uncertainty to
zero (the returns can still vary from month to month, but only
exactly according to forecast). For any forecaster, however, the size
of the remaining uncertainty in the return stays the same, indepen-
dent of any particular forecast. And, given typical skill levels, the
reduction in risk due to the skill of the forecaster is minimal.
276
Information Processing
ST
TABLE
10.4
Let opriog and oposr be estimates of volatility without forecast
information and with forecast information. The formula’ relating
these is
Opost = Oprior
* V1 — IC?
(10.30)
Table 10.4 shows how a preforecast volatility of Opriog = 18 percent
(annual) would change depending on the IC of the researcher.
Reasonable levels of the IC (from 0 to 0.15) have very little effect
on the volatility forecasts.
So much for the volatility forecasts. What about the correla-
tions? The calculation is more complicated, but the general result
will be the same. Consider the simplest case of two assets and two
forecasts. We now have four balls in the air. We will call the assets
S&P 500 (L for large) and MIDCAP (M for medium). The task is
to determine how the correlation between the medium and large
stock returns will be changed by our research. This will require
some notation. Suppose that the correlation between the medium
and large stock returns is py, (in our example, py, = 0.95). The
term IC, captures the correlation between the forecasts for the
MIDCAP and the subsequent MIDCAP returns. A typical (optimis-
‘The basic variance forecasting formula is
Var{r|g} = Var{r} — Cov{rg} - Var-{g} - Covig,r}
This leads to Eq. (10.30). This formula is discussed in Proposition 2 of the
technical appendix.
.
Forecasting Basics
277
tic) number is 0.1. The term IC, is the correlation between the large
stock (S&P 500) forecasts and the subsequent S&P 500 returns—
again, typically 0.1 or smaller.
We will assume that the correlation between the forecasts is
also py,. We also have to specify the cross-correlations between the
MIDCAP forecasts and the S&P 500 return and between the S&P
500 forecasts and the MIDCAP return. For simplicity, we will as-
sume that these are zero.°
Under those reasonable assumptions, we find the following
formula for the revised correlation:
oie
eee
ii ICu i Kee
PML <a PML
Se
V (1. — IC) - A — IC?)
At first, this appears to be a formidable equation. However, if
ICy = IC;, then the naive correlation forecast is unchanged. A little
analysis will show that the correlation changes very little when the
information coefficients are in the 0 to 0.15 range. Once again, the
revised correlation depends only on our skill at forecasting and
not on the forecast.
What can we conclude? The researcher who tries to forecast
returns over the near horizon should ignore the slight impact of
those forecasts on the volatility and correlation estimates for the
assets. Asset allocators in particular should take note of this. Many
asset allocators are seduced by the possibility of forecasting volatil-
ity and correlation along with returns. They believe that the market
has changed and is obeying a new reality. The same force responsi-
ble for the exceptional returns is also changing the covariance struc-
ture. This is easier to imagine than to establish. There is some
evidence of “regime changes” in short-run currency volatilities
and correlations, however, in general there is more stability than
instability in asset volatilities and correlations.
(10.31)
‘It might be slightly more clever to say that the MIDCAP forecast gives us some insight
(through IC,,) into future MIDCAP returns, and that future MIDCAP returns give
us insight (through py.) into future S&P 500 returns. That would lead us to
correlations of ICy - py, between the MIDCAP forecast and the S&P 500 return,
and of IC; - py, between the S&P 500 forecast and the MIDCAP return.
278
Information Processing
ADVANCED TECHNIQUES
Up to this point, we have concentrated on simple techniques like
counting in the binary model or linear regression. There are a host
of more sophisticated forecasting procedures. As a general rule,
increasing levels of sophistication carry both additional power and
a larger chance that you may lose control of the process: The invest-
ment insights become submerged, the technique takes over, and
you lose sight of the statistical significance of the results. If the
technique is in control of you rather than the other way around,
then you should probably look for more basic and more stable tools.
A guiding principle is to move from the simple to the more
complicated; master the simple cases, understand the shortcomings,
and then move to more complicated situations and techniques.
Also, when using sophisticated techniques, always run two specific
tests to make sure they are working correctly. First, see how they
work when you feed in random data. Successful predictions from
random data indicate a problem. Second, feed in simulated data
where you know the underlying relationship. Does the sophisti-
cated technique find it? Many sophisticated techniques do not come
with associated statistical tests. Fortunately, modern computers,
combined with the bootstrapping methodology, allow you to run
your own statistical tests.
Here we will present several specific advanced techniques. In
the next chapter, “Advanced Forecasting,” we come back to the
basic methodology, but apply it to more complex, real-world situ-
ations.
Time Series Analysis
This is a world unto itself, with its own jargon and notation. The
textbook of Box and Jenkins (1976) is standard, as is the more resent
treatment by Liitkepohl (1991). The litany of models is:
AR(q). Autoregressive: The time t value of a variable, r(t),
depends on a weighted sum of the varible’s past g values
(r(t-1), r(t-2),..., r(t-q)} plus some random input, e(#):
WE)
dy hay’ 1th
UY ites cost ae Tagen Nee C2)
MA(p). Moving average: The time t value of a Variable is
Forecasting Basics
279
the weighted average of a sum of p + 1 random
(independent) inputs e(t), e(t — 1),..., e(t — p):
TD ea Ceci
Lisa
tC Nea Pct oc)
ARMA(q,p). Autoregressive moving average. You guessed
it, a combination of AR) and MA(p).
ARIMA. ARMA applied to first differences; i.e., instead of
looking at returns, look at the changes in returns.
VARMA. ARMA applied to more than one variable at a
time: vector ARMA. The method predicts K returns using J
possible explanatory variables along with their lagged
values.
ARCH, GARCH, etc.
ARCH stands for autoregressive conditional heteroskedasticity, and
GARCH for Generalized ARCH. Typically, the goal of these models
is to forecast volatility (and sometimes correlations). Robert Engle
developed this technique. For a review of applications in finance,
see the article by Bollerslev, Chou, and Kroner (1992).
The ARCH and GARCH methods apply when volatility
changes in some predictable fashion; e.g., periods of high volatility
tend to follow large negative or positive returns. The standard
GARCH model of volatility posits the following structure: Three
factors influence current volatility. First, even changing volatility
exhibits a long-run average. Second, mean reversion will tend to
move current volatility toward that long-run average. Third, recent
returns can shock volatility away from the long-run average. These
are basic time series concepts applied to volatility instead of return.
More advanced GARCH models allow for the differing influ-
ence of large negative and large positive recent returns. We often
observe that stock market volatility increases on downturns, but
decreases as the market rises.
ARCH and related nonlinear techniques are most useful when
a limited number of returns are under consideration; i.e., they are
more appropriate for asset allocation than for stock selection. In
risk models, these techniques can enhance the forecast covariance
matrix by improving the forecast of market or systematic risk. The
280
Information Processing
idea is to extract the most important single factor, and then apply
this advanced technique to that one time series. ARCH techniques
are most pronounced when the investment horizon is short—days
rather than the longer investment horizon of months or years.
Finally, ARCH techniques can be extremely useful in strategies that
have a strong option component, because better volatility forecasts
lead directly to better option prices.
Kalman Filters
Kalman filters are closely linked to Bayesian analysis. Our funda-
mental forecasting law is a simple example. We start with a prior
mean and variance for the returns and then adapt that mean and
variance conditional on some new information. Kalman filters work
in the same manner, although their working is often obscured by
electrical engineering/optimal control jargon. See Bryson and Ho
(1969), chap. 12, for an introduction to Kalman filters and an explo-
ration of the links with Bayesian analysis when the random vari-
ables are normally distributed. See the paper of Diderrich (1985)
for a link between Kalman filters and Goldberger-Theil estimators
in regression analysis.
Chaos
Chaos theory concerns unstable and nonlinear phenomena. In the
investment context, it has come to mean the discovery and use
of nonlinear models of return and volatility. We would like to
distinguish between random phenomena and predictable phenom-
ena that are generated in a deterministic but highly nonlinear way.
These can appear to be the same thing.
A typical example is the random-number generator. Comput-
ers generate random numbers in a totally reproducible way, but
the numbers appear to be random. The forecaster using chaos
theory starts with the output of the random-number generator and
tries to reverse-engineer the nonlinear rules that are used to produce
its outputs. This is not an easy task.
Another example of chaos is the tent map. Given an initial
number x(0) between 0 and 1, we generate the next number with
x(t) = Min{2- x(t — 1),2 — 2+ x(t — 1)}>
(10.32)
Forecasting Basics
281
Figure 10.1
If x(t) gets stuck on 0, choose x(f+1) at random. This rule will
produce a sequence of numbers that looks very much like a se-
quence of randomly distributed numbers between 0 and 1. How-
ever, if we look in two dimensions at the pairs {x(t-1),x(t)}, we see
that they all lie on the tent-shaped line in Fig. 10.1. For a true
sequence of random numbers, the pairs {x(t-1),x(f)} would fill up
the entire square in two dimensions.
To apply chaos theory to forecasting, take the residuals from
the forecasting rules and look at these two-, three-, and higher-
dimension pictures for evidence of a nonlinear relationship like the
tent map. If there is such evidence, strengthen the model by trying
to capture that relationship. See the paper by Hsieh (1995) for an
excellent application of this idea and some interesting modeling
techniques.
Neural Nets®
In the past few years, application of neural nets to various problems
across the spectrum of the investment world has gained wide pub-
’Hertz, Krogh, and Palmer (1991) is a standard reference.
282
Information Processing
Axon
Dendrites
Output =1if
B>T
0 otherwise
(b)
Figure 10.2
licity. Hornik, Stinchcombe, and White (1988) have shown that
neural nets can approximate almost any conceivable function. In
problems involving high signal-to-noise ratios, neural nets have
proved to be a powerful analytic tool. In problems involving low
signal-to-noise ratios, in particular forecasting exceptional returns,
the applicability of neural nets is far from certain.’
Neural nets are a model of computation inspired by biological
neural circuitry (see Fig. 10.2). Each artificial neuron weights several
input signals to determine its output signal nonlinearly. Typically,
as the weighted input signal exceeds some threshold T, the output
quickly varies from 0 to 1. A neural network is an assembly of
these artificial neurons, with, for example, a layer of input neuxons
feeding into an inner (hidden) layer of neurons that feeds into an
output layer (Fig. 10.3).
Neural nets can solve very general problems, but they are not
very intuitive. Unlike more standard computer programs, neural
nets do not have the problem solution built into them from the
7See Kahn and Basu (1994).
E
Forecasting Basics
283
Output
Hidden
Input
Figure 10.3
ground up. Instead, they are taught how to solve the problem by
training them with a particular set of data. The neural net is trained
(its internal coefficients estimated) to optimally match inputs with
desired outputs. Therefore, neural nets are very dependent on the
data used for training.
Neural nets have been applied to many areas of research and
finance. All of these fall into two general categories, which we can
illustrate by example. We characterize the first category by the
problem of modeling bond ratings. Here we wish to apply neural
net technology to predict bond ratings from underlying company
financial data. Effectively, we are reverse-engineering the process
implemented by Moody’s and S&P. We can characterize this prob-
lem by its nonlinear relation between the financial data and the
ratings, its relative stability over time, and its high signal-to-noise
ratio. We can illustrate the second general category by the applica-
tion of neural nets to forecasting returns. Here we wish to use
neural nets to predict asset returns from underlying financial and
economic data and past returns. We can characterize this problem
by its nonlinear relation between explanatory variables and ob-
served returns, its relative instability over time, and its low signal-
to-noise ratio.
Neural nets have worked well for the first type of problem,
characterized by nonlinearities, stable relationships, and high
signal-to-noise ratios. As for the second type of problem, many
financial researchers have applied neural nets here, with many
claims of success. However, definitive and statistically significant
proof of success is still lacking.
284
Information Processing
Genetic Algorithms®
Genetic algorithms are a heuristic optimization method motivated
by a loose analogy to the process of biological evolution. Species
evolve through survival of the fittest; each generation begets the
next through a mixture of mating, mutation, and training. The
overall population thus evolves in a semirandom manner toward
greater fitness.
The computational analogy is optimizing a function of several
variables, where each combination of the variables defines an “indi-
vidual” and the function to be maximized is the “fitness” criterion.
We choose a random initial “population” and evaluate the
fitness of each individual member; then we create each successive
generation by combining the fittest members of its prior generation.
We repeat this last step until we converge to a best solution. A
strong element of randomness in the “evolution” step allows wide
exploration of possible solutions. For instance, we can randomly
combine elements of the fitter solutions or randomly alter some
elements of a fit solution—we label these “mating” and “muta-
tion,” respectively.
One area where we have applied genetic algorithms is the
paring problem, e.g., find the best 50-stock portfolio to track the
S&P 500. A standard quadratic optimizer can find the optimal
portfolio weights for a given list of 50 stocks to track the S&P 500.
The tricky part is to search through the possible lists of 50 names.
The combinatorics involved guarantee that we can’t exactly solve
this problem.
BARRA and others have developed heuristic approaches to this
problem. After considerable research efforts (~6 person-months),
they have developed methods which quickly (a few seconds on a
1998 PC) find reasonable answers. As an alternative, they coded a
genetic algorithm in a weekend; it found similarly good answers to
this problem after about 48 hours of CPU time ona similarly powered
machine. So for this type of problem, genetic algorithms are quite
attractive as one-time solutions. They are perhaps less attractive for
use in industrial-strength commercial software.
®Holland (1975) is a standard reference.
*
Forecasting Basics
285
In the realm of forecasting, we often search for the signal with
maximum information ratio. Imagine instead a “population” of
possible signals, initially chosen at random, which we then “evolve”
using the criterion of maximum information ratio.
Since genetic algorithms are effectively able (in successful ap-
plications) to “learn” the characteristics of the fittest solutions, they
require less coding than analytic techniques, and they run faster
than an explicit examination of all possible solutions.
SUMMARY
Active management is forecasting. We can use a basic forecasting
formula to adjust forecast returns away from the consensus, based
on how far the raw forecasts differ from the consensus and on the
information content of the raw forecasts. We capture this basic
result in the forecasting rule of thumb: The exceptional return fore-
cast takes on the form volatility - IC - score. The chapter has applied
these relationships in several specific examples.
The next chapter will move on to some more complicated
situations, especially those involving multiple assets and cross-
sectional forecasts.
PROBLEMS
1. Assume that residual returns are uncorrelated, and that
we will use an optimizer to maximize risk-adjusted
residual return. Using the data in Table 10.3, what asset
will the optimizer choose as the largest positive active
holding? How would that change if we had assigned
a = 1 for buys and a = —1 for sells? Hint: At optimality,
assuming uncorrelated residual returns, the optimal
active holdings are
2-Drp*> wr
hy,
2. For the situation described in Problem 1, show that
using the forecasting rule of thumb, we assume equal
risk for each asset. What happens if we just use a = 1
for buys and a = —1 for sells?
286
Information Processing
3. Use the basic forecasting formula [Eq. (10.1)] to derive
Eq. (10.20), the refined forecast in the case of one asset
and two forecasts.
4. In the case of two forecasts [Eq. (10.20)], what is the
variance of the combined forecast? What is its covariance
with the return? Verify explicitly that the combination of
g and g’ in the example leads to an IC of 0.1090.
Compare this to the result from Eq. (10.23).
5. You are using a neural net to forecast returns to one
stock. The net inputs include fundamental accounting
data, analysts’ forecasts, and past returns. The net
combines these nonlinearly. How would the forecasting
rule of thumb change under these circumstances?
REFERENCES
Bickel, P. J., and K. A. Doksum. Mathematical Statistics (San Francisco: Holden Day,
1977), pp. 127-129.
Black, Fisher, and Robert Litterman, “Global Asset Allocation with Equities, Bonds,
and Currencies.” Fixed Income Research, Goldman, Sachs & Co., New York,
October 1991.
Bollerslev, T., R. Y. Chou, and K. F. Kroner. “ARCH Modeling in Finance.” Journal
of Econometrics, vol. 52, no. 1, April 1992, pp. 5-59.
Box, George E. P., and Gwilym M. Jenkins. Time Series Analysis: Forecasting and
Control (San Francisco: Holden-Day, 1976).
Bryson, A. E., and Y. C. Ho. Applied Optimal Control. (Waltham, MA: Blaisdell, 1969).
Chopra, Vijay Kumar, and Patricia Lin. “Improving Financial Forecasting: Combin-
ing Data with Intuition.” Journal of Portfolio Management, vol. 22, no. 3, 1996,
pp. 97-108:
Diderrich, G. T. “The Kalman Filter from the Perspective of Goldberger-Theil
Estimators.” The American Statistician, vol. 39, no. 3, 1985, pp. 193-198.
Grinold, Richard C. “Alpha Is Volatility Times IC Times Score, or Real Alphas
Don’t Get Eaten.” Journal of Portfolio Management, vol. 20, no. 4, 1994, pp. 9-16.
Hertz, J., A. Krogh, and Richard G. Palmer. Introduction to the Theory of Neural
Computation (Redwood City, Calif.: Addison-Wesley, 1991).
Holland, John H. Adaptation in Natural and Artificial Systems (Ann Arbor: University
of Michigan Press, 1975).
Hornik, K., M. Stinchcombe, and H. White. “Multi-layer Feedforward Networks
Are Universal Approximators.” Working paper, University of California,
San Diego, June 1988.
Hsieh, D. A. “Chaos and Nonlinear Dynamics: Application to Financial Markets.”
Journal of Finance, vol. 46, no. 5, 1991, pp. 1839-1877.
:
Forecasting Basics
287
. “Nonlinear Dynamics in Financial Markets: Evidence and Implications.”
Financial Analysts Journal, vol. 51, no. 4, 1995, pp. 55-62.
Johnson, N. L., and S. Kotz. Distributions in Statistics: Continuous Multivariate
Distributions (New York: John Wiley & Sons, 1972), pp. 40-41.
Kahn, Ronald N., and Archan Basu. “Neural Nets and Fixed Income Strategies.”
BARRA Newsletter, Fall 1994.
Liitkepohl, H. Introduction to Multiple Time Series Analysis (New York: Springer-
Verlag, 1991).
Rao, C. R. Linear Statistical Inference and Its Application, 2d ed. (New York: John
Wiley & Sons, 1973), pp. 314-333.
Searle, S. R. Linear Models (New York: John Wiley & Sons, 1971), pp. 88-89.
Theil, Henri. Principles of Econometrics (New York: John Wiley & Sons, 1971),
pp. 122=123:
TECHNICAL APPENDIX
This appendix will cover two technical topics: deriving the basic
forecasting formula, along with some related technical results, and
analyzing specific examples from the main text of the chapter.
The Basic Forecasting Formula
We will now show that the basic forecasting formula provides the
linear unbiased estimate with minimum mean squared error. Most
statistics books discuss this topic under the name of either minimum
variance unbiased estimates (m.v.u.e.) or best linear unbiased estimates
(b.l.u.e.),? and deal with the case where Var{g}, E{g}, and Covir,g}
are unknown.
Let’s start with the estimate:
t = E{r} + Cov{rg} « Var Ng} - (g — Elg})
(10A.1)
Proposition 1
fis
1. An unbiased estimate of r
2. The estimate of r that has the smallest mean squared
error among all linear estimates of r
%See Bickel and Doksum (1977), pp. 127-129; Theil (1977), pp. 122-123; and Rao (1973),
pp. 314-333.
288
Information Processing
Proof A general linear estimate can be written as
r(g;b,A)=bt+A-g
(10A.2)
The estimation error is q = r — r(g;b,A), and the mean squared
error is
MSE{b,A} = E{q’ - q} = HS a}
(10A.3)
To minimize the mean squared error, we take the derivative of
MSE{b,A} with respect to each of the N elements of b and each of
the N - K elements of A and set them equal to 0.
Setting the derivative with respect to b,, equal to 0 yields
K
be
AEM
Dvuucl ee)
(10A.4)
k=1
This result, along with Eq. (10A.2), demonstrates that the expected
error is 0, i.e., the linear estimate that minimizes mean squared
error is unbiased. We can therefore restrict our attention to linear
estimates of the form
r(g;b,A) = E{r} + A: (g — E{g})
(10A.5)
For convenience, let us introduce the notation s = g — E{g} and
p =r -— E {r}. With this notation, we have q = p — A-
5s, and so
E{g} = 0 and
MSE{A} = E{p’: p} — 2: E{p’-
A- s} + E{s’- AT- A-s}
(10A.6)
3
Taking the derivative of the mean squared error with respect to
the element A, leads to
K
E{Gn/Si3 = Cov {nS = H(
Pn =. By Ags . 3}
Ma ss (10A.7)
j=l
According to Eq. (10A.7), the errors in our estimate areuncorrelated
Forecasting Basics
289
with the raw forecasts. If q and s are correlated, we are leaving
some information on the table; we should exploit any correlation
to further reduce the mean squared error.
In matrix notation, Eq. (10A.7) becomes
E{q - s'} = Covirg} — A: Var{g} = 0
(10A.8)
A = Covirg} - Var -{g}
(10A.9)
Equations (10A.9) and (10A.5) now demonstrate that f is the linear
estimate with minimum mean squared error.
The linear estimate f has additional properties if rand g have
a joint normal distribution.
Proposition 2
If {rg} have a normal distribution, then
1. fis the maximum likelihood estimate of r given g.
2. # = E{r|g} is the conditional expectation of r given g.
3. Var{r|g} = Var{r} — Covirg}
- Var-'{g}
- Cov{g,r} is the
conditional variance of r given g.
4, ¢ has minimum mean squared error among all unbiased
estimates, whether they are linear or not.
Proof
The covariance of r and g is
Ss Var{r}
en
Covig,r}
Varig}
oe)
and the inverse covariance matrix is
ey
meee
ro
i
Os er Ol 4,
vino= {ae Os
rae
Given an observation {p,s} and the normal distribution assumption,
the likelihood of that observation is
ih
alay
6
ve \-
(p’s’) 2 all
[ee
2 eae
(104.12)
V (2a)" ** det[Q]
290
Information Processing
Maximizing the log likelihood function is therefore equivalent to
minimizing
p’: Qir}: p +2:
p’- O{rg}-s +s"- O{g}-s
(10A.13)
If we fix s and choose p to minimize Eq. (10A.13), the optimal p* is
p= —O
“rl: Olsg!
«is
(10A.14)
However, since Q is the inverse of V, we can use Eqs. (10A.10) and
(10A.11) to show that
Covirg} - Var {g} = —Q"'{r} - O{rg}
(10A.15)
Equations (10A.14) and (10A.15) establish item 1.
Items 2 and 3 are standard properties of the multinormal
distribution.” Note that
Q°'{r} = Var{r} — Covi{rg} - Var“ {g} - Covig,r}
(104.16)
Item 4 involves some statistical theory. There is a covariance
matrix, called the Cramer-Rao lower bound, such that the covari-
ance of any unbiased estimate of r will be greater than or equal to
the Cramer-Rao
lower bound."
In the case
of normal
ran-
dom variables, one can show that Var{r|g} equals the Cramer-Rao
lower bound, and thus it is the minimum-variance unbiased
estimate without adding the restriction that the estimate must be
linear.
Technical Treatment of Examples
We have now proved the basic forecasting formula and discussed
some further technical results. The remainder of the appendix will
discuss some specific examples from the main text concerning mul-
tiple forecasts for an asset.
Let’s consider the case of one asset with K forecasts:
g = [91,...,
xl
(10A.17)
"See Johnson and Kotz (1972), pp. 40-41.
"See Rao (1973) or Searle (1971).
~
Forecasting Basics
291
Std{g,}
0
and Var{g} =
a
(10A.18)
0
Std {gx}
Std{gi}
0
"Ps °
oe
0
*
Std{gx}
Now the covariance matrix between the return and these K signals
will involve K information coefficients:
Covirg} = w- [IC,... IC]:
i
(10A.19)
0
~
Stdi{gxs
We can now substitute Eqs. (10A.18) and (10A.19) into the basic
forecasting formula [Eq. (10.2)], to find
= Covirg} - Var-'{g} - (g — Efg})
(10A.20)
1
Std{gi}
”
ai PtSi
Eee Cle
pe:
op
;
(ae se
— Elgx)
2
saizeltce
1
Using our definition of scores, z, we can simplify this to
Zy
b =o
[IC,...ICkl* p,*-|
;
(10A.21)
ZK
=o. 1C' «9,9
z
where
eee
ies E{g)}
(10A.22)
1
Std{g}}
Furthermore, we can use Eq. (10A.21) to calculate the variance
292
Information Processing
of the combined signal, its covariance with the return, and hence
its combined information coefficient:
ICeombined = VICT - pz’ - IC
(10A.23)
Equations (10A.21) and (10A.23) are the general results. If
K = 1, then p, = 1, and these reduce to the standard volatility - IC -
score. If K = 2, then
1
pp
Fa
10A.24
Ps
Pr
1 |
(
)
.
1
a
un
Lie
Se
eee
12
Ps
(;
a | be 1 |
Oe?
ands
eae (Pe Ca) nto (e zal | an
1 a P12
1 5
P12
(10A.26)
which is basically Eq. (10.20) in the main text. We can similarly
show that Eq. (10A.23) reduces to Eq. (10.23) when K = 2.
If K = 3, we need to invert:
1
pp
ps
P, 1
(270)
1
P23
(10A.27)
Pn
p3
1
For any number of forecasts, the key is to invert the matrix p,. Note
that for any number of forecasts, Eq. (10A.21) always leads to
refined forecasts of the form
f
=o: SIC -z
(10A.28)
j
The refined forecast is always a linear combination of the scores.
The goal of this methodology is simply to determine the weights
(the adjusted information coefficients) in that linear combination.
Forecasting Basics
293
Exercise
1. Using Eq. (10A.21), what is the variance of the combined
forecast? What is its covariance with the return?
Remember that the combined forecast is simply a linear
combination of signals. We know the volatilities and
correlations of all the signals, and we know the
correlation of each signal with the return.
Verify Eq. (10A.23) for the IC of the combined
forecast. Demonstrate that when K = 2, it reduces to Eq.
(10.27) in the main text of the chapter.
‘
”
t
x
>
.
7
:
;
-
a,
a
‘4
¢
~
’
"
j
‘
}
“
j
’
«
—
A
i
A’
}
a
e
7
4
‘
3
“ms
“
a
Dy
Vid
heer
;
ei ae
sim,
+
Os
Pn
ay
iW
n
|
;
eh
ci
VE hee PUA
L Ber ei,
