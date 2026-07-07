# Quantitative Equity Portfolio Management: An Active Approach to Portfolio Construction and Management, Second Edition

- **book_name**: 5073 Quantitative Equity Portfolio Management, Second Ed.
- **main_source**: epub
- **cross_check_source**: none
- **pdf_role**: not_needed
- **split_scope**: chapter file = appendix5C

---

APPENDIX 5C
Converting Z-Scores to Returns
In some instances, it will be useful to convert Z-scores to returns, as we have already mentioned in this chapter. For example, when computing after-tax returns or after transactions costs returns, it will be more pertinent to convert one’s Z-scores to returns. There are various ways to do this that are more accurate, which we discussed in Sections 5.5 and 5.6. In this appendix, we will give an example using the second method described in Section 5.6 and based on
Eq. (5.10)
, but it could easily be extended to a method also controlling for other risk factors. In particular,
Eq. (5.10)
shows that when regressing Z-scores on future stock returns, the expected return of a stock conditional on the Z-score is given by
E
[
r
i,t
|
z
i,t
−1
] =
E
[
r
t
] +
δ
[
z
i,t
−1
−
E
(
z
t
−1
)] =
E
[
r
t
] +
ρ
(
r
t
, z
t
−1
)
S
(
r
t
)
z
i,t
−1
. When estimated as a cross-sectional regression (or a panel regression), the estimates will be the best predictor of the realized return, that is,
.
Suppose you are looking forward and have computed the Z-scores for all stocks in period
t
. You can then use the distribution of stock returns in period
t
to translate your Z-scores to either
α
or expected stock returns. If you do not perform estimations and assume that the correlation between stock returns and the Z-score is 1, then the transformation is simple: convert the Z-score distribution and maintain the relative Z-score values between stocks, but convert the distribution to resemble the first two central moments of the cross section of stock returns. Thus, the Z-scores for each stock would be modified as follows:
where
is the adjusted Z-score to be used as the expected return for each stock, and
σ
r
and
μ
r
are the cross-sectional standard deviation and mean of stock returns.
However, this is unrealistic and probably exaggerated, since it would be rare for the Z-score and stock returns to be perfectly correlated. If instead a regression had been run or an empirical estimate of the correlation between stock returns and the Z-score had been estimated, then you could transform the Z-scores to the stock return distribution as follows:
where the
has been estimated on recent data.
1
This would have the effect of scaling down the distribution to reflect the predictive component of the Z-scores in historical data. Of course, all of these examples involve using past data to extrapolate to the future, which will result in a margin of error. Even when historical correlations are taken into account, if the correlation is low, the result only represents a partial explanation of stock returns. Nevertheless, this is a technique that can aid practitioners in transforming Z-scores to stock returns to be used in optimization models that require assessment of transactions costs or tax costs.
5C.1 A NUMERICAL EXAMPLE
An example of this conversion of Z-scores is shown in
Fig. 5C.1
for December 2020. The first graph in
Figure 5C.1
shows the distribution of the Z-scores among 3,000 stocks according to a particular Z-score model in December 2020. The second graph shows the distribution of monthly stock returns for the same stocks. The third graph shows the distribution of the modified Z-scores adjusted for the mean and standard deviation of the cross section of stock returns assuming unrealistically a perfect correlation between stock returns and Z-scores. In this particular example, the mean and standard deviation of the cross section of stock returns was 2.98% and 11.07%. The mean of the Z-score was 0 and 1, and the
modified Z-score has the same mean and standard deviation as the stock returns. In the fourth graph, we show the modified distribution of Z-scores using the actual historical correlation between Z-scores and stock returns of 0.0306. One can see that this reduces the return distribution based on Z-scores to something more in line with the Z-score predictive power.
FIGURE 5C.1
Conversion of Z-scores to modified Z-scores using data from December 2020 in a universe of 3,000 stocks. In this figure,
μ
r
= 2.98,
σ
r
= 11.07,
μ
Z
= 0,
σ
Z
= 1,
, and
The means and standard deviations are from a cross section of monthly stock returns.
QUESTIONS
5.1.
What is stock screening used for in QEPM?
5.2.
Compare our Lakonishik-inspired screen with our Piotroski-inspired screen. How are they similar? How are they different?
5.3.
How might we screen for management’s view of the future of a company?
5.4.
There are many ways for a business to increase its earnings. One way is to increase the net profit margin. Another way is to increase the number of stores in operation. How might one measure a company’s market saturation?
5.5.
What types of factor screening are very common among the famous portfolio managers whom we discuss in this chapter?
5.6.
What are the advantages of simultaneous stock screening over sequential stock screening?
5.7.
What is the Z-score, and how is it related to simultaneous stock screening?
5.8.
(a)   What is meant by an ad hoc aggregate Z-score?
(b)   What is the danger with using this method of weighting?
(c)   Why might some people say that this method is
not really
QEPM?
5.9.
What is the optimal aggregate Z-score? How do you come up with it?
5.10.
A portfolio manager is building his portfolio of stocks. His benchmark is the S&P 500. He will focus on three factors to build his portfolio of stocks. These factors are P/B ratio, P/E ratio, and 12-month momentum (M12M). He generally believes that high-momentum stocks will continue to perform well in the future. For the other factors, he bases his judgment on the documented anomalies.
(a)    In the preceding table, for each stock, compute the Z-scores of each factor (
z
P/E
, z
P/B
, z
M12M
).
(b)    The manager believes that momentum is the most important item in determining stock returns. Thus he wishes to assign it a 50% weighting while weighting the other factors equally. In the preceding table, compute the aggregate Z-score for each stock.
(c)    If the portfolio manager were to create a long-only portfolio of two stocks weighted by their relative Z-scores, which stocks would go in the portfolio, and what would their weights be?
5.11.
Suppose a portfolio manager has created Z-scores for all stocks in the universe for a given factor. What is the probability that a stock with a Z-score of 2 or greater is observed in the population? How is your answer dependent on whether the distribution is normal or non-normal?
5.12.
Given the similarity in the signal between the factor group aggregate Z-score and the regular Z-score, why would a quantitative portfolio manager ever use the former?
5.13.
A portfolio manager has the data available in the following table. She believes in using a factor group approach to creating aggregate Z-scores. She has decided to construct four groups (i.e.,
M
= 4). Group 1 is titled the valuation group (V), group 2 is titled the technical group (T), group 3 is titled the profitability group (P), and group 4 is the alternative group (A). She also has seven factors that she has identified in predicting stock returns. They are the book-to-price (B/P) ratio, the earnings-to-price (E/P) ratio, the cash-flow-to-price (CF/P) ratio, the 12-month past stock return (M12M), standardized unanticipated earnings (SUE), current accruals (CACC), and net profit margin (NPM).
(a)    In which group would each of these factors most likely be placed?
(b)    Compute the Z-score of each factor and each stock.
(c)    Suppose that factors within each group are equally weighted. Compute the aggregate Z-score for every factor group.
(d)    After careful analysis, the portfolio manager has found that the optimal weights of the factor groups are 20%, 30%, 20%, and 30%, respectively, for the four groups. Compute the aggregate Z-score for each stock.
(e)    Suppose that the
δ
in
Equation (5.8)
is 1. Suppose that the portfolio manager constructs a portfolio with the three stocks with highest Z-scores equally weighted. What would be the difference between the expected return of this portfolio and the return of a portfolio with all six stocks equally weighted?
5.14.
Quantitative portfolio managers generally manage their portfolios versus a benchmark. Thus they usually require a set of expected returns and risks to construct a portfolio.
(a)    What problem does this requirement pose when using solely the aggregate Z-score to rank favorable stocks?
(b)    What are three methods to convert an aggregate Z-score of a stock into an expected return or
α
for use in portfolio construction?
(c)    Describe the strengths and weaknesses of each method.
5.15.
Suppose that a portfolio manager is interested in whether an aggregate Z-score is useful in forecasting the return of stocks in the next period. Suppose that he takes a month of stock returns and the aggregate Z-score of the individual stocks and runs the following regression:
r
i,t
=
γ
+
δz
i,t
−1
+
ϵ
i,t
. What hypothesis should he test?
5.16.
Some people express the regression equation
r
i,t
=
γ
+
δz
i,t
−1
+
ϵ
i,t
as something called the
forecasting rule of thumb
, which states that the expected return of the stock conditional on the Z-score information minus the unconditional return of the stock is equal to
IC
· volatility · score.
(a)    What does it mean when
IC
= 0, and what does it imply for the conditional excess expected return? What would the regression coefficient
be equal to if this were true?
(b)    What does it mean when volatility = 0, and what does it imply for the conditional excess expected return? What would the regression coefficient
be equal to if this were true?
(c)    What does it mean when score = 0, and what does it imply for the conditional excess expected return? What would the regression coefficient
be equal to if this were true?
5.17.
Suppose that a portfolio manager is examining two sectors of the U.S. economy in which to invest. She constructs Z-scores relative to the sector for each stock. The cross-sectional volatility of stock returns for the latest month is 20% and 40%, and the correlation between the Z-score and returns of stocks is 0.2 and 0.1 for stocks in sectors
A
and
B
, respectively.
(a)    In which sector will a Z-score be relatively more important at forecasting returns?
(b)    What are
and
of
Eq. (5.8)
? Is your conclusion the same as in part (a)?
5.18.
When is the Z-score model, as used in
Eq. (5.8)
, equivalent to the fundamental factor model? What does this mean?
5.19.
(a)   Why do portfolio managers who use the Z-score typically eliminate Z-scores with absolute values greater than 3?
(b)    What is an alternative way of handling such Z-scores? What is the common name given to this method?
(c)    Name a third way of dealing with these Z-scores that is mentioned in the chapter.
5.20.
For each test below, describe what it is used for and to what type of data it applies.
(a)    Rosner’s test
(b)    Grubb’s test
(c)    Dixon’s test
1
The conversion of Z-scores to returns in
Eq. (5C.2)
is exactly the same as using the estimated
Eq. (5.8)
to get the predicted values. That is,
.
