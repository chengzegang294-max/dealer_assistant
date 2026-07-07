# Quantitative Equity Portfolio Management: An Active Approach to Portfolio Construction and Management, Second Edition

- **book_name**: 5073 Quantitative Equity Portfolio Management, Second Ed.
- **main_source**: epub
- **cross_check_source**: none
- **pdf_role**: not_needed
- **split_scope**: chapter file = chapter05

---

CHAPTER 5
Stock Screening and Ranking
Our life is frittered in detail … simplify, simplify
.
—Henry David Thoreau
5.1 INTRODUCTION
The aim of quantitative equity portfolio management (QEPM) is to refine investing to a reliable, repeatable, quantitative method that avoids the biases and errors of purely qualitative stock picking.
Stock screening
is the ranking of stocks within the investment universe such that they are separated easily into those that are more favorable and those that are less favorable according to the views of the portfolio manager. Screening also can be used to narrow the investment universe. There are two kinds of stock screening, sequential and simultaneous. In
sequential
screening, the portfolio manager prioritizes his or her stock-picking criteria. He or she eliminates stocks from the investment universe first based on the most important criterion, then based on the second most important criterion, and so on and so forth until he or she has reduced the investment universe to a list of stocks that meet all his or her criteria. The more advanced version of stock screening is multifactor simultaneous screening. In
simultaneous
screening, the manager applies all the criteria to the investment universe at once. As a result, all the stocks in the universe receive rankings according to their overall scores on the entire set of criteria.
One of the most popular simultaneous screening methods is what we call the
aggregate
Z-
score approach
. It involves choosing factors that explain stock returns and aggregating the factors into one score with which to rank the stocks in the investment universe. A Z-score ranking either can serve as the basis for a whole model of stock returns or can add information to an existing model. The stand-alone Z-score model relates the return of a stock to its Z-score and is sometimes equivalent to the fundamental factor model that we introduced in
Chapter 3
. If a manager is already using a fundamental or economic factor model, the Z-score can be added to the model as the constant term
α
when certain conditions are satisfied.
The stock screening and ranking methods in this chapter are useful starting points for people just beginning to build quantitative portfolios. They are not the most sophisticated tools of portfolio construction, but they are simple to apply because they do not require mastering a great deal of mathematics or statistics. Many practitioners also will find these approaches to be intuitive.
5.2 SEQUENTIAL STOCK SCREENING
Imagine for a moment that a portfolio manager has only one criterion for investing: He or she believes that low P/B ratio stocks provide the highest excess returns. To create his or her portfolio, the manager would compute the P/B ratios of all the stocks in his or her investment universe.
1
He or she then would rank all the stocks from lowest to highest P/B ratio. If the portfolio were to include 60 stocks, then the manager would invest in the 60 lowest P/B ratio stocks on the ranked list. Alternatively, the portfolio manager could have used the inverse of the P/B ratio, that is, the book-to-market ratio (a.k.a., the B/P ratio). Only the criterion for selection would change: the portfolio manager would pick the
60 highest B/P ratio stocks.
2
This rudimentary process is stock screening in its most basic form.
What are the attributes of a good stock screen? A good stock screen should be easy to automate. In other words, it should be easy to run the screen regularly as stock data change. The screen should be easy to replicate as well. Any analyst who has the screening procedure and the raw stock-specific data should be able to run the screen and come up with the same stock list that another analyst would come up with using the same data.
A good stock screen, of course, should accurately reflect the portfolio manager’s preferences. If the goal is to create a
value
portfolio, then the stock screen should use value factors, such as a high B/P ratio.
Finally, in a sequential screen, the factor screens should be run one at a time in order of importance. This means that the first screens should be for the factors that speak most directly to the manager’s investment goals. If market cap is the most important factor in the manager’s mind, then that should be the very first screen.
3
Suppose that we would like to invest in the companies that have the highest positive profit margins (which we suppose we can capture by selecting the top 30% of the S&P 500 by net profit margin) and a third of those companies with the highest B/P ratios. We would first screen our investment universe, the S&P 500, by
net profit margin and choose the top 150 companies (30% of 500). We would eliminate the other 350 companies from our investment universe. The next step would be to sort the top 150 stocks by the B/P ratio. We would keep the 50 with the highest B/P ratios and eliminate the remaining 100.
We implemented this screen of S&P 500 stocks using data as of December 2020.
Table 5.1
shows some of the stocks selected by the screen. First, we chose the 150 stocks with the highest profit margins. It turned out that all 150 had positive net profit margins. The highest (147.9%) belonged to Bio-Rad Laboratories and the lowest (14.7%) to Keysight Technologies. Then we chose the 50 stocks in this group with the highest B/P ratios. Neither Bio-Rad nor Keysight made it through the B/P screen. Among the final 50 stocks, the lowest ratio was 0.23 for American Water Works (which is not included in the table), and the highest was 1.38 for People’s United Financial. With this final list of 50 stocks, our hypothetical portfolio would have been complete.
4
TABLE 5.1
Selected Stocks from a Sequential Stock Screen
5.3 SEQUENTIAL SCREENS BASED ON FAMOUS STRATEGIES
The portfolio manager’s success lies in his or her ability to identify what it is that leads to superior stock returns. Many managers follow an investment style or philosophy that guides their choices, and they may think that this style or philosophy cannot really be quantified. Yet it is possible to devise quantitative stock screens from a wide range of investment approaches. In this section we examine some of the most successful equity managers’ investment strategies—many of them qualitative or fundamental—and translate them into stock screens.
5
The philosophies of each manager and the screens that we built from them are also presented in Tables 5A.1 through 5A.6 in
Appendix 5A
.
Peter Lynch has come up several times already in this book, and as we have noted, he found success with a fairly qualitative portfolio strategy. However, in his books
One Up on Wall Street
(1989) and
Beating the Street
(1993), Lynch also expounds on certain quantitative methods that can be collected in a valuable screening methodology. The Lynch screen is a combination growth-and-value strategy that seeks a P/E ratio that is less than the industry average but also desires a price-to-earnings-to-growth (PEG) ratio that is less than 1.0. This indicates that the P/E ratio multiple is less than the growth rate in earnings and that the underlying company is generating strong bottom-line growth given its current market valuation. The P/E ratio to dividend yield is limited to stocks with a ratio of less than 4.0, which helps to provide adequate income and downside protection against further market deterioration. By restricting the growth rate in earnings to greater than 0% but less than 50%, we are including stocks with positive earnings momentum and excluding stocks that Lynch would believe to be at risk for failing to meet expectations owing to overly optimistic forecasts. Stocks with higher growth also may be candidates for accounting manipulation. An insider buying-to-selling ratio of greater than 1.5
also may shed light on management’s view of the future of the business. Insider selling can occur for a variety of reasons, including a diversification of holdings. However, insider buying generally occurs only when management is optimistic about the future of the company and believes that the share price is undervalued. Further screening criteria include a long-term debt ratio of less than the industry median, a market capitalization of less than $5 billion, and institutional ownership of less than 50%. These criteria increase the possibility that the stocks are undervalued and improperly priced because they lack a large or sophisticated following of investors.
Warren Buffett is perhaps the most widely emulated investor in history. Numerous books have been written about his buy-and-hold strategy. By applying Robert Hagstroms’
The Warren Buffett Way
(1994) and perusing Berkshire Hathaway’s annual reports, we were able to construct a simple screen based on Buffett’s investment principles. We first decided to limit the screen to the top 30% market capitalization of listed equities on the New York Stock Exchange (NYSE), American Stock Exchange (AMEX), and NASDAQ, which would aid us in excluding small-cap securities. Buffett generally believes in purchasing stocks that have a strong competitive advantage and are capable of outperforming other companies and demanding a premium for their services. Most small-cap firms fail to possess such strong competitive advantages or the economies of scale necessary to compete against large industry titans. They therefore fail to generate the necessary free cash flow to fund expansion and wield pricing power. Buffett is extremely concerned with management’s ability to operate efficiently and produce superior returns on equity. High free cash flow indicates management’s ability to generate sufficient cash to fund its operations and reward its shareholders for taking on risk. Companies that do not generate sufficient free cash flow may be suffering from liquidity crunches or failing to collect payments on their sales. Hence two screening categories include return on equity (ROE) that is greater than or equal to 15% and free cash flow that ranks in the top 30% of listed securities in the investment database. Net profit margins should exceed industry averages, and the current D/E ratio should be in line with or lower than the industry median. Finally, forecasted free cash flow for the next five years should be greater than the current market price of the stock when discounted back to the present. This may indicate that the stock is
undervalued and provides a “margin of safety” for uncertainty over future returns.
The Lakonishok screen is a value screen based on the work of Josef Lakonishok, the William G. Karnes Professor of Finance at the University of Illinois at Urbana-Champaign. Professor Lakonishok is also the CEO and founder of LSV Asset Management and has published widely in many prestigious academic journals. The crux of the Lakonishok screen is that some companies go out of favor with the market owing to overly pessimistic forecasts that depress their share prices. There is a great potential for profit for the patient investor who can identify which companies eventually will rebound from such depressed prices. The screen aims to avoid small companies that may not possess the necessary financial strength or customer base to weather the downturn. Therefore, part of the screen restricts our investment list to companies with market capitalizations in the top 30% of the NYSE, the AMEX, and the NASDAQ. To screen for undervalued stocks, the price-to-earnings (P/E) ratio and the price-to-book (P/B) ratio are set below their respective industry median values. The consensus earnings estimate for the next fiscal year must be greater than the forecasted earnings estimate for the current year. This helps to eliminate companies that are expected to continue on a dismal trajectory. The final step of the Lakonishok screen is to find companies whose stock returns have performed better than the S&P 500 over the last few months. This upward momentum may indicate the beginning of the turnaround, and it will help to filter out companies whose stock prices will continue to languish.
Another value screen similar to the Lakonishok screen but with an increased emphasis on the underlying financial condition of the firm is a screen based on the work of Stanford Professor Joseph Piotroski. Professor Piotroski is a world-renowned expert in financial statement analysis, and the Piotroski screen seeks to uncover undervalued firms with the necessary financial strength to succeed. As in the Lakonishok screen, market capitalization is restricted to the top 30% of the NYSE, AMEX, and NASDAQ. However, this criterion now takes a backseat to other financial ratios. The P/B ratio is restricted to the lowest 30% of listed securities in the database (the investment universe). Return on assets (ROA) must be positive, and both the debt-to-equity (D/E) ratio and the long-term debt-to-equity ratio are evaluated so as to exclude companies with overly burdensome debt obligations and
inadequate financing. The current ratio and the cash ratio must be improving from the previous fiscal year to offer adequate liquidity to fund current operations. Finally, the asset turnover must show an improvement on a year-over-year basis, which helps to avoid companies that have failed to manage their assets efficiently and realize adequate top-line growth.
A seasoned money manager, David Dreman was the founder and chairman of Dreman Value Management LLC (the value strategies and funds were purchased by Foundry Partners in 2016). He is the best-selling author of several prominent books on the low P/E ratio contrarian value investment approach, including
Contrarian Investment Strategies: The Next Generation
(1998) and
Psychology and the Stock Market
(1977). The Dreman screen attempts to adopt some of the crucial tenets of Dreman’s contrarian philosophy. He favors mid- to large-sized companies because he feels that they have greater visibility in a market rebound, and by being highly scrutinized by a variety of investors, they are less susceptible to accounting manipulation. We therefore have restricted our market capitalization to the top 25% of the S&P 1500. The contrarian strategy seeks out-of-favor stocks, and thus we have limited our investment options to stocks whose P/E ratios are in the lowest 40% of the S&P 1500. This helps to identify undervalued securities. A requirement that the D/E ratio be less than 1 and that the total-liabilities-to-total-assets ratio be less than the industry average ensures that the companies have adequate financial strength. A dividend yield above the S&P 500 dividend yield offers a cushion and provides downside protection to companies in a prolonged downturn. The final major criterion is that earnings growth must continue to outpace the S&P 500 and industry median levels on a current and forecasted basis. All these screening steps attempt to identify firms that may be trading below their historical price levels but still show potential for future development and bottom-line growth that has not yet been priced into the stock.
Another famous investor and one whom Warren Buffett studied extensively in developing his own investment philosophy is the late Philip Fisher. Fisher authored several books on his investment strategy, including
Common Stocks and Uncommon Profits
(1958) and
Conservative Investors Sleep Well
(1975). Fisher believed that the business cycle made annual sales growth inherently unpredictable and failed to convey the proper underlying ability of the business to succeed. Year-over-year metrics could be distorted eas
ily by slight alterations in the business environment and therefore should be judged in light of other, longer-term trends. We therefore have decided to screen for companies whose sales have increased on a year-to-year basis for the last five years and whose three-year compound growth rates in sales are greater than their industries’ median sales growth rates over the same period. This helps to smooth out the effects of the business cycle and include only companies that have consistently performed above average in a variety of economic conditions. Fisher also was interested in identifying growth that was a result of a low-cost advantage, strong marketing organization, a strong research and development enterprise, and excellent management depth with the utmost integrity. Growth was important, but only in the context of value, so we confined the PEG ratio to be greater than 0.1 but less than 0.5. This helps to ensure that the stock multiple neither gets ahead of the growth rate in earnings nor falls too far below it. Fisher believed that research and development (R&D) was an important component for maintaining a competitive advantage, but only if it could generate a high level of sales per R&D expense. Hence we have decided to add the criteria that R&D expenses as a percentage of sales be greater than the industry median ratio and that sales growth keep up with or exceed the growth in R&D expenses. Finally, we screen for companies that are not expected to pay a dividend and therefore are likely to reinvest any retained earnings for the future growth of the business.
Bill Miller was the CEO of Legg Mason Capital Management, Inc., a division of the Baltimore financial services firm Legg Mason (purchased by Franklin Templeton Investments in 2020). He managed the Legg Mason Value Trust from 1982 to 2016, beating the S&P 500 in 21 of those 35 years. In 2016, he left Legg Mason and created Miller Value Funds. Miller adheres to a value strategy that aims exclusively for securities that trade below their intrinsic value, as indicated by his multifactor valuation analysis. His strategy differs from that of many value managers in that it focuses on cash earnings rather than on accounting earnings. Many of his holdings, including positions in several “new economy” growth stocks such as internet high fliers Google, Amazon, and Facebook (as of the end of 2020), continue to be controversial among “pure value investors” owing to their speculative and/or growth qualities.
The Miller screen attempts to capture the core principles of his strategy by combining various financial metrics aimed at discovering undervalued companies that possess the necessary competitive advantage to sustain a high level of growth. The first major criterion in the Miller screen is that the current market capitalization of the company cannot exceed three times the total estimated free cash flow for the next five years. This is a value ratio that attempts to eliminate companies whose current market valuation appears overly optimistic and exceeds the amount of discretionary cash the business is expected to generate over the next several years. Free cash flow also should be increasing on a year-to-year basis. This helps to reaffirm Miller’s emphasis on cash flows and cash earnings as the impetus behind the dynamics of valuation. The PEG ratio then is restricted to a level of 1.5 or below. A maximum of 1.0 may be too restrictive in this screen because we do not want to eliminate growth companies that may have P/E ratio multiples slightly higher than their growth rates but nevertheless still may possess vast potential that has failed to be discounted properly into the stock price. A skilled management team is highly crucial to success, and therefore, the Miller screen takes into account that gross margins should be increasing and that ROE should exceed the industry median. Finally, the long-term debt ratio should be below industry average levels to prevent future liquidity difficulties or cash-flow shortages.
The late Richard Driehaus was the founder of Chicago-based Driehaus Capital Management. It was one of the top small- to mid-cap money managers. His superior investment performance resulted in his acceptance to the elite
Barron’s
All-Century Team of fund managers, whose members include such luminaries as Peter Lynch and Sir John Templeton.
The Driehaus screen is structured around earnings and price momentum. The initial steps focus on year-over-year positive and increasing earnings growth. The next major aspect of the Driehaus screen incorporates earnings surprises. Earnings surprises to the upside are taken as a positive signal of a company’s ability to generate income and capitalize on its position in the market. A failure to meet expectations is taken as an indication that the company is failing to execute its strategy and that it may be facing increasing costs or intensified competition. The screen looks for companies that have had positive earnings surprises over the last
fiscal year, meaning that the actual rate of earnings growth has exceeded analyst estimates during the most recent time period. The strategy also values surprises in which the range or standard deviation of the estimates is tighter or more significant on subsequent returns. Price momentum then is evaluated to ensure that there is sufficient buyer pressure on the stock price to encourage further demand and maintain an upward trajectory. The screen requires that the current market price be greater than its 200-day moving average, which indicates a long-term uptrend in the stock. The 50-day moving average then is set at greater than the 200-day moving average so that we can eliminate stocks whose momentum has already peaked. The on-balance volume (OBV), a technical indicator that compares price to volume, then is used to determine if the momentum is a net accumulation of shares or a distribution. Finally, the screen requires that the company be followed by fewer than five analysts so that there is a good chance of improper valuation, giving the astute investor an opportunity to purchase neglected securities and profit immensely when the market recognizes their potential.
Several other screens listed in the tables in
Appendix 5A
include the Neff contrarian screen, the Muhlenkamp screen, the Templeton screen, and the Dogs of the Dow screen. The Neff screen draws on the fundamentals of legendary Vanguard Windsor Fund manager and former
Barron’s
Roundtable member John Neff. Neff’s value strategy, explained in his book
John Neff on Investing
(1999), targets low P/E ratio stocks with strong sales growth, healthy operating margins, increasing free cash flow per share, and underhyped estimated earnings growth between 7% and 20%. The Muhlenkamp screen is a growth-and-value screen based on Ronald Muhlenkamp’s investment strategies and mutual fund performance. It seeks an above-average and stable ROE figure over the last five years. It looks for strong earnings growth, low P/E and P/B ratios, and adequate liquidity, as indicated by the current ratio and others. The O’Shaughnessy value-and-growth screens are named after seasoned investor Jim O’Shaughnessy, who still manages the O’Shaughnessy Funds. Their strategy is to gather data on companies and turn those data into custom factors that can be used to evaluate each stock; these custom factors are then used to build a portfolio with the highest-ranking factor profiles while also managing risk exposures and implementation costs. The Templeton screen has an international focus rooted in the strategies of global
pioneer investor Sir John Templeton.
6
It seeks value—through low P/B and P/E ratios, as well as strong forecasted and actual earnings-per-share (EPS) growth—in an entire universe of securities such as the Compustat database.
7
ROE and operating margins for the trailing 12 months should be above average, and financial strength should be strong enough to face a downturn in market conditions. Finally, the Dogs of the Dow screen is a simple strategy of choosing the top 10 highest-yielding stocks in the Dow Jones Industrial Average at the beginning of the year and holding them.
Further information on these screens and others, including background information, a description of the screen, and the actual screening steps, is included in Tables 5A.1 through 5A.6 of
Appendix 5A
.
5.4 SIMULTANEOUS SCREENING AND THE AGGREGATE Z-SCORE
In the preceding section we discussed the simplest type of screening, sequential stock screening. A more sophisticated way to refine the investment universe is to use multifactor simultaneous screening (a.k.a.
simultaneous screening
). In simultaneous screening, the portfolio manager still picks stocks according to a list of factors, but he or she screens for all the factors at once rather than one at a time. He or she therefore does not need to prioritize the factors in advance of screening. The entire list of factors is taken as a single set of criteria with which to evaluate all stocks in the investment universe.
Since the stocks undergo just one screen rather than multiple rounds, there is no chance of eliminating an otherwise good stock simply because it does not measure up during an early round of screening. For example, suppose that the portfolio manager believes that both the B/P ratio of a stock and its change in gross profit margin are equally important in selecting stocks. With sequential screening, he or she would have to make a choice to screen first for one factor or the other. If he or she screened first for high B/P ratio stocks, he or she might throw out a lot of companies
with tremendous profit growth. Simultaneous screening sidesteps this problem by considering stocks for both their B/P ratios and their profit growth concurrently.
Another benefit of simultaneous screening is that the portfolio manager is in no danger of running out of stocks. In sequential screening, the stock list gets smaller and smaller with each successive factor screen. When screening with four or more variables, it is not unusual to end up with a list of fewer than 20 stocks—hardly sufficient for an entire portfolio and probably not diversified in any case. Simultaneous screening preserves all the stocks in the universe and assigns each of them a score based on the whole set of factors.
Once a portfolio manager has chosen the list of factors, how does he or she screen for all of them at once? Unfortunately, since different types of factors are expressed in different units, adding all the factor values together does not work. For a two-factor list of the B/P ratio and size, trying to add a B/P ratio of 0.08 (P/B of 12.5) and a size of $36,026,000,000 would yield a meaningless number. It does not scale the factors, so the size, which is by far the larger factor in terms of absolute value, dominates the stock ranking.
The right way to aggregate factors is to
standardize
or
normalize
them. Standardization or normalization refers to transforming variables so that they are comparable with each other by converting them to a standard unit of measurement. The most commonly used standardization method is known as the Z-
score method
.
8
5.4.1 The Z-Score
A population of data has a cross-sectional mean and variance. For example, as of December 2020, the average value of the B/P ratio for all stocks in the S&P 500 was 0.3577. The standard deviation of the
B/P ratio of all firms in the S&P 500 was 0.3794.
9
We can use this information to standardize any value of B/P ratio for any stock in December of 2020. We obtain the Z-score value of any stock’s B/P ratio by taking the difference between the stock’s B/P ratio and the mean value of the B/P ratio for the universe of stocks and then dividing the difference by the standard deviation of the B/P ratios of all stocks in the universe. Standardizing the values of factors allows us to make clear statements about how far any particular observation is from the population mean. For example, if we find a company with a B/P ratio Z-score of 2, then we can say that the company’s value is 2 standard deviations away from the population mean. The Z-score therefore shows how far a stock is from the norm.
The Z-score also allows us to compare the values of two different factors. Suppose that, as a portfolio manager, you think that companies with high B/P ratios and high profit growth are buys. There is one company whose normalized B/P ratio value is 2 (i.e., the company’s B/P ratio is 2 standard deviations from the mean of all the companies’ B/P ratios) and whose normalized value of profit growth is also 2. Since the values are normalized (or standardized), you can say that this particular company is as desirable from the perspective of the B/P ratio factor as from the perspective of the profit-growth factor. Also, since both factors are measured in the same units, you will be able to combine these factors into an aggregate Z-score.
In certain situations, standardization is truly normalization, and this is in part why this terminology is used. If the original cross-sectional distribution of the stocks’ factor exposures is a
normal distribution—and many things in society follow a normal distribution—then we can make clear statements about how probable a particular observation is or how rare it is. For example, a normalized factor score of 2 would mean that the probability of obtaining a stock with a higher value would be less than 2.27%.
10
Let’s look at the mechanics of assigning Z-scores. First of all, a portfolio manager should make sure that the Z-scores match the underlying factor values. That is, if high Z-scores are going to represent good stocks and low Z-scores bad stocks, then the factors themselves must be expressed such that high values are good and low values are bad. For instance, if a high book-to-price (B/P) ratio is considered a good quality in a stock, then the B/P ratio must be used to create the Z-score, not the P/B ratio.
11
Once this issue is resolved, to create a Z-score for a factor, a portfolio manager needs to compute the mean (or average) value of the factor for all stocks in the investment universe.
12
Call this value
for factor
k
.
13
The next step is to compute the standard deviation of the factor across all stocks in the investment universe. Call this value
S
(
β
k
) for factor
k
.
14
Putting these pieces together, the Z-score computation for stock
i
for factor
k
is
where
z
i,k
represents the Z-score of factor
k
for stock
i
, which is the normalized value of the factor value.
5.4.2 The Aggregate Z-Score
Multifactor simultaneous screening means screening for more than one factor (hence the name
multifactor
), but since all factors must be screened for simultaneously, they need to be combined into a single screening value for each stock. Once we have calculated a Z-score for every factor of every stock in the investment universe, calculating each stock’s aggregate Z-score is fairly straightforward. Since Z-scores are
scale independent
, we can simply add them together. The sum of a stock’s Z-scores is its
aggregate
Z-
score
.
There may be some individual factor or stock aggregate Z-scores with extreme values. Different portfolio managers will deal with these in different ways. If it seems that a Z-score is an
outlier
, then one control mechanism is to round all Z-scores above 3 down to 3 and similarly to round up all Z-scores below −3 to −3.
15
It is also possible to throw out stocks that have extreme Z-score values, but this may result in the loss of good information about potentially very high-return or very low-return stocks. In
Appendix 5B
, we discuss several methods to deal with outliers.
We can choose how to weight each of the factors within a stock’s aggregate Z-score. One option is to weight all the factors equally. The aggregate Z-score with
K
factors then would equal
where
is the aggregate Z-score for stock
i
, and
z
i,k
represents the Z-score for factor
k
and stock
i
. The equal weighting of Z-score factors is a common method portfolio managers use to compute aggregate Z-scores. Some portfolio managers prefer equal weighting to more sophisticated weighting schemes because it produces relatively more stable results.
5.4.3 Ad Hoc Aggregate Z-Score
There are also a number of ad hoc ways to weight the individual factor Z-scores within the aggregate Z-score. The portfolio manager can weight the factors according to his or her ex-ante beliefs or investing style. If he or she prefers the value factor above all others,
he or she can amplify its importance by assigning it a weight of 80% and dividing the remaining 20% weight among the rest of the factors. Factor Z-scores also can be weighted according to some interpretation of their relative levels of importance in influencing stock returns. It is important not to let this sort of weighting scheme be unduly influenced by past research or past reading, which could amount to “data snooping.”
16
In any case, since weighting according to general ideas of factor importance and weighting by preference are not methods of quantitative portfolio management, we do not recommend these methods.
Some portfolio managers weight the factor Z-scores according to the factors’ information ratios, obtained by creating decile or quintile portfolios of each factor and computing the factor’s historical information ratio.
17
The higher the information ratio, the more important the factor is in predicting stock returns. Factors with high information ratios are weighted more heavily. This ad hoc procedure has more merits than weighting according to general notions of factor importance, although it still neglects the effect of the correlation between factors.
5.4.4 Optimal Aggregate Z-Score
Equally weighting the Z-score factors is a simple procedure. However, it ignores certain information contained in the data. It ignores the importance of each factor Z-score in predicting the returns of stocks. The ad hoc methods of weighting attempt to assign weights that vary with the perceived importance of the factors, but these methods are highly subjective. Both the equal weighting and ad hoc methods also fail to account for the correlation between factors. We can find better ways to weight the factor Z-scores. There are several
optimal weighting
methods.
One very common approach to optimal weighting is to use econometrics to estimate the optimal exposures using a historical sample data set. The portfolio manager takes a series of monthly returns on all the stocks in the universe, combined with the factor Z-score values for each stock at the beginning of the month, and
runs a set of cross-sectional regressions over the sample period to find the optimal Z-score weights.
18
Suppose that we have
K
factor Z-scores for each of the
N
stocks in the universe and that we have
T
periods of return information (e.g., 120 months of sample data). We can use the following econometric techniques to estimate the parameter exposures of each factor. This will tell us the best way to combine Z-scores so as to use the information contained in the variance-covariance matrix of Z-scores and returns. One can estimate the following regression with a sample of historical data:
where
γ
i
represents a constant term,
δ
k
is the coefficient estimate for the contribution of the factor Z-score
k
to the stock returns, and
ϵ
i
is a typical error term.
19
The regression can be estimated as a panel regression. The
δ
estimates are the optimal combination of the factor Z-scores.
20
The portfolio manager might run this type of regression over various horizons and time periods to check the robustness of the results.
A variation on the optimal weighting scheme is to determine the optimal weights for various economic scenarios. The portfolio manager constructs three or more hypothetical economic environments and calculates a set of optimal Z-score weights for each of
them. This method requires the exercise of more subjective judgment than the original method does, but it gives the manager a chance to consider which way the economic winds are blowing and to weight the factors accordingly.
It might be useful to provide a simple example of the aggregate Z-score procedure using real stock data. For simplicity, we took a snapshot of stocks from the S&P 500 as of December 2020.
Table 5.2
shows 10 selected stocks from the S&P 500 with their corresponding factor values for E/P, B/P, and D/E ratios, the natural logarithm of market capitalization (SIZE), and the 12-month momentum (M12M), i.e., the average monthly stock return over the previous 12 months.
21
These factors do not necessarily represent some phenomenal
α
model; they were chosen merely for illustration. One will notice that the table gives the mean and standard deviation of all stocks in the S&P 500 for the month of December 2020. We will need these values to compute the Z-scores.
TABLE 5.2
Selected Factor Exposures and Z-Scores of Selected Stocks
To compute the Z-score for the B/P ratio factor of the tech company Apple, we need the value for
β
AAPL,B/P
= 0.0290 for December 2020. The mean for all the S&P 500 stocks is 0.3577 (i.e.,
= 0.3577), and the standard deviation is 0.3794 [i.e.,
S
(
β
B/P
) = 0.3794]. Thus the Z-score for the B/P ratio factor for Apple is −0.866 [
z
AAPL,B/P
= (0.0290 − 0.3577)/0.3794]. Although the sign is negative for the Z-score, this does not necessarily imply that it will be a negative contribution to the aggregate Z-score. This will depend on the portfolio manager’s ultimate belief regarding this factor. If the portfolio manager believes that a high B/P ratio is a negative for picking stocks based on his or her previous analysis, he or she should multiply this factor Z-score by −1 when computing the aggregate Z-score so that higher Z-scores imply a better stock.
One can continue computing the Z-scores for the other factors for Apple. They are all listed in the table. The aggregate Z-score then will be a combination of the individual Z-scores for each factor. In this example, we assume that the portfolio manager
equal-weights
the individual Z-scores. Thus the aggregate Z-score for Apple in December 2020 is equal to −0.645. It is important that in aggregating the individual Z-scores, the portfolio manager uses the appropriate
sign for each individual Z-score according to his or her beliefs. For example, to obtain the aggregate Z-score, we did the following:
A negative sign precedes several factors’ Z-scores because these factors are considered detrimental to stock returns. All individual factor Z-scores must possess the correct sign. The portfolio manager in this example likes stocks with high E/P and B/P and low D/E ratios, so the negative of the D/E Z-score is added to the total Z-score, while the E/P and B/P Z-scores are added as is. The manager also likes smaller-cap stocks, hence the negative sign in front of the Z-score for the SIZE. He believes that momentum in stock returns is a positive technical indicator, so the momentum Z-score is added to the total Z-score. For a different portfolio manager, the signs might be different. The important thing is consistency. If high exposure to a factor is supposed to boost stock returns, add the factor’s Z-score to the total; if high exposure to a factor is supposed to hurt stock returns, subtract its Z-score.
Table 5.2
goes through the computations of Z-scores for nine other stocks from the S&P 500 in December 2020. A portfolio manager would do this for all stocks in his or her investment universe and then rank the stocks by their aggregate Z-scores to determine which stocks are the most and least attractive.
5.4.5 Factor Groups and the Aggregate Z-Score
Some quantitative portfolio managers choose to separate the
K
factors that they use into
M
factor groups. For example, suppose that we have a B/P ratio factor, an E/P ratio factor, and a price-to-sales (S/P) ratio factor. A manager might create a composite group known as the
valuation group
and place all three of these factors into the valuation group. He or she may do this for other factors as well.
Although dividing the factors into groups might seem at first like an arbitrary step, it offers several benefits. It organizes the screening process. Rather than having to keep track of a large group of
K
factors that all represent different attributes of stock returns, the manager will be able to look at the factors in sets of
M
groups that represent the essential forces that are believed to affect
stock returns. This simplifies both modification of the model and presentation of performance results to an investment committee.
Second, a manager might be tempted to use only one factor to represent a category such as value. However, to the extent that there are idiosyncracies in the way individual factors represent the same concept, it might be better to collect more than one factor to represent the concept (e.g., using B/P, S/P, and E/P ratios to represent value rather than just the B/P ratio in isolation).
Third, by creating factor groups that represent fundamental forces on stock returns, a manager can easily change the weights (which represent the relative importance) of factor groups according to changing economic conditions or for other reasons.
21
Although one could change the relative weights of each of the
K
factors individually, it is easier to change the weights of
M
factor groups, where
M
<
K
.
Formally creating composite Z-scores using factor groupings is relatively straightforward. The following steps are very similar to the procedure for aggregate Z-scores discussed in the last section.
1.
Determine the number of factor groups
M
. For example, if
M
= 4, we might have a
valuation composite
, a
profitability composite
, a
financial-soundness composite
, and a
technical composite
. These four composites or groups represent the four main themes that we believe predict stock returns in our investment universe.
2.
Decide which factors to include in each factor group. For example, the manager might believe that B/P, E/P, and S/P ratios are all factors that determine value and place those in the valuation composite. He or she then might decide that gross profit margin belongs in the profitability composite. The inverse interest coverage ratio (IICR) and the firm’s debt-to-equity ratio then might go in the financial soundness composite. Finally, the manager might put a factor such as momentum in the technical composite.
3.
Compute all the factors for every stock in the investment universe. Thus, if there are
N
stocks in the investment
universe and
K
factors, the investor will have to make
N
×
K
computations.
4.
Compute the mean and standard deviation of each factor exposure in the cross section of all the stocks in the investment universe. These values should be stored. Label these as
and
S
(
β
k
), respectively, for each factor
k
.
5.
Compute the Z-scores for every factor and every stock. This is similar to the preceding section, where
z
i,k
=
represents the Z-score of factor
k
for stock
i
, which is the normalized value of the factor value.
6.
Compute the aggregate Z-score for
every factor group
for every stock. Thus, for each factor group, compute the group Z-score for stock
i
, that is,
where
S
m
is the set of factors in the
m
th factor group,
is the weight of factor
k
in the
m
th factor group (so that
, and
z
i,k
represents the Z-score of factor
k
for stock
i
. This weighted sum is computed for every factor group to obtain a factor group Z-score for every stock and every factor group.
7.
Compute the aggregate Z-score for every stock in the universe. This is the final step for the ranking of the stocks. The final formula is to compute
where
is the aggregate Z-score for stock
i, w
m
is the weight given to the factor group
m
, and
is the factor group Z-score for group
m
for stock
i
.
This procedure is almost identical to the procedure for computing aggregate Z-score. The only real difference between the two is that here we have classified the individual factors into specific factor groups. We have not discussed how to weight the relative factor groups or how to weight the factors within factor groups. The methods available are similar to the ones we described in the preceding section. If the weighting scheme of the factors within groups and across groups is similar to the weighting scheme in the normal Z-score aggregation without groups, this final step should
produce results similar to the results of the procedure that does not divide factors into groups.
Let’s walk through a simple example of grouping factors. We return to the example from an earlier section that uses data for S&P 500 stocks for December 2020. Following the seven steps of factor grouping, our first step is to choose the number of groups. We choose four factor groups (
M
= 4). The groups are a
valuation composite
, a
profitability composite
, a
financial-soundness composite
, and a
technical composite
.
Our second step is to decide which factors will go in each composite. Suppose we decide on the following factors for our model: E/P, B/P, and S/P ratios; gross profit margin (GPM); IICR and D/E; and M12M.
22
It makes sense to place the first three factors in the valuation composite, the next one in the profitability composite, the next two in the financial-soundness composite, and the last one in the technical composite. See
Table 5.3
.
TABLE 5.3
A Possible Categorization of Factors into Composite Groups
The third step is to compute the factor values for all stocks. We have listed these for selected stocks in
Table 5.4
. The fourth step is to compute the mean and standard deviation of all the factors for the investment universe. In this specific example, the S&P 500 is our investment universe. The mean and standard deviation of each factor are listed in the table as well. The fifth step is to compute the Z-scores for every factor, and the sixth step is to compute the Z-scores for each factor group. We equally weighted the Z-scores of
each factor within a group to obtain the factor group Z-scores for each stock listed in the table.
TABLE 5.4
Selected Factor Exposures and Group Z-Scores of Selected Stocks
The next step is to calculate the factor group Z-scores. As in the aggregate Z-score procedure, the factor Z-scores should be added together (or subtracted from each other) according to the way they are expected to contribute to (or detract from) stock returns. For example, to obtain the valuation Z-score of Microsoft (
z
MSFT,V
), we take our three valuation factors of Microsoft and equal-weight them, making sure the signs are correct.
23
Since the portfolio manager believes that higher E/P, B/P, and S/P ratios signal “good” attributes of stocks, each individual Z-score can be added together without multiplying by −1, that is,
Applying the same process to each factor group, we can calculate other factor group Z-scores for Microsoft as well, including the profitability Z-score (
z
MSFT,P
= 1.273), the financial-soundness Z-score (
z
MSFT,F
= 0.231), and the technical Z-score (
z
MSFT,T
= 0.582). Microsoft receives a poor valuation rating owing in particular to its unusually low B/P and S/P ratios. It scores a very good rating for profitability given its gross profit margin of 76.25% compared to the S&P 500 average of 43.26% and also receives a good rating for financial soundness due to its lower-than-average debt-to-equity ratio and lower-than-average inverse interest coverage ratio. Microsoft also earns decent marks for its technical group, directly due to the factor M12M: relative to the investment universe, its stock price has grown over the last year by 42.5% compared to the S&P 500 average of 15.24%. With an aggregate Z-score of 0.423, Microsoft is overall a mildly attractive stock as of December 2020, according to the set of criteria used in this example (see
Table 5.4
).
5.5 THE AGGREGATE Z-SCORE AND EXPECTED RETURN
5.5.1 Expected Return Implied by the Z-Score
Expected stock returns can be found from aggregate Z-scores by performing a regression of actual stock returns against the aggregate Z-scores. This can be done using a panel series regression of stock returns on the Z-score of the prior periods (e.g., of the previous months). The regression would take the form
where
γ
i
represents a constant term,
24
δ
is the coefficient that relates the aggregate Z-score to the stock return, and
ϵ
i,t
is a typical error term. Given the estimates of
γ
i
and
δ
, the expected return of stock
i
for time
T
+ 1 can be written as (see
Fig. 5.1
)
FIGURE 5.1
Timeline.
There are some problems with this methodology. First, Z-scores may not change much from one period to another, but factor premiums may change substantially. Thus one’s estimated coefficients may not be stable or reliable. One way to reduce this problem is to run panel regressions on a larger period of historical data rather than just one single cross-sectional regression over one particular period.
25
The second problem is that there may be a low correlation between the Z-score and the subsequent returns. While we are using Z-scores at time
t
to predict stock returns at time
t
+1, the
link might be rather weak because the equation is not based on a rigorous theory.
The third problem with this procedure is that it adds complexity to the process, which is a weakness given that the biggest strength of the aggregate Z-score model is its simplicity.
5.5.2 Forecasting Rule of Thumb
Many portfolio managers are familiar with the
forecasting rule of thumb
and love to talk about it.
26
We personally do not understand what makes this equation so exciting because it is essentially an algebraic manipulation of a simple regression equation. We will make a few comments about it, though, because it may have some limited use in QEPM.
One can manipulate
Eq. (5.8)
and obtain the following:
In this equation,
IC
is by definition the correlation between the aggregate Z-score or raw signal and the actual security returns, the volatility in this particular case represents the cross-sectional volatility of the returns of the securities, and score refers to the aggregate Z-score.
27
Although this is a neat formula, the portfolio manager should be sufficiently well versed in econometrics not to need this transformation of variables to make a connection between the raw scores or aggregate Z-score and the actual returns or residual returns of the security. This equation would be helpful if, for some
reason, it were easier to compute
IC
and volatility than to run a regression. Otherwise, the equation does not add much to the screening process.
28
5.5.3 The Equivalence between the Z-Score Model and the Fundamental Factor Model
We can show that the Z-score model of
Eq. (5.8)
produces an expected return identical to that of the fundamental factor model under certain conditions. Specifically, if
the factor premium is inversely proportional to the standard deviation of the factor exposure
, then the aggregate Z-score model produces the same result as the fundamental factor model.
Let us assume that the factor premium is inversely proportional to the standard deviation of the factor exposure. Let
β
k
be the exposure to the
k
th factor and
f
k
be the premium on the
k
th factor.
Then
where
c
is a constant. Then the fundamental factor model can be rewritten as
where
ᾶ
i
is a constant defined as
Equation (5.12) shows the relationship between the parameters of the aggregate Z-score model and the parameters of the fundamental factor model.
Certain conditions may give rise to an inverse proportionality between the factor premium and the standard deviation of the factor exposure. When the factor exposure variation is large, even a small factor premium can affect the excess return tremendously. Thus, to preserve the overall excess return of the universe, it might make sense to have the factor premium be proportional to the inverse of the standard deviation of the factor exposure. This would imply that a factor with extremely high variation has a low factor premium, thus in some sense preserving the balance of excess return.
5.6 THE AGGREGATE Z-SCORE AND THE MULTIFACTOR
α
Ultimately, most portfolio managers will have to optimize their portfolios versus a benchmark and cannot apply ad hoc weightings to the stocks in the portfolio. Typically, many portfolio managers will use commercial software to perform the optimizations versus a benchmark.
29
Commercial software allows the user to supply the multifactor
α
(i.e., the part of the expected return that a multifactor model cannot explain). Many portfolio managers transform the aggregate Z-score into a multifactor
α
. In this section we examine three popular methods for doing this, discussing the strengths and weaknesses of each method.
Perhaps the simplest method is a one-to-one transformation that uses the actual Z-scores as
α
’s. Although the aggregate Z-scores clearly do not represent the actual excess returns of the stocks, they do represent the relative ranking of each stock in the manager’s mind. Thus, we could just use the Z-score as a surrogate for the
α
of each stock. One immediate problem with doing this is that if the Z-scores do not really represent returns, they could distort the stock-selection process by favoring stocks with extremely high predicted Z-scores much more than is justified by real excess return
potential. Fortunately, though, if the Z-scores are treated for outliers, such as using either windsorization, the IQR method, or the Rank method, the Z-scores will reside within a limited range (e.g., +3 to −3). In the extreme case of limiting Z-scores to a range of +3 to −3, the highest
α
a particular stock can have is 3% above its expected return, and the worst it can have is 3% below its expected return, with most values falling somewhere between +1 and −1.
30
Therefore, one could add the aggregate Z-score to the expected return of each stock predicted by a risk model. If one uses a standard commercial software package to build the portfolio, then the software will add these aggregate Z-scores to the expected returns of each stock according to the software’s risk model. One then performs an optimization to form the portfolio.
31
The basic point is that if the portfolio manager has constructed trimmed aggregate Z-scores, one method to convert aggregate Z-scores to the
α
of each stock is just to do a one-to-one mapping in which the
α
of each stock equals the aggregate Z-score of each stock.
The second method is to use the expected excess return from
Eq. (5.9)
as
α
. This is a more accurate method since the empirical relationship between the Z-score and actual stock returns is taken into account.
The third method is more complicated. This method attempts to link the Z-score to residual stock returns rather than actual stock returns. The residual stock returns can be computed with respect to a multifactor model or a benchmark. The idea is to obtain all stocks’ factor exposures and factor premiums and use them to calculate historical
α
. Then one can estimate the relationship between
α
and the aggregate Z-score from the following regression:
where
r
i,t
is the return of stock
i
at time
t
,
is the estimated factor exposures of stock
i
,
f
t
represents the realized factor exposures at time
t, γ
i
represents a constant term,
δ
is the coefficient that relates the aggregate Z-score to
α
, and
ϵ
i,t
is a typical error term.
32
Then the
portfolio manager can use the estimates from this equation to forecast the
α
’s of all the stocks for the next period (
t
+ 1) given their aggregate Z-scores for time
t
. Thus, with the estimated coefficients, the portfolio manager can translate aggregate Z-scores into
α
’s. These values eventually will be used with a risk optimizer to create a portfolio of stocks.
There are drawbacks to all three of these methods. It may introduce serious distortion if the data behind the Z-score and the data behind the factor model are not sufficiently different. In such a case, the information criterion will be violated.
33
The second and third methods also require more computation, and the improvement in the optimization may not compensate for the added complication. Finally, the third method requires more estimation periods and more stability of estimates through time to be meaningful.
5.7 CONCLUSION
This chapter introduced the aggregate Z-score model of stock selection. We began by discussing the concept of sequential stock screening because it is one of the simplest quantitative methods of picking stocks and easy for most investors to understand. We also discussed some of the investing styles of famous portfolio managers and translated their approaches into sequential stock screens.
While sequential stock screening is a very useful starting point, it is not as efficient or as commonplace in the portfolio management world as multifactor simultaneous stock screening. Using what we call the aggregate Z-score model, we showed how to standardize or normalize all stock return factors in order to perform multifactor simultaneous stock screening. We focused on Z-score standardization across stocks in the entire universe but also discussed the fact that some portfolio managers might choose to standardize the Z-scores by industry or sector and then select representative samples of stocks from each industry or sector. Finally, we introduced the concept of factor groups as a means of further structuring and clarifying the screening process.
The aggregate Z-score model is helpful in its simplicity, but it has the drawback of ranking stocks relatively instead of directly estimating the stocks’ expected returns or
α
’s. The portfolio man
ager who does not manage against a benchmark does not need to worry about this because he or she simply can pick the stocks that are most attractive and weight them using any of a variety of methods (e.g., equal weighting the 100 top-ranked stocks). However, for a portfolio manager who manages against a specific benchmark (e.g., the S&P 500), it is necessary to know the expected returns in order to perform a risk optimization versus the benchmark. We have suggested some ways to convert the aggregate Z-scores into the stocks’ expected returns or
α
’s. The last step in the portfolio process for portfolio managers who use the aggregate Z-score model is to combine the model with a risk optimizer and create the portfolio of stocks with stock weights.
Stock screening can serve as the basis for a model of stock returns, but in QEPM it is usually just a preliminary step in creating the portfolio. In the next chapters we delve into the core of QEPM, which is the factor model. We introduced factor models in
Chapter 3
. Now that we are familiar with the various kinds of factors at our disposal, some methods for choosing them, and the option of screening the investment universe, we are ready to take a closer look at how to gather factors into a quantitative model of stock returns. We look first at the fundamental factor model in
Chapter 6
and then at the economic factor model in
Chapter 7
.
1
The investment universe corresponds to the set of stocks that a portfolio manager is allowed to trade in his or her portfolio. For example, a portfolio manager who manages against the Standard & Poor’s (S&P) 500 benchmark might only be allowed to purchase the 500 stocks in the S&P 500. His or her
investment universe
would be the 500 stocks that make up the S&P 500. Other managers’ investment universes might follow other indices, such as the Russell 1000, or more complicated definitions.
2
Oftentimes, it is useful to use one version of a factor over another. For example, in
Chapter 4
, we used the price-to-book (P/B) and price-to-earnings ratio (P/E) because they are familiar to most people. However, we find that using the E/P ratio is more effective. Many companies have negative earnings, which renders a P/E ratio meaningless: it makes no sense to argue that a low P/E ratio company is “cheaper” than a high P/E ratio company when companies with zero or negative earnings are included. However, if we calculate the E/P ratio of companies, we don’t have to exclude companies with negative earnings. For example, a company with a very high P/E ratio will have a very small E/P ratio but will still be considered relatively “cheaper” than a company with a negative E/P ratio. The E/P ratio thus gives us a ratio that can be compared across many more companies. Another reason for using the E/P ratio rather than the P/E ratio is that a company’s earnings for a particular period could be close to zero. This leads to an enormous value of P/E that isn’t really representative of the company. Using the E/P ratio resolves this problem. As with P/E, it is more effective to use the inverse of the P/B ratio, the B/P ratio. In the rest of this book, we shall use both B/P and E/P rather than the more common ratios. In the Practical Application part of this book, Part V, we will use the inverse of many other common ratios for the exact same reason.
3
Some people argue that the first screens should be the ones that eliminate the most data possible, but we do not agree.
4
These correspond to P/B ratios of 0.72 and 1.11, respectively.
5
Our descriptions of these famous portfolio managers and professors and our interpretations of their approaches in the form of quantitative stock screens are based partly on our readings of books written by the managers and on information supplied by the American Association of Individual Investors (AAII). The stock screens we present may not be the actual methods by which these managers select equities. The managers have in no way endorsed the stock screens that we present here.
6
Templeton died in 2008. Prior to that, he requested that a large part of his portfolio be placed in a short strategy, since he was convinced that there was trouble in the markets. In fact, he turned out to be correct, although he died before seeing the entire realization of his prediction.
7
A low price relative to expected earnings in three to five years is also used as a forward-looking measure of value.
8
This term originates from the idea of converting any normal distribution to a standard normal distribution. The new variable created by adjusting the raw data to a standard normal distribution is traditionally called a Z-
score
. The concept of aggregating Z-scores of different variables is loosely linked to the Altman Z-score due to Edward Altman’s original model to try to predict stocks that would go bankrupt. The use of the Z-score in QEPM, however, is very different from the use originally proposed by Altman (1968). In Altman’s original work, he used a concept known as
multiple discriminant analysis
(MDA) to aggregate financial ratios that would help to predict whether a firm would go bankrupt or not. The weights of the financial ratios were chosen through the statistical optimization of past data. A final Z-score would result for each stock. There was usually a cutoff value below which a stock would be predicted to go bankrupt. Our analysis is slightly different from Altman’s, but the growth of these type of models in QEPM is most attributable to his original work.
9
The corresponding P/B ratios would be 2.795 for the average and 2.635 for the standard deviation of P/B (just the inverse of the numbers listed in the text).
Table 5.2
shows the values for other representative factors for the S&P 500. The numbers for both E/P and B/P may be different than expected for several reasons. First, we are using the inverse of the common ratios. Second, and most important, we are using equal-weighted averages of stocks in the S&P 500 for the Z-score, whereas most published metrics for the S&P 500 are market-capitalization weighted. Third, some published indices eliminate negative P/E or P/B stocks and just average the remaining stocks—or they average the values substituting a value of zero for negative P/E or P/B stocks. Fourth, our data avoid look-ahead bias, since we use the most recent market value of a company and the book or earnings of three months prior, rather than the coincidental values. Fifth, our S&P 500 universe does not include REIT stocks or any stocks that do not have a CRSP share code of 10, 11, or 12. The reason for excluding REITs is that most quant models would not apply to REIT securities. It should be noted that none of these issues alter the basic composition of our S&P 500 universe. Using this S&P 500 universe, we divide the S&P 500 total market value by total earnings or total book value, which results in a P/B of 4.20 and a P/E of 36.82—figures closer to what is more familiar.
10
Standardizing or normalizing the factor values is based on the idea of converting a normal distribution to the standard normal distribution for analysis purposes. The reader can refer to any basic statistics book such as DeGroot (1986). The Z-score concept still works even if the underlying cross-sectional factor distribution is not normal. The Z-score still gives a sense of how far a variable is from the mean of the distribution. If it turns out that the factor distribution is normal, it simply means that you can make statements about the probabilities of factor Z-scores.
11
The portfolio manager could use the P/B ratio to calculate the Z-scores, but he or she would need to remember to multiply all the Z-score values by −1 so that high Z-scores represented good stocks.
12
Some portfolio managers who wish to have industry neutrality or believe that their factors are very industry sensitive will create Z-scores for each stock relative to its industry average. They will rank each stock within its industry rather than within the entire investment universe and for the portfolio select the best stocks within each industry.
13
Most computer programs and software packages compute the mean very easily. The typical formula is
, where
N
equals the number of stocks in the universe, and
β
i,k
represents the factor exposure
k
for stock
i
.
14
Most computer programs and software packages compute the standard deviation very easily. The typical formula is
, where
N
equals the number of stocks in the universe, and
β
i,k
represents the factor exposure
k
for stock
i
.
15
An outlier is an observation in a distribution that is very far from the mean and has an extremely small probability of occurring. An outlier looks inconsistent with the rest of the data.
16
The phenomenon of data snooping, which we discussed in
Chapter 2
, involves picking factors solely based on past reports of their usefulness without any statistical evidence that they continue to relate significantly to stock returns.
17
For those unfamiliar with this process, it is discussed in more detail in
Chapter 15
.
18
The researcher should be very careful to avoid look-ahead bias, which is sometimes a problem when a portfolio manager uses historical factor data. The data set may contain a factor value for a certain month, but in that month, that piece of data would not have been available. By using data that the market did not have in that month, the quantitative portfolio manager has “looked ahead,” potentially causing the model to estimate parameters incorrectly. A typical solution to look-ahead bias is to know the delivery lag of all factors that one is using and place a lag on the factor. For example, if you’re using a factor that relates to March but is only reported in April, you may wish to use the
t
− 1 value of that factor in any historical estimations. This is discussed in more detail in
Chapter 16
.
19
When we typically estimate these factor models, we use information at time
t
to predict returns at time
t
− 1 or similarly use information at time
t
− 1 to predict returns at time
t
. Sometimes, in this book, for convenience, we write the equation with time subscript
t
everywhere and sometimes we explicitly write the expressions with factor exposure
t
− 1 and returns of time
t
. In all cases, the reader should understand that we are using information at
t
to predict returns at time
t
− 1. In other words, the factor exposure at time
t
− 1 is the exposure value as of the end of period
t
− 1, which we may refer to sometimes as the beginning of month exposure for time
t
.
20
This regression also tells us how Z-scores are related to stock returns. In some cases, like when dealing with returns accounting for transactions costs, it is beneficial to convert Z-scores to returns. In
Appendix 5C
we suggest a crude way to do this.
21
Using the natural log of market capitalization might also be uncomfortable to some. In order to get the more standard market capitalization, just take the exponential of the value. For example, for Apple, exp (14.6251) = $2,255,991 million or $2.25 trillion.
21
For some procedures related to common tests for structural change, see Chow (1960), Toyoda (1974), Schmidt and Sickles (1977), Toyoda and Ohtani (1986), Ploberger et al. (1989), Banerjee et al. (1992), Stock (1994), Chu et al. (1995), and Hoyo and Llorente (1997). Some of these papers are also useful for parameter stability tests discussed earlier in the book.
22
These acronyms for factors can be found in Abbreviations of Factor Names at the beginning of the book or in
Appendix 16A
.
23
Of course, alternative weighting schemes could be used.
24
If a single-period cross-sectional regression were used instead of a panel series regression, then there would not be a
γ
for each stock; thus
γ
i
would be replaced by
γ
.
25
Panel regressions consist of using a time series of cross-sectional data to estimate the coefficients.
26
This concept was popularized by Richard Grinold (1989). Significant research discussing and expanding our understanding of this law has been done since it was proposed [see Bolshakov and Chincarini (2020), Buckle (2004), Chincarini and Kim (2007), Clarke et al. (2002), Ding and Martin (2017), Hallerbach (2014), Van Loon (2018), Ye (2008), and Zhou (2008a, 2008b)].
27
Because
E
(
z
t
−1
) is zero and
S
(
z
t
−1
) = 1, we can achieve the second to last part of the derivation. This is so because the Z-score is already normalized.
28
The equation we present here differs from Grinold and Kahn’s original description because they use actual signals or raw forecasts prior to normalizing the variables. The actual regression of the returns on the raw signals or factors creates this equation where by definition the raw forecasts are normalized. This is why regressions are convenient: You don’t have to normalize prior to estimating them. They normalize for you. It is therefore difficult to see the magic in this formula.
29
Common commercial software platforms include Factset, FTSE BIRR, MSCI Barra, Northfield, and Qontigo’s Axioma. For more details, see Appendix D at
www.ludwigbc.com
under QEPM Exclusive Content. In
Chapter 9
we show how a quantitative portfolio manager can build his or her own portfolio optimization models.
30
If the factor distribution were truly normal, then 68% of the stocks would fall into this area.
31
The process of portfolio optimization is discussed in significant detail in
Chapter 9
.
32
There are several ways to estimate this equation. For example, one could use a set of data to estimate the factor exposures,
, to factor premiums (or benchmark returns) of each stock. In the next sequential period of data, given the stock returns and realized factor premiums (or benchmark returns), the residual returns are regressed against Z-scores to obtain the relationship between Z-score and residual returns.
33
We discussed this issue in
Chapter 3
. Also see Chincarini and Kim (2007).
