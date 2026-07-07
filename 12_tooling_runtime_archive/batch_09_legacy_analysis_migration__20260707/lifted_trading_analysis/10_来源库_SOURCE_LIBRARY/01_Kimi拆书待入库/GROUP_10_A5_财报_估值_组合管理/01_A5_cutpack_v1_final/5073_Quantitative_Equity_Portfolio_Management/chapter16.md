# Quantitative Equity Portfolio Management: An Active Approach to Portfolio Construction and Management, Second Edition

- **book_name**: 5073 Quantitative Equity Portfolio Management, Second Ed.
- **main_source**: epub
- **cross_check_source**: none
- **pdf_role**: not_needed
- **split_scope**: chapter file = chapter16

---

CHAPTER 16
The Backtesting Process
Tell me and I forget, teach me and I remember, involve me and I learn
.
—Benjamin Franklin
16.1 INTRODUCTION
In this chapter we use historical data to formulate models of stock returns and test the performance of hypothetical portfolios based on the models. Building and testing models with past data in this way is referred to as
backtesting
. Backtesting is used widely in quantitative equity portfolio management (QEPM) as a first step in evaluating how well a new investment idea might work. The results of a backtest show whether a strategy would have worked over a significant period in the recent past, which might give an indication of how it will work in the near and not-so-near future.
Certain decisions must be made in the course of backtesting. They include
1.
The historical data set and software to use.
2.
The time period over which the strategy should be tested and the frequency of the data to be used.
3.
The investment universe and the benchmark.
1
4.
The factors to use in the quantitative model of stock returns.
5.
The type of stock return and risk model with which to pick stocks and manage the risk of the portfolio.
2
6.
The rebalancing frequency.
7.
The type of portfolio construction.
8.
How to present the performance results of the backtest.
These are the main decisions that the portfolio manager must make in order to set up the test and simulate the results of actual past portfolios. In this chapter we cover the first seven issues of backtesting. We will deal with the presentation of performance results in
Chapter 17
.
16.2 THE DATA AND SOFTWARE
The choice of data for the backtest is largely determined by the factors that the portfolio manager uses in his or her model of stock returns.
3
For our backtest, we collected five major categories of data: fundamental data, prices and returns, analyst forecasts, social-issue data, and macroeconomic indicators. The fundamental data are from Standard & Poors Compustat database, which contains items from the balance sheets, income statements, and cash-flow statements of the companies. Price and return data are from the University of Chicago’s Center for Research in Security Prices (CRSP) database. Basic information related to stock prices such as daily prices, shares outstanding, dividends per share, and trading volumes were obtained from the CRSP database. We supplemented the CRSP volume data with odd-lot volume data downloaded from the U.S. Securities and Exchange Commission’s website. Analyst forecasts are from the Institutional Broker Estimates System (IBES) database, and the social-issue data are from the Morgan Stanley Capital International–Kinder Lydenberg Domini (MSCI-KLD) database. Macroeconomic data together with index-related data are from Bloomberg.
4
For all of the data, we chose to collect data from 1981 (or the earliest year after 1981 for which data were available) through 2020. This period gave us enough historical data with which to test the performance of our strategies over a relatively long investment horizon. Part of the analyst data was available only beginning in 1993, and the social-issue data were available beginning in 1991. Index future data started in 1982. The industrial classification code we use, the Global Industrial Classification System, began in 1994.
Our raw data are of varying frequencies. Price and return data are daily, analyst forecasts data and many of the macro series are monthly, most of the fundamental data are quarterly, and social-issue data and some of macro series are annual. For ease of management, we arranged all of our data in a monthly format. To do so, certain daily items were summed or averaged across days of a month; quarterly and annual items were recorded in the month when the quarter or the year ended. We also lagged data, to adjust for reporting and release lags, in our historical data set.
A total of 14,945 stocks were included in our historical data set. Two main criteria for inclusion in the historical data set were that both the CRSP and Compustat databases contained the stocks and that the stocks belonged to the top 3,000 in terms of market capitalization at some point during the sample period. More specifically, to construct our database, we went through the following steps. First, for each month
t
, we selected all the common stocks in the CRSP database (SHRCD = 10, 11, or 12).
5
Second, for each stock month (
i, t
), we determined whether stock
i
was the primary share class of a company. For many companies, there exists only one share class, in which case no further action was necessary. When there were multiple share classes, we determined the share class with the largest market capitalization as the primary share. We then excluded nonprimary shares for the purpose of determining the inclusion in our historical data set. (We retained information for nonprimary shares; we just did not consider nonprimary shares for inclusion in our historical data set.) Third, for each stock month (
i, t
), we checked whether basic items such as total assets, total common equity, sales, and net income were available, assuming a reporting gap of three months; that is, if these items were reported for the quarter ending in month
t
− 3,
t
− 4, or
t
− 5, then we considered month
t
to have valid data. We then excluded each stock month (
i, t
) without valid
data. Fourth, for each stock month (
i, t
), we checked whether monthly returns for the current month and the past 11 months could be retrieved. If not, we excluded the stock. Finally, we ordered the remaining stocks by market capitalization from the largest to the smallest for each month
t
. Stocks belonging to the top 3,000 for any one month were included in our historical data set. For the purpose of computation, we stored the entire data history of each stock that entered the historical data set in any month.
Our next step was to combine all of the data from all of the databases into one database. Stocks can be identified by CUSIP number or exchange ticker, but these identifiers change over time and, worse yet, are often recycled. For this reason, financial databases use their own, permanent, alphanumeric identifiers for stocks. Linking the permanent identifiers, though, can be a bit of a challenge.
For merging the CRSP and Compustat databases, we utilized the mapping between the CRSP ID (PERMNO) and the Compustat ID (GVKEY) provided by the CRSP database. This mapping was carefully created and maintained by CRSP, so we used it. The CRSP database also provides a mapping between the CRSP ID and the IBES ID. This mapping appears to be somewhat less reliable than the CRSP–Compustat mapping, so we manually examined some of the suspicious matches, checking the CUSIP number, ticker, and company names in both databases.
6
The MSCI-KLD data were matched to the merged database using the CUSIP number and ticker. When the match was not perfect (i.e., when the CUSIP numbers matched but the tickers did not or when the tickers matched but the CUSIP numbers did not), we manually examined the company names and determined whether the match was valid. The SEC data containing odd-lot volume were matched to the merged database using tickers. In all of the matching procedures, the changes in the CUSIP number, ticker, and company name over time were carefully checked so that our matching was not corrupted by recycled IDs.
Coverage varies in the databases. The percentage of the CRSP–Compustat matched to each of the other databases is listed in
Table 16.1
. For December 2015, CRSP-Compustat data (after applying the “cleaning” criteria described earlier) included 3,920
stocks. When we merged CRSP-Compustat with IBES, we found that only 86.38% of the CRSP-Compustat stocks had valid data in IBES. The percentage of matched stocks declined to 56.58% for MSCI-KLD, while it was higher at 88.47% for the SEC odd-lot volume data. Note that MSCI-KLD data were available only up to 2018, and the SEC odd-lot volume data were available only from 2012 through 2020.
TABLE 16.1
Number of Companies in the Historical Data Set
Note:
The Compustat-CRSP column shows the number of stocks in our historical data set, which includes the entire history of all the stocks that belong to the top 3,000 companies by market capitalization at some point in time after applying the data-cleaning procedures described in the text. For other columns, the table describes the number of stocks or the percentage of stocks in our historical data set that were matched with another database. MSCI-KLD refers to the social responsibility data from MSCI, and SEC refers to the odd-lot volume data from the SEC. The entire period represents the average number of stocks we had in the sample period. For example, when we matched our Compustat-CRSP to the IBES data in December 2020, only 2,870 of the 3,459 companies were matched, representing about 82.97% of our original data. MSCI-KLD data were only available until December 2018, and SEC odd-lot data were only available since 2012.
In addition to the matching percentages, we gathered statistics on various variables for various months in our historical sample period. These are provided in
Table 16.2
. The historical data set for December 2020 contains 2,992 firms with valid earnings-to-price ratios. The average earnings-to-price ratio is −0.053. The minimum is −10.499, which is for AMC Entertainment Holdings (AMC), whereas the maximum is 1.479, which is for Xbiotech Inc. (XBIT). Log market capitalization is calculated for 3,000 firms. The average log market capitalization is 7.631, which corresponds to about 2 billion dollars (=
e
7.631
million dollars). The largest company is Apple Inc. (AAPL), with a log market capitalization of 14.629 (2.256 trillion dollars), and the smallest company is Lightpath
Technologies Inc. (LPTH), with a log market capitalization of 4.628 (102.3 million dollars). The net profit margin is available for 2,992 firms, with an average of −7.070. The minimum net profit margin is −3,128.7 for VolitionRX Ltd (VNRX), and the maximum is 1,248.4 for Virnetx Holding Corp (VHC).
TABLE 16.2
Selected Summary Statistics of the Historical Data Set
For the computations presented in this and the next chapter, we chose to use two software programs. For the data management and model estimation, we used STATA. For the portfolio optimization, transactions costs, tax management, leverage, and market neutrality, we chose to use MATLAB. STATA is superior in data management, especially when the data are not completely numerical, as is the case in our exercise. MATLAB is superior when matrix algebra and optimization are involved.
7
16.3 THE TIME PERIOD
If a portfolio manager is considering an investment idea to be implemented a number of years down the road, it is possible to do
real-time testing
rather than backtesting. Real-time testing means applying a new strategy to current data and recording how well the strategy works going forward. This kind of testing, a bit like performing a long-range study, involves years of collecting real-time data. It is therefore quite different from backtesting, which is meant to give a more immediate evaluation of a strategy. As we have mentioned, backtesting requires sophisticated commercial databases with cleaned historical data, as well as programming tools.
The backtesting method is flexible to different test structures, and some real-time testing is often appended to it. Typically, a backtest includes three segments of data, as depicted in
Figure 16.1
. The first two segments cover the time period from
T
0
, the earliest date for which there are historical data, to
T
2
, the present. These segments encompass all the historical data on stocks, factors, and other variables needed for the evaluation of the investing strategy. The third segment of data covers the time period from
T
2
to
T
3
, which is some point in the future. The third segment of data therefore is future data that will be collected on a real-time basis.
FIGURE 16.1
The backtesting data.
The two historical data segments are the
in-sample
data from
T
0
to
T
1
and the
out-of-sample
data from
T
1
to
T
2
.
8
A portfolio manager or analyst usually has several competing models of stock returns and performs sequential tests with them, dropping or adding a factor in each test. As we discussed in
Chapter 2
, though, testing and discarding models until one comes across a “significant” one is a form of data mining. Although the original model may have been based on sound economic theory, the final variation may not be. The analyst therefore should limit the sequential testing to the in-sample data, and then, once he or she finds a satisfactory model, test that one on the out-of-sample data. This mitigates the problem of data mining because, since the out-of-sample data are not used to test the many discarded variations of the model, the degrees of freedom are preserved,
9
and the test statistics can be interpreted normally. If the stock return model performs well on the out-of-sample data, it is a decent indicator that it might work for a real portfolio. Of course, if the model fails on the out-of-sample data, beginning the testing process all over again on the same data will lead to data mining. Everyone in a QEPM research department, manager and analyst alike, needs to be well versed in the correct use of data for backtesting.
Parameter stability, which we discussed in
Chapter 2
, factors into consideration the time period of the backtest. If relationships
between stock returns and factors did not change over time, it would be sufficient to estimate the stock return model once on the in-sample data and then immediately put it to use in the model. Unfortunately, one of the most frustrating parts of being a portfolio manager is that financial market relationships seem to always change. Many relationships between factors and stock returns change. However, it is the goal of QEPM to find relationships that are stable over time [as stated in tenet 6 of QEPM (see
Chapter 2
)], and this is accomplished with models with stable parameters. If the parameters seem to change over time, the stability of the model can be preserved by using
rolling windows
of data. Rather than estimate the parameters or model on one particular in-sample data period, the analyst should create a
rolling in-sample window
and dynamically reestimate the parameters over time,
10
as depicted in
Figure 16.2
. For example, suppose that an analyst has five years’ worth of data. The in-sample period is January 2010 through December 2010. The out-of-sample period is January 2011 through December of 2015. The rolling in-sample period is one year. The analyst’s first step is to estimate the model’s parameters on the first year of in-sample data (January 2010 through December 2010), use those parameters to forecast January 2011 returns, and check the model’s performance. The next step is to move forward one month in the in-sample data, reestimate the parameters on the year of data from February 2011 through January 2012, and then use those parameters to forecast February 2012 returns and check the model’s performance. This process is continued through the December 2015 data, the end of the out-of-sample period. The rolling in-sample window therefore
ventures into the out-of-sample period, but it does not negate the purpose of the out-of-sample data.
FIGURE 16.2
Backtesting with rolling in-sample windows. (
Note
: Each horizontal series of dots represents a rolling sample.)
The main difference between this method and the one with a static in-sample period is that the parameters are updated continually to reflect changes in the relationships between factors and stock returns, if there are any. The analyst should be careful to make sure, though, that the reestimations reflect actual changes in the underlying parameters and are not just capturing statistical noise.
For our particular historical backtesting example, we utilize data from 2006 (
T
0
= 2006) through 2020 (
T
2
= 2020). We treat the first 5 years from 2006 to 2010 as the in-sample period (i.e.,
T
1
= 2010) and the remaining 10 years from 2011 to 2020 as the out-of-sample period.
11
We believe that 5 years is a reasonable length of time with which to test our factors and to build our stock return models. The remaining 10 years are used for testing our portfolio construction strategies. We used a dynamic rolling in-sample window as described earlier. We discuss more details in Section 16.7 on rebalancing.
We chose a time interval of one month for the data set and obtained end-of-month factors and monthly stock returns to perform our analysis. As we mentioned in the preceding section, any data available only quarterly or annually were recorded to one particular month. To deal with such data we therefore confronted a choice. One way of handling such data is to fill the months that follow with the same piece of data. This leads to some biased relationships, because it joins a static number with varying monthly stock returns. Another way to handle it is to study only the relationships between factors and stock returns at a quarterly or annual interval. This method, though, severely reduces the sample size of the data, making it difficult to infer any statistical relationships between the factor returns and stock returns while also violating our basic decision to use a monthly time interval. For this reason, we chose to fill in quarterly and annual data for the entire period to which they applied. In the end, any potential bias arising from this method was not a concern because none of the quarterly factors was selected for the return model.
16.4 THE INVESTMENT UNIVERSE AND THE BENCHMARK
By delineating an investment universe, the portfolio manager preliminarily confines the model and the portfolio to a certain pool of stocks. The investment universe may be defined by some criteria, or it may be shaped via a screening mechanism. The investment universe also may be the portfolio’s benchmark, although the portfolio may have a better chance of outperforming the benchmark if stocks can be drawn from a wider selection. The investment universe also might be restricted by the need for trading liquidity. The stock needs to be liquid enough for the manager to make trades whenever necessary. For our backtesting example, the investment universe consisted of the top (in terms of market capitalization) 1,500 stocks in the United States.
12
The choice of benchmark is motivated by several factors. A good benchmark should be
representative
of the underlying investment universe. Thus, a U.S. equity portfolio manager should choose an index that represents the U.S. equity market. A benchmark should be
investable and replicable
. That is, the portfolio manager should be able to replicate the performance of the benchmark easily, and there should be few securities in the benchmark that either cannot be purchased or are very illiquid. The benchmark should be
accurate and reliable
, and information about it should be
timely
so that performance comparisons and analysis can be done easily. The benchmark should be
transparent
, with known component securities. The benchmark should have
liquid futures
so that it is possible to use futures contracts for equitization of the portfolio’s cash flows. Finally, the benchmark should not experience high
turnover
. This generates high trading costs and causes a drag on the portfolio’s returns. Most of the indices that we will discuss meet these basic criteria, although some more than others (see
Table 16.3
for the basic criteria).
TABLE 16.3
Important Characteristics of an Equity Benchmark
16.4.1 U.S. Equity Benchmarks
The major benchmarks for U.S. equity portfolio managers are the S&P 500, S&P 400, S&P 600, and S&P 1500 indices, the Russell 3000, Russell 2000, and Russell 1000 indices, the S&P 500 Barra Value and Growth indices; the Russell Value and Growth indices; the NASDAQ 100; the Dow Jones and the Wilshire 5000. Each of these benchmarks is a paper index created by a committee.
The S&P 500, a large-cap index, is probably the best-known equity benchmark. The S&P 400 is a mid-cap index, and the S&P 600 is a small-cap index. The S&P 1500 is simply a market-cap or float-weighted index consisting of the stocks in the S&P 400, 500, and 600. The stocks in the S&P 400, 500, and 600 are chosen by the Standard & Poors Index Committee, which meets regularly to decide which stocks should be added or dropped from the indices.
13
The committee will consider dropping a stock when
stocks are delisted, when there are corporate actions such as mergers, and when basic inclusion criteria are no longer met. Among the committee’s criteria for including a stock in an index are the following: the stock must be a U.S. company; must have positive as-reported earnings in the most recent quarter, as well as over the most recent four quarters (summed up); and must have a certain percentage of its shares freely floating (10% for inclusion in the S&P 500, 50% for inclusion in the S&P 600 or S&P 400).
The Russell indices, run by the Frank Russell Company, are also very popular benchmarks for U.S. equity portfolio managers. The Russell 3000 is an index of the top 3,000 publicly traded stocks in the United States by market capitalization. The Russell 1000 (a.k.a. Russell Large-Cap) takes the top 1,000 stocks of the Russell 3000, and the Russell 2000 (a.k.a. Russell Small-Cap) takes the bottom 2,000. The criteria for inclusion in the Russell indices are less subjective than they are for the S&P indices. Once per year, on the reconstitution date, the Frank Russell Company ranks all the common stocks trading in the United States by market capitalization and screens certain stocks out of the ranking, including stocks trading below $1.00, pink-sheet or bulletin stocks, non- U.S.-incorporated stocks, foreign stocks, and American Depository Receipts (ADRs). Any stocks dropped from the indices during the year in between reconstitution dates are not replaced until the next reconstitution date. New shares of stock resulting from spinoffs and other corporate actions are allowed to stay in the index. The Russell indices’ stocks are float-weighted rather than market-cap-weighted. In 2020, the reconstitution date for these indices was May 8, whereas additions and deletions were made publicly available in June, and the new index for the year became effective on June 29.
14
Standard and Poors created the S&P 500 Value and Growth indices by ranking companies in the S&P 500 by their growth rank relative to their value rank. Growth stocks are considered stocks with high values of growth in earnings-per-share, growth in sales-per-share, and 12-month price changes, while value stocks are considered stocks with high values of book-to-price, earnings-to-price, and sales-to-price ratios. Stocks with a high rank in the growth factor compared to the value factor become part of the S&P Growth Index, while companies with a low rank in the growth factor com
pared to the value factor become part of the S&P Value Index. The stocks in the indices are market-capitalization-weighted. These indices are rebalanced annually in December.
15
The Russell 1000 and Russell 2000 Value and Growth indices are determined by another type of screening. The stocks in the Russell 1000 and Russell 2000 are ranked separately by three variables—the book-to-price (B/P) ratio, the IBES medium-term (2 years) growth forecasts by analysts, and the 5-year historical sales-per-share growth. The stocks are ranked by their scores, and then these scores are combined to determine which stocks become part of the value index and which stocks become part of the growth index. This results in four indices: the Russell 1000 Value, Russell 1000 Growth, Russell 2000 Value, and Russell 2000 Growth. These indices are rebalanced annually along with the rebalancing of the Russell 1000, 2000, and 3000.
The NASDAQ 100 encompasses the largest 100 nonfinancial companies trading on the NASDAQ. Once per year in December, NASDAQ nonfinancial stocks are ranked by market capitalization. The top 75 in the ranking go into the index, while the other 25 are chosen based on preference for companies already in the index that are still ranked in the top 125. New companies that made the top 100 are also considered. The stocks are weighted by a modified-capitalization scheme so that the index is not too skewed toward stocks with high market capitalization. All securities must meet basic eligibility requirements for inclusion.
16
The index is rebalanced quarterly.
The Dow Jones Industrial Average (DJIA) is very popular with personal investors but much less popular as a benchmark for professional portfolio managers. The DJIA contains 30 stocks selected by the Dow Jones Company to represent the U.S. economy.
17
The stocks are price-weighted rather than float-weighted or market-capitalization-weighted, which makes the index susceptible to significant changes from stock splits and other corporate actions that have no bearing on the underlying economics of the index.
This is one of the reasons why the DJIA is not a popular benchmark with portfolio managers.
The Wilshire 5000 is the index most representative of the U.S. equity market. Despite its name, it does not contain 5,000 stocks.
18
It was created in 1974 to represent the performance of all publicly traded U.S. companies. All companies in the index must be headquartered in the United States. The index is market-capitalization-weighted. The Wilshire 5000 is often referred to as the
total market index
.
19
16.4.2 A Comparison of the Major U.S. Equity Benchmarks
How do the major domestic equity indices compare with one another in terms of performance?
Table 16.4
lists their return statistics from 1995 to 2020.
20
All these statistics include the reinvestment of dividends into the underlying index. The benchmark with the highest geometric return over the period was the NASDAQ 100, with a 14.93% annual return. The S&P 400 (12.14%) and S&P 600 (11.21%) followed closely behind. The Russell 2000 Growth had the lowest annual return for the period (9.04%).
TABLE 16.4
Statistics of Common Benchmarks from 1995–2020
In terms of risk, the NASDAQ 100 had the highest annualized standard deviation (24.58%), and the Russell 2000 Growth had the second highest (22.74%). The benchmark with the lowest annualized standard deviation was the Dow Jones Industrial Average (14.93%).
All the major equity indices exhibit negative skewness. The distributions of their returns are skewed left of the normal distribution, which means that the probability that they have earned less-than-average returns in any given year is less than 50%. All the indices also exhibit positive excess kurtosis. The distributions of their returns have thicker tails than the normal distribution does, so the probability of extreme returns is greater than a normal distribution would predict. The skewness and kurtosis of these indices have been noted in data from other historical periods, not just
the rocky period of 1995–2020 covered here. The last column of the table computes a Jarque-Bara test, which is a test for the normality of the return distribution based on the skewness and kurtosis of the returns as compared with a normal distribution. For every benchmark, the test rejects the assumption of normality.
21
It is often interesting to see how much the returns of different equity benchmarks are related. The correlation of two return series describes how they move in relation to each other. Correlation values range from −1 (the series move in exact opposition to each other) to 1 (the series move in exact unison).
Table 16.5
shows the correlations of the returns of the major benchmarks over the period 1995–2020.
TABLE 16.5
Correlations of Common Benchmarks from 1995–2020
It turns out that the S&P 500 is highly correlated with some of the other well-known indices. The S&P 500’s correlation with the Russell 1000 is 0.998; with the Russell 3000, 0.994; with the S&P 1500, 0.998; and with the Wilshire 5000, 0.989. The S&P 500 is less correlated with other indices. Its correlation with the NASDAQ 100 is 0.822; with the S&P 400 and S&P 600, 0.906 and 0.826, respectively; and with the Dow Jones Industrial Average, 0.951.
More comparisons are possible by observing some of the indices’ fundamental factors or financial ratios.
Table 16.6
gives the vital statistics or fundamental ratios of the various indices using data from the end of 2020.
22
TABLE 16.6
Vital Statistics of Common Benchmarks for December 2020
A few patterns stand out. The highest P/S ratio is for growth indices, like the S&P 500 Growth Index and the NASDAQ 100. The highest P/E ratios are from the Russell 2000 Growth and Value indices. The lowest P/E ratio index at the end of 2020 was the Dow Jones Industrial Average with a P/E of 27.12. Not surprisingly, the index with the largest total market capitalization is the Russell 3000, whose stocks trade at a total market cap of $40,930,135 million. The smallest benchmark is the S&P 600, which has a market capitalization of $938,212 million.
16.4.3 The Most Popular Benchmarks and Our Benchmarks
The choice of benchmark is often dictated by a portfolio manager’s investment style and by the liquidity of the potential benchmarks’ underlying futures.
Table 16.7
shows that the most popular benchmark is the S&P 500.
23
TABLE 16.7
Most Popular Benchmarks for Global Equity Managers in 2021
The S&P 500 was the first benchmark embraced by investors, and it remained popular because of the liquidity of its securities and futures, because it was more manageable as a benchmark than indices containing thousands of stocks, and because of its brand recognition, which gave managers the sense that they were measuring themselves against the same benchmark that their peers were. The main drawback to the S&P 500 is that the popularity of the index as a benchmark may create distortions in its returns. If enough index managers make trades that mirror changes in the index, the traded securities’ prices will fluctuate simply as a result of being added or dropped from the index.
Like many other portfolio managers, we chose to use the S&P 500 as the benchmark for our backtesting example. Our choice was determined partly by data availability. Having several benchmarks would have allowed us to compare the performance of our portfolios with various types of indices: large-cap, small-cap, value, and growth. The difficulty of obtaining sufficient data for multiple comparisons, however, obliged us to choose only one benchmark. Benchmarking with the S&P 500 made sense for a number of reasons. As the most popular benchmark used by portfolio managers, it is likely quite familiar to our readers. It is also highly correlated with many of the other major equity benchmarks. It has the most liquid futures contracts available for trading, which is useful when we consider leverage. From a practical standpoint, the fact that the Compustat database has a flag to identify each S&P 500 stock in every month of our historical data made it fairly easy for us to construct the benchmark historically for optimizations and other analyses. Finally, although we use the
S&P 500 as our benchmark, we allow our investment universe to be any of the top 1,500 stocks in the United States by market capitalization.
24
16.5 THE FACTORS
We discussed factor choice at length in
Chapter 4
. In this section we list factors that we think might be important in explaining stock returns and in generating
α
B
. We also show statistics on the significance of various factors.
Before testing factors, the data need to be organized and cleaned. All researchers know the immense challenges of data organization and cleaning. There are really three steps in preparing the data for use in testing. The first is to check the general consistency and accuracy of the data. Are all the financial variables for each stock computed correctly, or are there some clear data errors? Errors could include ratios that are glaringly off (e.g., an earnings-to-price ratio of 0.000002) or, harder to detect, ratios computed with erroneous inputs. The second step is to check that the data are recorded as of the correct dates. Some data vendors record earnings per share (EPS) as of the quarter in which they were earned even though they were not reported until a few months after the quarter ended. This creates
look-ahead bias
. Any data recorded this way should be moved to the month in which it actually became available to the public. The third step in preparing the data is the arduous task of
data organization
, which includes anything else necessary to get the data in the right shape to be read into the model and portfolio-building software. One problem encountered at this point is
survivorship bias
. Owing to mergers, acquisitions, delistings, bankruptcies, and other events, some stocks that existed in the past do not exist today. If a backtest uses only data on stocks that exist today, the results of the test will be biased, usually upward. A backtest always should include all the data available on any stock that meets the investment universe criteria on any given date. Some databases, such as CRSP, provide returns of extinct stocks based on their likely selling prices (i.e., the prices at which investors actually would have been able to sell shares back to the company or to creditors). If the portfolio manager does not have access to a database with these sorts of estimated returns, he or she will have to make up his or her own sensible rules for dealing with extinct stocks in the backtest.
To begin the factor testing for our backtest, we considered some of the most important factors that might be related to stock returns. Our initial selection of factors, drawn from the factors described in
Chapter 4
, was based on theoretical reasoning. In
Table 16.8
, we name the factors we chose, the reason for choosing them, and our ex-ante belief about how they relate to the cross section of stock returns in the fundamental factor model.
25
TABLE 16.8
Initial Factor Choices
In order to test the factors, we first created programs that computed the historical factor exposures for every stock in our database. We ran these programs at monthly intervals to create a historical series of monthly factor exposures for each stock, all the while being vigilant about look-ahead bias. The historical book-to-price (B/P) ratios, for example, were computed by dividing each company’s total common equity by the product of the company’s price per share and the number of shares outstanding. For common equity, we allowed for a lag in reporting of three months, so we searched for the book value as reported three months prior to the month for which we
created the B/P ratio. For a detailed description of all our factor formulas, see Tables 16A.1 to 16A.13 in
Appendix 16A
.
For macroeconomic factor exposures, the computation was slightly more complicated. We first collected the premium for all of the macroeconomic factors, again avoiding look-ahead bias by taking into account the appropriate lags in the reporting of indicators. For example, to create the monthly inflation variable for a given month, we divided the consumer price index (CPI) of the previous month by the CPI of two months prior and subtracted 1 from that value. This avoids look-ahead bias by recognizing the one-month delay in CPI releases. This type of logic was applied to all our macroeconomic variables so that we created a time series of macroeconomic factors that would have been available at the end of each month. We then ran individual regressions of each stock’s monthly returns against each monthly economic factor up to 60 months and no less than 12 months. We required all the stocks in our investment universe in month
t
to have at least a 12-month return history. Thus, we were able to calculate factor exposures for all the stocks in our investment universe. To keep the estimates fresh, we constructed the factor exposures on a rolling basis for each month looking back a maximum of four years.
The resulting factor exposures give us a direct relationship between factor values and stock returns. For example, the factor exposure of Boston Beer Company (SAM) to GDP growth each year was mostly negative in recent periods. The estimate for December 2020 was −1.145. If GDP growth for the quarter prior to December 2020 was 1%, then the expected return on the stock would be −1.145% (ignoring the constant term). Similarly, if GDP growth for the prior quarter was −1%, we would expect the stock price to have gone up by 1.145%. The negative exposure fits with the intuition that SAM is a defensive stock. There were some outliers in the factor exposure estimates as well. Some practitioners will carefully remove these outliers; instead we chose not to remove the extreme observations in our backtests.
26
One outlier that sticks out in the data is Eastman Kodak (KODK). The stock has an exposure to GDP growth of −18.857 due to the extreme volatility in July and August of 2020. This volatility was related to the news that the U.S. government wanted the firm to produce pharmaceutical components to fight the pandemic (although they never actually ended up doing this).
Once we created the factor exposures for every stock per month, we wrote programs to perform the factor tests using simple single-factor regressions and testing the returns of unidimensional zero-investment portfolios, as explained in
Chapter 4
. The results of these factor tests are shown in
Table 16.9
. Since the out-of-sample time period was 2011–2020, we could use only the years prior to 2011 to perform our initial factor tests. We chose to concentrate on factor tests for the five-year period from 2006–2010.
TABLE 16.9
Results of Factor Analysis from 2006–2010
The astute reader will notice that out of 164 factors listed in
Table 16.9
, one factor is missing in
Table 16.9
. The odd-lot balance factor (numbered 110) is not included for factor testing as the underlying data for this factor were only available beginning in 2012. In Appendix 16B, we report factor tests for different time periods, and in some of those tests we include the odd-lot balance factor.
27
With the results in
Table 16.9
, we proceeded to select the factors for our stock return models.
28
We selected two sets of factors, one set to build a fundamental factor model and another set to build an economic factor model. We also constructed a Z-score model, for which we used the same set of factors that we used for the fundamental factor model. Our selection proceeded as follows.
First, we checked whether the return-exposure regression coefficient
sign (positive or negative) was in accordance with what we expected from theory and whether it was statistically significant. Only when the sign of the coefficient corresponded with our ex-ante theoretical beliefs shown in
Table 16.8
, and the absolute value of the associated
t
-statistic was greater than 1.64, did we keep the factor as a candidate for the fundamental factor model. Out of 163 factors (164 factors less the odd-lot balance factor), only the following 19 factors satisfied our requirements: EBITDA-to-EV (EBITDAEV), long-term asset growth (LTAG), annual change in ET (ETD), total asset turnover (TAT), TAT minus industry average (TATX), annual change in TAT (TATD), total accruals (TACC), cash flow to total assets (CFTA), gross profit to total assets (GPTA), return on common equity (ROCE), return on owner’s equity (ROE), return on total capital (ROTC), cash-flow-from-operations ratio (CFOR), inverse cash-flow coverage
ratio (ICFCR), annual change in D/E (DED), Pastor and Stambaugh liquidity (PSL), Bollinger bands (BB), consumer confidence growth (CCG), business confidence growth (BCG), and standardized unanticipated earnings (SUE). As for an economic factor model, we determined the candidate factors based on the zero-investment portfolio return
r
ZI
and the associated
t
-statistic. We kept a factor as a candidate only if the sign of
r
ZI
corresponded with our ex-ante beliefs shown in
Table 16.8
and the absolute value of the
t
-statistic was greater than 1.64. Out of 163 factors, the following 13 factors satisfied our requirements: EBITDAEV, equity turnover (ET), FAT minus industry average (FATX), TAT, TATD, CFTA, GPTA, PSL, BB, inflation (CPIG), ten-two-year term premium (TP2Y), ten year-three-month term premium (TP3M), and SUE.
Second, we made sure that the selected factors were not too similar to one another. Since our factor tests were univariate tests, there was a possibility that some factors were very similar. To check for this possibility, we calculated the correlation and the rank correlation of every pair of factors.
29
Whenever we found a pair of factors that had a correlation higher than 0.75, we excluded the factor that had the smaller
t
-statistic. This step eliminated ETD from the candidate factors for the fundamental factor model and TATD from the candidate factors for the economic factor model.
Finally, we performed a multivariate analysis. For the fundamental factor model, we regressed the returns on the 18 potential factors and selected the five most significant variables. For the economic factor model we regressed the returns on dummy variables created from the 12 potential factors. The dummy variable had a value of 1 if the stock had a high value of the factor and a value of 0 if the stock had a low value of the factor. This regression
is identical to the test of zero-investment portfolio returns created from 12 potential factors. Again, we selected the five most significant variables. The final factors for the fundamental and economic factor models are listed in
Table 16.10
. For our aggregate Z-score model, we used the same factors as for the fundamental factor model.
TABLE 16.10
Final Factors for Stock Return Models
16.6 THE STOCK RETURN AND RISK MODELS
With the list of factors finalized, it is possible to create the model of stock returns and risk that eventually will lead to the desired portfolio. As we emphasized with the information criterion, it is best to use the same model to both forecast stock returns and calculate risk. We ran our data through three different models—a fundamental factor model, an economic factor model, and an aggregate Z-score model. The fundamental and economic factor models produce both expected returns and risk for all the stocks in the investment universe, but the aggregate Z-score approach does not. We chose to use the version of the aggregate Z-score in which the Z-score becomes the factor exposure. That is,
where
γ
i
represents a constant term,
δ
k
is the coefficient that relates the Z-score to the stock returns, and
ρ
i,t
is a typical error term.
In order to construct our optimal portfolio for every period of data, we concerned ourselves only with the specific case of an enhanced active portfolio manager. In all cases, we considered our benchmark to be the S&P 500 and maximized our excess return over the benchmark subject to a tracking-error constraint.
We performed a variety of backtests and optimizations, abiding by the following parameters for the optimizations. The tracking-error constraint was 5%, but we also considered tracking errors of 2% and 10% (that is,
TE
≤ 2%, 5%, or 10%). We did not allow for short selling (that is,
w
≥ 0) except for the market-neutral strategy. The portfolio had to be fully invested (that is,
w
′ι
= 1), except for the market-neutral strategy. We applied a diversification constraint that no individual stock weighting be greater than 5% of the portfolio (that is,
w
≤ 0.05). For the market-neutral strategy, we required the
absolute
value of any stock weight to be less than 5% of the portfolio value. Finally, we imposed a trading liquidity constraint: Assuming that we were managing a $500 million portfolio, we restricted the weight of each security to less than 33% of the average daily dollar trading volume (ADDTV) so that
w
t
≤
. We computed the updated ADDTV for every stock every month but did not adjust the relevant size of the portfolio.
We also considered further variations in which the sector weightings were identical to those of the benchmark. Another optimization involved matching the factor exposures of the benchmark.
30
16.7 PARAMETER STABILITY AND THE REBALANCING FREQUENCY
Before building the stock return models, it is useful to test for parameter stability. Tenet 6 of QEPM states that quantitative models should reflect persistent and stable patterns. Testing for parameter stability determines how frequently a stock return model must be re-estimated to ensure that it describes persistent, stable patterns in the data. Recall that in the factor-selection stage, we regressed the return on the factor exposure for each month. By pooling the month
ly regressions, we were able to test whether the factor premium was stable over time.
For instance, consider the regression of the return on the long-term asset growth factor:
In this equation,
LLOGTA
i,t
is the long-term asset growth of firm
i
at the beginning of month
t
or end of month
t
− 1, and
f
t
is the factor premium of month
t
. This equation was estimated for each month
t
from January 2001 through December 2010. At the end of this procedure, we had 120 sets of estimates for
α
and
f
, each set corresponding to one month.
By pooling 120 regressions and running them at the same time, we tested whether
f
was stable over time. Note that in the pooled regression, we did not impose any restriction on
f
or
α
; we still estimated 120
f
’s and 120
α
’s. The resulting estimates are identical to those we obtained from the month-by-month regressions. The pooled regression made hypothesis testing easier without adding any restrictions.
Once the pooled regression was estimated, we examined whether the factor premium was stable for a quarter. First, we tested whether the
f
of January 2001, the
f
of February 2001, and the
f
of March 2001 were identical. The null hypothesis was that all three
f
’s were identical; the alternative hypothesis was that they were not identical. If the
p
-value of this sort of test is high, we have more confidence in the null hypothesis. If the
p
-value is low, the alternative hypothesis is more likely to be true. We used the conventional cutoff value of 5%. With a cutoff value of 5%, if the
p
-value is higher than 5%, the null hypothesis is accepted. If the
p
-value is lower than 5%, the null hypothesis is rejected.
We ran this same test for the next quarter (i.e., for the
f
of April 2001, the
f
of May 2001, and the
f
of June 2001), and we repeated it until we had completed all 40 quarters of data from 2001 through 2010.
31
Of the 40 tests performed, we rejected the null hypothesis 22 times, a rejection rate of 55% (=22/40 · 100). This rejection rate indicates that the premium of long-term asset growth is more or less stable in a quarter.
The same testing procedure is easily extended to any other length of time. We carried out the analysis for periods of six months, nine months, and one year, in addition to the quarterly periods. Since we did not use overlapping data in the test, we performed the test on 20 six-month periods (Jan 2001–June 2001, Jul 2001–Dec 2001, … , Jul 2010–Dec 2010); on 12 nine-month periods (Jan 2001–Sep 2001, Oct 2001–Jun 2002, … , Jan 2010–Sep 2010); and 10 one-year periods (Jan 2001–Dec 2001, … , Jan 2010–Dec 2010).
Table 16.11
summarizes the rejection rate for selected factors. The rates suggest that for the annual change in D/E, the parameters are stable for one year, whereas for the other factors, the parameters change frequently.
TABLE 16.11
Rejection Rate in Parameter Stability Tests for Selected Factors
Rather high rejection rates for a quarter suggest that it may be advantageous to keep the period between reestimations shorter than a quarter. We thus decided to reestimate all our models at monthly intervals.
For the construction of our portfolios, we adopted the following strategy. At the end of month
T
, we estimated three models—the fundamental factor model, the aggregate Z-score model, and the economic factor model—using the 60 months of data (i.e., from month
T
− 59 to month
T
). After the estimation of each model, we collected monthly factor premiums for these 60 months, used them as inputs to a VAR (vector autoregression), and forecast the factor premium for month
T
+ 1.
32
We also collected factor exposures for the beginning of month
T
+ 1.
33
Finally, we created the portfolio
for month
T
+ 1 based on these factor premiums and exposures. We repeated the entire procedure at the end of every month of data by rolling the estimation window forward one month.
An example with actual dates illustrates these procedures. Suppose that we are building the portfolio for January 2011. For the fundamental factor model, we use stock return data from January 2006 to December 2010 and factor exposure data (e.g., LLOGTA) for the beginning of each month of this period. We use the version of the fundamental factor model where we allow factor premiums to change month-to-month. We thus obtain monthly factor premiums from January 2006 to December 2010; by running a VAR using these data, we obtain an estimate of the January 2011 factor premium distribution. By combining this estimate with the beginning-of-January-2011 factor exposure, we are able to compute the expected returns, standard deviations, and correlations of all stocks in the universe and build the portfolio for the beginning of January 2011.
For the economic factor model, we used the same stock return data from January 2006 to December 2010. We combined these data with the factor premium data for the same period. We estimated a VAR using these factor premiums and obtained estimates of the January 2011 factor premium distribution. We also estimated the factor exposure of all stocks from the stock-by-stock regression of returns on factor premiums. By combining the factor exposure estimates with the factor premium distribution estimates, we were able to compute the expected returns, standard deviations, and correlations of all stocks in the investment universe and build the portfolio for the beginning of January 2011. The process was then repeated for every subsequent month of data.
We did not choose factors again over our out-of-sample period. Some quantitative portfolio managers might wish to reselect the underlying factors at some regular interval, say, every five years. To simplify our presentation, we did not do this.
16.8 THE VARIOUS TYPES OF CONSTRUCTED PORTFOLIOS
Our baseline portfolio for each of the three models is the maximum-expected-return portfolio with five constraints: a 5%-tracking-error constraint, a no-short-selling constraint, a full-investment constraint, a diversification constraint, and a trading-volume constraint.
We consider 11 variations on this baseline portfolio. For the first two variations, we replace the 5% tracking error with a 2% and 10%
tracking error, respectively. For the third variation, we added a sector weight constraint that required the sector weights of the portfolio to be identical to those of the benchmark. We used the Global Industrial Classification System (GICS) to identify 10 major sectors of stocks and then set up our portfolio so that its weights in those 10 sectors matched the benchmark’s weights in those sectors. The fourth-variation portfolio included a factor exposure constraint that required the factor exposures of the portfolio to be identical to those of the benchmark. Since we had five factors, the factor exposure constraint amounted to five constraints. For each of the five factors, we made sure that the portfolio’s exposure matched the benchmark’s exposure. The fifth and the sixth variations of the baseline portfolio used transactions costs management and tax management, respectively. We made tracking portfolios that maximized the expected excess-return accounting for either transactions costs or taxes. All the other features of the baseline portfolios were maintained.
The remaining five variations involve creating leveraged or short positions. We modified the portfolio to purchase futures contracts so as to increase the portfolio beta (variation 7), created a “sector-matched” tracking portfolio and at the same time sold the S&P 500 (variation 8), and bought the “factor-matched” tracking portfolio and at the same time sold the S&P 500 (variation 9). The last two long-short portfolios are comparable to the one created by relaxing the no-short-sale constraint while imposing a sector-neutral constraint (variation 10) or a factor-neutral constraint (variation 11).
16.8.1 Transactions Costs
Portfolio managers often backtest strategies without considering transactions costs, an omission that colors the test results an unrealistically rosy hue. The portfolio strategy that yields the best results in a test without transactions costs may involve high turnover that will chip away at the manager’s
α
B
when put into practice. Ignoring transactions costs also can bias the manager toward selecting smaller-cap stocks despite the fact that small-caps’ trading costs actually are typically higher than the costs associated
with large-cap stocks in similar lines of business. A fair backtest must deal with transactions costs in some way.
Our backtest period is 1995–2020. Conversations with traders will give a portfolio manager a rough idea about transactions costs, but a more detailed picture emerges when the manager can examine many trades and determine precisely how transactions costs differ depending on the types of trades.
Abel Noser keeps track of institutional trading costs for U.S. equities.
34
The Abel Noser data divide trading costs into several categories, including
commissions, market impact, delay
, and
opportunity cost
. Commissions are the explicit fee paid for brokerage services to enact a trade. Market impact is any change in the market price of a stock owing to supply/demand imbalances caused by placing a trade. Impact is measured as the difference between the price at which the broker receives the order and the execution price. Delay summarizes the inter-day costs of price movements that occur while orders are held over from one day to the next owing to either lack of liquidity or failure to act. A more esoteric component of trade-related costs is opportunity cost, which is defined as the theoretical loss of return associated with not fully completing a trade order. Opportunity cost results from delaying execution to lessen market impact, from not being able to make the execution at all, or from abandoning part of the trade because the market has turned against the strategy. If an investment manager’s strategy envisioned the purchase of 100,000 shares, and only 50,000 were actually purchased, the lost potential returns on the remainder represent an opportunity cost.
These transactions costs can add up significantly. For example, in the fourth quarter of 2020, commissions contributed 3.7 basis points, market impact contributed 20.4 basis points, and delay contributed 19.2 basis points to the total trading costs for all stocks. In total, 43.3 basis points per trade were just transactions costs. A model
α
B
would have to be rather high to counteract such transaction costs!
Table 16.12
gives the breakdown of transactions costs for various years.
TABLE 16.12
Transactions Costs for Selected Periods
To run the variation of the baseline portfolio with transactions costs, we had to decide which costs were relevant. For trades of 25,000 shares or more, practitioners suggest that managers define the average transactions costs as commissions plus market impact plus delay, whereas for transactions of 10,000 shares or less, it is sufficient to use commissions plus market impact. To be conservative, we chose to use the more inclusive definition of trading costs. We calculated the overall transactions costs as 80% of the large-cap costs plus 20% of the small-cap costs.
35
16.8.2 Taxes
Backtesting without considering tax consequences also can seriously distort the test results. As we emphasized in
Chapter 11
,
what matters to investors in the end is the after-tax return, and the after-tax return can be quite different from the before-tax return. Taxes create two tasks for portfolio managers. The first is to calculate and report both the before-tax and after-tax returns of the portfolio. The second is to consider actively tax-managed portfolios that generate extra returns through tax savings.
Calculating the after-tax return is simple in principle but can be demanding in practice. Tax rates vary for different investors, so it is not always obvious which tax rates to apply to long-term capital gains, short-term capital gains, and dividends. Keeping track of tax lots requires additional effort. For the purpose of our backtest, we assumed a 15% rate on long-term capital gains and a 37% rate on short-term capital gains. Tax rates on dividend income vary significantly among different types of investors, so we ignored dividend taxes in the backtest. We did keep track of tax lots and applied the tax-lot selection method detailed in
Chapter 11
to minimize the tax burden. In this method, the potential tax burden of each tax lot is calculated before trading so that the first trade uses the lot with the lowest potential taxes.
For the actively tax-managed portfolio, we adopted the loss-harvesting approach. Loss harvesting, which involves selling shares that are trading at less than the purchase price, generates capital losses and reduces the overall tax burden of the portfolio. Loss harvesting every single losing share maximizes the tax benefit but has the undesirable effect of increasing the portfolio’s tracking error with respect to the benchmark. For our backtesting example, we implemented a more conservative form of loss harvesting. We created the tax-managed portfolio in two steps. In the first step, we decided which stocks to buy and which stocks to sell, without considering taxes. In the second step, we decided how many shares to buy and how many shares to sell using the loss-harvesting technique. This two-step procedure ensured that the loss harvesting did not raise the portfolio’s tracking error too much.
More specifically, in the first step, we determined what our baseline tracking portfolio would be without accounting for taxes. A comparison of this tracking portfolio with the current portfolio told us which stocks to buy and which to sell. To make this comparison, we denoted the weight of stock
i
in the current
portfolio before rebalancing by
and the weight in the optimal tracking portfolio by
.
36
If the weight of the stock was higher in the optimal tracking portfolio than in the current portfolio (that is,
), we knew we needed to buy more shares of the stock. On the other hand, if the weight of the stock was lower in the optimal tracking portfolio than in the current portfolio (that is,
), we knew we needed to sell shares of it.
In the second step, we decided exactly how many shares to buy and sell from a loss-harvesting perspective. The idea is to move the new portfolio weights closer to the full loss-harvesting weights to increase the tax benefit. To do so, we subtracted the tax rate from the expected return of stock
i
if selling stock
i
realized a loss and added the tax rate to the expected return of stock
i
if selling stock
i
realized a gain. The actual procedure was complicated as we needed to distinguish between short-term and long-term losses and also between short-term and long-term gains. Thus, for each stock included in the current portfolio, we identified tax lots with short-term gains, long-term gains, short-term losses, and long-term losses. We denoted by
w
bL
the weight of tax lots with short-term gains. (
Note
: This weight is always smaller than the total weight of the stock. Thus,
.) We denoted by
the weight of tax lots with short-term gains plus the weight of tax lots with long-term gains. (That is,
was the sum of
and the weight of tax lots with long-term gains. Thus,
.) Finally, we denoted by
w
bH
the weight of tax lots with short-term gains plus the weight of tax lots with long-term gains plus the weight of tax lots with long-term losses. (That is,
was the sum of
and the weight of tax lots with long-term losses. Thus,
.) We then compared the tax-ignorant optimal weight
to
,
,
, and
and decided on the necessary adjustment of expected return and the additional constraints to impose.
The additional constraints and the necessary modification of the optimization can be summarized as follows: Let
be the new portfolio weight of stock
i
. Also, let us use
,
,
,
, and
as defined above. We will indicate the short-term and long-term tax rates by
τ
s
and
τ
l
. Then
1.
If
, then (
) is added as a new constraint.
2.
If
, then (
) is added as a new constraint, and the expected return
µ
i
is replaced with
μ
i
−
τ
s
. This will ensure that we realize more short-term losses than indicated by
.
3.
If
, then (
) is added as a new constraint, and the expected return
μ
i
is replaced with
μ
i
−
τ
l
. This will ensure that we realize all the short-term losses and some long-term losses.
4.
If
, then (
) is added as a new constraint, and the expected return
µ
i
is replaced with
μ
i
+
τ
l
. This will ensure that we realize all the losses but avoid realizing too much of the long-term gains.
5.
If
, then (
) is added as a new constraint, and the expected return
μ
i
is replaced with
μ
i
+
τ
s
. This will ensure that we realize all the losses but avoid realizing too much of the short-term gains.
All the other features of the baseline portfolios remain unaffected in the optimization.
16.8.3 Leverage
For the leveraged portfolio, we combined the baseline tracking portfolio with S&P 500 futures. Given the capital asset pricing model (CAPM)
β
of the baseline portfolio, we purchased enough S&P 500 futures to boost the portfolio’s
β
to 2 with respect to the S&P 500. The baseline portfolio’s
β
was computed from the
β
’s of the individual stocks in the portfolio.
37
The correct number of futures to purchase for an overall
β
of 2 was determined from the following formula
38
:
where
β
* is the target
β
(in our case, 2),
β
s
is the
β
of the stock portfolio,
V
t
is the value of the baseline portfolio at time
t, S
t
is the spot price of the index underlying the futures contract (in our case, the S&P 500), and
q
is the size of one futures contract (250).
In
Chapter 15
we discussed formulas for computing the returns of leveraged portfolios. In our backtest, we used
Eq. (15.10)
to compute the returns of the leveraged portfolio:
With our specific parameters,
ξ
= 0,
β
f
= 1, and
β
* = 2, the resulting equation for returns of the leveraged portfolio is
16.8.4 Market-Neutral
To test the market-neutral strategy, we created a dollar-neutral portfolio that was
β
-neutral to each of the factors in the economic factor model. Since we already discussed the construction of a factor-exposure-matched tracking portfolio, we simply took a long position in this optimal tracking portfolio and a short position in the benchmark. The resulting portfolio is dollar-neutral because the long position and the short position were the same in dollar amount. The resulting portfolio is also
β
-neutral because the tracking portfolio and the benchmark portfolio have the same factor exposures.
In addition to this, we also created a dollar-neutral, sector-neutral portfolio from the sector-matched tracking portfolio and the benchmark. We took a long position in the optimal tracking portfolio and a short position in the benchmark. The resulting portfolio was both sector and dollar neutral.
Finally, we created two market-neutral portfolios directly from the optimization. That is, in the optimization we imposed the dollar-neutrality constraint (that weights sum to 0) and either the factor neutrality constraint (that the portfolio exposure to each factor is 0) or the sector neutrality constraint (that the weight of each sector is 0). We dropped the full-investment constraints, the no-short-sale constraint, and the tracking-error constraint. We modified the diversification constraint and the trading-volume constraint so as to put limits on the absolute weights rather than the weights themselves.
16.9 CONCLUSION
In this chapter we set out to demonstrate the process of backtesting using historical U.S. stock data. Quantitative equity portfolio managers often use backtesting to see how well a strategy would have worked in the past. If past and current conditions relevant to the model are expected to continue, more or less, into the future, then a backtest gives an indication of how well the hypothetical portfolio might perform going forward. How a manager decides to set up and run a backtest influences the test results. We used our decision-making processes in this particular chapter to illustrate reasonable approaches to the practical problems generally encountered at each stage of a test. We discussed our decisions about the data and software, the time period and frequency of the data set, the investment universe and benchmark, the factors to include in the stock return model, the type of model to use, the portfolio’s rebalancing frequency, and the type of portfolio construction. Procedures that we outlined briefly in this chapter are described more fully in earlier chapters of the book.
Chapter 17
presents the actual performance statistics of the strategies we backtested and implemented in hypothetical portfolios. We tested three different models—a fundamental factor model, an economic factor model, and an aggregate Z-score model. With each of these models, we then built a baseline portfolio and a number of variations on it with different constraints (on stock weights, factor exposures, transactions costs, or taxes) or different characteristics (leveraged, market-neutral). Some of the portfolios’ performance statistics are exciting, others lackluster. The goal of our example is not to advocate particular strategies but rather to show how to test, implement, and evaluate them. Thus, we will not be selective in presenting our results. The judgment on whether a certain strategy is worth pursuing is left to the reader.
1
Typically, the manager will already know his benchmark. The investment universe is the group of stocks from which holdings can be selected for the portfolio.
2
It is preferable to use the same model for both return and risk, although it is possible to use different ones.
3
See
Chapter 4
for a discussion of factors. For information on databases and vendors, see Appendix D under General Appendices at
www.ludwigbc.com
under QEPM Exclusive Content.
4
We downloaded the Survey of Professional Forecasters data from the Federal Reserve Bank of Philadelphia and also utilized the risk-free rate series from the website of Professor Kenneth French of Dartmouth College.
5
This step excluded most of the REITs from our investment universe.
6
CUSIP (Committee on Uniform Securities Identification Procedures) numbers are nine-digit identifiers assigned to U.S. stocks and bonds and Canadian stocks. The first six digits of the CUSIP number identify the company; the next two digits identify the type of each security.
7
We provide programs, data, and labs to practice QEPM in STATA, MATLAB, or R. These labs can be downloaded from our website with the appropriate password. They can be found under Classroom Labs at
https://ludwigbc.com/books/qepm/exclusive_qepm_content_2020/
or at
www.ludwigbc.com
and look for QEPM Exclusive Content.
8
A more technically oriented reader may prefer to call the latter period the
pseudo-out-of-sample data
, rather than the out-of-sample data, as they are, technically, both part of our sample. In addition, some readers might be more familiar with the terms
estimation period
and
testing period
or perhaps with the terms
training data
and
validation data
.
9
Degrees of freedom
are a measure indicating whether the data set is large enough to run meaningful statistical tests with given the number of parameters in the model. The degrees of freedom are preserved because enough unused data points remain.
10
Some people call this
walk-forward testing
.
11
We constructed the historical database covering the 40-year period from 1981 to 2020. We provide the factor tests for some of the earlier periods in Appendix 16B under Chapter Appendices at
https://ludwigbc.com/books/qepm/exclusive_qepm_content_2020/
for the curious reader.
12
The inclusion in the investment universe was determined separately for each month. Thus, every month the investment universe could potentially change. Our historical data set, as explained earlier, includes every stock that, at one point in time, belonged to the top 3,000 companies ranked by market capitalization. This allows us flexibility in making various calculations and constructing factors. However, this is different than our investment universe, which is the group of stocks that we allow for inclusion in our optimal portfolios.
13
For more information on the selection criteria, see
https://www.spglobal.com/en/.
14
For more information, see
https://www.ftserussell.com/.
15
For more information on the exact methodology for index construction, see
https://www.spglobal.com/en/.
16
For more information, see
https://www.nasdaq.com/nasdaq-100.
17
The index excludes transportation and utliity stocks. For more information, see
https://www.spglobal.com/en/.
18
In 2021, it had approximately 3,544 stocks.
19
Wilshire also has a float-weighted and an equal-weighted version of its index. For more information, see
https://www.wilshire.com/.
20
For the NASDAQ 100, the total return index starts in 1999; thus, from 1995 to 1999, we used the price series and then appended the total return series starting in 1999.
21
For the 5% significance level, the critical value for the Jarque-Bera test is 5.99.
22
These ratios are from Bloomberg and may be influenced by missing data and negative-earning companies that are excluded from the P/E calculations for the index.
23
Since this list contains international benchmarks, like MSCI, if one wants to know the relative use of these benchmarks for U.S.-only benchmarks, one can compute the relative percentage after removing the MSCI component. For example, if one does this, the relative percentage of S&P 500 used as a domestic benchmark is 53% for AUM and 32% for strategies.
24
We considered using the Russell 3000 as our benchmark because it is representative of the larger market. However, our data source does not have a flag indicating every stock included in the Russell 3000 historically, and tickers and CUSIPs are recycled. Even with a list of distinct, historical Russell 3000 tickers, if we searched for these tickers in our data set, we might not find them. Our next natural choice of benchmark was the S&P 1500 Composite, which combines the S&P 500, 400, and 600. For no particular reason, we did not choose this as our benchmark. Alternatively, we could have created a custom benchmark closely related to the Russell 3000. That is, for every year of data, we could have ranked all the stocks in the United States by market capitalization and called that group of stocks our benchmark. We would have rerun this ranking, just as Russell does, for every year of data and created a customized benchmark related to the well-known Russell 3000.
25
The relationship between factors and returns is easier to describe for the fundamental factor model than for the economic factor model. For the fundamental factor model, we can describe the relationship in terms of the sign of the estimated factor premium; for the economic factor model, the sign of the estimated factor exposure varies from stock to stock. For some factors, we were unsure what the sign should be. These were given an ambiguous signal.
26
Econometricians say that all the information is in the outliers, anyway.
27
Appendix 16B can be found under Chapter Appendices at
https://ludwigbc.com/books/qepm/exclusive_qepm_content_2020/
or at
www.ludwigbc.com
and look for QEPM Exclusive Content.
28
We did not consider the MSCI-KLD socially responsible factors for this exercise, because we only had data through 2018, while our testing period extends through 2020.
29
For the rank correlation, we calculated the Kendall statistic. A Kendall statistic close to 100% implies that two factors rank stocks exactly the same way, whereas a statistic near −100% implies that two factors rank stocks in exactly the opposite way. The Kendall statistic is a ratio. The numerator equals the number of factor pairs that rank two variables the same way minus the number of pairs that rank two variables completely differently. The denominator is the total number of factor pairs. We adjusted the Kendall statistic for the panel structure of the data. That is, we calculated the numerator and the denominator for each period and then aggregated over the entire time period. The same adjustment was made for the correlation calculation.
30
This allowed us to focus solely on the extra return from
α
MF
rather than from
α
B
.
31
We did not use data from the same month twice, so there were no overlapping data. If we had, interpretation of the
p
-value would have been quite complicated.
32
See
Chapter 8
for a discussion of VAR.
33
As mentioned several times before, you can consider this also the value of the factor exposure as of the end of month
T
.
34
We thank Steve Glass of Aber Noser for supplying us with transactions costs data from 2010 to 2020 for the purposes of our backtests. We also thank Wayne Wagner of the former Plexus Group for supplying us with similar data from 1994 to 2004.
35
This increased the large-cap costs and slightly decreased the small-cap costs. We chose not to define a cutoff point between large-cap and small-cap and use separate costs for each category. Many stocks would have been categorized as either small-cap or large-cap despite being very close to the cutoff point. An alternative would have been to interpolate the costs around the break point dividing large-cap and small-cap stocks.
36
The superscript
b
indicates before the rebalancing. The superscript *, as is conventional, indicates that the weights of the portfolio were created from the optimization.
37
The portfolio
β
is simply the weighted average of the
β
’s of individual stocks, where the weights are the portfolio weights.
38
This comes from
Eq. (12.13)
in
Chapter 12
