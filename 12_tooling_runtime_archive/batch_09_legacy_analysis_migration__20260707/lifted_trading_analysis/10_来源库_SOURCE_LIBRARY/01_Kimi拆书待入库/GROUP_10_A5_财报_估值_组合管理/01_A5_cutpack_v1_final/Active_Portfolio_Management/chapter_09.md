# Chapter 9: Valuation in Practice

- **book_name**: Active Portfolio Management
- **main_source**: pdf
- **cross_check_source**: none
- **pdf_role**: main_text_source
- **split_scope**: pages 247-282

---

CHAPTER
9
Valuation in Practice
INTRODUCTION
The previous chapter investigated the theory of valuation. That
theory has proved useful in valuing options, futures, and other
derivative instruments, but has yet to be used for the valuation of
equities. In this chapter, we will look at some of the quantitative
methods that have been used for equity valuation. These will be
ad hoc, although they will have some vague connection with theory.
The reader should not be surprised that the chapter does not de-
scribe a “right” way to value stocks. We described the theoretically
correct approach in the previous chapter. This chapter is evidence
of our inability to make the theoretically correct scheme operational.
We have to turn to more ad hoc schemes.
The reader should keep the humility principle in mind: The
marketplace may be right and you may be wrong. The reader
should also keep the fundamental law of active management in
mind: You don’t have to be right much more than 50 percent of
the time to add value! With these modest goals in mind we shall
commence.
Insights included in this chapter are:
a The basic theory of corporate finance provides ground
rules for acceptable valuation models.
= The standard valuation model is the dividend discount
model, which focuses on dividends, earnings, and
growth. Dividend discount models are only as good as
their growth forecasts.
225
226
Expected Returns and Valuation
SEO Ne
a
a a
ees
= Comparative valuation models price attributes of a firm.
= Returns-based analysis focuses directly on the ultimate
goal of valuation models: forecasting exceptional returns.
Returns-based analysis is related to APT models.
The goal is to find assets that are unfairly valued by the market,
hoping that the market will eventually correct itself. This requires
some insight. Quantitative methods can help to focus that insight
and use it efficiently, but they are not a substitute for insight.
CORPORATE FINANCE
The modern theory of corporate finance is based on the notion of
market efficiency. Modigliani and Miller showed the power of mar-
ket efficiency in their classic studies demonstrating that
® Dividend policy influences only the scheduling of cash
flows received by the shareholder. It is a “pay you now
or pay you later” arrangement. Dividend policy doesn’t
affect the total value of the payments.
# A firm’s financing policy does not affect the total value of
the firm. Financing policy will keep the total value of the
firm’s liabilities constant.
These ideas were extremely controversial at first, but they
have stood up for decades and are at least partially responsible for
the authors’ Nobel prizes. Active managers with market inefficiency
in their veins can read these two precepts as: “Dividend and financ-
ing policy aren’t very important.” Any valuation method that
hinges on some magic associated with dividends or debt financing
may be dangerous.
The economic value of a firm comes from its profitable a¢tivi-
ties. If the firm can transform inputs it buys for $1.00 into outputs
it sells 3 months later for $1.45, then the firm can profit. If the firm
can find additional projects that create value, then the firm can
grow. This ability to generate profits and to make those profits
grow is at the heart of attempts at valuing the firm. Much of the
confusion about the Modigliani and Miller results arises from two
issues: taxes and a failure to separate the operations of the firm
from its financing activities.
|
Valuation in Practice
227
Let’s ignore taxes for the moment. The failure to separate
operations from financial decisions is quite natural. A firm borrows
because it has capital expenditures that are needed to support future
growth. A firm increases its dividend because its operations have
been successful and future success is anticipated. We want to sepa-
rate the operational considerations (the new plant, the successful
product, etc.) from the financial. The new plant could have been
financed from either retained earnings (reduced dividends), sale
of new equity, or issuance of new debt. The benefits of the successful
product launch could be used to retire debt, kept as retained earn-
ings, or distributed as dividends. With the aid of the Modigliani
and Miller principles, we can consider the firm’s equity value as
stemming from two sources: operational value and financial value:
Stock value = financial value + operational value
(9.1)
In a simple context, the financial value is the difference between
the firm’s capital surplus and its debt. The capital surplus is any
money left after we have paid dividends and interest (if any) and
paid for new investments that are needed in order to grow or
sustain the operational side of the business.
The operational value is derived from the revenue from opera-
tions (excluding interest), less the cost of those operations (labor,
materials, and support, but not interest expense), and less the capital
costs of maintaining and augmenting the capital stock (plant, ma-
chines, research, etc.).
As an example, think of two firms operating side by side. The
widget side of the business builds widgets, sells widgets, and invests
in new and better widget-making equipment. The financing side of
the business pays interest, pays dividends, retains earnings, issues
(or repurchases) shares, and issues (or repurchases) bonds. If the fi-
nancial side of the business is net long (retained earnings plus paid-
in capital exceeds debt), then it invests the balance at the risk-free
rate. If the financing side is net short, then it pays interest on the
difference between the equity account and the bond account.
As Modigliani and Miller point out, value is created on the
widget side of the business. The financial side of the business moves
money through time and allocates shares of the operational value
between stock- and bondholders. A debt incurred today implies a
228
Expected Returns and Valuation
sequence of interest payments in the future. The present value of
those interest payments is equal to the present value of the debt.
Figure 9.1 shows the flows into and out of our prototype firm.
On the first level, we have the operating company. We call its output
the cash flow. The cash flow is an input to the financial company.
As we can see, the financial company pays dividends, pays interest
if there is a debt position, collects interest on the capital surplus
(if any), and either issues or repurchases dept and equity.
Figure 9.1 might be called the world according to Modigliani
and Miller. It is a conceptually useful way to look at the firm.
Unfortunately, accountants don’t share this view. Accounting infor-
mation is based on the aggregate of the operational and financial
sides of the firm. By adjusting dividend and debt policy, it is possible
to manipulate not only dividends and debt/equity ratios, but earn-
ings per share (EPS), the growth in EPS, earnings-to-price ratios,
and book-to-price ratios.
The reader should keep these Modigliani and Miller principles
in mind in conjuring up and evaluating valuation schemes. Most of
those schemes start with the notion of dividends. We'll start there too.
Operating Company
Cash Flow
Financial Company
Dividends
Interest
Figure 9.1
Valuation in Practice
229
THE DIVIDEND DISCOUNT MODEL
John Burr Williams, in his classic Theory of Investment Value, antici-
pated much of modern financial theory. In particular, Williams
stressed the role of dividends as a determinant of value in an early
version of the dividend discount model. An investor is paid for an
investment either through dividends or through the sale of the
asset. The sale price is based on the market’s assessment of the
firm’s ability to pay future dividends.
Other variables such as earnings may be important in valuing
a firm, but their importance is derived from their ability to predict
the future flow of dividends to the investor. So high current earnings
may signal the firm’s ability to increase dividends, and low current
earnings signal a possible future decrease in dividends, or at least
delays in future increases.
This emphasis on dividends appears to clash with the Modigli-
ani and Miller principle on dividend policy. This is not really the
case. You can read the Modigliani and Miller principle as “pay me
now or pay me later.” What Modigliani and Miller say is that the
firm is free to schedule the payment of the dividends to the investor
in any way it likes. The scheduling will not (or should not) affect
the market’s perception of the value of the firm.
The emphasis on dividends may also appear jarring to today’s
U.S. equity investors, conditioned to focus almost exclusively on
price appreciation, almost to the point of disdaining current divi-
dends. This wasn’t always the case. In the 1950s and earlier, divi-
dend yields exceeded bond yields. Equities are riskier than bonds,
so investors required added incentives to purchase equities, ac-
cording to the logic then. Even now, high-yield bonds follow
this trend.
Certainty
If p(0) is the price of the firm at time 0, i; is the per-period interest
rate, and d(t) is the certain dividend to be paid at time t, then both
Williams and our theoretical valuation formula would say that
da) , d2 ,
,
dt)
(Cie)
Ftp)
ia
(9.2)
p(O) =
230
Expected Returns and Valuation
ced
ee
ee
EE EE EE EE
Modigliani and Miller interpret this equation as both a valuation
formula (i.e., a definition of p(0)) and a constraint on dividend
policy [i.e., increasing d(1) by 1 dollar and decreasing d(2) by (1 +
ir) dollars will preserve the total value of the firm]. As we saw in
the preceding chapter, uncertainty complicates the analysis.
Uncertainty
We can capture uncertainty in the future dividends with a risk-
adjusted discount rate’ y called the dividend discount rate.
AIS rp reclOD, ee
hs
SLO
ca isp
(Deha)se Claeys oe Taian):
(+ yi
p(0) =
(9:3)
Equation (9.3) can serve as either a net present value formula
or an internal rate of return formula. In the net present value
application, we take the sequence of dividends d(t) and the dividend
discount rate y as given, and solve for the price p(0). Any discrep-
ancy between the model price p(0) and the market price would
imply an opportunity for exceptional return.
In the internal rate of return calculation, we take the sequence
of dividends d(t) and the price p(0) as given, and solve for the
dividend discount rate y. This internal rate of return—an expected
total rate of return given the dividends and the price—may also
imply an opportunity for exceptional return if it differs from the
consensus expected total return i; + B - fz. Later, we will return
to these two approaches and the connection between dividend
discount models and expected returns. We now confront the. big-
gest challenge presented by Eq. (9.3): the specification of the divi-
dend stream d(t). To start, we will consider the constant-growth
model.
‘Recall that in the previous chapter, we showed that the theoretically pure approach is to
keep the discount rates equal to the risk-free rate and “risk-adjust” the anticipated
cash flows.
Valuation in Practice
231
The Constant-Growth Dividend Discount Model
The constant-growth, or Gordon-Shapiro, dividend discount model
assumes that dividends grow at a constant rate g. In other words,
d(t) = d()- (1 + 9)
(9.4)
Substituting Eq. (9.4) into Eq. (9.3) and applying some algebra, we
find the simplified formula
d(1)
Uy = 49)
This is the fundamental result of the constant-growth dividend
discount model. Given a dividend d(1) and a growth rate g, the
stock price increases as the dividend discount rate decreases, and
vice versa. Low prices imply high dividend discount rates, and
high prices imply low dividend discount rates or high growth rates.
We will now consider another approach that leads to the same
destination and provides further insight into Eq. (9.5). We can split
the return on a stock into two parts, the dividend yield and the
capital appreciation:
p(0) =
(9.5)
ptr ab+e= ete )
(9.6)
where p = the price of the stock at the beginning of the period
p = the price of the stock at the end of the period
d = the dividend paid in the period (assumed to be paid
at the end)
ip = the risk-free rate of interest
r = the excess return
€ = the uncertain amount of capital appreciation
Let g = E{é} be the expected rate of capital appreciation, f = E{r}
be the expected excess return, and y = i; + f be the expected total
rate of return. Taking expected values, Eq. (9.6) becomes
pt faSteny
(9.7)
We are assuming that the dividend is known or that d represents
the expected dividend. We are also assuming that the expected
total rate of return over the period, ir + f, equals the internal rate of
232
Expected Returns and Valuation
nies
ener ee ee ee a
ee
ee
return y, which is the (constant) average return calculated over the
entire future stream of dividends.
Solving Eq. (9.7) for the price leads back to the constant-growth
dividend discount model result:
pape
BO
(y — g)
Equations (9.5) and (9.8) imply that the expected rate of capital
appreciation is identical to the expected rate of dividend growth.
So far, this is something of a tautology, since we have, in fact,
defined g to make this work. But we will next introduce a model
for growth g, to show that we can equate it to the expected rate
of capital appreciation.
p
(9.8)
MODELING GROWTH
We can use a simple model to show that the expected rate of capital
appreciation equals the growth in the company’s earnings per share
and the growth in the company’s dividends. Let
e(t) = earnings in period t
d(t) = dividends paid out at the end of period t
K = company’s payout ratio
I(t) = amount reinvested
p = return on reinvested earnings
and assume that the payout ratio k and reinvestment rate of return
p remain constant. In particular, assume that $1 of investment pro-
duces an expected perpetual stream of p dollars per period. Then,
earnings either flow into dividends or are reinvested:
e(t) = d(t) + I(t)
"(9.9)
The dividends constitute a fraction k of the earnings:
d(t) = « - e(t)
(9.10)
The reinvested earnings constitute the remaining fraction (1 — k)
of the earnings:
Id) = (1 — 0) e@)
:
(9.11)
Valuation in Practice
233
And, since reinvestment produces returns p, we can determine
e(t + 1) based on e(t) and the fraction reinvested:
et+1)=[1+(—x«)-p]-e(t)
(9,12)
Equation (9.12) simply states that next year’s earnings equal this
year’s earnings plus an increase due to the return on the portion
of this year’s earnings that was reinvested (the increase in equity).
Of course, e(t) and e(t + 1) lead to the growth rate:
et + 1) = (1 + g)- eff)
(9.13)
Therefore
g=(1-k)-p
(9.14)
and, as desired,
d(t) = d(1)-(1 + g)*!
(9,15)
The payout ratio is constant, and hence dividends are proportional
to earnings. Therefore, the dividend growth rate [in Eq. (9.15)] is
also the earnings growth rate [in Eq. (9.13)]. Moreover, this growth
rate is determined by both the reinvestment rate 1 — k (a measure
of opportunity) and the average return on reinvested capital p [from
Eq. (9.14)]. This average return on invested capital is, in turn, linked
to the return on equity. Suppose b(t) is the book value at time ft,
and we start with e(1) = p - b(0); then book value will grow at rate
gas well, and p willbe the constant return on equity: e(t) = p- b(t — 1).
Multiple Stocks
The more general form of the dividend discount model for multiple
stocks indexed by n = 1, 2,... Nis
p.(0) = >) Tee 7;
(9.16)
The multiple-stock version of Eq. (9.7) becomes
dy,
; Jt Qn = ip + iB = Yn
(9.17)
234
Expected Returns and Valuation
We can give this analysis some teeth by combining it with the
consensus expected returns. The expected return f, includes both
consensus expected returns’ and alphas: f, = 8, ° fg + o,. Substituting
into Eq. (9.17), we see that
St y= ie
+ Bro fot Ona I
(9.18)
We illustrate this relationship in Fig. 9.2, for a 4 percent risk-free
rate, a 6 percent expected excess return on the benchmark, and an
asset beta of 1.2. If the asset’s yield is 2.5 percent, then it will be
fairly priced, a, = 0, if the expected rate of capital appreciation is
8.7 percent.
Alphas versus Growth
15%
S
=
2h
& 20%
-
2
:
y
=
se
20%
Yield = 2.5%
=———-Yield=00%
Growth
Figure 9.2
’Here we will assume that the expected benchmark return f; matches the long-run
consensus expected benchmark return j1s; ie., we are assuming no benchmark
timing.
i
Valuation in Practice
235
If we solve Eq. (9.18) for alpha, then we have a simple model
for expected exceptional return in terms of yield, risk (as measured
by beta), and growth:
ene
Qa, = (é:
= |
te (2, _ B, : fe)
(O19)
This formula points out the most important insight we must keep
in mind while using a dividend discount model:
The Golden Rule of the Dividend Discount Model: g in, g out.
Each additional 1 percent of growth adds 1 percent to the alpha.
The alphas that come out of the dividend discount model are as
good as (or as bad as) the growth estimates that go in. If it’s garbage
in, then it’s garbage out.
Implied Growth Rates
We can use Eq. (9.19) in a novel way: starting with the presumption
that the assets are fairly priced, and determining the growth rates
necessary to fairly price the assets. We call these the implied
growth rates:
Eee
i -
(9.20)
We know the risk-free rate i, and we can estimate the beta and the
yield with reasonable accuracy. We can also make a reasonable
estimate of the expected excess return on the market fs.
The implied growth rates are handy in several ways. First
they provide a rational feel for what growth rates should be, and
help to point out consistent biases in analysts’ estimates, either
within sectors or across all stocks. Second, the implied growth rates
can identify companies whose prices reflect unrealistic growth
prospects.
For example, in Table 9.1 we have listed the Major Market
Index stocks along with their yield, 60-month historical beta, and
implied growth rates as of December 1992. The table assumes an
expected excess return on the Major Market Index, fe, of 6 percent
and uses the risk-free rate (3-month Treasury bills) of 3.1 percent,
which was the rate at the end of December 1992.
236
Expected Returns and Valuation
0
pee he
ee
ee
eee
TABLE
9.1
Stock
Implied Growth Rate
American Express
6.36%
AT&T
6.26%
Chevron
1.10%
Coca-Cola
7.80%
Disney
10.04%
Dow Chemical
5.26%
DuPont
5.94%
Eastman Kodak
1.80%
Exxon
1.22%
General Electric
8.06%
General Motors
6.00%
IBM
—2.66%
International Paper
7.56%
Johnson & Johnson
8.20%
McDonalds
8.72%
Merck
7.34%
3M
4.34%
Philip Morris
5.52%
Procter & Gamble
7.06%
Sears
4.94%
We can see that reasonable growth rates average about 5.5
percent and that the standard deviation of growth rates in the
Major Market Index is 3.1 percent. One of the difficulties in using
a dividend discount model is implicit in the Golden Rule: The
growth inputs can be wildly unrealistic. They tend to be too large
in general, since Wall Street research (which drives the consensus)
is interested in selling stocks, and positive bullish outlooks help
to sell stocks.
Dealing with Unrealistic Growth Rates
We can treat this problem of unrealistic growth estimates in three
ways. The first is a direct approach:
1. Group stocks into sectors.
Valuation in Practice
237
2. Calculate the implied growth rate for each stock in the
sector.
3. Modify the growth forecasts so that they have the same
mean and standard deviation as the implied growth
rates in each sector.
This approach linearly transforms the growth estimate g,, to
Snr =at+d-g,
(9.21)
where we choose a and b to match the mean and standard deviation
of the implied growth rates g%. The result is
Std{g*}
Std{g}
gn = Mean{g*} + (
- (g, — Mean{g*})
(i222)
where we calculate the mean and standard deviation cross-section-
ally over stocks in the sector. The revised growth estimates are the
sector average implied growth rate plus a term proportional to the
difference between the initial growth estimates and that sector
average implied growth rate.
Table 9.2 shows the results of this approach for the stocks in
the Major Market Index, using the 5-year historical earnings-
per-share growth rates (as of December 1992) as inputs. In this
table, we have treated all these stocks as one sector. Table 9.2 also
shows the alphas from Eq. (9.19), based on the modified growth
inputs.
One possible difficulty with this approach is that it may delete
valuable sector timing information. Remember that the implied
growth rates assume zero alphas, so this scheme will move the
sector alphas toward zero.’ If you have no sector timing ability,
then this is not a problem, but if you are trying to time sectors,
you must account for sector alphas when generating target mean
growth rates for each sector.
The second approach to dealing with unrealistic growth esti-
mates is a variant of the first approach which can, in principle,
Issues of coverage and capitalization weighting keep the sector alphas from exactly
equaling zero after this procedure.
238
Expected Returns and Valuation
Lh A
gee en er
ee
Se
ee ee
eee
TABLE
9.2
Stock
Growth Forecast
Modified Forecast
Alpha
American Express
—3.20%
4.90%
—1.46%
AT&T
—19.21%
2.21%
—4.05%
Chevron
3.18%
4.91%
3.81%
Coca-Cola
19.31%
8.68%
0.88%
Disney
12.18%
7.49%
—2.55%
Dow Chemicals
eS 2orweve
1.54%
3.1270
DuPont
—7.46%
4.19%
Werke
Eastman Kodak
—37.51%
—0.86%
—2.66%
Exxon
3.32%
6.00%
4.78%
General Electric
16.14%
8.15%
0.09%
General Motors
4.72%
6.23%
0.23%
IBM
—32.53%
—0.038%
2.63%
International Paper
—10.86%
3.62%
—3.94%
Johnson & Johnson
15.27%
8.01%
—0.19%
McDonalds
12.09%
7.47%
ilkZovo
Merck
22.95%
9.30%
1.96%
3M
4.48%
6.19%
1.85%
Philip Morris
22.92%
9.29%
3.77%
Procter & Gamble
23.30%
9.35%
2.29%
Sears
—7.96%
4.10%
—0.84%
Mean
0.58%
5.54%
-0.01%
Standard deviation
18.40%
3.09%
2.70%
account for the investor’s skill in predicting growth. As we will
discover in Chap. 10, a basic linear forecasting result is
gi =e t+c-(g, — g)
(9.23)
Unlike in Eq. (9.22), we start with the stock’s implied growth rate,
not the sector average, and shift away from it based on comparing
the initial growth forecast to the stock’s implied growth rate.
Furthermore, as we will learn in Chap. 10, the constant c
depends in part on the investor’s skill in predicting growth, where
we measure skill using the correlation between forecast and realized
Valuation in Practice
239
growth rates. With no skill, we set c to zero. We leave the details
to Chap. 10.
A third, more conventional and more elaborate, approach to
getting realistic growth inputs is the three-stage dividend dis-
count model.
THE THREE-STAGE DIVIDEND
DISCOUNT MODEL
The three-stage dividend discount model is built on the premise
that we may have some insights about a company’s prospects
over the short run (1 to 4 years), but we have little long-range
information. Therefore, we should use something like the implied
growth rate for the company (or the sector) as the long-run value,
and interpolate between the long and the short.
The idea stems from the initial dividend discount formula [Eq.
(9.3)], which would naturally lead one to distinguish between long-
range and short-range growth rates.
The three-stage dividend discount model is complicated. The
reader who is uninterested in the details can skip to the next subsec-
tion, where we comment (negatively) on the net effect of the three-
stage approach.
There are several ways to build a three-stage dividend discount
model. What follows is typical, and we don’t believe that different
model structures give materially different results. The required
inputs include the following:
T;, T, = times which define the stages—stage 1 runs from 0
to T,, stage 2 from T, to T,, and stage 3 from T;
onward
= the short-term (0 to T;) forecast growth in earnings
per share
8rq = the long-range or equilibrium (T, onward) forecast
growth in earnings per share
Ky = the current (0 to T;) payout ratio
Kg = the long-run (T, onwards) payout ratio
EPS(1) = the forecast of next year’s earnings per share
Yq = the equilibrium expected rate of return, JT B ip
o9 2 |
240
Expected Returns and Valuation
ian
nnere NEON ee eee by hater ah ne
We input the short-term and long-term growth forecasts. For
the growth during the intermediate period, we linearly interpolate:
chs
Pe
i uae
hy
gt) = gv (Z
¥ x]
+ 850 (4
i |
(9.24)
for T,; < t < T>. We similarly interpolate the payout ratios k(t).
Then the earnings per share and dividend paths will be
EPS(@) = [1 + ¢@)] > EPSG — 1)
(9:25)
d(t) = k(t)
- EPS()
(9.26)
We now proceed by first finding a time T, value of the company,
and then focusing on the current value of the company. At time
Tz, we can value the company using the equilibrium growth and
dividend discount rates:
d(T, + 1)
inten
(9.27)
p(T») TH
Then we can solve for the dividend discount rate y that discounts
to the current price p(0):
d(t)
—
p(T) _
p(0) = >
Gta
aye
(9.28)
The Three-Stage Dividend Discount
.
Model Evaluated
The entire three-stage dividend discount procedure is motivated
by the tension between a short-run growth rate gy and a long-run
rate gro. In spirit, it is just another approach to adjusting 9; toward
8rq and applying Eq. (9.3). A cynical view would even be that this
is an elaborate (and confusing) way to smooth the growth inputs.
It is important to remember that the three-stage dividend discount
Valuation in Practice
241
a
a
a ae
ee
ee ee ee
3%
Short Term Growth Forecast
Figure 9.3 Three stage dividend discount model. Alpha versus short term
growth forecast.
model is not magic. It cannot transform bad growth forecasts into
good growth forecasts. The golden rule still applies.
To understand this better, consider the following exam-
ple. We will set up a typical three-stage dividend discount
model’ and use it to estimate internal rates of return and alphas
(by subtracting i; + B - fz). Figure 9.3 illustrates the almost linear
relationship between gin and alpha. In this case, the implied
growth rate is 12.62 percent, and each additional 1 percent
of growth adds 0.54 percent to the alpha. The golden rule has
been modified slightly, to say “g in, 0.54
- (g — 12.62 percent)
out.”
We can apply the same analysis to observe the sensitivity
of alpha to the initial earnings per share forecast. Figure 9.4
illustrates the result. The relationship between the initial earn-
ings per share forecast and the alpha is slightly nonlinear; how-
ever, 30 basis points of alpha for each $0.20 of earnings per share
is a reasonable guide.
‘The parameters are 5 and 15 years for the stage times, 0.0 for the short-run payout, and
0.3 for the long-run payout. The long-run expected market excess return was 5.5
percent, the stock’s beta was 1.2, and the risk-free rate was 4 percent. This means
that the stock’s long-run fair expected return was 10.60 percent. The first year’s
EPS number was $4.80, and the market price was $50.00.
242
Expected Returns and Valuation
ciel eee
ee eS ee Ee
ee eee
$3.00
$3.50
l
:
:
K
‘
$6.50
Alpha
yoy
-1%
7
Initial Earnings per Share Forecast
-3
Figure 9.4 Three stage dividend discount model. Alpha versus initial earnings
per share forecast.
DIVIDEND DISCOUNT MODELS
AND RETURNS
To use a dividend discount model in the context of active portfolio
management, the information in the model must be converted into
forecasts of exceptional return. There are two standard approaches,
based on calculating either internal rates of return or net present
values. These approaches differ in their assumption of the horizon
over which any misvaluation will disappear.
In the internal rate of return mode, we use the stream of
dividends and the current market price as inputs, and solve for
the internal rate of return y which matches the dividends to the
market price. We then obtain asset alphas in two steps: first aggre-
gate the rates of returns y, to estimate the predicted benchmark
excess return fs,
fe ae
B te ip = a Yn * hen — tr
(9.29)
and then convert the internal rates of return to expected residual
returns:
O, — Uy
iets ae fe)
(9.30)
The underlying assumption is that the misvaluation of the asset
will persist; i.e., after 1 year, the proper discount rate will still be
Valuation in Practice
243
y, and not the “fair” rate i; + 8, - fs. To see this, we can verify,
using Eq. (9.3), that the expected total rate of return for the asset
will be y,, if we assume that y, remains constant. Mathematically,
Pn(1) aE d,(1) i AW) an
| p,0)
Yn
ol)
assuming
p,(1) = >
7
Tassie
(9.32)
The expected price in 1 year is simply the dividend stream from
year 2 on, discounted at the same internal rate of return y,. The
alphas from Eq. (9.27) presume that the mispricing will persist
indefinitely, and that one will continue to reap the benefits.
In the net present value mode, we take the stream of divi-
dends and a fair discount rate y, = if + B, ° fg as inputs, and
solve for the fair market price as we would for a net present
value calculation. We then compare this price to the current
market price, to determine the degree of overvaluation or under-
valuation. To convert these “pricing errors” into alphas, we could
use the following two-step process. First we adjust fs (and hence
y,) so that the aggregate fair market value of all the assets equals
the aggregate current market value of the assets. Second, assum-
ing that the pricing error disappears after 1 year, we define
alpha as
(lotdpAe Ba {ps4
(9:33)
x _
|pn(O,model) —
p,(O,market)
ee
»,(0,market)
or approximately as”
,(0,model) —
p,(0,market)
p,(O,market)
+ ~
One eS
(9.34)
The alpha forecast in Eq. (9.33) presumes that all of the misvaluation
‘For monthly alpha forecasts, Eqs. (9.33) and (9.34) differ by about a factor of 1.01.
244
Expected Returns and Valuation
eee
will disappear in 1 year. In fact, we derive Eq. (9.33) by defining
alpha using
» —
|PxQ) + dni) =
pn(O,market)
oa
ging tr
p,(O, market)
(9.35)
and assuming
d,(t)
=
So —_——_*__—
9.36
pu(1) rae
(9.36)
t=2
ie., the end-of-year price is the net present value of the future
stream of dividends, discounted at the fair rate ip + B,, - fp.
Beneficial Side Effects
of Dividend Discount Models
Beyond their possible value in forecasting exceptional returns, divi-
dend discount models also have some beneficial institutional side
effects. The dividend discount model is a process. Used properly,
it entails keeping records and viewing all assets on an equal footing.
Hence, it can identify the judgmental input to a portfolio. We can
compare the portfolio that the dividend discount model would have
purchased with the actual portfolio, and attribute the difference to
judgmental overrides and implementation costs (trading, etc.). In
the longer run, this process can lead to evaluation and improvement
of the inputs.
On the downside, total devotion to the dividend discount
model as the only appoach to valuation is a form of tunnel vision. In
the remainder of this chapter we will consider some other practical
approaches to valuation.
COMPARATIVE VALUATION
The theoretical valuation formula of Chap. 8 and the dividend dis-
count model look to future dividends as the source of value. There
is analternative, which involves looking at the current characteristics
of a company and asking if that company is fairly valued relative to
other companies with similar characteristics. The most obvious and
simple example compares companies solely on the basis of current
Valuation in Practice
245
price-earnings ratios. The Wall Street Journal provides these numbers
every day. A second example is the rules of thumb quoted by invest-
ment bankers: “Consulting firms sell for two times revenues,” “Asset
management firms sell for 5 percent of assets,” etc.
These examples are familiar, unidimensional (and possibly
static) approaches to valuation based on current attributes. Compar-
ative valuation, as we will describe it, is a more systematic and
sophisticated (multidimensional) application of this idea: pricing
by comparison with analogous companies, or as a function of sales
and/or earnings multiples. We will motivate’ this approach using
the dividend discount model as a starting point.
The “clean surplus” equation of accounting’ connects a com-
pany’s dividends, earnings, and book value according to
B= DE — I) ae)
ah)
(9.37)
where we measure the book values b(f — 1) and b(£) at the beginning
and end of period ¢ (running from ¢ — 1 to time ft), the earnings
e(t) accrue during period t, and the company pays the dividend
d(t) at the end.
We can use the dividend discount rate y to split earnings into
two parts: required and exceptional:
e(t) = y- b(t — 1) + e*(t)
(9.38)
Anticipating that these exceptional earnings e*(t) will die out gradu-
ally leads to
e*(t + 1) = 8- e*(t) + noise
(9.39)
where 8 < 1.
Now combine Eqs. (9.37), (9.38), and (9.39) to estimate
the expected dividend, which
is what the dividend discount
model requires:
A) =i cect) ae BO)) re sCL)a—= BCL)
(9.40)
AQ) =1.+ y) eb) +5 ~e4(1) —D@)
ADs
)oebG = Diekole eh)
‘In this case, “motivate” will involve a set of assumptions and logic leading to a formula,
rather than any rigorous derivation. We will then use the formula in an empirical
way.
7See Ohlson (1989) for an in-depth discussion.
246
Expected Returns and Valuation
le eee
Sena ree
en tbh)
ee
Now substitute this expected dividend stream into the dividend
discount model [Eq. (9.3)] to find (after some manipulation)
el) ]
(9.41)
ESS
1
‘ ad tad eer ee
Equation (9.41) expresses the current price as a linear combination
of anticipated earnings e(1) and current book value b(0). The coeffi-
cients are company-specific and depend on the dividend discount
rate and the persistence of exceptional earnings.
This particular derivation is motivation for a more general
application. In the general case, we would like to explain today’s
price p(0) in terms of several characteristics: earnings, book, antici-
pated earnings, cash flow, dividends, sales, debt, etc. The idea is
to use a cross-sectional comparison of similar companies and thus
isolate those that are overpriced or underpriced.
For example, suppose we wished to apply the ideas contained
in Eq. (9.41) to a group of similar medium-sized electrical utilities.
We are looking for coefficients c, and c, to fit
Pr(O) = C1 + b,(O) + Cz + e,(1) +
(9.42)
Starting from Eq. (9.41), the idea is that for these similar companies,
the coefficients should be identical, and so the pricing error e, will
identify misvaluations. The exact procedure for implementing Eq.
(9.42) could vary, from an ordinary least-squares (OLS) regression,
to a generalized least squares (GLS) regression that takes into ac-
count company prices, to a pooled cross-sectional and longitudinal
regression that looks at the relationship across time and across
assets.
In general, the goal of comparative valuation is to estimate
a relationship
Market.
fitted
price
=
price sachs
>
(9.43)
Valuation in Practice
247
where the fitted price depends upona
variety of company charac-
teristics. Equation (9.43) leads to an exceptional return fore-
cast of
fitted _ market
ag = —ftror_
_ price
price
(9.44)
market
market
price
price
presuming that the fitted price is more accurate than the market
price, and that the asset will move to the fitted price over the
horizon of the alpha.
We can provide an arbitrage interpretation of this comparative
analysis. Suppose we split the companies into two groups: the
overvalued companies (with market price exceeding fitted price)
and the undervalued companies (with market price less than fitted
price). We can then construct a portfolio of the overvalued compa-
nies and a portfolio of the undervalued companies with identical
attributes: e.g., the same sales, the same debt, and the same earnings.
This creates two megacompanies—call them OV and UV, respec-
tively—that are alike in all important attributes. However, we can
purchase megacompany UV more cheaply than megacompany OV.
Two “identical” companies selling for different prices is an arbi-
trage opportunity.
This comparative valuation procedure requires only current
and forecast information, e.g., current book value and anticipated
earnings, and thus is independent of the past. It is not an extrapola-
tion of historical data. It also is a high-tech way of mimicking
the investment banking valuation procedures, which are typically
grounded on multiples of sales and earnings. The hope is that the
set of characteristics in the model completely determines com-
pany valuations.
If the model omits some important attribute, the valuation
may be misleading: The pricing errors may measure just the missing
component, not an actual misvaluation. One example of a missing
factor might be brand value. If we ignored brand name value and
applied comparative valuation to a consumer goods sector, we
might find some companies that were overvalued on average over
248
Expected Returns and Valuation
time. This might not be an opportunity to sell, but rather the appear-
ance of brand value. One way to account for this would be to
compare current overvaluation or undervaluation to historical aver-
age valuations.
Comparative valuation is quite flexible in practice. We can
build separate valuation models for banks, mining and extraction
companies, industrials, electric utilities, etc. This can help us focus
on comparability within groups of similar companies.
RETURNS-BASED ANALYSIS
The linear valuation model described above can serve as a useful
introduction to returns-based analysis. The valuation model
made a link between a purported percentage pricing error (the
difference between the fitted and the current price divided by
the current price) and the future residual return. Why not attack
the problem directly and try to fit the price in a way that best
forecasts residual returns? Suppose company n has attributes
(earnings, dividends, book, sales, etc.) A,,(t) at time t. We might
try the following model to directly explain residual returns using
these attributes:
0,2) = Sy Ant) + git) + e,(€)
(9.45)
k
Equation (9.45) is one example of returns-based analysis. A more
typical returns-based analysis works with excess returns r,(t) rather
than the residual returns 6,(¢), and uses risk control factors to sepa-
rate residual and benchmark returns. Its basic form is similar to
Eq. (9.45):
‘
rit) = SY Xns(t) » b(t) + uy(E)
(9.46)
k=1
but here the company exposures X,,,(f) include both the attributes
A,,(t) and the risk control factors.
Equation (9.46) has the form of an APT model, as discussed
in Chap. 7. At the same time, Eq. (9.46) may be somewhat more
Valuation in Practice
249
flexible. According to Chap. 7, we can fairly easily find qualified
APT models—any factor model that can explain the returns to
a diversified portfolio should probably do. But Eq. (9.46) could
include all the APT model factors as risk factors, plus a new
signal to forecast specific returns from that APT model. The
APT theory doesn’t allow forecasting of specific returns. But
we are now in the ad hoc, empirical, nonefficient world of ac-
tive management. We have the flexibility to forecast specific
returns [although in Eq. (9.46) we express that forecast as an-
other factor].
There are three important points to note concerning the use
of the linear model [Eq. (9.46)] to forecast returns. First, in a true
GLS regression, the factor return b,(t) is the return on a factor portfolio
with unit exposure to factor k, zero exposure to the other factors,
and minimum risk. If we know the exposures X,,,(t) at the start of
the period, even without knowing the returns r,(t), we can deter-
mine the holdings in the factor portfolio at the start of the period
necessary to achieve the factor return b,(t).
Second, the equations aggregate. In particular, looking at the
benchmark return,
a(t) = > xpx(E) > b(t) + up(t)
(9.47)
k
where
xai(t) = DS) healt) * Xna(t)
(9.48)
We will utilize this linear aggregation property to help separate
residual from benchmark returns.
Third, when estimated using least-squares regression, the lin-
ear model [Eq. (9.46)] can be unduly influenced by outliers. One
rule of thumb is to pull in all outliers in the X,,(f) to +3 standard
deviations about the mean. This will help avoid having all the
explanatory power arise out of only one or two (possibly sus-
pect) observations.
The simplest approach to separating residual from benchmark
returns is to model the residual returns directly, as in Eq. (9.45).
250
Expected Returns and Valuation
ON 8
ee ee
eee
es
Even then, we should be careful. The aggregate equation for the
benchmark is
On() = >) api( #) > gilt) + ex(t)
(9.49)
k
where
apx(t) = >) h(t) + Analt)
(9.50)
Since 0,;(t) = 0, we should adjust® the variables A,,(t) so that
ap(t) = 0.
In the more typical situation where we are modeling excess
returns, to separate benchmark from residual returns, we must
include one or more variables that will pick up the benchmark
return. The simplest approach is to include predicted beta as a
risk control factor, and make sure that all other characteristics
have a benchmark-weighted average of zero. The factor return
associated with predicted beta will tend to pick up the bench-
mark return, leaving the other factors to describe residual re-
turns.
A more complicated procedure is to include a group of
industry or sector variables as risk control factors. The factor
returns associated with these industry or sector variables will pick
up the benchmark effect.’? These industry or sector assignments
add up to an intercept term in the regression. To separate bench-
‘If Z,,(t) is the raw description of the exposure of asset n to attribute k at time t, and
Zau(t) = DY Aanlt) > Zeal)
is the benchmark exposure to attribute k at time t, then replace Z,,(t) with
®
Anil) = Zajlt) — Ze,(8)
If the beta of asset 7 is B,(t), then a slight variant is to replace Z,,,(t) with
Anx(t) = Zyxlt) — Bn(t) > Zax(6)
*The remaining factor portfolio returns may still be correlated with the benchmark, even
if the benchmark’s exposure to the factor is zero. For example, factors associated
with volatility (even after adjusting for market neutrality) tend “2
PIV Ae strong
positive correlation with the market.
Valuation in Practice
251
mark from residual returns, the choice’ is between a beta and an
intercept term.
Using Returns-Based Analysis
Once set up, returns-based analysis examines past returns and
attributes those returns to firm characteristics. The active manager
starts the process by searching for appropriate characteristics. Some
characteristics might directly explain residual returns—for exam-
ple, alpha forecasts from dividend discount models or comparative
valuation models. Other characteristics include reversal effects (e.g.,
last month’s realized residual returns), momentum effects (e.g.,
the past 12 months’ realized returns), earnings surprise effects, or
particular accounting variables possibly connected with excep-
tional returns." In this case, the hope is that the factor returns b,(¢)
associated with these characteristics exhibit consistent positive
returns.
Alternatively, the manager could choose characteristics associ-
ated with investment themes, sometimes in favor and sometimes
not—for example, growth forecasts or company size. Then the asso-
ciated factor returns b,(f) would not consistently exhibit positive
returns, but the manager would hope to forecast the sign and
magnitude of these returns. For example, how will growth stocks
or small-capitalization stocks perform relative to the market as a
A word of caution if you try to include both betas and an intercept (or sectors or
industries). There will be no problem with the factor portfolios that have
benchmark-neutral attributes. Those factor portfolios will have both a zero beta
and zero net investment. The difficulty is that the benchmark return will be
spread between the beta factor and the intercept. We can avoid this confusion by
introducing an equivalent regression. Suppose Z,,;(t) is the allocation of company
n to sector k and:
Zylt) = >) Hanlt) + Znslt)
n=1
is the benchmark exposure to sector k at time t. If we substitute
Xnxt) = Zny(E) — Bult) + Zab)
for Z,,,(t), we can interpret the factor portfolio returns as the residual (the factor
portfolio’s beta will be zero) return on sector k when we control for the other variables.
The returns to the benchmark-neutral factors will not change.
"For examples, see Ou and Penman (1989) and Lev and Thiagarajan (1993).
252
Expected Returns and Valuation
whole? These forecasts might rely on extrapolations of past factor
returns, e.g., using moving averages. More sophisticated forecasting
might use economic indicators such as long and short interest
rates, changes in interest rates, corporate bond spreads, or average
dividend yields versus interest rates.
Sometimes the manager may wish to forecast factor returns
even for characteristics that generally exhibit consistent positive
factor returns. For example, the BARRA Success factor in the United
States,
a momentum factor, generally exhibits positive returns.
However, these returns are often negative in the month of January.”
Managers who wish to bet on momentum should take into account
(forecast) this January effect.
Managers can of course combine these different types of sig-
nals, forecasting factor returns for investment themes as well as
using company-level valuation models. The relative emphasis will
depend on the information ratios associated with these various
efforts. Chapter 12, “Information Analysis,” and Chap. 17, “Perfor-
mance Analysis,” describe this research and evaluation effort in
more detail. Chapters 10 and 11, which cover forecasting, will
greatly expand on the technical issues surrounding forecasting of
returns. The notes section of this chapter includes a list of popular
investment signals.
SUMMARY
This chapter began with a discussion of corporate finance, to moti-
vate the development of valuation models based on appropriate
corporate attributes. It then discussed dividend discount models
in considerable detail, especially the critical issues of dealing with
growth and expected future dividend payments, and converting
information from the dividend discount model into exceptional
return forecasts. The chapter went on to empirically expand’ the
dividend discount concept with comparative valuation models, less
rigorous in principle but more flexible in practice. The chapter
ended with a discussion of returns-based analysis—which focuses
“We attribute this to investors’ tendency to “window dress” portfolios by keeping
winners for the year-end and selling losers in December, and to accelerate capital
losses (take them in December) and postpone capital gains (take them in January).
Valuation in Practice
253
directly on forecasts of exceptional return— and alternative empiri-
cal approaches that are available.
NOTES
Given the nature of active management, we can’t provide recipes
for finding superior information. Hence, this chapter has focused
on structure and methodology. But we can provide some indication
of what types of information U.S. equity investors have found
useful in the past. According to an annual survey of institutional
investors conducted by Merrill Lynch, these factors, attributes, and
models include
EPS variability
Return on equity
Foreign exposure
Beta
Price/earnings ratios
Price/sales ratios
Size
Earnings estimate revisions
Neglect
Rating revision
Dividend yield
EPS momentum
Projected growth
Low price
Duration
Relative strength
EPS torpedo
Earnings estimation dispersion
Debt/equity ratio
EPS surprise
DDM
Price/cash flow ratios
Price/book ratios
254
Expected Returns and Valuation
oe
ee
Se ee
Se i eee
eee
Most investors responding to the survey relied on five to seven of
these factors. See Bernstein (1998) for details.
PROBLEMS
1. According to Modigliani and Miller (and ignoring tax
effects), how would the value of a firm change if it
borrowed money to repurchase outstanding common
stock, greatly increasing its leverage? What if it changed
its payout ratio?
2. Discuss the problem of growth forecasts in the context of
the constant-growth dividend discount model [Eq. (9.5)].
How would you reconcile the growth forecasts with the
implied growth forecasts for AT&T in Tables 9.1 and 9.2?
3. Stock X has a beta of 1.20 and pays no dividend. If the
risk-free rate is 6 percent and the expected excess market
return is 6 percent, what is stock X’s implied growth
rate?
4, You are a manager who believes that book-to-price
(B/P), earnings-to-price (E/P), and beta are the three
variables that determine stock value. Given monthly
B/P, E/P, and beta values for 500 stocks, how could you
implement your strategy (a) using comparative
valuation? (b) using returns-based analysis?
5. A stock trading with a P/E
ratio of 15 has a payout ratio
of 0.5 and an expected return of 12 percent. What is its
growth rate, according to the constant-growth DDM?
REFERENCES
Bernstein, Peter L. “Off the Average.” Journal of Portfolio Management, vol. 24, no.
171997, Dac:
<
Bernstein, Richard. “Quantitative Viewpoint: 1998 Institutional Factor Survey.”
Merrill Lynch Quantitative Publication, Nov. 25, 1998.
Brennan, Michael J. “Stripping the S&P 500 Index.” Financial Analysts Journal, vol.
04, no. 1, 1998, pp. 12-22.
Chugh, Lal C., and Joseph W. Meador. “The Stock Valuation Process: The Analyst's
View.” Financial Analysts Journal, vol. 40, no. 6, 1984, pp. 41-48.
Durand, David. “Afterthoughts on a Controversy with Modigliani and Miller,
plus Thoughts on Growth and the Cost of Capital.” hed Management,
vol. 18, no. 2, 1989, pp. 12-18.
Valuation in Practice
255
Fama, Eugene F.,, and Kenneth R. French. “Taxes, Financing Decisions, and Firm
Value.” Journal of Finance, vol. 53, no. 3, 1998, pp. 819-843.
Fouse, William. “Risk and Liquidity: The Keys to Stock Price Behavior.” Financial
Analysts Journal, vol. 32, no. 3, 1976, pp. 35-45.
. “Risk and Liquidity Revisited.” Financial Analysts Journal, vol. 33, no. 1,
1977, pp. 40-45.
Gordon, Myron J. The Investment, Financing, and Valuation of the Corporation (Home-
wood, Ill.: Richard D. Irwin, 1962).
Gordon, Myron J., and E. Shapiro. “Capital Equipment Analysis: The Required
Rate of Profit.” Management Science, vol. 3, October 1956, pp. 102-110.
Grant, James L. “Foundations of EVA for Investment Managers.” Journal of Portfolio
Management, vol. 23, no. 1, 1996, pp. 41-48.
Jacobs, Bruce I., and Kenneth N. Levy. “Disentangling Equity Return Opportuni-
ties: New Insights and Investment Opportunities.” Financial Analysts Journal,
vol. 44, no. 3, 1988, pp. 18-44.
. “Forecasting the Size Effect.” Financial Analysts Journal, vol 45, no. 3, 1989,
pp. 38-54.
Lev, Baruch, and S. Ramu Thiagarajan. “Fundamental Information Analysis.”
Journal of Accounting Research, vol. 31, no. 2, 1993, pp. 190-215.
Modigliani, Franco, and Merton H. Miller. “Dividend Policy, Growth, and the
Valuation of Shares.” Journal of Business, vol 34, no. 4, 1961, pp. 411-433.
Ohlson, James A. “Accounting Earnings, Book Value, and Dividends: The Theory
of the Clean Surplus Equation (Part I).” Columbia University working paper,
January 1989.
Ou, Jane, and Stephen Penman. “Financial Statement Analysis and the Prediction
of Stock Returns.” Journal of Accounting and Economics, vol. 11, no. 4, Novem-
ber 1989; pp. 299-329.
Rosenberg, Barr, Kenneth Reid, and Ronald Lanstein. “Persuasive Evidence of
Market Inefficiency.” Journal of Portfolio Management, vol. 11, no. 3, 1985,
. 9-17.
ne Michael S. “The Three-Phase Dividend Discount Model and the ROPE
Model.” Journal of Portfolio Management, vol. 16, no. 2, 1989, pp. 36-42.
Sharpe, William F., and Gordon J. Alexander. Investments (Englewood Cliffs, N.J.:
Prentice-Hall, 1990).
Wilcox, Jarrod W. “The P/B-ROE Valuation Model.” Financial Analysts Journal,
vol. 40, no. 1, 1984, pp. 58-66.
Williams, John Burr. The Theory of Investment Value (Amsterdam: North-Holland
Publishing Company, 1964).
TECHNICAL APPENDIX
This technical appendix will discuss how to handle nonlinear mod-
els and fractiles in the (linear) returns-based framework. The idea
will be to capture the nonlinearities in the exposures to linearly
256
Expected Returns and Valuation
en
een neeneenn st ease ee ees oe
fe
ee eee
estimated factors. We can even make these exposures bench-
mark-neutral.
Let’s start with an example. Suppose you think that the rela-
tionship between earnings yield and return is not linear. Here is
one approach to testing that hypothesis. Divide the assets into three
categories, high earnings yield, low earnings yield, and average
earnings yield,’* and consider two earnings yield variables, high
yield and average yield. So the model is
oF =a X hich
; Drigh i G ave
- (pee
(9A.1)
The high-earnings-yield assets have X, nigh = 1 and X,ave = 0. The
average-earnings-yield assets have Xnhien = O and Xyave = 1. We
can determine the exposures of the low-yield assets by imposing
benchmark neutrality. Assuming that each group has equal capital-
ization, the condition 8; = 0 leads to
Diow = a Urign az Disie)
(9A.2)
So for the low-yield assets, we must have X,, high = —1and Xj ave = —1.
Once we estimate the factor returns, we can determine whether
there exist any nonlinearities. For example, one sign of a nonlinear
effect would be the return to the high-yield assets relative to the
average assets differing significantly from the return of the low-
yield assets relative to the average assets.
We can clearly extend this approach to quartiles, quintiles, or
deciles. In fact, this returns-based fractile analysis has the advantage
of allowing for controls. We can make sure that each fractile portfo-
lio is sector- and/or benchmark-neutral, and perhaps neutral on
some other dimension that we believe may be confounding the
effect.
Other methods for analyzing nonlinear effects also exist. Let’s
start with an attribute X,, that is benchmark-neutral: > hz, -
Xn; = 0. We wish to analyze nonlinearities while still ensuring
“The choice of three categories is arbitrary, and mainly done for ease of explanation. If
we considered four categories, this would be quartile analysis. As in quartile
analysis, we also have a choice in how to form the group: equal number in each
group or equal capitalization in each group.
~
Valuation in Practice
257
benchmark neutrality.
A simple approach is to include a new
variable:
Xn2 ae x? rae > he n . xX,
(9A.3)
The squared exposure has the disadvantage of placing undue em-
phasis on outliers. Other alternatives would include using the abso-
lute value of X,,;, the square root of the absolute value of X,,;, or
the Max{0, X,,;}, in each case benchmark-neutralized as in Eq. (9A.3).
Each of these would reduce the nonlinear effect for the more ex-
treme positive and negative values of X,,;.
Exercise
1. You forecast an alpha of 2 percent for stocks that have
E/P above the benchmark average and IBES growth
above the benchmark average. On average, what must
your alpha forecasts be for stocks that do not satisfy
these two criteria? If you assume an alpha of zero for
stocks which have either above-average E/P or above-
average IBES growth, but not both, what is your average
alpha for stocks with E/P and IBES growth both below
average?
Applications Exercise
1. Use appropriate software (e.g. BARRA’s Aegis and
Alphabuilder products) to determine the current
dividend-to-price ratio, dividend growth, and beta (with
respect to the CAPMMI) for GE and Coke. Using these
data, a risk-free rate of 6 percent, and expected
benchmark excess return of 6 percent, what are the
prices implied by the constant-growth DDM? What is
the dividend discount rate? Estimate alphas for GE and
Coke using both methods described in the section
“Dividend Discount Models and Returns.”
iy)
dy
opines hid i
'
ad
Nad al gy ng) ihial
.
.
‘Vitel ‘glee
wh tah 5 arit Lheveseete :
,
|
.
ris do tied itn” ited Hay
|S.
Setesulbms
par
tem
ag et ai
eS
a
ee
x*
leet
apy Casa
:
pe
hl nh
esti
sree
a tal rt
oe eee
‘
.
wy
7
SEIT
hi
tere EMA
We ag ‘atl
i"
(
i
7 iey
*
he
4
: 7”
a ether
Ip
;
j
a
a
ure
i
:
—
U
Jf
Ae
fi ee if i. remy
——
:
pe
N mt
' y
i a) ? a tes Lat |,
ee
mire MS
cS
pay
]
at Laieu'es
SE
ead
Aa pede NS
PiAL
tJ
i
yagi nee sf 4c Srl
i 7 wa
=
P
4
i
¥i
mi?
Oty (qe
ee
Se
wae
er
rity he "yay
=" 43,
—
.
nig
j
*4i5 aie
a
Lh:
gir
|
oar
ha
~~”
-)
7
|
>
ea
athe nt iat
‘Veal
at) nu
ve
+ 4c.
Mie
Meu Na
~
mein
? ies
—
a
“
:
‘ ev
%
j
~
4: "aha
=
‘
ik
a>
.
Je
=
ety ESS s wa
i
i.
ie -.
pik
7 fe v
.
vi
hiv
|
eile h
OY wn an
sad
oo
ay
459 a
WG Cab tars , erie
=< Hiv?
Bese)
|
oa
AP)
EAL)
‘ ALY
, ener | hi ate
sk
i?
a
EY Ur
ate Aye Sat, 1 . ,
ii
a
Pe
Pe
a
97 Aa? &
i
42
{
Dy,
’
aaet
ait
nee
iy &
ih
lia
‘
a
yA re see Wane
HHI
nay
i
pehetin
tev
HT WYe ean aaal ae wel
Ml
‘
:
‘
yer
oy tage
wigs be ce ts adja
li
odieeh alesis ual ale aateee
L
.
ji
soil Wunhoadt tainty”
; me
PART
THREE
Information Processing
