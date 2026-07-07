# Chapter 19: Benchmark Timing

- **book_name**: Active Portfolio Management
- **main_source**: pdf
- **cross_check_source**: none
- **pdf_role**: main_text_source
- **split_scope**: pages 563-580

---

CHAPTER
19
Benchmark Timing
INTRODUCTION
In Chap. 4 we separated active management into benchmark timing
and stock selection and postponed consideration of benchmark
timing until a later chapter. We can postpone it no longer. In this
chapter we will explore benchmark timing as another avenue for
adding value.
The main conclusions of this chapter are as follows:
® Successful benchmark timing is hard. The potential to
add value is small, although it rises with the number of
independent bets per year.
= Exceptional or unanticipated benchmark return is the key
to the benchmark timing problem. Forecasts of
exceptional benchmark return lead to active beta
positions.
= We can generate active betas using futures or stocks with
betas different from 1. There is a cost—measured in
unavoidable residual risk and transactions
costs—associated with relying on stocks for benchmark
timing.
= Performance measurement schemes exist to evaluate
benchmark timing skill.
We'll start with the definitions.
DEFINING BENCHMARK TIMING
As discussed in Chap. 4, benchmark timing is an active manage-
ment decision to vary the managed portfolio’s beta with respect
541
542
Implementation
to the benchmark. If we believe that the benchmark will do better
than usual, then beta is increased. If we believe the benchmark will
do worse than usual, then beta should be decreased. Notice the
relative nature of our expectations—better than usual and worse
than usual. We will need some feeling for what we should expect
in the usual circumstances.
In its purest sense, we should think of benchmark timing as
choosing the correct mixture of the benchmark portfolio and cash.
This is a one-dimensional problem, and variations along that di-
mension should not cause any active residual bets in the portfolio;
i.e., all the active risk will come from the active beta. This type of
benchmark timing is akin to buying or selling futures contracts’
on the benchmark.
Benchmark timing is not asset allocation. As we saw in Chap.
18, asset allocation focuses on aggregate asset classes rather than
specific individual stocks, bonds, etc. In the simplest case, the aggre-
gates may be domestic equity, domestic bonds and cash. In more
complicated cases, the asset allocation may include several kinds
of equity and bonds as well as international equities and bonds,
real property, and precious metals. International managers betting
on several country indices are engaged in global asset allocation,
not benchmark timing. The motivation for asset allocation is to
simplify an extremely complicated problem.
While tactical asset allocation involves 5 to 20 assets, bench-
mark timing involves only 1. This makes adding value through
benchmark timing very difficult, as we can see from the fundamen-
tal law of active management. Remember that the information ratio
for benchmark timing arises from a combination of forecasting skill,
the benchmark timing information coefficient ICg;, and breadth BR,
the number of independent bets per year:
*
IRsr = [Cpr -
V BR
(191)
An independent benchmark timing forecast every quarter leads to
a breadth of only 4. Then, according to Eq. (19.1), to generate a
'A forward contract is equivalent te being long the benchmark and short cash, i.e.,
borrowing to buy the benchmark. A futures contract is very similar to a forward
contract.
Benchmark Timing
543
benchmark timing information ratio of 0.5 requires an information
coefficient of 0.25—extremely high! The fundamental law of active
management captures exactly why most institutional managers
focus on stock selection.
Stock selection strategies can diversify bets cross-sectionally
across many stocks. Benchmark timing strategies can diversify only
serially, through frequent bets per year. The fundamental law quan-
tifies this. Significant benchmark timing value added can arise only
with multiple bets per year. To keep this point clear, this chapter
will monitor the forecast frequency: first once per year and later
multiple times per year.
FUTURES VERSUS STOCKS
Benchmark timing is choosing an active beta. We can implement
benchmark timing with futures. We can also implement an active
beta without modifying the cash/benchmark mix. For example, if
we think the benchmark will be exceptionally strong this month,
then we might overemphasize the higher-beta stocks in our portfo-
lio. However, this has three drawbacks. First, we have to take on
residual risk as a result of emphasizing one group of stocks over
another. Second, we must have faith that we have identified the
betas of the stocks correctly. Even the best forecasts of beta are
subject to error. There is no error in the pure cash/benchmark trade-
off. The beta of cash is exactly 0, and the beta of the benchmark is
exactly 1. Third, the transactions costs involved in trading many
individual securities are generally much greater than for a forward
or futures contract.
We can push the residual risk problem a bit further with the
following analysis. Let’s build the minimum-risk, fully invested
portfolio with beta constrained to be Bp. Given the beta constraint,
the portfolio which minimizes total risk will also minimize residual
risk. As shown in the technical appendix, the optimal portfolio is
a weighted combination of the benchmark and portfolio C. Its
residual variance—the lowest possible residual variance for a fully
invested portfolio with specified active beta Bp, = Bp — 1—is
wp = (Bra * Op)” ° (;
ard
(19.2)
544
Implementation
Assuming a benchmark risk of 18 percent and a portfolio C risk
of 12 percent, and remembering that the beta of portfolio C is:
an active beta of 0.1 leads to a residual risk of at least 1.6 percent.
With a moderate level of residual risk aversion (Ag = 0.1), this
corresponds to a penalty of about 0.25 percent.
This analysis of the benefits of using futures rather than stocks
to implement benchmark timing strategies has clear implications
for situations where the benchmark has no closely associated fu-
tures contract. In that case, the potential for adding value through
benchmark timing is very small.
VALUE ADDED
In Chap. 4 we derived an expression for the value added by bench-
mark timing. The key ingredients in this formula are
Bp, = the portfolio’s active beta with respect to the
benchmark. This is the decision variable.
Afs = the forecast of exceptional benchmark return. This is
the departure, positive or negative, from the usual
level of benchmark return. If j, is the usual annual
expected excess return on the benchmark and fs is
our refined forecast of the expected excess return on
the benchmark over the next year, then Af = fg — wp
is the exceptional benchmark return in the next
year.
og = the volatility of the benchmark portfolio.
\pgr = a measure of aversion to the risk of benchmark
timing.
We will start with the simple case in which we only make one
benchmark timing decision per year. In Chap. 4 we determined
that the value added by benchmark timing is
~
VA{BpalAfs} = Bra: Afs — Apr * B34 * 03
(19.4)
Benchmark Timing
545
TABLE
19.1
Re
ee oe
es ee
Active Beta
Aversion to Timing Risk 5;
Exceptional Forecast Af,
High, 0.14
Medium 0.09
Low, 0.06
4.00%
0.05
0.08
0.12
2.00%
0.02
0.04
0.06
0.00%
0.00
0.00
0.00
—2.00%
—0.02
—0.04
—0.06
—4.00%
—0.05
—0.08
One
The optimal level of active beta, B,, is determined by setting the
derivative of Eq. (19.4) with respect to beta equal to zero. We find
pines
Settee
(19.5)
PA = 2 - hen: OF
Table 19.1 shows how By, will vary with changes in the exceptional
forecast Af; and the aversion to benchmark timing risk Agr. Table
19.1 assumes a 17 percent annual volatility for the benchmark.
The value added at the optimal beta Bj, is
2
VA“(Afs) = VA(BRIAf) =
19.6)
*
Apr * OB
Table 19.2 displays this value added, assuming a benchmark volatil-
ity of 17 percent. Given only one active decision per year, this
corresponds to basis points per year.
We can take this analysis a step further by looking in depth
at the forecast deviation Af, and the risk aversion gr. In particular,
we want to reformulate this analysis to
= Avoid the need to forecast the usual expected excess
return on the market pz,
= Make it easier to build up a forecast of exceptional return
Afs
® Avoid having to determine the risk aversion parameter
pr
546
Implementation
Naa
TABLE
19.2
Value Added
Aversion to Timing Risk Agr
Exceptional Forecast Af,
High, 0.14
Medium 0.09
Low, 0.06
4.00%
39
15.4
23.1
2.00%
2.5
3.8
5.8
0.00%
0.0
0.0
0.0
—2.00%
2.5
3.8
5.8
—4.00%
9.9
15.4
23.1
To begin with, we can see from Eq. (19.5) that the difference Af,
between the forecast fg and the usual yw, drives the optimal active
beta. Hence, we can greatly simplify matters by not worrying about
either pg or fs and forecasting the exceptional return Af; directly.
However, we must adjust our thinking from an absolute framework
(e.g., fg) to a relative framework (e.g., Afs).
This view is completely consistent with the approach to fore-
casting discussed in Chap. 10. Recall that the refined forecast of
exceptional benchmark return is
Afs 0
Hap (Gants
(19.7)
where IC = the information coefficient, the correlation be-
tween our forecasts and subsequent exceptional
benchmark returns. It’s a measure of skill.
S = score, a normalized signal with mean 0 and
standard deviation equal to 1 over time.
What is an appropriate level of benchmark timing skill? With
sufficient data on past forecasts, you can calculate the IC directly.
Without those data, or if you think that the past is not an accurate
guide to the future, then reasonable IC estimates are 0.05, 0.1, or
0.15 depending on whether you are good, very good, or terrific.
This is where humility should enter the game. Benchmark timing
skill is rare. If you assume that you have this skill that most others
lack, you may be misleading yourself. As a crude test, consider
your ability to forecast whether the benchmark will do better than
TABLE
193
Scores for Benchmark Timing
View
Probability
Score
Very positive
0.11
1.73
Positive
0.22
0.87
No view
0.33
0.00
Negative
0.22
—0.87
Very negative
0.11
=e}
average.” With a correlation of IC = 0.1, you would expect to be
correct 55 percent of the time.
Table 19.3 shows one way to translate qualitative views into
quantitative scores. The scores in Table 19.3 have an average of 0
and a standard deviation of 1. The probability column indicates
that we should be, on average, very positive one time in nine.
Using Af; = o, - IC - S, we can calculate the optimal active
beta and value added as a function of the score:
+
=
orn
.
=
.
BE (S) = (=) S=k«:S
(19.8)
gS
bi{
Ca
aay
recs
ICs
(iis
Sea
ese Bhs
pa
Table 19.4 displays these relationships, assuming an IC of 0.10, a
17 percent benchmark volatility, and a risk aversion of 0.06.
To make the benchmark timing process more transparent, we
would like to ignore the risk-aversion parameter and find a more
direct way to determine aggressiveness. We can do this using k,
defined in Eq. (19.8). Assuming that the score is normally distrib-
uted, a « of 0.06 implies that the portfolio’s beta will lie between
0.94 and 1.06 two-thirds of the time, falling above 1.06 one time in
six and below 0.94 one time in six. If that seems too aggressive,
then decrease x. This implies an increase in risk aversion and/or
a decrease in information coefficient, but we can also deal with k
2This does not mean better than the risk-free rate.
548
Implementation
TABLE
19.4
Active
Value
View
Probability
Score
Forecast
Beta
Added
Very positive
0.11
ila
2.94%
0.09
0.12%
Positive
0.22
0.87
1.47%
0.04
0.03%
No view
0.33
0.00
0.00%
0.00
0.00%
Negative
0.22
O87
—1.47%
—0.04
0.03%
Very negative
0.11
Sere}
—2.94%
—0.09
0.12%
directly. Table 19.5 shows how « depends on risk aversion and
information coefficient.
Using k, we can also examine value added in more detail.
Equation (19.9) writes the value added conditional on the score S.
The unconditional value added then is
VA* = E{VA*{S}} = (eee J6)
- E{S} = (s-se-IC) (19.10)
using the condition that the scores have mean 0 and standard
deviation 1. A very good forecaster, with an IC = 0.10, given a
benchmark volatility of 17 percent and a x of 0.05, can produce a
not very impressive expected value added of 4.2 basis points.’ And
TABLE
19.5
K
Aversion to Timing Risk
Skill Level
High, 0.14
Medium, 0.09
Low, 0.06
Good
0.01
0.02
0.02
Very good
0.02
0.03
0.05
World class
0.03
0.05
0.07
*The situation is even worse if the forecaster implements the timing bet using stock
selection as opposed to futures. The technical appendix will show that even a low
aversion to the unavoidable residual risk of that approach will shave 2.9 basis
points off that 4.2 basis points.
Benchmark Timing
549
with only one forecast per year, this is 4.2 basis points per year.
However, we shouldn’t give up yet. The way to add more value
with benchmark timing is to make high-quality forecasts more
frequently.
FORECASTING FREQUENCY
The analysis to this point has assumed a 1-year investment horizon.
That 1-year horizon is mainly responsible for the vanishing contri-
bution of benchmark timing to value added. The strategy’s informa-
tion ratio and value added depend on skill and breadth, according
to the fundamental law of active management, and benchmark
timing once per year sets the lower positive bound on breadth
(1 bet per year). To add more value, we must forecast more fre-
quently.*
Assume that we can make T forecasts per year. Divide the
year into T periods, indexed by t = 1, 2,..., T, with each period
of length 1/T years. For quarterly forecasts,
T = 4; for monthly
forecasts, T = 12; for weekly forecasts, T = 52; and for daily fore-
casts, T = 250 trading days. The volatility of the benchmark over
any period t will be
o,(t) = Wt
(19.11)
Period by period, the forecasting rule of thumb still applies:
oa,‘ IC:
S(t)
W/o
Now the IC is the correlation of the forecast and return over the
period of length 1/T.
Since we ultimately keep score on an annual basis, we must
analyze the annual value added generated by these higher-
Afp(t) = op(t) - IC - S(t) =
(19:12)
‘Consider the plight of a gambler who has a 65 percent chance to “beat the spread” on
the Super Bowl (once per year) compared to another gambler who has a 55
percent chance to beat the spread on each of the 480 (as of 1999) regular season
and playoff games.
550
Implementation
frequency forecasts. It is the sum of the value added for each period.
So, appropriately extending Eq. (19.4), we find
IE
q
VA = > Bra(t) « Afs(t) — der - >) Bia(t) - o3(f)
(19.13)
t=1
t=1
Using Eq. (19.12), this becomes
A
a
2
iy
\Wi\ = (22 «|
; Ss Bra(t) - S(t) — Apr: (2)
; De B3,(t)
(19.14)
yt
t=1
AV
and therefore the optimal active beta in period t becomes
Ke
Bit) = VT - (<—
- S(t)
(19.15)
If we forecast once per year, this reduces to Eq. (19.8). If we
forecast more frequently, we can be more aggressive. So, according
to Eg. (19.15), other things being equal, our active betas will double
if we forecast quarterly instead of annually. However, we will also
see later that the IC may shrink as we move to shorter time periods.
Given the optimal active betas in each period, the annual value
added conditional on the sequence of scores {S(1), S(2), ...
, S(T)} is
1g
2
VAMS(1),S(2), ..., S(T} = (7 }
Sst)
(19.16)
bia
and the unconditional expected annual value added is
re
SN
VA*
= (; -. T
C1917)
This is a form of the fundamental law of active management: The
optimal value added is proportional to the breadth T of the strategy.
Table 19.6 shows this potential for value added for various numbers
of forecasts per year and various IC levels. We have assumed a
medium aversion to risk of Agr = 0.09.
These results assume that each forecast is based on new infor-
mation. The forecasts must be independent. If you make one yearly
forecast, then divide it by 4 and use that for the four quarterly
forecasts, you have added no new information. It still counts as
only one forecast per year.
TABLE
19.6
a
a
ee a
a
Value Added
Number of Forecasts per Year
To see this concretely, let us represent the benchmark’s excep-
tional return over the year using a binary model:
rp(t) = [EN 6, ar 0, aie 2
o O95 8399 We 8400
(19.18)
where the 0; are independent and equally likely to be +1 or —1.
We will further specify this model in the following particular way:
Of those 400 components, the first 100 occur in the first quarter,
the second 400 occur in the second quarter, etc.” According to this
model, the benchmark exceptional return has annual variance of
400 and annual risk of 20 percent, with quarterly variance of 100
and quarterly risk of 10 percent.
First assume that we make only one forecast g per year:
8
g = 0; + 02 + Vio + 102 + O21 + B22 + 9301 + 8392 + > Nj
(19.19)
p=
where g includes elements of signal, the 0,; and elements of noise,
the n;, which are independent of the 6, and of each other. Each 7;
is equally likely to equal +1 or —1. The variance of this raw forecast
is 16; its standard deviation is 4 percent. Using Eq. (19.19), we can
calculate both an annual and a quarterly information coefficient
Alternatively, we could label these binary elements as 6, with i = 1,...,4 andj =
1,...100. The label i would denote the quarter. We prefer the notation in the text
because it emphasizes that without additional information, we will not know
which binary element influences which quarter.
552
Implementation
by correlating the forecast g with the annual and quarterly return,
respectively. We find
Ona
IC Sona wee
(19.20)
IC,
== = 0005
(19.21)
See
T0374
tn
We can substitute these results into Eq. (19.17) and see that the
value added is identical whether we consider the forecast g annually
or quarterly.
In contrast, suppose that we receive the same information, but
in parcels each quarter. The quarterly forecasts are
% = 9+ & +m +
(19.22)
82 = 8101 + O12 + N3 + 11
(19.23)
83 = B21 + B22 + Ns + No
(19.24)
84 = B30. + 8302 + 17 + Ns
(19.25)
The IC in each quarter is
2
IC,
= 79-9 = 0.10
(19.26)
and we get the full benefit of the four separate forecasts, according
to Eq. (19.17). We can also observe that breaking the annual forecast
g into four appropriate quarterly forecasts g, through g, requires
information on precisely which components of our signal apply to
which quarters. The signal g in Eq. (19.19) contains only the sum
over all the quarterly information.
»
PERFORMANCE ANALYSIS
We have already discussed performance analysis generally in Chap.
17, where we even presented approaches to benchmark timing
performance analysis. If we are limited to returns-based perfor-
mance analysis, Chap. 17 showed how to estimate benchmark tim-
ing skill by distinguishing up-market betas fron: down-market
betas.
Benchmark Timing
553
For portfolio-based performance analysis (or for benchmark
timing so long as we have ex ante estimates of portfolio betas),
we can separate the achieved active systematic return into three
components: expected active beta return, active beta surprise, and
active benchmark timing return. To do this, we require two parame-
ters: the expected benchmark return 1g and the average active beta.
The ex ante analysis takes yp, as given and assumes that the
average active beta is 0. In an ideal world, these parameters would
be part of the prior agreement between the manager and the client.
With these two parameters, we can attribute the systematic active
return, Bp,(t) « rg(t), over the time interval {t, t + At} as
Brat) > re(t) = Bpa(t) - pp: At + Bps(t) - [re(t) — wg: At]
(19.27)
We can interpret these components as
1. The expected active return Bp,(f)
+ wg - At
2. Benchmark timing Bp,(t) - [7s(t) — we - Af]
The benchmark timing component measures whether the portfo-
lio’s active beta is positive (negative) when the benchmark’s excess
return is greater (less) than jg - At. This benchmark timing term
is the realization of exactly what we are hoping for in the benchmark
timing utility, Eq. (19.4).
The ex post approach to portfolio-based performance attribu-
tion is very similar, except that it establishes the average market
return and beta target ex post. Let
Bra = (t) >)
Brat)
(19.28)
t=1
IE
and
7,° At = (t) Sn
(19.29)
fel
Then we separate the active systematic return as follows:
Bra(t) - re(t) = Bpalt) - 7g ° At + Bra ATs babe At]
(19.30)
+ [Bpa(t) — Boal « [re(t) — 7p - Ad]
or Bpa(t) « re(t)
(19.31)
= Boalt): Fp ° At + Bra: [ra(t) — 7p - At] + SB(t) - Sra(E)
554
Implementation
This ex post approach is similar in spirit to the ex ante ap-
proach. The two approaches would be identical if we had specified
ex ante an average return of 7; and an average beta of Bp.
_
Over the entire period, the first term averages
to Bm °
7, ‘ At. The second term averages to zero. The third term, the bench-
mark timing contribution, when averaged, captures the in-sample
covariance between the active beta and the benchmark returns.
We can also invent hybrid approaches, with one of the parame-
ters set ex ante and the other ex post.
As a final, general comment, the forecasting frequency can
also affect this ex post component of benchmark timing. A one-
forecast-per-year strategy will exhibit not only a low information
ratio and value added, but also a low t statistic. It may require
many years of observations to prove with statistical confidence the
existence of any benchmark timing skill.
SUMMARY
Benchmark timing strategies adjust active portfolio betas based on
forecasts of exceptional benchmark returns. Benchmark timing is
a one-dimensional problem, so whereas stock selection strategies
can benefit from diversifying bets cross-sectionally across stocks,
benchmark timing strategies can diversify bets only serially, by
frequent forecasts per year. Benchmark timing can realistically gen-
erate significant value added only through such frequent forecasts
per year. The most efficient approach to implementing benchmark
timing is through the use of futures, as opposed to the use of stocks
with betas different from 1. Performance analysis techniques exist
that can measure benchmark timing contributions.
PROBLEMS
1. Given a risk aversion to benchmark timing of 0.09, an
exceptional market return forecast of 5 percent, and
market risk of 17 percent, what is the optimal portfolio
beta?
2. Bob isa benchmark timer. His IC is 0.05, he bets once
per year, and he has a low aversion to benchmark timing
risk \gr = 0.06. What is his value added? What is his
optimal level of active risk?
Benchmark Timing
555
3. How many years of active returns would you require in
order to determine that Bob has statistically significant
(95 percent confidence level) benchmark timing skill?
4. How would the answers to problems 1 and 2 change if
Bob bet 12 times per year?
REFERENCES
Ambachtsheer, Keith P. “Pension Fund Asset Allocation in Defense of a 60/40
Equity/Debt Asset Mix.” Financial Analysts Journal, vol. 43, no. 5, 1987,
pp- 14-24.
Brocato, Joe, and P. R. Chandy. “Does Market Timing Really Work in the Real
World?” Journal of Portfolio Management, vol. 20, no. 2, 1994, pp. 39-44.
. “Market Timing Can Work in the Real World:
A Comment.” Journal of
Portfolio Management, vol. 21, no. 3, 1995, pp. 39-44.
Cumby, Robert E., and David M. Modest. “Testing for Market Timing Ability.”
Journal of Financial Economics, vol. 19, no. I, 1987, pp. 169-189.
Gennotte, Gerard, and Terry A. Marsh. “Variations in Economic Uncertainty and
Risk Premiums on Capital Assets.” Berkeley Research Program in Finance
Working Paper 210, May 1991.
Henriksson, Roy D., and Robert C. Merton. “On Market Timing and Investment
Performance II. Statistical Procedures for Evaluating Forecasting Skills.”
Journal of Business, vol. 54, no. 4, 1981, pp. 513-533.
Larsen, Glen A., Jr. and Gregory D. Wozniak. “Market Timing Can Work in the
Real World.” Journal of Portfolio Management, vol. 21, no. 3, 1995.
Modest, David. “Mean Reversion and Changing Risk Premium in the U.S. Stock
Market: A Survey of Recent Evidence.” Presentation at the Berkeley Program
Finance Seminar, April 3, 1989.
Rudd, Andrew, and Henry K. Clasing, Jr. Modern Portfolio Theory, 2d ed. (Orinda,
Calif.: Andrew Rudd 1988).
Sharpe, William F. “Likely Gains from Market Timing.” Financial Analysts Journal,
vol. 43, no. 2, 1975, pp. 2-11.
. “Integrated Asset Allocation.” Financial Analysts Journal, vol. 43, no. 5,
1987, pp. 29-32.
Wagner, Jerry, Steve Shellans, and Richard Paul. “Market Timing Works Where
It Matters Most ... in the Real World.” Journal of Portfolio Management, vol.
18, no. 4, 1992, pp. 86-92.
TECHNICAL APPENDIX
This technical appendix will investigate how to implement a bench-
mark timing strategy using stocks instead of futures. It will show
that such an approach leads to unavoidable residual risk.
Consider the problem of constructing a fully invested portfolio
with beta Bsr and minimum residual risk.
556
Implementation
Proposition 1
1. The portfolio BT,
hr = (PP) -h, + (7
—
Be)
‘he
(19A.1)
is the minimum-risk, fully invested portfolio with B = Bgr.
As is clear from Eq. (19A.1), it is a linear combination of
the benchmark and portfolio C.
2. Portfolio BT is also the minimum-residual-risk, fully
invested portfolio with B = Bp5r
3. Portfolio BT has residual risk wpr:
wer = (Bra * Op)” ° (;
bc}
(19A.2)
where Bp, is portfolio BT’s active beta: Bp, = Bsr — 1.
Proof
To prove item 1, start with the observation that portfolio
BT is clearly fully invested, since the weights in Eq. (19A.1) sum
to 1, and the benchmark and portfolio C are fully invested. We can
also quickly verify that portfolio BT has B = Bs; More generally,
we can show that portfolio BT is the solution to the problem
Min{h’ - V - h}
(19A.3)
Subject to
h’-e=1
(19A.4)
1p
ee
(19A.5)
It is the minimum-risk portfolio, subject to the constraints of full
investment and 6 = B57. To derive Eq. (19A.1), we must solve the
minimization problem, use the definition of portfolio C, and use
the definition of the vector B in terms of the benchmark portfolio.
To prove item 2, for any portfolio P, we can decompose total
risk as
op = Bp: 03 + wh
(19A.6)
Among the universe of all portfolios with 8 = Bp the minimum-
total-risk portfolio is also the minimum-residual-risk portfolio.
Benchmark Timing
557
To prove item 3, we can calculate the residual holding for
portfolio BT:
herr = hpr — Bor * hz
(19A.7)
w= (BB (LEB)
cn
Using Eq. (19A.8), we can directly calculate residual variance and
verify Eq. (19A.2).
We can use this result to analyze further the value-added
implications of this unavoidable residual risk. Assuming T forecasts
per year, we will incur SADESeS,) residual risk over the year of
E{w3y} >
E{w3,(t)}
(19A.9)
The expected residual variance each period is
a3
Elwix(t)} = (2)
: (; oc -| E(B}
(19.10)
where the benchmark total variance over period t is o3/T. Using
Eq. (19.14) from the main text, which solves for the active beta each
period, Eq. (19A.10) becomes
ff
i 52
od (el
Seal
aS
&
Elvin) = (2) (2) (AS) E{S%()}
(19A.11)
ol
4
2
Elwgr(t)} = (8 , (F ic)
(194.12)
Subtracting the value-added cost of this expected uncondi-
tional residual variance from the expected unconditional value
added from benchmark timing [Eq. (19.16)] leads to
a
cera
Es Gj
; Nbr
| ibe Bc
Apr
As we discussed in the main text, remembering that Bc = o¢/o%
and assuming o; = 18 percent and o¢ = 12 percent leads to Bc = 4/9.
Equation (19A.13) then shows that benchmark timing via stock
selection leads to positive net value added only if the investor’s
(19A.13)
558
Implementation
aversion to residual risk is significantly less than his or her aversion
to benchmark timing risk.
Exercise
1. Prove Eq. (19A.1), the formula for the minimum-risk,
fully invested portfolio with B = Bsr.
Applications Exercises
Using the MMI stocks, build portfolio BT, the minimum-risk, fully
invested portfolio with B =
1.05 relative to the (benchmark)
CAPMMI. Also build portfolio C from MMI stocks.
1. What is the beta of portfolio C?
2. Compare portfolio BT to the linear combination of
portfolio C and portfolio B (the CAPMMI) according to
Eq. (19A.1).
3. What is the residual risk of portfolio BT? Compare the
result to Eq. (19A.2).
