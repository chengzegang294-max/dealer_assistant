# Chapter 15: Long/Short Investing

- **book_name**: Active Portfolio Management
- **main_source**: pdf
- **cross_check_source**: none
- **pdf_role**: main_text_source
- **split_scope**: pages 441-466

---

CHAPTER
15
Long/Short Investing
INTRODUCTION
U.S. institutions have invested using long/short strategies since at
least the late 1980s. These strategies have generated controversy,
and, over time, increasing acceptance as a worthwhile innovation.
Long/short strategies offer a distinct advantage over long-only
strategies: the potential for more efficient use of information, partic-
ularly but not exclusively downside information.
This chapter will analyze several important aspects of long/
short strategies and, by implication, some important and poorly
understood aspects of long-only strategies. We will define long/
short strategies and briefly introduce their advantages and the
controversies surrounding these advantages. We will then analyze
in detail the increased efficiency offered by long/short strategies
and the subtle but pervasive effects of the long-only constraint.
This analysis is therefore important to all managers—not just those
offering long/short strategies. We will later discuss the appeal of
long/short strategies and some empirical observations. The chapter
ends with the usual notes, references, and technical appendix.
The main results of this chapter include the following:
= The benefits of long/short investing arise from the
loosening of the (surprisingly important) long-only
constraint.
® Long/short implementations offer the most improvement
over long-only implementations when the universe of
assets is large, the assets’ volatility is low, and the
strategy has high active risk.
419
420
Implementation
# The long-only constraint tends to induce biases,
particularly toward small stocks. Surprisingly, it can
limit the ability to completely act on upside information,
by not allowing short positions that could finance long
positions.
In this chapter, we will define long /short strategies specifically
as equity market-neutral strategies. These strategies have betas of
0 and equal long and short positions. Some databases group these
strategies in the more general category of “hedge fund.” However
the hedge fund category can include almost any strategy that allows
short positions. We will focus much more specifically on equity
strategies managed according to the principles of this book, and
with zero beta and zero net investment.
Long/short investing refers to a method for implementing
active management ideas. We can implement any strategy as long/
short or long-only. Long/short investing is general. It does not
refer to a particular source of information.
Now, every long-only portfolio has an associated active
portfolio with zero net investment and often zero beta. There-
fore, every long-only portfolio has an associated long/short
portfolio. But the long-only constraint has a significant impact
on this associated long/short portfolio. Long/short strategies
provide for more opportunities—particularly in the size of short
positions in smaller stocks (assuming a capitalization-weighted
benchmark).
Long/short strategies are becoming increasingly popular.
According to Pensions and Investments (May 18, 1998), 30 invest-
ment management firms offer market-neutral strategies, up from
the 21 investment management firms one year earlier.
«
Market-neutral strategies are something of a “phantom” strat-
egy. The Pensions and Investments list does not include many large
investment management firms that offer market-neutral strategies.
It also appears to underreport the assets invested for some of the
firms listed. Market-neutral strategies short stocks, a strategy
frowned upon by some owners of funds. This apparently leads
to enhanced discretion by the managers. But this is only part of
the controversy.
Long /Short Investing
421
a
ee
eee Ae
THE CONTROVERSY
Proponents of long/short investing offer several arguments in its
favor. One simple argument depends on diversification. A long/
short implementation includes effectively a long portfolio and a
short portfolio. If each of these portfolios separately has an informa-
tion ratio of IR, and the two portfolios are uncorrelated, then the
combined strategy, just through diversification, should exhibit an
information ratio of IR - \/2. The problem with this argument is
that it applies just as well to the active portfolio associated with
any long-only portfolio. So this argument can’t be the justification
for long/short investing.
A second argument for long/short investing claims that the
complete dominance of long-only investing has preserved short-
side inefficiencies, and hence the short side may offer higher alphas
than the long side.
The third and most important argument for long/short in-
vesting is the enhanced efficiency that results from the loosening
of the long-only constraint. The critical issue for long/short in-
vesting isn’t diversification, but rather constraints.
These arguments in favor of long/short investing have gener-
ated considerable controversy. The first argument, based on diversi-
fication, is misleading if not simply incorrect. Not surprisingly, it
has attracted considerable attack. The second argument is difficult
to prove and brings up the issue of the high implementation costs
associated with shorting stocks. The third argument is the critical
issue, with implications for both long/short and long-only in-
vestors.
THE SURPRISING IMPACT OF THE
LONG-ONLY CONSTRAINT
We are interested in the costs imposed by the most widespread
institutional constraint—the restriction on short sales—or, equiva-
lently, the benefits of easing that constraint. We will ignore transac-
tions costs and all other constraints, and focus our attention on
how this constraint affects the active frontier: the trade-off between
exceptional return a and risk o.
Let’s start with a simple market that has N assets and an equal-
weighted benchmark. We presume in addition that all assets have
422
Implementation
identical residual risk w and that residual returns are uncorrelated.
This model opens a small window and allows us to view the
workings of the long-only constraint.
Let a, be the expected residual return on asset n and Xz the
residual risk aversion. In this setup, assuming that we want zero
active beta, the active position for asset n is
Qn
The overall residual (and active) risk wp is
N
1
3 os Arsen ‘ > a2
(15.2)
We know from Chap. 10 that alphas have the form a, = o -
(IR/\/N) - z,, where z, is a score with mean 0 and standard devia-
tion 1, and we have invoked the fundamental law of active manage-
ment to write the information coefficient in terms of the information
ratio and the number of assets. Hence, the active positions and
portfolio active risk become
TRiz,
See a
;
area
(15.3)
toe oh
Det
yeaa. \
Nivel
ak
DN
a)
n=1
We can use Eqs. (15.3) and (15.4) to link the active position with
the desired level of active risk Wp the stock’s residual risk w, and
the square root of the number of assets \/N:
Wp ‘Zn
Re
oe oe
VN +o
is >)
The limitation on short sales becomes binding when the active
position plus the benchmark holding is negative. For an equal-
weighted benchmark, this occurs when
a=
W
ithe
(15.6)
Figure 15.1 shows this information boundary as a function of the
number of stocks for different levels of active risk.
“YSU
eater
o1osz10d
03
AyAIsuag
[Gc]
amMBry
syassy
Jo
Joaquin
086
oss
OSL
0s9
oss
OSP
OSE
0S7
OST
0s
9.1096 WINUHUTTA,
423
424
Implementation
Information is wasted if the z score falls below the minimum
level. The higher the minimum level, the more information we are
likely to leave on the table. As an example, if we consider a strategy
with 500 stocks, active risk of 5 percent, and typical residual risk
of 25 percent, we will waste information whenever our score falls
below —0.22. This will happen 41 percent of the time, assuming
normally distributed scores.
This rough analysis indicates that an aggressive strategy in-
volving a large number of lower-volatility assets should reap the
largest benefits from easing the restriction on short sales. The more
aggressive the strategy, the more likely it is to hit bounds. The
lower the asset volatility, the larger the active positions we take.
The more assets in the benchmark, the lower the average benchmark
holding, and the more likely it is that we will hit the boundary.
Indirect Effects
In a long-only optimization, the restriction against short selling has
both a direct and an indirect effect. The direct effect, studied above,
is to preclude exploiting the most negative alphas. The indirect
effect grows out of the desire to stay fully invested. In that case,
we must finance positive active positions with negative active posi-
tions. Hence, a scarcity of negative active positions can affect the
long side as well: Overweights require underweights.
Put another way, without the long-only constraint we could
take larger underweights relative to our benchmark. But since un-
derweights and overweights balance, without the long-only con-
straint we will take larger overweights as well.
We can illustrate this “knock-on” effect with a simple case.
We start with an equal-weighted benchmark and generate random
alphas for each of the 1000 assets. Then we construct optimal portfo-
lios in the long-only and long/short cases. Figure 15.2 displays the
active positions in the long/short and long-only cases, with assets
ordered by their alphas from highest to lowest.
In the long/short case, there is a rough symmetry between the
positive and negative active positions. The long-only case essentially
assigns all assets after the first 300 the same negative alpha. We ex-
pected that the long-only portfolio would less efficiently handle neg-
006
008
‘YTeuysueq
payys1em
yenba
:suoyisod
aayoe
ATUO-Buo]
pue
joys
/Su0T
z'¢1
amBry
yuey
jassy
002
009
00S
00r
00¢
007
00r
0
%ST-
%V'C-
%S1-
%01-
%S0-
J40yS/su0']
—
A[UQ-3u0']
——
00
BuIP[OH 2AndV
S50
OT
ST
VT
425
426
Implementation
ative alphas than the long/short portfolio. More surprisingly, Fig.
15.2 shows that it also less efficiently handles the positive alphas.
THE IMPORTANCE OF THE
BENCHMARK DISTRIBUTION
This knock-on effect is more dramatic if the benchmark is not equal-
weighted. We can illustrate this with an extreme case where the
benchmark consists of 101 stocks. Stock 1 is 99 percent of the bench-
mark, and stocks 2 through 101 are each 0.01 percent: Gulliver and
100 Lilliputians. To make this even simpler, suppose that 50 of
the Lilliputians have positive alphas of 3.73 percent and 50 have
negative alphas of the same magnitude. We consider two cases:
Gulliver has a positive alpha, again 3.73 percent, and Gulliver has
a negative alpha, —3.73 percent.
In the long/short world, the capitalization of the stocks is
irrelevant. Table 15.1 displays the active positions of the stocks,
along with some portfolio characteristics:
Gulliver does not merit special consideration in the long/
short world. Gulliver, Ltd., receives the same active position as a
Lilliputian company with a similar alpha. Note that since all of the
active positions are smaller than a
, the no-short-sale restriction
would not be binding if the benchmark assets were equal-weighted.
We encounter significant difficulty with the highly imbalanced
benchmark when we disallow short sales. In that case, it makes a
TABLE
15.1
Long/Short Results
a (Gulliver)
Characteristic
Positive
Negative
Gulliver active position
0.79%
—0.79%
Positive stock active position
0.79%
0.80%
Negative stock active position
—0.80%
—0.79%
Portfolio alpha
3.00%
3.00%
Portfolio active risk
.
2.00%
2.00%
Long /Short Investing
427
TABLE
15.2
pee Le
eS
a
i
ee
a
Long-Only Results
a (Gulliver)
Characteristic
Positive
Negative
Gulliver active position
0.01%
SS
Positive stock active position
0.01%
0.04%
Negative stock active position
—0.01%
—0.01%
Portfolio alpha
0.04%
0.15%
Portfolio active risk
0.02%
0.39%
great deal of difference whether Gulliver’s alpha is positive or
negative. With a negative alpha, we assume a very large negative
active position (—1.55 percent) that allows us to finance the over-
weightings of the Lilliputians with positive alphas.’ But when Gul-
liver has a positive alpha, we can achieve only tiny active positions,
both long and short. Table 15.2 displays the results.
The Gulliver example illustrates another problem: the poten-
tial for a significant size imbalance. The shortage of negative active
positions causes relatively larger underweighting decisions on the
higher-capitalization stocks. If the alpha on Gulliver had a 50/50
chance of being a positive or negative 3.73 percent, the average
active holding of Gulliver would be —0.77 percent.
Capitalization-Weighted Benchmarks
The Gulliver example shows that the distribution of capitalization
in the benchmark is an important determinant of the potential for
'There is an alternative approach:
® Relax the condition that the net overweight must equal the net underweight.
®@ Use a short cash position (leverage!) to finance the overweights.
@ Sell the benchmark forward to cover the added benchmark exposure.
In the Gulliver model, this procedure allows us to achieve an alpha of 1.53
percent with an active risk of 1.42 percent. The negative cash position is 39
percent of the portfolio’s unlevered value.
428
Implementation
adding value in a long-only strategy. To calculate the benefits of
long/short investing in realistic environments, we will need a
model of the capitalization distribution. This requires a short detour.
We will use Lorenz curves to measure distributions of capital-
ization. To construct them, we must
® Calculate benchmark weight as a fraction of total
capitalization.
m Order the assets from highest to lowest weight.
® Calculate the cumulative weight of the first n assets, as n
moves from largest to smallest.
The Lorenz curve plots the series of cumulative weights. It starts
at 0 and increases in a concave fashion until it reaches 1. If all assets
have the same capitalization, it is a straight line.
Figure 15.3 shows Lorenz curves for the Frank Russell 1000
index, an equal-weighted portfolio, and a model portfolio designed
(as we will describe below) to resemble the Frank Russell 1000
index.
One summary statistic for the Lorenz curve is the Gini coeffi-
cient, which is twice the area under the curve less the area under
the equal-weighted curve. Gini coefficients must range between 0
(for equal-weighted benchmarks) and 1 (for single-asset bench-
marks). So we can draw Lorenz curves for benchmarks with any
arbitrary distribution of capitalization, and summarize any distri-
bution with a Gini coefficient. To progress further, we must assume
a specific form for the distribution of capitalization.
A Capitalization Model
We will assume that the distribution of capitalization is log-normal.
Here is a one-parameter model that will produce such a distri-
bution.
First, we order the N assets by capitalization, from largest
(n = 1) to smallest (n = N). Define
aod
JVC
Leen
ti fica
These values look like probabilities. They start close.to 1 and move
toward 0 as the capitalization decreases. Next, we calculate a nor-
yuey
jossy
0001
006
008
OOL
009
00s
0Or
Siem
jenby.
—
.
—
[epoxy
[eWI0U-3o7]
0001
Yi
———
"SJOSSP
(QOL
‘SPAMS
ZUsIOT
EG]
aN3Iy
00€
00¢
001
0
SsUIpP[OY aAnejnUuIND
429
430
Implementation
eee
ee
ee
ee
ee
TABLE
15.3
eS
Country
Index
Assets
Gini
Constant c
U.S.
Frank Russell 1000
1000
0.71
1:55
U.S.
MSCI
381
0.66
1.38
U.K.
MSCI
135
0.63
1.30
Japan
MSCI
308
0.65
1.35
The Netherlands
MSCI
23
0.64
1.38
Freedonia
Equal weight
101
0.00
0.00
Freedonia
Cap weight
101
0.98
WES
mally distributed quantity y, such that the probability of observing
Ya 1S Pas
Pn = Ply}
(15.8)
where ®{ } is the cumulative normal distribution.
So far, we have converted linear ranks to normally distributed
quantities y,. To generate capitalizations, we use
CAP, = Exple=
y,}
(15.9)
We can choose the constant c to match the desired Gini coefficient
or to match the Lorenz curve of the market.”
We used this model to match the Frank Russell 1000 Index in
Fig. 15.3. Table 15.3 contains similar results for several markets
covered by Morgan Stanley Capital International (MSCI) Indexes
as of September 1998. The equal-weighted and Gulliver examples
reside in the hypothetical land of Freedonia.’
The constant c ranges from 1.30 to 1.60 in a large number of
countries. To analyze the loss in efficiency due to the long*only
*As an alternative, set the constant c to the standard deviation of the log of the
capitalization of all the stocks. The two criteria mentioned in the text place greater
emphasis on fitting the larger-capitalization stocks.
*Freedonia appeared in the 1933 Marx Brothers movie Duck Soup. During a 1994 Balkan
eruption, when asked if the United States should intervene in Freedonia, several
U.S. congressmen laughed, several stated that it would require further study, and
several more were in favor of intervention if Freedonia continued its policy of
ethnic cleansing.
Long/Short Investing
431
constraint, we will use the value 1.55. This stems from a feeling
that the MSCI indices necessarily trim out a great many of the
smaller stocks in a market. The Freedonia rows show an equal and
a very unequal benchmark for comparison purposes.
Armed with this one-parameter model of the distribution of
capitalization, we are ready to derive our rough estimates of the
potential benefits of long/short investing.
An Estimate of the Benefits of
Long/Short Investing
We cannot derive any analytical expression for the loss in efficiency
due to the long-only constraint, since the problem contains an
inequality constraint. But we can obtain a rough estimate of the
magnitude of the impact with a computer simulation. As our previ-
ous simple analysis showed, the important variables in the simula-
tion include the number of assets and the desired level of active
risk. We considered 50, 100, 250, 500, and 1000 assets, with desired
risk levels* from 1 to 8 percent by 1 percent increments, and from
there to 20 percent by 2 percent increments.
For each of the 5 levels of assets and the 14 desired risk levels,
we solved 900 randomly generated long-only optimizations. For
each case, we assumed uncorrelated residual returns, identical re-
sidual risks of 25 percent, a full investment constraint, and an
information ratio of 1.5. We ignored transactions costs and all other
constraints. We generated alphas using
Oy, = O° (4) ee
(15.10)
Figure 15.4 shows the active efficient frontier: the alpha per unit
of active risk.
We can roughly estimate the efficient frontiers in Fig. 15.4 as
{1 + w/100}!-™ — 7
i 4)
(15.11)
a(wN) = 100: IR - ;
“We used Eq. (15.4) to convert desired risk levels to risk aversions. We required
extremely high levels of desired risk, since the long-only constraint severely
hampers our ability to take risks.
PSL ansry
YSKY PAMIV 38B92104
%0'6
%0°8
% OL
%0°9
%0°S
%0'P
%0'€
%0°7
%0'T
%0'°D
%0'0
%0'T
%0'°%
OE
=
%0r
3
uoys/3u0] —e—
8
B
>
w0S
8
<
@
w
oO
09
la}
i}
%0'L
%0'8
%0°6
%0'01
432
Long/Short Investing
433
where
y(N) = {53 + N}°°”
(15.12)
and, as elsewhere in the book, we measure a and w in percent.
As anticipated, with the information ratio held constant, long-
only implementations become less and less effective, the greater
the number of assets. We can also see that higher desired active
risk lowers efficiency. In fact, we can define an information ratio
(and information coefficient) shrinkage factor as
Shinkage = toile
(15.13)
7 (22) {! + w/100}!-%™ — i
Le
1 — y(N)
Figure 15.5 illustrates the dependence of shrinkage on risk and the
number of assets. For typical U.S. equity strategies—500 assets and
4.5 percent risk—the shrinkage is 49 percent according to Eq. (15.13),
0.75
0.50
IR
Shrinkage
Factor
0.25
0.00
0.0%
10%
20%
30%
40%
50%
6.0%
7.0%
8.0%
9.0%
Forecast Active Risk
Figure 15.5
434
Implementation
which agrees with Fig. 15.5. The long-only constraint has enormous
impact: It cuts information ratios for typical strategies in half!
Equation (15.13) also allows us to quantify the appeal of en-
hanced indexing strategies, ie., low-active-risk strategies. The
shrinkage factor is 71 percent for a long-only strategy following
500 assets with only 2 percent active risk. At this lower level of
risk, we lose only 29 percent of our original information ratio.
At high levels of active risk, long/short implementations can
have a significant advantage over long-only implementations. At
low levels of active risk, this advantage disappears. And, given the
higher implementation costs of long /short strategies (e.g. the uptick
rule, costs of borrowing), at very low levels of active risk, long-
only implementations may offer an advantage.
With a large number of assets and the long-only constraint,
it is difficult to achieve higher levels of active risk. Using Eq. (15.11),
we can derive an empirical analog of Eq. (15.4):
ey ee ee
2°
@) 4 (1 41ay 100)"
See the technical appendix for details.
Figures 15.4 and 15.5 illustrate efficient frontiers under several
assumptions: an inherent information ratio of 1.5, a log-normal
size distribution constant c = 1.55, and identical and uncorrelated
residual risks of 25 percent. We have analyzed the sensitivities of
the empirical results to these assumptions.
Changing the inherent information ratio does not affect our
conclusions at all. As Eq. (15.11) implies, the efficient frontier simply
scales with the information ratio.
Changing the log-normal size distribution constant through
the range from 1.2 to 1.6, a wider range than we observed in
examining several markets, has a very minor impact. Lower ceeffi-
cients are closer to equal weighting, so the long-only constraint is
less restrictive. At 4.5 percent active risk and 500 assets, though,
as we vary this coefficient, the shrinkage factor ranges only from
0.49 to 0.51.
Figure 15.6 shows how our results change with asset residual
risk. Our base-case assumption of 25 percent is very close to the
median U.S. equity residual risk. But we may be focusing on a
more narrow universe. As asset residual risk increases, we can
achieve more risk with smaller active positions, making the long-
Xr
(15.14)
Long/Short Investing
435
0.50
IR
Shrinkage
Factor
0.25
0.00
0%
1%
2%
3%
4%
5%
6%
7%
Forecast Active Risk
Figure 15.6 Sensitivity to asset residual risk.
only constraint less binding. At the extremely low level of 15 per-
cent, the long-only constraint has very high impact. In the more
reasonable range of 20 to 35 percent, the shrinkage factor at 4.5
percent risk and 250 assets ranges from 65 to 54 percent.
We can also analyze the assumption that every asset has equal
residual risk. Given an average residual risk of 25 percent, and
assuming 500 assets, we analyzed possible correlations between
size (as measured by the log of capitalization) and the log of residual
risk. We expect a negative correlation: Larger stocks tend to exhibit
lower residual risk. Looking at large U.S. equities (the BARRA
HICAP universe of roughly the largest 1200 stocks), this correlation
has varied from roughly —0.51 to —0.57 over the past 25 years.
Figure 15.7 shows the frontier as we vary that correlation from
0 to —0.6. With a correlation of 0, we found a shrinkage factor of
49 percent at 4.5 percent active risk. With a correlation of —0.6, the
situation improves, to a shrinkage factor of 0.63.
Finally, Fig. 15.8 displays the size bias that we anticipated.
Figure 15.8 shows the result for various correlations between size
and the log of residual risk, though the correlation does not signifi-
%9
09°Q- = 1403 —y»—
0S°0- = 1109 —y—
Op'0- = 41109.-@--
00°0 =41109..4--
%S
YSN
9AWIV
3S8¥99107
%®V
‘suOTIETaLIOD APTHRTOA /azIs 0} APANISUaS Z°C¢] aINSLy
ME
Te
%1
%0
00°0
Sz'0
0s"0
SL°0
10}98,y ISEYULIYS YY
436
%0°L
%0°9
%0°S
“SUOHLALIOD
ApTHRIOA
/azZIs
07
APLAYISUAS
SeIq
aZIS
g’CT
amnsiy
YSTY
IAI
1S¥I910,4
0b
VE
0
OT
%0°0
6°0-
000
=
00»
09'0-
=
1103
—e—
OS
0-
=
00
x
Op’
0-
=
0S
—y—
£0"
c0-
T0-
00
selg aZ1¢
437
438
Implementation
cantly change the result. We have measured size as log of capitaliza-
tion, standardized to mean 0 and standard deviation 1. So an active
size exposure of —0.3 means that the active portfolio has an average
size exposure 0.3 standard deviation below the benchmark.
These size biases are significant. Figure 15.8 implies that a
typical manager following 500 stocks and targeting 4.5 percent risk
will exhibit a size exposure of —0.65. In the United States, from
October 1997 through September 1998, the size factor in the BARRA
U.S. equity model exhibited a return of 1.5 percent: Large stocks
outperformed small stocks. This would have generated a 98-basis-
point loss, just due to this incidental size bet. From September
1988 through September 1998, the same size factor experienced a
cumulative gain of 3.61 percent, generating a loss of 2.35 percent
over that 10-year period.
THE APPEAL OF LONG/SHORT INVESTING
Who should offer long/short strategies? Who should invest in
them? Clearly, long/short strategies are a “pure” active manage-
ment bet. The consensus expected return to long/short strategies
is zero, since they have betas of zero. Put another way, the consensus
investor does not invest in long/short strategies. Therefore, the
most skillful active managers should offer long/short strategies. It
allows them the freedom to implement their superior information
most efficiently.
Long/short strategies offer no way to hide behind a bench-
mark. A long-only manager delivering 15 percent while the bench-
mark delivers 20 percent is arguably in a better position than a
long/short manager losing 5 percent. While this isn’t an intrinsic
benefit of long-only strategies, it can be a practical benefit for inyest-
ment managers.
Long/short strategies also offer investment managers the free-
dom to trade only on their superior information. They can build
a long/short market-neutral portfolio using only utility stocks, if
that is where they add value. They have no reason to buy stocks
just because they are benchmark members. Both the long and the
short sides of the portfolio may have large active risk relative to
the S&P 500—just not to each other.
Long/Short Investing
439
For investors, long/short strategies offer the most benefit to
those investors who are best able to identify skillful managers.
Given that, long/short strategies are quite appealing because of
the (engineered) low correlation with equity market benchmarks.
Long/short strategies can, in this way, successfully compete
against bonds.
Long/short investing also offers the appeal of easy alpha por-
tability. Futures contracts can move active return from one bench-
mark to another. If we start with a strategy managed relative to
the S&P 500, and sell S&P 500 futures and buy FTSE 100 futures,
we will transfer the alpha to the FTSE 100. In a conventional long-
only strategy, this transfer requires an extra effort. It is not the
natural thing to do. A long/short strategy places the notion of a
portable alpha on center stage. With a long/short strategy, we start
with the pure active return, and must chose a benchmark. The
potential for transfer is thrust upon us.
Finally, long/short investing offers the possibility of more
targeted active management fees. Long-only portfolios contain, to
a large extent, the benchmark stocks. Long-only investors pay active
fees for that passive core. Long/short investors pay explicitly for
the active holdings.
EMPIRICAL OBSERVATIONS
Here we wish to present preliminary observations on long/short
strategies. These strategies do not have a sufficiently long track
record
to definitively compare
their performance to that of
long-only strategies. But we can begin to understand especially
their risk profile, and observe at least initially their performance
record.
These results are based on the performance of 14 U.S. long/
short strategies with histories of varying lengths, but all in the
1990s, ending in March 1998.° These 14 strategies are those of large,
sophisticated quantitative managers. Most of these managers are
5See Freeman (1997).
6See Kahn and Rudd (1998).
440
Implementation
SS
Ee EE
E—E—E—e———————————Ee
ee
TABLE
15.4
History
S&P 500
Percentile
(Months)
Volatility
Beta
Correlation
96
10.90%
0.10
0.23
86
6.22%
0.06
0.15
1
5.50%
0.02
0.04
50
4.12%
—0.03
—0.07
28
3.62%
—0.16
—0.20
BARRA clients. Table 15.4 shows the relevant observations. It is
important to keep in mind the small and potentially nonrepresenta-
tive sample behind these data.
First, note that the risk levels here do not substantially differ
from the typical active risk levels displayed in Table 5.8.’ So, at
least based on these 14 sophisticated implementations, long/short
strategies do not exhibit substantially higher levels of risk than
long-only strategies.
Second, according to Table 15.4, these strategies achieved mar-
ket neutrality. They exhibit realized betas and market correlations
very close to zero. In fact, the highest observed correlations corres-
ponded to managers with the shortest track records. There is no
statistical evidence that any of these strategies had true betas differ-
ent from zero, and the realized numbers are all quite small. This
(admittedly limited) sample refutes the argument that achieving
market neutrality is difficult.
Third, at least in this historical period, these long/short strate-
gies as a group exhibited remarkable performance. The performance
results of 14 strategies over a particular market period do not prove
that long/short implementations will boost information ratios, but
they do help explain the increasing popularity of these strategies.
‘The standard error of the mean risk level for these long/short strategies is 0.64 percent.
So while the medians displayed here exceed those in Table 5.8,the difference is
not significant at the 95 percent confidence level.
Long/Short Investing
441
SUMMARY
Long/short investing is an increasingly popular approach to imple-
menting active strategies. Long/short strategies offer the potential
to more efficiently implement superior information. Because the
long-only constraint is an inequality constraint, and because its
impact depends on the distribution of benchmark holdings, we
cannot derive many detailed analytical results on exact differences
in efficiency. However, both simple models and detailed simula-
tions show that the benefits of long/short investing can be signifi-
cant, particularly when the universe of assets is large, the assets’
volatility is low, and the strategy has high active risk.
From the opposite perspective, long-only managers should
understand the surprising and significant impact of the long-only
constraint on their portfolios. Among the surprises: This constraint
induces a significant negative size bias, and it constrains long po-
sitions.
Empirical observations on long/short investing are prelimi-
nary, but should certainly inspire further interest and investigation.
NOTES
The debate over long/short investing has been contentious, and
even acrimonious. In part, the controversy arose because the initial
arguments in favor of long/short investing relied on diversification,
as we discussed first. That simple argument is misleading in sev-
eral ways.
The first serious criticism of long/short investing was by Mi-
chaud (1993). From there the debate moved to Arnott and Lein-
weber (1994), Michaud (1994), Jacobs and Levy (1995), and a confer-
ence of the Institute for Quantitative Research in Finance (the “Q
Group”), “Long/Short Strategies in Equity and Fixed Income,” at
La Quinta, California, in October 1995. Jacobs and Levy (1996),
Freeman (1997), Jacobs, Levy, and Starer (1998), and Levin (1998)
have subsequently published further detailed analyses of aspects
of long/short investing.
More recent work has looked at how long/short strategies fit
into overall pension plans [Brush (1997)] and the performance of
long/short managers [Kahn and Rudd (1998)].
442
Implementation
PROBLEMS
1. Jill manages a long-only technology sector fund. Joe
manages a risk-controlled, broadly diversified core
equity fund. Both have information ratios of 0.5. Which
would experience a larger boost in information ratio by
implementing his or her strategy as a long/short
portfolio? Under what circumstances would Jill come out
ahead? What about Joe?
2. You have a strategy with an information ratio of 0.5,
following 250 stocks. You invest long-only, with active
risk of 4 percent. Approximately what alpha should you
expect? Convert this to the shrinkage in skill (measured
by the information coefficient) induced by the long-only
constraint.
3. How could you mitigate the negative size bias induced
by the long-only constraint?
REFERENCES
Arnott, Robert D., and David J. Leinweber. “Long-Short Strategies Reassessed.”
Financial Analysts Journal, vol. 50, no. 5, 1994, pp. 76-78.
Brush, John S. “Comparisons and Combinations of Long and Long/Short Strate-
gies.” Financial Analysts Journal, vol. 53, no. 3, 1997, pp. 81-89.
Dadachanji, Naozer. “Market Neutral Long/Short Strategies: The Perception ver-
sus the Reality.” Presentation at the Q-Group Conference, La Quinta, Calif,
October 1995.
Freeman, John D. “Investment Deadweight and the Advantages of Long/Short
Portfolio Management.” VBA Journal, September 1997, pp. 11-14.
Jacobs, Bruce I. “The Long and Short on Long/Short.” Journal of Investing, vol. 6,
no. 1, Spring 1997, Presentation at the Q-Group Conference, La Quinta,
Calif, October 1995.
Jacobs, Bruce I., and Kenneth N. Levy. “More on Long-Short Strategies.” Financial
Analysts Journal, vol. 51, no. 2, 1995, pp. 88-90.
. “20 Myths about Long-Short.” Financial Analysts Journal, vol. 52, no. 5,
1996, pp. 81-85.
Jacobs, Bruce I., Kenneth N. Levy, and David Starer. “On the Optimality of Long-
Short Strategies.” Financial Analysts Journal, vol. 54, no. 2, 1998, pp. 40-51.
Kahn, Ronald N., and Andrew Rudd. “What's the Market for Market Neutral?”
BARRA Preprint, June 1998.
Levin, Asriel. “Long/Short Investing—Who, Why, and How.” In Enhanced Index
Strategies for the Multi-Manager Portfolio, edited by Brian Bruce (New York:
Institutional Investor, Inc., 1998).
Long/Short Investing
443
Michaud, Richard O. “Are Long-Short Equity Strategies Superior?” Financial Ana-
lysts Journal, vol. 49, no. 6, 1993, pp.44-49. Presentation at the Q-Group
Conference, La Quinta, Calif, October 1995.
Michaud, Richard O. “Reply to Arnott and Leinweber.” Financial Analysts Journal,
vol. 50, no. 5, 1994, pp. 78-80.
Pensions and Investments, May 18, 1998, and May 12, 1997, articles on market-
neutral strategies.
TECHNICAL APPENDIX
We will present the derivation of Eq. (15.14), the risk aversion
required to achieve a given level of risk.
We express utility in terms of risk as
U = aw) — Ag: wo
(15A.1)
Using Eq. (15.11), this becomes
=
{ha 100
1
U = 100-IR ;
T= yN)
We solve for the optimal level of risk by taking the derivative of
U with respect to w and setting the result equal to zero. We find
}
—)g:o*
(15A.2)
—y(N)
R-{1+ 72 Uh
Woylon
(15A.3)
This leads directly to Eq. (15.14).
de ee
a
ae
2
Cot
Sain
i ee
cote Perris ve spar ende
on
ob We peeve ol hey ARR
id
gid
etre! aay Vg
gil,
(ONG
tla
’
| hi
wacs
M eer wears
a’ a
m,
if
=
treme
tree
ae MORE
kT ahl
Pins eee
Se
“al
ee
Pee
~
coal
i =e a.
tn
Pi
TRS Soa lp
Xx Dee a
ear
SR
iy >
=
eine hate eres if
-
» az
‘
te TT ne a
:
}
/
;
46
Qaet
NY
Sees
air
wats!
Can
»,
ahs
iar ier ane
i,
ASF nie thee tndeanu gata
alee ahi.
| dees?
Fat
,
ounvied be Jtraty
a
~
F
Waste paid
ber
eee
wa
nat’ te a1
fee 8
i
Ho iak ek ‘oe
a
re
i
[
a View
te
1
=
:
;
z
rl
‘aa
UF ee Pa
fo U5.0o
Evel Tespuat bag ef bait i oY
tosis
galt)
is
‘
,
, he. bi is m 45
re i
i”
- -
a
é
4
ri
rh
