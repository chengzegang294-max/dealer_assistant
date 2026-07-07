# Quantitative Equity Portfolio Management: An Active Approach to Portfolio Construction and Management, Second Edition

- **book_name**: 5073 Quantitative Equity Portfolio Management, Second Ed.
- **main_source**: epub
- **cross_check_source**: none
- **pdf_role**: not_needed
- **split_scope**: chapter file = appendix5B

---

APPENDIX 5B
On Outliers
5B.1 GENERAL CONCEPTS
An
outlier
is an observation in a distribution that is extreme and looks very inconsistent with the rest of the data. These outliers could arise due to data errors by the data supplier or measurement error or could be correct values representing novel phenomena. If they arise due to data errors, it is a good idea for the portfolio manager to remove them entirely. If they are accurate and represent novel phenomena, there is no need to remove them. In practice, however, the portfolio manager may be unable to determine whether he or she is dealing with data errors or with novel phenomena. Thus, the portfolio manager in this case may wish to modify their values to some reasonable values just for safety. The outliers will still be strong signals vis-à-vis other stocks.
Formally speaking, we consider two possibilities. The first possibility (which might be called a
null hypothesis
) is that all the observations are random draws from distribution
A
. In this case, no outliers exist. The second possibility (which might be called an
alternative hypothesis
) is that most observations are random draws from distribution
A
, but some observations are from distribution
B
. Then we might label the observations from distribution
B
as outliers. In order to apply this categorization of outliers to real data, we need to know or assume the
A
distribution (of the null hypothesis). If we do not know distribution
A
or we are very uncertain about it, detecting outliers becomes theoretically
difficult, and excluding suspect observations from the analysis might not be justified.
Popular outlier detection techniques assume that the underlying distribution is a normal distribution. Grubb’s (1950) test, Dean-Dixon’s (1951) test, and Rosner’s (1975) test are three examples. There are also procedures applicable to non-normal distributions. Igleewicz and Hoaglin (1993) is a good reference for further discussion.
Dealing with outliers involves two steps. In the first step, we identify certain observations as outliers. This is the
labeling step
. In the second step, we decide what to do with identified outliers. We may remove these observations (
trimming
or
truncation
), replace their values with something less extreme (
winsorization
), or we may use a more creative approach.
5B.2 SPECIFIC PRACTICAL TECHNIQUES
5B.2.1 Utilizing the Z-Score
One method to deal with potential outliers is simply to label stocks with the absolute value of the Z-score greater than 3 as outliers. While easy, this is not a reliable method because the extreme values were used to compute means and standard deviations. A second method is the modified Z-score method, where, rather than using the standard deviation of the factor values, the median is used to compute the modified Z-score. The modified Z-score,
, is defined as
, where
M
(
β
i,j
) is the median value of factor
j
across stocks. All observations with the absolute value of the modified Z-score greater than or equal to 3 are considered outliers. Once the outliers are identified, they can be eliminated or their values can be adjusted.
Winsorization
is the process of replacing outliers with other values in order to prevent the outliers from unduly influencing the estimates. One form of winsorization we discussed in the main text is to convert all Z-scores with a value greater than 3 to the value 3 and those with a value less than −3 to −3.
Trimming
is the process of removing the
n
values consisting of
n
/2 of the largest values and
n
/2 of the smallest values. The Z-scores are then recomputed for the remaining data. A version of this is suggested in the text, which is to simply remove all Z-scores
whose absolute values are greater than some determined value, such as 3, 4, or 5.
5B.2.2 The Interquartile Method
One effective method to deal with outliers when building QEPM models is the
interquartile method
.
1
To implement the interquartile method, compute for each factor the interquartile range of the factor for the cross section of factors amongst stocks. This will be the value that is a measure of the middle 50% of factor values. This is computed by finding the third-quartile entry of every factor (Q3) and the first-quartile entry of every factor (Q1) and then subtracting them (Q3 − Q1) to find the interquartile range (IQR). At this point, a decision must be made on what deviation from the 75th percentile and 25th percentile constitutes an outlier. This is known as the
IQR coefficient
. For example, if the IQR coefficient is equal to 3, then upper and lower bounds of the factor are computed as
2
Then consider all stocks with factor values above the upper bound and below the lower bound to be outliers.
For these, set their values to missing and compute the Z-scores for the remaining stocks. For the outlier stocks, fix the Z-scores at the maximum and minimum of the nonoutlier stocks’ Z-scores.
A Numerical Example
In December 2020, the raw data for our beta calculations based on excess market returns and company stock returns for the universe of the top 3,000 stocks in the United States by market capitalization ranged from −5.78 to 7.48. These corresponded to the stocks AVGO and IBIO. Based on an IQR coefficient of 3, the values for the IQR procedure were Q3 = 1.7391, Q1 = 0.8721, IQR = 0.8669,
UB 204= 4.3398, and LB = −1.7287. This removed 0.83% of all of our cross-sectional data, or 25 observations, but left very stable Z-score values for 99.17% of our stock data. The range of Z-scores was also less extreme. Using the traditional Z-score method, the maximum and minimum Z-scores were 7.46 and −8.75, respectively, compared to 4.10 and −3.97 using the IQR method.
5B.2.3 The Ranking Method
Another reasonable method to remove outliers is to use a ranking method. Rather than use Z-scores for the individual factors, the portfolio manager could use cross-sectional ranks. That is, every evaluation period, order the stocks according to the stock’s factor value, and rank the stocks from highest to lowest. Then compute Z-scores on the actual rank, rather than the factor values. This resolves the outlier problem; however, it also loses information contained in the distance between different stocks’ factor values, keeping just the relative value of Z-score between stocks. The ranking Z-score value for each stock in a given month is given by
where rank is the cross-sectional numerical rank of each stock in the universe from high (better attribute) to low.
A Numerical Example
Using the same example as in Section 5B.2.2 with betas in December 2020 with the rank method, the maximum and minimum rank Z-scores were 1.7312 and −1.7312, respectively.
5B.2.4 The Percentile Ranking Method
A method very similar to the ranking method is the
percentile ranking method
. Once the
N
stocks are ranked from highest to lowest, the following calculation is made for each stock:
Using the same example as in Section 5B.2.2 with betas in December 2020 using the percentile method, the highest-beta stock, AVGO, would have a 100th percentile and the lowest-beta stock, IBIO, would have a 0th percentile. With multiple factors, the factors can be combined by percentile rank—and this can be normalized further to obtain an aggregate percentile rank that ranges from zero to one.
1
See Chincarini (2017, 2018) for more information. This is a better method than simple winsorization, which has a major drawback: after the winsorization method has removed certain stocks and the Z-scores are recomputed, there may be still a group of outliers. The procedure must then be repeated again, leading to an iterative process that takes more time and might be less efficient.
2
Another common value for the IQR coefficient is 1.5. Other values can be chosen as well.
