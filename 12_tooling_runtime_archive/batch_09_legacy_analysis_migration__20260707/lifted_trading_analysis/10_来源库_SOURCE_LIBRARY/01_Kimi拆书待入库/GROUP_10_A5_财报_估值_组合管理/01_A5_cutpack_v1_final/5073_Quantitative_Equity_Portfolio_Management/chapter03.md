# Quantitative Equity Portfolio Management: An Active Approach to Portfolio Construction and Management, Second Edition

- **book_name**: 5073 Quantitative Equity Portfolio Management, Second Ed.
- **main_source**: epub
- **cross_check_source**: none
- **pdf_role**: not_needed
- **split_scope**: chapter file = chapter03

---

CHAPTER 3
Basic QEPM Models
The greatest work is inside man
.
—Pope John Paul II
3.1 INTRODUCTION
The central, unifying element of quantitative equity portfolio management (QEPM) is the quantitative model that relates stock movements to other market data. Quantitative equity portfolio managers create such models to predict stock returns and volatility, and these predictions, in turn, form the basis for selecting stocks for the portfolio.
Some readers may wonder whether it is necessary to know how to make quantitative models from scratch when there are so many excellent commercial software packages with prepackaged models. When a portfolio manager relies completely on commercial software, he or she may not be able to use all the information available to him or her. Different models make use of different types of information, and any given software program likely ignores some relevant information. If the portfolio manager tries to be “creative” and combine his or her own calculations with a prepackaged model, the resulting hybrid most likely will violate the information criterion. Some dependence on commercial software may be unavoidable,
1
but with an understanding of the modeling process,
the manager will know how to get the most out of the software, what to do with it, and what not to do with it.
We begin this chapter by discussing the two basic models of QEPM. As we discuss these models, we consider how they fit into the entire construction of the portfolio, from picking factors to determining the portfolio weights. It turns out that the basic models of QEPM share many properties and produce similar portfolios in certain circumstances. We explain the equivalence of the models in Section 3.3. Portfolio managers often combine one of the basic models with some ad hoc model of stock returns. In Section 3.5 we discuss how these combinations are attempted and why they are not advisable in light of the information criterion. Section 3.6 weighs the basic models’ strengths and weaknesses and discusses reasons for using one rather than the other.
3.2 BASIC QEPM MODELS AND PORTFOLIO CONSTRUCTION PROCEDURES
The central idea of modern financial economics is that the average return of a stock is the payoff to the shareholder for taking on risk. Factor models express this risk-reward relationship.
Factors
are explanatory variables that represent different types of risk. A factor model shows that the average stock return is proportional to the stock’s exposure to the risk that the factor represents (the
factor exposure
) and to the payoff for each unit of exposure to the risk (the
factor premium
).
There are two generic factor models in QEPM that are used to determine how stock returns and risks vary with factors. They are the
fundamental factor model
and the
economic factor model
. The models take their names from the types of factors typically associated with them. The fundamental factor model uses fundamental factors, which are stock characteristics such as the P/E ratio and market capitalization. The economic factor model was developed originally for macroeconomic variables such as gross domestic product (GDP) and inflation, but it is general enough to handle other types of factors as well. While the models are distinguished in name by the types of factors that go into them, it is important to understand that, in addition,
the fundamental factor model and the economic factor model employ different techniques for modeling stock returns
.
Both the fundamental factor model and the economic factor model are based on the principle that the average stock return is determined by the product of the
factor premium
and the
factor exposure
. The factor premium measures how much investors are willing to pay for each factor, whereas the factor exposure measures how sensitive the stock return is to a factor. The factor premium and factor exposure operate differently in the fundamental and economic factor models. Factor exposures are directly observable for the fundamental factor model but not directly observable for the economic factor model. For the fundamental factor model, the exposures of fundamental factors can be read straight from companies’ financial statements and other data sources. For the economic factor model, each stock’s exposure to economic (or other) factors is not observable and instead must be estimated from the historical relationship between stock returns and factor premiums.
The factor premium functions in almost the opposite manner in the two basic models. In principle, the factor premium is not observable and must be estimated. This is the case in the fundamental factor model, for which the factor premium must be estimated from the historical relationship between stock returns and the factor exposures. In the economic factor model, however, the factor premium can be determined up to a proportionality without a statistical estimation in certain cases. In other cases, it is determined by constructing
zero-investment portfolios
or through a mathematical method called
principal-component analysis
. We will explain these methods a little later.
Table 3.1
summarizes the different ways that the basic QEPM models estimate the expected returns and risks of stocks. The specific steps involved in constructing a portfolio depend partly on which model is used. In the remainder of this section we summarize the procedures of portfolio construction from A to Z, beginning with the factor choice and ending with the assignment of portfolio weights. The procedures outlined in this overview will be discussed in detail in subsequent chapters.
TABLE 3.1
How Expected Return and Risk Are Determined in Basic QEPM Models
3.2.1 Factor Choice
The first step toward building a quantitative portfolio is choosing factors that seem to drive stock returns. Good factors are really the secret sauce of QEPM. All quantitative portfolio managers are at
least reasonably proficient at using the various types of quantitative models. What distinguishes one manager from another is the particular set of factors that he or she uses in his or her model. Managers use a wide variety of factors to explain stock returns, but not all factors can be used in all models. The fundamental factor model restricts factor choice somewhat because it typically takes only fundamental factors. The economic factor model is more flexible, allowing for both economic factors and all fundamental factors. We catalog many factors and discuss how to choose them in
Chapter 4
, so for the rest of this chapter’s discussion on portfolio construction we shall assume that we have already completed the first step of portfolio construction and chosen
K
factors to represent the behavior of stock returns.
3.2.2 The Data Decision
The data set for the model is determined with a type of factor model and a set of factors in mind. A data set has two dimensions: the
cross-sectional dimension
and the
time-series dimension
. The cross-sectional dimension defines a data set by the characteristics of the stocks it includes. One may decide to gather data on stocks in a specific industry, stocks in the Standard and Poor’s (S&P) 500, or all stocks traded on the New York Stock Exchange (NYSE). The cross-sectional dimension of data matters because the attributes of
the data set will affect the attributes of the ultimate portfolio and because the number of stocks included in the data set will affect the ease of estimation. The time-series dimension concerns the
periodicity
of the data (i.e., the time intervals at which data points were recorded) and the time
period
of the entire data set. The data could have been recorded daily, weekly, monthly, quarterly, or annually. The entire set of data could cover a few years or just one. The periodicity and the period of the data may affect parameter stability and parameter uncertainty.
2
Given the model and the data set, the portfolio manager may have to make a few more decisions. If the portfolio manager measures his or her performance against a benchmark, which is typically the case, there is the question of whether to include the benchmark itself as a factor in the model. Also, the portfolio manager should decide whether to use the gross return or the logarithm of the return and whether to use the return in excess of a risk-free rate.
3.2.3 Factor Exposure
Once the portfolio manager has chosen the factors and defined the data set, it is possible to determine the factor exposure and factor premium. We begin with the factor exposure, also referred to as
factor loading
. In the fundamental factor model, determining the factor exposure is fairly straightforward. For example, if the factor is the P/B ratio, the factor exposure of stock
i
is the latest observed value of the P/B ratio for stock
i
. (The factor also could be something more complicated, such as an average of the P/B ratio or a forecast of the P/B ratio.)
We will now introduce some mathematical symbols to represent the factor exposure. Suppose that there are
K
factors chosen for the model. We denote the
K
factor exposures of stock
i
by
β
i
1
,…,
β
iK
. If the first factor in the model is the P/B ratio, then
β
i
1
is the P/B ratio of stock
i
.
3
In the economic factor model, because the factor exposure is not directly observable, the factor premiums must be determined first (we explain how in the next section). Then the factor exposure can be estimated from the relationship between returns and factor premiums. We denote the factor premium of
K
factors as
f
1
,…,
f
K
. Given the factor premium, the following equation for the return of stock
i, r
i
, can be estimated:
where
β
i
1
,…,
β
iK
are the factor exposures of stock
i
, whereas
α
i
is the constant term of the equation. The last term,
ϵ
i
, is the error, which reflects the random nature of returns. The equation is typically estimated by a time-series regression using observations made at various time periods. That is, the portfolio manager takes factor premiums, which are the variables of interest that affect stock returns, and regresses stock
i
’s returns at every time interval in the data period on the corresponding factor premiums. The estimate from this regression becomes the factor exposure. For example, the factor premium
f
j
might be real GDP growth. The factor exposure
β
ij
found by estimating the regression shows how sensitive stock returns are to real GDP growth.
3.2.4 Factor Premium
The quantitative portfolio manager also must know the factor premium, which is essentially the premium that the market places on exposure to whatever risk a factor represents. If we know that a stock has a high exposure to the P/B ratio factor, for instance, we need to know what kind of return the P/B ratio provides. These two pieces of information together will allow us to predict the return of the stock.
In the fundamental factor model, the factor premium is estimated from the historical relationship between the stock return and the factor exposure. The equations representing the fundamental and economic factor models are identical to
Eq. (3.1)
, but whereas in the economic factor model the factor exposures
β
i
1
,…,
β
iK
need to be estimated, in the fundamental factor model the factor premiums
f
1
,…,
f
K
must be estimated. The factor premium for the fundamental factor model is estimated by means of either cross-sectional regression, which involves using observations
for various stocks at a single point in time, or panel regression, which entails using observations for various stocks at many points in time.
In the economic factor model, the factor premium is determined first and in various ways depending on the nature of factors. For macroeconomic factors, the values of the variables themselves are taken as factor premiums. For example, if the inflation rate is 3% this month, then the premium for the inflation factor is 3%. This value is not exactly the premium; it does not mean that investors are willing to pay exactly 3% for a unit of stock exposure to inflation. However, the exact premium is proportional to the inflation rate, so for the purpose of forecasting the stock return, the rate itself can be called the factor premium. More generally, the factor premium is calculated by constructing zero-investment portfolios. A
zero-investment portfolio
is a theoretical construct in which the hypothetical investor does not have to invest any capital. For example, if an investor shorts $100 of one stock, theoretically he or she can use the $100 in short-sale receipts to buy $100 of another stock. In the real world, margin requirements prevent such a neat transfer of funds, but for theoretical exercises, it is helpful to imagine such a zero-investment portfolio. We can determine the factor premium by calculating the return on a zero-investment portfolio of investments that exhibit the factor in question. Suppose that size is one of the factors in a model. A zero-investment portfolio could be created for the size factor by going long a small-cap subportfolio and shorting an equivalent amount of a large-cap subportfolio. The factor premium on size would be the difference between the return of the small-cap subportfolio and the return of the large-cap subportfolio.
3.2.5 Expected Return
Whichever factor model is used, estimation of the model provides important information about a stock’s expected returns. The estimation essentially allows us to determine the expected returns of stocks based on their factor exposures and the factor premiums.
3.2.6 Risk
The estimation of the model also provides important information about stock risks. The estimation essentially decomposes the risk of
stocks into two components: nondiversifiable risk and diversifi- able risk.
Nondiversifiable risk
is the primary concern for investors because it comes from a stock’s exposure to risks in the market that cannot be removed from the portfolio. Nondiversifiable risk is represented by
α
i
+
β
i
1
f
1
+ … +
β
iK
f
K
in
Eq. (3.1)
.
Diversifiable risk
, on the other hand, can be removed from the portfolio by diversifying holdings. It is captured by
ϵ
i
. Diversifiable risk is often called the
stock-specific risk
. By calculating the variance or the standard deviation of each component of risk, we can estimate the stock’s total risk.
3.2.7 Forecasting
Expected stock returns are simply the product of the factor premiums and the factor exposures. Once the stocks’ risk levels have been determined, the portfolio manager has gathered all the information needed to construct a portfolio. But he or she does not have all the information to construct an optimal portfolio. The factor premiums and factor exposures in the model are determined from past data. The relationships among return, exposure, and premium are likely to change in the future. The portfolio manager wants to know
future
values, not historical values. In all likelihood, the factor exposure will not change in the immediate future, but the factor premium
is
likely to change in a very short amount of time. Thus it is usually necessary to forecast the factor premium. We explain how to forecast it in
Chapter 8
.
3.2.8 Security Weighting
With the estimates of stock returns and risks based on the new forecasts, the portfolio manager can use optimization techniques to select the stocks for the portfolio and assign them their respective weights. The weighting of stocks in the portfolio can be set to maximize the portfolio’s overall return, minimize its risk, and satisfy other constraints such as diversification requirements and specific investment style requirements. Alternatively, the portfolio manager may decide to minimize the tracking error between the portfolio and the benchmark. This issue is explored fully in
Chapter 9
.
3.3 THE EQUIVALENCE OF THE BASIC MODELS
The fundamental factor model and the economic factor model are built on the same principle: The expected stock return can be expressed as the product of the factor exposure and the factor premium. Therefore, it is not surprising that the two models produce identical portfolios when certain assumptions are satisfied. The equivalence of the factor models can be established starting with the following proposition:
LEMMA 1 (THE EQUIVALENCE OF FACTOR MODELS)
The fundamental factor model and the economic factor model are equivalent to each other if the expected stock return is a linear function of the fundamental factor exposure
.
If the fundamental factor model is a correct model, then the economic factor model is also a correct one.
4
The proof of this claim proceeds in the following way: First, we assume that expected stock returns are a linear function of fundamental factor premiums, as described by the fundamental factor model. Then, under this assumption, we show that the expected stock return can be expressed as a linear function of the factor exposure, as described by the economic factor model.
Let us first express the stock return using the fundamental factor model. If there are
K
factors, then the return of stock
i, r
i
, is
where
x
i
1
,…,
x
iK
are the factor exposures of stock
i, π
1
,…,
π
K
are the factor premiums, and
c
i
is the constant term of the equation. For this section only, we have deliberately changed the notation to distinguish the fundamental factor model from the economic factor model.
What happens if we use the same
K
factors but in the economic factor model? Does the economic factor model correctly describe stock returns? The answer is yes. All we need to show is that the expected stock return can be expressed as a linear function of the factor premium, as described by the economic factor model.
We provide the proof for the case in which the factor exposures are independent of one another.
5
In the economic factor model, the factor premium is determined by constructing the zero-investment portfolio. To determine the premium of factor
k
, one could distribute all stocks into two or three groups based on the value
x
ik
. Suppose that each stock is assigned to one of three groups: a high group
, a low group (if
, and a middle group (with the cutoff values
and
). The factor premium
f
k
is the expected return to the zero-investment position that puts $1 into the high group and shorts $1 in the low group,
6
that is,
If factor exposures are independent, then, using
Eq. (3.2)
, we can rewrite the equation as
where
d
k
is a constant defined as
Using
Eq. (3.4)
, we can rewrite
Eq. (3.2)
in the following way:
This equation shows that the expected stock return can be written as a linear function of the factor premiums. In fact, it shows the exact relationship between the fundamental factor model and the economic factor model. The constant term in the economic factor model (
α
i
) is identical to the constant term in the fundamental factor model (
c
i
). The factor exposure in the economic factor model (
β
ik
) is proportional to the factor exposure of the fundamental factor model (
x
ik
/
d
k
).
For practitioners, the equivalence of the factor models means that to the extent that the fundamental factor model is a correct model, it does not really matter whether one use the fundamental factor model or the economic factor model. The two models produce essentially identical results. The only catch is that if the fundamental factor model is not correct, then it is best to use the
economic factor model because it has a stronger theoretical basis than the fundamental factor model does.
3.4 THE SCREENING AND RANKING OF STOCKS WITH THE Z-SCORE
Many portfolio managers screen and rank stocks using
Z-scores
. Sometimes stock screens and rankings supplement the use of a factor model in determining the mix of stocks for the portfolio. More often they are used as alternatives to the factor model. Since screening and ranking are widespread practices among managers, we discuss them more fully in
Chapter 5
.
In the context of stock screening and ranking, a Z-score is a stock’s standardized exposure to a fundamental factor. To calculate the Z-scores for the stocks in some investment universe, we need to know the factor exposures of every stock. Then, for each stock, we subtract the universe’s mean factor exposure from the stock’s individual factor exposure and divide that difference by the standard deviation of factor exposures for the universe. What comes out of this standardization is a set of Z-scores, factor exposures with a mean of 0 and a standard deviation of 1.
For example, suppose that we want to calculate Z-scores for exposure to the P/B ratio. If
β
1
, …,
β
N
are the P/B ratios of stocks 1, …,
N
, then the Z-score of stock
i
is defined as
where
µ
and
σ
are the average and standard deviation of
β
1
, …,
β
N
. The standardization allows us to interpret the Z-score in the following way: If
z
i
is 2, then the P/B ratio of stock
i
is 2 standard deviations away from the average.
Given the Z-score of one factor—or, more commonly, of many factors—portfolio managers can develop a number of screening and ranking strategies. We look at a simple example in the next section and more realistic examples in
Chapter 5
.
3.5 HYBRIDS OF THE MODELS AND THE INFORMATION CRITERION
Practitioners often try to add extra inputs to the basic QEPM models by combining them with ad hoc models. The resulting hybrid models are sometimes reasonable descriptions of stock returns, but
in many cases they have a number of undesirable effects. The most critical problem with hybrids is that they frequently violate the information criterion.
Recall that in order to uphold tenet 4 of QEPM and satisfy the information criterion, a portfolio manager must use all available information in the most efficient way. A hybrid model combining two models that are based on different information may violate the information criterion by combining the two original sets of information inefficiently. If a hybrid model is based on two models that use the same information, the hybrid may violate the information criterion by incorrectly “double counting” the information. Consider the following hypothetical situation: Adam, a portfolio manager, creates a fundamental factor model but decides to combine it with a Z-score analysis. Specifically, Adam calculates the expected return based on the Z-score method and adds this expected return to the fundamental factor model as a constant. Adam uses portfolio management software that implements the fundamental factor model automatically and allows the user to add a constant [i.e.,
α
in
Eq. (3.1)
].
Is Adam using all the available information in the most efficient way? Not if he created the Z-score model and the fundamental factor model from the same data. The addition of the Z-score analysis not only presents no gain, but it in fact also introduces distortion in the model, which will lead to a less-than-optimal portfolio. Even if Adam used different sets of information to create the Z-score model and the fundamental factor model, the two sets of information are still not being combined in the most efficient way. In either case, the hybrid does not satisfy the information criterion. With data on his models and portfolio, we can find out exactly how inefficient Adam’s hybrid is by calculating the information loss. The following numerical example illustrates the problem with patching together two models.
3.5.1 The Setup
Imagine that there are only two stocks in the world, stock
A
and stock
B
. Suppose that current stock returns
r
are determined by the price-to-earnings (P/E) ratios at the end of the previous period. Specifically, we assume
7
where
ϵ
is the random component of the stock return and is assumed to have a normal distribution with a variance of 10 or 20.
8
We also assume that the covariance between the two random errors is zero. Suppose that for the last period
T
, the P/E ratio of stock
A
is 20 and of stock
B
is 10. Therefore, the average P/E ratio is 15 [=(20 + 10)/2], the variance is 25 {= [(20 − 15)
2
+ (10 − 15)
2
]/2}, and the standard deviation is
. Suppose further that the average and the variance are constant over time and across stocks.
Table 3.2
summarizes this assumption and the corresponding calculations of the Z-score.
TABLE 3.2
Price-to-Earnings Ratio and the Z-Score
3.5.2 The Z-Score Model
The Z-score is the normalized factor exposure. To calculate one stock’s Z-score, we subtract the mean factor exposure of all stocks from the individual stock’s factor exposure and then divide that difference by the cross-sectional standard deviation of the factor exposures of all stocks. The Z-score for stocks
A
and
B
are reported in
Table 3.2
. Once the Z-score is calculated, it is possible to estimate the following equation to predict the expected stock return:
where
z
it
is the Z-score of stock
i
at time
t, a
i
is a constant, and
v
i,t
+1
is the error. From the numbers given in
Table 3.2
, the values of
a
A
, a
B
, and
b
are as follows
9
:
and
Given the time
T
value of the Z-score, the preceding estimates imply the following expected returns for stock
A
and stock
B
:
Note that the expected returns of stock
A
and stock
B
are correct. The Z-score model itself does not create any problem with the efficient use of information. The problem arises when the Z-score model is combined incorrectly with other models, as illustrated below.
3.5.3 A Hybrid of the Z-Score Model and a Fundamental Factor Model
Adam first estimated the fundamental factor model, i.e.,
Eq. (3.1)
. Then he did the Z-score analysis. Now he creates his hybrid model by setting the term
α
in the fundamental factor model according to the expected return from the Z-score model. Specifically he adjusts
α
of stock
A
to be 1 and
α
of stock
B
to be −1 so that the sum of
the
α
’s remains equal to 0. For time
T
+ 1, he incorrectly modifies
Eqs. (3.8)
and
(3.9)
into the following:
Given time
T
’s P/E ratio, Adam is going to construct a portfolio at time
T
+ 1 based on the following numbers:
If the weight of stock
A
in the portfolio is
w
, then the expected return and the variance of the portfolio (according to Adam’s calculations) are
To construct his optimal tangent portfolio, Adam finds the value of
w
that maximizes
µ
P
/σ
P
. This value is
w
= 1. Thus 100% of Adam’s portfolio will go into stock
A
and 0% into stock
B
.
3.5.4 Information Loss
Adam thinks that he has created the optimal portfolio, but he is actually not achieving the maximum Sharpe ratio because his estimates of the expected return are not correct. The information loss reveals exactly how much potential Sharpe ratio Adam is losing by combining two models. Let us first determine the maximum Sharpe ratio Adam could have achieved if he had not combined the Z-score analysis with the fundamental factor model. By not combining the models, we obtain the true expected returns of stock
A
and stock
B
:
We should emphasize the fact that the loss of potential returns does not arise from choosing one model over the other. Adam would have found the correct expected return whether he used the Z-score model or the fundamental factor model. It was the combination of the two that muddied the analysis. Given the correct expected return of the individual stocks, the expected return and variance of Adam’s current portfolio (invested 100% in stock
A
and 0% in stock
B
) are
Thus Adam’s portfolio’s actual Sharpe ratio (
SR
) (ignoring the risk-free rate) is
Adam’s current portfolio weights are not optimal. The maximum Sharpe ratio is achieved when
w
= 0.5. When
w
= 0.5, the expected return and the variance of the portfolio are
If the portfolio had been constructed optimally, Adam could have attained a maximum Sharpe ratio of
Given the actual Sharpe ratio and the maximum Sharpe ratio, the information loss (
IL
) is the difference between the two:
The information loss of 0.1005 means that when Adam takes 1% extra risk, his reward for taking that extra risk is 0.1% lower than it could have been. Since Adam is currently taking 4.5% risk, he earns 0.45% less than he could have. He loses 0.45%, or 45 basis points, in expected return by incorrectly combining two models. The moral of the story is clear. The best thing to do is to choose one model and stick with it. Combining basic models is hard to justify in terms of the information criterion. Another practical implication of this example is that there are benefits to building one’s own model at the outset. Many managers want to model information in
a specific way, but prepackaged programs are not flexible to modifications. It does no good to tack an ad hoc model onto the one that the software generates, so designing an entire custom model may be the best course of action.
3.6 CHOOSING THE RIGHT MODEL
It is clearly best to choose just one model of stock returns in order to create the portfolio, but which one of the two general factor models is the right one to use in a given situation? As we noted earlier, the economic factor model handles a different range of factors and operates differently from the fundamental factor model. Here we discuss some criteria for choosing one type of model over the other (see
Table 3.3
for a summary).
TABLE 3.3
Criteria for Selecting the Right Model
3.6.1 Consistency with Economic Theory
Tenet 5 of QEPM states that quantitative models should be based on sound economic theory. The economic factor model upholds tenet 5 better than the fundamental factor does. Economic theory suggests that high expected returns are justified only as the payoff for bearing extra risk. Small-cap and value stocks might produce extra returns not because there is anything especially good about being small cap and value but because being small cap and value increases the stocks’ risk. If this were the case, a fundamental factor model using those two variables would not give us meaningful information about the sources of risk and how they affect stock prices. It would be better to use a model that gets to the underlying risk of the stocks directly rather than looking at size and value. An economic factor model can measure the sensitivity of stocks to various economic risk factors.
Of course, if the relationship between the stock return and the fundamental factor exposure is linear, then the fundamental factor model is equivalent to the economic factor model, as we showed earlier. If the relationship is not linear, however, the fundamental factor model not only lacks theoretical backing, but it also lacks econo-metric justification because the cross-sectional regression becomes misspecified. In other words, we are estimating the wrong equation.
10
3.6.2 Ability to Combine Different Types of Factors
Not all factors can be used in both the economic and fundamental factor models. Both models can handle fundamental factors, such as the P/B ratio, the P/E ratio, and size. They also can use technical factors, such as momentum and trading volume. There are some factors, however, that only the economic factor model can handle. These include macroeconomic factors, such as GDP and inflation. If a portfolio manager wants to use a mix of all types of factors, the economic factor model is the necessary choice.
3.6.3 Ease of Implementation
In terms of ease of implementation, however, the fundamental factor model is preferable to the economic factor model. For the fundamental factor model, only factor premiums need to be estimated. For the economic factor models, factor exposures of individual stocks need to be estimated, and forecasts of factor premiums are usually needed as well. A manager should remember, though, that the ease of implementing the fundamental factor model comes at the cost of restrictions on the types of factors that can be used.
3.6.4 Data Requirement
The fundamental factor model can be estimated without a large amount of historical data.
11
On the other hand, to estimate the economic factor model, portfolio managers have to gather a relatively large period of historical returns because the estimation of factor exposures requires a time-series analysis of returns.
In terms of the cross-sectional dimension, the data requirement for the economic factor model may be lower than the data requirement for the fundamental factor model. The economic factor model
is estimated for each stock separately, and in the extreme case, it may be estimated for just one stock. To estimate the fundamental factor model, however, one needs a significant number of stocks (typically a few hundred).
However, this difference should not be exaggerated. When the economic factor model is estimated for a small number of stocks, the estimation error in the factor exposure may remain significant
after
the portfolio is constructed. If the portfolio is composed of a large number of stocks, the estimation error in the factor exposure of one stock is likely to be canceled out by the estimation error of another stock. This sort of canceling out is not likely to happen in a portfolio composed of very few stocks. Thus, in practice, the economic factor model also requires data on many stocks in order to be useful in the portfolio construction process.
12
3.6.5 Intuitive Appeal
The intuitive appeal of a model goes beyond whether it can be explained with economic theory. The best model is the one that makes common sense and is easy enough to explain in plain language. Portfolio managers always should understand the models they are using. Even an excellent model is dangerous in uneducated hands. In terms of gaining familiarity and becoming comfortable with quantitative models, reading this book carefully is a step in the right direction.
3.7 CONCLUSION
In this chapter we introduced the basic models that quantitative equity portfolio managers use to predict stock returns. The main models of QEPM are the fundamental factor model and the economic factor model. The fundamental factor model is used primarily to explain stock returns with stock fundamentals, whereas the economic factor model can be used to explain returns with almost any type of factor. The fundamental and economic factor models work somewhat differently but follow a common formula: the average stock return equals the product of factor exposures and factor premiums. We demonstrated that the two types of models produce identical results under certain conditions, but we also looked at reasons for choosing one type over the other.
Many managers use stock screening and ranking methods in addition to or instead of factor models. Although the Z-score analysis involved in screening and ranking stocks works fine by itself to estimate stock returns, it is best not to combine it with factor models. The resulting hybrid models fail the information criterion, and the resulting portfolios miss out on potential returns.
In this chapter we described how quantitative models fit into the seven steps of portfolio construction (factor choice, data preparation, estimation of factor exposures, estimation of factor premiums, determination of risk, forecasting of factor premiums, and, finally, security weighting). We will examine the fundamental and economic factor models in greater detail in
Chapters 6
and
7
, again in the context of the overall portfolio construction process, which is the subject of Part II of this book.
QUESTIONS
3.1.
What are the two most frequently used models of stock return in QEPM?
(a)   How do you obtain the factor exposure for each model?
(b)   How do you obtain the factor premium for each model?
(c)   How do you obtain expected returns for each stock from each model?
(d)   How do you measure the risk of each stock with each model?
3.2.
What are the steps in the general portfolio construction process of QEPM? Describe each one briefly.
3.3.
What is the difference between a cross-sectional data set and a time-series data set?
3.4.
Below is a series of statements by a quantitative portfolio manager. Decide whether each statement relates more to a fundamental factor model or to an economic factor model.
(a)   The average P/B ratio of our portfolio is very high.
(b)   Our portfolio will be quite resilient if oil prices rise to our negative exposures.
(c)   Our philosophy at the Financial Artists Hedge Fund is that economics drives stock returns; thus we use economic data to predict individual stock returns.
(d)   The factor exposure of every stock is known and publicly available.
(e)   Analyst forecasts drive stock returns.
(f)   Our investment department is very good at predicting presidential elections. We choose stocks accordingly.
3.5.
Macroeconomic variables cannot be used in stock return models because they are the same for all stocks. True or false. Explain.
3.6.
How do you obtain the factor premium for an economic factor model and a fundamental factor model? Give an example of each.
3.7.
How useful is the annual inflation rate of the United States as a factor premium?
3.8.
Why is forecasting factor premiums necessary? Why doesn’t this same logic apply to factor exposures? Please answer with respect to both types of QEPM stock return models.
3.9.
In this chapter we proved the equivalence of factor models under the assumption that the factor exposures are indepen
dent of one another. Prove the equivalence of factor models without this assumption.
3.10.
In this chapter we proved that if the fundamental factor model is correct, then the economic factor model is also correct. However, the reverse is not true. Consider the following example. Suppose that the expected stock return is proportional to the squared firm size and that the stock return can be written as
r
i
=
α
+
πx
2
i
+
ϵ
i
where
x
i
is the size of stock
i
.
(a)    Show that it is possible that the economic factor model is correct; i.e., the expected stock return is a linear function of the factor premium
f
defined as
f
=
E
(
r
|
x
>
µ
x
) –
E
(
r
|
x
<
µ
x
)
where
µ
is the average of the firm size.
(b)    Explain why the fundamental factor model may not be consistent with the preceding setup.
(c)    Given this one-way relationship, which model would you prefer in practice?
3.11.
What is a common standardization that portfolio managers use before screening stocks?
3.12.
Why might it be dangerous for a quantitative equity portfolio manager to combine the Z-score model with a commercial risk model to build an optimized portfolio?
3.13.
In the example of Section 3.5 we assumed that the true return-generating process is
That is, we assumed that
α
is zero. Suppose that
α
is not zero. Instead, assume that the true return-generating process is
(a)    If Adam estimates the Z-score model, what would be the estimated expected return of stock
A
and stock
B
? Are the estimates correct?
(b)    If Adam uses the estimated expected return from the Z-score model as
α
in the fundamental factor model, what would be the estimated expected returns of stock
A
and stock
B
? Are the estimates correct?
(c)    Explain why the information criterion is not satisfied regardless of whether the true
α
is zero or not.
(d)    Calculate the information loss.
3.14.
A portfolio manager estimated the expected stock return from a Z-score model of the price-to-earnings ratio and used it as
α
in the fundamental factor model, as discussed in Section 3.5. This time, however, instead of estimating the fundamental factor model with the price-to-earnings ratio, the portfolio manager estimated the fundamental factor model with the size. Thus the portfolio manager is not double counting any information. Is the information criterion satisfied now?
3.15.
Below we list some criteria for selecting a stock return model. Indicate which factor model (fundamental or economic) best meets each criterion.
(a)    Theoretical reasoning
(b)    Factor accommodation
(c)    Ease of implementation
(d)    Data requirements
(e)    Intuitive appeal
3.16.
Economic and fundamental factors are both used in practice.
(a)    Which type of factor is more theoretically justified?
(b)    Give one reason why this is so.
(c)    Eugene Fama might be heard saying the following: “I still would rather not use the type of factor in part (a) because it does not perform well out of sample.” What does he mean? Is he right?
1
One advantage of commercial software packages is that the companies that produce them tend to do a lot of data cleaning, which makes them a good source of polished data.
2
We will discuss these issues further in
Chapters 6
and
7
.
3
The convention in statistics is to use Greek letters for unobservable quantities and Latin letters for observable quantities. In the economic factor model, the factor exposure is unobservable, so it makes sense to use Greek letters for factor exposure. In the fundamental factor model, although the factor exposure is observable, it is still represented by the Greek letter
β
so that the notation is consistent in both types of factor models.
4
The reverse relationship cannot be established in general. That is, even if the economic factor model is a correct description of reality, the fundamental factor model still may not be correct.
5
This proof can be modified easily for the more general case.
6
Note that the expectation is taken across stocks. It is the cross-sectional average of the expected stock return.
7
In reality, we never know the true return-generating process, so the example may seem unrealistic. The fact that we are assuming certainty in the return-generating process, though, does not affect the lesson of the example that combining two models creates distortion.
8
When we typically estimate these factor models, we use information at time
t
to predict returns at time
t
+ 1. This is to avoid any look-ahead bias. Sometimes in this book, for convenience, we write the equation with time subscript
t
everywhere. It should still be interpreted as using information at time
t
to predict returns at time
t
+ 1. Sometimes we will refer to this as having beginning-of-month or equivalently end-of-the-previous-month factor exposures with this month’s returns.
9
The formula can be obtained by demeaning (i.e., subtracting the mean from) both sides of the equation and applying the standard ordinary least squares (OLS) formula.
10
Another assumption typically adopted in implementing the fundamental factor model is that the factor premium is stable for some time. Similarly, in implementing the economic factor model, the assumption is often that the factor exposure is stable for some time. Whether these assumptions make sense or not can be another criterion for choosing a model. However, as we explain in
Chapter 8
on forecasting, neither of these assumptions has to be adopted.
11
To estimate the variance of each stock return requires the variance of the error terms of each stock and the variance-covariance matrix of the factor premiums. It is possible to obtain the variance-covariance matrix of the factor premiums from (the estimation error of) a single cross-sectional regression. Thus a historical time series may improve the estimation but is not necessary. However, to be able to estimate the variance of the error of each stock, we do need some historical data because in a cross-sectional regression the variance of the error is assumed to be the same across stocks. The importance of estimating the error, however, is somewhat less than other estimations. Thus the fundamental factor model requires some historical data to be able to estimate the variance of individual stock returns, which is ultimately required to build optimized portfolios. However, the data required are still less than what are required in the economic factor model.
12
It also means that since the fundamental factor model is affected by the errors of factor returns and not of factor exposures, the fundamental factor model’s estimation errors will be similar regardless of the diversification of a portfolio. Thus one might believe that fundamental factor models would work better for very undiversified or concentrated portfolios.
