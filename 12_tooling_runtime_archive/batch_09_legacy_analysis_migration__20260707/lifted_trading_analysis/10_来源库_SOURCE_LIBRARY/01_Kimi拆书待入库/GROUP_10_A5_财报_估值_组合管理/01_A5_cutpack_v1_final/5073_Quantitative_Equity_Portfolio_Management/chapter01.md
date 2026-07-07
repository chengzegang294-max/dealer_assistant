# Quantitative Equity Portfolio Management: An Active Approach to Portfolio Construction and Management, Second Edition

- **book_name**: 5073 Quantitative Equity Portfolio Management, Second Ed.
- **main_source**: epub
- **cross_check_source**: none
- **pdf_role**: not_needed
- **split_scope**: chapter file = chapter01

---

CHAPTER 1
The Power of QEPM
The first duty of intelligent men is the restatement of the obvious
.
—George Orwell
1.1 INTRODUCTION
Personal investors place their savings in the hands of professional money managers in the belief that the professionals, with their specialized skills, will make the best investment decisions for them. In fact, more than 106 million Americans, the equivalent of about half of all U.S. households, entrust their money to mutual funds. They and other investors are the reason why there are more than 11,000 U.S. stock mutual funds and exchange-traded funds (ETFs) managing $24.9 trillion and more than 3,000 U.S. hedge funds.
1
Yet, while assets in these types of investment funds stand in the trillions of dollars, many people have begun to question whether the professionals really do have an edge on amateur investors. There is evidence that only 14% of equity mutual funds managed to beat the
Standard and Poor’s (S&P) 1500 from 2000 to 2020.
2
Despite poor performance by some funds, however, we firmly believe that professional managers
do
invest better than the average investor when they use certain tools available to them to quantify and truly understand the risks they are taking. Superior portfolio returns are possible through
quantitative equity portfolio management
(QEPM).
In this book, we use
QEPM
to refer mostly to an active, quantitative style of equity portfolio management, although the quantitative tools we describe can be applied easily to passive management strategies. Broadly speaking, equity portfolio management styles can be defined in two dimensions:
passive
versus
active
and
qualitative
versus
quantitative
. The passive-versus-active dimension reflects whether the portfolio is being managed simply to match the return of the benchmark or exceed the return of the benchmark. Passive management, also referred to as
indexing
, involves following and trying to match the returns of an equity index (e.g., the S&P 500) or other benchmark as closely as possible. The “passive” portfolio manager only initiates trades in order to mimic changes in the composition of the index, to reinvest dividends, to deal with the portfolio’s cash inflows and outflows, or to respond to corporate actions that affect stocks that make up the index. Index portfolio managers typically are rewarded for their ability to replicate the index. In the U.S., passive management grew from 8.69% in 2000 to 40% in 2020 of all managed mutual funds and ETFs, primarily owing to the poor performance of many active fund managers versus standard equity indices. Passive management implicitly assumes that portfolio managers cannot beat the market.
Active management takes the view that it is possible to choose stocks that will outperform an equity index or other benchmark. “Active” managers also sometimes aim for some absolute level of performance without any reference to an index or benchmark. Trading takes place when the manager wants to buy stocks expected to have superior returns, when there are dividends to reinvest, or when cash flows into or out of the portfolio. In many cases, actively managed portfolios have higher turnover than passively managed ones because active portfolio managers tend to trade
more frequently than passive managers do. Active managers usually are rewarded for the portfolio’s absolute return or risk-adjusted return over a benchmark.
The second way to define portfolio management styles is to look at whether the manager bases decisions mainly on qualitative or quantitative analysis. Of the two general styles, perhaps the easiest for the average investor to understand is
qualitative management
, which is sometimes called
fundamental management
(although that term can be misleading because quantitative managers look at stock fundamentals as well). What makes the style qualitative is the fact that the research focuses on intangibles and generally does not involve using mathematics or computer programs specifically to identify “good” and “bad” stocks. Qualitative management is almost always a kind of active management because qualitative managers handpick stocks that they expect to outperform the market. Their selections are based on information from income statements and balance sheets, financial ratios, phone interviews with company personnel, research reports, and ad hoc methods of analysis. They also rely on their own gut reactions. For the most part, qualitative managers use their own judgment and informal calculations to filter the information that they and their analysts gather.
Peter Lynch, who led the Fidelity Magellan Fund to a compounded return of more than 2,700% during his tenure as fund manager from 1977 to 1990, is one of the best-known practitioners of the qualitative style. One of Lynch’s largest holdings at Magellan was inspired by his wife’s enthusiasm for L’eggs, Hanes Corporation’s brand of women’s hosiery packaged in egg-shaped containers and sold at local drugstores and supermarkets. Magellan’s position in Hanes prospered when L’eggs became a huge hit with consumers. Subsequently, a competitor of Hanes, the Kayser-Roth Corporation, tried to copy the success of L’eggs by selling its own brand of panty hose. Concerned about possible erosion of Hanes’ market share, Lynch undertook what he has termed “fundamental research” on the matter. He bought 48 pairs of Kayser-Roth’s No Nonsense panty hose and asked a group of female coworkers to try them for a few weeks. Based on their assessment that the No Nonsense product was not nearly as good as L’eggs, Lynch decided to hold onto Hanes’ stock. He was richly rewarded for his (somewhat unconventional) qualitative methods when Hanes’ stock continued to rise, and the company
eventually was acquired by what is currently known as the Sara Lee Corporation.
3
Quantitative management
, unlike the rather intuitive process of qualitative management, is rooted in mathematics and statistics and less concerned with intangibles. Quantitative portfolio managers use any numerical data or quantifiable information relevant to the investment decision. This could include stock fundamentals from the income statement and balance sheet, technical data (e.g., stock prices and trading volumes), macroeconomic data, survey data, analyst recommendations, and any other data collected and stored in a database. Quantitative managers, unlike their counterparts in the qualitative tradition, use their data to build quantitative models of security returns. These models, along with advanced statistics, mathematics, and computer software, are used to identify “good” and “bad” stocks. Essentially, quantitative managers filter information mathematically rather than intuitively.
The particular field of quantitative management that we refer to as QEPM is, like most forms of qualitative management, an active approach to investing. With QEPM, the manager aims for returns that exceed a benchmark or market index. QEPM’s tools for measuring and controlling risk do allow for highly accurate passive management. QEPM can accomplish much more than pure indexing, though, so our focus is on exploiting quantitative methods for outperformance.
Quantitative management is associated less with great individuals than with great institutions, and many successful mutual funds practice QEPM. There is a strong quantitative management presence at Acadian Asset Management, AQR Capital, Blackrock, Goldman Sachs Asset Management, Parametric Portfolio Associates, Putnam Investments, Quantitative Management Associates, State Street Global Advisors, and Two Sigma, among others. Many hedge funds’ portfolios are based on QEPM as well. And even many enhanced index managers (more passive style) who manage portfolios with respect to a benchmark with the goal of modest excess performances also practice QEPM.
Over the years, quantitative management gradually has gained prevalence as even self-described qualitative managers have adopted some quantitative methods. A number of forces have
propelled this shift toward the quantitative, the first being the advancement of technology since the 1990s. Complicated computer models of stock returns that once took days to run are now generated in a matter of minutes. Computing speed also allows computer programs to dig through great amounts of data in order to uncover buried treasures. The internet, meanwhile, makes it easier to access a wealth of data to analyze. With so much information at their fingertips, though, investors sometimes can become overconfident and make poor investment choices. The near glut of data only increases the need for quantitative analysis, which imposes discipline on the decision-making process.
In some ways, quantitative approaches also fare better in the post-Enron regulatory environment than qualitative styles do. Now that companies are required to give
fair disclosure
of events, portfolio managers and analysts can no longer get company news ahead of the rest of the market by chatting with the CFO, for instance. Fair disclosure means that all information must be uniformly distributed and available through public data resources—a boon for quantitative managers, who typically use software programs to access large quantities of data, but a blow to qualitative managers, who traditionally have gathered a great deal of their information through informal, one-on-one conversations with company executives.
Quantitative methods help managers to respond to calls for greater transparency as well. Average folks are becoming savvier investors and demanding more information from the people who manage their money. Employees want to know exactly how pension funds are investing their retirement savings. When questioned about their investment strategies, quantitative fund managers can point to clear, objective methods as the basis for their decisions.
Finally, the stability of quantitatively managed portfolios is becoming a selling point with investors. Quantitative strategies can control risk precisely. Precise risk control helps the portfolio avoid large swings in value and instead earn reliable, if modest, returns, which are what many investors seek. Although there have been a number of star managers who have consistently figured out how to beat the market, many qualitative managers have failed to beat the S&P 500 on average over time. Their portfolios have sporadically earned extremely high returns only to sink subsequently into years of underperformance. Portfolios that employ the quantitative risk controls that keep volatility low offer an attractive alternative to such roller-coaster rides.
1.2 THE ADVANTAGES OF QEPM
Quantitative equity portfolio managers gain numerous advantages over their traditional, qualitatively oriented counterparts by organizing and filtering great amounts of data with advanced statistics and mathematics. The disadvantages of QEPM mainly have to do with the possibility of relying the wrong way on quantitative models and historical data.
Table 1.1
lists QEPM’s advantages and disadvantages in comparison with qualitative management.
TABLE 1.1
The Advantages and Disadvantages of QEPM versus Qualitative Management
One of the greatest advantages of QEPM is that when a model of stock returns is in place, construction of the portfolio is a highly objective process. The quantitative manager creates quantitative models of returns from underlying financial and other data, and these models tell the manager how to construct an optimal portfolio of stocks. The actual buy and sell decisions of the quantitative portfolio manager come directly from the model. This significantly lessens the impact of one person’s biases on the portfolio. In contrast, a qualitative manager’s buy and sell decisions often are based solely on the manager’s opinion and thus are relatively more susceptible to the influence of behavioral biases. The objectivity of QEPM boosts the portfolio’s returns and also supports management
transparency. There is a clearly defined process for selecting stocks that can be presented to investors.
Another major advantage of QEPM is that computerized quantitative models can analyze large amounts of data and a large volume of stocks in a short amount of time. We call this the
advantage of breadth
. The same breadth is practically impossible with qualitative management because, to use Peter Lynch’s metaphor, there are simply too many rocks to turn over one by one.
4
In the course of analyzing literally thousands of stocks with computer programs, the quantitative manager may unearth some diamonds in the rough that the qualitative manager would never find. Some qualitative portfolio managers do use stock screens and elements of quantitative management to help them sort through the stock universe. Ultimately, though, a total QEPM approach is a more complete analysis of the entire stock universe than this sort of mixed analysis.
As we mentioned earlier, QEPM inoculates the portfolio, to some extent, against behavioral biases and errors. The area of behavioral finance has grown in recent years as economists have identified the types of impulses that lead to irrational investment decisions. Portfolio managers may be better than the average investor at controlling these impulses, but they have them just the same. One such impulse is the
disposition effect
, the desire to hold onto “loser,” or poorly performing, stocks too long. Investors often hope that losers will rebound despite all evidence to the contrary. Strict adherence to QEPM procedures helps to prevent a portfolio manager from trading on this sort of wishful thinking because it takes the final decision out of the manager’s hands to some extent. If the quantitative model of stock returns recognizes a “bad” stock, that is the trigger for selling the stock. (It is easy for the model to make the tough calls about selling; after all, it lacks any emotional attachment to the stocks.)
Overconfidence
, another common behavioral bias, leads to too much trading, raising transactions costs. QEPM curbs overconfidence because the optimization model specifically controls trading costs.
Confirmation bias
leads some investors to block out relevant bad news on stocks they like. Again, with QEPM, the quantitative model processes all relevant information objectively.
QEPM strategies also have the benefit of being replicable. Portfolio managers can pass their models on to their successors when they leave a firm. The firm is not completely dependent,
therefore, on the presence of a star manager. Replicability also makes it possible to backtest investment strategies on historical data over different time periods, in different markets, and with alternative specifications. Unlike quantitative methods, qualitative interpretations of market events are largely in the eye of the beholder, making them difficult to replicate in the absence of the manager who comes up with them, difficult to backtest, and difficult to articulate to investors as a methodology.
The cost of portfolio management is generally lower with QEPM than it is with qualitative management. The Ph.D.’s and other “quants” who must be hired to build the stock models generally demand high salaries, but, after the models are implemented, computers do a big share of the work. This keeps the QEPM department’s head count relatively low compared with departments that delve into extensive qualitative research.
One of the most important advantages of QEPM is that it provides precise measurements of risk. A good understanding of stocks’ exposure to risk factors is essential to the entire construction of the portfolio. More specifically, the ability to measure the risk of the portfolio versus a benchmark has opened the gate for controlled enhanced index management. By quantifying the tracking error of the portfolio, managers can select stocks that both earn high returns and keep the risk of the portfolio within very specific boundaries. This is difficult to do without using quantitative risk-control mechanisms.
There are some minor disadvantages to QEPM, the most prominent being the problem of translating qualitative inputs into quantitative data for use in a quantitative model. Despite the problems inherent in investing in subjective perceptions, there are valuable insights to be gained from, for instance, visiting a store and evaluating its level of customer service. Incorporating this sort of evaluation into QEPM is not simple. Numerical customer satisfaction ratings of the store might be a useful stand-in for a manager’s first-hand observations, but such information probably would be difficult to obtain. Even if it were available, how should it be added to a model already built on other data? Later in this book we will show how qualitative inputs from fundamental analysts can be translated into data suitable for quantitative models.
5
QEPM’s heavy reliance on historical data has drawbacks. Historical relationships may not continue in the future, throwing off stock-return forecasts. New types of companies and new market environments, such as the internet bubble of the late nineties, diminish the relevance of inferences and expectations based on past patterns. QEPM is not unique in its reliance on historical information, however, and the statistical tests that quantitative managers apply to a set of data may help them to determine what portion of it is no longer useful. Statistical tests resolve some, but not all, questions about the continuity of trends in the data.
There is the potential for misuse of statistical tests. Data mining, a highly inappropriate practice, involves testing many statistical relationships in historical data and picking the one that apparently explains past stock returns most accurately.
6
The “mined” strategy will have almost no relation to current market conditions and therefore very little ability to predict future stock returns.
7
Unfortunately, many quantitative managers and analysts nonetheless are tempted to do data mining because it is so easy to keep testing and discarding models until finding one that works well on historical data. It takes integrity and discipline to resist the temptation.
8
Qualitative managers are susceptible to a form of data mining known as
data snooping
,
9
so the misapplication of historical relationships is endemic to active portfolio management as a whole.
The last disadvantage we associate with QEPM is its reaction time.
10
QEPM strategies may be slow to react to a shift in the economic paradigm or a change in the investment environment because they are drawn from historical data. Advanced statistical
analysis, research, and ingenuity can improve the reaction time. Delayed reaction to new conditions is a problem shared, though to a lesser extent, by qualitative managers. Qualitative strategies can be modified quickly in the face of changing conditions. How well the modifications work depends, of course, on how accurately the manager and analysts interpret events.
Overall, we believe that QEPM’s advantages far outdistance its disadvantages. Many of the disadvantages of QEPM are common to all types of active portfolio management. Its particular benefits, however, make it especially well suited to this age of information overload and ever-growing competition among investment funds to find good, unexploited opportunities.
1.3 QUANTITATIVE AND QUALITATIVE APPROACHES TO SIMILAR INVESTMENT SITUATIONS
We have spoken in general about the advantages of QEPM, but you may be wondering how a quantitative manager’s response to specific market conditions differs from a qualitative manager’s. In this section we discuss quantitative versus qualitative strategies for real-world investment problems.
11
The Federal Reserve of the United States sets interest rates through the Fed funds target rate, which is typically announced at Federal Open Market Committee (FOMC) meetings. At its meeting on March 15, 2020, at the outbreak of the Covid-19 pandemic, for instance, the Fed lowered the Fed funds target rate to a range between 0% and 0.25%. Such changes in the target rate reverberate throughout the bond and equity markets, so investors try to anticipate them and also gauge what the rest of the market expects them to be. The market trades on these expectations via Fed futures that are based on the effective Fed funds rate, the daily average of the Fed funds rate over the previous month.
With an FOMC meeting on the horizon, a qualitative manager might say, “It’s highly likely that Fed Chairman Powell will raise rates by 25 basis points. We should reduce the
β
exposure of the portfolio.” This assessment may be right on the nose, especially
given the qualitative manager’s years of experience watching the markets. A quantitative manager, however, is more likely to use market data, such as Fed fund futures prices, to specify exactly the implied probability that the Fed will raise rates. In this way, the quantitative manager can state with confidence, “The market has already priced in a 98% probability of a 25 basis point raise in rates.” The quantitative manager also has the tools to quantify the effect of a rise in rates on various types of equities, including cases in which the market expects the increase.
12
This is a much more precise analysis, for investment purposes, than the qualitative manager’s gut-feeling approach.
Recently, the government of a major country, certain that interest rates were on the rise, wanted to invest in a portfolio of stocks inversely related to interest rates. There are many types of fixed-income investments that would have been appropriate for protecting against a rise in interest rates, but the government wanted an all-equity portfolio. A qualitative analyst might have begun constructing the portfolio using some rule of thumb, such as screening for companies with low debt-to-equity ratios or for companies in the utilities industry, which is known to hold up well in the face of high interest rates. The screen would have yielded a list of stocks that ought to do well in the upcoming high-rate environment.
By contrast, a quantitative analyst probably would have started work on this portfolio by creating an economic factor model that explicitly modeled stock returns in relation to the macroeconomic factor of concern, interest rates.
13
From the results of the model, the analyst then would have constructed a portfolio of equities with low or negative exposures to interest rates. As opposed to the merely directional prediction of the qualitative manager’s rule of thumb, the quantitative model would have shown
how much
individual stocks and the entire portfolio likely would react to higher interest rates, with an estimate of the degree of uncertainty of the expected behaviors. Being able to anticipate not only the direction but also the amount and uncertainty of movement in stock prices, the quantitative manager would have formulated a more precise interest-rate hedge.
Sometimes companies are provided with windfall revenue streams, such as when another company or the government awards them a contract. This happened during the Covid-19 pandemic to AstraZeneca when it won a contract with the U.S. government for its Covid-19 product AZD7442. On October 9, 2020, the U.S. government announced that it would provide AstraZeneca with approximately $486 million for two phase 3 clinical trials and related development activities. A qualitative manager might have seen this announcement and said, “The stock has only gone up about 62 cents per share. I have a feeling this deal is worth a lot more than that. Let’s make it a short-term buy.” This intuition may have merit, but it is not very precise. Given the available information, it would have been possible to do a much more precise analysis quantitatively.
The manager could have used a modified discounted cash-flow model to evaluate the impact of this deal on the stock price of the company. The manager then could have observed the actual change in the stock price, compared it with the predicted change in the stock price from the model, and made an informed decision about whether to go long or short the stock as a short-term trade.
14
Performance attribution is another type of analysis that benefits from quantitative techniques. With classic performance attribution, a quantitative performance analyst can split the portfolio’s excess returns over the benchmark into their underlying sources, making it easier to pinpoint the investment decisions that augmented or diminished the portfolio’s performance. Calculations of risk-adjusted performance tell the analyst whether a portfolio’s excess performance was due to extra risk (pseudo-outperformance) or to additional return without additional risk (true outperformance). For analyzing the performance of a competitor’s portfolio, techniques such as style analysis help the analyst to get an idea of the competitor’s investment strategy even if the individual securities in the portfolio are unknown. QEPM approaches to performance measurement analyze performance rigorously and provide a great deal of information and feedback to portfolio managers and investment committees.
Ultimately, investors care about the after-tax returns of their portfolios. Both qualitative and quantitative managers try various
ways to reduce the tax burden. Qualitative managers use some very good rules of thumb, such as selling the oldest tax lots first and selling the tax lots with the lowest gains. They also take futures positions that can be traded in the short term with relatively little tax burden. Quantitative methods incorporate these techniques and also generate many more tax-reduction strategies. Moreover, it is possible to integrate tax considerations directly into a quantitative investment model.
15
With QEPM, the manager can look at the tax effects of a transaction before deciding whether to buy or sell. QEPM also offers a solution to instances in which trades made to reduce the tax burden end up disturbing the balance of stocks in the portfolio. For instance, selling poorly performing stocks at year end to generate capital losses that offset capital gains may make the portfolio less than optimal versus the benchmark or increase its tracking error. A method known as
characteristic matching
can be used to find stocks similar to those that were sold to generate capital losses. Purchasing the matching stocks restores some of the overall characteristics of the portfolio even though some of the original stocks were sold temporarily for tax purposes. Such quantitative tax management strategies protect and often significantly increase after-tax returns.
The financial markets often stray from efficiency. For example, when companies report higher-than-expected earnings, their stocks often earn higher-than-normal returns during the few weeks following the report. Qualitative managers may or may not trade on this sort of market anomaly. If they do—for instance, by purchasing stocks with higher-than-expected earnings announcements—it is often in an ad hoc fashion. QEPM equips quantitative managers to study anomalies in detail and exploit them in a calculated fashion. Quantitative methods help to determine the underlying source of an anomaly, which (if any) time period or industry it is specific to, and the expected excess return of a strategy that centers on it. Quantifying the risks, the gains, and the idiosyncrasies of the anomaly makes for a well-informed trading decision.
Managing a portfolio involves buying and selling stocks repeatedly. Buying and selling generates transactions costs in the form of commissions, price impact, and delay. Studies of equity mutual funds show that most mutual fund managers fail to beat the S&P 500 after accounting for transactions costs.
16
Qualitative
managers typically only consider transactions costs implicitly. Quantitative managers can use optimization algorithms to focus directly on the effect of transactions costs on the portfolio’s return. Now that some commercial research vendors gather detailed data on the costs of trading, including commissions, price impact, and delay, it is possible to determine the effect of the costs on returns quite precisely. Some investment funds also do their own in-house estimates of transactions costs. From either in-house or vendor-provided data, the quantitative manager can find out whether certain transactions are worthwhile and can avoid
churning
, or excessive turnover.
17
Many equity portfolio managers use leverage to increase the returns of their portfolio. The typical way to leverage the portfolio—through index futures such as the S&P 500 futures—achieves levered exposure to the overall market but is not always the optimal route because it dilutes a manager’s excess performance. Qualitative managers, for the most part, ignore the dilution effect and leverage with index futures. QEPM makes it possible to design a plan that does not dilute the performance. Single-stock futures or equity-swap baskets lever the excess returns of the portfolio in addition to its market exposure, thereby multiplying the excess return rather than diminishing it. To the extent that a manager is able to generate excess returns, the quantitative approach to leverage produces better results.
18
The QEPM method of
factor tilting
highlights another difference between qualitative and quantitative approaches. Qualitative managers typically purchase stocks that they believe will outperform, accepting all risks associated with each stock. Although this is not necessarily a bad decision, and quantitative managers sometimes do the same, it is possible, using factor tilting, to calibrate the portfolio’s exposures to different types of risks. Suppose that a manager is very good at forecasting the future value premiums of stocks but very bad at forecasting the other variables that compromise his or her stock-return model. Factor tilting lets the manager create a portfolio with zero exposure, relative to the benchmark, to all variables except the future-value factor. The result is a model that is relatively more exposed to the factor that the manager is fairly capable of forecasting and relatively less exposed to the ones
that he or she cannot forecast well. Factor tilting can be a very effective way of managing an equity portfolio and is one of the many powerful tools of QEPM.
These are only a sample of the types of decisions that might differentiate portfolio managers who use QEPM from those who do not avail themselves of quantitative methods. Clearly, responses to specific investment situations vary from manager to manager. Along the spectrum of management styles, some qualitative managers use quantitative methods frequently, and some quantitative managers draw significantly on qualitative information. As we see it, the more consistently a manager uses quantitative methods, the more consistent and precise are the portfolio’s results. QEPM structures the decision-making process, and it is a structure adaptable to practically all types of investment scenarios.
1.4 A TOUR OF THE BOOK
The field of QEPM is vast, and there are literally thousands of ways to go about building quantitative models to select stocks for a portfolio. In this book we focus on the most prevalent QEPM methods. Our goal is to cover the entire QEPM process, from modeling stock returns, to building the actual portfolio, to assessing the performance of the portfolio.
The book is divided into five parts.
Part I
introduces the concept of quantitative equity portfolio management.
Chapter 2
discusses the fundamental principles of QEPM, as well as the concept of market efficiency and why QEPM works in mostly efficient markets.
Chapter 3
describes the typical QEPM process and introduces the most common models of stock returns.
Part II
of the book is about portfolio construction and maintenance. The first step in building a model of stock returns is to choose a mix of explanatory variables for the model.
Chapter 4
defines the most commonly used factors and provides simple methods for selecting ones for the model. Factors also can be used for preliminary stock screening and ranking.
Chapter 5
explains the basics of stock screening and introduces the aggregate Z-score model, a simple model for ranking stocks. We also describe the investment philosophies of famous portfolio managers and suggest stock screens that emulate their strategies.
Chapters 6
and
7
discuss in detail how to build fundamental and economic factor models, the two types of models that
quantitative managers use to estimate and explain stock returns and volatility.
Chapter 8
discusses how to forecast future factor premiums, which, in the framework of the factor models, can be used to forecast future stock returns and risks. The forecasts are the basis for including or excluding stocks from the portfolio.
Chapter 9
ties together
Chapters 4
through
8
by showing how to use stock-return models and concepts from optimization theory to determine the optimal weights for the stocks in the portfolio while abiding by any investment constraints.
Chapters 10
and
11
discuss refinements to the basic construction and maintenance process.
Chapter 10
explains ways to improve the performance of the portfolio by paying particular attention to transactions costs. Managers can avoid excessively high turnover and high transactions costs by incorporating the costs explicitly into the model of stock returns.
Chapter 11
discusses ways to improve performance by managing the effect of taxes. By taking taxes into account in the model itself, the manager can be clever about the timing and composition of trades.
In
Part III
of the book we step outside the core set of QEPM procedures to explore methods for increasing the portfolio’s performance that are not related to actual stock picking. We refer to these methods collectively as α
mojo
(“alpha mojo”) because they boost α, which is the portion of a portfolio’s returns that goes above and beyond the return of the benchmark or reference portfolio.
Chapter 12
looks at the first form of α mojo, leverage. Leverage is used by many portfolio managers to increase the exposure of the portfolio to the market. The chapter shows various methods for leveraging an equity portfolio to boost its excess returns.
Chapter 13
discusses creation of the market-neutral portfolio. Market-neutral and long-short portfolios are widely used structures for quantitative portfolios, especially among hedge funds. They eliminate or reduce market exposure and increase α, improving the risk-return profile of the portfolio. A market-neutral portfolio is ideal for a quantitative equity portfolio manager who wants to focus on his or her specialty of picking good stocks.
In
Chapter 14
we use some advanced statistical concepts, known collectively as
Bayesian analysis
, to show how a quantitative portfolio manager can take advantage of qualitative insights. We also show how scenario analysis fits into the quantitative stock-return model.
Part IV
of the book brings the portfolio management cycle to its last stage, performance analysis. Though often neglected, the cultivation of an excellent performance measurement department is one of the keys to an investment firm’s success.
Chapter 15
discuses various standard practices, as well as some new concepts related to quantitative performance measurement and attribution.
Part V
implements all the ideas in the first four parts of the book. With an example of the practical application of QEPM, we discuss everything related to building a quantitative portfolio, including data issues, estimation problems, portfolio construction with real data, transactions costs, tax issues, leverage, and performance analysis.
Five appendices can be found online.
19
Appendix A is a history of financial theory for readers who need a quick overview of the subject. Appendix B explains three well-known models of stock returns: the dividend discount model (DDM), the capital asset pricing model (CAPM), and the arbitrage pricing theory (APT) model. Appendix C provides a basic review of mathematical and statistical concepts useful to readers of this book. Appendix D includes a discussion of organizational considerations for investment research departments, followed by a summary of commercial databases and software modeling programs useful for QEPM. Finally, Appendix E looks at the game of craps as an entertaining example of the importance of using quantitative techniques.
1.5 CONCLUSION
Quantitative equity portfolio management (QEPM) is growing in popularity among professional portfolio managers. This style of management offers plenty of advantages over traditional qualitative portfolio management. A combination of advanced statistics,
mathematics, and a disciplined approach, QEPM makes it possible to quantify stocks’ expected returns and risks with a good degree of precision, as well as quantify the uncertainty of the forecasts themselves. To begin the book, we described what we see as the major advantages of QEPM over qualitative approaches to asset management, and we gave examples of typical differences between the two styles of management in the face of specific investment decisions. In the rest of the book we will attempt to guide you through the very broad field of QEPM. We will take you step by step through every aspect of the QEPM process, from stock-return forecasting, to portfolio building, to performance measurement.
QUESTIONS
1.1.
Name three advantages of QEPM versus qualitative equity management.
1.2.
Name three disadvantages of QEPM versus qualitative equity management.
1.3.
Name four realistic investment situations in which a quantitative portfolio manager differs from a qualitative portfolio manager in his or her approach.
1.4.
In some ways, a qualitative portfolio manager could never really be an index portfolio manager, whereas a quantitative portfolio manager could be. Explain why.
1.5.
What is factor tilting? What type of portfolio manager engages in it?
1.6.
Fed fund futures are actively traded instruments on the Chicago Board of Trade. The contract is cash settled to the simple average of the daily effective Fed funds rate for the delivery month. Although the daily effective Fed funds rate is not perfectly equal to the Fed funds target rate, it is very close. Market practitioners use the Fed fund futures rate to gauge the market’s assessment that the Fed will change the Fed fund’s rate. Suppose that there will be an FOMC meeting 10 days into the current month. Use the following variables,
i
f
t
as the Fed fund futures rate,
i
pr
e
t
as the target rate prevailing before the FOMC meeting,
i
pos
t
t
as the target rate expected to prevail
after
the FOMC meeting,
p
as the probability of a target rate change,
d
1
as the number of days between previous month end and the FOMC meeting,
d
2
as the number of days between the FOMC meeting at the current month end, and
B
as the number of days
in the month. (
Note
: In practice, the Fed attempts to achieve a certain target rate or target range, but it varies from day to day. For
i
pr
e
t
you can think of it as the midpoint of the previous target range or use the average Fed funds effective rate of the prior month. For
i
pos
t
t
you can use the midpoint of the next jump in the target range [e.g., 25 basis points] or some other value of your choice.)
(a)   Write down a general formula for the probability of an FOMC target-rate change.
(b)   Given that the current target rate is 3.5%, the expected rate after the meeting is 3.75%, the Fed futures implied rate is 3.60%, there are 30 days in the month, and the FOMC meeting will take place on the tenth day of the month, what is the probability implied by the market prices that the Federal Reserve will raise interest rates?
1
In 2021, there were approximately 11,323 stock mutual funds and 3,508 U.S. hedge funds. There were also about 126,457 open-end funds in the world managing $63.1 trillion in assets and 8,042 hedge funds worldwide managing $3.6 trillion. In 2021, there were also approximately 1,974 quantitative hedge funds in the world managing $1.004 trillion.
Source:
Collins et al. (2021) and Hedge Fund Research (
www.hfr.com
).
2
See Liu and Sinha (2021). In addition, over this 20-year period, only 6% of large-cap funds beat the S&P 500, 12% of mid-cap funds beat the S&P 400, and 12% of small-cap funds beat the S&P 600.
3
See “Interview with Peter Lynch,”
https://www.pbs.org/wgbh/pages/frontline/shows/betting/pros/lynch.html
. Warren Buffett is also another well-known qualitative-style manager.
4
See Morgenson (1997).
5
Chapter 14
explains how Bayesian statistics serve as a powerful method for converting qualitative data into quantitative data.
6
In general, QEPM requires a good understanding of statistics. Not using statistical methods appropriately may create a number of problems. Data mining is just one of them. Not accounting for parameter uncertainty and overinterpreting the estimation from a small sample are other serious problems. We discuss some of these issues in
Chapter 2
. Nonetheless, the abuse and misunderstanding of statistics, not QEPM itself, are mainly to be blamed.
7
We discuss the issue of data mining in more detail in
Chapter 2
.
8
We have noticed that data mining occurs with particular frequency in investment departments dominated by office politics.
9
See
Chapter 2
for an explanation of this concept as well.
10
This is not the same as
skid
, a term used in the industry to describe a movement in price that occurs in the time between the recognition of an idea and its implementation in the portfolio. Skid is also a problem for portfolio managers because a price movement may eliminate an investment opportunity.
11
On a lighter note, in Appendix E found at
www.ludwigbc.com
under QEPM Exclusive Content, we also hypothesize about how a quantitative manager and a qualitative manager might differ in their approaches to the game of craps.
12
For more details, the reader is referred to Bieri and Chincarini (2005).
13
We introduce economic factor models in
Chapter 3
and discuss them in greater detail in
Chapter 7
.
14
In Appendix B at
www.ludwigbc.com
under QEPM Exclusive Content, we discuss additional realistic uses of discounted cash-flow models.
15
See
Chapter 11
on tax management.
16
See Bogle (1999).
17
We discuss transactions costs further in
Chapter 10
.
18
For more on leverage, see
Chapter 12
.
19
Go to the website
www.ludwigbc.com
. Once you reach the website, choose Books, then Quantitative Equity Portfolio Management, then QEPM Exclusive Content. The password is qepm2020rig179. You will find a folder with all the solutions to the end-of-chapter questions in the book, a folder with additional appendices for each chapter, a folder with General Appendices (Appendices A–E), a folder with programs and examples written in MATLAB, R, and Stata for learning and for classroom labs, a folder with PowerPoint slides for every chapter, a folder with sample stock data, and a downloadable file of historical factor returns.
