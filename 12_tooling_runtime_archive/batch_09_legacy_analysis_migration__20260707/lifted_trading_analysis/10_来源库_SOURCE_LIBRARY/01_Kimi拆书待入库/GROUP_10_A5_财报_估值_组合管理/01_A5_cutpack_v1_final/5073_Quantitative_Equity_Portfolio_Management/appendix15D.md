# Quantitative Equity Portfolio Management: An Active Approach to Portfolio Construction and Management, Second Edition

- **book_name**: 5073 Quantitative Equity Portfolio Management, Second Ed.
- **main_source**: epub
- **cross_check_source**: none
- **pdf_role**: not_needed
- **split_scope**: chapter file = appendix15D

---

APPENDIX 15D
Measuring Market Timing Ability
Although market timing is not usually the forte of the quantitative portfolio manager, there are performance measurement techniques to discover whether the portfolio manager has market
timing ability
as opposed to just general stock-picking ability. Traditionally, these two components have been separated by running either of the following regressions:
The
α
continues to measure portfolio selectivity performance,
β
continues to represent the market exposure of the portfolio, and a positive
γ
indicates market timing ability. The first measure is due to Treynor and Mazuy (1966), and the second measure is due to Henrikkson and Merton (1981). In
Eq. (15D.2)
, a perfect market timer should have a
β
= 1 and a
γ
= 1. This is true for a timer who shorts or goes long 100% the market depending on which does better. Most portfolio managers are not so extreme and will fall somewhere in between, even with perfect ability. There have been squabbles about the potential bias of this measure of market timing [Grinblatt and Titman (1989), Jaganathan and Korajczyk (1986), and Chance and Hemler (2001)]. The reason for this is that one is using the proxy of a monthly put as a market timer measure; however, the portfolio manager may trade daily. Thus one is estimating a misspecified equation. This problem is magnified as the distance
between the decision horizon and the evaluation horizon grows (i.e., it is worse for measuring the timing ability of a portfolio manager who makes daily trading decisions using quarterly data). Given the difficulty of access to daily return data, Goetzmann et al. (2000) propose an alternative estimation:
where
d
is a counter to represent the subperiods within the investment horizon, and the new term is the instrument that simulates a daily market timer’s performance over the month. It is correlated with daily put values on the equity market index without the cost of the put premium. When working with a monthly horizon,
d
indexes the number of days in the month. Thus, in this case, the term after the
γ
is the product of the maximum of the function related to daily return values during the month. This creates an expression for each period
t
, which can be used in the regression. Simulations have shown that this measure is able to correct the bias when the portfolio manager trades on a more frequent basis than the measurement horizon.
1
QUESTIONS
15.1.
What’s the difference between performance attribution and performance measurement? Which should be used to determine bonuses?
15.2.
Why is it especially difficult to compute the returns of an actual portfolio when there are cash flows in and out of the portfolio?
15.3.
(a)    Why do the Global Investment Performance Standards (GIPS) and other associations’ guidelines require time-weighted return measurement as the method of computing the performance of actual portfolios?
(b)    When measuring the returns of separate accounts, clients typically get confused about time-weighted returns and ask to have internal rate-of-return (IRR) calculations produced instead. Why?
15.4.
What is the modified Dietz method?
15.5.
Suppose that portfolio
X
has a closing value of $50 million on day 1. On day 2 there are withdrawals from the portfolio during the day totaling $45 million. The end-of-day value of the portfolio, as measured by the accounting department, is $6 million. Using the Dietz method, what would the performance analyst compute as the daily return of this portfolio? Does the number make sense?
15.6.
(a)    Which is a better measure of risk, standard deviation or semi-standard deviation?
(b)    Under what conditions would standard deviation and semi-standard deviation be equally good measures of risk?
(c)    Which one is used more in practice? Why is that?
15.7.
Refer to the following table with monthly return data on a portfolio and the benchmark.
(a)    What are the standard deviations of the portfolio and the benchmark?
(b)    What is the monthly tracking error of the portfolio? The annualized tracking error?
(c)    Why might it worry you that practitioners use tracking error as a measurement of risk versus the benchmark?
15.8.
Which method would likely be most accurate in reporting the
β
P
of a portfolio versus a benchmark: taking the weighted average of the individual
β
’s of all the stocks in the portfolio or taking the historical portfolio returns and running a regression of those returns against the benchmark to find
β
P
? Why?
15.9.
Suppose that you are running a complicated hedge fund. One of the founding principles of this hedge fund is to invest in a variety of
n
strategies. Any pair of these strategies has a correlation of
ρ
(you also can think of this as the average correlation across strategies), and each strategy has a similar variance of
σ
2
and a mean return of
μ
i
.
(a)    Write the formula for the expected return and variance of the entire portfolio when every strategy is equally weighted.
(b)    Write down the expected return and risk formula when the portfolio is leveraged in every strategy, proportionally, by an amount
l
. (
Hint
: Leverage is accomplished by borrowing at the risk-free rate
r
f
.)
15.10.
In the preceding problem, suppose that
n
= 50,
ρ
= 0,
μ
i
=
μ
= 0.0057,
σ
= 0.04,
r
f
= 0.0048, and the confidence interval is 95% (that is,
k
= 1.65). These are all monthly return figures and not expressed in percentage terms. Suppose also that the portfolio is valued at $4.1 billion.
(a)    What is the VaR per month given a leveraged value of 1 (that is,
l
= 1)?
(b)    If the leverage is 30 times, what is the VaR of the portfolio in any given month?
(c)    Suppose that the quantitative portfolio manager mismeasured the correlation between strategies and it turned out to be much higher ex post, say,
ρ
= 0.2. How much would the VaR on the $4.1 billion be now?
(d)    What does this illustrate about the dangers of using VaR?
(e)    What’s a simple fix the risk analyst could do to measure VaR more accurately?
15.11.
Does a correlation of 1 imply a
β
of 1?
15.12.
Which measure of ex-post
α
is reported most frequently to the quantitative portfolio manager? Which ex-post
α
might be the most accurate at describing whether the portfolio manager has had excess performance?
15.13.
A QEPM department is about to hire a new portfolio manager. A candidate for the job claims that his previous tenure as a portfolio manager was quite successful. The performance analyst of the QEPM department decides to study this claim. She obtains the historical monthly returns of the candidate’s portfolio, the benchmark, and the risk-free rate.
(a)    Using these data, compute the Sharpe ratio of the benchmark and the portfolio. Compute the ex-post
α
B
of the portfolio and its corresponding
t
-statistic.
(b)    Compute the information ratio of the portfolio using the common but less accurate method and using the more accurate method.
(c)    What do you conclude about this portfolio manager and his claim?
(d)    Would you expect the portfolio manager to perform the same if he were hired by your firm?
15.14.
A performance analyst collected the following monthly portfolio returns and the returns of three popular factors for use with a multifactor performance measurement. Use the data to construct a linear regression to assess the performance of this portfolio.
(a)    What can you conclude about the portfolio manager’s performance over the period?
(b)    What type of portfolio is the portfolio manager most likely managing?
15.15.
Suppose that a QEPM department hires a new quantitative equity portfolio manager to manage one of its portfolios. Suppose that the portfolio manager’s benchmark is the S&P 500, with a Sharpe ratio of 0.25. After 1 year, the manager has an information ratio (
IR
) of 0.5. Should the head of the department award him a bonus based on this
IR
?
15.16.
A performance analyst is worried that the quantitative models produced by the portfolio managers are biased toward selecting financial and utility stocks. The portfolio managers have one model for security returns that they apply to a large universe of stocks and then use as an optimizer to control tracking error. The performance analyst decides to investigate by creating three divisions of the universe of stocks—a financial sector, a utilities sector, and all other sectors. After dividing the universe thus, the performance analyst performs classic attribution. She computes the returns of the portfolio and benchmark in these sectors, as well as the aggregate weights. The following table should be used to answer the follow-up questions.
(a)    Based on the preceding table, is the performance analyst’s gut feeling correct?
(b)    Using the table, compute the portfolio and benchmark returns
r
P
and
r
B
.
(c)    Compute the allocation effect (
AE
) and the security-selection effect (
SSE
) for the portfolio manager. What can you infer about the portfolio manager’s stock return models?
(d)    Given the results of part (b), what suggestion would you make to the portfolio manager and/or the investment committee regarding the investment process?
15.17.
Suppose that a portfolio manager is using index futures to increase the leverage of his overall portfolio. He currently manages a portfolio of $100 million with 10% in cash and 90% invested in a portfolio of stocks with a
β
versus the benchmark of 1.6 (that is,
β
s
= 1.6). He uses futures on the underlying benchmark; thus
β
f
=1. His target is
β
* = 3. The index starts at a value of 1,000. Suppose that after one month the futures value moves from 1,005 to 854.25, and the return of the stock portfolio is −24%. What would be the return of the overall portfolio for the period? (
Hint
: Ignore cash returns in this example, or assume that they are close to 1.)
15.18.
A performance analyst is faced with computing the historical returns of a market-neutral portfolio in a backtest. Over a period
t
to
t
+
k
, she is given the following information: The initial value of the long portfolio is $65 million, the initial value of the short portfolio is $40 million, and $4 million is required as a liquidity buffer. The return on the liquidity buffer is 2%, the return on cash is 2.5%, the return on the long portfolio is 7%, and the return on the short portfolio (before sorting) is 6%.
(a)    What’s the overall return of the market-neutral portfolio?
(b)    Is it really market-neutral? Why or why not?
15.19.
A performance analyst is interested in computing the multifactor attribution of a quantitative portfolio for the month of December 2020. The benchmark is an equal-weighted portfolio of 10 stocks. The portfolio manager uses a three- factor model of stock returns. The analyst collects the information in the table below, including the weight of each stock in the portfolio and the benchmark at the beginning of the month, the return of each stock in the benchmark for the month of January, and the factor exposures of each stock in the benchmark at the beginning of January. The analyst also measures the factor premiums or returns for the month of December, which are 0.47%, 0.29%, and 0.46%, respectively, for factors 1, 2, and 3. Compute the multifactor attribution for the month of January for the returns. (
Hint
: Use a table similar to the one in the top half of
Table 15.3
.)
15.20.
Continuing with the information provided in the preceding question, suppose that the performance analyst would like to perform a multifactor risk attribution. In particular, the analyst would like to understand the sources of risk from each factor based on the way the portfolio was constructed. The standard deviation of each factor is 4.43%, 2.89%, and 2.59%, respectively. The correlation between factors 1 and 2 is 0.35, between 1 and 3 is −0.37, and between 2 and 3 is 0.10. The variance of the error terms was estimated using historical data and is listed in the table. Construct a table similar to the one in the bottom part of
Table 15.3
, and decompose the hypothetical risk of the portfolio into the various components. Why might some portfolio managers claim that this is really not risk attribution?
1
For an application of measuring market timing across multiple factors, see Chincarini and Nakao (2011).
