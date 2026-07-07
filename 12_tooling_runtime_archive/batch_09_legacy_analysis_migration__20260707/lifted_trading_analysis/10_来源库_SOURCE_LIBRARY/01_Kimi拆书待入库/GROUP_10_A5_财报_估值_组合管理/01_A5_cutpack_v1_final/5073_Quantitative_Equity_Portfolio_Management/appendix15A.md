# Quantitative Equity Portfolio Management: An Active Approach to Portfolio Construction and Management, Second Edition

- **book_name**: 5073 Quantitative Equity Portfolio Management, Second Ed.
- **main_source**: epub
- **cross_check_source**: none
- **pdf_role**: not_needed
- **split_scope**: chapter file = appendix15A

---

APPENDIX 15A
Style Analysis
Style analysis
is a technique for determining the exposure of a mutual fund, hedge fund, or any equity portfolio to various asset classes. The performance analyst may not know the holdings of a portfolio or the exact types of stocks that its manager tends to buy, but with style analysis, he or she can obtain a pretty clear idea of the portfolio’s exposures. Style analysis is less useful for the portfolio manager or a portfolio management shop and more useful for financial advisors, fund-of-fund managers, and other investors in deciding whether to include a particular portfolio or fund manager in their asset allocations.
Style analysis is a powerful technique that was developed by William Sharpe (1988) to analyze the investment styles of portfolio managers. Rather than analyzing individual portfolio holdings, this method looks at how a portfolio’s historical returns are related to various investment styles. An investment style can be thought of as a method of investing or even as a kind of benchmark. For example, a portfolio manager who invested primarily in small-cap growth stocks would be said to follow a small-cap growth investment style. Other investment styles include large-cap value style or a government bond investment style.
1
Naturally, a portfolio may be a combination of many styles. For instance, the Fidelity Magellan Fund was once classified as 53% large-cap growth, 34% large-cap value, 10% small-cap growth, and 3% foreign stocks. Style analysis can be used to determine whether a portfolio or fund’s strategy has deviated from its stated investment objectives. Style analysis measures performance versus the “true” benchmark rather than an arbitrary benchmark such as the S&P 500. Finally, style analysis can be used to understand the true exposures of a portfolio and how it will best fit with an investor’s overall asset allocation. Style analysis is a statistical method of decomposing the portfolio’s returns into a set of style-specific benchmarks. The choice of benchmark styles can vary from study to study and from one performance analyst to another. Typical benchmarks include cash (a Treasury bill index), a government bond index, a corporate bond index, a foreign bond index, a large-cap value index, a large-
cap growth index, a small-cap value index, a small-cap growth index, and a foreign stock index. Once the relevant indices have been chosen, one uses a quadratic optimization technique on the past returns of the portfolio and the relevant indices to find the “style” of the portfolio.
Thus, suppose that we could represent the return of a portfolio or fund as a linear combination of other major asset classes (e.g., large-cap equity, value equity, fixed income, etc.). Thus
where
r
P,t
represents the monthly returns of the portfolio,
r
i,t
represents the monthly returns for the particular style index,
i, w
i
represents the style weight for benchmark
i
, and
ϵ
t
represents an error term. We can rearrange this equation in terms of
ϵ
t
, and the goal of style analysis is to minimize the variance of the error term subject to certain constraints.
2
Thus, formally, style analysis involves finding the weights on the style benchmarks
w
i
such that
The optimal weights
multiplied by the returns of the respective benchmark returns can be thought of as the “mimicking” fund for that portfolio or fund. That is, the
weights are the weights that one would invest in the style benchmarks to achieve the closest tracking error to the actual portfolio. Hence the style benchmark is all the benchmarks with their estimated
exposure.
3
Thus, to find the
style weights
in style analysis, one can either use a linear regression with constraints and renormalize the weights or one can use our tools of quadratic programming from
Appendix 9A
. The inputs for the quadratic optimization must be computed.
4
The matrix
Q
is the variance-covariance matrix returns of the style benchmarks and the portfolio. This variance-covariance matrix is computed from historical data. The
x
’s are the weights on the vari
ous style benchmarks (i.e., the
w
’s) and the weight on the portfolio. The weights on the asset classes will be determined by the optimization. Thus the vector of weights
x
will be an (
N
+ 1) × 1 matrix consisting of the
N
style weights and the portfolio weight. The constraints will be that all asset weights are between 0 and 1, except for the portfolio weight, which will be constrained to be −1.
5
Thus the matrix setup is as follows:
where
A
eq
and
b
eq
are a set of equality constraints and
A
ineq
and
b
ineq
are a set of inequality constraints.
Another important aspect of style analysis is to compute the so-called
R
2
of the regression. This measures to what degree the style benchmarks really represent the underlying portfolio. Just as in regression analysis, an
R
2
close to 1 means that the style benchmark accurately represents the return behavior of the portfolio, whereas an
R
2
close to 0 means that the style benchmark does a very poor job at representing the portfolio. Owing to the restrictions on the
w
i
s
, and since some people will use the quadratic optimization technique to solve for the optimal weights, we need to construct an
R
2
. One way to do this is simply to take the optimal parameters from the quadratic optimization and then create the time series of the style benchmark and subtract it from the portfolio returns. Thus the
R
2
can be computed as
A simple example might be useful. We took three quantitative portfolios that we knew relatively very little about and performed a style analysis using nine style benchmarks. The results are pre
sented in
Table 15A.1
. The three hypothetical portfolios that we chose to study by various portfolio managers were a utilities sector portfolio, an opportunities portfolio, and a Latin America portfolio. The style analysis results help us to understand the portfolio construction a bit better. First, the
R
2
of the utilities portfolio is much too low to make any important inference about it. It does suggest that the utilities portfolio has a strong sensitivity to interest rates given the large bond index exposure. The opportunity portfolio has a decent
R
2
. From the style analysis, we can infer that this portfolio behaves as if it were invested in 27% large-cap value, 58% large-cap growth, and 13% in non-U.S. dollar bonds. Thus this portfolio is pretty much a large-cap equity portfolio. For an investor deciding how to allocate this quantatative portfolio to his or her asset allocation, he or she can treat it as a large-cap portfolio or, to be more specific, as a portfolio that is roughly 85% large cap. The Latin America portfolio behaves mainly like a portfolio of U.S. large-cap stocks (75%) but also has a significant exposure to U.S. small-cap stocks (22%). Oddly enough, the returns of this portfolio behave more like U.S. stocks than foreign stocks (4%). This is one of the beautiful aspects of style analysis. Normally, we would consider a portfolio of Latin American stocks to be foreign stocks, but this analysis shows that this particular portfolio’s returns behave much like a portfolio of U.S. stocks. Of course, the
R
2
of 56 may warrant further analysis before a firm conclusion is made.
TABLE 15A.1
Selected Quantitative Portfolios Using Style Analysis
We conclude our discussion on style analysis by mentioning some other issues. First, when computing the style of a portfolio, it is important to consider how much historical data to use. We call this the
time period
or
measurement period
. It should be short enough to capture the style changes of a portfolio but long enough to not be measuring noise. A practitioner will have to gauge what that amount of data is. Typically, three years of monthly data will work well. Second, some practitioners will estimate the style of the portfolio dynamically. That is, they will estimate the style using three-
year windows and then roll the window along. This is what is meant by the term
rolling window
. They then plot the style changes of the portfolio. This is known as
style drift
, that is, that the portfolio is changing style over time. Third, using style analysis for portfolio managers of hedge funds may become tricky because these portfolio managers use leverage, derivatives, and other fancy tools. Thus Fung and Hsieh (1998) have suggested how to modify style analysis to measure more complicated managers, such as trend-following commodity trading advisors (CTAs).
6
Finally, although mutual fund managers are required to report their portfolio holdings only quarterly and there is a lag in this publication, we believe that a clever analyst could combine style analysis with the original stock weightings and holdings to unveil the actual holdings of the mutual fund manager using daily fund returns for mutual funds with low turnover. This might be an area of research for an ambitious performance analyst.
1
Even though we are concerned with equity managers, certain equity portfolios behave very much like a portfolio of government bonds; thus we can ironically describe an equity manager as having a bond investment style.
2
This is very similar to minimizing the tracking error of the portfolio with respect to the linear combination of style benchmarks.
3
Some practitioners estimate a portfolio’s style by estimating a regression with the constraints that the estimated coefficients sum to 1 and are between 0 and 1.
4
The optimization will be an optimization with inequality constraints, which can be done quickly by any standard quadratic optimizer.
5
Some practitioners may take this further and place constraints on the excess return of the portfolio versus the style benchmark. This is a simple addition to the constraints.
6
For an application to hedge funds, see Chincarini (2014) and Chincarini and Nakao (2011).
