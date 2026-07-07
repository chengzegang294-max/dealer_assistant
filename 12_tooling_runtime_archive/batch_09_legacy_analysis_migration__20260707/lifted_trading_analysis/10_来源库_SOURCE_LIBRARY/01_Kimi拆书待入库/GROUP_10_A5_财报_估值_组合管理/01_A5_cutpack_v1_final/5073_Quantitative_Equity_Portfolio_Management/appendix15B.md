# Quantitative Equity Portfolio Management: An Active Approach to Portfolio Construction and Management, Second Edition

- **book_name**: 5073 Quantitative Equity Portfolio Management, Second Ed.
- **main_source**: epub
- **cross_check_source**: none
- **pdf_role**: not_needed
- **split_scope**: chapter file = appendix15B

---

APPENDIX 15B
Measures of Opportunity
At a monthly investment meeting, portfolio managers typically look at the performance of their portfolios over the month or the quarter. They usually look at classic attribution or risk-model attribution. They may look at which stocks did well and which stocks did not do so well. One question that might be asked in such a meeting is what was the
opportunity
in the investment universe. By opportunity, we mean the possibility to create excess returns through quantitative management. There are many measures of opportunity. For example, the cross-sectional standard deviation of the returns of the stocks in the universe for the given performance period is a measure of opportunity. A larger standard deviation indicates that there was a greater opportunity to pick outperforming stocks. Another measure of opportunity might be the performance of the top decile stocks for the period equally weighted minus the bottom decile of stocks equally weighted. The higher this value, the greater was the opportunity in the universe for that performance period. Although these measures certainly signify some amount of opportunity in the universe for the period, they are more useful for comparisons across time (i.e., the same universe over different measurement periods) or across different sections of the universe (e.g., the opportunity of each sector in the universe for a given sample period). These measures are less useful in the monthly investment meeting relative to the performance of the actual portfolio manager. What might be useful, however, although it involves a bit of work, is creating a series of measures corresponding to portfolio managers with varying levels of skill ex post. There may be many methods to do this, but we describe one possible method here.
The method that we describe consists of taking the ex-post returns of the stocks and using this information to create a series of portfolios based upon the various levels of forecasting skills from 50% to 100%. The portfolios are constructed using the same optimization with constraints that the actual portfolio manager used to create his portfolio. The average returns of many simulated portfolios can then be compared against the portfolio manager’s returns. Since they were created in the same fashion, with the exception of the forecasting skill, they give a more accurate assessment of
opportunities really available to the particular portfolio manager. We discuss the steps the performance analyst should take to create these portfolios below.
Step 1:
The performance analyst should decide the levels of simulated skill he or she would like to produce. For example, a reasonable dispersion of skill might be 50%, 60%, 70%, 80%, 90%, and 100%.
Step 2:
For each skill level, use a random number generator to generate random values from a uniform distribution from [0, 1].
Step 3:
The critical point on the random draws will be determined by the skill level. For instance, if the skill level is 60%, then every value that is generated from 0 to 0.6 should reflect a correct foresight of the realized return of one stock in the entire universe. If the draw is from 0.6 to 1 (or generally from the critical value to 1), then this should reflect an incorrect forecast of the expected return of one of the universe stocks.
Step 4:
Begin by generating
N
randomly generated uniform draws. The number of draws less than the critical value is
n
g
, and the number of draws greater than the critical value is
n
b
. These stand for the number of good and bad predictions, respectively.
Step 5:
The performance analyst should begin with the good draws. First, each stock in the universe of
N
stocks should be given a number 1 to
N
. For each of the
n
g
values, another random uniform draw should be made, where one normalizes the uniform distribution by multiplying by
N
.
1
Thus the number that is drawn is the stock for which the forecaster forecasted the realized return correctly. Remove this stock along with its expected return and repeat the experiment, with
N
− 1,
N
− 2, and so on.
Step 6:
Once the
n
g
stocks have been removed, the remaining stocks can be assigned randomly the remaining returns. That is, every one of the
n
b
stocks has a realized return for the period. Rather than using their actual realized returns, randomly distribute these
returns to the stocks. This can be done by creating a new uniform draw for every stock and then ordering the stocks by random number and attaching the ranked realized returns to the ordered list. This will maintain the actual realized returns of all stocks for the period but randomly assign them among the bad forecasted stocks.
Step 7:
The performance analyst then should compute the mean return vector of the stocks along with the variance-covariance matrix of the stock returns. These should be used in conjunction with the same constraints that were used at the time of the original portfolio construction to construct the “look-ahead” portfolio. The portfolio that emerges with appropriate portfolio weights becomes the forecaster’s portfolio with skill level
p
, where
p
represents the ranges chosen earlier.
Step 8:
The paper performance of this portfolio should be computed.
Step 9:
The performance analyst should repeat this 100 times for each skill level and store the results, including the average returns and the SD of the returns.
Step 10:
A table should be compiled comparing the different forecasting skill levels’ average returns, excess returns, and information ratio to the actual portfolio returns of the portfolio manager.
This methodology is time-consuming, although with an in-house risk optimizer system and the computer speed of today, it is feasible. This is a method of comparing the true opportunity in the manager’s universe because it not only varies the forecasting accuracy of the portfolio manager but also constructs portfolios against the same benchmark and constraints the actual portfolio manager had to face. It is one method of measuring true opportunity for the portfolio manager.
1
That is, the number drawn will be
N
· uniform(0, 1).
