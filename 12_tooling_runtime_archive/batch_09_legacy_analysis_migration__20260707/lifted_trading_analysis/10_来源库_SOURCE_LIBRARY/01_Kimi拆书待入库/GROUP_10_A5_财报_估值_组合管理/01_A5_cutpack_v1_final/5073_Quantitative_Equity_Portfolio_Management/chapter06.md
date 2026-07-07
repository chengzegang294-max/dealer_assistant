# Quantitative Equity Portfolio Management: An Active Approach to Portfolio Construction and Management, Second Edition

- **book_name**: 5073 Quantitative Equity Portfolio Management, Second Ed.
- **main_source**: epub
- **cross_check_source**: none
- **pdf_role**: not_needed
- **split_scope**: chapter file = chapter06

---

CHAPTER 6
Fundamental Factor Models
In nature there is fundamental unity running through all the diversity we see about us
.
—Mohandas Gandhi
6.1 INTRODUCTION
Recall from
Chapter 3
the central idea of modern financial economics:
The average return of a stock is the payoff for taking risk
. In a factor model, the factor exposure represents the exposure of a stock to some kind of risk. The factor premium quantifies the payoff to an investor who takes on that risk by buying the stock. The average stock return therefore equals the product of the factor exposure and the factor premium:
In the fundamental factor model, the factor exposure is known. It is some observable fundamental characteristic of the stock, such as its market capitalization or book-to-market ratio. The factor premium, on the other hand, is not known. It is the proportionality between the average stock return and the factor exposure, and it must be estimated empirically.
The formula for the average stock return given above can be extended easily to a more realistic case of multiple factors. When there are
K
factors, the factor exposures of stock
i
can be written as
β
i
1
, … ,
β
iK
, and the factor premium can be written as
f
1
, … ,
f
K
.
1
Note that the factor premium does not vary across stocks and therefore does not require the subscript
i
. The return on stock
i, r
i
, can be written as
where
α
is the constant term and
ϵ
i
is the error term (i.e., the part of the stock return that does not depend on the
K
factors).
2
The average of
ϵ
i
is zero, so the average stock return is the cross-sum of the factor exposure and the factor premium
3
:
For the convenience of exposition, we will define
K
-dimensional column vectors
f
and
β
i
as
Then the preceding equation becomes
Using this notation, the average stock return becomes
We can see that the average stock return is simply the product of the factor exposure (
β
i
) and the factor premium (
f
) as before.
4
The average stock return is the payoff for taking risk—but what is this risk exactly? The risk of a stock has two components, diversifiable risk and nondiversifiable risk.
Since investors can eliminate diversifiable risk from their portfolios through diversification, the market only rewards exposure to nondiversifiable risk. Thus we may restate the central idea of modern financial economics as:
The average stock return is the payoff for taking nondiversifiable risk
.
The nondiversifiable risk can be expressed as the product of the factor exposure squared and the risk included in one unit of exposure.
5
We will call the risk of one unit of exposure the
factor risk
. Then we may write
Within the framework of the fundamental factor model, the total risk of a stock (nondiversifiable risk plus diversifiable risk) can be measured by the variance:
Using the same vector notation that simplified the formula for the stock return, the variance formula becomes
where
V
(
f
) is a
K
×
K
-dimensional variance-covariance matrix. In this model we can see each of the components of the total risk. The nondiversifiable component—the part that the market rewards—is the product of the factor exposure squared (
β
′
i
…
β
i
) and the factor premium risk [
V
(
f
)]. The diversifiable component, which an investor can diversify out of his or her portfolio, is the term
V
(
ϵ
i
).
The fundamental factor model can be used to predict both the returns and the risks of stocks, and these predictions can guide a portfolio manager in choosing the best stocks for his or her portfolio. In general, formulating a fundamental factor model involves four broad steps. First, before observing the factor exposure and
estimating the factor premium, there is some preliminary work to do, including deciding on the factors to include in the model, the treatment of the risk-free rate, the time interval and time period of the data, and the investment universe. Second, the factor exposures of individual stocks (
β
i
) must be determined. The third step is to estimate the factor premium (
f
) and the constant
α
from the factor exposure and the return. Finally, an assessment of the total risk should be made by estimating both the factor risk [
β
′
i
V
(
f
)
β
i
, a.k.a. the
nondiversifiable risk
] and the diversifiable risk [
V
(
ϵ
i
)]. We explain these steps in the following sections, and
Table 6.1
summarizes the specifics of the modeling process.
TABLE 6.1
Creating a Fundamental Factor Model
6.2 PRELIMINARY WORK
A sound model begins with good planning. The preliminary work of the portfolio manager is to make a series of decisions that will serve as a blueprint for construction of the model. The primary decision is the choice of factors. Other preliminary decisions determine the shape of the data set (including the nature of the stock returns, the time interval between data points, and the overall time horizon of the data) and the scope of stocks to consider for the portfolio. These general decisions come into play in building any factor model.
6.2.1 Choosing Factors
Factors represent risk. There are all kinds of factors, some of which describe stock characteristics and some of which describe conditions in the overall market.
6
Fundamental factors are observable characteristics of the stock itself, and they usually can be read (or easily calculated) from financial statements. Some technical factors and analyst factors also count as fundamental factors. For reference, here are some representative fundamental factors:
1.
Fundamental valuation factors
: dividend yield, book-to-price ratio, earnings-to-price ratio, and the sales-to-price ratio
2.
Fundamental size factors
: log of market capitalization
3.
Fundamental solvency and financial risk factors
: debt-to-equity ratio, current ratio, and the inverse interest coverage ratio
4.
Fundamental operating profitability factors
: net profit growth, return on assets, and the return on common equity
5.
Technical factors
: 12-month momentum, trading volume, and the short interest ratio
6.
Analyst factors
: analyst rating changes and earnings revisions
Note that economic factors [such as gross domestic product (GDP) and inflation] and behavioral factors (such as consumer sentiment) do not fit in the fundamental factor model because neither of these types of factors really can be called a characteristic of the stock itself. Rather, they measure risks in the market that affect all
stocks. Statistical factors, which must be derived from stock-return series, do not belong in the fundamental factor model either.
The astute reader will notice that when listing some of the more common factors, we describe their inverse. This is different than how we used these factors in
Chapter 4
. For example, most investors refer to the price-to-earnings ratio of a company rather than the earnings-to-price ratio. The reason for using the inverse is very practical. When companies have negative earnings, their P/E ratio doesn’t really have any meaning. As a result, it does not make sense to argue that a low P/E ratio company is “cheaper” than a high P/E ratio company when companies with zero or negative earnings are included. However, if we calculate the E/P ratio of companies, we have a ratio that can be compared across companies, which makes a lot more sense. For example, a company with a very high P/E ratio will have a very small E/P ratio but will still be considered relatively “cheaper” than a company with a negative E/P ratio. In practice, some practitioners use P/E and exclude stocks with negative earnings, while others use E/P and have a larger set of stocks to choose from.
7
The key point is that by using the inverse of certain common factors, we are able to analyze many more stocks, which offers a much richer view for stock selection. In the remainder of this book we shall use factors that allow us to evaluate many more stocks, even if the definitions are slightly altered from what the typical investor is accustomed to.
6.2.2 Treatment of the Risk-Free Rate
The factor premium in a fundamental factor model has to be estimated by looking at the relationship between stock returns and factor exposures. The reliability of the model therefore depends greatly on the quality of the stock return data that are used to estimate this relationship. Before gathering stock-return data, the portfolio manager must confront a larger theoretical question: how much of a stock’s return comes from the stock itself, and how much could have been earned on any investment? The investor earns a portion of the average stock return for free—not as a reward for taking on risk. The reward for taking on risk by buying a stock is therefore the average stock return in
excess of a risk-free rate
.
In order to focus on the portion of the stock return that actually rewards risk, some portfolio managers subtract a risk-free rate from the stock return before implementing the fundamental factor model. While a theoretically sound move, this is not easy to do in practice. The problem is that it is difficult to identify a truly risk-free asset, the return on which could be considered the risk-free rate. Financial economists tend to use the return on short-term U.S. Treasury bills as the risk-free rate because U.S. Treasury bills are considered a very safe investment. Yet they are not completely risk-free assets. Money market funds (MMFs), another substitute for the theoretical risk-free asset, certainly contain a level of risk as well.
8
Given the difficulty of identifying the true risk-free rate, subtracting an estimated risk-free rate might seem like an arbitrary practice. We believe, however, that a model that adheres to risk-reward theory by adjusting for the risk-free rate will provide more accurate results than one that does not. Given the return of stock
i
at time
t, r
it
, and the risk-free rate at time
t, r
ft
, we define the excess return
as
In subsequent calculations, we can replace
r
it
with
to adjust for the risk-free rate.
6.2.3 Choosing the Time Interval and Time Period
Two other interrelated questions also affect the quality of the data set: what time interval should fall between the data points, and what overall time horizon should the data set cover? Ideally, the time interval should reflect the investment horizon (i.e., the rebalancing frequency). If the portfolio is rebalanced every month, a monthly interval should be used. If the portfolio is rebalanced every year, an annual interval should be used. This will make things easier in the later stages of analysis.
However, consideration of the estimation precision may force the portfolio manager to choose a time interval different from the investment horizon. The fundamental factor model assumes that the factor exposure of a stock determines its average return. The
statistical estimation of the relationship between the factor exposure and the stock return will be imprecise unless the relationship is stable over the given time interval. For example, the stock return could have a stable relationship with the factor exposure for one month but not for an entire year. In that case, it would hardly make sense to set the time interval to a year, even if rebalancing occurs annually. At the same time, if the time interval is too short, the precision of the estimation again may decline because short-term fluctuations in the stock return may be random and unrelated to the factor exposure. Nonetheless, it is generally best to err on the side of a shorter time interval rather than a longer one. One can forecast the results of a longer time interval from the results of a shorter time interval, but not vice versa.
9
In practice, financial economists tend to prefer a monthly interval and, to a lesser degree, a weekly interval. Daily and annual intervals are rather uncommon.
The overall time period that the data cover (in statistical jargon, the
sample period
) should be decided in light of the estimation precision as well. If the time period is too short, so that the data encompass only a small number of time intervals, then the estimation precision may suffer. The general rule of estimation precision is: the larger the sample, the higher is the precision. However, if the time period covers many years, then the relationship between the stock return and the factor exposure may change over the course of the period. It is unlikely that the premium on any given factor will remain constant for an entire decade, for example. A very long time period also means that the data will cover more time intervals. The more time intervals, the more data points there are to collect, and the bigger will be the problem of finding complete data for a stock. Financial economists tend to include between 36 and 60 time intervals in their analyses when using a monthly interval (so that the total time period is three to five years). When using a weekly interval, the number of time intervals tends to be greater than 60 (while the overall time period tends to be shorter than three years). When using a quarterly or annual interval, the number of time intervals tends to be much smaller (while the overall time period is generally longer than five years).
We will use the lowercase letter
t
to indicate one time interval. For example,
r
it
represents the return to stock
i
at time
t
, whereas
β
it
denotes the factor exposure of stock
i
at time
t
. We will use
capital letter
T
to indicate the number of time intervals used in the analysis. Thus
t
will take an integer value from 1 to
T
. We write the relationship between the stock return and the factor exposure as
where, as before,
β
it
and
f
are
K
-dimensional column vectors, and
r
it
and
ϵ
it
are scalars.
10
6.2.4 Choosing the Universe of Stocks
In addition to questions of the nature and time span of the data, the portfolio manager faces the question of how many stocks to consider when applying the model. There already may be external restrictions on the investment universe of the portfolio. The portfolio may be limited, for instance, to technology stocks, value stocks, or stocks of some other stripe. Whether or not that is the case, the portfolio manager may have his or her own preliminary screening strategy that will narrow the list of potential investments. As we discussed in
Chapter 5
, many well-known portfolio managers put their stamp on a portfolio with a signature stock screen.
In the absence of external restrictions on the investment universe, there is no need (from a technological standpoint) to shrink the investment universe preliminarily. Given the current state of computing technology, the number of stocks is not really an issue. Even a personal computer can handle thousands of stocks without much trouble.
The size of the stock universe does affect some aspects of implementation, though. A very large investment universe provides a large pool of stocks from which to select. The bigger the selection pool, the more likely it is that there are high-return stocks somewhere in the pool. Yet calculation of stock correlations loses precision as the number of stocks in the pool increases, making the model less and less reliable. Thus, even though plenty of good
stocks may be floating around, it is harder to identify them. For this reason, we do not recommend starting with an investment universe of more than a few thousand stocks.
6.3 BENCHMARK AND
α
Many portfolio managers have a specific benchmark against which they measure the performance of their portfolios. If the portfolio manager aims to outperform a benchmark while minimizing the portfolio’s tracking error, then the benchmark must play a role in the model.
One approach to incorporating the benchmark into the fundamental factor model is to use the model to predict only the residual return rather than the entire stock return. The residual return is the part of the stock return not correlated with the benchmark. To transform the model into one of residual return, we need to run a regression of the stock return on the benchmark.
Given the stock return
r
i
and the benchmark return
r
B
, we estimate the following equation:
The typical way to estimate this equation is to use a time-series regression. We find the stock return and the benchmark return over many time periods, say,
r
i
1
, … ,
r
iT
and
r
B
1
, … ,
r
BT
, where the second subscript refers to time periods. After estimating
and
we define the residual return
as
Once the residual return is defined, the portfolio manager can use the fundamental factor model to predict the value of the residual return. To do so, he or she simply substitutes the residual return for the stock return given in the fundamental factor model in
Eq. (6.2)
.
The portfolio manager’s value-added is wrapped up in the term
(also known as
α
B
). Note that the expected return and the risk of the last term
are already known from the preceding estimation. The term with flexibility to boost the residual return is
What the portfolio manager does with this fundamental factor model is therefore all about
.
11
An alternative way to account for the benchmark, rather than predicting the residual stock return, is to add the benchmark to the model as one of the factors. This approach fits better with the economic factor model, however, so we will delay discussing it until the next chapter.
12
Accounting for the benchmark at this point in the modeling process, though useful, is not necessary. Some portfolio managers prefer to deal with the benchmark at a later stage in the process by, for instance, controlling for the tracking error in construction of the portfolio. This approach may make the most sense if the composition of the benchmark is known clearly.
13
6.4 FACTOR EXPOSURE
The factor exposure quantifies the exposure of a stock to risk. In the fundamental factor model, the factor exposure is the value of some observable (or easily calculable) characteristic of the stock. In some cases, the factor exposure shows up right in a company’s financial statements or on a price-volume chart. In other cases, a straightforward calculation drawing on figures from financial statements is enough. In other words, once the factors are chosen, determining the factor exposure is rarely a challenging task.
Table 6.2
presents the factor exposures of selected stocks for five commonly used factors. The E/P ratio is the annual earnings per share divided by the share price. The B/P ratio is the value of common equity reported in the company’s balance sheet divided by the share price.
14
The D/E ratio is the total value of liabilities divided by the total value of equity reported in the balance sheet. LOGSIZE is the natural log of the market capitalization of the company (in millions of dollars), where market capitalization is defined as the share price multiplied by the number of shares outstanding. Momentum (M12M) is the average monthly return (as a percentage) over the previous 12 months.
TABLE 6.2
Factor Exposure of Selected Stocks
From the table we can see that Amazon (AMZN) has a low earnings-to-price ratio of 0.0083 (i.e., a high price-to-earnings ratio of about 120) likely owing to expectations of rapid earnings growth. J.P. Morgan Chase (JPM), on the other hand, has a relatively high earnings-to-price ratio. If the factor premium for the earnings-to-price ratio were negative, then—all other things being equal—we would expect Amazon to have a higher return than J.P. Morgan Chase. Conversely, if the factor premium for the earnings-to-price ratio were positive, we would expect J.P. Morgan Chase to perform better than Amazon.
Looking at another factor, we see that momentum is very high for Apple and Amazon (reflecting their exceptional returns in 2020), whereas it is negative for J.P. Morgan Chase (reflecting its losses in value during the year). We may be able to predict which of these stocks will have the highest return in the following year if we determine the factor premium for momentum. If the factor premium were positive, we would expect Apple and Amazon to perform better than J.P. Morgan Chase.
Factor exposures change over time, and we need to be sure to assign the correct values to the correct dates. For monthly time intervals, it is standard practice to use the factor exposure recorded at the beginning of the month (or, alternatively, the value recorded at the end of the previous month). In calculating the earnings-to-price ratio (E/P), the book-to-price ratio (B/P), and the log of market capitalization (LOGSIZE) for this table (which shows factor exposures at the beginning of December 2020 or, alternatively, at the end of November 2020), we used the closing stock prices and shares outstanding as of November 30, 2020. In calculating momentum, we used the stock returns from December 2019 through November 2020.
15
Extra care needs to be taken in applying data from a company’s financial statements. Companies release their financial statements quarterly but not immediately when the fiscal quarter ends. As of the beginning of December 2020, the most recently released financial statements might represent the second or third quarter of 2020. Since we use quarterly data in calculating the earnings-to-price ratio, we used the earnings for the 12-month period ending in August, July, or June, depending on when a company’s fiscal quarter ended. If the fiscal quarter was over in September, the earnings for the July–September quarter might not be known by the beginning of December, so we did not use them to calculate the earning-to-price ratio. For the same reason, we used only figures for fiscal quarters ending in or before August to calculate the book-to-price and debt-to-equity ratios. Generally, it is reasonable to allow two to three months’ lag between the end of a fiscal period and the reporting of the variable.
Table 6.3
summarizes this timing scheme.
TABLE 6.3
Assigning the Correct Values to the Correct Time for December 2020
After all the factor exposures are determined, we collect the numbers and save them as a set of vectors {(
β
11
, … ,
β
N
1
), … , (
β
1
T
, … ,
β
NT
)} where
β
it
is the factor exposure of stock
i
for time
t
. For example, the factor exposure of Apple for December 2020 is (from
Table 6.2
)
We can read similar information for other stocks (different
i
’s) and for other time periods (different
t
’s) in a similar way.
6.5 THE FACTOR PREMIUM
The factor premium is the payoff for each unit of factor exposure, or exposure to risk, that the stock possesses. In the fundamental factor model, the factor premium is estimated from the pooled cross-sectional regression (i.e., panel regression) of the stock return on the factor exposure. Estimation of the factor premium with a regression is possible because the premium likely remains constant over several years
16
and across stocks.
Given the returns of
N
stocks over
T
time periods, {(
r
11
, …,
r
N
1
), …, (
r
1
T
, …,
r
NT
)}, and the factor exposures of
N
stocks over
T
time periods, {(
β
11
, …,
β
N
1
), …, (
β
1
T
, …,
β
NT
)}, we can estimate the following equation:
There are a number of ways to estimate this equation. The simplest is the ordinary least squares (OLS) approach. While the OLS estimator is simple to obtain, it may not be the most reliable estimator. We suggest that portfolio managers do a number of robustness checks on it and then decide whether to use a more sophisticated technique.
6.5.1 OLS Estimator of the Factor Premium
The OLS estimator of the factor premium
f
is given as
17
where
The constant
is calculated as
The standard error for the factor premium is the square root of (the diagonal elements of) the following variance:
where
is the estimated variance of
ϵ
it
, that is,
Table 6.4
presents the factor premium estimates and their standard errors. We made the estimations for Standard & Poors
(S&P) 500 stocks in the period from January 2016 to December 2020. If we look at the E/P ratio factor premium for a moment, we see that it is −3.425. A negative premium indicates that a high factor exposure hurts stock returns. In the case of the E/P ratio factor, the expected stock return will drop by 3.425% for every unit of exposure. To some, these results may seem counterintuitive, since we are familiar with the value anomaly. However, over a short horizon, as with this period, the realized premium may be different than the long-term premium, and this failure of “value” consumed much of the talk in the quant world from 2016 to 2020.
TABLE 6.4
The Factor Premium
Standard errors indicate how precise the estimates are. Small standard errors suggest that the estimates are very precise. For the E/P ratio and 12-month momentum, the standard errors are small enough to make the factor premiums “significant” in a statistical sense. For example, we can say with 95% certainty that the “true” value of the E/P ratio premium is approximately between −4.235 and −2.615, whereas the “true” value of the M12M premium is approximately between −2.807 and −1.999.
18
6.5.2 Robustness Check
A model is not usually an exact description of reality, only a good approximation of it. In statistics, shortcomings in the model are called
specification errors
.
19
Specification errors arise in any regression, and estimation of the factor premium is no exception. Yet we should strive to build models that reflect persistent and stable
patterns, as described by tenet 6 of quantitative equity portfolio management (QEPM). With a robustness check, we can gauge whether the factor premium estimates are stable when small details of the estimation change. If the current estimation is not robust, we ought to try an alternative estimation technique.
To check the robustness of the estimation, split the data set into a few subsets and see whether the estimates are very different across the subsets. They should not be too different if the estimation is robust. Subsets can be created along the time dimension. For example, we can estimate the factor premiums for the period from January 2016 to June 2018 and the period from July 2018 to December 2020, as reported in
Table 6.5
. Subsets also can be divided along the cross-sectional dimension. For example, we can estimate the factor premiums for different sectors, as shown in
Table 6.6
. These two tables suggest a certain level of stability across time and sectors.
20
TABLE 6.5
The Factor Premium for Subperiods
TABLE 6.6
The Factor Premium for Various Economic Sectors
6.5.3 Outliers and MAD Estimator of Factor Premium
The weakness of the OLS method is that in trying to minimize the sum of the squared residuals, it is highly sensitive to outliers. If a robustness check indicates that the OLS estimator is very unstable, it may be necessary to use an alternative estimation procedure that is less sensitive to outliers.
The
minimum absolute deviation
(MAD) estimation, also known as
median estimation
, is one such alternative. The MAD minimizes the sum of the absolute value of residuals rather than the squared residuals. Since this approach avoids squaring the residuals, any outliers have a much smaller effect on the estimate than they do in the OLS approach. Standard statistical software supports the MAD approach.
Table 6.7
shows the MAD estimates of the factor premiums in our example. We again performed an estimation using S&P 500 stocks for the period January 2016 to December 2020. Note that the earnings-to-price ratio (E/P) changed its sign from being significantly negative to significantly positive when we shifted from the OLS to the MAD approach. This implies that primarily outliers are driving the E/P ratio estimate here.
TABLE 6.7
The MAD Factor Premium
6.5.4 Heteroscedasticity and Autocorrelation-Consistent Estimation of the Standard Error
While OLS estimation often produces a not-so-reliable output, it has been the standard empirical tool for many generations of empirical analysts. Moreover, adopting an alternative estimation technique risks introducing additional errors, since every estimation technique is based on its own set of assumptions—and these assumptions may not be any more realistic than the assumptions driving OLS. Given this consideration, one popular approach is to continue to report the OLS estimates but at the same time to make adjustments for the standard errors so that certain assumptions of the OLS estimation are relaxed. More specifically, when calculating standard error, we may wish to relax two of the OLS assumptions: (1) that all the error terms of different firms have the same variance (the assumption of homoscedastic errors), and, (2) that the error terms of different time periods are independent (the assumption of no autocorrelation). The standard errors that we obtain after relaxing these two assumptions are called
heteroscedasticity- and autocorrelation-consistent standard errors
or, in short,
HAC standard errors
. Even for HAC standard errors, we do maintain certain restrictions regarding the error terms. For example, with HAC, we do not allow error terms of different firms to be correlated (though we allow error terms of one firm for different periods to be correlated). Also, HAC requires error terms of one firm for different periods to have the same variance (though we allow error terms of different firms to have different variances). The maintained assumptions guarantee that the OLS estimates are still consistent (i.e., correct if the sample is large enough), though they may not be the most efficient (i.e., there may be other
estimates with greater precision). Under the assumption of heteroscedastic and autocorrelated errors, the variance of the factor premium can be calculated as
where the residual
is calculated from the OLS estimate as
Compared to the simple variance formula in
Eq. (6.21)
, we now have a rather complicated formula. Looking closely, however, one may note that the first and last terms are identical. (For this reason, the formula is sometimes referred to as a “sandwich formula.”) The first and last terms represent the variation of factor exposure
β
it
whereas the middle term represents the variance of
β
it
. The HAC standard errors are simply the square root of the diagonal elements of the variance matrix shown above.
Table 6.8
shows the HAC standard errors together with the OLS estimates of factor premiums. The earnings-to-price ratio and the book-to-price ratio have noticeably higher standard errors compared to the unadjusted standard errors shown in
Table 6.4
. That is, the premiums for these two factors are not precisely estimated, and the standard errors shown in
Table 6.4
exaggerate the precision for these two premiums.
TABLE 6.8
The HAC Standard Errors along with the OLS Estimates
6.6 DECOMPOSITION OF RISK
Given the factor exposure
β
i
, the factor premium estimate
and the constant estimate
we can calculate the average stock return as the product of these two plus the constant,
To construct the optimal portfolio, however, we need to know the risk of the stock return. In the fundamental factor model, the risk of the stock return has two components: nondiversifiable risk captured by
and diversifiable risk captured by
The total risk of the stock return is simply the sum of these two risks. Let’s look at each of these two in turn.
Nondiversifiable risk arises from the randomness of the factor premium. Within the estimation sample, however, both factor exposure
β
i
and factor premium
vary over time, and it is not necessary to separate these two components. For the purpose of risk decomposition, we carry out a series of cross-sectional regressions, one regression for each month
t
, rather than a single pooled regression. From the regression for month
t
, we obtain factor premium and constant estimates
and
By repeating the regressions for all the sample months, we obtain a time series of factor premium and constant estimates,
and
. By multiplying the factor premium by the factor exposure and adding the constant, we also obtain a time series of
We can calculate the sample variance from this time series as
This variance, or the sample standard variation obtained by taking the square root of the variance, is our measure of nondiversifiable risk.
The diversifiable risk represents the part of the variation in the stock return that the variation in the model’s factors cannot explain. This part of the stock’s variation appears as the error term
ϵ
i
, that is,
. The procedures outlined in the previous paragraph provide an estimate of the variance of the error term:
This variance is our measure of the diversifiable risk. One can alternatively use the square root of the variance (standard deviation) as
a measure of risk. The total risk of stock
i
is simply the sum of the two risk components:
Table 6.9
shows the decomposition of risk for selected stocks estimated from January 2016 to December 2020. We report the risk in terms of the variance and the standard deviation.
TABLE 6.9
The Risk Decomposition for Selected Stocks
When we get to the stage of finding the optimal portfolio, we also need to know the correlations between stock returns. The total risk of a stock is composed of nondiversifiable risk and diversifiable risk. Likewise, the total return on a stock is composed of nondiversifiable and diversifiable components. The correlation between the returns on a pair of stocks consists of the correlation between their nondiversifiable components and the correlation between their diversifiable components. Instead of correlation, we will use covariance; the covariance between
r
it
and
r
jt
is
In practice, we estimate only the correlation between the nondiversifiable components of two stocks’ returns. As for the diversifiable components, the correlation between them can, in principle, be estimated in a straightforward way using the standard estimation technique. In practice, though, it is rarely done this way. One reason is that there are often simply too many parameters to estimate precisely. If there are
N
stocks, then [
N
(
N
−1)]/2 covariances have to be estimated. These covariances cannot be estimated precisely without using a great many time intervals for the estimation. The second reason that the standard estimation technique is hardly used to estimate the diversifiable component of the return is that the diversifiable return, like diversifiable risk, has little bearing on the stock return to the investor (or so says modern financial economic theory). For both these reasons, the convention is to assume that diversifiable risk
C
(
ϵ
it
, ϵ
jt
) equals zero.
6.7 CONCLUSION
In this chapter we explored one of the most common models of stock returns, the fundamental factor model. Factor models relate the return of a stock to the stock’s exposure to risks (a.k.a.
factor exposures
) and the market’s payoff to investors for taking on those risks (a.k.a.
factor premiums
). We showed how the fundamental factor model can act as a model of overall stock returns or, for managers who track an index, as a model of benchmark
α
. We explained how to obtain a stock’s fundamental observable factor exposures and how to estimate the factor premiums that the market awards them. With the factor exposures and factor premiums in place, the fundamental factor model can predict the expected return and expected risk of any stock in a portfolio manager’s investment universe. The model also can decompose the risk of a stock into its diversifiable and nondiversifiable components. The fundamental factor model is one basic tool for constructing a portfolio. In the next chapter we will take a look at an alternative tool, the economic factor model, that the portfolio manager also can use to predict and analyze stock returns and risks.
QUESTIONS
6.1.
Describe the main steps in creating and estimating a fundamental factor model.
6.2.
Explain why economic factors such as GDP and behavioral factors such as consumer sentiment cannot be included in a fundamental factor model.
6.3.
One strength of the fundamental factor model over the economic factor model is that the data requirement is relatively small. What is the minimum data requirement to estimate the fundamental factor model? Is it possible to estimate the fundamental factor model from a single cross section (i.e., the observation of many stocks in one time period)?
6.4.
It is possible to derive returns of many periodicities from returns of one periodicity. Suppose that we have estimated the following fundamental factor model using daily data:
Let us denote the estimates by
and
(a)   What would be the expected daily return and the variance of the daily return?
(b)   Assuming that error
ϵ
i
is serially uncorrelated over time, what would be the expected weekly return and the variance of the weekly return?
(c)   Under the same assumption as in part (b), what would be the expected monthly return and the variance of the monthly return?
(d)   Is the assumption made in parts (b) and (c) realistic?
6.5.
It makes a difference whether one includes the risk-free rate in the model. Consider two versions of a fundamental factor model:
where
r
f
is the risk-free rate.
(a)   If
r
f
is constant for the estimation period, what is the relationship between the estimates of
α
(1)
,
f
(1)
, and
σ
(1)
and those of
α
(2)
,
f
(2)
, and
σ
(2)
?
(b)   Would your answer to part (a) be different if
r
f
is not constant but is not correlated with any of the variables in the model?
(c)   Under what conditions does the inclusion of the risk-free rate in the model not change the estimates?
6.6.
Consider a fundamental factor model with many factors:
The goodness of fit of the regression can be measured by the adjusted
R
2
:
where
N
is the number of observations,
K
is the number of factors,
is the residual from the regression (i.e., the part of
r
i
that was not explained by the regression), and
V
(·) refers to the sample variance.
(a)   Calculate
when the number of observations is 100, the number of factors is 2, the sample variance of the return is 5%, and the sample variance of the residual is 3%.
(b)   What will happen to
if we keep the number of observations constant and increase the number of factors to 4? Assume that the sample variance of the return and the residual did not change.
(c)   What would be the required number of observations to keep
unchanged when the number of factors increases to 4?
6.7.
Define the residual return. What are the main components of it?
6.8.
Suppose that we estimated a fundamental factor model
r
i
=
α
+
β
i
f
+
ϵ
i
where
β
i
is the size exposure measured in dollars. Would the estimates of
α
and
f
be different if the size exposure were measured in thousand of dollars instead?
6.9.
After estimating a fundamental factor model, we obtained the following estimates:
r
i
= 1.5 + 0.02
β
i
1
+ 0.3
β
i
2
+
ϵ
i
where
β
i
1
is the size exposure of firm
i
, and
β
i
2
is the price-to-earnings ratio exposure.
(a)   What is the expected return of firm
A
whose size is 100 (million dollars) and that has a price-to-earnings ratio of 20?
(b)   What will happen to the expected return of firm
A
in part (a) if the firm size grows by 10 (million dollars)?
(c)   Explain why the factor premium can be interpreted as the marginal effect of the factor exposure on the expected return.
6.10.
The following is the result of the estimation of a fundamental factor model:
(a)    If the sample variance of the factor exposure is 100, what would be the standard error of the coefficient estimate?
(b)    What would be the standard error if the factor exposure were almost constant in the sample?
(c)    Can you come up with a criterion to choose a factor based on your calculation in parts (a) and (b)?
6.11.
Some portfolio managers remove the outliers from the sample before estimating a model. For example, one may decide to drop observations whose values are more than three standard deviations away from the mean. Considering the properties of ordinary least squares, what would be the consequence? Does it matter whether the outliers are determined based on the values of the stock returns or based on the values of the factor exposure?
6.12.
Some portfolio managers may “winsorize” the outliers before using them in the estimation. For example, if the mean of a variable is
μ
and the standard deviation of the variables is
σ
, any value that is greater than
μ
+ 3
σ
or less than
μ
– 3
σ
may be replaced with
μ
+ 3
σ
or
μ
– 3
σ
. Would the estimate of ordinary least squares still be unbiased (true on average)? Does it matter whether the variable we use for winsorization is the return or a factor exposure?
6.13.
One solution to the problem of the outliers is to use the minimum absolute deviation (MAD) estimation instead of the ordinary least squares (OLS) estimation. Under what circumstances do these two estimations produce identical estimates?
6.14.
Some researchers believe that small stocks experience higher variability in stock returns than large stocks do. That is, the variance of the error is believed to be greater for small stocks than for large stocks. Discuss the advantages and disadvantages of HAC standard errors in this situation.
6.15.
Define diversifiable risk and nondiversifiable risk. In what sense can the risk be diversified?
1
This notation requires explanation. It is the convention in statistics to use Greek letters for parameters that must be estimated and to use the more familiar Latin letters for variables whose values can be observed. We do not follow the convention here because in other models of stock returns the factor exposure is the unknown variable, whereas the factor premium is directly observable. To remain consistent across all models, we will always call the factor exposure
β
and the factor premium
f
.
2
Even when we estimate the factor premiums using time series of stock returns and factor exposures, one can think of the regressions as pooled regressions, where the intercept term is a constant.
3
The
expected stock return
, not
the average stock return
, is the correct term to use. We will switch to the technically correct terminology in later chapters.
4
There is an extra constant term in the formula, but it will be zero if the factor exposure is properly normalized and the risk free rate has already been subtracted from the return. This will be discussed in more detail later.
5
Risk can be measured either with the variance or the standard deviation. In the formula shown here, risk is defined as the variance.
6
Please refer to
Chapter 4
for a comprehensive catalogue of factors.
7
For major indices or portfolios, some investors calculate the weighted average of the E/P ratio or related ratio and then invert that average so that it appears to investors in the more common form.
8
It is also important to use a total return risk-free rate index. Sometimes people use the yield of the risk-free rate. Although this might be approximately correct, it’s much better to use the actual total return from the chosen risk-free instrument.
9
Chapter 8
discusses this concept in greater detail.
10
Typically, when we estimate these factor models, we use information at time
t
to predict returns at time
t
+ 1. For convenience, we sometimes write in this book the equation with time subscript
t
everywhere, as we do here. The factor exposure and the returns are at time
t
. The equation should still be interpreted as using information at
t
to predict returns at time
t
+ 1. In other words, the factor exposure at time
t
is really the factor exposure value as of the end of the previous period,
t
− 1, which we may refer to, sometimes, as the beginning-of-month exposure for time
t
. There is also the issue of when a factor exposure was truly available for the portfolio manager. We discuss that issue later in this chapter.
11
Be careful not to confuse ~
α
with the
α
of the model for total stock return in
Eq. (6.2)
. The concept of ~
α
is so important in the investment world that analysts sometimes refer to it simply as
α
. Refer to
Chapter 2
for a discussion of the various
α
’s of investing and their corresponding models.
12
If we use the benchmark as a factor in the fundamental factor model, we need to estimate the factor exposure of each stock in some way. To estimate the factor exposure, we will need to employ the technique we use for the economic factor model.
13
See
Chapter 9
for an explanation of this method.
14
As we explained in
Chapter 5
, there are many advantages to defining certain variables as their inverse. For example, one can analyze many more companies when using the E/P ratio rather than the P/E ratio. One might also notice that unlike in
Chapters 4
and
5
, we no longer have Tesla in our representative 10 stocks. This is because Tesla was not part of the S&P 500 in November of 2020.
15
We do this because in our estimations of factor premiums we estimate regressions over time and need to use the latest factor exposure (i.e., end of the month) against the subsequent monthly return of the stocks. Thus, we use end-of-November factor exposures and end-of-December returns to estimate factor premiums.
16
Though, as noted earlier in this chapter, the premium likely changes over the course of an entire decade.
17
We present the formulas for consistent estimators. For unbiased estimators, the degree-of-freedom correction is necessary.
18
Refer to Appendix C at
www.ludwigbc.com
under QEPM Exclusive Content for more on statistical significance, standard errors, and
t
-statistics.
19
See Appendix C at
www.ludwigbc.com
under QEPM Exclusive Content for more on specification error.
20
Eugene Fama would say that if you really believe a factor model, then you should not expect to see any sector effect on the estimates because the model already should have accounted for it. Nevertheless, it is industry practice to control for sectors with dummy variables.
