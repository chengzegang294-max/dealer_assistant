# Quantitative Equity Portfolio Management: An Active Approach to Portfolio Construction and Management, Second Edition

- **book_name**: 5073 Quantitative Equity Portfolio Management, Second Ed.
- **main_source**: epub
- **cross_check_source**: none
- **pdf_role**: not_needed
- **split_scope**: chapter file = appendix4B

---

APPENDIX 4B
On Data Mining and Techniques to Adjust the Significance of Factors
One way to describe the danger of data mining is as follows: If we determine a factor to be statistically significant whenever the absolute value of the
t
-statistic associated with the factor is greater than 1.96, we are most likely overstating the statistical evidence. In many real-life situations, we do not test a factor in isolation but consider many factors jointly. A particular factor that we like may have been selected because of its large
t
-statistic in comparison with the conventional critical value of 1.96. This may not be the appropriate critical value. Such a comparison will lead us frequently to declare a factor to be significant even when the factor is in reality not significant. The probability of false discovery will be much higher than our intended target of 5% (i.e., our selected significance level).
One straightforward solution is to choose a higher critical value so that the probability of false discovery declines to 5% even when we focus on one factor out of many due to its sample
t
-statistic. While this sounds straightforward in principle, applying this idea in practice is not so easy. The biggest challenge is that, quite often, we are not able to determine the total number of factors under consideration. If another portfolio manager conducted the analysis and only reported a factor with a large
t
-value, we cannot know the total number of factors that he or she tested. Even if we conducted the analysis ourselves, our choice of candidate factors may have been influenced by our reading of others’ research reports, and it is not easy to decide
how many factors were considered in the numerous research reports that we may have read over the years.
Despite these difficulties, we briefly describe two approaches to data mining that have been discussed in the academic literature. These approaches will not shield us from the danger of data mining completely, but may help us have a better sense of the magnitude of potential problems. The first approach, which we refer to as the
Bonferroni-type adjustment
, is based on the traditional, frequentist statistical theory in which the calculated
t
-statistic is compared to the distribution of all the
t
-statistics that we could have obtained assuming the truth about the null hypothesis. The second approach is based on Bayesian statistical theory in which our subjective probability of the null hypothesis being true is derived from the data and our personal beliefs.
4B.1 THE BONFERRONI-TYPE ADJUSTMENT
In the Bonferroni adjustment, the critical value for the
t
-test is determined by the total number of factors tested. The critical values are shown in
Table 4B.1
. These values are computed in the following way. Let
M
be the number of factors tested. Let
α
be the significance level that we choose (e.g., 0.05). Then the critical
p
-value in the Bonferroni adjustment is calculated as
α /M
. From this critical
p
-value, we can recover the critical
t
-value as
t
∗
= Φ
−1
(1 −
p
∗
/ 2), where
p
∗
is the critical
p
-value, Φ is the standard normal distribution function.
TABLE 4B.1
Critical
t
-Values for Bonferroni and Holm Adjustments
The Holm adjustment, a variation of the Bonferroni adjustment, proceeds in a slightly different way. When
M
factors are considered, we may order these factors from the one with the highest absolute
t
-value to the one with the lowest absolute
t
-value. Thus, we may denote these
t
-values by
t
1
≥ · · · ≥
t
M
. If we denote the
p
-values of these
M
factors,
p
1
≤ · · · ≤
p
M
. To proceed with the Holm adjustment, we first need to determine the index
j
such that
p
1
≤ · · · ≤
p
j
≤
α
/(
M
−
j
)
< p
j
+1
≤
p
M
. Once we determine
j
, we may conclude that the first
j
factors are significant. Note that the critical
p
-value,
α
/(
M
−
j
), is a function of the entire set of
p
-values and that it is not possible to convert this into a generic critical
t
-value. What we show in
Table 4B.1
instead is the
t
-value corresponding to
α
/(
M
−
j
) assuming
j
= 0.05
M
.
As mentioned earlier, the most difficult part of implementing the Bonferroni or Holm adjustment is the choice of the number of factors tested. Some researchers have suggested using the total
number of published and unpublished research articles since 1967 for this purpose. By some counts, this is about 313 articles (or 316 factors) through 2012. The Bonferroni critical
t
-value corresponding to the previously discovered factors is 3.78. If the rate of research articles produced continues at this same rate, the Bonferroni critical
t
-value will be 4.00 by 2032.
1
4B.2 A BAYESIAN ADJUSTMENT
Consistently applying the Bayes rule to assess the subjective probability of a null hypothesis may alleviate the problems associated with data mining. In the Bayesian approach, the posterior probability of a null hypothesis being true is determined as the product of the prior probability of the null hypothesis being true and its likelihood (i.e., the probability of the observed data being generated when the null hypothesis is true). The same can be said about the posterior probability of an alternative hypothesis. Combining these two ideas leads to this statement: the posterior odds ratio (the posterior probability of the null hypothesis being true divided by the posterior probability of the alternative hypothesis being true) is the product of the prior odds ratio and the likelihood ratio. Among these three concepts—the posterior odds ratio, the prior odds ratio, and the likelihood ratio—the likelihood ratio can be calculated without reference to a particular individual’s beliefs. Thus, this is a good starting point to construct a test statistic.
One potential choice to guide the portfolio manager is the minimum possible value of the likelihood ratio, determined by considering all the possible alternative hypotheses. This ratio might be called the
minimum Bayes factor
(MBF).
2
Once the value of MBF is determined, a new critical value of the
t
-test can be determined. At the significance level of 5%, a critical value of
t
is the one corresponding to the 95% posterior probability of the null hypothesis being true.
Table 4B.2
presents the critical
t
-values for different prior odds ratios. The prior odds ratio of 0.01 indicates that the null hypothesis is highly likely with 99:1 odds. The prior odds ratio of 0.50 indicates that the null hypothesis is as likely as the alternative hypothesis. In other words, the higher the odds ratio, the more the analyst or portfolio manager is convinced that the factor is important in predicting stock returns. A value of 0.99 or 99% would mean that he or she is almost certain of it.
TABLE 4B.2
Critical
t
-Values for a Type of Bayesian Adjustment
QUESTIONS
4.1.
What is a factor, and why is it important in QEPM?
4.2.
What are the four basic categories of factors in QEPM?
4.3.
What are some common fundamental valuation factors?
4.4.
Suppose that there is a group of stocks, group A, with an average P/B ratio that is lower than the industry average, and another group of stocks, group B, that has a P/B ratio that is higher than the industry average. Which group would a growth portfolio manager choose? A value manager?
4.5.
What would be more appropriate for a P/E ratio factor, a trailing P/E ratio or a forward P/E ratio? Explain.
4.6.
Using concepts from Appendix B, at
www.ludwigbc.com
under QEPM Exclusive Content, about the dividend discount model, combined with the discussion in this chapter, answer the following questions:
(a)    Derive an expression for the P/E ratio in terms of the payout ratio
k
, the required rate of return on equity
r
ce
, and the growth rate of earnings
g
.
(b)    Rearrange this expression so as to obtain the implicit growth rate of earnings implied by the actual P/E ratio of the stock and other parameters.
4.7.
Why would fundamental solvency factors be included in a stock return model?
4.8.
What might you expect to be more effective at explaining stock returns, gross profit margin or the change in gross profit margin? Explain.
4.9.
All else equal, would you prefer a low D/E ratio or a high D/E ratio company in your portfolio? What are some other measures of fundamental financial risk?
4.10.
(a)   Why might fundamental liquidity factors be important for QEPM?
(b)   What do you think is more relevant in this regard, average daily trading volume, market capitalization, or float-weighted capitalization? Explain.
4.11.
Technical factors are being used increasingly in QEPM.
(a)    What is the main reason for using technical factors?
(b)    Name four types of technical factors.
(c)    Which type of quantitative portfolio manager is likely to use a technical indicator as a factor, one who rebalances monthly or one who rebalances quarterly?
4.12.
Given the data in the following table on the stock AALC, please do the following:
(a)    Compute the mean, upper, and lower bands of a Bollinger band with two standard deviations (i.e.,
l
= 2)    and a 10-day rolling window (i.e.,
k
= 10) for the dates July 26, 2020–July 29, 2020.
(b)    Suppose that the quantitative portfolio manager is a contrarian. Thus she believes that markets overreact to information. Should she buy or sell or do nothing on each of those days according to the Bollinger band?
(c)    Using the same data, compute the relative strength index (RSI) for each of those days, assuming a nine-day Wilder period.
(d)    Some technicians would argue that the Bollinger band should not be used in isolation but in conjunction with other indicators, such as the RSI. Given this philosophy, would you buy or sell or do nothing on this stock on July 26, 2020?
4.13.
(a)   What are three of the biggest drawbacks of using macroeconomic factors?
(b)   What is one of the biggest benefits of using economic factors in stock return models?
4.14.
A quantitative manager is collecting data for use with a stock return model. He finds that there is a positive relationship between this month’s inflation and stock returns. What might you be worried about in use of these data?
4.15.
Many factors are lumped into an area called
alternative factors
. Please respond to each of the statements below.
(a)    Analyst factors are very useful because they incorporate a lot of analysis of a company into one number.
(b)    Analyst factors were more useful prior to 2000 than they are today due to the SEC rule known as Reg FD (fair disclosure) that became effective in October 2000.
(c)    A change in analyst recommendation describes stock returns better than the recommendation itself (strong buy, buy, sell, etc.)    does.
(d)    Downgrades of a stock by some analysts probably serve as more useful factors than downgrades of a stock by all analysts.
(e)    What are standardized unanticipated earnings (SUE)? Why might this be useful as a factor? (
Hint:
Use the idea of information diffusion in your explanation.)
4.16.
Does investing in socially responsible companies hurt portfolio returns?
4.17.
What kinds of tests or techniques can an analyst use to choose factors for
(a)    a fundamental factor model?
(b)    an economic factor model?
4.18.
Why might univariate factor tests not be sufficient to determine the factors in a fundamental model?
4.19.
True or false? The stepwise regression technique is very powerful in identifying the optimal combination of factors for use in a stock return model. Portfolio managers always should use it.
4.20.
What might the Kendall statistic or other rank-correlation statistic be used for?
4.21.
From a cross-sectional regression of stock returns on the exposure to factor
A
, we obtained the slope estimate of 0.5 and the standard error of 0.2.
(a)    If you apply the conventional
t
-test, will you conclude that factor
A
is a statistically significant factor?
(b)    Prior to running the regression, you have read through 100 research reports regarding 100 different factors including factor
A
and have learned that factor
A
has the highest
t
-statistic. In fact, this is why you became interested in factor
A
. Thus, your regression analysis is likely to be criticized as a data-mining exercise. In response to such criticism, you decided to apply the Bonferroni adjustment described in
Appendix 4B
. Will you conclude that factor
A
is a statistically significant factor?
(c)    Instead of applying the Bonferroni adjustment, if you adopt the Bayesian adjustment discussed in this chapter, will your answer be different?
1
See Harvey et al. (2016).
2
See Harvey (2017).
