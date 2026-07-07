# Chapter 13: The Information Horizon

- **book_name**: Active Portfolio Management
- **main_source**: pdf
- **cross_check_source**: none
- **pdf_role**: main_text_source
- **split_scope**: pages 369-398

---

CHAPTER
13
The Information
Horizon
INTRODUCTION
There is a time dimension to information. Information arrives at
different rates and is valuable over longer or shorter periods. For
most signals, the arrival rate is fixed. The shelf life (or information
horizon) is the main focus of interest. Is this a fast signal that fades
in 3 or 4 days, or is it a slow signal that retains its value over the
next year? The latest is not necessarily the greatest. In some cases,
a mix of old and new information is more valuable than just the
latest information.
Chapters 10 and 11 developed a methodology for processing
information and described how to optimally combine sources of
information. Chapter 12 presented an approach to analyzing the in-
formation content of signals. Chapter 13 will rely on both methodol-
ogies to tackle the special topic of the information horizon.
We will begin by applying information analysis at the “macro”
level: looking at returns to multiasset strategies. These may be
based on one or several sources of information, possibly but not
necessarily optimally combined. The goal is to determine the infor-
mation horizon, and whether the strategy is effectively using the
information in a temporal sense, i.e., whether any time average or
time difference of the information could improve performance. This
analysis has the advantage of requiring only the returns, not a
detailed knowledge of the inner workings of the strategy.
At the “micro” level, we will apply the methodology of Chap.
10 to the special case of optimal mixing of old and new signals.
347
348
Information Processing
The in-depth analysis of simple cases provides insight into the
phenomena we observe in more complicated and realistic cases.
These micro results echo the macro results.
Insights in this chapter include the following:
® The information horizon should be defined as the half-
life of the information’s forecasting ability.
# A strategy’s horizon is an intrinsic property. Time
averages or time differences can change performance, but
they will not change the horizon.
= Lagged signals or scores and past returns can improve
investment performance.
MACROANALYSIS OF THE
INFORMATION HORIZON
A natural definition of the information horizon, or shelf life, of a
strategy is the decay rate of the information ratio. What does it
cost us if a procrastinating investment committee forces a 1-month
delay in implementing the recommendations? We use the May 1
portfolio in June, the June 1 portfolio in July, and so forth. What
if there is a 2-month delay? Or a 6-month delay? In general, delays
will lead to a reduction in the strategy’s potential as measured by
its information ratio. A reasonable measure of the decay rate is the
half-life, the time it takes for the information ratio to drop to one-
half of its value when implemented with immediacy. In practice,
this means that we approximate the decay in the information ratio
as an exponential where a certain fraction of the information is lost
in each period.
The half-life is a remarkably robust characteristic of the strat-
egy. Attempts to improve the signal using its temporal dimensions
may improve performance, but they will have little or no effect on
the strategy’s half-life!
In Fig. 13.1, we see a gradual decay in the strategy’s realized
information ratio as we delay implementation for more and more
months. The half-life is 1.2 years.
The ability to add value is proportional to the square of the
information ratio. Thus the half-life for adding value is one-half
that of the information ratio. In the case illustrated in Fig. 13.1, we
The Information Horizon
349
Actual
0.60 +
- -
- Exponential Decay
0.00 +
ae
7
—-
-
+
+ pt
Ht
0
2
4
6
8
10
12
14
16
18
20
22
24
Months Lagged
Figure 13.1
have a half-life of 0.6 year for value added as opposed to 1.2 years
for the information ratio. This is a long-horizon strategy. We can
delay implementation of the recommended trades for more than
6 months and still realize 50 percent of the value added.
Figure 13.2 shows a strategy with a very short half-life.
The interplay of information and time is as subtle as the inter-
play of food and time. “Fresh is best” is a good rule but not univer-
sally accurate: Vegetables and baked goods are best when fresh,
fruit needs to ripen; wine and cheese improve with age, and sherry
is best as a blend of several vintages. Is the information sherry,
vegetables, or wine?
We can see if there is any value in the old information with
a thought experiment. Suppose there are two investment managers,
Manager Now and Manager Later. Manager Now employs an excel-
lent strategy, with an information ratio of 1.5. Manager Later’s
research consists of sifting through Manager Now’s trash to find
a listing of last month’s portfolio. Thus Manager Later follows the
same strategy as Manager Now, but with the portfolios 1 month
behind. Manager Later has an information ratio of 1.20. Both man-
agers have an active risk level of 4 percent.
Should we hire Manager Now, Manager Later, or a mix of
Now and Later? This decision hinges on the correlation of the active
350
Information Processing
ees
-
=
=
Exponential Decay
Actual
Information
Ratio
0
1
2
3
4
3]
6
y
8
)
Days Lagged
Figure 13.2
returns. If the correlation between Manager Now’s and Manager
Later’s active returns is less than 0.80 = 1.2/1.5, the decay rate of
the information ratio, then we can add value by hiring both Now
and Later. If the correlation is more than 0.80, we want to hedge
Manager Now’s performance by going short manager Later. Figure
13.3 shows the mix of Now and Later that we would want as
a function of the correlation between their active returns. At a
correlation of 0.7 between the active returns of Managers Now and
Later, the best mix is 18.5 percent to Manager Later and 81.5 percent
to Manager Now. If we presume a correlation of 0.85 in the active
returns of Managers Now and Later, then the optimal mix is a 118.5
percent long position with Manager Now offset by an 18.5 percent
short position with Manager Later.
We will show in the technical appendix that given a decay
rate of y and a correlation of p, the optimal weight on Now is
eee, are
WNow
y as 1
(13.1)
where
r= Le
;
(13.2)
The Information Horizon
351
40%
20%
-40 %
Percent
Allocated
teLATER
S
-60 %
Correlation of LATER’s active return with NOW’s active return
Figure 13.3
Figure 13.4 shows the change in the overall information ratio
that results from combining Managers Now and Later. We see that
there is no gain if the active return correlation is 0.8 and that there
are modest gains if the active return correlation strays above or
below that key level. The algebraic result here is
(oka a) ey Sa lox)
Miya) aa
oe ey) ilies aip
(13.3)
TR* = IRnow °
We will show more generally in the technical appendix that
the optimal combination of past portfolios mixes them so that the
correlation between the time t and the time t — 1 portfolios equals
the decay rate of the information ratio. For example, if the |-period
lagged information ratio is IR, = y' - IR and the portfolios at
each time ¢ are denoted h(t), h(t — 1),..., h(t — J),..., then the
combination with the best information ratio will be
NOH > yihe—)) — pah(t
1 —1)]
(13.4)
1=0
=([h@— p'hG— ll bys h*G—1)
352
Information Processing
1.60
1.55
Combined
Information
Ratio
1.50
:
0.50
0.55
0.60
0.65
0.70
0.75
0.80
0.85
0.90
Correlation of LATER’s active return with NOW’s active return
Figure 13.4
The correlation of active returns for the holdings h*(f) and h*(t — 1)
will be y. Note that h* is a weighted average of innovations, with
h(t — 1) — p- h(t — 1 — 1) capturing the new information in h(¢ — 1).’
This application of information analysis can quickly help a
manager determine if she or he is leaving any information on the
table, since a real manager can easily combine managers Now
and Later merely by combining the most recently recommended
portfolio with the portfolio recommended in the previous period.
For example, if the active return correlation is 0.5, then a mix of
33 percent of the lagged portfolio and 67 percent of the current
portfolio would produce an information ratio of 1.59. Combining
the portfolios is combining the outputs of the investment manage-
ment process. If there is a process where it is possible to link in)puts
with outputs, then we could also proceed by mixing the lagged
inputs and the current inputs in the same 33 percent and 67 per-
cent ratios.
‘If you regress 6(t — 1) on 6(t — | — 1), the coefficient on 6(f — 1 — 1) should be p, since
w(t — 1) = w(t — 1 — 1). Hence Eq. (13.4) effectively represents the residuals from
such a regression.
The Information Horizon
353
This optimal mix of Now and Later will improve performance
although it will not change the horizon. If we make an optimal mixture
of the old portfolios, the information ratio will increase, but the
horizon (half-life) of the resulting strategy will be exactly the same
as the horizon of the original strategy.
MICROANALYSIS OF THE
INFORMATION HORIZON
We will now apply our information processing methodology to
analyzing the information horizon at the micro level. We will focus
on the case of one asset, or, more precisely, one time series.” This
asset has return r(0,At) over a period between time 0 and time At.
For convenience, we assume that the expected return is 0. The
volatility of the return is o times the square root of At. We assume,
in general, that the asset returns are uncorrelated.
Information arrives periodically, in bundles that we'll call
scores, at time intervals of length Af—perhaps an hour, a day, a
week, a month, a quarter, or a year. These scores have mean 0 and
standard deviation 1, as described in Chap. 10.
The special information contained in the scores may allow us
to predict the return r(0,At). This prediction, or alpha, depends on
the arrival rate and shelf life of that information.
In the simplest case, “just-in-time” signals, the signal is of value
in forecasting return during the interval until the next one arrives,
but it is of no value in forecasting the return in subsequent periods.
For example, a signal that arrives on April 30 helps in forecasting the
May return but is of no use for June, July, etc. The next signal, which
arrives May 31, helps with the June return.
Let IC(At) be the correlation of the score with the return over
the period {0,At}. Given a score s(0), the standardized signal at time
0, the conditional expectation of r(0,At) is
a(At) = (o - V/Ab) - IC(At) - s(0)
(13.5)
’The point is that our results apply to a single asset, or a factor return, or a portfolio
long stocks and short bonds.
354
Information Processing
The information coefficient IC(At) is a measure of forecast accuracy
over the period. The first goal is to determine the value of the
information. Here we will use the information ratio. We can use
the fundamental law of active management to determine the infor-
mation ratio as a function of the forecast interval:
IR? = [IC(ADE- (4)
(13.6)
where we measure the breadth BR as simply the inverse of the
period, ie., 1/At. For example, a signal that arrives once per month
has a breadth of 12. We can see immediately that there is a trade-
off between the arrival rate, captured by At, and the accuracy,
captured by IC(Af?).
Two-Period Shelf Life
In the simplest case described above, we had “just-in-time” infor-
mation. The interarrival time At matched the shelf life At. Now
we'll consider cases where the interarrival time is shorter than the
shelf life.* In particular, we receive scores each period, and a score’s
shelf life is two periods long. The April 30 score predicts the re-
turns for May and June. The May 31 score predicts the returns for
June and July. We can measure the IC of the score on a period-by-
period basis. The term IC; measures the correlation between the
score and the first period’s return, and the term IC, measures the
correlation between the score and the second period’s return. The
information coefficient IC,,, is the correlation between the score
and the two-period return. The relation between these information
coefficients is
2
IC,
+ IC
Cee Een
(13.7)
‘It is possible, although less interesting, to have the interarrival time exceed the shelf life.
An example is earnings surprise for international companies; the information
arrives once a year, and its value has generally expired long before the next year’s
earnings announcement.
The Information Horizon
355
For example, a correlation of IC; = 0.15 for the first period’s return
and IC, = 0.075 for the second period’s return would imply a
correlation of IC,., = (0.15 + 0.075)/1/2 = 0.159 for the two peri-
ods. We are blessed with a longer shelf life. It remains to see how
we handle this blessing.
We want to make a one-period forecast based on the most
recent score, s(0), and the previous score, s(—At). In the monthly
example, we combine the April 30 score and the May 31 score to
produce a forecast for June. The critical variable in producing a
best forecast will be the correlation p between s(0) and s(—At).
In Chap. 10, we derived how to optimally combine two sepa-
rate signals. That result applies here as well, with the second signal
being simply the lag of the first signal:
a(At) = o - V/At - {IC¥ - s(0) + ICF - s(—Ad)}
(13.8)
The modified information coefficients IC? and IC} correct for the
correlation between the signals:
IC, pa Dae IC,
ere
(13.9)
(pe a
(13.10)
The IC of the combined signal is
2
De
r
4
.
Figure 13.5 shows how the modified information coefficients
change as the correlation between the signals varies, assuming
IC, = 0.15 and IC, = 0.075.
The combined forecast dominates using either the first or the
second score in isolation. Figure 13.6 demonstrates this for our
example.
356
Information Processing
ee eee
effective IC for score{0}
-
-
- effective IC for score{-1}
Information
Coefficient
Signal Correlation
Figure 13.5
The lagged score, s(— At), can help improve the forecast in one
of two ways:
= Diversification, as a second predictor of the return r(0,At)
= Hedging, as a way of reducing the noise in s(0)
The scores are part truth and part noise. The truth portion is per-
fectly correlated with future return. The noise component is uncor-
related with future return. By adding a fraction of the previous
score to the current score, we can reinforce the known facts and
diversify the noise. This is a good idea if IC, > p - IC, i.e., when
there is a relatively strong remaining signal and relatively low
correlation. The alternative is to subtract a fraction of the second
score from the first. This loses some signal, but if the scores are
strongly correlated, it will hedge the noise. Hedging is the tnost
beneficial path to follow if IC, < p - IC;,i-e., when there is a relatively
weak signal and strong correlation. In the intermediate case, when
IC, = p - IC, then ICf = IC, and IC} = 0. In effect, we ignore the
previous score.* We can see this critical point in Figs. 13.5 and 13.6
‘There are, of course, cases where IC, > IC, (as opposed to just IC, > p - IC,). The
correlation with period 2 is actually stronger than the correlation with period 1. In
this case, one would be advised to look into autocorrelation of the return.
The Information Horizon
357
0.18
0.17
Information
Coefficient
S — a
0.15
-0.10
0.00
0.10
0.20
0.30
040
90.50
0.60
0.70
0.80
Signal Correlation
Figure 13.6
where the correlation reaches 0.5, exactly the ratio of the informa-
tion coefficients.
This result for optimally combining new and old information
closely matches our results from the macroanalysis. In fact, Figs.
13.5 and 13.6 from the microanalysis resemble Figs. 13.3 and 13.4
from the macroanalysis. This is quite reassuring. We will now see,
however, that we can drill considerably deeper in microanalysis.
HAS THE ALPHA BEEN REALIZED?
Prior to the 1967 Arab-Israeli war, then private citizen Richard
Nixon predicted that
1. There would not be a war.
2. If a war started, it would be a long war.
The war started within days, making Mr. Nixon’s first prediction
no longer operative. When the war was over a week later, the second
prediction went nonoperative. You don’t receive such dramatic and
immediate feedback when you’re predicting asset returns.
Suppose that we have, as above, alphas arriving each month
that are useful in predicting returns over the next 2 months. Suppose
358
Information Processing
further that our signal produces an alpha prediction of 2 percent
at the beginning of March, and make a third supposition that the
realized alpha in March is 2 percent, as predicted. It would seem
that the prediction has come true and we can ignore the old informa-
tion; all the juice has been squeezed out of it. Not so! Many people
find it hard to believe, but they may be right for the wrong reasons.”
That 2 percent return may have been incidental.
To deal with this possibility, we can use the previous period’s
return, r(— At,0) as another possible variable in the prediction of next
period’s return, r(0,At). We turn r(—At,0) into a score by dividing it
by its standard deviation; the score is r(—At,0)/(o - \/At).
We now have three predictors of r(0,At): s(0), s(—At), and
r(—At,0)/(o - \/At). When there is no serial correlation in the returns
and no correlation between past returns and current scores, the
rule for adapting to the observed return changes the previous score
and is thus called “settling old scores.” The settled score’ is
IC,
r(—At,0)
ao: VAt
The “correction” in the previous score, the term IC, - r(—At,0)/
(o - \/Ab), is the part of the score that has been used up. The greater
the ability to predict, the more we discount from the score.
In general, the settling score effect is small, since the impact
depends on the product of IC, and IC}. However, there can be a
considerable effect in extreme situations. For example, consider an
asset allocation model with a stock minus bond score of —2.16 on
October 1, 1987. The October return was a 6.5 standard deviation
event; i.e., r(—At,0)/(o - \/At) = —6.5. With a first period IC, =
0.15, the corrected score is s*(—1) = —1.18. This is an extraordinary
change reflecting the extraordinary event. In a typical month with,
say, a 1 standard deviation event in the return, we would make a
small change of 0.15 to the score.
$*(—At) =s(— Ab) —
(13.12)
°On the other hand, people are always willing to believe that if they were wrong, it was
for the right reasons.
‘Technically, Eq. (13.12) does not describe a score, because it has a standard deviation not
equal to 1. Dividing by 1 — IC} will correct this problem. However, we prefer to
use Kq. (13.12) in the form given.
The Information Horizon
359
In this analysis, we have ignored some complicating features.
For example, if returns are autocorrelated, past returns play a dou-
ble role by settling old scores, as described above, and bringing
information about next period’s return. It also often happens that
past returns have an impact on future scores. The causality flows
from return to score, as well as from score to return. With a momen-
tum signal, higher past returns generally mean higher future scores.
With a value signal, large past returns tend to imply lower future
scores.’ The microanalysis methodology can handle both of these
situations. The technical appendix treats one special case, using the
binary model.
GRADUAL DECLINE IN THE VALUE
OF THE INFORMATION
The one- and two-period models described above are easy to ana-
lyze but lack realism. A more sensible information model is one
of gradual decline in forecasting power. The information coefficient
decays as we move more and more periods away from the arrival
of the information. A score available at time June 30 has a correlation
with July return of IC. The correlation with August return is IC - 6.
In general, the correlation with return in month n + 1 is IC - 8".
We can relate this continuous decay to the half-life:
1
= (5)
(13.13)
Art)
or
His Sh as
(13.14)
Figure 13.7 shows a gradual attrition of the information’s power.
In this case, monthly intervals, the half-life is one quarter; HL =
0.25, 8 = 0.7937. We can see the exponential decay in the monthly
7One way to eliminate this problem is to design a new score that is the residual of the
old scores regressed against the prior returns. This procedure extracts the
component explained by prior returns and isolates the component uncorrelated
with prior returns.
360
Information Processing
ee
a
ee
ee
Information
Coefficient
1
2
3
4
5
6
7
8
9
10
11
12
Delay in Months
Figure 13.7
information coefficient over time.® As the score and the return move
farther apart, the information coefficient decreases.
A different cut at this is to look at the correlation of the signal
with returns over longer and longer periods. Instead of lagging
the scores, we can lead the returns. We can examine the correlation
of a monthly score with the monthly return, 2-month return, quar-
terly return, annual return, etc.
What will influence the information coefficient for longer and
longer return horizons? On the positive side, the longer return
horizons should more completely reflect the signal’s information.
On the negative side, increasing volatility, o - \/t, accompanies the
longer time periods. We will show in the technical appendix that
the correlation of the returns with the signal over longer and longer
periods is
Hy
ics oi /At
a
la)
IC(0,t) = Corr{r(0,t),s(0)} = IC - (a
where the IC in Eq. (13.15) is the information coefficient over the
‘Measuring the IC each period ahead has the benefit of avoiding double counting by
using the dreaded “overlapping intervals.”
The Information Horizon
361
I
a
ee
0.150
0.125
0.100
0.075
0.050
Information
Coefficient
0.025
0.000
0.0
0.5
1.0
1.5
2.0
2.5
3.0
3.5
4.0
4.5
5.0
Horizon in Years
Figure 13.8
initial period of length Aft. Figure 13.8 illustrates this relationship.
The signal has its highest predictive power when the horizon is
about twice the half-life of the signal.’
As the signals arrive, we can use the most recent, or we can
attempt to combine new and old in order to get a more powerful
forecast. The ability to improve will still hinge on two parameters:
= The decay factor 6
® The correlation p between the adjacent scores
If 8 = p, then the most recent score has all the information that we
need. If 8 > p, we can diversify by using past scores to reinforce
the information. Finally, if 8 < p, we can use past signals to hedge
the noise in the most recent signal. This is a message we’ve seen
before, in the macroanalysis and in the two-period case.
To use the information in an optimal way, mix the past signals
so that the new mix has an autocorrelation equal to 8. The recipe is
s*(0) = >) 8"- {s(—m - At) — p+ s[—(m — 1) - At]} (13.16)
m=0
S(O) —p - star)
0s
(— AD
°The function (1 — e*)/\/x has a maximum value of 0.6382 at x = 1.257.
syuoy ul Avpag
s[eBusIs jsed |e JO XIU }Saq 9} SUISN OT
[BUSIS JUI901 JsOU 94} A[UO SUISN DO] wy
6 EL amnsry
00°0
soo
oro
JUIIIJIOD UOHeULIOJUT
sto
070
362
The Information Horizon
363
This is effectively the same result we saw in Eq. (13.4). This opti-
mally repackaged information will have the same half-life as the
original information. For example, in Fig. 13.9 we show the original
and repacked information coefficients. The half-life is one quarter,
and the correlation between signals is 0.5.
SUMMARY
The information horizon (half-life) is a critical characteristic of a
signal or strategy. The horizon can help us see if we are using
information efficiently in a temporal sense. Macroanalysis can fairly
easily tell you if your strategy is temporally efficient. Microanalysis
provides insight into how this works, and can handle many im-
portant cases. Past information—signals and returns—can help the
current forecast.
NOTES
Investment horizon is a term generally used in a strategic sense
for either the individual or the institutional investor. The horizon
metaphor is apt for an institutional investor, since an ongoing insti-
tution’s investment horizon will continually precede the institution
into the future. The long view is used to set a strategic asset alloca-
tion and investment policy.
In the individual investor’s case, the horizon metaphor is not
particularly appropriate; there is no receding horizon. We have
an uncertain, but finite, term until retirement and another, also
uncertain, interval until death. This is one of life’s cruel jokes.
Samuelson (1994) has more to say in this regard.
For another, more technical horizon topic, see Goetzmann and
Edwards (1994) and Ferguson and Simaan (1996). They tackle the
question of horizon as it relates to a single-period portfolio mean/
variance optimization. The questions are: How longa period should
we consider? and, Does it matter? This analysis hinges on the
interaction between the compounding nature of returns and the
additive nature of a buy and hold portfolio. It can get complicated,
and it does. Some of the difficulty goes away when you consider
multiperiod investing or continuous rebalancing. If you assume
lognormal returns, continuous rebalancing, and a power utility
364
Information Processing
function for cumulative return at the horizon, the portfolio selected
will be independent of the horizon. See Merton (1990), pp. 137-145.
PROBLEMS
1. Your research has identified a monthly signal with
IR = 1. You notice that delaying its implementation by
one quarter reduces the IR to 0.75. What is the signal’s
half-life? What is the half-life of the value added?
2. In further researching the signal in Problem 1, you
discover that the correlation of active returns to this
signal and this signal implemented 1 month late is 0.75.
What is the optimal combination of current and lagged
portfolios?
3. You forecast a = 2 percent for a stock with w = 25
percent, based on a signal with IC = 0.05. Suddenly the
stock moves, with 8 = 10 percent. How should you
adjust your alpha? Is it now positive or negative?
REFERENCES
Atkins, Allen B., and Edward A. Dyl. “Transactions Costs and Holding Periods
for Common Stocks.” Journal of Finance, vol. 52, no. 1, 1997, pp. 309-325.
Ferguson, Robert, and Yusif Simaan. “Portfolio Composition and the Investment
Horizon Revisited.” Journal of Portfolio Management, vol. 22, no. 4, 1996,
pp. 62-68.
Goetzmann, William N., and FE. R. Edwards. “Short Horizon Inputs and Long
Horizon Portfolio Choice.” Journal of Portfolio Management, vol. 20, no. 4,
1994, pp. 76-81.
Grinold, Richard C. “Alpha Is Volatility Times IC Times Score,” Journal of Portfolio
Management, vol. 20, no. 4, 1994, pp. 9-16.
. “The Information Horizon.” Journal of Portfolio Management, vol. 24, no.
1, 1997, pp. 57-67.
Merton, Robert C. Continuous Time Finance, (Cambridge, MA: Blackwell, 1990).
Samuelson, Paul A. “The Long Term Case for Equities.” Journal of Portfolio Manage-
ment, vol. 21, no. 1, 1994, pp. 15-24.
TECHNICAL APPENDIX
We will use this technical appendix to derive several results pre-
sented in the main text. We will show that mixtures of past strategies
The Information Horizon
365
cannot change the half-life of the strategy. We will analyze the
optimal mixture of past strategies. We will show how the correlation
of a signal with returns of varying horizons depends on that hori-
zon. Finally, we include an explicit optimal combination of current
and past signals and past returns, in the context of the binary model.
Mixtures of Past Strategies
Let’s start with some basic notation. We will need to explicitly keep
track of lagged information:
hp,QJ) = active portfolio lagged j periods
6(j) = return to the j-lag active portfolio”
IRG) = information ratio for the j-lag portfolio
We will further make the assumptions that
hpa(/) ~V- had) = >"
(13A.1)
hia(j) - V« hpa(k) = w? + p(|j — ki)
(13A.2)
The first assumption is not remarkable. It just says that any
old active position will have the same active risk as any other. Note
that this implies that any decay in the information ratio over time
must arise solely as a result of decay in the alpha:
IRG) = y - IR) = ou)
(13A.3)
The second assumption is stronger. It says that the covariance
between lagged positions depends only on the time interval be-
tween them. Note that this is weaker than saying that there is a
single parameter p such that p(|j — kl) = pl-4.
We define a mixture of past strategies using weights y(), j =
0,1,2,.... This mixture of past strategies will have an information
ratio IR*(0). But we can also lag this mixture strategy, giving rise
to anew sequence of lagged information ratios IR*(j),j = 0,1,2,....
We are assuming here that the portfolio beta is 1, and so active returns equal residual
returns.
366
Information Processing
Proposition
If the strategy information ratios decay exponentially [as in Eq.
(13A.3)], then any mixture strategy will exhibit information ratios
which also decay exponentially, at the same rate:
IR*(j) = y' - IR*(0)
(13A.4)
Proof The active holdings for the j-lag mixture strategy are
hej) = Sy) -hG +h
(13A.5)
k=0
with active returns
oj) = Si yh) 0G +h
(13A.6)
k=0
Our first step is to show that, while the risk of the mixture
strategy does not generally equal the risk of the underlying strategy,
the dependence on lag is the same. In fact, the risk of the mixture
strategy is independent of lag.
The risk of the lagged mixture strategy is
Var{6*(/)} = vay) y(k) - 0G + b|
(13A.7)
k=0
= SS yb) - CovioG + 6,4G + m)} - yim)
km
But our assumptions, Eqs. (13A.1) and (13A.2), guarantee that
Cov{0G + k),0G + m)} = Cov{0(k),6(m)}
(13A.8)
Hence
Var{0*(7)} = Var{0*(0)} = (w*)?
(13A.9)
So the decay in the information ratio for the mixture strategy
must depend entirely on the decay in the alpha for the mixture
strategy. We can now show that this decays at the same rate as the
alpha for as the underlying strategy.
The information ratio for the unlagged mixture strategy is
>) alk) - yl)
:
#0 Sith a
(13A.10)
W
IR*(0) =
The Information Horizon
367
But we can relate these alphas to information ratios:
> @ IR} - yb)
IR*(0) = aa ea
(13A.11)
The information ratio for the lagged mixture strategy is
' Si aG +b: yl)
yO
ie
ae ee
IR*()
*
a
(13A.12)
We can relate this too to the information ratios:
SY) o  IRG +H: yl)
IR*(j) = &*
(13A.13)
w*
Finally, we can simply calculate the ratio of lagged to unlagged
information ratios for the mixture strategy. Using Eqs. (13A.11) and
(13A.13), this becomes
SRG +
- yl
ae
ee
(13A.14)
IR*(0)
> IR(K) - y(k)
k=0
But using Eq. (13A.3), this becomes the desired result:
TRE
TR*(0)
ny
(13A.15)
While we will not explicitly demonstrate this, the correlation struc-
ture of lags of a mixture strategy retains the structure exhibited by
lags of the underlying strategy, namely, that the correlation depends
only on the separation between the two lags of the mixture strategy.
Optimal Strategy Mixtures
The main text presented two sets of results concerning optimal
strategy mixtures. First, it presented the optimal mix of
Now and
Later, the current and lagged portfolios. It then stated a more
general result, that optimal strategies should exhibit a correlation
structure matched to the decay of the information. We will calcu-
368
Information Processing
late both results here. We begin with the combination of Now
and Later.
Our goal is to combine current and past portfolios so as
to maximize the resulting information ratio. We characterize the
current portfolio with statistics anow @, and IRyow and the lagged
portfolio with statistics Oye, w, and IRyater Note that the current
and lagged portfolios exhibit the same risk. We will also assume
a correlation p between current and lagged active returns, and a
decay factor y between current and lagged information ratios.
Using Wyow to express the weight on the current portfolio, the
combined alpha is
Qp = Wnow
* &Now He (1 a Wnow)
* QLater
(13A.16)
OD
TRnow ¥ [Wow + (1 ~ Wow)
i y]
Here we have explicitly used the decay factor to express the infor-
mation ratio of the lagged portfolio. We can express the risk of the
combined portfolio as
@p = Wye
OP 45
We)
O che Wr
(= We) OD
a wo” [Wriow 45 (1 4 Wnow)” qa
oc) Wnow * (1 al Wnow) : p]
(13A.17)
We can put this all together and express the combined information
ratio as
2
(
IRp
=
[Wrow a0 (1 = Wnow) % yi
TRnow
Wow ta (1 = WNow)” Ma Wnow
* (1 =o Wnow) > (9)
(13A.18)
To maximize the combined information ratio, we need to take the
derivative of Eq. (13A.18) with respect to wyow, and set it equal to
zero. The procedure is algebraically messy, but straightforward.
The result is
ests apie
where
— =
(13A.20)
5
:
as stated in the main text. Furthermore, we can take Kq. (13A.19)
The Information Horizon
369
and substitute it back into Eq. (13A.18) to determine the maximum
information ratio achieved. The result is
Cie)
any al ey)
V Ary) re oe)? ay SE ) 8) = x)
(13A.21)
IR* = IRnow *
General Optimality Condition
We will now treat the general optimality condition quoted in the
main text. We will use the notation introduced at the beginning of
this appendix. In this general case, we want to minimize the vari-
ance of the mixture strategy, subject to the constraint that the alpha
remains constant (i.e., equal to the alpha of the current underlying
strategy). Mathematically,
Min} Vary >)
y(j) * acph|
(13A.22)
j=0
subject to the constraint
>) ¥@ - @ + IRG) = a0) = @ - IR(O)
(13A.23)
j=0
Note that the problem is feasible, since the case {y(0) = 1; y() =
0, i ~ 0} satisfies the constraint. Using a Lagrange multiplier, we
can rewrite the minimization problem as
Min{ Vary >)
y(j) - ap} +c:
0
The first-order conditions are
S. y@ + IRG) — IRO) !
(13A.24)
j=0
2: Cov a0), S yh): aco} +c-IRG)=0
(13A.25)
k=0
plus the constraint. Note that Eq. (13A.25) represents a set of equa-
tions, one for each lag j. Now, to solve for the Lagrange multiplier
370
Information Processing
c, we can multiply the equation for each lag j by the weight y(),
and sum them. The covariance term becomes
S20: Cov a0), > yo: aco}
(13A.26)
j=0
k=0
ba
=2: vay) y(k) - ao}
= 2: (w*)
k=0
The information ratio term becomes
Sc: yQ) - IRG) = c - IRO)
(13A.27)
io
Putting this together, we find that the term c is
eS x (w*)?
CR Oiee
(13A.28)
and the covariance relationship (first-order condition) becomes
*\2
,
‘
Covlo(),0%0))
= SD
(13.29)
Here we have used the notation 6* for the active return to the
mixture strategy.
In this scheme, the mixture strategy has a higher information
ratio than the underlying strategy specifically because it has lower
risk. We have constrained the alpha to remain constant. Hence the
ratio of IR(0) to IR*(0) is just the ratio of w* to w. So we can rewrite
Eq. (13A.29) as
Covla(),0%(0)) = 2
(134.30)
This is close to the answer we are seeking. We now have the covari-
ance structure between the underlying strategy and the optimal
mixed strategy. We want the covariance structure between the opti-
mal strategy and its lags. We can calculate this easily. The lagged
optimal strategy active return is
ee
e*(k) = SY y@) - OG +b)
Tone
@B43))
ies
The Information Horizon
371
We can calculate the covariance of this with 6*(0). Using Eq. (13A.30)
and the definition of IR*(k), this becomes
*)\2
,
+
Cov{o*(k),6#(0)} = a
(13A.32)
This directly reduces to the result we want:
IR*(k)
TR*(0)
Corr{0*(k),6*(0)} =
(13A.33)
that the correlation between lagged optimal mixes falls off as the
information ratio falls off between the lagged optimal mixes. In
particular, focusing on just one lag, the information ratio decays
by 5, and we have devised the optimal mix so that the correlation
between the current and lagged optimal mix is also 8, according
to Eq. (13A.33).
The result in Eq. (13A.33) plus the previous result [Eq. (13A.9)]
that all lags of mixture strategies maintain the same risk allows us
to directly verify Eq. (13.4). The optimal current mixture holdings
are just y times the lagged mixture holdings, plus the innovation
in the current strategy. We can verify that the innovation term is
uncorrelated with the lagged mixture strategy.
Return/Signal Correlations as a Function
of Horizon
The main text states results concerning the correlation of a score
with returns of increasing horizons, in the case where the informa-
tion decays by a factor of 8 each period. We derive the result here.
We measure the return horizon as variable t, the sum of several
periods of length Af. The correlation of our score with returns over
periods of length At out in the future decays by a factor of 8 each pe-
riod. The goal here is to sum up these effects for a return over a
period from 0 to t. We need to calculate
_ Covi{r(0,t),s(0)}
Corr{r(0,t),s(0)} = DEctdcon 4
(13A.34)
372
Information Processing
Remember that the standard deviation of the score is 1. We can
expand r(0,t) into a sum of returns over periods At:
t/At
con rlG — 1): At: sas}
=
(13A.35)
t/At
Std
1G
a) SAR sah
j=l
Now we can use the decay relationship and an assumed orthogonal-
ity in returns over different periods to simplify this to
OTN,
AG
Oe haya
O aie
Corr{r(0,t),s(0)} = TC OAL Gabi BO sygtcacks 2
ceed
w: Vt
Corr{r(0,t),s(0)} =
(13A.36)
We can sum this finite power series to find
=
Ns
Corr{r(0,t),s(0)} = IC - 4" pee
(13A.37)
6
the result quoted in the main text.
Optimal Mixing of Current and Past Signal
and Past Return
Finally, we include an explicit analysis combining current and past
signals and the past return, using the binary model.
Suppose we forecast the residual return each month, and that
forecast contains information about the residual returns in the next
2 months. Assume that the expected residual return is 0 and the
monthly volatility is 6 percent (annual 20.78 percent). In period t,
we have
36
r(t) = >* 6)
(13A.38)
jel
The forecasts have zero mean and a 4 percent standard deviation:
o(t) = 0,(t) + O,(t) + Ox) + Ox + 1) + 0,(¢ +1)
~
(13.39)
+ qf) Bene Pt) + at = De
ne)
The Information Horizon
373
The forecast g(t), available at the beginning of period t, has four com-
ponents:
= Three signals about return in the coming period:
{0;(t),02(t),83(#)}
# Two signals about return in the following period:
{0;(f + 1), O,(f + 1)}
= Seven elements of new noise: {y;(f),n2(b),...., Nb}
B Four echoes. of old noise: (n = )),.7.¢— 1), ~.:.
mat — 1) }
Of course, we observe only the sum of the elements in these
four groups.
In forecasting the residual return in period t, both the current
forecast and the previous forecast will be of use. The covariance
of the most recent forecast with the return is 3, the covariance of
the previous forecast with the return is 2, and the covariance be-
tween g(t) and g(t — 1) is 5, since they share one element of signal
and four elements of noise. The basic forecasting rule therefore
leads to
E{r(t) |
g(t), g(t — 1)} = (0.1645) - g(t) + (0.0736) * g(t — 1) (13A.40)
The IC of this refined forecast with the return is 0.1334. Note that
the IC of g(t) alone is 0.125 and the IC of g(t — 1) is 0.0833.
We can actually do slightly better by adding a source of infor-
mation that we have available: last period’s residual return r(t — 1).
The covariance of g(t —
1) and r(t —
1) is 3. In this model,
r(t — 1) is not correlated with 9(t) or r(t), so r(t — 1) itself is useless
as a predictor of r(t). However, r(t — 1) combined with g(t) and
g(t — 1) is (oh, so slightly) useful. Working through the basic fore-
casting formula again, we now find
E{r(é) | g(t), g(t — 1),r(t — 1}
(13A.41)
= (0.1641)
« g(t) + (0.0749) - g(t — 1) — (0.0062) - r(t — 1)
and the IC of the refined forecast is now 0.1335.
When the forecast horizon is shorter than the information
horizon, treat the older forecasts like forecasts from a different
source. Past realized returns may also improve the forecast.
374
Information Processing
Exercises
1. Show that any mixture strategy obeys the same
correlation structure we have assumed for the
underlying strategies. Namely, show that
Corr{6*(j),6*(K)} = p*(|j — kl)
2. Show that the optimal combination of Now and Later
leads to a mixture strategy with the correlation of the
mixture and its first lag equal to the decay factor vy.
PART
FOUR
Implementation
j
V4
ta
