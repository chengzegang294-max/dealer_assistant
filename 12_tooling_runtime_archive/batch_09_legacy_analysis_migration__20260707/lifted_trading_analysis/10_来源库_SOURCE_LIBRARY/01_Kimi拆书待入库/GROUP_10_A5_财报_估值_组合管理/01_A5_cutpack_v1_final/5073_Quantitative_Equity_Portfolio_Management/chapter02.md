# Quantitative Equity Portfolio Management: An Active Approach to Portfolio Construction and Management, Second Edition

- **book_name**: 5073 Quantitative Equity Portfolio Management, Second Ed.
- **main_source**: epub
- **cross_check_source**: none
- **pdf_role**: not_needed
- **split_scope**: chapter file = chapter02

---

CHAPTER 2
The Fundamentals of QEPM
Some people recognize beauty before others have recognized it, some people see beauty that no one else can see, and some people see no beauty
.
2.1 INTRODUCTION
Quantitative equity portfolio managers cannot simply go through the motions of quantitative analysis. Implementing quantitative equity portfolio management (QEPM) the right way requires a firm grasp of the underlying concepts that make the analysis work. Since quantitative equity portfolio managers generally aim to outperform a benchmark or index, we start our conceptual discussion with alpha (
α
), the measurement of a portfolio’s risk-adjusted returns over and above a reference instrument. There are a number of variations of alpha, but no matter what type of alpha a manager strives for, his or her work should be guided by the seven tenets of QEPM. The seven tenets encompass ideas necessary to the very existence of QEPM. One of these essential ideas is that financial markets do not operate entirely efficiently. Neither QEPM nor any other form of active management would succeed in a perfectly efficient market. We examine the evidence for market inefficiency, which is found mainly in studies of market anomalies, and we explore possible explanations for these anomalies. The seven tenets of QEPM also lay
down important principles for the practice of QEPM, including the efficient use of information in quantitative models. We discuss the popular but frequently misinterpreted fundamental law of active management as an important framework for understanding and achieving efficiency. Finally, the seven tenets demand the consideration of statistical issues that have direct bearing on the statistics-intensive methods of QEPM. We reflect on these issues, which include data mining, parameter instability, and parameter uncertainty, at the end of the chapter.
2.2 QEPM
α
The word
alpha
is constantly bandied about in the world of active portfolio management. Active managers use the term in many contexts, and sometimes it is not clear exactly what they are referring to when they use it. The simplest, colloquial meaning of
α
is outperformance. You might hear a portfolio manager say, “I’m trying to generate positive
α
.” He or she probably means that he or she wants the portfolio to outperform some other instrument. In general,
α
represents the excess return of the portfolio over the return of a reference instrument. There are different ways to define
excess performance
, though. In QEPM,
α
is a measure of the
risk-adjusted
excess return, which is the portfolio’s performance after accounting for its risk relative to the reference instrument. Increasing the
α
therefore means increasing the portfolio’s return without increasing its direct exposure risk to the reference instrument. When the reference instrument is the portfolio manager’s benchmark, we will refer to
α
as the
benchmark α
or
α
B
.
1
When the reference instrument is a series of multifactor benchmarks, we will refer to
α
as
multifactor α
or
α
MF
. When the reference instrument is the market portfolio, we will refer to
α
as the
CAPM α
or
α
CAPM
.
2
Given the returns of the reference instrument, it is possible to use statistical techniques to decompose the portfolio’s return into two parts—one that is related to the reference instrument and one
that is not. The related part is typically called
expected return
or
consensus return
, and the second part is known as
residual return
or
the return not explained by the model
. For each of the three types of
α
, there is a slightly different method for separating these two components of the portfolio’s return.
2.2.1 Benchmark
α
Given the portfolio return
r
P
and the benchmark return
r
B
, we can estimate the following equation
3
:
In this equation,
βr
B
is the expected or consensus return, which is the part of the portfolio’s return related to the benchmark. The remaining
α
+
ϵ
is the residual return.
4
The residual return is all that matters to the quantitative portfolio manager, because his or her goal is to increase the risk-adjusted return. If the benchmark return is positive, it is easy enough to generate higher returns simply by increasing the portfolio’s exposure to the benchmark, but the portfolio manager has not added value. The part of the portfolio return that represents an increase in return independent of increased direct benchmark exposure is the residual return. Benchmark
α
is the expected value of the residual return, and the second component of the residual return,
ϵ
, is the deviation of the residual return from its mean.
Equation (2.1)
is constructed so that
ϵ
averages zero. The benchmark
α
, also known as
α
B
, therefore has special significance: It is the risk-adjusted excess return over the benchmark.
2.2.2 CAPM
α
Given the portfolio return
r
P
and the market return
r
M
, we can estimate the following equation:
In this equation,
βr
M
is the expected or consensus return, which is the part of the portfolio’s return related to the market. The remaining
α
+
ϵ
is the residual return.
The reader will notice that this version of
α
is very similar to the one created using the benchmark return. In fact, since the market return is typically the Standard and Poor’s (S&P) 500 return, if the benchmark is the S&P 500, then those two measures of
α
are the same. In this equation, however,
α
is called the
CAPM α
because this decomposition of a portfolio’s returns follows from the capital asset pricing model (CAPM).
5
The equation says that the returns of all portfolios are related to the market portfolio. According to CAPM theory, the CAPM
α
should equal zero. When it is significantly positive, the portfolio manager is providing excess risk-adjusted returns. The CAPM
α
, or
α
CAPM
, is the risk-adjusted excess return over the market.
2.2.3 Multifactor
α
Given the portfolio return
r
P
and a series of factor returns
f
1
, … ,
f
K
, we can estimate the following equation:
where
β
1
f
1
+ … +
β
K
f
K
is the expected or consensus return from a multifactor model of stock returns (i.e., the part of the portfolio’s return related to the underlying risk factors in the economy). The remaining
α
+
ϵ
is the residual return, as before.
Note that this version of
α
is created using a model with many factors that influence stock returns. There will be more discussion of this framework in subsequent chapters. The
α
in this model is called the
multifactor α
, or
a
MF
, and it is a measurement of risk-adjusted excess return given multiple explanatory variables.
2.2.4 A Variety of
α
’s
The
α
’s in
Eqs. (2.1)
,
(2.2)
, and
(2.3)
are interrelated. In special cases, they are equivalent to each other.
1.
The multifactor
α
of a stock or a portfolio is the same as the CAPM
α
if the market return is the only factor in the model.
2.
The benchmark
α
of a stock or a portfolio is the same as the CAPM
α
if the market portfolio is the benchmark.
3.
The multifactor
α
and the benchmark
α
of a stock or portfolio are the same if the market return is the only factor in the model and is also the benchmark.
In other cases, the three
α
’s are not equivalent. Suppose that the manager uses an inefficient benchmark, which is evidenced by the fact that the
α
of the benchmark against the market return is negative. As a result, the benchmark
α
of the portfolio will be higher than the market
α
of the portfolio. To use our notation,
α
B
>
α
CAPM
. Using an inefficient benchmark therefore will make the portfolio’s performance look better than it would if it were measured against the entire market.
6
Many practitioners and academics may ask whether or not positive benchmark
α
is consistent with the arbitrage pricing theory (APT).
7
In fact, the answer is yes. Although it is practically difficult to test the APT because the theory does not specify the underlying factors of security returns, let’s assume for a moment that we know the true factors of stock returns. Suppose that the portfolio’s return is determined according to APT and can be expressed as
Let us also suppose that the first factor,
f
1
, is the benchmark (e.g., S&P 500). What would the benchmark
α
be in this case? Could it be positive?
Recall that the benchmark
α
is the part of the average return that is not related to the benchmark. If all the other factors in the APT model are uncorrelated with the first factor (the benchmark), then the benchmark
α
is given by
The benchmark
α
includes the effect of all the other factors. Thus it is quite likely that the benchmark
α
is positive. In general, if we allow the benchmark to be correlated with all other factors, the benchmark
α
is given by
where
γ
j
is the coefficient in the regression of
f
j
on
f
1
[i.e.,
C
(
f
1
,
f
j
)/
V
(
f
1
)]. While the formula is somewhat more complicated, the conclusion is the same. The benchmark
α
includes the effect of all factors aside from the benchmark, so it is very possible that the benchmark
α
is positive.
This analysis shows that when measuring the performance of a manager with benchmark
α
, benchmark
α
can be positive even if multifactor
α
equals zero. Although multifactor
α
equals zero, benchmark
α
still can be positive if the portfolio manager loads his or her portfolio with positive exposures to factors that have positive premiums according to the APT. A positive benchmark
α
therefore is consistent with the APT model, in which managers are rewarded for statistical arbitrages.
2.2.5 Ex-Ante and Ex-Post
α
Whichever type of
α
we use, there is usually a difference between the value we expect it to reach in the future and the value that it ultimately realizes. The
ex-ante α
is the expected
α
, whereas the
ex-post α
is the realized one. The ex-ante
α
is of interest to the quantitative portfolio manager when he or she is constructing his or her portfolio. Clearly, he or she sets out trying to achieve the highest possible
α
when he or she builds the portfolio subject to the portfolio constraints. Once the portfolio has been active for some period of time, the ex-post
α
shows whether the actual risk-adjusted performance lived up to expectations. The manager’s bonus is based on the ex-post
α
.
8
The best a manager can realistically hope for is that the ex-post and ex-ante
α
’s will be highly correlated.
2.2.6 Ex-Ante and Ex-Post Information Ratio
Though
α
by itself is the primary measure of a portfolio’s excess return, there is also a key metric, the
information ratio
, that adjusts
α
for the portfolio’s residual risk. As with
α
, there are ex-ante and ex-post information ratios. We will discuss only the ex-ante information ratio at this stage because the ex-post information ratio is discussed in detail in
Chapter 15
on performance measurement. The information ratio is directly related to the benchmark
α, α
B
. The ex-ante information ratio (
IR
) is given by
where
α
B
is the expected or predicted
α
of the portfolio manager, and
ω
is the predicted standard deviation of the residual [i.e.,
S
(
ϵ
)]. The ex-ante information ratio measures the expected excess return over the benchmark per unit of excess risk over the benchmark. The higher the ex-ante information ratio, the better we expect the portfolio to perform. All else equal, a higher forecasted ratio is better.
2.3 THE SEVEN TENETS OF QEPM
A quantitative equity portfolio manager aims for the twin goalposts of a high alpha and a high information ratio, and getting there requires knowing the rules of the game. QEPM is organized around certain principles. We call these principles the
seven tenets of QEPM
.
Tenet 1:   Markets are mostly efficient
.
Tenet 2:   Pure arbitrage opportunities do not exist
.
Tenet 3:   Quantitative analysis creates statistical arbitrage opportunities
.
Tenet 4:   Quantitative analysis combines all the available information in an efficient way
.
Tenet 5:   Quantitative models should be based on sound economic theories
.
Tenet 6:   Quantitative models should reflect persistent and stable patterns
.
Tenet 7:   Deviations of a portfolio from the benchmark are justified only if the uncertainty is small enough
.
Tenets 1 and 2 set boundaries on QEPM’s reach. Markets are mostly efficient, which means that it is not possible to make profits without taking risk. Risk-free opportunities, or pure arbitrage
opportunities, do not exist. Still, the markets are not perfectly efficient. There is room to make profits by taking relatively small amounts of additional risk. QEPM is the process of searching for such “statistical arbitrage opportunities,” as stated in tenet 3. Statistical arbitrage opportunities exist because stock prices do not always properly reflect all the available information. QEPM provides statistical methods for identifying information that the market has overlooked. As tenet 4 says, the quantitative manager must combine all the available information into an efficient model in order to identify the pieces that are key to earning higher returns.
Tenets 5, 6, and 7 establish standards for applying econometric techniques to choices involving the portfolio. Tenet 5 is absolutely fundamental to creating quantitative models of stock returns. All models used to pick stocks should be based on sound economic theory. Data mining violates this tenet. Factors dredged up from the data through data mining may seem to relate to stock returns on their surface, but they are unlikely to reveal real opportunities for statistical arbitrage. The manager has to have a good reason for choosing each factor that he or she includes in the model. There should be reason to believe that stock prices do not yet, but eventually will, reflect the information contained in each factor or in the group of factors as combined in the model. The model is not meaningful without a strong theoretical underpinning.
Likewise, the relationship between the factors and stock returns needs to be one that holds up over time. As tenet 6 says, the model should only make use of data patterns that are persistent and stable. Parameter stability is essential to the generation of precise estimates and reliable forecasts with the model.
Tenet 7 cautions that QEPM does not always involve differentiating the portfolio from the benchmark. Many quantitative portfolio managers mistakenly believe that deviations from the benchmark are necessary in QEPM. In fact, a deviation from the benchmark portfolio is justified only if the portfolio’s estimation error (a measure of uncertainty) is small enough. Quantitative managers always should take parameter uncertainty into account before steering the portfolio away from the benchmark onto another path dictated by the model.
9
In the following sections we discuss the seven tenets of QEPM in greater detail. We start with the concept of market efficiency and its implications for QEPM. Then we discuss how to use information efficiently, adopting the framework of the fundamental law of active management. Finally, we examine issues arising from the application of econometric techniques to QEPM.
2.4 TENETS 1 AND 2: MARKET EFFICIENCY AND QEPM
Tenets 1 and 2 of QEPM are based on the belief that markets are mostly, but not completely, efficient. If markets were completely efficient, QEPM would be a futile exercise. An active portfolio manager has to believe that there are inefficiencies in the market that he or she can exploit. In this section we discuss what it means for the market to be efficient and what the evidence is for some degree of market inefficiency.
2.4.1 The Efficient-Market Hypothesis
There are those who say that financial markets are efficient and those who say they are not, but what are people really talking about? In general terms, an efficient market is a market in which all information is reflected in current stock prices. For instance, in an efficient market, an investor could not earn excess returns by buying a stock on a tip that the company has a new CEO who is expected to improve operations. The price of the stock already would reflect this news and any other relevant information. In a perfectly efficient market, investors cannot earn excess returns without bearing extra risk, and portfolio managers, therefore, cannot create
α
.
10
In an efficient market, stock prices move randomly. If we looked at the historical prices of any stock in an efficient market, the
day-to-day changes would show no discernible pattern. When stock prices do move in some predetermined fashion, then presumably an investor can make money by trading around the pattern, which means that there is an inefficiency in the market.
Not even
near-arbitrage
opportunities exist in a perfectly efficient market. For example, if a publicly traded company traded at a price of $100, a subsidiary in which it owned a 95% stake could not trade at $200. If it did, an investor could buy the main company’s stock at $100 per share and short sell the subsidiary’s stock at $200 per share, making a profit when the two prices eventually aligned. When PALM was spun off from 3COM on March 1, 2000, the two companies’ stock prices displayed a similar imbalance, leading some to seriously doubt the efficiency of the stock market.
Asset bubbles are also signs of inefficient markets. In early 2000, the NASDAQ was overvalued by almost any measure of valuation. Internet startups traded at market capitalizations many multiples of the market caps of established brick-and-mortar companies in similar lines of business. From March 2000 to January 2003, however, the NASDAQ fell by 71%. A $100 million portfolio invested in the new technology revolution in 2000 would have been reduced to a mere $29 million in less than three years. The internet bubble was a huge, unsustainable deviation from market efficiency.
Perhaps one of the greatest dislocations of prices from fundamentals occurred during the housing bubble of 2008, also known as the Great Recession. In the period from 2003 to 2008, easy liquidity and lack of accountability caused housing prices and the stock market to soar. In 2008, the housing market came crashing down along with the stock market. The S&P 500 declined by 38% in 2008, and the national housing price index declined by 11.88%, with some cities experiencing even larger declines in housing prices. This perplexing inefficiency may have been caused by an immensely crowded investment space and pointed to the potential inefficiencies of markets.
11
In the 1970s, Eugene Fama, a professor at the University of Chicago, decided to establish testable criteria for market efficiency. Fama recognized that the market’s level of efficiency has to do with the degree to which security prices reflect information relevant to the investment decision. The nature of investment-relevant information is a continuum that spans from the most obvious public
information to the most private insider information. In Fama’s criteria, market efficiency is directly related to how much of the continuum is incorporated in market prices.
Fama described three increasing levels of efficiency—
weak form, semistrong form
, and
strong form
—at which market prices reflect increasingly more of the information continuum. (
Table 2.1
provides a quick overview of the three definitions of efficiency.) At the lowest level of efficiency, weak-form efficiency,
security prices reflect the information available in previous security prices
. This means that past prices of stocks give an investor no actionable information. For portfolio managers, it means that
technical analysis
does not work.
TABLE 2.1
Definitions of Market Efficiency
Technical analysis is popular with many investors, especially traders. A classic text written by John Murphy defines technical analysis as the study of market action through the application of charts and/or statistical techniques to forecast future price trends.
12
Whereas the fundamental analyst looks for the causes of market movements in the form of economic or operating data, the technical analyst is more concerned with patterns in the market movements themselves. Technicians look for patterns in data directly obtainable from securities, such as past prices, volume, and open interest. Like fundamental analysts, technicians believe that prices
adjust slowly to their proper levels when new information reaches the marketplace because not all investors have equal access to information. The time it takes for information to percolate through the hierarchy of professional traders down to the general investing public creates a window of opportunity for technicians to trade on the patterns that they have identified in the data.
One of the simplest patterns identified by technicians is
momentum
. The idea is that if a stock had a positive return in the period prior to this one (e.g., last week), then there is a good chance that the stock will have a positive return in the subsequent period (e.g., this week). If this pattern holds, the market is not weak-form efficient because past prices, which indicate the past returns, help you to invest for the future. In a weak-form efficient market, current prices incorporate all the information contained in past prices.
The next level of efficiency covers more of the public-to-private continuum of information. In the semistrong form of market efficiency,
security prices reflect all information that is publicly available
. This means that quantitative portfolio managers and other investors cannot use any publicly available information to pick stocks and earn risk-adjusted excess returns. Semistrong-form efficiency is bad news for QEPM. Most quantitative portfolio managers use some form of macroeconomic or fundamental data to choose superior stocks. If markets were semistrong efficient, these methods would not work. For example, some portfolio managers buy stocks with low price-to-book (P/B) ratios on the belief that such stocks are probably undervalued. This would not work in a semistrong-form efficient market because P/B ratios are public information, so stock prices already would correctly reflect low P/B ratios. Active management succeeds only by finding niches of the market that are not semistrong-form efficient, perhaps owing to the slow diffusion of information, or by developing proprietary investment strategies, which become themselves nonpublic information. In the semistrong form of efficiency, market prices do not incorporate nonpublic information.
At the highest level of market efficiency, strong-form efficiency,
security prices reflect all information that is publicly or privately held
. In a strong-form efficient market, even private information gives an investor no consistent advantage in picking stocks that will outperform the rest. Strong-form efficiency is the hardest form of efficiency to test because testing requires a precise definition of private information, yet the boundary between public and private information fluctuates. Many years ago (November 4, 1998), the Bureau
of Labor Statistics (BLS) accidentally posted its weekly unemployment report on its Web site two days before the report was supposed to be published. Some investors found the number, acted on it, and made abnormal profits. Since no one expected the report to be released until two days later, what was supposed to be released as public information ended up available ahead of time to a small group of lucky, or particularly diligent, investors. Private information often transforms into public information, but as the bureau’s slip-up demonstrates, information also can pass from the private domain into an in-between space not universally accessible. The law does at least draw one bright line between public and private by prohibiting trading on
inside information
. Company insiders and those who receive information from them are not allowed to take advantage of privileged knowledge. If the law is effective in barring people from trading on this sort of private information, then the market cannot be strong-form efficient.
The entire premise of active management, including QEPM, is that there are market inefficiencies prevalent and predictable enough to exploit consistently for high returns. Semistrong-form efficiency and strong-form efficiency would make active management nearly impossible. After all, a portfolio manager cannot depend on fluke opportunities such as the BLS’s early unemployment data release, much less on illegal insider stock tips. The fact that some active managers consistently outperform the market or a benchmark is enough to convince some people that the market is not wholly efficient. More rigorous evidence against strong-form and even semistrong-form efficiency comes from researchers who have documented signs of inefficiency in market prices.
2.4.2 Anomalies
Investment professionals and academics have observed patterns in historical financial data that contradict the theory of efficient markets.
13
Table 2.2
lists some of these so-called anomalies, along with references to studies on each of them.
TABLE 2.2
Well-Known Anomalies
Anomalies pose a significant challenge to the theory that markets are perfectly efficient. Proponents of efficiency might dismiss certain price irregularities as one-time aberrations in a generally efficient market. Anomalies cannot be dismissed so easily because they are patterns of recurrent irregularities. An anomaly suggests that investors habitually fail to consider and correctly interpret all the information relevant to the investment decision, or that institutional barriers prevent them from acting on certain information, or that, even with all the relevant information staring them in the face, they persist in making irrational choices. There are anomalies that contradict each definition of market efficiency from weak form to strong form.
Weak-Form Anomalies
Typical tests of weak-form market efficiency try to determine whether past prices can be used to predict future prices of individual stocks. For example, researchers may test whether there is significant autocorrelation in a stock’s returns.
Autocorrelation
is the statistical term for correlation between returns from period to period. If stock returns are positively autocorrelated over time, a positive return in one period suggests a positive return in the next. An investor could profit from this pattern, which technical analysts call
momentum
, by buying stocks that performed well in the last period.
Researchers have found that there is autocorrelation in stock indices over a daily, weekly, and monthly horizon. One study found that between July 1962 and December 1994, the autocorrelation in a certain stock index was about 35%. Individual securities exhibited a slightly negative autocorrelation, but this autocorrelation was economically and statistically insignificant.
14
Other studies found significant positive autocorrelation in quarterly stock returns over horizons of less than one year.
15
However, for horizons of one week or one month, individual monthly stock returns seem to be negatively autocorrelated.
16
There is also evidence that industry returns may exhibit positive autocorrelation.
17
There is mixed evidence on other technical indicators. Traders believe that they work, but tests of technical rules do not clearly confirm that belief. The standards for testing technical rules have
been inconsistent. Many practitioners fail to include transactions costs in their tests, making excess returns appear greater than they actually would have been. Tests are also usually done on closing prices, which may be the best and most complete data available but are not necessarily the prices at which trades would have been placed. In general, tests cannot easily replicate a trader’s discretion in applying technical strategies. A trader might have thought that a technical rule applied during one period but not during another. Technical trading is also not necessarily comparable with portfolio management. Some trading rules might work on intraday data, but they will not serve as portfolio strategies, which are supposed to work for months or years. Taking these limitations into account, the results of the tests of technical rules tend to fall on the side of weak-form efficiency because most technical rules do not seem to work consistently over time.
Semistrong-Form Anomalies
If technical data fail to provide reliable investment strategies, what about other publicly available information? There is a host of anomalies that provide evidence that market prices do not reflect all public information and that therefore the market is not semistrong-form efficient.
One well-known anomaly is the
earnings surprise anomaly
. Stocks that report higher-than-expected earnings tend to have excess risk-adjusted returns in the weeks following the announcement. What do we mean by
higher-than-expected earnings
? Wall Street stock analysts typically forecast the earnings they expect a company to report each quarter. The average of all analysts’ earnings forecasts is known as the
consensus estimate
of earnings for that company. When a company’s earnings clear the hurdle of the consensus estimate, they are higher than expected. The earnings surprise anomaly violates semistrong-form efficiency because some stocks continue to earn excess returns for weeks after earnings are reported to the public. A semistrong-form efficient market would incorporate the earnings report into the stock price immediately, but the real market responds more slowly. Studies show that stocks actually provide excess returns for 13 to 26 weeks after positive earnings surprises.
Another old and well-known anomaly is the
January effect
.
18
Small-cap stocks and the previous year’s poor performers tend to
do very well in January, especially in the first week. There are some logistical reasons for this phenomenon. One is that tax-loss harvesting by institutional and private investors involves selling poorly performing stocks in December to generate capital losses that offset capital gains and, to a lesser extent, income taxes.
19
The December sell-off depresses those stocks to prices below their actual nontax values, so investors might repurchase them once the new year rolls around.
20
The January effect is stronger when more investors engage in this tax-sensitive strategy.
Aside from tax harvesting, mutual fund managers also sell losing stocks at year end before they report their holdings to the Securities and Exchange Commission (SEC), in compliance with the required quarterly reporting. By selling a loser stock, the mutual fund manager does not have to report it as a holding and be scrutinized by investors who notice it on the SEC report. This tactic is known as
window dressing
. In the SEC report, investors will be able to see a mutual fund’s overall low return, but window dressing prevents them from seeing each of the manager’s bad picks.
It is also possible that the January effect occurs because many mutual fund managers “bet the house” early in the year. The annual bonus system at most funds might give managers an incentive to take big risks in January. They might think that if they lock in good returns at the beginning of the year, they will have gained a head start toward their bonuses; at the same time, if they lose a lot early on, they will have the rest of the year to grind their way back to a decent return.
21
Whatever the reasons for January buying, it is interesting to note that it is possible to see the forces of market efficiency at work on this anomaly. The January effect is gradually shifting backward as arbitrageurs and quantitative managers try to take advantage of it by placing trades ahead of time in December.
Other calendar effects exist as well. Mondays and the onset of daylight savings are among the calendar events associated with
trading patterns. The
Monday effect
is that the market tends to drop slightly on Mondays. The
daylight savings effect
is that the market tends to drop slightly on the first trading day after the beginning of daylight savings, supposedly because the disruption of traders’ circadian rhythms increases their aversion to risk.
There are many anomalies associated with fundamental data, which are the data obtained from a firm’s income statements, balance sheets, and cash-flow statements. Several studies have shown that a portfolio of stocks with a low P/B ratio or a low price-to-earnings (P/E) ratio will earn high risk-adjusted returns. If a simple strategy of purchasing stocks based on publicly available P/B or P/E ratios can lead to excess returns, then the market is clearly not semistrong-form efficient. Small-cap stocks also have tended to earn higher risk-adjusted returns than large-cap stocks over long periods, even though large-caps might outperform small-caps in any given time period. Is there any rationale for this behavior? Some people argue that small-cap stocks are actually inherently riskier than large-caps because there is less information on them, and standard measurements of risk do not capture this discrepancy in the amount of available information. Small-cap outperformance may, however, be an instance of the
neglected-firm effect
, in which firms with low analyst coverage or low institutional ownership tend to have higher risk-adjusted returns. Whatever the explanation for it, the fact that small-caps do especially well over the long run seems to imply that the difference between the amount of public information on small-caps and large-caps is a kind of information itself, and this sort of second-degree information is not efficiently factored into stock prices.
In recent years, some new anomalies have been documented and some old anomalies have become in vogue again. In particular, the low volatility and low beta anomalies have become popular again. These anomalies find that stocks with low measured historical volatility outperform stocks with high measured historical volatility. Similarly, stocks with low beta tend to outperform stocks with high beta. More recently, factors regarding liquidity and crowding have surfaced.
Crowding
is a recently identified risk in investing that might occur when multiple market participants begin to follow the same trade in such concentration that liquidity becomes fragile, altering the risk and return dynamics of the trade. Research has found that there are excess returns to purchasing less crowded stocks.
There are many studies that point to additional violations of semistrong-form efficiency (see
Table 2.2
). Some academics still believe that these sorts of anomalies are not a sufficient basis for successful portfolio strategies. Professor Richard Roll of UCLA once wrote that “[i]t’s extremely difficult to profit from the slightest deviation from market efficiency.”
22
Quite a few active managers, however, make a living doing exactly that.
Strong-Form Anomalies
The strong form of market efficiency is probably the hardest kind to believe in because it means that market prices already reflect
all
information, both public and private. It is also hard to test for strong-form efficiency. Some clever tests have been done, though.
One test is known as the
insider-traders test
. Company executives and other insiders have,
ceteris paribus
, a better understanding of a company’s operations and financial health than an outsider does.
23
Executives are required by the SEC to report their own purchases and sales of their companies’ securities. Researchers have obtained these reports and asked the following question: If an outsider purchased a stock when insiders purchased it and sold it when insiders did, would the outsider have earned risk-adjusted excess returns? The answer is oftentimes yes. Insider information is not immediately priced into stocks, as it would be if the market were strong-form efficient.
24
In the past, researchers were able to perform a test of the profits from specialists on the exchange. Stock exchange specialists were supposed to maintain an orderly market and manage their limit-order books. Access to the limit-order book was equivalent to having private information, because it contained the prices at which prospective buyers and sellers were prepared to buy or sell
a stock. One could imagine that a specialist might be able to use this knowledge to his or her advantage, and, indeed, historically, specialist profits have been extraordinary. Was this due to the contrarian nature of their trades, which must balance the order flow, or was it due to the fact that they could make use of private information? If it was the latter, the specialists’ profits of the past were another sign that markets were not strong-form efficient.
25
Behavioral Explanations for the Anomalies
Traditional theories of investor behavior have a difficult time explaining market anomalies. Staunch believers in the efficiency of the market usually argue that any strategies that yield excess returns must be a great deal riskier than other strategies. Another argument for market efficiency is that any statistical arbitrage opportunities that do exist are extremely small, not scalable, fleeting, and very costly to discover.
26
These arguments are hard to reconcile with the many studies that describe long-term strategies that produce risk-adjusted excess returns. The seemingly small eddies of inefficiency in the market sometimes create major opportunities for statistical arbitrage. The risk involved in statistical arbitrage, including the possibility of misjudging how long an anomaly will persist, does not always negate the return. It may be necessary to turn from the CAPM to a multifactor model of stock returns in order to completely understand a less-than-efficient market.
Additional explanations for the existence of anomalies can be found in a field of economics known as
behavioral finance theory
. Researchers cannot fully explain the presence of anomalies with theories that presume that investors behave rationally. Behavioral finance theory attempts to account for anomalies with a study of the effect of psychology and irrational behaviors on investment decisions. Behavioral biases, like the ones listed in
Table 2.3
, contribute to the kind of buying and selling that leads to mispriced securities.
27
TABLE 2.3
Common Behavioral Biases
2.4.3 Market Efficiency and QEPM
Anomalies and behavioral biases give fairly strong evidence that markets may not be much more than weak-form or only sporadically semistrong-form efficient. Summarizing the evidence, here are our top 10 reasons why markets are not perfectly efficient and why active portfolio management such as QEPM is a worthwhile endeavor:
1.
Obtaining information is costly. Not everyone is able or willing to pay for information.
2.
Information, even public information, travels somewhat slowly through the market.
3.
Not every investor has the ability to process a large amount of information, especially quantitative information.
4.
By filtering public information, some people may create what amounts to private information.
5.
Some investors base their investment decisions on sentiment rather than on the logical interpretation of information.
6.
Some attempts to exploit others’ presumed irrationality actually creates more inefficiency.
7.
Economic conditions, especially the state of technology, change all the time, and it takes time for people to adapt to these changes.
8.
Transactions costs create gaps between economic models and reality.
9.
Taxes cause distortions in the markets.
10.
Government regulation of financial markets creates gaps between economic models and reality.
Efficiency means that the market incorporates all relevant information into security prices, and this happens only when all investors have all the information relevant to investment decisions. In reality, investors operate with varying sets of information partly because accessing it is costly. Portfolio managers have access to extensive market databases paid for by their firms. Even with the introduction of low-cost databases tailored for individual investors, the majority of them simply cannot replicate the volume and functionality of commercial databases that contain historical and up-to-the-minute data.
Since people’s access and exposure to information vary, information moves through the market slowly and unevenly. Private information obviously stays within a fairly small radius, but even public information travels slowly and stops before reaching everyone. Many people rarely come in personal contact with the markets, do not keep track of market news, and never receive some information. Also, private information usually becomes public eventually, but often in a delayed and uneven fashion. This is especially the case with bad corporate news, which companies sometimes release in bits and pieces in order to avoid dropping bombs on their own stock prices.
Once information is publicly accessible, quantitative portfolio managers are in the best position to make use of it. They are alerted to news almost immediately via electronic data services, whereas average investors may not learn about it until later from the TV or newspaper headlines. Compared with other professional managers with access to data services, quantitative managers also have a great advantage because they make use of software and quantitative methods that sort through large data areas relatively quickly, and their stock-return models can be updated accordingly. The quantitative model of stock returns will warn the manager in as little time as it takes for the computer to run the program whether any news warrants selling stock.
By filtering public information with quantitative analysis and proprietary models, quantitative portfolio managers gain insights and uncover strategies that are essentially private information derived from public inputs. Since most investors cannot uncover the same things, this information is not yet priced into securities, and there is the potential for statistical arbitrage. Even if a number of portfolio managers use similar models, they still can earn excess returns as long as they are relatively few compared with the entire population of investors.
Investors’ biases also create statistical arbitrage opportunities because they cause mispricings. People inevitably let irrational hopes and fears creep into investment decisions, which causes them to ignore or misjudge certain relevant information. Quantitative equity portfolio managers are in a good position to both avoid and exploit irrational decisions. Quantitative models of stock returns help the manager to take his or her own emotions out of the investment decision while also uncovering irrational price movements that are vulnerable to statistical arbitrage.
Statistical arbitrage usually helps to return security prices to their efficient levels. Sometimes, though, it actually exacerbates market inefficiencies. For example, during the internet bubble of the late 1990s, many stocks were overvalued. Amazon (AMZN) was in the same line of business as Barnes & Noble (BKS), but it traded at a much higher multiple. If someone assumed that the higher multiple was a symptom of a short-lived overvaluation, then one could have gone long BKS and short AMZN. In contrast, if one assumed that the internet bubble was going to get bigger, one could have gone long AMZN and short BKS, thereby compounding the overvaluation.
28
The internet bubble also was a case in which the market did not appreciate or understand a change in economic conditions. Sometimes information is not priced into securities because it is not yet understood or even recognized. It takes time for even the best analysts, economists, and strategists to understand the real significance of changes in the economic environment. During the learning period, markets most likely will not factor the changes into securities prices correctly. During the late 1990s, for instance, investors’ zeal over the prospects of new e-commerce business models outstripped the actual growth potential of many startups.
The process of buying and selling in the market is itself a source of inefficiency. Transactions costs divert money away from its most efficient use. While an economic model may say what prices should be in equilibrium, actual prices may be quite different because of transactions costs. These costs can take the form of
broker commissions, price impact
, and
delay
. Mispricings due to transactions costs may not be exploitable by any investors, or they may be exploitable only by those who can keep their own transactions costs low. For instance, commissions and delays prevent many small investors from trading as frequently as professional traders do and from pursuing strategies of scale that require large funds.
Taxes are another significant cost and source of inefficiency in investing. Investors are ultimately concerned with after-tax returns, so tax consequences weigh on investment decisions. The distribution of investors’ tax rates, as well as any changes in that distribution as a result of changes in the tax laws, affects the relative prices of securities. If even a few large institutions buy or sell stock for tax reasons, prices can shift away from their true nontax values. At times, the price shifts create exploitable market inefficiencies.
Market inefficiencies can be the by-products of other government regulations as well. Some countries with fixed exchange rates have experienced fluctuations in which the exchange rate suddenly dropped by as much as 40% of its value in a matter of hours. The drastic rate corrections have cost foreign investors enormous amounts of money. Clearly, such fixed exchange rates did not price the currencies according to all the information available in the marketplace. Government-imposed systems also create less dramatic distortions. In the case of equities, numerous government regulations alter the flow of investment, including restrictions on short selling, rules related to tick increments (i.e., decimal pricing), and rules related to stock ownership.
29
Although the intent of the regulations is presumably to ensure some public good, they still cause distortions that may be exploited for excess returns.
These are the essential reasons why markets are not perfectly efficient, which is to the benefit of quantitative equity portfolio managers. Why haven’t QEPM managers and other arbitrageurs already eliminated inefficiencies from the market? There are two simple answers to this question. The first is that inefficiencies lead not to pure arbitrage opportunities but rather to statistical arbitrage opportunities that are low but not zero risk (as stated in tenets 2 and 3). The second answer is that there are simply not enough arbitrageurs in the marketplace, with enough investing power relative to the rest of the investing public, to trade away every inefficiency. The markets remain an abundant source of potentially profitable mispricings for the active manager.
2.5 TENETS 3 AND 4: THE FUNDAMENTAL LAW, THE INFORMATION CRITERION, AND QEPM
The portfolio manager has to apply good quantitative analysis to market data to find and exploit the opportunities for excess return that are hidden in market inefficiencies. Tenets 3 and 4 of QEPM state that quantitative analysis opens up the possibility of statistical arbitrage so long as the methods and models that are used combine all the available information efficiently. These two tenets are best illustrated within the framework of the
fundamental law of active management
.
30
The fundamental law has gained popularity among portfolio managers. Through a simple formulation, it shows the portfolio manager’s contribution to the portfolio management process. We know from Section 2.2.6 that a high information ratio is one of the goals of QEPM, and the fundamental law helps us to understand how to achieve it through the application of statistics and the efficient, full use of information.
The fundamental law states that the
information ratio
(
IR
) is the product of the
information coefficient
(
IC
) and the square root of
breadth
(
BR
), that is,
Given the definition of the information ratio in
Eq. (2.7)
,
This equation shows that a higher information ratio can be achieved by increasing the information coefficient or by increasing the breadth. For quantitative managers who build stock-return models, the
IC
can be increased by finding factors that are more significant than the ones already in the model, and the
BR
can be increased by finding more factors that are relatively uncorrelated with the ones already in the model.
The fundamental law was first introduced as a way to gain insights into the quantitative portfolio management process, but its nature and use are sometimes misunderstood. We use the results of standard econometrics to accurately quantify and make clear statements about the components of the law, which will be especially useful to quantitative managers who use linear stock-return models to build their portfolios. We stress, however, that the fundamental
law is for
understanding
QEPM, not for
doing
QEPM. A quantitative portfolio manager does not use the law to actually create portfolios. Rather, the law provides the manager with a useful conceptual framework for analyzing the QEPM process.
2.5.1 The Truth about the Fundamental Law
One of the essential tasks of QEPM is to predict future stock returns by estimating a model that specifies a relationship between the stock return and a list of explanatory variables (a.k.a.
factors
). Suppose that the model specifies that the return of stock
i
at time
t, r
i
t
, is a linear function of the value of
K
factor premiums at time
t
, that is,
f
1
t
, …,
f
Kt
:
where
α
i
, β
i1
, …,
β
iK
are parameters to be estimated, and
ϵ
it
is the random-error term (i.e., the deviation of the stock return from its expected value). Assume that the portfolio manager estimates the preceding equation using data from time 1 to
T
, that is,
t
= 1, … ,
T
.
The fundamental law assesses how well
Eq. (2.10)
explains the stock-return process, and it expresses the equation’s goodness of fit as the product of the
number of explanatory variables
and each variable’s
average contribution
. Depending on what portfolio managers do after estimating
Eq. (2.10)
, the fundamental law may be expressed in different ways, but several truths always hold
31
:
1.
IR
2
approximately equals the goodness of fit (
R
2
) of the return forecasting equations.
32
2.
The breadth is the number of explanatory variables in the return forecasting equations.
33
3.
IC
2
is the average contribution of each explanatory variable in increasing
R
2
.
4.
The fundamental law decomposes the goodness of fit into the number of explanatory variables and their average contribution.
5.
When the benchmark is ignored and the risk-free rate is subtracted from the portfolio returns,
IR
is essentially the maximum Sharpe ratio one can achieve, and the fundamental law decomposes the maximum Sharpe ratio into the number of explanatory variables and their average contribution.
2.5.2 The Information Criterion
One misconception about the fundamental law is that it applies to all active portfolio management.
The fundamental law applies only when the portfolio manager creates the optimal portfolio
. While it may be surprising, many portfolio managers unknowingly create suboptimal portfolios often because they do not use all the available information in the most efficient way (thereby violating tenet 4). When constructing the portfolio, a manager should use all the information gathered from the estimation of
Eq. (2.10)
. This important point has not been emphasized enough by proponents of the fundamental law, so we want to state it as a general principle.
LEMMA 1 (THE INFORMATION CRITERION)
.
The fundamental law of active portfolio management as expressed in
Eq. (2.8)
is valid only if the portfolio manager combines all the available information in the most efficient way
.
An example helps to illustrate the preceding criterion. A portfolio manager may follow the analyst-revision strategy: Construct an equal-weighted portfolio of stocks whose analyst ratings improved in the last month. We can consider “inclusion in the portfolio” a variable. That is, we may define a variable
β
it
that has a value of 1 if stock
i
’s rating improved at time
t
and a value of 0 otherwise. The manager estimates the following equation from historical data:
where
r
i,t
+1
is the return to stock
i
at time
t
+1,
α
and
f
are the parameters to be estimated, and
ϵ
i,t
+1
is the error (the part of the
return that is not explained by the model). If the value of
f
is positive, the equation suggests that those stocks with
β
it
= 1 will have higher future returns. Thus the portfolio manager constructs an equal-weighted portfolio of stocks for which
β
it
= 1, indicating that their ratings improved in the last month.
In doing this, however, the portfolio manager is not using all the available information.
Equation (2.11)
not only says that those stocks with
β
it
= 1 have a higher expected return, but it also identifies which stocks have higher risk (volatility). Stocks with higher volatility should have smaller weights in the eventual portfolio. Since the portfolio manager did not use this piece of information, the information criterion is not satisfied.
We believe that some of the current industry practices do not pass the information criterion. We will encounter such examples in the following chapters, and we will discuss exactly what aspects of the practices violate the information criterion in each case. The bottom line is that if the portfolio construction strategy does not satisfy the information criterion, then there must be a better way to construct the portfolio.
34
2.5.3 Information Loss
The loss that results from not using all information can be quantified easily within the framework of the fundamental law. The fundamental law suggests that the contribution of the portfolio manager (and, by implication, of the information that the portfolio manager uses to increase the portfolio’s return) is summarized by the information ratio. Similarly, the lack of contribution of the portfolio manager is also reflected in the information ratio. By comparing the information ratio that the portfolio manager could have achieved using all available information with the information ratio that he or she actually obtained using only a subset of the available information, we can quantify the amount of information he or she lost, known simply as the
information loss
(
IL
). Thus
To the extent that the information ratio is similar to the maximum Sharpe ratio, the information ratio can be understood as the reward-to-risk ratio. If the information ratio is 0.5, this means that
taking on 10% more risk will result in 5% extra return. On the flip side, the information loss shows the reduction in the reward-to-risk ratio. If the information loss is 0.1, then the portfolio manager is missing out on 1% of potential extra return for every 10% of risk he or she takes.
2.6 TENETS 5, 6, AND 7: STATISTICAL ISSUES IN QEPM
Tenets 5, 6, and 7 of QEPM concern issues arising from the application of statistical techniques to the portfolio-choice problem. In this section we discuss the three issues that a portfolio manager cannot neglect:
data mining, parameter stability
, and
parameter uncertainty
.
2.6.1 Data Mining
One of the biggest challenges for quantitative portfolio managers is to avoid the problem of data mining. Data mining violates tenet 5, which requires that quantitative models be based on sound economic theory. In some quantitative analyses, the use of data mining is quite obvious, but in other cases it is harder to detect.
Data mining
is the practice of running regressions of historical stock returns on so many combinations of factors that one is virtually guaranteed of finding a model or handful of factors that seem significantly correlated with stock returns but are in fact not particularly meaningful. Suppose that there are 99 potential factors
f
1
, …,
f
99
that may explain a stock’s return. Let
f
1
t
, …,
f
99
t
and
r
t
be the values of the factors and the stock’s return for month
t
. Suppose that we observe the value of these factors and the stock’s return for 100 months, and then we regress the stock return on all 99 factors. That is, we estimate the following equation:
What will we find out from the estimation? In this case, the goodness of fit (
R
2
) of the regression will be 100% because there will be no error in the regression (i.e.,
ϵ
t
= 0). With this equation, we superficially “explain” the stock return completely.
35
In truth,
though, the
R
2
of 100% simply reflects the fact that we included too many variables in the regression. From this regression, we cannot make any statistical inference about whether the model is valid or not. Even if we had made up the values of factors for the 100 months using a random-number generator, the regression still would have assigned coefficients so that
R
2
would equal exactly 100%. In fact, when there are 100 observations and more than 99 explanatory variables, the
R
2
always will be 100%. Basic statistics tells us not to include 99 variables when there are 100 observations.
Sometimes the problem is not so obvious. Suppose that we do a so-called stepwise regression. That is, we deliberately find the most significant variable out of 100 variables. Can we make statistical inferences from such a regression? No. Imagine again that we made up the value of factors using a random-number generator. If we deliberately look for the most significant of the 100 variables, we are guaranteed to get a significant variable because we have such a large pool of variables from which to choose. We set up the regression so that it would generate a significant variable, knowing in advance that whatever variable we eventually selected would be significant. The statistical significance of the variable is therefore no real indication that the variable explains stock returns well.
To illustrate the concept,
Fig. 2.1
shows the frequency distribution of the absolute value of
t
-statistics when we deliberately choose the most significant variable out of 100 randomly generated variables. For each simulation, 100 observations of the dependent variable and 100 explanatory variables were generated from the standard normal distribution independently. Given 100 explanatory variables, we selected the most significant explanatory variable by running regressions of the dependent variable on the selected explanatory variable and a constant. The simulation was repeated 1,000 times.
FIGURE 2.1
Frequency distribution of the absolute values of
t
-statistics from 1,000 simulations.
As can be seen from the figure, in most cases the absolute value of the
t
-statistic is greater than 2. The standard interpretation of this high
t
-statistic is that the selected variable is significant. But we know from the design of the simulation that the selected explanatory variable does not have anything to do with the dependent variable. The
R
2
of the regression will be high simply because the
t
-statistic is high, so the
R
2
also will be meaningless. For each simulation just described, we selected the 10 most significant explanatory variables and ran a regression of the dependent
variable on the selected variables and a constant. The frequency distribution of the resulting
R
2
is plotted in
Fig. 2.2
.
R
2
is mostly around 30% and 40%, quite high values, but again, the high
R
2
does not suggest true statistical significance. The outcomes of stepwise regressions are, in a sense, rigged, and this is not the kind of research a portfolio manager ought to perform.
FIGURE 2.2
Frequency distribution of
R
2
from 1,000 simulations.
Even avoiding stepwise regression in one’s own analysis, statistical conclusions still may be tainted indirectly by data mining. Even when an individual researcher does not select variables deliberately, the community of researchers may be doing a stepwise regression collectively. For example, in the 1970s, an MBA student in the business school of the University of Chicago found that the size (i.e., market capitalization) of a stock explained its return. Let’s say that the student came to this conclusion through valid statistical methods. We know, however, that there must have been thousands of other MBA students (not to mention hundreds of academics and practitioners) who have tried to explain stock
returns with other variables. The fact that one student’s conclusion about stock size gained widespread acceptance, whereas the conclusions of other studies did not, suggests that the community of financial researchers as a whole probably has been engaging in a kind of collective data mining referred to as
data snooping
. One therefore cannot accept in full faith the finding that the size of the stock is a significant explanatory variable.
We cannot completely avoid data mining or data snooping when we test a factor unless we use data that have never before been used to test that particular factor. When we test a factor with the same data that many other people have already used to test it, our conclusions may be influenced by their conclusions. For instance, authors of numerous investment textbooks have written about tests that they and others performed using U.S. stock data from the S&P Compustat database. In fact, many of these tests analyzed the same factors with the same stock data over the same time period. The P/E ratio in particular was one of the factors studied quite extensively. Thus, when we read in some textbooks that the P/E ratio explains stock returns well, we know, even before actually running any of our own regressions, that the P/E ratio will be
a good explanatory variable for much of the available data on U.S. stock returns. We cannot make any statistical inference from our own regression of returns on the P/E ratio unless we use data that have not already been extensively tested.
These problems suggest that careful empirical study is not enough to avoid the data-mining problem. The best way to generate meaningful statistics is to follow tenet 5 and make sure that the model is based on sound economic theory and common sense. Empirical evidence alone is not a sufficient basis for good practical decisions. A model will work only if there is a good reason to think that its factors explain stock returns and that the relationship between those factors and stock prices has not been exploited already by other investors.
In addition to letting theory guide the portfolio manager and using out-of-sample data, there are other methods to mitigate the data-mining problem.
36
In particular, portfolio managers, guided by the past research that has been done on factor anomalies, should attempt to control for data snooping through one of two methods: using statistical techniques like a Bayesian adjustment about a factor or investment strategy or adjusting the
p
-values or
t
-statistics of the significance of tests by the number of tests they are performing—and even the number of tests that may have occurred prior to their own testing and that might have influenced their beliefs. In the case of the Bayesian methods, they should adjust the significance of the empirical tests by their a priori belief about the importance of the factor (that is, theory leading). In the case of the
p
-value or
t
-statistic adjustments, the methods increase the critical values by which a factor should be accepted due to the repeated testing of many factors.
37
2.6.2 Parameter Stability
To make forecasts based on past data, we have to assume that history repeats itself. If the historical average of the stock return is around 1%, then we may assume that the stock return will be around 1% next month. If the standard deviation of the stock return is historically around 10%, then we may expect it to be around 10% next month.
Unfortunately, the constant flux of the market often interrupts the historical patterns that we might count on continuing. CEOs, employees, products, market conditions, and regulations change. As companies change, the properties of stocks also change. When the properties of stocks change, the parameters of stock-return models change. Thus, if we estimate
β
from the CAPM for, say, General Electric, then we have to ask ourselves, “Is the
β
of General Electric going to be the same next month? Next quarter? Next year?” If we estimate a more complicated model, we have to determine whether the estimation will be stable over time.
Consideration of parameter stability plays an important role in determining data sample size. For example, if we believe that
β
is generally not constant for more than five years, we should not estimate it from a sample that includes data covering more than five years. Or knowing that Daimler and Chrysler merged, we should not create a sample that includes both premerger data and postmerger data. Understanding parameter stability is crucial to QEPM. In
Chapter 16
we will discuss some simple ways to ensure parameter stability.
In the last decade, the threat to factor return stability has increased, and the risks associated with quantitative investing have also increased. The reason is partly due to the phenomenon of crowding.
38
Crowding is a recently identified risk in investing that can occur when multiple market participants begin to follow the same trade in such concentration that liquidity becomes fragile, altering the risk and return dynamics of the trade. That is, as portfolio managers and investors discover a new factor, the popularity
of the strategy can actually reduce the future performance of the strategy. When quantitative strategies or factor strategies become public through publication or through the launch of an investment product, the future risk-adjusted returns of that strategy decrease by a large magnitude. Thus, the measured performance might not be a stable estimate of the future performance.
39
In order to assess future strategy performance, portfolio managers should make sure historical backtesting is realistic (i.e., consider trading costs), be aware of crowding, and be aware of how the nature of the factors themselves is changing over time.
2.6.3 Parameter Uncertainty
Having extra information never hurts and is often helpful. However, extra information should not necessarily alter the portfolio composition. A portfolio manager may be able to construct a portfolio that is expected to outperform the benchmark. Does this mean that he or she should automatically choose the active portfolio instead of an indexed one? No. The active portfolio may have too much risk compared with the gain in expected return. Whether the risk is “too much” depends on an individual portfolio manager’s attitude, but the amount of risk can be checked in principle.
Even if the active portfolio does not look too risky on its surface, it could have a high degree of parameter uncertainty, which is a component of risk. Standard statistics overlooks this important point. Parameter uncertainty exists in all statistical estimations of stock-return models because all estimations contain some degree of estimation error, as measured by the standard error. Mean-variance optimizations therefore should take standard error into account as one aspect of a portfolio’s risk. When the standard error is considered, it may become apparent that a supposedly superior active portfolio’s risk-adjusted return is, in fact, no better than the benchmark’s.
The standard error, which measures the error of the estimation, depends on two things: the variance of the error in the model and the variance of the explanatory variables.
40
The variance of the
error shows how precise the model is. If the model is 100% precise, the error always will be zero. The variance of the explanatory variables shows how informative the data are. If the variables do not change at all, their variance is zero, and the standard error will be infinite. Therefore, to reduce the standard error, the model and the explanatory variables should be selected carefully.
In general, the portfolio manager should consider not only the estimated value but also the standard error of the estimates. If the standard error is large, then that should be considered part of the portfolio’s risk. This is one of the fundamental implications of Bayesian econometrics for portfolio selection. Bayesian econometrics is gaining acceptance by industry practitioners, and we will discuss the Bayesian approach in
Chapter 14
.
2.7 CONCLUSION
We started this chapter with a discussion of
α
and the information ratio, the concepts of risk-adjusted excess return, because the goal of QEPM is to create portfolios with high levels of return for risk. We then looked in detail at the seven tenets of QEPM that all quantitative equity portfolio managers should follow. The seven tenets deal with concepts of market efficiency, the fundamental law of active management, and statistical issues. As a form of active management, QEPM is based on the belief that markets, despite functioning efficiently in general, contain many patterns of inefficiency that open up opportunities for statistical arbitrage. An understanding of the information criterion and the concept of information loss from the fundamental law helps portfolio managers to exploit these opportunities to the fullest. Successful QEPM also depends on managers being vigilant about data mining, parameter uncertainty, and parameter stability.
Now that we have a firm grasp of QEPM concepts, we turn to the key piece of QEPM, the quantitative model of stock returns, which brings together theory and observation into one tool for selecting stocks for the portfolio.
QUESTIONS
2.1.
(a)   What are the three types of
α
used in QEPM, and how are they different?
(b)   What is another type of
α
commonly used by the general investing public, and why is it less relevant to QEPM?
2.2.
(a)   When does
α
B
=
α
CAPM
?
(b)   Can
α
MF
ever be the same as the other types of
α
?
2.3.
(a)   What distinguishes ex-ante
α
from ex-post
α
?
(b)   Ideally, what relationship would a portfolio manager want between them?
2.4.
(a)   Define the information ratio.
(b)   Why is it important in QEPM?
2.5.
Name the seven tenets of QEPM.
2.6.
Explain the difference between a pure arbitrage and a statistical arbitrage.
2.7.
Name the three types of market efficiency.
2.8.
Define weak-form market efficiency.
2.9.
Define semistrong-form market efficiency.
2.10.
Define strong-form market efficiency.
2.11.
Give an example of a type of quantitative analysis that would not work for each of the types of market efficiency.
2.12.
Name three documented anomalies. Can you think of a theoretical or behavioral justification for these anomalies? If so, explain.
2.13.
Name the three anomalies that are most likely to be subject to data mining or data snooping. Explain.
2.14.
What is ambiguity aversion? Give an investment example.
2.15.
What is the disposition effect?
2.16.
It has been documented that trading volume decreases during bear markets. Can you explain this phenomenon with common behavioral biases?
2.17.
Give three reasons why practitioners of QEPM might believe that markets are inefficient.
2.18.
A special case of the fundamental law is related to the idea that independent forecasts with informational value can improve the power of the overall forecasts. Suppose that you and your QEPM department decided to forecast the equity markets every month. The choices are market up, market down, or market flat. You collected the forecasts of every participant and then constructed the QEPM department’s
consensus forecast as follows. The aggregate forecast is the majority. Thus, if there are more than
n/
2 “long” signals, the combined forecast goes “long”; if there are fewer than
n/
2, the combined forecast goes “short”; and if there are exactly
n/
2, the combined forecast is determined by a coin flip. Suppose furthermore that you make the assumption that everyone’s opinions are independent of each other.
(a)    Under what conditions would the QEPM department’s consensus forecast be better than any individual forecast?
(b)    Suppose that everyone had the same probability of being right,
p
. Consider the following individual probabilities: 0.5, 0.53, 0.60, 0.65, 0.70, and 0.75. What would be the corresponding probabilities of the QEPM department’s consensus being right, assuming that there are 22 participants in the consensus?
2.19.
The fundamental law makes a number of approximations. One of them is
(a)    Calculate the error from the preceding approximation when the value of
R
2
is 10%, 20%, 50%, and 80%.
(b)    Express the approximation error as a function of
R
2
. Is the approximation error bounded?
(c)    We have claimed in this chapter that
IR
2
is approximately equal to
R
2
. However, while the value of
R
2
is bounded (0 ≤
R
2
≤ 1), the value of
IR
2
is not. Can you explain this discrepancy?
2.20.
That
IR
2
is approximately
R
2
can be verified by a very simple situation. Suppose that we estimated the following equation for stock
XYZ
:
where
f
1
t
, …,
f
Kt
are forecasting factors. Using this equation, we predict the return for
T
+ 1.
(a)    What is the expected return of stock
XYZ
for
T
+ 1? What is the standard deviation of stock return for
T
+1? Express the Sharpe ratio of stock
XYZ
for
T
+1 in terms of data and estimates.
(b)    Express
R
2
and
R
2
/(1−
R
2
) in terms of data and estimates.
(c)    Show that the squared Sharpe ratio of stock
XYZ
can be approximated by
R
2
. When would the approximation create a large error?
(d)    Show that
IR
2
can be approximated by
R
2
if the portfolio is made only of stock
XYZ
and the benchmark is the cash return.
2.21.
Suppose that a portfolio manager predicts the return of MSFT and GE from earnings forecasts of 10 analysts. Let
r
MSFT
and
r
GE
be the return of MSFT and GE and
E
MSFT,1
, …,
E
MSFT, 10
and
E
GE,1
, …,
E
GE,10
be the forecasts of 10 analysts.
(a)    Using the historical data, the portfolio manager may estimate the following equations:
If the portfolio manager predicts return based on this model, what would be the breadth?
(b)    Quite often in reality the portfolio manager has access only to the consensus forecasts (i.e., the average earnings forecasts). Then the portfolio’s return prediction may be based on the following equations:
What would be the breadth?
(c)    An alternative definition of the breadth is the number of “distinct signals.” If we adopt this alternative definition of the breadth, do your answers to (a) and (b) change?
(d)    One disadvantage of defining the breadth as the number of distinct signals is that the two preceding models will have the same breadth. Discuss why this is a dis-advantage.
2.22.
Suppose that a portfolio manager predicts the return of MSFT and GE from earnings forecasts of 10 analysts. Five analysts provide earnings forecasts for MSFT, and five analysts provide earnings forecasts for GE. Let
r
MSFT
and
r
GE
be the return
of MSFT and GE and
E
MSFT,1
, …,
E
MSFT,5
and
E
GE,6
,…,
E
GE,10
be the forecasts. Using the consensus earnings forecasts (i.e., average forecasts), the portfolio manager may estimate the following equations:
(a)    If the portfolio manager predicts return based on this model, what would be the breadth?
(b)    If the portfolio manager applies the models to GM stock as well as MSFT and GE, would your answer to (a) change?
(c)    If we define the breadth as the number of “distinct signals,” would your answer to (b) change? Explain why it is not practical to define the breadth as the number of distinct signals.
2.23.
The information loss is defined as the difference between the maximum information ratio and the actual information ratio.
(a)    What does it mean to have an information loss of 0.1?
(b)    What is the value of the information loss when the information criterion is satisfied?
(c)    What is the minimum possible value of the information ratio? Is there a maximum possible value of the information ratio?
2.24.
A portfolio manager believes that the expected returns of stocks
A, B, C, D
, and
E
are as follows:
She also found out that the risk (standard deviation) of each stock is 25% and that the five stocks are independent from one another. After examining this information, the portfolio manager created an equal-weighted portfolio of stocks
C, D
, and
E
.
(a)    Is the information criterion satisfied?
(b)    Calculate the expected return and the standard deviation of the portfolio.
(c)    What is the best portfolio one can create out of five stocks? Calculate the expected return and the standard deviation of the best portfolio.
(d)    Calculate the information loss.
2.25.
(a)    What are data mining and data snooping?
(b)    Is it possible for a quantitative portfolio manager to avoid them? Explain.
2.26.
What does it mean for parameters to change? What might cause parameters to change? Why might a quantitative portfolio manager be worried about parameter stability?
1
In practice, many quantitative managers simply refer to benchmark
α
as
α
because ultimately they measure their success or failure against a benchmark. The portfolio manager does typically increase his or her residual risk when pursuing
α
. Theoretically, a portfolio manager could increase his or her
α
with zero incremental risk, but practically this is rare.
2
CAPM
α
is also sometimes referred to as
Jensen’s α
.
3
The reader can think of these returns in these regressions as the returns minus the risk-free rate.
4
Note that this usage of residual is somewhat different from the standard usage in econometrics. In econometrics, the residual refers to the realization of
ϵ
and does not include
α
. Unfortunately, the use by practitioners does not always coincide with the use by academics.
5
For those unfamiliar with the CAPM, see a brief discussion of the fundamental models of stock return in Appendix B at
www.ludwigbc.com
under QEPM Exclusive Content.
6
Suppose that we postulate the following models of stock returns:
r
P
=
α′
+
β′r
B
+
ϵ′, r
P
=
α″
+
β″r
M
+
ϵ″
, and
r
B
=
α
+
βr
M
+
ϵ
. By substitution of variables, we see that
r
P
=
α′
+
β′α
+
β′βr
M
+
β′ϵ
+
ϵ′
. From this relationship we can see that
α″
=
α′
+
β′α
. Thus, for a positive
β′, α″
<
α′
when
α
< 0, and vice versa.
7
For those unfamiliar with the APT, see a brief discussion of the three fundamental models of stock returns in Appendix B at
www.ludwigbc.com
under QEPM Exclusive Content.
8
In golf, there is a saying that goes, “Drive for show, putt for dough.” In QEPM, it would be “Ex-ante
α
for show, ex-post
α
for dough.”
9
Parameter uncertainty depends, among other things, on sample size. If the sample size is small, the parameter uncertainty will be large. By properly accounting for the parameter uncertainty, portfolio managers can avoid the common mistake of exaggerating the estimation from small sample sizes.
10
If the market were perfectly efficient, would it have been possible for Warren Buffett to earn an average annual return of 20% between 1965 and 2020, beating the S&P 500 by 9.8% per year? (
Source
: Berkshire Hathaway 2021 Annual Report, Chairman’s Letter to Shareholders, p. 2.) Even in a perfectly efficient market, a few investors would indeed earn very high returns because there would still be some outliers in the distribution of returns. In a truly efficient market, however, Buffett’s returns would have come at the price of extra risk rather than generating
α
. Also, his performance would have been simply good fortune rather than an ability to find companies selling below their intrinsic values.
11
See Chincarini (2012) for a detailed account of crowding and the financial crisis of 2008.
12
See Murphy (1999).
13
A test of the efficient-market theory requires an asset pricing model (e.g., CAPM) for the purpose of calculating risk-adjusted returns. Thus the rejection of efficient-market theory, or the discovery of an anomaly, may indicate the failure of the chosen asset pricing model rather than the failure of the efficient-market theory. This ambiguity regarding the nature of an anomaly is known as the
joint hypothesis problem
. In this chapter, for the purpose of simple exposition, we describe an anomaly as representing the failure of efficient-market theory.
14
See Lo, MacKinlay, and Campbell (1997), p. 66.
15
See Conrad and Kaul (1988) and Jegadeesh and Titman (1993, 2001).
16
See Jegadeesh (1990). Also see the list in
Table 2.2
.
17
See Moskowitz and Grinblatt (1999).
18
The January effect is often attributed to Sidney Wachtel [see Wachtel (1942)].
19
The law currently only allows up to $3,000 to be used to offset income taxes.
20
There is a wash-sale rule that prohibits repurchasing before 30 days after the sale, so that adds some delay to the repurchasing by sellers.
21
In general, some portfolio managers may take big bets regardless of the month because they figure that the worst that will happen to them personally is to miss a bonus. There are no income penalties for poor performance, generally. Of course, after too many years of poor returns, a manager is likely to lose his or her job, not just his or her bonus. For more information on mutual fund incentives at other times of the year, see Brown et al. (1996), Busse (2001), and Taylor (2003).
22
Let us mention that Professor Roll used to have a money management shop with the late Professor Stephen Ross of MIT. In addition, Fuller-Thaler Asset Management, named after Nobel prize–winning behavioral economist Richard Thaler, manages around $11 billion to exploit behavorial biases.
23
As Gekko says in the movie
Wall Street
, “If you’re not inside, you’re way outside.”
24
It is illegal to trade on “material, nonpublic” information. However, to a certain degree, insiders have greater information about a company than outsiders. Some of this information can be traded on legally, leading them to profit from the trades they place on their companies’ stock. According to the SEC’s Rule 10b5–1, an executive’s trade is not considered “insider trading” if a detailed contract planning the trade was established before the executive gained the “material, nonpublic” information in question and the contract was executed exactly as written.
25
This test was known as the
specialist’s
test, but it is no longer useful because the structure of securities markets has dramatically changed and specialists are now known as
designated market makers
(DMMs). Electronic limit-order books and high-frequency trading have dramatically reduced the importance of specialists on the exchange.
26
See Ross (2002).
27
Some investors believe anomalies exist due to institutional constraints. That is, institutions may have constraints on their ability to buy or sell that create arbitrage opportunities for less constrained investors.
28
At the end of 1999, Amazon was trading at a large multiple to Barnes & Noble. A short position in AMZN and a long position in BKS would have made a return of 74% on the AMZN position and a 28% return on the BKS position as the price of Amazon collapsed while Barnes & Noble’s price rose. In the long run, however, it turned out that Amazon was much more than a bookseller, and an investment in Amazon turned out to be spectacular. From 2000 to 2019, a long position in Amazon yielded around 7,500%, while Barnes & Noble lost about 14%. This brings to mind another conundrum: is efficiency intrinsically related to the investment horizon?
29
For example, Regulation T of the Federal Reserve permits borrowing of stocks up to only 50% of their investment. Thus, borrowing, in reality, is not unlimited. Markowitz (2005) has reiterated that in the absence of unlimited borrowing and lending, the market portfolio will not be efficient.
30
See Grinold and Kahn (1995).
31
Since the mathematics involved is rather heavy, we have placed the derivations of these truths in Appendix 2A, which can be found at
www.ludwigbc.com
under QEPM Exclusive Content.
32
One may notice that the range of values
R
2
can take is bounded, whereas that is not the case for
IR
2
. This discrepancy results from a number of approximations introduced in the fundamental law. If
IR
2
has a high value, the approximations that the fundamental law introduces create a huge approximation error.
33
In theory, the breadth can be much larger than the number of explanatory variables if one counts the number of distinctive signals. We show in Appendix 2A, which can be found at
www.ludwigbc.com
under QEPM Exclusive Content, that this way of determining the breadth has limited practicality.
34
See Chincarini and Kim (2007).
35
We have 100 unknown parameters and 100 observations. Thus 100 unknown parameters are determined from a system of 100 equations. As long as the 100 equations are not linearly dependent, there will be a unique solution, and
ϵ
t
will not have any role.
36
Since the publication of the first edition of this book in 2006, there has been an explosion of factor research and a movement to address the data-mining problem that we emphasized in the first edition of this book. See Arnott et al. (2019), Harvey et al. (2016), and Harvey (2017).
37
These methods include the Bonferroni test, the Hommel test, the Holm test, the Hochberg test, the Dubey-Armitage-Parnar test, and the Tukey-Ciminera-Heyse test. See Sankoh et al. (1997), Hochberg (1988), Holm (1979), Hommel (1988), Armitage and Parmar (1986), Dubey (1985), Shi et al. (2012), and Tukey et al. (1985). The simplest method, the Bonferroni method, was named after Italian mathematician Carlo Emilio Bonferroni. A simple example may help. Suppose a researcher wants to test some data on whether 160 factors are significant with 60 months of data. The typical 5% error threshold for each factor would imply a
t
-statistic of 2 or greater. A Bonferroni adjustment would require a
t
-statistic of 3.83 for each factor. This assumes that factors are independent. One can adjust Bonferroni for correlations in a multiple of ways. One of the simplest would reduce the critical
t
-statistic for each factor to 3.66 with an average correlation of 0.4 amongst factors. See
Appendix 4B
for more information on these techniques.
38
See the work of Chincarini (2012), as well as Chincarini (1998, 2017), Chincarini et al. (2018), Cahan and Luo (2013), Yan (2014), Chue (2015), Zhong et al. (2016), Baltas (2019), Brown et al. (2019), and Volpati et al. (2020). For the problems related to copycat trading amongst quantitative funds, see Chincarini (1998), Rothman (2007, 2008), Goldman Sachs (2007a, 2007b), and Khandani and Lo (2008). There are also more references for crowding in some of the presentations at
https://ludwigbc.com/presentations/slides/
.
39
See Arnott et al. (2016), Calluzzo et al. (2019), McLean and Pontiff (2016), Jacobs and Muller (2020), and Hou et al. (2020).
40
Readers who are not familiar with these concepts may consult Appendix C at
www.ludwigbc.com
under QEPM Exclusive Content.
