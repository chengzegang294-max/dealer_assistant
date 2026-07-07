# Quantitative Equity Portfolio Management: An Active Approach to Portfolio Construction and Management, Second Edition

- **book_name**: 5073 Quantitative Equity Portfolio Management, Second Ed.
- **main_source**: epub
- **cross_check_source**: none
- **pdf_role**: not_needed
- **split_scope**: chapter file = chapter07

---

CHAPTER 7
Economic Factor Models
Beta is the color of an angel’s eye
.
—Zvi Griliches
7.1 INTRODUCTION
Tenet 4 of quantitative equity portfolio management (QEPM) requires quantitative analysis to efficiently combine all the information relevant to an investment decision. In
Chapter 6
, we looked at the fundamental factor model as one efficient way to combine relevant information about stocks into a system for determining returns and risks. The economic factor model is the counterpart to the fundamental factor model. It also combines relevant stock information in an efficient way, but with a different twist on the factor model framework.
1
The structure of the model remains the same as we move from the fundamental factor model to the economic factor model. The model still expresses the central idea that stock returns are the payoff for taking risk. As in the fundamental factor model, stock
returns are determined by the product of factor exposures (i.e., exposures to risk) and factor premiums (i.e., payoffs for exposure to risk). In the economic factor model, however, the roles of the factor exposure and factor premium are, in a way, reversed. Recall that for the fundamental factor model, the factor exposure is observable in financial statements, whereas the factor premium must be estimated from a cross-sectional regression. In the economic factor model, the factor premium is the known value (or, at least, the value that can be calculated from given data), whereas the factor exposure must be estimated by a regression of stock returns on factor premiums.
Take, for instance, an economic factor model with just one factor, inflation. In this model, the factor premium is the observed rate of inflation (or a rate that corresponds to the inflation rate). The factor exposure is the stock’s sensitivity or reactivity to inflation, which is estimated as the relationship between the return on the stock and the rate of inflation. The economic factor model, therefore, takes as a given the premium that the market generally places on exposure to the risk but requires the estimation of a particular stock’s exposure to the risk. This type of model especially makes sense for economic factors, which represent external risks in the marketplace that affect all stocks.
2
In this case, the particular type of risk that we are concerned with is inflation. The factor premium therefore shows the amount of reward investors demand when they invest in stocks affected by inflation. This amount of reward demanded most likely will be different from the actual inflation rate for two reasons. The first is that the units are different. The inflation rate is not expressed in risk terms, so we cannot say that the reward for taking 1% inflation rate should be 1% expected return. The second is that not all inflation corresponds to risk. Specifically, the expected component of inflation does not qualify as risk; only the unexpected component of inflation should be considered a risk. So why do we use the actual inflation rate as the factor premium?
The economic factor model does not assume that the amount of reward demanded by investors is the actual inflation rate. What it assumes is that the amount of reward is a linear function of the
actual inflation rate. The reward for exposure to an
x
% inflation rate may not be
x
% expected return, but it may be stated as
a
+
bx
. This assumption removes the necessity to distinguish between the true factor premium and the observed inflation rate because the estimation of the model will not be affected whether we use the true factor premium or the observed inflation rate. This assumption also takes care of the problem caused by the expected component of inflation. The expected component will be adjusted by the constant
a
in the formula
a
+
bx
. For this reason, for the remainder of this chapter we do not distinguish between the true factor premium and the observed values of the economic variables.
Mathematically, the economic factor model defines the return to stock
i, r
i
, as
where
f
1
, …,
f
K
are factor premiums (which do not vary across stocks and so do not have the subscript
i
), and
β
i
1
, …,
β
iK
are factor exposures (which do vary across stocks and have the subscript
i
). The term
α
i
is the constant. The term
β
i
1
f
1
+ … +
β
i
K
f
K
represents the nondiversifiable risk of the stock, and
ϵ
i
, the error, reflects the diversifiable risk of the stock.
3
In terms of the basic equation, there is no difference between the fundamental factor model and the economic factor model.
4
As with the fundamental factor model, we again define
K
-dimensional column vector
f
and
β
i
as follows:
Using this notation,
As we saw in
Chapter 6
, the average stock return is the product of the factor exposure and the factor premium plus the constant term,
whereas the total risk is the sum of the nondiversifiable risk and the diversifiable risk, that is,
The model also can express the stock return at a particular time interval. We use lowercase letter
t
to indicate one time interval and the capital letter
T
to indicate the number of time intervals. Thus the return to stock
i
at time
t, r
i
t
, is written as
where
α
i
is a
K
-dimensional column vector of the factor exposure of stock
i
,
f
t
is a
K
-dimensional column vector of the factor premium at time
t
, and
ϵ
it
is the diversifiable component of the return to stock
i
at time
t
.
5
Note that the factor premium has time subscript
t
because it changes over time. That is, we interpret the factor premium as a random variable that has different values at different times. On the other hand, the factor exposure does not have time subscript
t
because it is not assumed to change over time. We interpret the factor exposure as an unknown parameter rather than a random variable.
In academia, the economic factor model has long been the only factor model deemed valid, with the fundamental factor model only recently gaining some credence. In fact, the academic literature fails to distinguish between economic and fundamental factor models, using instead the term
multifactor pricing model
to refer generally to the framework of the economic factor model. We choose to distinguish between the two types of models using the terms
economic factor model
and
fundamental factor model
because many practitioners use the former for modeling stock returns against economic indicators and the latter for modeling stock returns against stock fundamentals.
Table 7.1
summarizes the process of creating an economic factor model.
TABLE 7.1
Creating an Economic Factor Model
7.2 PRELIMINARY WORK
As with the fundamental factor model, constructing the economic factor model begins with good planning. The general decisions are the same—the choice of factors, the treatment of the risk-free rate, and the makeup of the sample (in terms of time interval, time period, and stock universe). Since the criteria for deciding how to treat the risk-free rate, for determining the investment universe,
and for defining the time interval and period are the same for either type of model, we will just discuss the factor choice here.
6
The strength of the economic factor model is that it can include practically all kinds of factors. In terms of how the model treats them, there are three categories of factors:
1.
Economic/behavioral/market factors:
Gross domestic product (GDP), inflation, unemployment, interest rates, and other macroeconomic variables; consumer sentiment index, business confidence index, investor sentiment index, or other survey-based indexes; returns on broad market indexes such as the Standard & Poor’s (S&P) 500 or returns on other market group/industry indexes
2.
Fundamental/technical/analyst factors:
Log of market capitalization, book-to-price ratio, earnings-to-price ratio, debt-to-equity ratio, and other firm characteristics available through financial statements; momentum, trading volume, and other information reflected in trading data; analyst rating changes, earnings revisions, or other information provided by analysts
3.
Statistical factors:
Factors obtained from principal-component analysis applied to historical returns
For economic/behavioral/market factors, computation is minimal. In most cases, relevant information is publicly available or provided by data vendors. On the other hand, for fundamental/technical/analyst factors, computation can be somewhat demanding, and even though they may be obtained from an external source, the vendor’s methodology should be examined carefully. Some studies suggest, though, that thoroughly vetted fundamental/technical/analyst factors predict stock returns more effectively than other factor groups do.
7
Statistical factors require the highest level of computation.
7.3 BENCHMARK AND
α
Many quantitative portfolio managers manage their portfolios against a benchmark. As we mentioned in
Chapter 6
, it is useful but not necessary to account for the benchmark at the outset of creating a model. Some portfolio managers prefer to account for the benchmark later on—by controlling for the tracking error at the portfolio construction stage, for instance.
8
As a measure of portfolio performance, however, it can be useful to create a model that reflects, or adjusts for, the effects of the benchmark. One way to do this is to remove the benchmark-related return from the stock return before building the model.
9
We first regress stock returns on the benchmark returns and calculate the residual, the part of stock returns that is not correlated with the benchmark return. Then we construct an economic factor model for the residual stock return rather than the total stock return. The resulting model shows the relationship between the factor premium, the factor exposure, and the portion of the stock return that is above and beyond the benchmark return.
Alternatively, we can include the benchmark in the economic factor model explicitly. If the benchmark is the broad-market index, the capital asset pricing model (CAPM) supports its inclusion in the model as a predictor of stock returns. Even if the benchmark is something other than the broad-market index, including it in the model will clarify the relationship between the portfolio and the benchmark.
Let
r
B
be the benchmark return. If we add the benchmark as the
K
th factor in the economic factor model, then the economic factor model becomes
Given this formulation, we can interpret the right-hand side of the equation up to the term
β
i,K
−1
f
K
−1
as the expected return of stock
i
that is not related to the benchmark. Collectively, these terms represent the benchmark alpha, or
α
B
, that is,
The benchmark
α
shows the contribution of the portfolio manager (and the model he or she creates) to the stock return and is one measure of the portfolio manager’s performance.
10
7.4 THE FACTOR PREMIUM
Recall that to create the fundamental factor model, the portfolio manager collects a data set of many observations of stock return and factor exposure. The factor exposure changes over time (and the factor premium—a single, statistically estimated proportion—remains constant). By contrast, to create the economic factor model, the portfolio manager gathers pairs of stock returns and factor premiums, and the factor premiums change over time. If there are
K
factors, one needs to find the factor premiums of the
K
factors at each time interval
t
,
f
t
= (
f
1
t
, …,
f
Kt
).
In the economic factor model, the factor premium is the
known
value (as opposed to the factor exposure, which is a regression
estimate
). This does not mean that one can always observe a factor premium directly, though. For economic/behavioral/market factors, the computation is rather trivial. For fundamental/technical/analyst factors, though, the computation is somewhat more demanding, and for statistical factors, it poses quite a bit of a challenge.
7.4.1 Factor Premium for Economic/Behavioral/Market Factors
Obtaining factor premiums for economic/behavioral/market factors does not involve any computation. All we need to do is simply “copy and paste” the values.
11
Table 7.2
presents the premiums for three factors: unemployment, consumer sentiment, and overall market return. To find the factor premium for unemployment, we simply take the unemployment rate published by the Bureau of Labor Statistics (BLS). For example, the unemployment rate in December 2019 was 3.6%, so
after allowing for a one-month reporting gap, the factor premium for January 2020 is 3.6%. For consumer sentiment, we take the consumer sentiment index compiled by the University of Michigan, which shows the level of consumer sentiment for each month. The factor premium is simply the growth rate of this index from one month to the next month. For example, the consumer sentiment index for December 2019 was 99.3, whereas the index for January 2020 was 99.8. Thus, our consumer sentiment factor premium is 0.50%
The market factor premium is the S&P 500 total return in excess of the one-month U.S. Treasury bill return.
12
For example, in January 2020, the S&P 500 total return was −0.04%, whereas the one-month U.S. Treasury bill return was 0.13%. Thus, the factor premium for January 2020 was −0.17% (= −0.04 − 0.13).
Table 7.2
Premium of Unemployment, Consumer Sentiment, and Market Factors
After we have all the factor premiums for a certain time interval, we may store them in a set of vectors {
f
1
, …,
f
T
}, where
f
t
is the
factor premium for time
t
. In this example, we can write the factor premium for January 2020 as
The first element of
f
t
always reflects the existence of the constant term in the return equation.
7.4.2 Factor Premium for Fundamental/Technical/Analyst Factors
A little more computation is necessary to find the factor premiums for fundamental/technical/analyst factors. The computation involves constructing zero-investment portfolios and calculating their returns. A zero-investment portfolio simultaneously takes a long position in a portfolio of stocks with high factor exposures and a short position in a portfolio of stocks with low factor exposures. Suppose that we want to find the factor premium on value, and suppose that we use the book-to-price (B/P) ratio as a proxy for value. We need to identify a portfolio of stocks with high exposure to the value factor (i.e., high B/P ratio) and a portfolio of stocks with low exposure to the value factor (i.e., low B/P ratio). To be systematic about it, we can start by ranking all the stocks at time
t
in order of their B/P ratio, with the highest ratio stock ranked first. We can create a high-value portfolio by equally weighting the stocks in the top 33% of the list and a low-value portfolio by equally weighting the stocks in the bottom 33%. The zero-investment portfolio return equals the difference between the return on the high-value portfolio and the return on the low-value portfolio.
The frequency of the zero-investment portfolio construction needs to be carefully selected if the sorting variable is not frequently updated. In the case of the book-to-price ratio, book values are only reported every quarter, while price is updated daily. While it is possible to calculate the book-to-price ratio every day, the daily fluctuation in this ratio would only reflect daily changes in the stock price rather than daily changes in the book value. Therefore, the ratio is likely to have a big jump when the book values are updated. Thus, creating a zero-investment portfolio too frequently may not reflect information an investor needs and, consequently, may not be a wise choice.
It is important to note that a single piece of data can represent more than one type of factor. The same B/P ratio value, for instance,
can either be considered high exposure to a value factor or low exposure to a growth factor. There are many instances of this sort of symmetry. We could use market capitalization figures to measure a small-size factor, in which case a large market capitalization would mean low exposure to the small-size factor. Conversely, we could interpret the same large market cap figure as a high exposure to a large-size factor. If we are considering including a momentum factor in the model, a low exposure to the momentum factor means the same thing as a high exposure to the contrarian factor. The same numerical figure can stand in for either factor. In fact, we could use either factor to represent the continuity or change in direction of a stock’s return from one year to the next. The sign and name of the factor do not matter as long as we assign consistent meanings (low exposure or high exposure, as the case may be) to high and low values.
In general, these are the steps to calculate the factor premium for fundamental/technical/analyst factors:
1.
Rank all the stocks at time 1 in terms of the factor.
2.
Create high-exposure and low-exposure portfolios by equally weighting the stocks in the top 33% of the list and in the bottom 33% of the list. (A critical value other than 33% may be justifiable.
13
)
3.
Calculate the zero-investment portfolio return as the difference between the returns on the high-exposure and low-exposure portfolios. The return on the zero-investment portfolio is the factor premium for time 1.
Repeat these steps for time 2. If lack of data prevents the construction of new portfolios for time 2, calculate the returns as of time 2 on the same portfolios used for time 1. Repeat the procedure for each factor at each time interval. In other words, the total number of iterations of the procedure will equal the number of factors multiplied by the number of time intervals.
Table 7.3
presents the premium for the size and value factors.
14
TABLE 7.3
Premium of Market Capitalization and Book-to-Price Factors
7.4.3 Factor Premium for Statistical Factors
Obtaining factor premiums for statistical factors involves a rather intensive computation. The computational procedure is known as
principal-component analysis
and is available on standard computer software packages.
The starting point for principal-component analysis is estimating the variance-covariance matrix of stock returns. We will express
N
stock returns at time
t
as an
N
-dimensional column vector; that is,
r
t
= (
r
1
t
, …,
r
Nt
)′. We have a total of
T
such vectors {
r
1
, …,
r
T
}. The variance-covariance matrix of returns
Σ
is estimated as
where
is the average return vector, that is,
Once we have the variance-covariance matrix, we “diagonalize” it by finding an orthogonal matrix
Q
(that is,
Q
−
1
=
Q
′) such that
where
D
is a diagonal matrix whose diagonal elements are eigenvalues (i.e., characteristic values) of
. It turns out that each column of
Q
is an orthonormal (i.e., of unit length) eigenvector corresponding to eigenvalues of
.
To be more specific, let
λ
1
, …,
λ
N
be the eigenvalues of
such that
λ
1
≥ … ≥
λ
N
≥ 0. (Since
is a positive definite matrix, all the eigenvalues are positive.) Then matrix
D
is constructed as
Let
q
1
, …,
q
N
be the orthonormal eigenvectors corresponding to
λ
1
, …,
λ
N
. Then matrix
Q
is
If we want to find
K
factors, then we obtain
K
factor premiums by weighting individual stock returns using the first
K
columns of
Q
. That is, factor premiums
f
1
, …,
f
K
are defined as
These
K
factors together have the highest in-sample explanatory power for
N
stock returns among any set of
K
explanatory variables constructed from linear combinations of
N
stock returns.
15
7.5 FACTOR EXPOSURE
7.5.1 The Standard Approach
In the economic factor model, factor exposures typically are determined from the time-series regression of stock returns on factor premiums. Since the regression coefficients (the factor exposures) measure the sensitivity of the dependent variable (the stock return)
to the change in the independent variables (the factor premiums), factor exposures sometimes are called
factor sensitivities
. They are also sometimes referred to as
factor loadings
.
Given the returns of stock
i
and the factor premium for
T
periods of time, {
r
i
1
, …,
r
i
T
} and {
f
1
, …,
f
T
}, we can estimate the following equation
16
:
where “coefficient”
β
i
is the factor exposure that we wish to discover, and
ϵ
it
is the error term reflecting the diversifiable risk of stock returns. The ordinary least squares (OLS) estimator of
β
i
is given by
where
and
By repeating the regression for each of the
N
stocks, we will obtain all the factor exposures we need:
The standard error of the factor exposure is the square root of (the diagonal elements of) the following variance:
where
is the estimated variance of
ϵ
it
:
Table 7.4
presents the factor exposure estimates and standard errors for selected stocks for a five-factor model. These factor
exposures were estimated using monthly data from January 2016 to December 2020. The unemployment factor exposures are negative for Microsoft, Johnson & Johnson, and Amazon but positive for Apple and Walmart. This reflects Apple’s and Walmart’s positions as business-cycle-defensive stocks: stocks whose values tend to go up when the economy slows down.
17
Although one would expect all five stocks in
Table 7.4
to have a positive exposure to the log of market capitalization factor, they do not. That is, Microsoft, Walmart, and Johnson & Johnson have a positive exposure, meaning these stock returns tend to be positive when the portfolio of large-cap companies does better than a portfolio of small-cap companies. However, Amazon and Apple have a slightly negative reading. The value or book-to-price exposures indicate that Walmart is a value stock (with a positive exposure to the value or book-to-price factor), whereas the other companies are growth stocks (with negative exposures to the book-to-price factor).
TABLE 7.4
Factor Exposure of Selected Stocks
It is worth noting that while the factor exposure estimates in
Eq. (7.4)
can be explained with common sense, this does not necessarily imply that they are identical to the factor exposures we used for the fundamental factor model in
Chapter 6
. For example, the ranking of stocks according to estimated size exposure does not exactly correspond to the ranking of stocks according to actual market capitalization, which was what we used as the size factor exposure in
Chapter 6
. As a result, here Walmart ranks first in terms of size exposure, whereas it ranks fourth after Apple, Microsoft, Amazon, and Johnson & Johnson in terms of actual market capitalization. Similarly, the ranking of stocks by the estimated B/P ratio or value exposure does not correspond exactly to the ranking of stocks by the observed B/P ratio of each stock.
7.5.2 When the Standard Approach Fails
To run time-series regressions, portfolio managers need to have enough data on stock returns and factor premiums to thoroughly cover a reasonable time period at regular time intervals. Recent initial public offerings (IPOs) and the stocks of recently merged or divested companies lack sufficient data for meaningful regressions. For a stock with insufficient data, we may infer the factor exposures by weighting groups of similar stocks and using the weighted factor exposures as proxies for the original stock’s exposures.
When two firms merge, the natural thing to do is to find the weighted average of the factor exposures of the two premerger firms.
18
The appropriate weights would be the market capitalizations of the premerger firms. Suppose that firm
A
and firm
B
merged recently. From stock returns of firm
A, r
A
t
, we can find the factor exposures of firm
A
,
, by regressing factor premiums on stock returns, that is,
We can find the factor exposures of firm
B
,
in a similar way. Then the factor exposures of the merged firm
can be calculated by
where
s
A
is the premerger market capitalization of firm
A
, and
s
B
is the premerger market capitalization of firm
B
.
For a recent IPO, the only available information about the firm is the observable firm characteristics (i.e., what is reported in financial statements). We can use this information to find similar firms and take the average factor exposures of those similar firms. Suppose that we want to find similar firms using
L
characteristics. Then we calculate the Z-score for each of the
L
characteristics of each firm for which we already have factor exposures (see
Chapter 5
for Z-score). Let a young firm
i
’s Z-score be
z
i
= (
z
i
1
, …,
z
iL
). To identify similar firms, we can choose a small critical level
e
and find all firms
j
such that (
z
i
−
z
j
)′(
z
i
−
z
j
) <
e
. We choose a critical level
e
that will give us more than one similar firm. Once we identify the similar firms, we can take the equal-weighted average of the factor exposures of the similar firms as the factor exposure of firm
i
. That is, if firms 1, …,
M
are similar to young firm
C
, then the factor exposure of the young firm
C
,
is given by
where
are the factor exposures of firms 1, …,
M
.
This process of identifying similar firms is called
characteristic matching
, and it applies to searching for other characteristics, such as expected stock return, as well.
19
An alternative to characteristic matching is using the industry-average figure. For example, the average factor exposure of the entire pharmaceutical industry can stand in for the factor exposure of one new pharmaceutical company’s stock. This approach is used quite often to guess the market “beta” of IPO stocks. Financial economic research suggests, however, that characteristic matching works better than using the industry average.
7.6 DECOMPOSITION OF RISK
7.6.1 The Standard Approach
The total risk of the stock return is the sum of nondiversifiable risk and diversifiable risk. The nondiversifiable risk depends on the factor exposure and the variance of the factor premium, whereas the diversifiable risk equals the variance of the error term, that is,
We already have the estimate for
β
i
. Given the factor premium data {
f
1, … ,
f
T
}, finding the estimate for
V
(
f
t
) is straightforward:
The estimate for
V
(
ϵ
i
) is obtained naturally from estimation of the factor exposure if the factor exposure was estimated by the standard approach in Section 7.5.1. However, if the factor exposure was estimated by the approach in Section 7.5.2, we need to use an alternative approach. Given the estimate of the factor exposure and constant
and
the estimate for
V
(
ϵ
i
) is as follows:
Table 7.5
shows the decomposition of risk for selected stocks estimated from January 2016 to December 2020. We show the risk
as measured by the variance and the standard deviation. Note that the relative size of the diversifiable risk varies quite a bit across stocks.
TABLE 7.5
Risk Decomposition for Selected Stocks
When we get to the stage of finding the optimal portfolio, we also need to know the correlation among stock returns. The correlation between two stocks’ returns has two parts: the correlation between the nondiversifiable components and the correlation between the diversifiable components. The covariance between two stock returns
r
i
and
r
j
is
The estimate for
C
(
ϵ
i
, ϵ
j
) can be found from estimation of the factor exposure, that is,
In practice, however, unless
T
is quite large, it is conventional to assume that
C
(
ϵ
i
, ϵ
j
) is zero. If there are
N
stocks, then
N
(
N
−1)/2 covariances should be estimated. Unless
T
is large, not all these covariances can be estimated precisely. If the model is good, it does not create too much distortion to assume that the covariance is zero. Diversifiable risks, the
ϵ
terms, can be diversified out of the portfolio and ignored, so their covariance ought to be negligible as well.
7.6.2 When the Standard Approach Fails
If a stock is new and lacks data, then
V
(
ϵ
i
) cannot be estimated in a conventional way. However, even if a stock is new, it usually has at least a short trading history. Thus it may be possible to estimate the variance of the error term at a higher frequency (shorter time interval) and recover the variance of the frequency that we need.
For the purposes of illustration, let us assume that the time interval of the analysis is a month. Suppose that for young stock
A
the available data cover only a few days. In this situation, we can recover the variance of the monthly error term from the variance of the daily error term. We use letter
s
to indicate the daily time interval. The data for stock
A
are available for
S
days,
s
= 1, … ,
S
. Let
be the return to stock
A
on day
s
. Given the factor exposure and
constant estimate
and
we can estimate the variance of the daily error term
that is,
where
is the factor premium for day
s
.
20
To recover the variance of the monthly error term, first we identify the stocks that are similar to stock
A
based on the characteristics, as explained in the preceding section. Suppose that stocks 1, … ,
M
are such similar stocks. Then we estimate the variance of the daily error term for those similar stocks,
as well as the variance of the monthly error term for those similar stocks,
. Assuming that the ratio of the monthly variance to the daily variance is similar for similar stocks, we can estimate the monthly variance of stock
A
as
This procedure will allow the estimator to have less extreme values because we are scaling the monthly variance from similar stocks.
7.7 CONCLUSION
In this chapter we turned our attention from one major tool of QEPM—the fundamental factor model—to the other—the economic factor model. The economic factor model, like its counterpart, relates a stock’s return to its factor exposures and the factor premiums that the marketplace assigns them, but it emphasizes the fact that stock returns react to changes in the overall economic environment. The economic factor model is one of the most theoretically sound models of stock returns and, at the same time, one of the most flexible in terms of the variety of factors it can handle.
The conceptual distinctions between the economic and fundamental factor models can confuse even the most experienced practitioners. We pointed out that the major difference between the two models is the fact that in the economic factor model the
factor exposure of each stock must be estimated from the data, whereas in the fundamental factor model statistical estimation is instead necessary for the factor premium. For an economic factor model, for instance, we must estimate how much a company’s stock reacts to a shift in unemployment or real GDP growth. Another difference between the models is that the economic factor model encapsulates a straightforward, intuitively appealing concept: stocks react to external risks in the marketplace. Even when data are scarce, such as with recent IPOs or recently merged companies, this model can help us to gauge how stocks will respond to the economic environment.
The two factor models achieve similar ends, though. Like the fundamental factor model, the economic factor model can be a model of either overall stock returns or of benchmark
α
, providing a performance metric for benchmarked portfolios. It can be used to predict the expected return and expected risk of any stock in the portfolio manager’s investment universe, as well as decompose the risk of any stock into diversifiable and nondiversifiable components. Both factor models serve as essential tools as we move toward
Chapter 9
and strive for the final frontier of portfolio construction, the optimal portfolio. Before we can construct a portfolio, though, we need to gather inputs that are necessary in order to make predictions about future stock returns.
QUESTIONS
7.1.
Explain why the capital asset pricing model (CAPM) is a special case of the economic factor model.
7.2.
Explain why the economic factor model is typically estimated from time-series data.
7.3.
Explain why the factor premium is treated as observable in the economic factor model but not in the fundamental factor model.
7.4.
Discuss the strengths and weaknesses of the economic factor model compared with the fundamental factor model.
7.5.
If the benchmark is a broad market index, can benchmark
α
be interpreted as CAPM
α
?
7.6.
Consider a simple economic factor model:
Suppose that the estimation produced
and
. The portfolio manager has a benchmark whose return is denoted as
r
B
.
(a)   Calculate the benchmark
α
when the benchmark return and the factor premium are identical.
(b)   Calculate the benchmark
α
when the benchmark return and the factor premium are perfectly correlated.
(c)   Express the benchmark
α
as a function of the following three quantities: the correlation between
r
B
and
f
, the variance of
r
B
, and the variance of
f
.
(d)   Specify the exact condition under which multifactor
α
is identical to benchmark
α
.
7.7.
Describe three ways to calculate the factor premium.
7.8.
Based on the capital asset pricing model (CAPM), a broad market index is often included as a factor in the economic factor model. Would it be a good idea to use the Dow Jones Industrial Average for this purpose?
7.9.
Consider an economic factor model with the following three factors: the size factor (i.e., based on the market capitalization), the return on the S&P 500, and the return on the S&P 600. What problem would you encounter in estimating such a model?
7.10.
In the financial economic literature, the factor premium is assumed to have a mean of zero. One way to satisfy this assumption is to write the economic factor model as
r
i
=
α
i
+
β
i
1
[
f
1
−
E
(
f
1
)] + … +
β
iK
[
f
K
−
E
(
f
K
)] +
ϵ
i
Would the estimation of this equation result in different estimates of
β
i
1
, …,
β
iK
? How about the estimates of
α
i
?
7.11.
Suppose that there is an exact linear relationship between the expected stock return and firm size; that is,
E
(
r
i
) = 5 + 0.01
x
i
where
x
i
is the size of firm
i
. Assume that
x
i
is uniformly distributed between 100 and 900. (That is, every value between 100 and 900 has equal probability of being realized.)
(a)    To calculate the size premium, we may sort all the firms by size and create two size-sorted portfolios. That is, we assign the top 50% of the firms to the large-size portfolio and the remaining 50% of the firms to the small-size portfolio. Each portfolio is equal-weighted. The factor premium is defined as the difference between the two portfolios’ returns. What would be the expected value of the factor premium?
(b)    Instead of making two portfolios, we may create three size-sorted portfolios, each containing 33.3% of firms in the sample. Each portfolio is equal-weighted. The factor premium can be defined as the difference between the first portfolio return and the last portfolio return. What would be the expected value of the factor premium?
(c)    Does it matter how many portfolios we create to calculate the factor premium? Do we always get the same expected factor premium?
7.12.
Principal-component analysis is used quite often in psychology. For example, a psychologist could have given a test with 100 multiple-choice questions to 1,000 subjects. The answers to each question are treated as a single series, and principal-component analysis can identify a small number of factors that together explain most of the variations in the answers. Then the psychologist is able to interpret each factor by examining the components of each factor (e.g., “This factor represents aversion to the color red,” “This factor represents childhood trauma,” etc.). In applying principal-component analysis to stock returns, however, portfolio managers cannot easily interpret what each factor really means. Explain why portfolio managers have more difficulty in interpreting factors than psychologists do.
7.13.
Discuss whether principal-component analysis is free from the danger of data mining.
7.14.
When firm
A
and firm
B
merge, we may use the weighted average of the premerger factor exposures of the two firms as the factor exposure for the new merged firm.
(a)    Show that the expected return implied by the factor exposure of the merged firm is the weighted average of the premerger expected returns of the two original firms.
(b)    If there is synergy from the merger, would the procedure just described be reasonable?
7.15.
After estimating an economic factor model for stock
A
, we obtained the following decomposition of the risk:
Nondiversifiable risk    90
Diversifiable risk    60
The risk is measured in variance.
(a)    What is the
R
2
of the regression?
(b)    Explain the relationship between
R
2
and the decomposition of risk.
1
The material we present in this chapter is based on Chen et al. (1986), Fama and French (1993), Lehmann and Modest (1988), and Connor and Korajczyk (1988), who based their arguments on Ross (1976). Chen et al. developed a model for economic factors, whereas Fama and French developed a model for fundamental factors. Lehmann and Modest (1988) and Connor and Korajczyk (1988) developed models for statistical factors. All these academic studies are based on the arbitrage pricing theory of Ross (1976).
2
The economic factor model can process fundamental factors, but it still frames them this way. Since the basic equations of both the economic and fundamental factor models are the same, though, they yield similar results when they use the same factors. Please see
Chapter 3
for further explanation of the equivalence of the models.
3
Bear in mind that the only risk that matters to a diversified investor is the nondiversifiable risk.
4
If you compare
Eq. (7.1)
to
Eq. (6.2)
very carefully, you will find one difference: the constant term
α
does not have subscript
i
in
Eq. (6.2)
. Subscript
i
was not necessary in
Eq. (6.2)
as we presented the simplest version of the fundamental factor model. A more sophisticated version of the fundamental factor model is discussed in
Chapter 16
, where subscript
i
is necessary.
5
Typically, when we estimate these factor models, we use information at time
t
to predict returns at time
t
+ 1. For convenience, we sometimes write in this book the equation with time subscript
t
everywhere, as we do here. The factor exposure and the returns are at time
t
. The equation should still be interpreted as using information at time
t
to predict returns at time
t
+ 1. In other words, the factor exposure at time
t
is really the factor exposure value as of the end of the previous period,
t
− 1, which we may refer to, sometimes, as the beginning-of-month exposure for time
t
.
6
Refer to
Chapter 6
for a discussion of the risk-free rate and investment universe decisions.
7
Chen et al. (1986), Lehmann and Modest (1988), and Connor and Korajczyk (1988), who used nonfundamental factors, report rather limited out-of-sample predictive power of their models. On the other hand, Fama and French (1993) and Daniel and Titman (1997) and others who used fundamental factors generally report higher predictive power. See also
Chapter 16
.
8
See
Chapter 9
for a discussion of how to control for the tracking error.
9
See Section 6.3 of
Chapter 6
.
10
The reader should consult
Chapter 2
, where we discussed the various types of
α
’s that are used in the portfolio management world.
11
People sometimes use the variation from the mean as the factor premium to reflect the idea that what matters is the surprise of the variable, not the level of the macro variable. This surprise approach, however, does not improve the model unless the deviation from the mean really reflects the surprise. It is not easy to measure the magnitude of the surprise.
12
We used the one-month Treasury bill return downloaded from the website of Professor Kenneth R. French of Tuck School of Business:
https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html
.
13
If there are clear breaks elsewhere in the list, then divide the list accordingly. In the absence of other clear breaks, use 33% as the default cutoff value.
14
For size, we use the log of market capitalization and for value, we use the B/P ratio.
15
For further details, see page 399 of Srivastava (2002).
16
We are assuming that the number of time intervals is constant across stocks. This does not have to be the case in general. If the number of time intervals is different for different stocks, we would indicate the number of time intervals
T
with the subscript
i
.
17
One might not think of Apple as a defensive stock, but it could be that the iPhone has become a staple for individuals and thus has altered the way Apple’s stock price behaves.
18
This is one method to approach the problem, especially when running models on a large database of firms. In some cases, the analysis is much more complex, such as when the acquiring firm does so by issuing much more debt.
19
See Chincarini and Kim (2001) for the application.
20
When factor premiums are not available on a daily frequency, we have to make certain approximations, such as calculating a daily premium by dividing the monthly number by the number of trading days in the month.
