# Quantitative Equity Portfolio Management: An Active Approach to Portfolio Construction and Management, Second Edition

- **book_name**: 5073 Quantitative Equity Portfolio Management, Second Ed.
- **main_source**: epub
- **cross_check_source**: none
- **pdf_role**: not_needed
- **split_scope**: chapter file = chapter09

---

CHAPTER 9
Portfolio Weights
A little caution outflanks a large cavalry
.
—Otto von Bismarck
9.1 INTRODUCTION
In
Chapters 5
through
8
we discussed how to create models for stock selection.
1
Models serve as essential tools for identifying “good” and “bad” stocks. However, to construct a portfolio, the manager ultimately needs to do more than separate the wheat from the chaff. A good manager does not just throw a bunch of stocks into the same basket. Rather, he or she assigns them relative weights so that they make sense as a single portfolio.
There are many ways to generate stock weights. Some methods are very rudimentary, such as choosing the best stocks in one’s universe and weighting them equally. Another simple method is to weight the stocks by market capitalization, as many indices do. A slightly more complicated twist on market-capitalization weighting is to weight by the square root of the market capitalization. The most complex weighting methods draw on ideas from modern portfolio theory and attempt to weight stocks in a way that maximizes the portfolio’s expected return and minimizes its overall risk.
For the majority of portfolio managers who manage their portfolios against a benchmark, the weighting possibilities multiply. For
instance, a manager could weight the stocks such that the weighted-average factor exposures of the stocks equal the benchmark’s weighted-average factor exposures. Extending the concepts of modern portfolio theory to the weighting decision, the manager could try to maximize the excess expected return while placing a limit on the allowable tracking error of the portfolio versus the benchmark.
In order to weight stocks in a way that minimizes tracking error or risk, the manager needs to know each stock’s expected return, each stock’s risk or variance, and the covariances among stocks.
2
A manager also may wish to put constraints on the portfolio creation process. He or she may, for instance, prohibit short sales (i.e., not allow negative stock weights) or specify the range of permissible weights for individual stocks (e.g., to uphold mutual fund diversification rules). The manager then puts all these parameters and constraints into a
quadratic optimizer
and solves for the optimal weights of the portfolio.
This chapter discusses the mathematical and statistical concepts of portfolio weighting. For portfolio managers who use commercial software, the discussion will be helpful for understanding the mechanics of combining their preferred stocks with the vendor’s risk models to determine the portfolio weights. For those who want to build their own in-house risk models and portfolio optimizers, this chapter will walk you through the important methods.
We begin by discussing the two ways to create a portfolio that is not managed against a benchmark. Ad hoc methods (Section 9.2) use various rules of thumb to weight stocks. The mean-variance optimization method (Section 9.3) minimizes the portfolio’s total risk given its expected return.
We then consider the four potential approaches to creating a portfolio that is managed against a specific
benchmark
. The portfolio manager again could use an ad hoc weighting method that only roughly tracks the benchmark. Alternatively, he or she could use a method of sampling known as
stratification
, which involves choosing representative samples of the benchmark. Or he or she could use
factor exposure targeting
, in which the stocks are weighted so that the average factor exposures of the portfolio and the benchmark
match. Finally, the manager could follow the most common weighting method of professional money managers—
tracking-error minimization
. The stock weights are chosen so as to achieve the highest possible expected return or
α
of the portfolio while keeping the tracking error below a specified threshold. Of the four weighting techniques, only the ones that minimize risk have theoretical rigor. They also require, though, a larger skill set, more time, and more effort than do the other less quantitatively precise techniques.
9.2 AD HOC METHODS
Once the portfolio manager decides which stocks to include in his or her portfolio, there are two very easy ways to determine the portfolio weights: equal weighting and value weighting.
Equal weighting
is simply assigning the same weight to every stock. If there are 10 stocks, then each stock will have a weight of 0.1 (= 1/10). If there are 50 stocks, then each stock will have a weight of 0.02 (= 1/50). In general, if there are
N
stocks, each stock will have the weight of 1/
N
. Equal weighting is certainly quick and simple, but it has one major deficiency: It reflects neither the risks nor the expected returns of stocks. Equal weighting makes sense only when the portfolio manager has very poor information about the expected return and the risk of stocks selected.
Value weighting
is assigning weights proportional to the stocks’ market capitalizations. For example, if the market capitalization of stock
A
is twice as great as the market capitalization of stock
B
, then the weight of stock
A
also should be twice the weight of stock
B
. In general, if there are
N
stocks with market capitalizations
x
1
, …,
x
N
, then the weight of stock
i, w
i
, is
Just like equal weighting, value weighting does not reflect the expected returns or the risks of the selected stocks, so it is also not the best method when there is good information about stock returns and risks. In the absence of such information, value weighting may be an improvement on equal weighting. The performance of the value-weighted portfolio is at least guaranteed to match the
market average performance because market capitalizations are the weights, so to speak, that the market assigns to stocks.
There are a number of variations on value weighting.
3
Some portfolio managers have gone so far as to weight stocks by the square root of the market capitalization. Using the square root reduces the weighting bias toward stocks with very large market capitalizations. In this scheme, stock
i
would get a weight of
One could get even more creative and do the cubed root, and so on and so forth.
Instead of equal weighting or value weighting, portfolio managers also can use
price weighting
. In the price-weighting scheme, the manager buys the same number of shares in each stock so that the weights are proportional to the prices of stocks. If the share price of a stock is high, this stock will have relatively more weight in the portfolio. This is the way the Dow Jones Industrial Average and the Nikkei 225 are calculated.
We will discuss a few more ad hoc weighting schemes when we discuss the weighting of benchmarked portfolios.
9.3 STANDARD MEAN-VARIANCE OPTIMIZATION
Given the mean and the variance of future stock returns, we can use the quadratic programming technique to find the portfolio that has the
minimum risk
. That is, we can find the portfolio that has the lowest ex-ante risk among portfolios with identical expected returns. This is known as
mean-variance optimization
or simply,
MVO
.
The underlying idea of this method is the comparison of all the portfolios that potentially could be built given a list of stocks. We theoretically compute each portfolio’s ex-ante risk from the variances and covariances of the returns of all stocks and each portfolio’s expected return from the mean returns of individual stocks. Then we theoretically compare the ex-ante risks and the expected
returns of all the portfolios and choose the one with the lowest risk for a given level of expected return. (Or, conversely, we can choose the portfolio with the highest expected return for a given level of risk.
4
)
Of course, actually calculating the expected return and the risk of every potential portfolio would take forever because there are infinite potential portfolios. Thus we use quadratic programming to find the minimum-risk portfolio without having to explicitly calculate every portfolio’s risk and return.
One common objection of MVO is that the selected portfolio often assigns very large weights to certain outlier stocks, including stocks with very low variances or very high means. This in itself should not be a concern. If the stock indeed has a low variance for a given return, then it is smart to overweight it in the portfolio. However, in portfolio construction, we must estimate the means and variances of stocks, so we cannot be sure of their true values. Some outliers could be mismeasurements and throw off our results (“Garbage in, garbage out,” as the saying goes). The portfolio manager therefore must do his or her best to account for estimation error.
5
If this is not practical, the manager may include additional portfolio constraints in the quadratic optimization problem that put limitations on the maximum and minimum stock weights. The most common additional portfolio constraints are short-sale constraints, which do not allow for a negative weight on any stock; diversification constraints, which restrict any stock from having more than a certain threshold weighting; and sector constraints, which do not allow the composite weight of any group of stocks in a certain sector of the economy to be beyond a certain level.
The portfolio manager must be careful not to impose so many constraints that some of them begin to contradict each other. As a rather obvious example, not all stocks in a portfolio can weigh less
than 5% if the portfolio is limited to 10 stocks; the portfolio will not be fully invested. Typically, portfolio managers impose only the most obvious or needed constraints and let the optimizer do the rest.
9.3.1 No Constraints
Let us first look at how to use MVO without imposing additional constraints. We assume that the portfolio manager already has built a model of expected stock returns and risk either by using one of the models discussed in previous chapters or by using commercial software risk models combined with his or her excess-return models.
The first step is to include all the relevant information about individual stock returns in a vector
μ
and a matrix
Σ
.
μ
is an
N
-dimensional column vector of expected returns of individual stocks, where
N
is the number of stocks in the investment universe.
Σ
is an
N
×
N
matrix of variances and covariances of individual stock returns. That is,
where
E
(
r
i
) is the expected return of stock
i, V
(
r
i
) is the variance of stock
i
’s return, and
C
(
r
i
, r
j
) is the covariance between stock
i
’s return and stock
j
’s return.
A portfolio is specified by a weight vector
w. w
is an
N
-dimensional column vector of stock weights:
where
w
i
is the weight of stock
i
in the portfolio. For
w
to be a valid weight, the sum of all the elements in
w
should be 1. We may define
ι
as an
N
-dimensional vector of 1 such that
The sum of elements in
w
is
or simply
w
′
ι
, which should be 1. For the portfolio specified by weights
w
, the expected return of the portfolio is
or simply
w′
μ
, whereas the risk of the portfolio (i.e., the variance of the portfolio return) is
or, in matrix notation,
w′Σw
. Thus the portfolio that has the minimum risk with the expected return of
μ
P
is the solution to the following minimization problem:
Note that the objective function (
w′Σw
) is a quadratic function of
w
(i.e., the weight terms are squared), whereas the constraints (
w′
μ
=
μ
P
) are linear in
w
. Mathematicians call this problem a
quadratic optimization problem
and have developed a way of dealing with this called
quadratic programming
. In fact, mathematicians would prefer to rewrite the constraints in the following way:
where
We show in
Appendix 9A
that this particular form of the quadratic minimization problem with equality constraints has a closed-form solution. The solution is
Figure 9.1
provides a visual example of the results from a mean-variance optimization. In this particular optimization, we focused on the 32 stocks that comprise the consumer staples sector of the Standard & Poor’s (S&P) 500. We created a five-factor model of security returns using the unemployment rate, consumer senti
ment growth, excess market returns, log of market capitalization, and book-to-price factor. We estimated the economic factor model for the period from January 2016 to December 2020,
6
and we produced forecasts for the expected returns and variances of all stocks for January 2021.
FIGURE 9.1
Efficient frontier for consumer staples sector (January 2021). Based on data from January 2016 to December 2020. Dots indicate the expected returns and the standard deviations of individual stocks. Expected return and standard deviation are annualized and in percent.
After that, we used our mean-variance optimization to create the minimal-risk portfolios for a variety of expected portfolio returns. We first found the stocks with the lowest and highest mean returns. We then began the optimization procedure to minimize risk for a given level of expected return using the expected return
of the lowest expected return stock. Storing the optimal portfolio weights that would create this portfolio, we incremented the mean return and performed the optimization again, finding the optimal weights for that given mean return. We continued doing this until we reached the expected return of the security with the highest mean return. At this point we stopped running the optimization and plotted all the points in the diagram and connected them. The curve that results from these plotted points is typically called the
efficient frontier
in modern portfolio theory, although, technically, the efficient frontier is only the part of the curve whose gradient is positive (the upper half of the curve). Also, since we forecasted the expected returns and variances, we should call this curve the
predictive efficient frontier
.
Typically, we decide how many intervals of expected return and variance we would like to plot. Smaller intervals necessitate more computation but also result in a smoother plot of the efficient frontier. The interval is usually chosen by taking the highest expected return max(
μ
), subtracting the minimum expected return min(
μ
), and dividing by the number of intervals one desires (that is, [max(
μ
)−min(
μ
)]/number of intervals = increment). This value becomes the incremental value to the expected portfolio return in the mean-variance optimization problem. Thus one starts with min(
μ
), computes the optimal portfolio weights, and then recomputes the optimization problem using the portfolio mean of min(
μ
) plus increment. And the process continues until one reaches the maximum expected return.
We also plotted the expected returns and variances of all the individual stocks in the consumer staples sector. (These are represented by dots.) This plot of the efficient frontier completes the process and maps out our portfolio choices. We should decide on the expected-return–expected-risk profile we wish to have and then pick the weights of the stocks corresponding to that profile on the efficient frontier.
Table 9.1
shows the characteristics and composition of selected portfolios along the efficient frontier that we created. We chose to show five portfolios with varying annual expected returns from −5.35% to 18.65%. Every stock in the original universe is included in the portfolios. Stock weights vary from about minus 9.88% to plus 17.64%. Since we did not impose the short-sale restriction, a number of stocks have negative weights. In this table, we show the three largest-weight stocks and the three smallest-weight stocks.
TABLE 9.1
Selected Efficient Portfolios from the Consumer Staples Sector
Let’s look at portfolio C on the efficient frontier. We expect that portfolio C will generate an annualized expected return of 6.65%. The annualized standard deviation is expected to be 7.86%. This optimal portfolio contains 32 stocks. Hormel Foods (HRL) has the highest weighting (12.99%) in this portfolio, and Monster Beverage Corp (MNST) has the lowest weighting (−5.27%). A portfolio manager might like to create a portfolio with a 6.65% annual expected return and a standard deviation of 7.86%, but he or she may not be able to implement the results of this mean-variance optimization. For instance, if he or she is not allowed to short stocks, a 5.27% short of MNST is out of the question. This illustrates why the manager might wish to perform a mean-variance optimization with
additional constraints. We discuss some of the most common additional constraints in the next subsections.
9.3.2 Short-Sale and Diversification Constraints
Portfolio managers may face constraints on their investment portfolios for various reasons, such as legal restrictions or prospectus mandates. The main constraint on a long-only portfolio manager is the short-sale restriction that prevents shorting securities. Mathematically, we can represent the short-sale restriction as the condition that
which indicates that each stock has at least a weight of zero.
This restriction simply can be added to the minimization problem as an additional constraint. This type of constraint, however, is an
inequality constraint
. We show in
Appendix 9A
that when dealing with inequality constraints, the quadratic optimization problem does not have a simple analytical solution and instead requires numerical methods to solve for the optimal portfolio weighting.
Techniques designed to solve this type of quadratic minimization with inequality constraints are known as
quadratic programming
. Most portfolio managers simply need to formulate the constraints, enter them into the commercial software or quadratic optimizer, and let the software/optimizer do the rest. For readers who are more interested in the mathematics of quadratic programming, we discuss it in
Appendix 9A
.
Using the same data as before and a quadratic optimization programming tool, we recalculated the set of efficient portfolios with the additional short-sale constraints using the same approach.
Figure 9.2
plots the efficient frontier. As before, we focused on the same consumer staples sector of the S&P 500 and used the same time period for estimation, January 2016 to December 2020, and the same model for security returns. We then produced forecasts for the expected returns and variances of all stocks for January 2021.
FIGURE 9.2
Efficient frontier for consumer staples sector with short-sale constraints (January 2021). Based on data from January 2016 to December 2020. Dots indicate the expected returns and the standard deviations of individual stocks. Expected return and standard deviation are annualized and in percent.
Compared with
Figure 9.1
, the efficient frontier has shifted to the right owing to the additional short-sale constraint. This makes sense. By adding an additional constraint to the optimization, the lowest-risk portfolio we can create will have a higher risk than the
lowest-risk portfolio we were able to create without the short-sale constraint.
Table 9.2
shows the characteristics and composition of selected portfolios along the efficient frontier. We chose to show three portfolios with target monthly mean returns identical to the portfolios listed in
Table 9.1
. We did not include two portfolios with expected returns of −5.35% and 0.65%. The variances of these portfolios are higher than the variance of portfolio C, so, in the strictest sense, they are no longer efficient portfolios. The minimum-risk portfolio includes fewer stocks to achieve the same expected return. Its maximum stock weights are also higher than in the optimization without constraints. In this table, we show the weights for the five stocks with the largest weights in the optimal
portfolio. Portfolio E is an extreme case in which the entire portfolio consists of just one stock, CHD.
TABLE 9.2
Selected Efficient Portfolios from the Consumer Staples Sector with Short-Sale Constraints
Let’s look again at portfolio C on the efficient frontier. We expect that portfolio C will generate an annualized expected return of 6.65%. This is comparable to portfolio C in the unconstrained case reported in
Table 9.1
. The annualized standard deviation is expected to be 8.23%. Even though this optimal portfolio’s expected return is similar to that of portfolio C in
Table 9.1
, the risk is clearly higher. This optimal portfolio contains 18 stocks compared with the 32 in the unconstrained portfolio, with the highest-weighted stock representing 13.81% of the portfolio. The constraint has removed the extremely negative weighting of MNST, as it should. At first glance, one might be unsatisfied with the results of the mean-variance optimization because this portfolio is not as optimal as the portfolio in the unconstrained case. However, the
new portfolio will satisfy the needs of a long-only portfolio manager, demonstrating why it is useful to perform a mean-variance optimization with short-sale constraints.
In addition to short-sale constraints, portfolio managers also may wish to have
diversification constraints
. These are constraints that a mutual fund accepts in compliance with the diversification requirements of the Investment Company Act of 1940.
7
Of course, even if a portfolio manager is not regulated by the Securities and Exchange Commission (SEC), he or she may wish to follow maximum-weight constraints because too much exposure to very few stocks also increases the portfolio’s diversifiable risk. Restrictions of this kind generally can be expressed as
where
w
and
are
N
-dimensional vectors of maximum and minimum allowed weights. This constraint can be added easily to the optimization problem and satisfies both the short-sale constraint and the diversification constraint simultaneously.
9.3.3 Sector or Industry Constraints
Many portfolio managers—especially those who manage against a benchmark—wish to constrain the sector weightings of the portfolio. Here is a simple modification to the framework to constrain sector weightings:
where
w
j
represents the weight of sector
j
in the portfolio.
8
9.3.4 Trading-Volume Constraint
One of the typical constraints that portfolio managers add to the optimization is the trading-volume constraint. This is particularly relevant when the value of the portfolio is large and the portfolio manager’s transactions have a large price impact.
9
To avoid creating negative price impact, the portfolio manager may restrict the holding of each stock to keep it below some threshold amount, typically a fraction of the average trading volume of each stock.
Suppose that the value of the portfolio is $500 million and that the portfolio manager wants to keep the holding of one stock below 10% of the average daily trading volume of the stock (ADV). If
w
i
is the portfolio weight of stock
i
and
x
i
is the average trading volume of stock
i
measured in millions of dollars, then the constraint is 500
w
i
≤ 0.1
x
i
or
w
i
≤ (0.1/500)
x
i
.
In general, the trading volume constraint can be expressed as
where
x
is a vector of average daily trading volume in dollar terms, and
c
is a constant indicating the threshold.
9.3.5 Risk-Adjusted Return
So far we have formulated the mean-variance optimization problem as a risk minimization. Some portfolio managers may prefer an alternative formulation with expected return maximization. The expected return maximization can be written as
and other constraints. The expected return maximization may be more useful if the portfolio manager has a specific target risk level
, whereas the risk minimization may be more useful if the portfolio manager has a target expected return.
10
When the portfolio manager has neither a target risk nor a target expected return, the mean-variance optimization can be expressed in terms of
risk-adjusted
expected return. We can adjust
the expected return for the risk by subtracting some multiple of the risk, that is,
μ
P
−
A
. The multiplier
A
is called the
risk-aversion parameter
because a high value of
A
indicates that the portfolio manager considers the risk very costly. If the value of
A
is 2, it means that the portfolio manager equates a 1% increase in the variance with a 2% decrease in the expected return. Once the value of the risk-aversion parameter is decided, the mean-variance problem becomes
This formulation turns out to be quite useful in certain applications.
11
9.4 BENCHMARK
Most portfolio managers manage the portfolio versus a benchmark. Managers who stick very closely to the benchmark sometimes are referred to as
index managers
, but managers who manage very loosely with respect to the benchmark are described more accurately as
active managers
or
enhanced index managers
. The goal of active managers is to produce a portfolio of stocks that is broadly similar to the underlying benchmark but that outperforms the benchmark by some amount. The manager must walk a fine line in order to outperform the benchmark without diverging dramatically from it. Fortunately, when the benchmark itself is not efficient, these two goals do not conflict.
12
There is a whole set of tools to deal with tracking a benchmark while producing
α
(outperformance) over the benchmark. We will describe a number of these in the following sections, including ad hoc methods, stratification, factor exposure targeting, and tracking
error minimization. The last method is the most popular because, in theory, it provides the tightest control on risk versus the benchmark while still allowing the portfolio manager to select his or her favorite stocks.
9.5 AD HOC METHODS AGAIN
One rather simplistic approach to weighting a benchmarked portfolio so that it follows the benchmark closely is to select the largest holdings of the benchmark for the portfolio. If the portfolio is going to include 50 stocks, this would amount to choosing the 50 stocks with the largest market capitalization in the benchmark and then possibly computing the weights of the 50 stocks according to their relative market capitalizations. A manager could further tilt the weights slightly toward his or her preferred stocks. There are a number of ad hoc methods for tilting the weights toward preferred stocks. Let’s assume that the portfolio manager has ranked the stocks by the aggregate Z-score methodology described in
Chapter 5
.
13
The portfolio manager should renormalize the aggregate Z-scores so that the sum of the Z-scores of the subset of 50 stocks (or whatever number of stocks he or she chooses) is equal to 0. The steps to alter the relative market capitalization weighting are as follows: First, the portfolio manager should decide what is the maximum percentage deviation in weight he or she is willing to allow from the market-cap weighting for the maximum absolute Z-score value. Call this
η
. The second step is to find the maximum absolute Z-score of all the stocks in the universe of 50 stocks. Thus, take the absolute value of all the individual Z-scores and find the maximum; call this
z
max
. The third step is to compute the Z-score multiplier
m
=
η
/
z
max
. The fourth step is to compute the new weights
of the portfolio such that (
=
w
i
+
mz
i
), where
w
i
is the relative market capitalization weight within the benchmark.
14
The adjusted portfolio is complete.
As a brief example of this method for creating an altered market-capitalization portfolio to track the benchmark with the top
N
stocks by market capitalization, we selected the top 30 S&P 500 stocks and modified the relative market capitalization weights using the Z-scores methodology used in
Table 5.2
. The modified weights as well as the relative weights and the Z-scores are shown in
Table 9.3
. By altering the portfolio in this way, the portfolio manager can continue to track the benchmark relatively closely while still altering the stock weights to take advantage of his or her
α
model.
TABLE 9.3
Ad Hoc Modified Market-Cap Weights to Reflect Z-Score Model
Although this is certainly one type of ad hoc method to compute portfolio weights while still tracking the benchmark, it will not be the best solution. For one, there was no attempt to choose the portfolio based on minimum tracking error versus the index. Thus there will be no control of other risk factors or of asset-specific risk in the portfolio. Almost surely it will not be the optimal portfolio. Moreover, the relatively small number of stocks in the portfolio (30 in our example) represent only a fraction of the total market capitalization of the benchmark (less than 50% in our example). Though simple, this is an inefficient way to choose the stocks.
Other ad hoc methods are possible, but a professional portfolio manager will be dissatisfied with them despite their simplicity. Ultimately, a manager wants to quantify his or her risk versus the benchmark, something that simply is not possible with these other, rather amateurish mechanisms.
9.6 STRATIFICATION
Stratification or stratified sampling is another simple way to build portfolios while maintaining a very rudimentary risk control mechanism. Stratified sampling was devised primarily for empirical statisticians who wanted to understand the characteristics of a population but could not afford to gather observations on every member of the population. One method to create a representative sample of the population would be to randomly select members of the universe. While this method converges to the true mean and
standard deviation of the population, we can improve on it by first stratifying the sample and then choosing a certain number of observations within each stratum.
15
We assume that the portfolio manager already has predicted the excess returns of all the stocks in his or her universe. His or her goal is to choose the high-
α
stocks while controlling risk versus the benchmark. The stratification method involves minimizing the exposures of the portfolio along many dimensions of risk. The first stage of stratification is to stratify the universe of stocks by dividing it into
J
nonoverlapping groups. We might want to stratify, for instance, by dividing the stocks into industry buckets so that each stratum represents a different industry. Call the number of stocks in stratum
j, N
j
. The total stocks in the universe can be represented by
N
. Thus
.
The next step in stratified sampling with one subgroup classification is to select representative stocks from each stratum. At this point the portfolio manager will have to decide how many stocks he or she wants in the portfolio. Let’s call this number
N
P
. The idea of stratification is to select a proportion of stocks from each stratum that is representative of the universe of stocks. Thus, from each stratum, the portfolio manager should choose
N
j
N
P
/
N
stocks. This value may need to be rounded to the nearest integer. In traditional stratified sampling, an index portfolio manager would select the stocks at random, which is a valid procedure for just replicating the characteristics of the index. Beyond pure mimicry, though, a manager ought to maintain some risk controls while picking the high-
α
stocks. Thus, before making selections of stocks from each stratum, he or she should rank the stocks in each stratum according to aggregate Z-score, expected return, excess expected return, or
α
and then choose the stocks with the highest values of the chosen criterion. For example, if the stock universe is divided into sectors and four stocks must be chosen from the transportation sector, those four stocks could be the ones with the highest relative ranking according to future risk-adjusted returns.
Of course, a portfolio manager might wish to create more than one subgroup classification to control risk. This can be accomplished by dividing the universe of
N
stocks into a group of
J
categories based on one classification and then dividing each group into subgroups, and so on and so forth. For example, to divide the
universe of stocks into two subgroup classifications, we could divide them by industry and then by size.
Figure 9.3
depicts the stratification of the universe of stocks into two subgroup classifications based on 9 industry groups and 3 size groups (large, medium, and small). With the stocks separated into 27 separate groups, or buckets, the manager ranks them according to highest Z-score or some other excess-return criterion. He or she selects stocks from each subgroup based on the formula
N
j
N
P
/
N
rounded to the nearest integer.
FIGURE 9.3
The stratified-sample approach.
Stratification is an easy way to choose one’s preferred stocks while also controlling the risk via broad diversification. A portfolio manager might have an
α
model that, left to its own devices, tends to select stocks in one particular industry. Stratifying across industries or sectors ensures broad diversification and risk control versus the benchmark. The biggest drawback to stratification is that it is a fairly rudimentary method for controlling risk. Most professional portfolio managers would be averse to using it because it does not precisely quantify ex ante how much risk they are taking. Managers ought to be able to quantify their risks using all the available information. Clearly, stratification lacks a precise, quantitative control mechanism.
9.7 FACTOR EXPOSURE TARGETING
Another way to bring the portfolio in line with the benchmark is to set the benchmark’s factor exposures as target factor exposures for the portfolio. Or one may set the portfolio’s overall beta with respect to the benchmark equal to (or very close to) 1.
16
The benchmark beta of any portfolio is simply the weighted average of the benchmark betas of the individual stocks. Let
β
be an
N
-dimensional column vector of the benchmark beta of individual stocks, that is,
where
β
i
is the beta of stock
i
with respect to the benchmark. The beta of the portfolio equals
w
′
β
. We can add the following constraint to the optimization problem:
Or we can specify some range for the portfolio
β
instead:
Let us return to the consumer staples example. In the example we created the efficient frontier given a short-sale constraint. Now let us add a constraint that requires the
β
of the portfolio with respect to the benchmark to be no less than 0.85. The benchmark for the portfolio manager in this case is the value-weighted (i.e., market-cap-weighted) return of all stocks in the consumer staples sector. Other than our new constraint, the computation here is based on the same model and the same data as in Tables 9.1 and 9.2.
Table 9.4
shows the selected minimum-risk portfolios created from 32 stocks in the consumer staples sector with the restriction on the benchmark
β
. Portfolio A (with a mean return of −5.35%) and portfolio B (with a mean return of 0.65%) are not reported because there is no minimum-variance portfolio with either of those mean returns owing to the additional constraint.
TABLE 9.4
Selected Efficient Portfolios from the Consumer Staples Sector with Short-Sale and Benchmark
β
Constraints
We imposed an inequality constraint on the portfolio requiring that the market
β
be no less than 0.85. In the case of portfolios A and B, since the betas of the portfolios turned out to be exactly 0.85, which hit our minimum requirement, the constraint was binding. Since the constraint was binding, the variances of these portfolios
are greater than the variances of the portfolios constructed in Tables 9.1 and 9.2. The compositions of these new portfolios also differ significantly from the compositions of the previous portfolios.
While we began with the simple case of targeting the portfolio’s benchmark
β
to a specified range, we may prefer to stipulate a range for each of the portfolio’s other factor exposures as well. This is sometimes referred to as
factor tilting
because we are tilting the portfolio toward greater exposure to certain factors and less exposure to others, according to our view on the factors and upcoming market conditions. If a portfolio manager believes that the market will rally, for instance, he or she may wish to have a higher market
β
than that of the benchmark while keeping all other factor exposures equal to those of the benchmark. He or she would tilt the portfolio toward the market factor.
The factor exposure of a portfolio is the weighted average of the factor exposures of individual stocks. Let
B
be an
N
×
K
matrix of factor exposures of individual stocks. That is,
where
K
is the number of relevant factors, and
β
ik
is the exposure of stock
i
to factor
k
. Then the factor exposure of a portfolio with weight
w
is simply
B′w
. Thus we may add the following general factor exposure constraint:
The portfolio manager can exercise his or her particular management style through this sort of constraint. Assigning a minimum exposure (say, 0.9) to the growth factor orients the portfolio toward growth investments. If the first factor is the growth factor, then the manager would set the first element of
β
to 0.9.
9.8 TRACKING-ERROR MINIMIZATION
9.8.1 Direct Computation
Most professional portfolio managers with a benchmark use the minimization-of-tracking-error approach to weighting stocks and building a portfolio. There are two ways to formulate the optimization problem using this approach. One way is to minimize the tracking error for a given expected excess return over the benchmark, and the other is to maximize the expected excess return over the benchmark without exceeding a maximum tracking-error constraint. The former approach is explained in this subsection, and the latter approach is explained in Section 9.8.4. We prefer the latter formulation because it is more realistic. In the practical application part of this book (
Chapters 16
and
17
), we use the latter approach.
Typically, the portfolio manager would like to use all his or her tracking-error constraints so long as he or she is adding to the expected excess return over the benchmark. Tracking-error constraints vary from portfolio to portfolio but can range from as little as 0.5% per annum to 10% per annum. The investment committee of the investment management firm often comes up with the tracking-error constraint, but sometimes portfolio managers choose to be even more conservative than required by the committee’s constraint. Fortunately, the quadratic optimization framework we have already discussed is applicable to tracking-error minimization. We need only make slight modifications to the optimization problem.
Tracking error
(
TE
) is defined by most portfolio managers as the standard deviation of portfolio returns minus benchmark returns.
17
Thus
where
S
(·) is the standard deviation function.
The first method for minimizing the tracking error of the portfolio is to minimize it given some expected level of excess returns over the benchmark. Now consider the components of the variance term
18
:
The last term, the variance of the benchmark, is beyond our control. Thus, to find a portfolio that minimizes the tracking error of the portfolio, we minimize
V
(
r
P
) − 2
C
(
r
P
, r
B
).
Given the portfolio weight
w
, the variance of the portfolio is given as
w′Σw
. The covariance between the portfolio and the benchmark can be computed from the covariances between individual stock returns and the benchmark return. Let
γ
be an
N
-dimensional vector of the covariances between individual stock returns and the benchmark return:
Then the covariance between the portfolio return and the benchmark return equals
w
′
γ
.
To find the portfolio that minimizes tracking error, we need to solve the following quadratic minimization problem:
The same quadratic programming routine that was used in the preceding section can solve this problem as well. Typically, the chosen portfolio mean
μ
P
will be some excess return over the benchmark. Practically, we should think of
μ
P
=
μ
B
+
δ
. That is, we should take the expected return of the benchmark and add a small amount to it according to our desire and then run the optimization to find the portfolio weights. Just as in the case of a portfolio with no benchmark, we will see shortly that we can again add various additional constraints, such as the short-sale, diversification, and style constraints.
9.8.2 Tracking by Factor Exposure
There is an alternative but equivalent representation of the tracking-error minimization problem. Recall from
Chapters 6
and
7
that the variance of an individual stock
i
can be estimated as
Assuming that the covariance between the residuals of the stocks is 0, we can write the variance-covariance matrix of all stock returns as
where
B
is an
N
×
K
matrix of factor exposures,
V
(
f
) is a
K
×
K
matrix of factor premium variances and covariances, and
V
(
ϵ
) is an
N
×
N
diagonal matrix of error variances. Given this, the squared tracking error is
where
w
P
is the weight of the portfolio, and
w
B
is the weight of the benchmark. Once other relevant constraints are added, this tracking-error minimization problem can be solved using the quadratic optimizer.
19
Table 9.5
shows the minimum-tracking-error portfolio created from 32 stocks in the consumer staples sector. The table is based on the same model and data as in Tables 9.1, 9.2, and 9.4. The benchmark is the value-weighted portfolio of 32 stocks in the consumer staples sector, which is identified as portfolio A in the table. As we try to obtain higher expected returns, the tracking error increases. To obtain a 5.29% (6.65% − 1.36%) excess return over the benchmark (portfolio C), the portfolio manager can expect a tracking error of 1.79%. To obtain a 17.29% excess return over the benchmark (portfolio E), the portfolio manager must accept an expected tracking error close to 20%.
TABLE 9.5
Selected Portfolios from the Consumer Staples Sector by Minimizing Tracking Error with Short-Sale Constraints
Minimizing tracking error will force the factor exposures of the portfolio to be quite close to those of the benchmark, so the first term in
Eq. (9.29)
will be less significant than the second term. In fact, when the portfolio manager has specific desired values for portfolio factor exposures, the first term can be completely dropped. In this case the optimization problem is specified simply as minimization of the variance of error terms subject to the additional constraint on the portfolio factor exposure. This is a type of
factor tilting
.
Suppose that the portfolio manager wants to tilt the portfolio toward small growth stocks but in all other respects wants the portfolio’s exposures to remain identical to those of the benchmark. He or she can achieve this by setting the portfolio’s exposures to the size factor and the growth factor higher than the benchmark’s exposures to those factors while keeping its other factor exposures equal to those of the benchmark. For example, if there are five factors—market return, log of market capitalization, GDP growth, unemployment, and consumer sentiment growth—then he or she can add the following constraints:
where
The zeros in vector
d
will make sure that the portfolio’s exposures to the market return, unemployment, and sentiment factors are identical to the benchmark’s exposures to those factors. The value of 0.1 in vector
d
will make sure that the portfolio’s exposures to the size and growth factors will be higher than the benchmark’s exposure to those factors by 0.1. With factor tilting, the optimization problem becomes
subject to
Eq. (9.30)
and any other constraints.
9.8.3 Ghost Benchmark Tracking
There may be cases in which the portfolio manager does not know the weights of the underlying benchmark’s securities or he or she cannot estimate all the benchmark’s factor exposures. In this case, the minimization of tracking error involves minimizing the tracking error with respect to the stream of historical returns on the benchmark.
The tracking-error formula must undergo some modification because we do not know the benchmark weights. After some manipulation of the equation, the squared tracking error becomes
In this equation,
β
B
is the benchmark’s factor exposure, and
ϵ
B
is the benchmark’s error term. Once the tracking error is defined, the tracking-error minimization can proceed as described earlier.
9.8.4 Risk-Adjusted Tracking Error
In practical situations, the portfolio manager may have some maximum tracking-error constraint, say, 3% per annum. He or she can keep increasing the expected excess return until he or she reaches the tracking-error constraint. This problem is essentially identical to what we discussed so far. The objective function will be the expected return of the portfolio rather than the tracking error, and the constraint will include the tracking error rather than the expected return. Mathematically speaking, given the target tracking error of σ
x
,
and other constraints.
If there is neither a target tracking error nor a target mean, then the problem might be expressed in terms of the tracking-error-adjusted expected return. As we did for the risk-adjusted return, we can adjust the expected return for the tracking risk by subtracting some multiple of the squared tracking error
. The multiplier
A
is called the
tracking-error aversion parameter
because a high value of
A
indicates that the portfolio manager considers the tracking error very costly. Then the problem becomes
subject to other additional constraints.
Note that there is an important relationship between the two formulations. The set of maximum-return portfolios that we obtain as we vary the target tracking error σ
x
is identical to the set of optimal portfolios that we obtain as we vary the tracking-error aversion parameter
A
. That is, we can always choose the target tracking error σ
x
or the tracking-error aversion parameter
A
so that the two formulations are equivalent. This property can be quite useful in the optimization process. A commercial software package may not support maximizing the expected return subject to a quadratic constraint.
20
In such a case we can maximize the tracking-error-adjusted expected return [i.e.,
Eq. (9.35)
] for a certain value of
A
. After the maximization, we can check whether the tracking-error constraint is satisfied. If not, we change the value of
A
and continue this process until we satisfy the tracking-error constraint. The value of
A
that makes the optimal portfolio satisfy the tracking-error constraint
can be found in a small number of iterations using the property that a higher value of
A
reduces the tracking error of the optimal portfolio. This is the approach we follow in Part V of this book.
9.9 CONCLUSION
In this chapter we showed how to turn the factor model’s predictions of stock return and risk into a portfolio through various methods of stock weighting. As we saw, there are a number of very simple ad hoc ways to assign weights in a portfolio that are not measured against a benchmark, but they do not allow the portfolio manager to maintain good control of the risk of the portfolio. For nonbenchmarked portfolios, we instead recommended mean-variance optimization (MVO), which maximizes the portfolio’s return and minimizes its risk while also allowing the manager to impose certain constraints on the portfolio’s characteristics. More often than not, though, managers try to track a benchmark with their portfolios, so we turned our attention to weighting methods that take into account the relationship between the portfolio and the benchmark. Again, we found that ad hoc methods failed to provide anything more than quick-and-easy but incomplete fixes to the weighting problem. The stratification method was an improvement over ad hoc methods because it offered a very rough risk control mechanism by allowing us to divide stocks into groups and select samples from each group. The factor exposure method also controlled for risk, and it let us “tilt” the portfolio’s beta toward the factors that we thought were most important. We saw, however, that the best method of weighting stocks in a benchmarked portfolio is tracking-error minimization because it minimizes the portfolio’s tracking error, or risk, without compromising returns (or, conversely, it maximizes the portfolio’s return without exceeding a certain tracking error). This method of weighting achieves the highest possible return for the least possible relative risk, works even when the portfolio manager does not know the exact makeup of the benchmark, and allows him or her to place constraints on the portfolio. We have completed the portfolio construction process by showing how to design a portfolio that balances the weights of high-quality stocks in the optimal way. Yet even a well-designed portfolio is always a work in progress. As conditions change, the portfolio needs to be rebalanced, and the transactions costs of rebalancing must be considered. The portfolio also should be refined to operate as best as it can within the tax environment. Many managers fail to counteract the draining effect of taxes, yet there are strategies for fortifying a portfolio against the tax drain. We discuss these sorts of improvements in the next two chapters.
1
The reader may wish to review
Chapters 5
,
6
,
7
, and
8
before proceeding with this chapter.
2
The choice of how to determine these values is up to the manager. Some managers use models to forecast the expected stock returns (or
α
) but rely on commercial software to calculate the implicit risks of the portfolio. Other managers build their own risk models.
3
Many portfolios and indices are also
float-weighted
, which has the same sort of characteristics as value weighting, except stocks are weighted by their floating shares, not their shares outstanding.
4
Mathematicians and software programs, however, prefer the formulation in which the objective function is quadratic and the constraint is linear (rather than the other way around). See
Appendix 9A
and
Appendix 9B
for the mathematical details of typical quadratic optimization problems.
5
Chapter 8
discussed methods to measure estimation error. The reader also may be interested in a book that deals with estimation error, such as Michaud (1993). This book is particularly critical of MVO. On page 3, it reads, “MV optimizers function as a chaotic investment decision system. Small changes in input assumptions often imply large changes in the optimized portfolio. The procedure overuses statistically estimated information and magnifies the impact of estimation errors. The result is that the optimized portfolio is ‘error maximized.’”
6
We produce forecasts of the factor premiums using a VAR model as described in
Chapter 8
. We then use the estimated factor exposures along with the forecasts to calculate expected returns and variances.
7
The Investment Company Act of 1940 specified various rules on investment companies, including Section 12d and Section 5b. Section 12d specifies certain investment constraints for diversified and nondiversified mutual funds. One rule prohibits mutual funds from owning more than 5% of other investment companies, which are firms that derive more than 15% of their revenue from securities-related activity and a maximum of 10% of the investment company’s total AUM from such activity. This might be a constraint for any portfolio manager holding any type of banking stocks or investment banking stocks. Section 5b specifies rules for funds that advertise themselves as
diversified
. These funds may not hold more than 5% of their assets in any particular company or hold more than 10% of the voting stock of any company for 75% of the portfolio’s assets. Due to this rule, we like to call the restriction on the maximum weight of a stock in the portfolio the
diversification rule
.
8
Most software packages, such as MATLAB, have a simple way to add upper- and lower-bound constraints to their quadratic optimizer.
9
In
Appendix 10C
, we discuss more direct ways to deal with market impact.
10
In fact, there is one more practical reason why this formulation may be preferred. In the minimization of the risk with a target expected return, there is a danger that the target expected return may not be feasible given the parameters. Thus the portfolio manager may end up getting a portfolio he or she did not wish to obtain, or, even worse, the optimization may fail altogether.
11
This formulation has a theoretical appeal as well. The objective function can be interpreted as an investor’s utility function, and the optimization can be interpreted as an investor’s utility maximization. This is how theory says investors make portfolio decisions. On the other hand, maximizing the information ratio or some ratio of expected return to risk does not have such theoretical appeal.
12
In practice, the benchmark is rarely efficient. A simple way to see whether the benchmark is efficient is to make a plot similar to the one in
Figure 9.1
. On the plot, add a dot corresponding to the benchmark. If the dot is close to the efficient frontier, then the benchmark is nearly efficient. If not, then the benchmark is not efficient. This efficiency, sometimes called
mean-variance efficiency
, may not be the only measure of efficiency. Some prefer to define efficiency with respect to the benchmark. In such a case, of course, the benchmark is always efficient. Minimizing tracking errors when the benchmark is inefficient may lead to inefficient portfolios in a variety of cases. For more on this, see Roll (1992).
13
It is not important for this ad hoc weighting mechanism that the QEPM use the aggregate Z-score methodology. In fact, the manager can use any relative ranking method for the stocks. However, so that the ad hoc conversion mechanism we describe will function properly, the manager should normalize the ranking method so that the sum of all the ranks equals 0.
14
One can see that the new weights will add up to 1 as well so long as σ
N
i
=1
z
i
= 0. This is why it is critical to normalize the aggregate Z-scores or other ranking method among the subset of benchmark stocks.
15
There really are two types of stratified sampling: proportional and disproportional. The one we describe here is proportional random sampling, in which the same proportion is chosen for the sample as is represented in the population. Disproportional random sampling may overweight certain strata with respect to their size in the population for a variety of reasons that will not be discussed here.
16
This, of course, does not control the asset-specific risk, and thus the tracking error is not bounded. That is, controlling directly for asset-specific risk with similar stocks and similar stock weights will imply a rather tight control of factor risk, but controlling for factor risk will not necessarily imply a tight control on asset-specific risk.
17
For further details on tracking error, including how to measure it ex post, see
Chapter 15
. If the standard deviation of the difference between the portfolio return and the benchmark return is zero, but the expected values of the two returns are different, do we have a perfect tracking portfolio? Of course, the answer is no. The tracking error, as defined above, however, would misleadingly equal zero because it ignores the expected difference in returns. A better way of measuring the tracking error is to use the root mean squared error (RMSE). RMSE is defined as
RMSE accounts for the expected value of the difference as well as the variation in the difference. The RMSE equals the tracking error as previously defined only if there is no difference between the expected return of the portfolio and the benchmark. Fortunately, however, whether we use RMSE or the standard deviation to measure tracking error, the optimal portfolio selection problem is not affected (see the questions at the end of this chapter). For this reason, and also to follow convention, we use the standard deviation as the measure of the tracking error.
18
We obtain this by the standard statistical result that
V
(
a
−
b
) =
V
(
a
) +
V
(
b
) − 2
C
(
a, b
).
19
Since minimizing squared tracking error is equivalent to minimizing tracking error, we will refer to them interchangeably when disussing the optimization problem.
20
IBM’s CPLEX package does provide this functionality. It is discussed in more depth throughout this book, especially in
Appendix 9B
.
