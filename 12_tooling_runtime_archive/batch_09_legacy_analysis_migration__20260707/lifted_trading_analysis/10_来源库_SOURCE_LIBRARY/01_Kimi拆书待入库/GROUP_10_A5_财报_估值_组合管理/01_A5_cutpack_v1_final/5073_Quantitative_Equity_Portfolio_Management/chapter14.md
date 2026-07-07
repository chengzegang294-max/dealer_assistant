# Quantitative Equity Portfolio Management: An Active Approach to Portfolio Construction and Management, Second Edition

- **book_name**: 5073 Quantitative Equity Portfolio Management, Second Ed.
- **main_source**: epub
- **cross_check_source**: none
- **pdf_role**: not_needed
- **split_scope**: chapter file = chapter14

---

CHAPTER 14
Bayesian
α
Fool me once, shame on you. Fool me twice … well the point is we can’t get fooled again
.
—George W. Bush
14.1 INTRODUCTION
Whether from a qualitative research report or from knowledge passed along by word of mouth, portfolio managers usually have useful investing information that does not originate in a data set. Managers often attempt to build such information into an existing quantitative factor model by transforming it into the constant term
α
, but these attempts can be awkward. Assigning values to qualitative ideas can be somewhat arbitrary, and the new information may not combine efficiently with the estimation in the model. In such cases,
Bayesian theory
is extremely helpful. The theory, which provides a rigorous way to combine heterogeneous sets of information, is a good guide for how best to combine extra qualitative information with the estimation from a factor model.
We start this chapter with a quick review of Bayesian theory and define what we call the
Bayesian α
. We lay out the two stages of Bayesian analysis, determining the prior and determining the posterior. We walk through a number of typical examples to illustrate how to determine the prior, which summarizes all the extra qualitative information that the manager wants to add to the
model. We then discuss the posterior, which combines the extra information with the standard estimation from the factor model. At the end of the chapter we warn managers to avoid mistakes in applying the theory that violate the information criterion.
1
14.2 THE BASICS OF BAYESIAN THEORY
Bayesian theory is a systematic application of a statistical theorem called
Bayes’ rule
. To lay the foundation for Bayes’ rule, let us review the concept of conditional probability. Conditional probability is the probability of an event (
b
) happening when we know that another event (
a
) will happen. For example, event
a
is, “It will rain tomorrow,” and event
b
is, “The temperature will be below 100 degrees tomorrow.” We may ask, “What is the probability of the temperature being below 100 degrees tomorrow if it rains tomorrow?” We can express the question as a conditional probability
P
(
b
|
a
). If the answer to this question is 99% (i.e., when it rains, the temperature is unlikely to reach 100 degrees), it is the same as saying that the probability of
b
conditional on
a
is 99%, or
P
(
b
|
a
) = 99%.
Bayes’ rule relates probabilities to each other. It says that the probability of
b
conditional on
a, P
(
b
|
a
), is proportional to two probabilities: the probability of
a
conditional on
b, P
(
a
|
b
), and the probability of
b, P
(
b
). Mathematically, we may write
where
∝
means “is proportional to.” Continuing the example, if rain is more likely when the temperature is below 100 degrees, then a temperature below 100 degrees is more likely when it rains. In other words, when
P
(
a
|
b
) has a high value,
P
(
b
|
a
) has a better chance of having a high value as well. Also, if a temperature below 100 degrees is likely whether it rains or not, then it is more likely to be under 100 degrees if it rains. Expressed in terms of probabilities, the idea is that if
P
(
b
) has a high value, then
P
(
b
|
a
) probably also will be quite high.
We can interpret Bayes’ rule in
Eq. (14.1)
in a more general way. That is, we can take
a
and
b
to be random variables rather than events and
P
(·) to be the probability density of a random variable rather than the probability of an event.
Random
variables are any
variables (such as stock returns) that can take on different values, with different levels of likelihood for each potential value. We can revise our example about tomorrow’s weather so that we are discussing random variables rather than events. Suppose now that
b
is a random variable that equals the temperature at noon tomorrow, and
a
is a random variable that equals the amount of rainfall tomorrow. For discreet random variables (i.e., variables with only a limited set of potential values), probability is the same thing as probability density. For continuous random variables, the probability of attaining a certain value must be recovered by integrating the probability density over an interval. For example, if
b
is the temperature at noon tomorrow, then the probability that the temperature will be between 90 and 100 degrees can be found by integrating
P
(
b
) over
b
between 90 and 100. Whether it is for a discrete variable or for a continuous variable, the conditional probability density is the probability density of a random variable conditional on a specific value of another random variable. If
a
is the amount of rainfall tomorrow and
b
is the temperature at noon tomorrow, then
P
(
b
|
a
) is the probability density of temperature
b
given a specific amount of rainfall
a
.
Let us apply Bayes’ rule to a specific kind of conditional probability density, the probability density of parameters conditional on data. We will indicate parameters as
θ
(potentially a vector) and data as
x
(probably a very long vector). For factor models, the coefficients on explanatory variables and the error variances are the parameters. In the fundamental factor model, the factor premiums and the error variances are the parameters, whereas in the economic factor model, the factor exposures and the error variances are the parameters. For both factor models, the values of dependent and explanatory variables are data.
To apply Bayes’ rule to the probability density of parameters conditional on data, we simply can replace
b
and
a
in
Eq. (14.1)
with
θ
and
x
:
This formula takes the central place in Bayesian theory, and each term deserves an explanation. The last term,
p
(
θ
), is called the
prior
.
2
This is the probability density of the parameters
prior to
data
analysis. The prior may be based on qualitative or nondata information, intuition, or logic.
The probability density of the data conditional on the parameters,
p
(
x
|
θ
), is called the
likelihood function
, or the
likelihood
for short. It shows how
likely
it is that the data are drawn from the given parameters. For example, if the data are −100 and −101, then we know that they are very unlikely to be from the normal distribution with a mean of 0 and a variance of 1. On the other hand, if the data are −0.1 and 0.1, then we can say that they are quite likely to be from the normal distribution with a mean of 0 and a variance of 1. The likelihood function expresses this. To put it another way, the likelihood function measures the distance between the data and the parameters.
The probability density of the parameters conditional on the data
p
(
θ
|
x
) is called the
posterior
. It is the probability density of the parameters
after
we analyze the data. The posterior combines the information we had before analyzing the data (the prior) and the information we obtained from the data (the likelihood). Thus the posterior summarizes all we know about the parameters. The formula in
Eq. (14.2)
is a simple way to combine nondata or qualitative information about the parameters into the data analysis. We simply need to multiply the prior and the likelihood. Not only is it simple, but it turns out to be the best way of adding nondata information to the data analysis.
Since Bayesian theory seems quite straightforward, one might wonder why it deserves to be called a theory. Although it is indeed straightforward mathematically, Bayesian theory represents a huge philosophical jump from “classical” statistical theories. In classical theory, there is a clear distinction between what is a random variable and what is not a random variable. The parameters of a model are not considered random variables. While we do not know the true values of the parameters, the classical thinking goes, true values must be somewhere “out there,” so we cannot treat them as random variables. Thus the parameters cannot have probability distributions, and we can think neither of the prior nor of the posterior. Bayesian theory, on the other hand, makes no distinction between random and nonrandom variables. Even if we do not know the exact value of a variable, we still can assign a probability to each possible value and treat the variable as random. Another important feature of Bayesian theory is that the probabilities do not have to be objective. In fact, the prior is a subjective probability of
the parameters. If you have special information, the prior you calculate will be different from the prior another person calculates. In classical theory, the probability of a value is taken almost as a law of nature, and there is no room to add one’s subjective opinion to it.
While the philosophical difference between Bayesian and classical is great, the practical differences should not be exaggerated. When both the classical theory and the Bayesian theory are applicable, their conclusions are identical more often than not. In this chapter we are mostly interested in situations in which only the Bayesian theory is applicable. Classical theory has only limited use (or almost no use) when one attempts to combine qualitative information with data analysis. In such cases, we do not have any choice but to adopt Bayesian theory.
14.3 BAYESIAN
α
MOJO
Instead of adopting the Bayesian approach from beginning to end, we will focus on where Bayesian theory clearly adds value to quantitative equity portfolio management (QEPM), which is in incorporating qualitative information on
α
into the QEPM process in a systematic way. Portfolio managers often have nondata information on individual stocks, and this information is often qualitative rather than quantitative. Maybe a research report appears saying that stock
XYZ
has an exceptionally positive outlook but that its current stock price does not reflect the positive outlook. Maybe an analyst, who has information not available to the portfolio manager, comes up with a selection or a ranking of stocks, and the portfolio manager would like to incorporate that into the analysis. Or perhaps the manager has a data set that he or she finds informative but not suitable as the basis for a factor model.
In such cases, a portfolio manager typically attempts to set the value of
α
in the factor model in some ad hoc way that reflects the extra information. The portfolio manager may use the following economic factor model to estimate the return of stock
i, r
i
:
where
f
1
, …,
f
K
are factor premiums,
β
i1
,…,
β
iK
are factor exposures of stock
i
, and
ϵ
i
is the error component of stock
i’s
return. The alpha of stock
i, α
i
, is the part of the average stock return that the model cannot explain. The portfolio manager bases the factor
premiums and factor exposure on his or her original data set. Since this data-based model cannot explain
α
i
, the manager attempts to set the value of
α
i
according to his or her nondata information. However, since the nondata information is qualitative, assigning values could be arbitrary.
Bayesian theory becomes very useful at this stage. Rather than setting the value of
α
in an arbitrary way, the portfolio manager can adopt the Bayesian approach and assign a distribution to the
α
that is consistent with the nondata information. This assigned distribution is what Bayesian theorists call the
prior
. Once the prior is assigned, the portfolio manager can follow the standard procedure of the Bayesian approach to obtain the best estimates of
Eq. (14.3)
that reflect not only the information in the data but also the useful nondata information. Calculating the
Bayesian α
, as we call it, is consistent with the information criterion that we introduced in
Chapter 2
. Attempts to incorporate nondata information into the model without calculating the Bayesian
α
most likely will fail to exploit the information completely and violate the information criterion, seriously distorting the portfolio. The Bayesian
α
, on the other hand, is entirely a gain to the portfolio manager and another strong source of
α
mojo.
14.4 QUANTIFYING QUALITATIVE INFORMATION
The first step of Bayesian analysis is to decide on the prior of the
α
from the nondata information, a somewhat challenging step because nondata information is often qualitative. In this section we will go through three relatively simple but commonly faced situations involving calculating the prior. More complicated cases will be dealt with in the next two sections. First, we will start with the situation in which the portfolio manager receives a list of stocks screened by other analysts. Then we will consider the case in which the portfolio manager receives a ranking of selected stocks. Lastly, we will consider the case in which the portfolio manager wants to incorporate buy and sell recommendations for selected stocks.
14.4.1 Quantifying a Stock Screen
Suppose that we have many lists of analyst-recommended stocks, each list made by an analyst through some screening process. How
can we convert these lists into the prior for the
α
of each stock? When a stock is included in a list, it means that an analyst believes that the stock is likely to outperform the stocks not included in the list. That is, a listed stock is likely to have a higher
α
than that of an unlisted stock. If stock
A
is included in a list but stock
B
is not, we can say that
If stock
A
is included in many analysts’ lists and stock
B
in none, then we can be more confident that
α
A
is greater than
α
B
because more analysts agree on the superiority of stock
A
. Specifically, if we consider each list (or analyst) equally reliable, then we can say that
That is, if half the analysts say that
α
A
is greater than
α
B
, then we may be 50% sure that
α
A
is greater than
α
B
. If every analyst says that
α
A
is greater than
α
B
, then we may be (almost) 100% sure that
α
A
is greater than
α
B
.
If stock
B
is not included in any of the lists, the lists do not say anything about stock
B
. Thus, as far as
α
B
is concerned, we do not need to do anything special. We can estimate
α
B
in the usual way and obtain the estimate
and its standard error
S(
). From the Bayesian perspective,
and its standard error are considered to be the mean and the standard deviation of
α
B
. That is, assuming a normal distribution, we can write
Once
Eqs. (14.5)
and
(14.6)
are obtained, it is straightforward to find the prior distribution for
α
A
. The inclusion of stock
A
into the list does not imply anything about the relative amount of uncertainty regarding
α
A
and
α
B
. Thus it is reasonable to take
S
(
) as the standard deviation of
α
A
as well. Now we only have to determine the mean of
α
A
. Let
µ
A
be the mean of
α
A
. Assume that
α
A
has a normal distribution and is independent of
α
B
(which is reasonable given that we do not have any information indicating otherwise). Then
It follows immediately that
where Φ is the standard normal cumulative distribution function. Considering
Eqs. (14.5)
and
(14.8)
,
where Φ
−
1
is the inverse standard normal cumulative distribution function that takes a probability as the argument. Thus we have determined the prior distribution for
α
A
. We can generalize this analysis in a number of directions. First of all, we can find the distribution of
α
B
using all the stocks that are not included in any of the lists. If we cannot find such stocks, then we can use an arbitrary set of stocks and modify
Eq. (14.5)
. Also, if different analysts are not equally reliable, then we may assign different weights to different analysts and lists.
A more important generalization of the analysis is the case in which there is only one list of stocks. It may be that all analysts work as a team and produce a single list, or it may even be the case that the portfolio manager is the one who produces the list. For one stock list, the preceding analysis is still valid except for
Eq. (14.5)
. For
Eq. (14.5)
, the portfolio manager himself or herself must decide on the probability that
α
A
is greater than
α
B
. While this may seem quite subjective, this is not necessarily a problem. The prior distribution is meant to represent subjective opinion. Unless the portfolio manager chooses different probabilities for different stocks,
Eq. (14.9)
is common for all stocks included in the list. That is, all stocks in the list have the same mean as expressed in
Eq. (14.9)
.
14.4.2 Quantifying a Stock Ranking
Suppose that instead of having a simple list of stocks, we have analyst-prepared rankings of stocks. We can easily extend the idea developed in the preceding subsection to this case. If stock
A
is ranked higher than stock
B
, it means that an analyst believes that the
α
of stock
A
is higher than the
α
of stock
B
. The probability of the
α
of stock
A
being higher than the
α
of stock
B
can be computed by comparing the number of analysts who believe this to be true to the total number of analysts who do not. That is,
Note that
Eq. (14.10)
is essentially identical to
Eq. (14.5)
. Thus we can follow the same procedure for dealing with stock screens.
Once stock
B
is chosen, this same stock should be compared with all the other stocks to exploit all the information in the ranking. One possibility is to choose for stock
B
a stock that is ranked most frequently at the bottom of ranked lists, and for each of the remaining stocks, calculate
Eq. (14.10)
relative to stock
B
. In any case, how stock
B
is selected does not really matter as long as it is compared with all other stocks. The procedure is identical whether all stocks are ranked by every analyst or different stocks are ranked by different analysts. If there is only one ranking (perhaps made by the portfolio manager himself or herself), then the portfolio manager assigns a number to
P(α
A
>
α
B
) in
Eq. (14.10)
and follows the same procedure.
14.4.3 Quantifying the Buy and Sell Recommendations
Qualitative information also may be in the form of analysts’ buy and sell recommendations. Instead of a simple “buy” or “sell,” analysts often give stocks one of five recommendations: strong buy, buy, neutral, sell, and strong sell. These recommendations can be converted easily into the probability of one stock having a higher
α
than another stock. One way to do this is to use the
buy ratio
, which is the number of buy recommendations divided by the total number of buy and sell recommendations. Once the buy ratio is calculated for every stock, we can find the probability of the
α
of stock
A
being greater than the
α
of stock
B
by subtracting the buy ratio of stock
B
from the buy ratio of stock
A
. That is,
The buy ratio of stock
A
shows what fraction of analysts believes that stock
A
is superior, and the buy ratio of stock
B
shows the fraction of analysts that believes that stock
B
is superior. The difference
between the two buy ratios shows the fraction of analysts that believes that stock
A
is superior to stock
B
. This is exactly true if the same analysts make recommendations for stocks
A
and
B
and approximately true in other cases. After
Eq. (14.11)
is determined, we can proceed as we did in the previous cases.
14.5 THE Z-SCORE-BASED PRIOR
The Z-score approach explained in
Chapter 5
produces rankings of stocks based on certain factors. It is therefore possible to generate the prior of the
α
from the Z-score and then estimate a factor model using other unused information. This approach is superior to using the Z-score alone because it employs all the information available in the data. Suppose that we have
L
factors and a calculated Z-score for each stock. If we have not aggregated the Z-score, then the Z-score for each stock is a vector of
L
numbers. Let
z
i
= (
z
i
1
, …,
z
iL
) be the Z-score of stock
i
. The Z-score for each factor implies a certain ranking of stocks. Since there are
L
factors, we have
L
implied rankings of stocks. Once we interpret the Z-score as the ranking of stocks, the prior of the
α
can be generated according to the method for stock rankings described earlier. That is, given stock
A
and stock
B
, the probability that the
α
of stock
A
is greater than the
α
of stock
B
is
where
I
(·) is an indicator function returning the value 1 if the expression inside the parentheses is true and 0 if not.
The preceding formula is based on the idea that each factor is equally informative. However, as we discussed in
Chapter 5
, we may have reason to assign different weights to different factors. Suppose that for factor
l
we want to assign weight
υ
l
so that
υ
1
+ … +
υ
l
= 1. Then the probability that the
α
of stock
A
is greater than the
α
of stock
B
changes to
After the probability is calculated, we can easily determine the prior of the
α
of stock
A
as explained in the preceding section. We
choose an arbitrary stock
B
and obtain the estimate
and its standard error
S
(
) from a factor model. Then the prior for the
α
of stock
A
becomes
where
The derivation of this formula is the same as the derivation explained in the preceding section. That is,
p
A
is calculated from
Eq. (14.8)
, and we can substitute
p
A
into
Eq. (14.15)
.
14.6 SCENARIO-BASED PRIORS
The prior of the
α
can be generated systematically from what is known as
scenario analysis
. Scenario analysis is suitable when the portfolio manager has strong opinions about how individual stocks will perform under specific situations. Different variables in the economic or natural environments present opportunities for scenario analysis. For instance, investors use scenario analysis before presidential elections to guess how different election outcomes will affect stocks. Investors in the agricultural and certain manufacturing industries use it to try to anticipate the effect of weather patterns on future stock returns. The portfolio manager can systematically incorporate his or her views about stock returns under different conditions into the prior of the
α
through scenario analysis. For each scenario, the portfolio manager determines—whether based on his or her own beliefs or on some outside evidence—two quantities: the probability of the scenario being realized and the
α
of the stock when the scenario is realized. Given the probability of each scenario and the value of the
α
, he or she can construct a distribution for the stock’s
α
, which becomes the prior of the
α
.
The first step in scenario analysis is to identify all possible scenarios. Typically, this can be done with an
event tree
. Suppose that the portfolio manager has certain beliefs about future stock returns, which are conditional on the following events: high or low inflation, high or low unemployment, high or low productivity growth, and high or low oil prices. An event tree organizes these events, as illustrated in
Figure 14.1
, producing 16 possible scenarios. In general, if
E
pairs of events are considered, then 2
E
scenarios are possible.
FIGURE 14.1
Scenario analysis event tree.
The second step in scenario analysis is to assign probabilities to each scenario. If each pair of events is independent of the others, then the probability of a scenario is simply the product of the probabilities of the events that happen in the scenario. For example, the probability of scenario 1 is given by
3
However, if each pair of events is not independent, this formula does not work, and the probability of each scenario must be found individually through, for instance, the forecasting methods discussed in
Chapter 8
.
The third step is to determine the
α
of each stock. There are two approaches to this, the subjective approach and the event-study approach. The subjective approach draws on the portfolio manager’s personal beliefs. The event-study approach assigns the
α
based on historical data. To determine
α
through the event-study approach, we need first to define the event exactly. For example, we may define high unemployment as an unemployment rate of above 5% and low unemployment as an unemployment rate of below 5%. Then we need to find the average abnormal return for each event. During the period from January 2011 to December 2020, 72 months can be categorized as high-unemployment months, and the remaining 48 months can be categorized as low-unemployment months. The abnormal return can be calculated in various ways, but the simplest method is to calculate the excess return of each stock over the market return.
Table 14.1
shows the average abnormal returns as well as the standard deviation of selected stocks for low- and high-unemployment months. These average abnormal
returns can be used as
α
’s. When applying the event-study approach, one should be careful not to base the prior on the data that eventually will be used to estimate the stock return model. This issue will be discussed further toward the end of this chapter.
TABLE 14.1
Average Abnormal Returns of Selected Stocks in the High-/Low-Unemployment Scenario
Suppose that we defined
S
scenarios. Let
P
(
s
) be the probability of scenario
s
and
α
i
(
s
) be the
α
of stock
i
in scenario
s
. Then the profile of the probability and the
α
{[
α
i
(1),
P
(1)], …, [
α
i
(
S
),
P
(
S
)]} completely determine the distribution of the
α
. We certainly could stop here as far as the prior is concerned. However, approximating the prior distribution as a normal distribution reduces the computational burden significantly at a later stage of the analysis. The approximate normal distribution is given as follows:
where
and
14.7 POSTERIOR COMPUTATION
Once the prior is determined, the posterior can be computed from Bayes’ rule. While the formula for the posterior may look complicated, the computation itself is straightforward. This is especially
true when the prior is a normal distribution. When the prior is a normal distribution, the posterior is also a normal distribution, and we only have to determine the mean and the variance of the posterior. In this section we focus on the interpretation of the posterior formula.
4
Suppose that the portfolio manager uses the following factor model to estimate the return of individual stocks:
where
r
i
is the return of stock
i, f
1
, …,
f
K
are factor premiums,
β
i
1
, …,
β
i
K
are factor exposures of stock
i
, and ϵ
i
is the error component of stock
i’s
return.
α
i
is the
α
of stock
i
for which the portfolio manager defined the following prior using one of the approaches described in the preceding section:
We assume that the portfolio manager did not define the prior for
β
i
1
, …,
β
iK
. The computation is in fact easier if the prior for
β
i
1
, …,
β
iK
is defined as well, but we will focus on the more typical situation in which it is not.
5
Since the posterior combines the information in the prior and the information in the data [which is summarized in the ordinary least squares (OLS) estimate], for
α
i
, the posterior mean is the weighted average of the prior mean and the OLS estimate. The weights are the inverse of the respective variances. For the prior mean, the weight is the inverse of the prior variance, and for the OLS estimate, the weight is the inverse of the OLS variance of the estimate (i.e., the squared standard error of the estimate). The inverse of the variance shows how precise the quantity is. If the variance is large, the quantity is less precise, and if the variance is small, the quantity is more precise. For this reason, the inverse of the variance is called the
precision
of the estimate. It is often said that the posterior mean is the
precision-weighted average
of the prior mean and the OLS estimate. The posterior mean of
α
i
is given as follows:
where
ι
is a
T
-dimensional vector of 1s and
T
is the number of observations in the estimation, and
M
is the residual matrix (defined in Appendix 14A). As explained earlier, the posterior mean is the weighted average of the prior mean (
µ
α
i
) and the OLS estimate (
). The average is taken using the prior precision (1/
σ
2
αi
) and the OLS precision [(1/
σ
2
ϵi
)
ι
′
M
ι
] as the weights. The “denominator” (in the matrix sense), (1/
σ
2
αi
) + (1/
σ
2
ϵi
)
ι′
M
ι
, is simply the sum of the prior precision and the OLS precision. By “dividing” each weight by this quantity, the sum of the weights equals 1.
The posterior variance of
α
i
is the inverse of the sum of the prior precision and the OLS precision. That is, the posterior precision is the sum of the prior precision and the OLS precision. The precision shows how much confidence we have in a given quantity. If we have great confidence in our prior (there is high prior precision), then we still will have great confidence after the estimation (high posterior precision). Even if we have little confidence in our prior, if the OLS produces reliable results (there is high OLS precision), then our confidence level will go up (high posterior precision). Thus it makes sense to add the prior precision and the OLS precision to get the posterior precision.
The posterior variance of
α
i
is given as
It is the inverse of the sum of the prior precision (1/
σ
2
αi
) and the OLS precision [(1/
σ
2
ϵi
)
ι
′
M
ι
].
The formulas for the posterior mean and the variance of
β
i
1
, …,
β
iK
(together with other useful quantities) are presented in Appendix 14A.
6
Here we only note that while the prior is defined
only for
α
i
, the estimates of
β
i
1
, …,
β
iK
will be affected by the prior as well. This is so because there is a correlation between the estimate of
α
i
and the estimates of
β
i
1
, …,
β
iK
. Since the prior influences the estimate of
α
i
, it also will indirectly affect the estimates of
β
i
1
, …,
β
iK
, even though there is no prior for
β
i
1
, …,
β
iK
.
14.8 THE INFORMATION CRITERION AND BAYESIAN
α
The Bayesian approach is an extremely powerful tool for combining two sets of information, typically data information and nondata information. Data information is summarized by the factor model (i.e., the likelihood), and nondata information is summarized by the prior. The two sets of information are optimally combined in the posterior. While the Bayesian approach is quite useful, it is easy to make certain mistakes in applying it, especially (though not only) when the prior is determined from data information. If the prior is determined from data information and if the data are not properly
excluded
from the model estimation, one will end up double counting certain information. The following are examples of possible
mistakes
that portfolio managers might be tempted to make:
•  Screen stocks based on the price-to-earnings ratio, develop the prior for the alpha based on the screen, and use the price-to-earnings ratio again as a factor in the estimation of the factor model.
•  Rank stocks based on momentum or some other factor, develop the prior for the alpha based on the ranking, and use momentum again as a factor in the estimation of the factor model.
•  Generate the prior based on analyst recommendations, and when estimating the factor model, use the analyst factor again based on the same information.
•  Base the prior on the Z-score of certain factors, and use some of these factors again when estimating the factor model.
•  Do the scenario analysis based on the past stock performance when inflation was high or low, and use the same inflation data as a factor in the factor model.
The list of possible mistakes is infinite, but the general idea is the same: Information should not be used twice. If a piece of information was used to make the prior, it should not be used in estimating the model. The information criterion we developed in
Chapter 2
encapsulates this rule. In
Chapter 2
we emphasized that information should not be wasted and that all information should be combined in the most efficient way. Using the same information twice is inefficient. In fact, it violates all the fundamental assumptions of statistical inference. Thus the standard errors will be wrong if the same information is used twice.
14.9 CONCLUSION
Bayesian theory represents a major step forward from classical statistical theory because it allows us to treat any variable as a random variable and assign subjective probabilities, based on qualitative or nondata information, to the variable’s potential values. Bayesian theory opens up the possibility of encapsulating such extra information in a Bayesian
α
that amplifies the QEPM model of stock returns. In this chapter we first showed how to calculate the Bayesian
α
’s prior, which summarizes and quantifies extra information that does not originate in the data set with which the factor model was estimated. This extra information can come from stock screens and rankings, buy/sell recommendations, Z-scores, or scenario analysis. We then discussed how to calculate the Bayesian
α
’s posterior, which summarizes all the available information by combining the prior and the factor model estimation. Having calculated the posterior, we can fully describe the distribution of Bayesian
α
. As long as all pieces of extra information contained in the
α
are distinct from the data used to estimate the factor model, adding Bayesian
α
to the model upholds the information criterion. Bayesian
α
, with its ability to widen the scope of a purely data-based factor model into diverse kinds of information, is our third source of
α
mojo.
QUESTIONS
14.1.
Prostate cancer affects roughly 12.5% of the male population. A prostate-specific antigen (PSA) test is able to detect whether men might have the disease. The test has a type I error of 70% (when the person does not have cancer, there is a 70% chance that the test will conclude that he does) and a type II error of 20% (when the person does have cancer, there is a 20% chance that the test will conclude that he does not). In a recent testing at UCSF Medical Center, a person tested positive for prostate cancer.
(a)    What is the probability that the person has prostate cancer?
(b)    A company called Grail has a blood cancer screening test called Galleri. Its false-positive rate is 0.5% and its false-negative rate is 0.6%. If 100,000 men took the new test over the old test, how many more people with cancer would be alerted early? How many more people without prostate cancer would avoid the psychological stress and physical inconvenience of a biopsy? (
Note
: The false-positive and false-negative rates were obtained from a study by Grail; however, they are for detecting all cancers and not specifically prostate cancer. The prostate-specific cancer numbers were not available).
14.2.
The probabilities for events
A
and
B
are given as follows:
P
(
A
) =
,
P
(
B
) =
,
P
(
A ∩ B
) =
. Find the probability of event
A
happening conditional on event
B
happening, that is,
P
(
A
|
B
).
14.3.
Suppose that the stock return
r
has the following conditional distribution:
r
|
µ
~
N
(
µ
, 1).
µ
has the following distribution:
µ
~
N
(
α, β
).
(a)    What is the expected value of
r
?
(b)    What is the variance of
r
?
(c)    What is the marginal distribution of
r
?
14.4.
What is the prior? Explain the possible role of the prior in quantitative equity portfolio management (QEPM).
14.5.
Explain the difference between the Bayesian approach and the classical approach to estimation.
14.6.
One criticism of the Bayesian approach is that different analysts may come to different conclusions. Explain how a Bayesian statistician would respond to such criticism.
14.7.
In the Bayesian framework, the OLS estimation is a special case of Bayesian analysis. Describe the prior distribution under which Bayesian analysis and an OLS estimation would produce identical results.
14.8.
Suppose that the stock return
r
has the following conditional distribution:
r
|
µ
~
U
[
µ
− 1,
µ
+ 1]
where
µ
may take a value of 0 or 1 with equal probability, and
U
indicates a uniform distribution. That is, the probability density function of
r
is
(a)    If you observe the value of
r
to be 1.9, what do you conclude the value of
µ
to be?
(b)    If you observe the value of
r
to be −0.5, what would do conclude the value of
µ
to be?
(c)    Find the posterior distribution of
r
in each of the above cases.
14.9.
The capital asset pricing model (CAPM) is a special case of the economic factor model. Suppose that we estimated the CAPM in the following form:
r
i
=
α
i
+
β
i
r
M
+
ϵ
i
Using the OLS method, we obtained the following estimates:
The numbers inside the parentheses are standard errors.
(a)    One implication of the CAPM is that the true value of
α
is 0. If you believe the CAPM 100%, what would be the posterior distribution of
α
i
?
(b)    If you are convinced that the CAPM is not true, but if you do not have any other prior opinion about the value of
α
, what would be the posterior distribution of
α
i
?
(c)    If you believe that there is a 50% chance that the CAPM is correct and that there is a 50% chance that the CAPM is incorrect, what would be your posterior distribution of
α
i
?
14.10.
The return of stock
A
is known to have the normal distribution with mean 10 and variance 25, that is,
r
A
~
N
(10, 25)
The return of stock
B
is known to have a normal distribution with a variance of 25, but the mean
µ
of the distribution is not known, that is,
r
B
~
N
(
µ
, 25)
Assume that
r
A
and
r
B
are independent.
(a)    A poll of 100 analysts indicates that 50 of 100 analysts believe that stock
B
will outperform stock
A
, whereas the remaining 50 analysts believe that the opposite will happen. Considering the poll, what is your best guess at the value
µ
?
(b)    Suppose that 70 of 100 analysts believe that stock
B
will outperform stock
A
. Find the value of
µ
that is consistent with the poll.
(c)    If the variance of
r
B
is not known, how would you change your answers to parts (a) and (b)?
(d)    If
r
A
and
r
B
are not independent, how would you change your answers to parts (a) and (b)?
(e)    If the distribution of
r
A
is not known, how would you change your answers to parts (a) and (b)?
14.11.
An event tree is useful in identifying different scenarios. Draw an event tree for a scenario in which the stock return depends on the following two outcomes: (a) which party (Republican, Democratic, or Green) wins in the next U.S. presidential election and (b) whether NASA’s spaceship lands on Venus.
14.12.
The return of stock
A
heavily depends on the oil price. The return of stock
A
(
r
A
) conditional on the oil price (
G
) is given as follows:
(a)    Suppose that the probability of each of the four scenarios happening is 25%. Describe the distribution of
r
A
.
(b)    Estimation of an economic factor model suggests that
r
A
~
N
(10, 25)
Treating the distribution given in part (a) as a prior, describe the posterior distribution of
r
A
.
14.13.
The posterior mean is the weighted average of the prior mean and the OLS estimate, where the weights are the precisions. Explain the similarity between this formula and the formula for the optimal portfolio weights in
Chapter 9
. Is the similarity a coincidence?
14.14.
The posterior computation can be carried out using a pseudo- random-number generator. This exercise outlines the steps.
(a)    Show that if
x
is a random draw from the uniform distribution
U
[0, 1], then
y
= Φ
−
1
(
x
) may be considered a random draw from the standard normal distribution
N
(0, 1).
(b)    Show that if
y
is a random draw from
N
(0, 1), then
z
=
µ
+
σy
is a random draw from
N
(
µ, σ
2
).
(c)    Let
z
1
, …,
z
J
be random draws from
N
(
µ, σ
2
). Show that the expected value of a function of
z, f
(
z
), can be approximated as
(d)    Let
p
(
θ
) be the prior and
l
(
θ
) be the likelihood. Show that
(e)    Let
θ
1
, …,
θ
J
be the random draws from the prior. Show that the probability in part (d) can be approximated by
14.15.
The Bayesian approach can be very powerful in combining qualitative information with quantitative data. However, when two sets of quantitative data are to be combined, there is a danger of double counting the same piece of data in the prior and in the estimation. What would be the consequence of such double counting?
1
See
Chapter 2
for a discussion of the information criterion.
2
It is also common to use
f
(·) to denote probability density functions instead of
p
(·).
P
(·) is used to denote the actual probability of a specific event.
3
The probability of each event can be found in various ways. For example, suppose that a portfolio manager is interested in the effect on certain stocks of a Federal Reserve (Fed) easing. Prior to 2008, the probability of a Fed easing (or tightening) could be derived from Fed fund futures. This probability could be used in an event tree dependent on Federal Open Market Committee (FOMC) actions. After 2008, the Fed switched to an upper and lower Fed funds target rate to allow flexibility in managing the Fed funds rate. Thus, in order to estimate the probability of a Fed change in rates, the portfolio manager needs to estimate the effective daily funds rate before and after the FOMC meeting. Although not exact, the portfolio manager can make the assumption that the effective funds rate will be at the midpoint of the upper and lower Fed funds target rate. Thus, the probability of a Fed move can be expressed as
where
i
f
is the futures rate implied by the relevant contract,
i
pre
is the midpoint of the upper and lower target Fed Funds rate prevailing before the FOMC meeting,
i
post
is the midpoint of the upper and lower target rate that the investor expects to prevail after the FOMC meeting,
d
2
is the number of days between the FOMC meeting and the current month’s end, and
B
is the number of days in the month. This formulation assumes no Fed funds changes between meetings and that the midpoint of the upper and lower target Fed funds rate is a reasonable proxy for the actual effective Fed funds rate over the period before and after the FOMC meeting—although this is often not true. For example, if the Fed funds futures (
i
f
t
) is 2.06% (100 − 97.94), the midpoint of current target rates (
i
p
r
e
t
) is 2.125, and the expected lower range is from 1.75 to 2 with a midpoint (
i
pos
t
t
) of 1.875, and given that the FOMC meeting takes place on the 18th day of the month, then there is a 65% probability that the Fed will lower its target range from 2-to-2.25 to 1.75-to-2. There are other methods of making this calculation, including using the most recent average effective funds rate for the value of
i
p
r
e
t
. In this particular example, using this value would give a 75% probability of a Fed reduction in target rates. A negative probability implies that the market expects the Fed to do the opposite of what the investor believes; thus he or she should change expected change to its opposite and recalculate.
4
The derivation is presented in Appendix 14A, which can be found at
https://ludwigbc.com/books/qepm/exclusive_qepm_content_2020/
or at
www.ludwigbc.com
and look for QEPM Exclusive Content.
5
See Appendix 14A at
www.ludwigbc.com
and look for QEPM Exclusive Content for the posterior when the prior for
β
i
1
, …,
β
iK
is defined.
6
Appendix 14A can be found under Chapter Appendices at
https://ludwigbc.com/books/qepm/exclusive_qepm_content_2020/
.
