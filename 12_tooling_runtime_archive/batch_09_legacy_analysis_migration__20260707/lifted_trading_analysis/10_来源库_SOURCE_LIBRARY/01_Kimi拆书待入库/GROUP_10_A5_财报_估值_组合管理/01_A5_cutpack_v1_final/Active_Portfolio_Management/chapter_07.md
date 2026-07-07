# Chapter 7: Expected Returns and the Arbitrage Pricing Theory

- **book_name**: Active Portfolio Management
- **main_source**: pdf
- **cross_check_source**: none
- **pdf_role**: main_text_source
- **split_scope**: pages 195-220

---

CHAPTER
7
SB
a SN
EE
Expected Returns and the
Arbitrage Pricing Theory
INTRODUCTION
We have now completed our treatment of fundamentals. The next
three chapters cover expected returns and valuation.
The arbitrage pricing theory (APT) is an interesting and power-
ful alternative to the CAPM for forecasting expected returns. This
chapter describes the APT and emphasizes its implications for ac-
tive managers. The conclusions are:
# The APT is a model of expected returns.
= Application of the APT is an art, not a science.
= The APT points the quantitative manager toward the
relationship between factors and expected returns.
= APT factors can be defined in a multitude of ways. These
may be fundamental, technical, or macro factors.
= The flexibility of the APT makes it inappropriate as a
model for consensus expected returns, but an appropriate
model for a manager’s expected returns.
® The APT is a source of information to the active manager.
It should be flexible. If all active managers shared the
same information, it would be worthless.
The APT requires less stringent assumptions than the CAPM
and produces similar results. This makes it sound as if the APT is
a dominant theory. The difficulty is that the APT says that it is
possible to forecast expected stock returns but it doesn’t tell you
173
174
Expected Returns and Valuation
i So ee Bee
re eee ee
EE
eee
how to do so. It has been called the “arbitrary” pricing theory for
just this reason. The CAPM, in contrast, comes witha
user’s manual.
The APT states that each stock’s expected excess return is
determined by the stock’s factor exposures. The link between the
expected excess return and the stock factor exposures is described
in Eq. (7.2). For each factor, there is a weight (called a factor forecast)
such that the stock’s expected excess return is the sum over all the
factors of the stock’s factor exposures times the factor forecasts.
The theory doesn’t say what the factors are, how to calculate
a stock’s exposure to the factors, or what the weights should be in
the linear combination. This is where science steps out and art
steps in.
In discussing the APT, one should be careful to distinguish
among
= Stories that motivate the APT. These usually involve basic
economic forces that alter the relative valuation of stocks.
The motivating stories may mislead some people into
thinking that it is necessary for the APT to be based on
exogenous macroeconomic factors. The applications
described in this chapter indicate that this is not the case.
= Attempts to implement the APT. The APT is by nature
arbitrary. Different individuals’ attempts to implement it
will take different forms. One should not confuse a
particular implementation with the theory.
# The theory. The technical theory has evolved since its
origins in the mid- to late 1970s. This chapter will
provide an idiosyncratic view of the theory. Other ways
to look at the APT are cited in the chapter notes.
This chapter will first detail some weaknesses of the CAPM
that the APT was designed to correct. It will then describe the APT
and its evolution as a theory. The final sections of this chapter will
deal with the problem of implementation and give some examples
of ways in which people either have tried or could try to implement
APT models.
TROUBLE WITH THE CAPM
The CAPM is based on the notion that the market portfolio is
not only mean/variance-efficient but, in fact, the fully invested
Expected Returns and the Arbitrage Pricing Theory
175
portfolio with the highest ratio of expected excess return to volatil-
ity. In practice, the theory has been applied to say that common,
broad-based stock indices are efficient: the S&P 500 in the United
States, the FTA in the United Kingdom, and the TSE1 in Japan.
If we consider a broader notion of the market, including all
bonds, international investments, and other assets such as precious
metals, real property, etc., then we can see that the market consists
of more than the local stock index. Even if the CAPM is true in
some broader context of a worldwide portfolio, it cannot be valid
in the restricted single-market world in which it is ordinarily ap-
plied. All of the other assumptions underlying the CAPM (mean/
variance preferences, identical expectations of mean and variance,
no taxes or transactions costs, no restrictions on stock positions, etc.)
can be challenged, adding additional wounds. The most grievous of
these is the CAPM requirement that all participants know every
stock’s expected excess return. This assumption should be viewed
in the context of our quest to get a handle on the expected excess
returns in the first place! Thus we would suspect that the CAPM
can be only approximately true. It provides a guideline that should
be neither ignored nor taken as gospel.
One dramatic episode that points out the weakness of the
CAPM occurred for U.S. equities in 1983 and 1984, during a period
characterized by a considerable drop in interest rates. The equities
most adversely affected had high betas, and the equities most bene-
ficially affected had low betas.
We can illustrate this episode by a simple experiment. In De-
cember 1982, take the stocks in the S&P 500, order them according
to their predicted beta, and form ten portfolios, each with an equal
amount of capitalization. Portfolio 1 has the lowest-beta stocks,
portfolio 2 the next lowest group, and so on, with portfolio 10
holding the highest-beta stocks. Then follow the capitalization-
weighted returns on these portfolios for the next 24 months. It
turns out that over the out-of-sample period, the predicted betas
were excellent forecasts of the realized betas. No problem here. In
Fig. 7.1, we see the scatter diagram of predicted versus realized beta.
The regression line in Fig. 7.1 has a slope of 0.93, and the R? of
this regression was 0.89. The prediction of beta was quite accurate.
The CAPM would say that the alpha of each portfolio should
be zero. It didn’t turn out that way. Not only were several of
176
Expected Returns and Valuation
a Ee
Sar eS ee Se
Predicted
Beta
“0.0
0.2
0.4
0.6
0.8
1.0
1.2
1.4
1.6
Realized Beta
Figure 7.1
the alphas significantly different from zero, they were perversely
related to the portfolio betas. The results are shown in the scatter
diagram in Fig. 7.2.
Remember that we already checked our predictions of beta
and found that they were quite accurate. The explanation for this
event must lie elsewhere. Something, most likely changes in interest
rates and changes in inflationary expectations, was making higher-
beta stocks have negative residual returns and lower-beta stocks
have higher residual returns.’ This pattern was common throughout
the early 1980s.
There are periods in which CAPM predictions of expected excess
returns appear to have systematic defects.
"
This episodic evidence is meant to be suggestive, not to dash
the CAPM once and for all. In fact, financial statisticians have
'This points out the hazards of benchmark timing by tilting the portfolio toward higher-
beta stocks. The market was up considerably over this period; however, higher-
beta stocks had relatively bad results. Benchmark timing with futures would have
been much more effective, since it did not entail a residual bet’on the high-beta
stocks.
Expected Returns and the Arbitrage Pricing Theory
177
0.80%
0.60%
0.40%
0.20%
0.00%
0
-0.20%
-0.40%
Realized
Alpha
-0.60%
-0.80%
-1.00%
-1.20%
Realized Beta
Figure 7.2
thrown considerable empirical sophistication into attempts to prove
or disprove the validity of the CAPM, without coming to any hard-
and-fast conclusions.” Those efforts should be enough to convince
the investor to value the notion that the market plays a central—
indeed, the most important—role in the formation of expected
returns. However, the example should be enough to convince you
that it is worthwhile to look for further explanations.
THE APT
The APT postulates a multiple-factor model of excess returns. It
assumes that there are K factors such that the excess returns can
be expressed as
K
sO Graal iar
(7.1)
k=1
*Most recently, Fama and French (1992) have attempted to discredit the CAPM, with
considerable publicity. However, as described in Black (1993) and Grinold (1993),
these results require careful scrutiny.
178
Expected Returns and Valuation
where X,,, = the exposure of stock n to factor k. The exposures are
frequently called factor loadings. For practical
purposes, we will assume that the exposures are
known before the returns are observed.
b, = the factor return for factor k. These factor returns
are either attributed to the factors at the end of the
period or observed during the period.
u, = stock n’s specific return, the return that cannot be
explained by the factors. It is sometimes called the
idiosyncratic return to the stock.
We impose very little structure’ on the model. The astute reader
will note that the APT model, Eq. (7.1), is identical in structure to
the structural risk model, Eq. (3.16). However, the focus is now on
expected returns, not risk.
The APT is about expected excess returns. The main result is
that we can express expected excess returns in terms of the model’s
factor exposures. The APT formula for expected excess return is
K
fa = Elta) = DS) Xnx > my
(7.2)
k=1
where m, is the factor forecast for factor k. The theory says that a
correct factor forecast will exist. It doesn’t say how to find it.
The APT maintains that the expected excess return on any stock is
determined by that stock’s factor exposures and the factor forecasts
associated with those factors.
EXAMPLES
We can breathe some life into this formula by considering a few
examples. The CAPM is the first example. For the CAPM, we have
one factor, K = 1. The stock’s exposure to that factor is the stock’s
beta; i.e., X,,; = B,. The expected return associated with the factor
is m, = E{ru} = fw the expected excess return on the market.
*We assume that the specific returns u(n) are uncorrelated with the factor returns b(k);
i.e., Cov{b(k),u(n)} = 0. In most practical applications, we assume that the specific
returns are uncorrelated with each other; i.e., Cov{u(n),u(m)}
= 0 if m # n;
however, we do not need this second assumption for the theory to hold.
Expected Returns and the Arbitrage Pricing Theory
179
The second example is more substantial. We first classify stocks
by their industry membership, then look at four other attributes
of the companies. These attributes are chosen for the purpose of
example only. (Why these attributes, and why defined in just this
way? That question reinforces the notion that the APT model will
be in the eye of the model builder. It will be as much a matter of
taste as anything else.) The four attributes selected are
# A forecast of earnings growth based on the IBES
consensus forecast and past realized earnings growth
= Bond beta: the response of the stock to returns on an
index of government bonds
# Size: the natural logarithm of equity capitalization
® Return on equity (ROE): earnings divided by book
The four attributes include a forecast (earnings growth), a
macroeconomic characteristic (bond beta), a firm characteristic
(size), and a fundamental data item (return on equity).
It is easier to make comparisons across factors if they are all
expressed in the same fashion. One way to do this is to standardize
the exposure by subtracting the market average from each attribute
and dividing by the standard deviation. In that way, the average
exposure will equal zero, roughly 66 percent of the stocks will have
exposures running from —1 up to +1, and only 5 percent of the
stocks will have exposures above +2 or below —2. Table 7.1 displays
the primary industry, standardized exposures to these four factors,
and predicted beta for the 20 stocks in the Major Market Index as of
December 1992. Note that these exposures are standardized across a
broad universe of over 1000 stocks, so, for example, the size factor
exposures for the Major Market Index stocks are all positive.
The APT forecast is based on the factor forecasts for the four
factors and a forecast for the chemical industry. The factor forecasts
are 2.0 percent for growth, 2.5 percent for bond beta, —1.5 percent
for size, and 0.0 percent for return on equity. (These forecasts are
for illustration only.) We think that growth firms will do well,
interest-rate-sensitive stocks (which are usually highly leveraged
firms) will do well, smaller stocks will do well, and return on equity
will be irrelevant. In addition, we forecast 8 percent for the chemical
industry, and 6 percent for all other industries.
ve O0—
ce
0-
Oi Os
oo
0—
vO'0—
SEO
=
cl
O-
€c0—-
LS°0
VL
ve
0—
(=
605
Ol'O—
v90—
EL
0
c0'0—
€S'0—
9F0-—
Zt0
ymol
salojs jueuUedeq
sjonpoid
swoyH
oo0eqolL
JBdIWaYyd
s6nuig
jueine|sey
sjonpoid
jeolpayy
jeded pue sjonpoid }se104
ayempuey Jayndwog
S9}DIYSA JOO/\|
jeoujoaja Aneoy
uononpoid
pue
sesuesei
Afseug
a/nsis7
JESIWAYD
JBSIWSYD
jugwUleya}Uy
abeianeq pue pooy
uononpoid
pue
saviases
ABsoug
sauoudeyay
saolas
jeloueul4
Aaysnpu]
sieas
B|QUeS ¥Y 198}901d
SHOW
diyiUd
We
O18
spjeuoqow
uosuyor
»
UuosuYyor
Jedey
jeuoleuse}u|
Wal
SIOJO [2E19Ud4)
ouj0a|q yesQUayH
UOXXy
yepoy
uewjsey
jUOdNq
jeoluayDy
Mog
Aeusiq
BjOD-2909
UOJABUD
L8iV
sseidxg
ueuEwYy
4901S
bZ
327
€84V1
180
Expected Returns and the Arbitrage Pricing Theory
TABLE
7.2
Stock
American Express
AT&T
Chevron
Coca-Cola
Disney
Dow Chemical
DuPont
Eastman Kodak
Exxon
General Electric
General Motors
IBM
International Paper
Johnson & Johnson
McDonalds
Merck
3M
Philip Morris
Procter & Gamble
Sears
Industry
Finance services
Telephones
Energy reserves and
production
Food and beverage
Entertainment
Chemical
Chemical
Leisure
Energy reserves and
production
Heavy electrical
Motor vehicles
Computer hardware
Forest products and paper
Medical products
Restaurant
Drugs
Chemical
Tobacco
Home products
Department stores
APT
5.93%
5.33%
3.10%
4.60%
3.05%
3.70%
4.38%
4.29%
2.23%
3.51%
5.89%
3.73%
2.83%
5.87%
5.56%
5.02%
4.67%
4.33%
5.68%
1.42%
CAPM
6.96%
5.04%
4.20%
6.36%
6.78%
6.78%
5.58%
5.64%
4.26%
6.60%
7.50%
6.66%
6.48%
6.42%
6.36%
6.60%
5.46%
6.12%
6.30%
6.60%
181
APT-
CAPM
—1.03%
0.29%
saileilili/o
Sailnili7o
—3.74%
—3.08%
—1.21%
—1.36%
—2.03%
—3.10%
—1.62%
—2.93%
—3.66%
—0.55%
—0.81%
—1.59%
—0.80%
Salevovo
—0.62%
—5.18%
The CAPM forecast is for 6 percent expected market excess
return.
We display the final stock forecasts in Table 7.2. Here we
display the APT forecast, the CAPM forecast, and the residual APT
forecast (the APT forecast less the CAPM forecast).
We can see from this example that whatever the use of an
APT model in forecasting expected returns, it can make a great
talking point. By putting in different expectations for the various
factors, we could automatically generate mountains of research.
THE APT RATIONALE
The APT result follows from an arbitrage argument. What would
happen if we had a returns model like Eq. (7.1), and the APT
182
Expected Returns and Valuation
relationship [Eq. (7.2)] failed to hold? We could find an active posi-
tion with zero exposure to all of the factors* and expected excess
return of 1 percent. Since the active position has zero factor expo-
sure, it has almost no risk, and so we can achieve 1 percent expected
excess return at low risk levels. We can therefore also add this
active position to any portfolio P and improve our performance
by increasing expected excess return with little additional risk.
Arbitrage means a certain gain at zero expense. In the case
described above, we have a nearly certain gain, since the expected
return is positive and the risk is very, very small. There is no
expense, since it is an active portfolio (zero net investment). We
call this second situation a quasi-arbitrage opportunity. If we rule
out these quasi-arbitrage opportunities, then the APT must hold.
How do we find the factor model that will do this wonderful
trick? The APT is silent on that question. However, a little old-
fashioned mean/standard deviation analysis can provide some
clues.
PORTFOLIO Q AND THE APT
The APT is marvelously flexible. We can concentrate on any desired
_
group of stocks.” Among any group of N stocks, there will be an
efficient frontier for portfolios made up of the N risky stocks. Figure
7.3 shows a typical frontier.
With each portfolio we can associate a risk, as measured by
the standard deviation of its returns, and a reward, as measured by
the expected excess return. Portfolio Q in Fig. 7.3 has the highest
reward-to-risk ratio (Sharpe ratio).
Knowledge of portfolio Q is sufficient to calculate all expected
returns.° Portfolio Q plays the same role as the market portfolio
does in the CAPM; in fact, the CAPM is another way of saying
that portfolio Q is the market portfolio.’
‘This will typically imply net zero investment, unless the factor model does not have an
intercept. Even then, we have built a portfolio with almost no risk and 1 percent
expected excess return. We can combine this with the risk-free asset for a net zero
investment with an expected excess return and almost no risk.
*Contrast this with the CAPM, where coverage should, in theory, be universal.
*And vice versa. See Chap. 2 for more details.
»
’See the technical appendix to Chap. 2.
Expected Returns and the Arbitrage Pricing Theory
183
20%
18%
16%
14%
12%
10%
Expected
Excess
Return
8%
Q
6%
4%
2%
0%
10%
20%
30%
40%
50%
Risk
Figure 7.3
The expected excess return on any stock will be proportional
to that stock’s beta with respect to portfolio Q. We might assume
that we can stop here. We cannot, since we don’t know portfolio
Q. However, all is not lost. We can learn something from portfolio Q.
We need to separate two issues at this point. The first is defin-
ing a qualified model, and the second is finding the correct set of
factor forecasts. A multiple-factor model [as in Eq. (7.1)] is qualified
if it is possible to find factor forecasts m(k) such that Eq. (7.2) holds.
184
Expected Returns and Valuation
Once we have a qualified model, we still must come up with the
correct factor forecasts m(k). We argue in the next section that it
should not be hard to find a qualified model. However, in the
section following that, we argue that the ability to make correct
factor forecasts requires both considerable skill and a model linked
to investment intuition.
THE EASY PART: FINDING
A QUALIFIED MODEL
This section describes the technical properties required for a
multiple-factor model to qualify for successful APT implementa-
tion. The details are in the technical appendix. More significantly,
we argue by example that we can fairly easily find qualified models.
Let’s start with the technical result.
A factor model of the type described in Eq. (7.1) is qualified,
ie., Eq. (7.2), will hold for some factor forecasts m,, if and only if
portfolio Q is diversified with respect to that factor model. Diversified
with respect to the factor model means that among all portfolios
with the same factor exposures as portfolio Q, portfolio Q has
minimum risk. No other portfolio with the same factor exposures
is less risky than portfolio Q. How do we translate this technical
rule into practice?
A frontier portfolio like Q should be highly diversified in the
conventional sense of the word. Portfolio Q will contain all the
stocks, with no exceptionally large holdings. We want portfolio Q
to be diversified with respect to the multiple-factor model. Common
sense would say that any multiple-factor model that captures the
important differential movements in the stocks will qualify. The
arbitrary aspect of the APT can be a benefit as well as a drawback!
It’s a drawback in that we don’t know exactly what to do; %t’s a
benefit in that it suggests that there are reasonable steps that will
possibly succeed.
We can check this idea by devising some surrogates for portfo-
lio Q and seeing if they are diversified with respect to the BARRA
U.S. Equity model. The BARRA model was constructed to help
portfolio managers control risk, not to explain expected returns.
However, it does attempt*to capture those aspects. of the market
that cause some groups of stocks to behave differently from others.
Expected Returns and the Arbitrage Pricing Theory
185
TABLE
7.3
Portfolio
Number of Assets
Unexplained Variance (%)
MMI
20
2.51
OEX
100
0.99
S&P 500
500
0.30
FR1000
1000
0.21
FR3000
3000
0.18
ALLUS
~6000
0.17
We find that well over 99 percent of the variance of highly diversi-
fied portfolios is captured by the factor component. Table 7.3 shows
the percentage of total risk that is not explained by the model for
several major U.S. equity indices as of December 1992. The ALLUS
portfolio includes approximately the 6000 largest U.S. companies,
which are followed by BARRA.
Table 7.3 indicates that portfolios are highly diversified with
respect to the BARRA model. It may be possible to find a portfolio
that has the same factor exposures as the Frank Russell 3000 index
and less risk. However, the two portfolios would have the same
factor risk (recall that they have the same factor exposures), and
so they can differ only in their specific risk. Since 99.82 percent of
the risk is explained by the factor component of return, there is
very little margin for improvement. We cannot find portfolios that
have the same factor exposures and substantially less risk, since
the amount of nonfactor risk is already negligible.
Any factor model that is good at explaining the risk of a diversified
portfolio should be (nearly) qualified as an APT model.
The exact specification of the factor model may not be im-
portant in qualifying a model. What is important is that the model
contain sufficient factors to capture movement in the important di-
mensions.
THE HARD PART: FACTOR FORECASTS
We have settled one part of the implementation question. Any
reasonably robust risk model in the form of Eq. (7.1) should qualify.
186
Expected Returns and Valuation
The next step is to find the amount of expected excess return, ™m;
in Eq. (7.2), to associate with each factor.
Forecasting the m, is not easy just because we may have 1000
stocks and only 10 factors. If it were true that “fewer is better,”
then we could just concentrate on forecasting the returns to the
bond market and the stock market. In fact, as the fundamental law
of active management states, it is better to make more forecasts
than fewer for a given level of skill. If we can forecast expected
returns on 1000 stocks or 10 factors, then to retain the same value
added, we need ten times more skill in forecasting the factor returns
than in forecasting the stock returns.
The simplest approach to forecasting m; is to calculate a history
of factor returns and take their average. This is the forecast that
would have worked best in the past—i.e., a backcast rather than
a forecast. If we hope that the past average helps in the future, we
are implicitly assuming an element of stationarity in the market.
The APT does not provide any guarantees here. However, there is
hope. One of the non-APT reasons to focus on factors is the knowl-
edge that the factor relationship is more stable than the stock rela-
tionship. For example, it is probably more valuable to know how
growth stocks have done in the past than to know the past returns
of a particular stock that is currently classified as a growth stock.
The problem is that the stock may not have been classified as a
growth stock over the earlier period; the stock may have changed
its stripes. However, the factor returns will give us some informa-
tion on how it may perform in its current set of stripes!
Haugen and Baker (1996) have proposed an APT model whose
factor forecasts rely simply on historical factor returns. Their factors
roughly resemble the BARRA model, except that they replace more
than 50 industries with 10 sectors, and they replace 13 risk indices
with 40 descriptors.® Each factor forecast is then simply the trailing
12-month average of the factor returns. So they forecast the finance
sector return, the IBES estimated earnings-to-price factor return,
etc., as their past 12-month averages.
Model structure can be very helpful in developing good fore-
casts. As we'll see in the next section, APT models can be either
purely statistical or structural. The factors have some meaning in
>,
‘This leads to collinearity, which the BARRA model attempts to avoid.
Expected Returns and the Arbitrage Pricing Theory
187
the structural model; they don’t in a purely statistical model. In
statistical models, we have very little latitude in forecasting the
factor returns. In a structural model, with factors that are linked
to specified characteristics of the stocks, factor forecasts can be
interpreted as forecasts for stocks that share a similar characteristic.
We can apply both common sense and alternative statistical proce-
dures to check those forecasts.
Factor forecasts are easier if there is some explicit link between
the factors and our intuition. Consider, for example, a “bond market
beta” factor. This factor will show how the stock will react as bond
prices (i.e., interest rates) change. A forecast for this factor is in fact
a forecast for the bond market. This doesn’t mean that forecasting
future interest rates is easy. It means that the knowledge that you
are, in fact, forecasting interest rates should make the task clearer.
A similar result would hold for a factor defined in terms of
a stock’s fundamentals. Consider a “growth” factor, with consensus
growth expectations as the factor exposures. Now our forecast is
an expression of our outlook for growth stocks. Once again, we
haven't guaranteed that we can forecast the outlook for growth
stocks correctly. We have simply made the task more explicit, and
thus given ourselves a greater chance for success.
This suggests an opportunistic approach to building an APT
model. We should take advantage of our conclusion that we can
easily build qualified APT models. We should use factors that we
have some ability to forecast. Suppose we are reasonably good at
forecasting returns to gold, oil, bonds, yen, etc., and we have some
skill at predicting economic fluctuations. We should work from our
strengths and build an APT model based on those factors, then
round out the model with some others (industry variables) to cap-
ture the bulk of the risk. There is no use building the world’s
greatest (most qualified) APT model if we cannot come up with
the factor forecasts.
Factor forecasts are difficult. Structure should help.
The next section describes some approaches to building an
APT model.
APPLICATIONS
We have tried to emphasize the flexible nature of the APT. There
are many ways to build APT models. The arbitrary nature of the
188
Expected Returns and Valuation
APT leaves enormous room for creativity in implementation. Two
equally well-informed scholars working independently will not
come up with similar implementations. We’ve given six illustrations
here. They fall into two catagories, structural and statistical.
Structural models postulate some relationships between spe-
cific variables. The variables can be macroeconomic (unanticipated
inflation, change in interest rates, etc.), fundamental (growth in
earnings, return on equity, market share), or market-related (beta,
industry membership). All types of variables can be used in one
model. Practitioners tend to prefer the structural models, since these
models allow them to connect the factors with specific variables
and therefore link their investment experience and intuition to
the model.
Statistical models line up the returns data and turn a crank.
Academics build APT models to test various hypotheses about
market efficiency, the efficacy of the CAPM, etc. Academics tend
to prefer the purely statistical models, since they can avoid putting
their prejudgments into the model in that way.
There are a great many ways to build an APT model.
Structural Model 1: Given Exposures, Estimate
Factor Returns
The BARRA model, described in detail in Chap. 3, “Risk,” can
function as an APT model. As we saw above, it qualifies with ease,
and it is just as easy (i.e., not very) to forecast returns to the BARRA
factors as to any others. The BARRA model takes the factor expo-
sures as given based on current characteristics of the stocks, such
as their earnings yield and relative size. The factor returns are es-
timates.
e
Structural Model 2: Given Factor Returns,
Estimate Exposures
In this model, the factor returns are given. For example, take the
factor returns as the return on the value-weighted NYSE, gold, a
government bond index, a basket of foreign currencies, and a basket
of traded commodities. Set the exposure of each stack to the NYSE
equal to 1. For the other factors, determine the past exposure of
Expected Returns and the Arbitrage Pricing Theory
189
the stock to the factor returns by regressing the difference between
the stock return and the NYSE return on the returns of the other
factors.
The factor forecasts are forecasts of the future values of the
factor returns. Note that we hope that the estimated factor expo-
sures are stable over time.
Structural Model 3: Combine Structural Models
1 ande2
This model is the inevitable hybrid of structural models 1 and 2:
Start with some primitive factor definitions, estimate the stock’s
factor exposure as in structural model 2, then attribute returns to
the factors as in structural model 1.
Statistical Model 1: Principal
Components Analysis
Look at the returns of a collection of stocks, or portfolios of stocks,
over many months—say 50 stocks over 200 months. Calculate the
50 by 50 matrix of realized covariance between these stocks over
the 200 months. Do a principal components analysis of the 50
by 50 covariance matrix. Typically, one will find that the first 20
components will explain 90 percent or more of the risk. Call these
20 principal component returns the factors. These factors are purely
statistical constructs. We might as well call them Dick, Jane, Spot,
-.. OF red, green, blue. .;.
The analysis will tell us the exposures of the 50 stocks to the
factors. It will also give us the returns on those factors over the
200 months. The factor returns will be uncorrelated. We can deter-
mine the exposures to the factors of stocks that were not included
in the original group by regressing the returns of the new stocks
on the returns to the factors. The regression coefficients will measure
the exposures to the factors; the fact that the factor returns are
uncorrelated is useful at this stage. To implement this model, we
need a forecast of the m,. The obvious forecast is the historical
average of the factor returns. It may be the only possible forecast:
Since the factors are by construction abstract, it would be hard to
justify a forecast that differed from the historical average.
190
Expected Returns and Valuation
Statistical Model 2: Maximum Likelihood
Factor Analysis
Here we perform a massive maximum likelihood estimation, look-
ing at Eq. (7.1) over 60 months. To make this possible, we assume
that the stock’s exposures X,,, are constant over the 5-year period.
If we applied this to 500 stocks over 60 months and looked for 10
factors, we would be using 500
- 60 = 30,000 returns to estimate
500 - 10 = 5000 exposures and 60 - 10 = 600 factor returns.
Statistical Model 3: The Dual of Statistical
Model 2
This is quite imaginative. A detailed description is difficult, but
see Connor and Korajezyk (1988). When N stocks are observed
over T time periods, N is usually much greater than T. Instead
of analyzing the principal components of the N by N historical
covariance matrix, we look at the T by T matrix of covariances.
This analysis reverses the role of factor exposure and factor return!
SUMMARY
We have described the APT and talked about its relevance for active
management. The APT is a powerful theory, but difficult to apply.
The APT does not in any way relieve the active manager of the
need for insight and skill. It is a framework that can help skilled
and insightful active managers harness their abilities.
Problems
.
1. According to the APT, what are the expected values o
the u, in Eq. (7.1)? What is the corresponding
relationship for the CAPM?
2. Work by Fama and French, and others, over the past
decade has identified size and book-to-price ratios as
two critical factors determining expected returns. How
would you build an APT model based on those two
factors? Would the model require additional factors?
Expected Returns and the Arbitrage Pricing Theory
191
3. In the example shown in Table 7.2, most of the CAPM
forecasts exceed the APT forecasts. Why? Are APT
forecasts required to match CAPM forecasts on average?
4. In an earnings-to-price tilt fund, the portfolio holdings
consist (approximately) of the benchmark plus a multiple
c times the earnings-to-price factor portfolio (which has
unit exposure to earnings-to-price and zero exposure to
all other factors). Thus, the tilt fund manager has an
active exposure c to earnings-to-price. If the manager
uses a constant multiple c over time, what does that
imply about the manager’s factor forecasts for earnings-
to-price?
5. You have built an APT model based on industry, growth,
bond beta, size, and return on equity (ROE). This month
your factor forecasts are
Heavy electrical industry
6.0%
Growth
2.0%
Bond beta
—1.0%
Size
—0.5%
ROE
1.0%
These forecasts lead to a benchmark expected excess return
of 6.0 percent. Given the following data for GE,
Industry
Heavy electrical
Growth
—0.24
Bond beta
0.13
Size
1.56
ROE
0.15
Beta
Ke
what is its alpha according to your model?
NOTES
In the early 1970s, Sharpe (1977) (the paper was written in 1973),
Merton (1973), and Rosenberg (1974) advocated multiple-factor ap-
proaches to the CAPM. Their arguments were based on reasoning
similar to that underlying the CAPM. The results were a multiple-
192
Expected Returns and Valuation
ee ee
beta form of the CAPM, identical in form to Eq. (7.2). In fact, an
active money management product called a “yield tilt fund” was
launched based on the notion that higher-yielding stocks had higher
expected returns.
In the mid-1970s, Ross (1976) proposed a different way of
looking at expected stock returns. Ross used the notion of arbitrage,
which was the foundation of Black and Scholes’s work on the
valuation of options. In certain cases the mere ruling out of arbitrage
opportunities is sufficient to produce an explicit formula for a
stock’s value. Later other authors, notably Connor (1984) and Hub-
erman (1982), added additional assumptions and structure to pro-
duce the exact form of Eq. (7.2). Modern theoretical treatments of
the APT reserve a role for the market portfolio. See Connor (1986)
for a discussion.
Bower, Bower, and Logue (1984); Roll and Ross (1984); and
Sharpe (1984) have expositions of the APT aimed at professionals.
See also Rosenberg (1981) and Rudd and Rosenberg (1980) for a
discussion of the CAPM and APT. The text by Sharpe and Alexander
(1990) has an excellent discussion.
Applications of the APT are described in Roll and Ross (1979),
Chen, Roll, and Ross (1986), Lehmann and Modest (1988), and
Connor and Korajczyk (1986).
For a discussion of some of the econometric and statistical
issues surrounding the APT, see Shanken (1982), Shanken (1985),
and the articles cited in those papers.
Actual implementations of APT models are described by Roll
and Ross; Chen, Roll, and Ross; Lehmann and Modest; Connor
and Korajczyk, etc.
REFERENCES
Black, Fischer. “Estimating Expected Returns.” Financial Analysts Journal, vol. 49,
no. 5, 1993, pp. 36-38.
Bower, D. H., R. S. Bower, and D. E. Logue. “A Primer on Arbitrage Pricing
Theory.” The Midland Journal of Corporate Finance, vol. 2, no. 3, 1984, pp. 31-40.
Chamberlain, G., and M. Rothschild. “Arbitrage, Factor Structure, and Mean-
Variance Analysis on Large Asset Markets.” Econometrica vol. 51, no. 5, 1983,
pp. 1281-1304.
Chen, N., R. Roll, and S. Ross. “Economic Forces and the Stoek Market.” Journal
of Business, vol. 59, no. 3, 1986, pp. 383-404.
»
Expected Returns and the Arbitrage Pricing Theory
193
Connor, Gregory. “A Unified Beta Pricing Theory.” Journal of Economic Theory, vol.
34, no. 1, 1984, pp. 13-31.
- “Notes on the Arbitrage Pricing Theory.” In Frontiers of Financial Theory,
edited by G. Constantinides and S. Bhattacharya (Boston: Rowman and
Littlefield, 1986).
Connor, Gregory, and Robert A. Korajczyk. “Performance Measurement with the
Arbitrage Pricing Theory.” Northwestern University working paper, 1986.
——.. “Risk and Return in an Equilibrium APT: Application of a New Test
Methodology.” Journal of Financial Economics vol. 21, no. 2, 1988, pp. 255-290.
Fama, Eugene F., and Kenneth R. French. “The Cross-Section of Expected Stock
Returns.” Journal of Finance, vol 67, no. 2, 1992, pp. 427-465.
Grinold, R. “Is Beta Dead Again?” Financial Analysts Journal, vol 49, no. 4, 1993,
pp. 28-34.
Haugen, Robert A., and Nardin L. Baker. “Commonality in the Determinants of
Expected Stock Returns.” Journal of Financial Economics, vol. 41, no. 3, 1996,
pp. 401-439.
Huberman, G. “A Simple Approach to Arbitrage Pricing Theory.” Journal of Eco-
nomic Theory, vol. 28, 1982, pp. 183-191.
Lehmann, Bruce N., and David Modest. “The Empirical Foundations of the Arbi-
trage Pricing Theory.” Journal of Financial Economics, vol. 21, no. 2, 1988,
pp. 213-254.
Mayers, D., and E. M. Rice. “Measuring Portfolio Performance and the Empirical
Content of Asset Pricing Models.” Journal of Financial Economics, vol. 7, no.
2, 1979, pp..3-28,
Merton, R. C. “An Intertemporal Capital Asset Pricing Model.” Econometrica, vol.
41, no. 1, 1973, pp. 867-887.
Pfleiderer, P. “A Short Note on the Similarities and the Differences between the
Capital Asset Pricing Model and the Arbitrage Pricing Theory.” Stanford
University Graduate School of Business working paper, 1983.
Roll, Richard. “A Critique of the Asset Pricing Theory’s Tests.” Journal of Financial
Economics, vol. 4, no. 2, 1977, pp. 129-176.
Roll, Richard, and Stephen A. Ross. “An Empirical Investigation of the Arbitrage
Pricing Theory.” Journal of Finance, vol. 35, no. 5, 1979, pp. 1073-1103.
. “The Arbitrage Pricing Theory Approach to Strategic Portfolio Planning.”
Financial Analysts Journal, vol. 40, no. 3, 1984, pp. 14-26.
Rosenberg, Barr. “Extra-Market Components of Covariance in Security Returns.”
Journal of Financial and Quantitative Analysis, vol. 9, no. 2, 1974, pp. 263-274.
. “The Capital Asset Pricing Model and the Market Model.” Journal of
Portfolio Management, vol. 7, no. 2, 1981, pp. 5-16.
Ross, Stephen A. “The Arbitrage Theory of Capital Asset Pricing.” Journal of
Economic Theory, vol. 13, 1976, pp. 341-360.
Rudd, Andrew, and Henry K. Clasing, Jr. Modern Portfolio Theory, 2d ed. (Orinda,
Calif.: Andrew Rudd, 1988).
Rudd, Andrew, and Barr Rosenberg. “The ‘Market Model’ in Investment Manage-
ment.” Journal of Finance, vol. 35, no. 2, 1980, pp. 597-607.
194
Expected Returns and Valuation
Shanken, J. “The Arbitrage Pricing Theory: Is It Testable?” Journal of Finance, vol.
37, no. 5, 1982, pp. 1129-1140.
. “Multi-Beta CAPM or Equilibrium APT? A Reply to Dybvig and Ross.”
Journal of Finance, vol. 40, no. 4, 1985, pp. 1189-1196.
. “The Current State of the Arbitrage Pricing Theory.” Journal of Finance,
vol. 47, no. 4, 1992, pp. 1569-1574.
Sharpe, William F. “Factor Models, CAPMs, and the APT.” Journal of Portfolio
Management, vol. 11, no. 1, 1984, pp. 21-25.
Sharpe, William F. “The Capital Asset Pricing Model: A ‘Multi-Beta’ Interpreta-
tion.” In Financial Decision Making under Uncertainty, edited by Haim Levy
and Marshall Sarant (New York: Academic Press, 1977).
Sharpe, William F., and Gordon J. Alexander. Investments (Englewood Cliffs, N.J.:
Prentice-Hall, 1990).
TECHNICAL APPENDIX
This appendix contains
# A description of factor models of stock return
# A derivation of the APT in terms of factor models
Factor Models
A factor model represents excess returns as
r=X-b+u
(7A.1)
where X is the N by K matrix of stock exposures to the factors, b
is the vector of K factor returns, and uw is the specific return vector.
For any portfolio P with holdings hp of the risky assets, the
portfolio’s factor exposures are
Gy
x7
hp
(7A.2)
Recall that portfolio C is the fully invested portfolio ‘with
minimum variance and that portfolio Q is the fully invested portfo-
lio that has the highest ratio of expected excess return to risk. In
the technical appendix to Chap. 2, we established that the expected
excess return on each asset is proportional to that asset’s beta with
respect to portfolio Q.
We assume that
= f- > 0, and thus portfolio Q exists and fg >0.
Expected Returns and the Arbitrage Pricing Theory
195
= The specific returns u are uncorrelated with the factor
returns b.
= The factor exposures X are known with certainty at the
start of the period.
With these assumptions, the N by N asset covariance matrix is
VSXe PX
(7A.3)
where F is the K by K covariance of the factors and A is an N by
N matrix that gives the covariance of the specific returns. We usually
assume that A is a diagonal matrix, although that is not necessary.
We refer to the factor model as (X, F, A). We say that a factor
model explains expected excess returns f if we can express the vector
of expected excess returns f as a linear combination of the factor
exposures X. The model (X, F, A) explains expected excess returns
if there is a K-element vector of factor forecasts m such that
f=X-m
(7A.4)
Equation (7A.4) gives us an expression for f. In the appendix to
Chap. 2, we derived another expression for f involving portfolio
Q. Let’s look for the link between these two expressions.
The N-element vector of stock covariances with respect to
portfolio Q is
From Eq. (2A.36) (Proposition 3 in the technical appendix to
Chap. 2), we know that the expected excess returns are
f= fo Wg 2 Ky KF XT + A)
(7A.6)
where
weedy
(7A.7)
uf
Compare Eqs. (7A.4) and (7A.6). We are getting perilously
close to the APT result. As an initial stab, we could write m* =
Ko ° F- xX’. ho. Then
f=X-m*+ Ko: A-hg
(7A.8)
One alternative is to ignore the second term and live with
196
Expected Returns and Valuation
ce
i
ere
a little imperfection. To attain perfection, however, we need one
additional assumption. We show below that this assumption works
and that we need to make it; i.e., this assumption is both necessary
and sufficient. First a definition: A portfolio P is diversified with
respect to the factor model (X, F, A) if portfolio P has minimal risk
among all portfolios that have the same factor exposures as portfolio
P; i.e., of all portfolios h with X’ - hp = xp, portfolio P has the
least risk.
Our assumption is that portfolio Q is diversified with respect
to the factor model (X, F, A).
Proposition 1 (APT)
The factor model (X, F, A) explains expected excess returns if and
only if portfolio Q is diversified with respect to (X, F, A).
Proof Suppose first that portfolio Q is diversified with respect
to (X, FE, A). Now we can find the portfolio with exposures xg that
has minimal risk by solving
(h7- V-h)
Minimize
5
, subject to X7- h = xg
(7A.9)
The first-order conditions for this problem are satisfied by the
optimal solution h* and a K-element vector of Lagrange multipliers
a that satisfy
V-h*-X-a=0
(7A.10)
XT -h =x,
(7A.11)
Since portfolio Q is diversified with respect to (X, F, A), then hg =
h* is the optimal solution. Therefore
V-ho=X-a
(7/A.12)
Combining Eq. (7A.12) with Eqs. (7A.6), (7A.7), and (7A.4) leads to
m= ko' 7
(7A.13)
and the factor model (X, F, A) explains the expected excess returns.
For the converse, suppose that the factor model (X, F, A) ex-
plains the expected excess returns and that portfolio Q is not diversi-
fied with respect to (X, F, A). Then there exists a portfolio P with
Expected Returns and the Arbitrage Pricing Theory
197
the same exposures as portfolio Q, i.e., xp = X’ + hp = Xg, and less
risk than portfolio Q, i.e., 03 < 0%. However, we have fp = fo, since
the factor exposures determine the expected returns, and portfolios
P and Q have identical factor exposures. So fe
> fo,
Jains?
Portfolio P cannot be all cash, since the expected excess return
on cash is zero. Therefore portfolio P is a mixture of cash and a
nonzero fraction of some fully invested portfolio P*. It must be
that fp/op = fp:/op. Recall, however, that portfolio Q is the fully
invested portfolio with the largest possible ratio of expected excess
return to risk. This contradiction establishes the point: Portfolio Q
must be diversified with respect to (X, F, A).
Exercises
1. A factor model contains an intercept if some weighted
combination of the columns of X is equal to a vector of
1s. This will, of course, be true if one of the columns of
X is a column of 1s. It will also be true if X contains a
classification of stocks by industry or economic sector.
The technical requirement for a model to have an
intercept is that there exists a K-element vector g such
that e = X - g. Assume that the model contains an
intercept, and demonstrate that we can then determine
the fraction of the portfolio invested in risky assets by
looking only at the portfolio’s factor exposures.
2. Show that a model that does not contain an intercept is
indeed strange. In particular, show there will be a fully
invested portfolio with zero exposures to all the
factors—a portfolio P with hj - e = 1 (fully invested) and
xp = X' - hp = 0 (zero exposure to each factor).
Applications Exercises
1. What is the percentage of unexplained variance in the
CAPMMI portfolio? Does this portfolio qualify as highly
diversified? How much would it be possible to lower the
risk of the CAPMMI in a portfolio with identical factor
exposures?
198
Expected Returns and Valuation
2. Assume an excess return forecast of 5 percent per year
for a value factor, excess return of —1 percent per year
for a size factor, and excess return forecasts of zero for
all other factors. Using the CAPMMI as a benchmark,
what MMI asset has the highest alpha? What is its
value?
