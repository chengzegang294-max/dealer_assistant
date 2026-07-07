# Quantitative Equity Portfolio Management: An Active Approach to Portfolio Construction and Management, Second Edition

- **book_name**: 5073 Quantitative Equity Portfolio Management, Second Ed.
- **main_source**: epub
- **cross_check_source**: none
- **pdf_role**: not_needed
- **split_scope**: chapter file = chapter04

---

CHAPTER 4
Factors and Factor Choice
Not everything that can be counted counts, and not everything that counts can be counted
.
—Albert Einstein
4.1 INTRODUCTION
Factors are the ingredients of quantitative equity portfolio management (QEPM) models. Just as high-quality ingredients make for excellent cuisine, carefully selected factors can, in the right combination, create models for outperformance. Factors come in many varieties: fundamental, technical, economic, and alternative. How does a portfolio manager select the right ones for a model? QEPM tenets 4 and 5 advise the manager to build quantitative models that reflect sound economic theories and persistent, stable patterns. Good factors therefore exhibit relationships with stock returns that not only are stable and persistent but also can be explained by economic theory. As we discussed in
Chapter 2
, the likelihood of finding high-quality factors depends on how one goes about looking for them. Data mining produces factors that appear to be highly correlated with stock returns, but the relationships between those factors and returns are only superficial. The way to find good factors is to apply solid, well-reasoned quantitative techniques to the search. This chapter describes the main types of factors and some methods of choosing them.
4.2 FUNDAMENTAL FACTORS
A
factor
is any variable that can predict stock returns. Perhaps the most obvious influence on stock performance is the financial condition of the firm.
Fundamental
factors describe a firm’s financial condition. The most common fundamental factors are ratios calculated directly from the income statement, balance sheet, and statement of cash flows. Innumerable financial ratios and combinations of financial statement variables potentially could be constructed from the financial statements and used to forecast stock returns. Since many of these possible fundamental factors are correlated with each other, we can boil the list down to some essential ones that every portfolio manager should know.
We group the fundamental factors into seven subcategories: valuation factors, size factors, operational efficiency factors, operating profitability factors, solvency factors, financial risk factors, and corporate activity factors. Valuation factors, such as the price-to-book (P/B) ratio and the price-to-earnings (P/E) ratio, attempt to measure whether stocks are relatively cheap or expensive. Size factors, such as market capitalization, attempt to classify companies by their size and measure whether size has effects on stock return behavior. Operating efficiency factors, such as inventory turnover, and operating profitability factors, such as gross profit margin, tell us how well management is running the company. Solvency factors attempt to measure a company’s ability to meet future short-term obligations. Indicators in this subcategory include the current ratio and the cash ratio. Financial risk factors measure financial health in ratios such as debt-to-equity and interest coverage. Finally, corporate activity measures factors that are related to corporate executive decisions or do not necessarily fall into any of the other categories. Tables 4A.1 through 4A.7 in
Appendix 4A
provide complete lists of the fundamental factors for QEPM models.
4.2.1 Valuation Factors
Table 4.1
shows the values of popular valuation factors for selected stocks. Legions of managers have based investment strategies on the P/E ratio, and, as we saw in
Chapter 2
, many studies have documented a P/E ratio effect.
1
Low P/E ratio stocks tend to
outperform high P/E ratio stocks on a risk-adjusted basis.
2
One possible explanation for this effect is that the market generally overreacts to bad news, leaving the prices of some stocks excessively deflated. Portfolio managers can purchase the “unpopular” stocks at bargain prices and eventually earn outsized returns as the rest of the market realizes that the stocks are underpriced. Since the P/E ratio is such a popular factor, it is important not to fall into the trap of including it in a model by default. There always should be a clear reason for including it based on sound economic theory. When considering P/E ratio or any other factor to add to a model, it is also important to anticipate how it will fit with the rest of the factors in the model.
TABLE 4.1
Valuation Factors for the Top 10 Standard and Poor’s (S&P) 500 Companies
The P/E ratios of the companies listed in
Table 4.1
vary substantially. Tesla, one of the world’s leading electric auto companies, carries a P/E ratio of approximately 1,203, whereas megabank J.P. Morgan has a mere 15.18 P/E ratio.
3
This quick cross-industry comparison does not tell us the whole story, though. A company’s P/E ratio—and other financial metrics—needs to be viewed in the context of the company’s industry. In 2020, J.P. Morgan’s P/E ratio was roughly in line with a banking-industry multiple of about 17 times. Tesla’s P/E ratio of 1,203, on the other hand, was very high compared with the automobile industry’s average of about 317. Sometimes, though, a stock’s P/E ratio may exceed the overall market P/E ratio but fall a bit below its industry’s average P/E ratio. PayPal, the digital payment company, provides a prime example of undervaluation within its industry. Paypal’s P/E ratio of 87 (as of December 2020) is above the current 78.70 P/E ratio of the S&P 500.
Yet PayPal falls short of the average P/E ratio of 274 that the information technology sector commands as a whole.
Dividend yield (DY), P/B ratio, price-to-sales (P/S) ratio, price-to-cash-flow (P/CF) ratio, and price-to-EBITDA (P/EBITDA) ratio all attempt to capture the value of a stock. These variables are highly correlated with each other, so a manager can pick one according to his or her preference.
4
Some portfolio managers prefer to use P/B ratio rather than P/E ratio because P/E ratio cannot be calculated for firms with negative earnings.
5
Some portfolio managers also prefer the P/B ratio because of its prevalence in academic studies. Some quantitative portfolio managers instead use the P/CF ratio because they view cash-flow measures as less susceptible to manipulation by a company’s management. All these ratios have been linked to the same trend, though. It has been documented that companies with high dividend yields and low P/B, P/S, P/CF, and P/EBITDA ratios tend to outperform stocks for which the reverse is true. There are many potential explanations for this trend. One explanation is that stocks with low values of these variables have experienced a serious price decline, which could lead many investors to shy away from them or demand a higher risk premium for holding them.
Stocks with high P/B ratios generally are referred to as
growth stocks
, and stocks with low P/B ratios are referred to as
value stocks
. In 2020, retail behemoth Walmart (WMT) had a P/B ratio of 5.42, whereas technology giant Apple had a P/B ratio of 34.53. Judging from the P/B ratios, Apple is more of a growth stock and Walmart more of a value play. As with the P/E ratio, though, we need to put the stocks in industry context to get the full story. In comparison with the 2020 retailing industry P/B ratio of about 13.21 or the subindustry of general merchandise stores’ P/B ratio of 5.92, Walmart is undervalued. On the other hand, if a P/B ratio is too low, it could be evidence that management has failed to generate sufficient returns to its shareholders and that the stock price has slid in response. P/S and P/CF ratios reveal similar information and also may help to expose incidences of manipulation of earnings because sales and cash-flow numbers are generally
more transparent than book values. While Walmart’s P/B ratio was well below Apple’s P/B ratio, its P/CF ratio, at 12.35, was closer to Apple’s 27.96 P/CF ratio.
The price-to-earnings-to-growth (PEG) ratio is another valuation measure typically used to identify good growth companies. The idea behind the PEG ratio is that a high P/E ratio is justified if a company’s earnings are expected to grow a lot in the next few years. From the P/E ratio alone, a stock might appear overvalued, but if the stock has a low PEG ratio, the high P/E ratio could be reasonable given the company’s expected earnings growth. Consider data on Microsoft (MSFT), one of the world’s leaders in software and technology, and the giant drug manufacturer Johnson & Johnson (JNJ). In 2020, Microsoft had a P/E ratio of 35, and Johnson & Johnson had a P/E ratio of about 24. From the P/E ratios, we might hasten to conclude that Johnson & Johnson was undervalued relative to Microsoft. However, as of December 2020, given the median analyst-forecasted earnings-per-share (EPS) growth rates of 14.45% and 4.31% for Microsoft and Johnson & Johnson, respectively, we can calculate the PEG ratio. Microsoft’s PEG ratio is 2.45, and Johnson & Johnson’s is 5.66. Owing to Microsoft’s superior earnings growth outlook, Johnson & Johnson now appears to be slightly overvalued with respect to Microsoft. Microsoft’s greater rate of forecasted earnings growth more than compensates for its higher price multiple. Although we used the stock analysts’ consensus forecasts of earnings growth to compute the PEG ratio, some investors prefer to use historical earnings growth instead since they are unaffected by overly optimistic analyst forecasts.
The P/E ratio can be adjusted one step further by dividing it by the sum of the company’s expected growth rate and its dividend yield. The resulting ratio, the price-to-earnings-to-growth-plus-yield (PEGY) ratio, indicates how attractive the stock’s valuation is, given both its expected growth rate and its dividend yield.
6
For example, Apple and Walmart have PEG ratios that are roughly equivalent at 3.24 and 3.38, respectively. However, when we take into account Apple’s dividend yield of 0.61% and Walmart’s 2.77% yield, we end up with different PEGY ratios of 3.08 and 2.77, respectively. A relatively low PEGY ratio makes Walmart look more attractive than Apple on a pure valuation basis.
The dividend yield also can serve as an invaluable aid in determining a company’s maturity and growth prospects. Stable, mature businesses tend to generate sufficient cash flow and offer relatively high dividend yields. Many of these companies find that they have limited opportunities to undertake highly lucrative growth projects, so they return discretionary cash to shareholders in the form of dividends rather than squandering it on low-return investments. Of the 10 companies in
Table 4.1
, J.P. Morgan Chase and Johnson & Johnson, the two oldest and most mature businesses on the list, have the highest dividend yields, 2.86% and 2.47% respectively. On the opposite end of the spectrum, Amazon, Google, Facebook, and Tesla do not even issue a dividend and instead reinvest all their earnings to fund future growth. Observations of the dividend yield will provide insights into a company’s prospects for growth, whether organic or through mergers and acquisitions.
4.2.2 Size Factors
Table 4.2
shows the values of size factors for selected stocks. The market capitalization of a company, which is usually called its
size
, is another popular fundamental factor. It has been documented that small-cap stocks outperform large-cap stocks in the long run.
Although this may not be the case during a single investment period, there are several reasons why it might occur over the long term. Some people believe small-cap companies pose greater risks than large, established companies and that they therefore merit an additional risk premium. The information story is that small-cap stocks receive less analyst coverage or less attention in general, so it takes longer for information about them to diffuse through the market. Ambiguity aversion might also explain why investors require a risk premium on small-cap companies, which tend not to be household names. Other size factors include the common equity of a firm and the total assets of a firm.
TABLE 4.2
Size Factors for the Top 10 S&P 500 Companies
4.2.3 Operating Efficiency Factors
In
Table 4.3
we list the values of popular operating efficiency factors for selected stocks. Operating efficiency factors attempt to describe how efficiently a firm operates over both the short and the long term. An analysis of short-term efficiency would involve the inventory turnover (IT) ratio. The IT ratio is the cost of goods sold divided by average inventory, which represents the rate at which products move from inventory to sale. A high IT ratio generally is a good sign that a company’s products are selling at a fast clip.
Accounting standards and inventory conditions affect this ratio, so in making comparisons between companies, it is important to adjust the ratios for accounting discrepancies and to focus on companies in similar industries. For a test of a company’s long-term efficiency, the total asset turnover (TAT) ratio, which is net sales divided by average total assets, attempts to measure how much revenue the company gets out of its assets. A very high ratio suggests that the company is making the most of its assets. Equity turnover (ET) and fixed-asset turnover (FAT) ratios show how well the company converts those particular classes of assets into sales revenue.
TABLE 4.3
Operating Efficiency Factors for the Top 10 S&P 500 Companies
Although a high IT ratio generally is a good thing, keep in mind that extremely rapid turnover increases the risk of failing to meet customer demand owing to a shortage of inventory on hand. Of course, this is often preferable to an extremely sluggish turnover, which means that the company either cannot sell its products or it ties up too much money by overordering supplies (which will hurt profits). The “normal” turnover for a particular line of business depends on marketplace competition and demands and industry practices and requirements. Taking a look at the consumer staples sector, of which Walmart is considered part, we find an average industry turnover rate of about 6.17 times. Walmart’s IT ratio is about 9.32, so it seems to be selling its products well by the standards of its industry. The trend in turnover also matters as much as the most recent numbers. It is an encouraging sign that Walmart has maintained an average inventory turnover of approximately 8.10 times (also greater than the industry average) since 2016 and has shown an increase in turnover from 8.78 times a year ago. Walmart’s turnover ratio is, by casual observation, strong for its industry and stable, which suggests that the company manages its supply chain well.
7
The ET, FAT, and TAT ratios, like the IT ratio, vary substantially across industries.
Table 4.4
lists the ET, FAT, and TAT ratios of S&P 500 companies in the semiconductor industry. We have calculated the average turnover ratios for the industry as a whole as well. Nvidia’s ET ratio of 1.08 and its TAT ratio of 0.52 are lower than the industry levels of 1.50 and 0.60, respectively. These TAT
ratios of roughly 1.0 or less are relatively normal for capital-intensive industries such as the semiconductor industry. We would expect higher levels of turnover for industries that maintain large levels of inventory and current assets, such as retail. The FAT ratio varies widely among the semiconductor companies as well, with Nvidia operating at 5.58 times turnover, Micron Technology at 0.72, and Applied Materials at nearly 10 times turnover.
TABLE 4.4
Semiconductor Industry in 2020
4.2.4 Operating Profitability Factors
In
Table 4.5
we list the values of popular operating profitability factors for selected stocks. One or more of these operating profitability factors (or transformations of these factors) appears in most
QEPM models. After all, highly profitable companies are the ones to own. All the variables in the table are standard measures of profitability. Quantitative managers look not only for profits but also for some percentage growth in profits. They typically look at year-on-year growth in the gross profit margin (GPM), the operating profit margin (OPM), or the net profit margin (NPM).
8
Other common profitability factors include the return on total capital (ROTC) and the return on common equity (ROCE). Portfolio managers compare these ratios both within and across industries.
TABLE 4.5
Operating Profitability Factors for the Top 10 S&P 500 Companies
Let’s take a look at Microsoft’s profitability factors. Microsoft has a GPM of 76.75%, an OPM of 46.64%, and an NPM of 32.29%. It is always important to examine these three ratios along several dimensions: within an industry, in relation to the market as a whole, and over time. Each dimension will provide different insights. At the moment, we shall focus on the trend over time.
Table 4.6
shows that Microsoft had a very high GPM of 77% in 2020 and that the margin has been increasing since 2016. The OPM simultaneously had risen from about 34% in 2016 to 47% in 2020. The 14% increase in OPM is larger than the 7% increase in GPM. Since operating profit is simply gross profit less sales, general, and administrative expenses, it appears that Microsoft has been able to control sales, general, and administrative expenses somewhat better than the cost of goods sold.
TABLE 4.6
Microsoft Trend Analysis
We can dissect Microsoft’s profitability even further. The ROTC measures the profitability of the company’s overall capital resources, whereas return-on-assets (ROA) and ROCE focus solely on the profitability of those types of resources. (These ratios also should be compared with the ratios of other firms within the industry to measure the capability of management to generate returns.) Microsoft has an ROA of 18.65%, an ROCE of 38.49%, and an ROTC of 27.18%. If these returns were below those of other rates available in the marketplace at a similar level of risk, then it would be better for the company to be broken up and have the assets reinvested where they would be more productive. For Microsoft, not surprisingly, these ratios only confirm that the company enjoys relatively high profitability.
4.2.5 Solvency Factors
In
Table 4.7
we list the values of popular solvency factors for selected stocks. The cash-flow-from-operations ratio (CFOR), the cash ratio (CR), the current ratio (CUR), and the quick ratio (QR)
are all measures of a company’s ability to cover liabilities with varying amounts of liquid cash. Companies with high solvency factor values are more liquid or solvent and less likely to be forced into bankruptcy by payments owed on debt and other liabilities. Many portfolio managers use one or more of these variables as a screen for financially sound stocks.
TABLE 4.7
Solvency Factors for the Top 10 S&P 500 Companies
CUR and QR are very industry sensitive, but a general rule of thumb in assessing these ratios is that the more liquid the current assets are, the less crucial it is that those assets exceed the current liabilities by a wide margin. CUR, which divides current assets by current liabilities, gives a general sense of the company’s liquidity versus its liabilities; QR refines the assessment by narrowing current assets down to cash, marketable securities, and accounts receivable. A high CUR generally indicates adequate short-term liquidity, but it should be examined alongside other ratios such as the inventory turnover (IT) ratio and return on assets (ROA) to ensure that there is not an inefficient use of cash or other marketable equivalents. Large inventories inflate CUR but may be a sign that the company’s products are not selling and are even becoming obsolete. QR is a better measure of liquidity in relation to liabilities for companies that rely on large inventories.
Microsoft’s CUR of 2.53 and QR of 2.30 contain several important facts about the company’s liquidity situation. Microsoft is
adequately funded on a short-term basis. The QR is only slightly less than the CUR as a result of excluding inventories from current assets, which indicates that the bulk of Microsoft’s current assets are in the form of cash and marketable securities rather than shelf upon shelf of inventory. By contrast, Walmart has a CUR of 0.79 and a QR of 0.27. The significant difference, percentagewise, between CUR and QR reveals that most of Walmart’s current assets are tied up in inventory, and the company may be suffering from inadequate liquidity. Although QR by itself raises a red flag, we should analyze other factors in conjunction with this, such as Walmart’s debt-to-equity and profitability ratios, which we also discuss in this chapter.
4.4.6 Financial Risk Factors
Table 4.8
lists the values of popular financial risk factors for selected stocks.
9
By controlling for signs of financial risk, portfolio managers can identify which companies are not well equipped to weather
the storm if sales temporarily slow down or if the economy hits a slump. A company with a high level debt-to-equity (D/E) ratio relative to other companies is more susceptible to bankruptcy even if its core business is solid. A high D/E ratio in conjunction with a low interest coverage ratio (ICR), which equals earnings before interest and taxes over interest expense, is cause for further concern because it means that the firm’s current earnings will not cover many interest payments.
TABLE 4.8
Financial Risk Factors for the Top 10 S&P 500 Companies
A high D/E ratio alone does not automatically spell financial danger. Higher levels of debt generally lead to greater earnings volatility and a higher risk of financial distress or possibly bankruptcy. However, businesses that generate large, stable cash flows can handle relatively large amounts of debt because they can finance the interest payments on the debt. They are therefore more likely to have higher D/E ratio values than companies that are short on cash. In 2020, Apple’s D/E ratio equaled 3.96, compared with an industry average D/E ratio of 3.34. Apple’s capital structure included a greater-than-average portion of debt, but its interest coverage of 23.35 times was also greater than the industry average. Its earning power covered its debt burden.
The best possible position to be in is to have little debt and plenty of cash on hand to cover the interest payments on it. Google’s D/E ratio is a mere 0.41, and its interest coverage ratio is 127 times. The fact that the company is capable of taking on much more debt gives it room to start new projects. Low financial risk does not just avert disaster; it is a big plus for expansion and new investment.
4.2.7 Corporate Activity Factors
The final category of fundamental factors is a category that concerns corporate activity like stock buybacks, insider purchases, and decisions on research and development (R&D) expenditure, as well as other factors that do not neatly fit in the other factor categories. Although stock buybacks are public information, quantitative portfolio managers sift through the data better than the average investor, and this ability is an informational advantage that creates near-arbitrage opportunities. Stock buybacks could reveal that management is upbeat about the future of the company. Some people refer to the shareholder yield as dividends plus net buybacks of stocks. Buybacks have the additional advantage that
they are not taxed as much as dividends. Insider purchases could also represent good news about a stock that is not yet public or could simply reflect management’s confidence in the company. Either way, studies have shown positive excess returns from stocks experiencing insider purchases and lower returns for stocks experiencing insider selling.
10
R&D expenditures reveal that management is actively betting on the future, which could be an indication of beneficial corporate activity.
4.3 TECHNICAL FACTORS
Most technical factors are constructed from past price and volume data (usually, open prices, high prices, low prices, closing prices, volume, open interest, and bid and ask prices) and other readily available financial information. One of the great advantages of technical factors is that they constantly update themselves. New fundamental data are available only quarterly at most, when a company files its financial statements with the Securities and Exchange Commission (SEC). Up-to-date technical indicators, on the other hand, are available as often as every few seconds—although most portfolio managers are happy with daily or monthly technical data. Portfolio managers typically use technical factors to capture very short-term changes in the relative value of stocks.
We group the technical factors into four subcategories: liquidity risk factors, price-based factors, volume-based factors, and overall market movement factors. Liquidity risk factors are used to understand the consequences and effects of trading a stock. Price-based factors are factors that are generated mainly from stock prices or stock returns and are used as indicators of potential future price movements in the stocks. Volume-based factors are generated principally from information in past trading or volume that might signal the intentions and changing behavior of market participants. Overall market movement factors are aggregate technical indicators that might help decipher overall stock market movements and their implications for the near future. Tables 4A.8 through 4A.11 in
Appendix 4A
provide complete lists of some of the most important technical factors for QEPM models.
11
4.3.1 Liquidity Risk Factors
Table 4.9
shows the values of some important liquidity factors—trading turnover (TT), Amihud illiquidity, and invariance illiquidity—for selected stocks. Liquidity factors gauge whether a stock’s liquidity matches trading demand. One of the easiest and most common liquidity factors is TT. TT, which is calculated as the average daily dollar trading volume (ADDTV) divided by market capitalization, measures the percentage of outstanding shares traded in a day on average. It gives an indication of how easy or difficult it is to trade the stock. Other proxies for liquidity include market capitalization and float capitalization, the portion of the market capitalization available for public trading. Floating shares and total shares traded are typically highly correlated, but some stocks have a very small float. The number of shareholders also indicates the ease with which an investor can enter and exit a
position in a stock.
12
Amihud illiquidity (AILIQ) is a measure of illiquidity based on the ratio of the daily return of the stock to the daily volume. The idea is that the higher the daily return for a given volume, the less liquid is the stock due to price impact. A more recently discovered measure of liquidity, or lack thereof, is invariance illiquidity (INVIL), which measures illiquidity based on a theoretical model. This measure is related to the average dollar volume of the stock and its volatility. As we can see from the table, TT, AILIQ, and INVIL vary even among relatively large, well-known stocks. In 2020, Amazon’s measured trading turnover was 0.87% compared to Walmart’s 0.24%. This says that Amazon is more liquid than Walmart in that much more trading occurs given Amazon’s market capitalization. More precisely, on average, about 1% of Amazon’s shares are being traded daily compared to one quarter of 1% for Walmart’s shares. Similar conclusions are drawn by using Amihud illiquidity and invariance illiquidity. For these measures, higher values mean that the stock is less liquid. Amazon’s AILIQ value is 0.13 compared to Walmart’s 1, suggesting Walmart is even less liquid than was implied by TT. Finally, Amazon’s INVIL is 0.76 compared to Walmart’s 1.49. Thus, all of these measures suggest, to varying degrees, that Amazon stock is more liquid that Walmart’s stock. Generally, these liquidity factors are correlated with each other.
TABLE 4.9
Selected Technical Liquidity Measures for the Top 10 S&P 500 Companies
All these liquidity factors matter only in relation to the size of the manager’s portfolio and the value of the trades he or she wants to place. Trading liquidity mainly becomes a concern when a manager wants to buy more than the available number of shares or sell more than the market will take. Some portfolio managers build liquidity factors into portfolio models as transactions costs, whereas others leave it to the trading desk to sort out the costs of the trades in light of liquidity constraints.
4.3.2 Price-Based Factors
Table 4.10
shows the values of some prevalent price-based factors for selected stocks.
13
These factors attempt to capture short-term movements in stock prices or measures related to stock prices that might indicate something about future stock returns.
Momentum is a very popular short-term indicator of future performance. Various academic studies have found positive auto-correlation in stock returns, meaning that positive returns in one period tend to lead to positive returns in the next period.
14
There is also evidence of negative autocorrelation in individual stock returns over periods of one week and one month.
15
Some portfolio managers measure momentum as the stock return over the last year, some measure it as the stock return over the last month, and others use more complicated variations. The same idea prevails: stocks that have performed well recently tend to continue performing well in the near future. You might argue that momentum cannot last because no stock can continue to rise forever. The technician would tell you that a positive stock return in the last period contains useful information that may not be fully distributed throughout the investing population. It could represent insider buying by company executives who anticipate profit growth, or it could represent buying by some knowledgeable investors who have deduced some as yet unreleased piece of good news that will help the stock in the near future. Tesla’s momentum (i.e., stock return for 2020) was 743%, while J.P. Morgan’s was −5.5%. To the extent that momentum works, it would tell you to buy stocks like Tesla, Apple, Amazon, and Google and avoid the smaller-momentum stocks.
TABLE 4.10
Selected Technical Price-Based Factors for the Top 10 S&P 500 Companies
Portfolio managers use various moving averages to capture information traveling through a stock’s price. The relative strength index is a popular indicator that attempts to pinpoint when a stock is a buy and when it is a sell. Bollinger bands, which delineate limits around the mean price for buying and selling, improve on simple moving-average models. When a stock hits the top band above the mean, it is a signal to sell; when it hits the bottom band below the mean, it is a signal to buy. Both moving averages and Bollinger bands may be useful for identifying short-term changes in the relative attractiveness of stocks. At the end of 2020, the Bollinger band signals for Apple and Microsoft are 1.00, meaning that there is positive movement in these stocks and they are a buy, while the signal is neutral on stocks like Google and Facebook and bearish on Walmart.
16
Beta is not conventionally thought of as a technical factor, since it’s based on the capital asset pricing model (CAPM) of finance. Beta is also different from other factors in that each stock’s beta exposure is estimated by a regression. Nevertheless, research dating back to the early 1970s shows that beta might be useful in predicting future stock returns. In fact, in recent years, this strategy has become so popular, it’s part of many QEPM portfolio models and tailored investment strategies for retail investors.
17
Contrary to theory, people have found that low-beta stocks have higher risk-adjusted returns than high-beta stocks. As of December 2020, the beta of Apple was 1.28, while the beta of Johnson & Johnson was 0.70. Theory would predict that Johnson & Johnson would be less volatile in relation to the stock market than Apple. However, recent empirical evidence might indicate that a portfolio of low-beta stocks will outperform a portfolio of high-beta stocks on a risk-adjusted basis.
4.3.3 Volume-Based Factors
Table 4.11
shows the values of a very important factor—the short interest ratio—for selected stocks.
18
Some people use a high degree of short interest as a contrarian signal. That is, when many
investors are shorting a stock, if the stock continues to rise due to buying pressure, it may force the very investors who shorted the stock to buy it back—causing the stock to rally even further. This factor was much in the news in 2021 as many retail traders targeted stocks with large amounts of short interest.
19
Consider data on Walmart, with a relatively small short interest ratio of 2.86%, and Tesla, which has a ratio of 1.97% but whose value declined significantly in 2020. In December 2015, Tesla’s short interest was 64 and in December 2019 it was 23 as people strongly believed the company was overvalued. Since that time, the stock is up 18-fold. Amongst companies in the S&P 500 not in the table, insurance broker AON and specialty chemical company IFF both have short interest ratios around 20%.
TABLE 4.11
Selected Technical Volume-Based Factors for the Top 10 S&P 500 Companies
4.3.4 Overall Market Movement Factors
Table 4A.11
lists the technical factors that are not computed for individual stocks but are rather computed for the overall market and are usually indicators of where the overall market is headed.
These are appropriately called
overall market movement factors
. In order to compute the exposures of individual stocks, you must estimate regressions of individual stock returns on these market-wide factors. In
Chapters 16
and
17
we actually compute these factors and their returns.
4.4 ECONOMIC FACTORS
The first arbitrage pricing models were based on economic indicators, and the popularity of economic factors endures in QEPM models.
20
Table 4A.12
gives a list of the most common economic factors used in QEPM models.
For macroeconomic models of stock returns, the portfolio manager should choose factors that affect all stock returns to some degree. GDP growth, the yield-curve slope, unemployment, and inflation are popular factors because they influence almost every corner of the market. Although each of these variables can be defined in different ways, there are some standard definitions. A common way of calculating inflation, for instance, is to take the latest monthly inflation number and annualize it. Quantitative managers must be careful to use the right data when calculating macroeconomic figures. There are significant delays between the measurement and release of macroeconomic data. The most current monthly inflation data are usually data on the conditions one month prior. Other macro variables are reported at different delays. The portfolio manager should create a table of data release months and adjust models to account for the lag in information.
21
4.5 ALTERNATIVE FACTORS
We group the remaining factors into a category called
alternative factors
for lack of a better name. There are three subcategories of alternative factors: analyst factors, captivus factors, and social responsibility factors. Tables 4A.13 and 4A.14 in
Appendix 4A
list the most common alternative factors used in QEPM models.
4.5.1 Analyst Factors
Analysts on Wall Street and elsewhere spend a lot of time researching individual companies. Wall Street analysts’ earnings forecasts, buy–sell recommendations, and related information can be valuable in forecasting stock returns.
22
There have been hundreds of studies documenting the success of analyst recommendations in predicting stock returns.
23
The beauty of an analyst recommendation is that it condenses hours and hours of research into a single directive, buy or sell. A portfolio manager can transform recommendations into factors that work in a quantitative model.
Some studies show that a portfolio of analyst-rated “strong buys” outperforms a portfolio of analyst-rated “strong sells.” Since the analyst recommendations are public information, one might wonder how portfolio managers could use them for statistical arbitrage. One argument is that quantitative managers have an advantage in filtering the vast amount of analyst data for useful recommendations. In mere seconds they can access newly released analyst ratings and use software to create or update a portfolio of the top-rated stocks. The average investor may not hear about ratings changes until the end of the trading day, and even then he or she probably does not own the kind of software that can quickly sort through hundreds of ratings.
24
A strategy of purchasing stocks that have been upgraded by analysts in the last month has been shown to outperform on a risk-adjusted basis. Similarly, selling downgraded stocks outperforms on a risk-adjusted basis. One would expect even better results from a strategy of shorting the firms that were downgraded by analysts of their own underwriter. Other analyst-related strategies seem to produce strong returns as well. It also has been documented that purchasing a group of stocks with recent upward earnings revisions by analysts outperforms on a risk-adjusted basis. The degree of dispersion in analyst ratings also may create opportunities to outperform.
Table 4.12
shows the values of several analyst factors for selected stocks, including the median recommendation, the percentage of buy and sell recommendations for each stock, and the standard deviation of the analyst ratings. Analyst recommendations are
given as numbers from 1 to 5, such that 1 is for “strong buy,” 2 is for “buy,” 3 is for “hold” or “neutral,” 4 is for “sell,” and 5 is for “strong sell.” Tesla has the lowest median analyst rating at 3 (i.e., neither a buy nor a sell, but a hold). The highest median rating of a buy (i.e., 2) is shared by many companies. The most bullish sentiment from analysts is for Amazon, with 94% of analysts suggesting a buy or strong buy. The most bearish sentiment is for Tesla, with 37% of analysts recommending a buy or strong buy and 31% recommending a sell or strong sell. Finally, the greatest disagreement amongst analysts concerns Tesla and Berkshire Hathaway, judging by the standard deviation of analyst ratings.
TABLE 4.12
Selected Analyst Factors for the Top 10 S&P 500 Companies
If analyst coverage provides useful information for models of stock return, what should be done about stocks that receive little or no analyst coverage? For example, Amazon has about 40 analysts researching the company, Tesla has about 15, but at the bottom of the S&P 500 there are companies with no analyst coverage or just a few, such as one analyst for Under Armour and three for NRG Energy. Lack of analyst coverage may in fact be an advantage unto itself. There is a neglected-firm effect in which stocks followed by few analysts or owned by few institutions tend to have relatively higher long-run risk-adjusted returns than heavily covered stocks. There could be an informational story for this effect. If it takes time for good information to seep through the marketplace, then information about a stock that is not covered will spread more slowly than information that is publicized by analyst comments and recommendations. When there is good news about a neglected stock, the stock’s price adjusts to the news more slowly than a well-known stock’s price would, which gives investors more time to buy before the gain. The neglected-firm effect suggests a strategy of purchasing neglected firms on good news and selling them on bad news. In reality, many quants look for good neglected stocks using a multifactor model that examines fundamental characteristics and assigns a bonus point to neglected status. Given two stocks with identical fundamentals, the model would rate the neglected one more highly than the well-known one.
4.5.2 Captivus Factors
With the advent of the internet and the explosion of technology into everyday life in the form of personal computers, smart phones, satellites, cameras, and social networks, everyone from police to investors has realized that capturing this information can be very valuable. As of 2020, about 45% of asset managers use some form of captivus data.
25
This type of data is often called
alternative data
or
big data
, but we prefer to call it
captivus
data,
which is the Latin word for “captured.” Whether it’s GPS or satellite data, social media data, or news feeds, the data are essentially captured by sophisticated programs. Some of the data is collected by specialized companies for resale and some is captured by portfolio managers for proprietary usage. One of the benefits of captivus data over other data used in QEPM is their usually higher frequency: captivus data are obtained earlier than typical fundamental data. Another advantage is that captivus data usually supplement or are complementary to more traditional data sources. The most popular method of obtaining captivus data is through
web scraping
. Web scraping is the process of locating web pages and extracting data from them, whether they are company sites, consumer sites, or social media sites. For example, a program that captures the posts of a group of Twitter and Instagram users and stores the data is web scraping. This data set is already large and growing. As of 2019, there were 5.5 billion mobile users worldwide, 4 billion internet users, and 3 billion users on social networks.
Since there is such a vast array of captivus data and these data are typically either proprietary to an institution or very expensive to purchase, we do not use them in this book directly. However, any serious investor could purchase the data from existing providers or hire a team to scrape the data themselves.
26
We can, however, provide some examples of how the data might be used. When attempting to predict the sales of a business in advance of earnings releases, you might use geolocation, foot traffic, and app usage data to predict the number of customers frequenting a particular store or stores. For example, as the 2020 Covid-19 pandemic unfolded, data on foot traffic from mobile phones and geolocation could be used to understand which cities were rebounding and which were not. For those interested in workout companies, you might use Instagram and Twitter posts to model trends in buying home workout equipment and other personal trends that are related to public companies. For earnings calls, rather than read and/or listen to every transcript, you could use machine learning and textual analysis to determine if there are any key language patterns that might be undetectable to the average person that hint at potential future company health. You might use data on air traffic and other transportation resources to
gauge the behavior of economies long before the actual GDP numbers are released.
27
And, of course, consumer trends can be analyzed for a host of retail companies through web traffic, Google Trends, and social media applications.
Captivus data are more varied than traditional data and are oftentimes expensive and more difficult to obtain. However, captivus data can offer many advantages to the quantitative manager, including higher frequency of information, earlier understanding of important metrics for a company, and significantly more accurate information for understanding a specific issue. Captivus data will continue to be an important part of the QEPM data tool kit in the future.
4.5.3 Social Responsibility Factors
Many investors believe that in order to maximize the return on their portfolios, they must separate financial decisions from social concerns. Some socially responsible business practices may in fact do nothing for a company’s bottom line over the short term. Yet, contrary to the view that socially responsible investing necessarily sacrifices profits in the name of doing good, many studies show
that factoring social concerns into investment decisions does not reduce the return of a portfolio.
28
Regardless of one’s philosophical stance on socially responsible investing, data on what we might call “social responsibility” factors may offer useful information for portfolio managers.
29
Probably the most useful factor in this arena is the employee relations factor. Quantifying the state of management’s relations with employees is admittedly not as straightforward as calculating the P/E ratio, and the quality of the measurement will affect the model.
30
This factor adds depth to a strictly financial model, though, because it contains information that may not be obvious from the most recent financials and yet may indicate a burgeoning operational problem (or, conversely, the seed of a future competitive advantage).
Table 4.13
shows the values of some prevalent socially responsible, or ESG, factors for selected stocks. For each category, we measure each company’s percentage of strengths in that category minus their percentage of weaknesses.
31
Many of the companies on the list are weak on corporate governance, which includes items such as exposure to bribery and fraud, controversial investment practices, and governance structure issues. Diversity includes elements such as the diversity of the board and discrimination practices. On the extreme positive side is Microsoft, with a 100% net positive reading, and on the negative side is Amazon with a −50% reading. Employee relations covers areas such as the health and safety of the workforce, as well as whether or not the firm engages in profit sharing with employees and human capital development and growth. By this score, Johnson & Johnson is on the positive side with a score of 44%, and Tesla is on the negative with a score of −22%. As for the environment and human rights, most firms are neutral to positive. QEPM’s ultimate goal is portfolio outperformance. Thus, QEPM should focus on using these factors to find signals of future good and bad stock performance. Some readers
might be skeptical about the validity of certain social responsibility variables, but they may help capture aspects of investor sentiment not captured by other variables. Therefore, we list them in
Table 4A.14
for those interested in this area of analysis.
32
TABLE 4.13
Selected Socially Responsible Factors for the Top 10 S&P 500 Companies
4.6 FACTOR CHOICE
Earlier in this chapter we compared QEPM factors with cooking ingredients. Building an investment model, like creating a meal, is a mix of science and art, and many managers build models very intuitively, adding factors according to taste. When it comes to building most quantitative models, though, the cooking comparison only goes so far. The chef may not need to know chemistry, but the quantitative portfolio manager must understand financial and economic theory in order to choose and combine factors appropriately, always keeping in mind the seven tenets of QEPM.
33
The manager has to ask himself or herself why the market has not already identified the arbitrage opportunity that he or she sees. He or she needs to consider whether factors that worked in backtests using historical data will continue to work in the future. In this section we suggest several techniques of factor choice supported by theory. As we discussed in
Chapter 3
, there are two basic types of
quantitative stock return models: the fundamental factor model and the economic factor model. To choose factors for the fundamental factor model, we suggest using the univariate and multiple regression techniques. To choose factors for the economic factor model, we suggest using the unidimensional and multidimensional zero-investment portfolio techniques.
34
In addition to these techniques, we also suggest using a simple correlation statistic or Kendall’s rank-correlation statistic to determine the correlation among factor choices. These techniques aid in combining and grouping factors.
4.6.1 Univariate Regression Tests
Many portfolio managers simplify the process of searching for relevant factors by performing a series of simple regressions of factors.
35
That is, they begin by first identifying a group of factors that they can theoretically justify explaining stock returns. They then run panel regressions on each factor versus the stock returns in the universe. Thus
where
β
i,t
is the factor exposure of stock
i
at time
t
, and the estimate of
f
from this panel regression will show the relationship between the factor and stock returns. If a factor has a significant value of
f
, then the factor is useful in explaining stock returns.
36
The drawback of univariate regressions is that the portfolio manager may find many variables that are significant in explaining stock returns but are surrogates for each other. For instance, he or she may find that both the P/E and P/B ratios explain stock returns but that they represent the same idea. Thus, only one of them may be needed in the model. Ideally, one would like to find factors that help in explaining stock returns but are not highly correlated with
each other. In terms of the fundamental law discussed in
Chapter 2
, we know that the more factors that we find to explain stock returns, the higher will be our information ratio,
provided
that the average contribution of each factor
does not decrease
. Thus, if we add a factor that is highly correlated with an existing factor, we probably will decrease the contribution of each factor, which will not improve the model. In that case, why use simple regressions for factor searching at all? First, they are very simple to perform. Second, they are a way to get an early idea of what might be relevant and what might not be relevant. If there are too many potential factors, the simple regression can be used to make the first round of cuts.
4.6.2 Multiple Regression Tests
The multiple regression is more sophisticated for determining which factors to include because it considers the relationship among factors while estimating the impact on return. The greatest danger with this method is that if the portfolio manager includes too many factors in the regression, there is a chance of
misspecification bias
, which leads to misleading statistical inference.
If the portfolio manager has limited the number of explanatory factors to something reasonable, say, fewer than 10 factors, then a multivariate panel regression can be estimated, that is,
where
K
is the number of factors to investigate, and
β
i,k,t
is the exposure for stock
i
to factor
k
at time
t
. Once this regression is estimated, all insignificant factors are dropped. The significant factors go into the factor model.
37
One of the biggest dangers here is data mining, of course. Data mining is the process of taking historical data on stock returns and factors and testing a variety of models until the portfolio manager finds the model that best predicts or explains past stock returns. There are many ways to do data mining, and we discourage all of them for two reasons. First, by searching in a set of historical data for the factors that best explain stock returns, the portfolio manager is guaranteed to find a group of factors that would have worked historically, but this provides absolutely no guarantee that these factors
will work in the future. The
t
-statistics or significance of these factors historically also is misleading because the manager did not take into account every factor he or she tested. If these were taken into account, the actual
t
-statistics would be much lower (see
Chapter 2
for more details on problems related to data mining). Second, by only finding the factors that explain stock returns statistically in the past, the portfolio manager has clearly failed to provide any theoretical explanation of why those factors were chosen. This is very bad practice for any serious quantitative portfolio manager. Data mining can be a serious problem when one uses the
stepwise regression
technique.
38
This method involves starting with a collection of factors and then running a regression on every possible combination of the factors and picking the set of factors with the largest
. It’s dangerous because, by searching for the best fit in a set of historical data, one might find a model that fits the past data very well but has no bearing on the underlying stock return generation and has a high likelihood of failing in predicting future stock returns.
A related technique is the sequential specification search. The portfolio manager begins with a list of factors that he believes explains stock returns, and, for this set of factors, he looks at the estimated coefficients. He may then decide to drop one factor because of insignificance and add another factor based on theory. The manager may do this a few times until he obtains a desired level of significance at explaining stock returns. This also leads to exaggerated statistical significance. Usually, the portfolio manager will not report the failed model attempts, which makes it very difficult for the investment committee to evaluate the truth or significance of the final stock return model.
The best advice for choosing factors is to begin with a strong explanation, grounded in theory, of why a model with certain factors will work. A manager might even start with a few potential models. She then should test the models on the data but be wary of adding and dropping variables. She should test the model over a variety of time periods for model robustness.
4.6.3 Unidimensional Zero-Investment Portfolio
Portfolio managers may construct zero-investment portfolios based on a factor and study the characteristics of the portfolio. Typically, a manager will split the universe of stocks conditional on a particular factor exposure into thirds, quintiles, or deciles. Of course, any other division of the stocks is acceptable. Usually, a portfolio is created from the first division, and another portfolio is created from the last division. The returns of the top division are
subtracted from those of the last division. These are the returns to a hypothetical zero-investment portfolio in which the top-division portfolio is bought and the last-division portfolio is shorted. It is called
zero investment
because, theoretically, no capital needs to be used to create the portfolio. The returns of this portfolio measure the benefits from using this factor to pick stocks.
We shall do an example with quintiles. Suppose that the factor of interest is the P/B ratio. The first task is to rank the universe of stocks by their P/B ratio exposure in each historical period. There are a variety of methods to do this. The stocks can be ranked monthly, quarterly, or yearly. The stocks should be ranked for every month for some historical period, say, 5 to 10 years of historical data to the present. The next step is to create an equal-weighted portfolio of stocks in the first quintile and an equal-weighted portfolio of stocks in the fifth quintile. The first quintile is just the 20% of stocks ranked highest according to the factor, which in this case is the P/B ratio. The fifth quintile is the bottom 20% of stocks ranked according to the P/B ratio. The next step is to compute the returns of the two portfolios for each monthly period. Of course, these portfolios will change over time on a monthly, quarterly, or yearly basis depending on the QEPM’s choice of rebalancing period. The final step is to calculate statistics on the historical returns of the first-quintile portfolio minus the fifth-quintile portfolio. This procedure should be repeated for every factor that the manager is interested in using as a predictor of stock returns.
39
After the zero-investment portfolio returns have been calculated, one can do a statistical test of whether the average portfolio return is significantly different from zero. Suppose that we calculated portfolio returns for
T
periods and obtained
r
1
, …,
r
T
. Then the
t
statistics can be calculated as follows:
where
is the sample average, i.e.,
, and
is the standard error of the mean. The value of the
t
-statistic should be
compared with the
t
distribution with
T
− 1 degrees of freedom. Although one should look at a
t
-statistics table for the actual critical values of the
t
-statistic to determine significance, a good rule of thumb is that if the absolute value of the
t
-statistic is greater than 2, the average portfolio return is significantly different from zero, and the factor is statistically significant.
40
4.6.4 Multidimensional Zero-Investment Portfolio
Zero-investment portfolios also can be created by considering many factors simultaneously. This approach is more rigorous than the unidimensional approach because we can examine the joint significance of factors. Construction of the zero-investment portfolio proceeds almost in the same way as before. The portfolio manager ranks all stocks by each factor of interest. If there are two factors, say, size and P/B ratio, then each stock will be assigned two rankings, one by size and the other by P/B ratio. Based on these rankings, the portfolio manager can group stocks into a number of joint quintiles or deciles. If the portfolio manager wants to create 10 groups out of each factor, then there will be 100 groups eventually. From the size factor, there will be 10 portfolios starting from the smallest to the largest. From the P/B ratio, there also will be 10 portfolios from the lowest to the highest. By taking intersections of these portfolios, one can obtain 100 portfolios.
Given 100 portfolios, the method to create the zero-investment portfolios depends on what the portfolio manager is interested in. If he or she is interested in whether small size and low P/B ratio together influence stock returns, he or she could create the zero-investment portfolio by taking a long position on a small–low
portfolio and a short position on a large–high portfolio. Once the zero-investment portfolio is constructed,
t
-statistics can be calculated to determine whether the joint effect of the factors is significant, as explained in the preceding subsection.
Alternatively, one may apply a multiple regression analysis. For each of the factors that we consider, we may define an indicator variable that takes the value of 1 if the stock belongs to the top division (e.g., quintile), a value of −1 if the stock belongs to the bottom division, and a value of 0 otherwise. If we run a regression of stock returns on the indicator variables, the estimated coefficients can be interpreted as the returns to suitably constructed zero-investment portfolios. Thus, the significance of the multiple regression can be taken as an indicator of the joint significance of selected factors.
4.6.5 Techniques to Reduce the Number of Factors
There are several methods to determine the correlation among factors. A quantitative portfolio manager could use these methods to determine whether certain factors are highly similar to one another either for the grouping of factors or to aid in reducing the number of factors in one’s stock return model. We discuss two types of statistics here, one based on simple correlation and the other based on rank correlation.
In general, a perfect correlation (i.e., a correlation of 1) indicates that the two factors are almost identical, whereas a correlation of 0 would indicate that the factors are quite independent. In the extreme cases of perfect positive or negative correlation, the two factors are more likely to be redundant. In the in-between cases, the quantitative analyst would have to have a cutoff criterion.
The first statistic we discuss is called the
within-correlation coefficient
. It is the correlation coefficient adjusted for the panel structure of the data. We first subtract the mean from each variable for each period and then calculate the correlation coefficient. The adjustment is necessary to make sure that we are examining the contemporaneous correlation amongst variables. Specifically, given two variables
X
and
Y
, the within-correlation coefficient is calculated as
where
and
are sample covariance and standard deviation, and
and
are the sample means of
X
and
Y
for period
t
, respectively.
The second statistic we discuss is based on Kendall’s
τ
. Kendall’s
τ
shows the rank correlation (i.e., whether the ranking by one variable is related to the ranking by another variable).
Conceptually, Kendall’s
τ
answers the following question: “Suppose that you choose a pair of observations. You rank these two observations based on the value of one variable. Then you rank the observations based on the value of another variable. Then what is the probability that the ranking by one variable is identical to the ranking by another variable?” Thus, if Kendall’s
τ
is 100%, then for every pair of observations, the ranking by one variable is always identical to the ranking by another variable. If Kendall’s
τ
is negative 100%, then for every pair of observations, the rankings by two variables are opposite. If Kendall’s
τ
is 0, half the time the rankings by two variables are the same, and the other half of the time the rankings are opposite.
Kendall’s
τ
needs to be adjusted for the panel structure of the data as well. We calculate the numerator (the number of pairs for which the rankings by two variables are the same minus the number of pairs for which the rankings by two variables are the opposite of each other) and the denominator (the total number of pairs) for each period and then aggregate over time. These techniques can be used to group factors or to reduce the number of significant factors in a model.
41
4.7 CONCLUSION
In this chapter we went through a wide range of factors for QEPM models. Portfolio managers should have a good understanding of why each factor may or may not be helpful in predicting stock returns. As we have reiterated several times, what distinguishes a portfolio manager from the crowd is the combination of factors he or she chooses for stock return models. There is no automatic way to select the best factors. We presented a number of statistical methods to aid the selection process, but they do not substitute for human judgment. Theoretical justification for including a factor in a model is as important as statistical proof. Finally, factor choice sometimes comes down to a matter of preference. Great managers, just like great chefs, often add things “to taste.” In
Chapter 5
we will examine the signature stock screens of some well-known managers who combined factors according to their individual investment styles.
1
See
Table 2.2
.
2
In this chapter, when we characterize a ratio as “high,” we generally mean that it falls within the top quartile or top decile of the investment universe. When we describe a ratio as being “low,” we generally mean that it falls within the bottom quartile or decile of the universe.
3
For those readers who replicate the calculations, some notes about our calculations will help. First, we use quarterly data and lag the data to avoid look-ahead bias, as discussed in
Chapters 6
and
16
. Thus, for December 2020, we use firm financial data from September 2020, with the exception of market data like prices. Second, when we discuss the S&P 500 averages, we remove companies that do not have a share code of 10, 11, or 12 in CRSP. This effectively removes REITs from our S&P 500 index. Thus, our averages might differ from the actual S&P 500. For industry and sector averages, we use the GICS code of the respective industry for only stocks in our S&P 500. Third, it must be remembered that many of the average statistics of the indices are weighted averages by the float-weighted capitalization, which is different than a straight average.
4
In the Practical Application section of this book (Part V; see
Chapters 16
and
17
), we give some idea of the correlation and relationships between many common factors.
5
Some portfolio managers also use the inverse of P/E for evaluating stocks since it allows for the consideration of negative-earnings companies. In footnote 2 of
Chapter 5
we expand on the reasons for choosing the inverse of certain ratios.
6
Another way of calculating this ratio is to divide the PEG ratio by the stock’s dividend yield.
7
The consumer staples sector of the S&P 500 has about 30 companies in it. If one compares Walmart to the smaller industry set of food and staple retailing, which includes companies like Walgreens and Costco, then Walmart’s inventory turnover ratio is slightly lower than the industry average of 11.78.
8
A strand of literature has noticed that while the market may treat all earnings the same, there is a difference between the accrual and cash-flow components of earnings, and it has an impact on future stock returns. In particular, the higher the accrual component of earnings, the lower are the future stock returns. For more information, see Sloan (1996).
9
The work of researchers such as Professor Edward Altman of New York University’s Stern School of Business, who used financial ratios to predict bankruptcies, has encouraged the QEPM community to look closely at financial risk factors. Financial risk factors are closely related to solvency factors. See Altman (2019).
10
See
Table 2.2
.
11
There are thousands of potential technical factors. For good descriptions of many technical indicators and how to use them, we recommend Achelis (2001).
12
This type of data is not easily available.
13
For an expanded list, see
Table 4A.9
and
Chapter 16
.
14
See
Table 2.2
.
15
See Jegadeesh (1990).
16
The reader should remember that many technical signals, like the Bollinger band, can be computed on various time horizons but also that these signals are for the very short term and must be updated frequently. For more details on how we computed this indicator, see the formulas in
Chapter 16
.
17
Also known as the
low-beta strategy
or
betting against beta
.
18
For an expanded list of volume factors, see
Table 4A.10
and
Chapter 16
.
19
In 2021, a group of social network–connected amateur traders made millions targeting high-short-interest stocks to buy, including Gamestop (GME), AMC Entertainment (AMC), and others. As they bought the highly shorted stocks, these stocks soared in price.
20
Arbitrage pricing theory (APT) was invented by the late Stephen Ross of MIT, and his suggested factors include macroeconomic factors such as monthly growth in industrial production, inflation and expected inflation, real interest rates, risk premiums (measured as the spread in returns between Baa bonds and government bonds), and the term structure or difference in returns between long-maturity government bonds and short-term Treasury bills. See Chen, Roll, and Ross (1986).
21
The original arbitrage pricing models assumed that the factor premiums should be unanticipated variables because it is only unanticipated changes that should affect returns. For macroeconomic variables, this usually means constructing derivatives of the variables that are unanticipated or have an average of zero. Most economic variables do not have an average of zero. This does not necessarily create a problem, however. We can simply interpret the economic factors as something that is proportional to the true factor premiums. We also could attempt to construct economic factors that are more like innovations, such as constructing unexpected inflation variables.
22
IBES is the main provider of analyst data, although Bloomberg and other data providers provide similar information. IBES is owned by Refinitiv, which was purchased by the London Stock Exchange Group in 2019.
23
For a list of some of those studies, see
Table 2.2
.
24
StarMine, which is now owned by Refinitiv, has made a name for itself by building models that weight analyst recommendations according to analysts’ historical ability to predict stock returns, taking into account preannouncements and using changes in recommendations to filter the information efficiently. The company finds that its models improve on the basic earnings revision model and have much higher information coefficients than the basic model. For more information, see
https://www.refinitiv.com/en.
25
See Thornton et al. (2020).
26
See Thornton et al. (2020) for a list of some companies that sell these types of data.
27
For example, using FlightRadar24 (
https://www.flightradar24.com/
) or something similar.
28
See Hamilton (1993), Cohen (1995), Diltz (1995), Kurtz and DiBartolomeo (1996), Guerard (1997), Guerard et al. (2002), Derwall et al. (2005), and Whelan et al. (2020).
29
Since the writing of the first edition of this book, new terminology has gained vogue, using the acronym ESG for environmental, social, and governance factors. Incorporating ESG factors is also called
sustainable investing
or
impact investing
. In addition, many more studies on this topic have been written, including Madhavan et al. (2020), Amel-Zadeh and Serafeim (2018), Briere et al. (2017), Pastor et al. (2021), Munoz et al. (2014), Berg et al. (2020), and Ezeokoli et al. (2017). Also, many of the leading investment banks are regularly publishing pieces on ESG, including J.P. Morgan, Sanford Bernstein, Bank of America Merrill Lynch, and others. One must also remember that investors can trade either side of these factors. For example, those who don’t agree with diversity can reduce the number of diversity-proponent companies in their portfolios, while those who agree with diversity can increase the number of these companies in their portfolios.
30
MSCI ESG KLD STATS is a database that classifies companies according to social criteria. The MSCI ESG database provides in-depth profiles of more than 3,000 U.S. corporations, including every company in the S&P 500, most of the Russell 3000, and all of KLD’s Domini 400 Social Index. The profiles present analyses on a range of issues that reflect a company’s overall social record and include social ratings that highlight a company’s strengths and weaknesses. The following issues are covered: community relations, employee and union relations, environmental liabilities, corporate governance, human rights, environmental impact, diversity, product quality and safety, environmental policies and practices, and company involvement in businesses related to abortion, contraceptives, military weapons, adult entertainment, firearms, nuclear power, alcohol, gambling, and tobacco. This database is maintained by MSCI after it bought KLD and its competitor, the Investor Responsibility Research Center (IRRC). There are other providers of social responsibility data, including Bloomberg, Sustainalytics, Vigeo Eiris, RobecoSAM, and Eikon. More information on all of these data providers can be found at
https://www.msci.com/,
https://www.bloomberg.com/,
https://www.sustainalytics.com/,
https://vigeo-eiris.com/
,
https://www.robeco.com/,
and
https://www.refinitiv.com/
, respectively.
31
For more details on the measures, the reader should see
Table 4A.14
and
Chapter 16
.
32
In recent years, it has been popular to consider socially responsible, or ESG, factors regardless of the future returns of stocks. Even when these factors are used in this fashion, the investor must be extremely cautious in interpreting the data. First, many providers of socially responsible data differ on their analyses of the same companies [Berg et al. (2020)]. Second, when investors choose criteria for their particular social concern, the screen brings up companies or sectors that would not even have this issue as part of their business—which begs the question of whether one is really doing anything like impact investing. Third, it is not always clear if social screening criteria are really Pareto improving. That is, while investing based on that view may be positive from a particular investor’s point of view, it might be detrimental to an entire other class of investors.
33
See
Chapter 2
.
34
For an additional discussion on testing the out-of-sample predictability of factors, see
Chapter 9
of Campbell et al. (1997).
35
Simple regression is a regression of one variable on another. Multiple regression is a regression of one variable on many other variables.
36
When we typically estimate these factor models, we use information at time
t
to predict returns at time
t
+ 1. Sometimes, in this book, for convenience, we write the equation with time subscript
t
everywhere, as we do here. The factor exposure and the returns are at time
t
. It should still be interpreted as using information at
t
to predict returns at time
t
+ 1. In other words, the factor exposure at time
t
is really the factor exposure value as of the end of the previous period,
t
− 1, which we may refer to sometimes as the beginning of month exposure for time
t
.
37
Appendix C describes some of the potential problems with including too few or too many factors in a factor model. Appendix C can be found at
www.ludwigbc.com
under QEPM Exclusive Content.
38
Unfortunately, we have met many portfolio managers who do this without understanding its implications. Most econometric software packages actually have procedures that do this very easily. Even if one understands the pitfalls of stepwise regression, it may be difficult to avoid stepwise regression completely. The point that we want to make is that one should be cautious interpreting the reported statistical significance.
39
We provide programs in R, MATLAB, and Stata that actually create these portfolios with real data. See
https://ludwigbc.com/books/qepm/exclusive_qepm_content_2020/
. We also discuss this topic more in
Chapter 16
.
40
When considering the testing of many factors, researchers may wish to adjust the
t
-statistics as explained earlier. Some suggestions for how to do this are contained in
Appendix 4B
.
41
Other techniques for reducing factors are also discussed in
Chapter 6
of Campbell et al. (1997), Bai and Ng (2003), and Barillas and Shanken (2018).
