# Chapter 1: Introduction

- **book_name**: Active Portfolio Management
- **main_source**: pdf
- **cross_check_source**: none
- **pdf_role**: main_text_source
- **split_scope**: pages 23-32

---

CHAPTER
1
Introduction
The art of investing is evolving into the science of investing. This
evolution has been happening slowly and will continue for some
time. The direction is clear; the pace varies. As new generations of
increasingly scientific investment managers come to the task, they
will rely more on analysis, process, and structure than on intuition,
advice, and whim. This does not mean that heroic personal invest-
ment insights are a thing of the past. It means that managers will
increasingly capture and apply those insights ina systematic fashion.
We hope this book will go part of the way toward providing
the analytical underpinnings for the new class of active investment
managers. We are addressing a fresh topic. Quantitative active
management—applying rigorous analysis and a rigorous process
to try to beat the market—is a cousin of the modern study of
financial economics. Financial economics is conducted with much
vigor at leading universities, safe from any need to deliver invest-
ment returns. Indeed, from the perspective of the financial econo-
mist, active portfolio management appears to be a mundane consid-
eration, if not an entirely dubious proposition. Modern financial
economics, with its theories of market efficiency, inspired the move
over the past decade away from active management (trying to beat
the market) to passive management (trying to match the market).
This academic view of active management is not monolithic,
since the academic cult of market efficiency has split. One group
now enthusiastically investigates possible market inefficiencies.
1
2
Chapter One
Still, a hard core remains dedicated to the notion of efficient markets,
although they have become more and more subtle in their defense
of the market.'
Thus we can look to the academy for structure and insight, but
not for solutions. We will take a pragmatic approach and develop a
systematic approach to active management, assuming that this is
a worthwhile goal. Worthwhile, but not easy. We remain aware of
the great power of markets to keep participants in line. The first
necessary ingredient for success in active management is a recogni-
tion of the challenge. On this issue, financial economists and quanti-
tative researchers fall into three categories: those who think success-
ful active management is impossible, those who think it is easy,
and those who think it is difficult. The first group, however brilliant,
is not up to the task. You cannot reach your destination if you don’t
believe it exists. The second group, those who don’t know what
they don’t know, is actually dangerous. The third group has some
perspective and humility. We aspire to belong to that third group,
so we will work from that perspective. We will assume that the
burden of proof rests on us to demonstrate why a particular strategy
will succeed.
We will also try to remember that this is an economic investiga-
tion. We are dealing with spotty data. We should expect our models
to point us in the correct direction, but not with laserlike accuracy.
This reminds us of a paper called “Estimation for Dirty Data and
Flawed Models.”? We must accept this nonstationary world in
which we can never repeat an experiment. We must accept that
investing with real money is harder than paper investing, since we
actually affect the transaction prices.
PERSPECTIVE
We have written this book on two levels. We have aimed the mate-
rial in the chapters at the MBA who has had a course in investments
'A leading academic refined this technique to the sublime recently when he told an
extremely successful investor that his success stemmed not from defects in the
market but from the practitioner’s sheer brilliance. That brilliance would have
been as well rewarded if he-had chosen some other endeavor, such as designing
microchips, recombining DNA, or writing epic poems. Who could argue with
such a premise?
*Krasker, Kuh, and Welch (1983).
Introduction
3
or the practitioner with a year of experience. The technical appendi-
ces at the end of each chapter use mathematics to cover that chap-
ter’s insights in more detail. These are for the more technically
inclined, and could even serve as a gateway to the subject for the
mathematician, physicist, or engineer retraining for a career in
investments. Beyond its use in teaching the subject to those begin-
ning their careers, we hope the comprehensiveness of the book also
makes it a valuable reference for veteran investment professionals.
We have written this book from the perspective of the active
manager of institutional assets: defined-benefit plans, defined-con-
tribution plans, endowments, foundations, or mutual funds. Plan
sponsors, consultants, broker-dealers, traders, and providers of
data and analytics should also find much of interest in the book.
Our examples mainly focus on equities, but the analysis applies
as well to bonds, currencies, and other asset classes.
Our goal is to provide a structured approach—a process—for
active investment management. The process includes researching
ideas (quantitative or not), forecasting exceptional returns, con-
structing and implementing portfolios, and observing and refining
their performance. Beyond describing this process in considerable
depth, we also hope to provide a set of strategic concepts and rules
of thumb which broadly guide this process. These concepts and
rules contain the intuition behind the process.
As for background, the book borrows from several academic
areas. First among these is modern financial economics, which
provides the portfolio analysis model. Sharpe and Alexander’s
book Investments is an excellent introduction to the modern theory
of investments. Modern Portfolio Theory, by Rudd and Clasing, de-
scribes the concepts of modern financial economics. The appendix
of Richard Roll’s 1977 paper “A Critique of the Asset Pricing Theo-
ry’s Tests” provides an excellent introduction to portfolio analysis.
We also borrow ideas from statistics, regression, and optimization.
We like to believe that there are no books covering the same
territory as this.
STRATEGIC OVERVIEW
Quantitative active management is the poor relation of modern
portfolio theory. It has the power and structure of modern portfolio
theory without the legitimacy. Modern portfolio theory brought
4
Chapter One
economics, quantitative methods, and the scientific perspective to
the study of investments. Economics, with its powerful emphasis
on equilibrium and efficiency, has little to say about successful
active management. It is almost a premise of the theory that success-
ful active management is not possible. Yet we will borrow some
of the quantitative tools that economists brought to the investigation
of investments for our attack on the difficult problem of active man-
agement.
We will add something, too: separating the risk forecasting
problem from the return forecasting problem. Here professionals
are far ahead of academics. Professional services now provide stan-
dard and unbiased? estimates of investment risk. BARRA pioneered
these services and has continued to set the standard in terms of
innovation and quality in the United States and worldwide. We
will review the fundamentals of risk forecasting, and rely heavily
on the availability of portfolio risk forecasts.
The modern portfolio theory taught in most MBA programs
looks at total risk and total return. The institutional investor in the
United States and to an increasing extent worldwide cares about
active risk and active return. For that reason, we will concentrate
on the more general problem of managing relative to a benchmark.
This focus on active management arises for several reasons:
= Clients can clump the large number of investment
advisers into recognizable categories. With the advisers
thus pigeonholed, the client (or consultant) can restrict
searches and peer comparisons to pigeons in the same
hole.
= The benchmark acts as a set of instructions from the fund
sponsor, as principal, to the investment manager, as
agent. The benchmark defines the manager’s investment
neighborhood. Moves away from the benchmark carry
substantial investment and business risk.
= Benchmarks allow the trustee or sponsor to manage the
aggregate portfolio without complete knowledge of the
*Risk forecasts from BARRA or other third-party vendors are unbiased in that the
process used to derive them is independent from that used to forecast returns.
Introduction
5
holdings of each manager. The sponsor can manage a
mix of benchmarks, keeping the “big picture.”
In fact, analyzing investments relative to a benchmark is more
general than the standard total risk and return framework. By
setting the benchmark to cash, we can recover the traditional
framework.
In line with this relative risk and return perspective, we will
move from the economic and textbook notion of the market to the
more operational notion of a benchmark. Much of the apparatus of
portfolio analysis is still relevant. In particular, we retain the ability
to determine the expected returns that make the benchmark portfo-
lio (or any other portfolio) efficient. This extremely valuable insight
links the notion of a mean/variance efficient portfolio to a list of
expected returns on the assets.
Throughout the book, we will relate portfolios to return forecasts
or asset characteristics. The technical appendixes will show explicitly
how every asset characteristic corresponds to a particular portfolio.
This perspective provides a novel way to bring heterogeneous char-
acteristics to a common ground (portfolios) and use portfolio theory
to study them.
Our relative perspective will focus us on the residual compo-
nent of return: the return that is uncorrelated with the benchmark
return. The information ratio is the ratio of the expected annual
residual return to the annual volatility of the residual return. The
information ratio defines the opportunities available to the active
manager. The larger the information ratio, the greater the possibility
for active management.
Choosing investment opportunities depends on preferences.
In active management, the preferences point toward high residual
return and low residual risk. We capture this in a mean/variance
style through residual return minus a (quadratic) penalty on resid-
ual risk (a linear penalty on residual variance). We interpret this
as “risk-adjusted expected return” or “value-added.” We can de-
scribe the preferences in terms of indifference curves. We are indif-
ferent between combinations of expected residual return and resid-
ual risk which achieve the same value-added. Each indifference
curve will include a “certainty equivalent” residual return with
zero residual risk.
6
Chapter One
When our preferences confront our opportunities, we make
investment choices. In active management, the highest value-added
achievable is proportional to the square of the information ratio.
The information ratio measures the active management oppor-
tunities, and the square of the information ratio indicates our ability
to add value. Larger information ratios are better than smaller.
Where do you find large information ratios? What are the sources
of investment opportunity? According to the fundamental law of
active management, there are two. The first is our ability to forecast
each asset’s residual return. We measure this forecasting ability by
the information coefficient, the correlation between the forecasts
and the eventual returns. The information coefficient is a measure
of our level of skill.
The second element leading to a larger information ratio is
breadth, the number of times per year that we can use our skill.
If our skill level is the same, then it is arguably better to be able
to forecast the returns on 1000 stocks than on 100 stocks. The
fundamental law tells us that our information ratio grows in propor-
tion to our skill and in proportion to the square root of the breadth:
IR = IC
- V/breadth. This concept is valuable for the insight it
provides, as well as the explicit help it can give in designing a
research strategy.
One outgrowth of the fundamental law is our lack of enthusi-
asm for benchmark timing strategies. Betting on the market’s direc-
tion once every quarter does not provide much breadth, even if
we have skill.
Return, risk, benchmarks, preferences, and information ratios
are the foundations of active portfolio management. But the practice
of active management requires something more: expected return
forecasts different from the consensus.
What models of expected returns have proven successful in
active management? The science of asset valuation proceeded
rapidly in the 1970s, with those new ideas implemented in the
1980s. Unfortunately, these insights are mainly the outgrowth of
option theory and are useful for the valuation of dependent assets
such as options and futures. They are not very helpful in the
valuation of underlying assets such as equities. However, the
structure of the options-based theory does point in a direction
and suggest a form.
Introduction
7
The traditional methods of asset valuation and return forecast-
ing are more ad hoc. Foremost among these is the dividend discount
model, which brings the ideas of net present value to bear on the
valuation problem. The dividend discount model has one unambig-
uous benefit. If used effectively, it will force a structure on the
investment process. There is, of course, no guarantee of success.
The outputs of the dividend discount model will be only as good
as the inputs.
There are other structured approaches to valuation and return
forecasting. One is to identify the characteristics of assets that have
performed well, in order to find the assets that will perform well
in the future. Another approach is to use comparative valuation
to identify assets with different market prices, but with similar
exposures to factors priced by the market. These imply arbitrage
opportunities. Yet another approach is to attempt to forecast returns
to the factors priced by the market.
Active management is forecasting. Without forecasts, manag-
ers would invest passively and choose the benchmark. In the context
of this book, forecasting takes raw signals of asset returns and turns
them into refined forecasts. This information processing is a critical
step in the active management process. The basic insight is the rule
of thumb Alpha = volatility - IC - score, which allows us to relate
a standardized (zero mean and unit standard deviation) score to
a forecast of residual return (an alpha). The volatility in question is
the residual volatility, and the IC is the information coefficient—the
correlation between the scores and the returns. Information pro-
cessing takes the raw signal as input, converts it to a score, then
multiplies it by volatility to generate an alpha.
This forecasting rule of thumb will at least tame the refined
forecasts so that they are reasonable inputs into a portfolio selection
procedure. If the forecasts contain no information, IC = 0, the rule
of thumb will convert the informationless scores to residual return
forecasts of zero, and the manager will invest in the benchmark.
The rule of thumb converts “garbage in” to zeros.
Information analysis evaluates the ability of any signal to fore-
cast returns. It determines the appropriate information coefficient to
use in forecasting, quantifying the information content of the signal.
There is many a slip between cup and lip. Even those armed
with the best forecasts of return can let the prize escape through
8
Chapter One
inconsistent and sloppy portfolio construction and excessive trad-
ing costs. Effective portfolio construction ensures that the portfolio
effectively represents the forecasts, with no unintended risks. Effec-
tive trading achieves that portfolio at minimum cost. After all, the
investor obtains returns net of trading costs.
The entire active management process—from information to
forecasts
to implementation—requires constant and consistent
monitoring, as well as feedback on performance. We provide a
guide to performance analysis techniques and the insights into the
process that they can provide.
This book does not guarantee success in investment manage-
ment. Investment products are driven by concepts and ideas. If
those concepts are flawed, no amount of efficient implementation
and analysis can help. If it is garbage in, then it’s garbage out; we
can only help to process the garbage more effectively. However,
we can provide at least the hope that successful and worthy ideas
will not be squandered in application. If you are willing to settle
for that, read on.
REFERENCES
Krasker, William S., Edwin Kuh, and William S. Welsch. “Estimation for Dirty
Data and Flawed Models.” In Handbook of Econometrics vol. 1, edited by
Z. Griliches and M.D. Intriligator (North-Holland, New York, 1983), pp.
651-698.
Roll, Richard. “A Critique of the Asset Pricing Theory’s Tests.” Journal of Financial
Economics, March 1977, pp. 129-176.
Rudd, Andrew, and Henry K. Clasing, Jr. Modern Portfolio Theory, 2d ed. (Orinda,
Calif.: Andrew Rudd, 1988).
Sharpe, William F., and Gordon J. Alexander, Investments (Englewood Cliffs, N.J.:
Prentice-Hall, 1990).
PART
ONE
Foundations
/]
i
ok oe Pas we
ple, CS Ie
- a
Jot GVaie
ry
5
7 A : = Schein
nie
evel
) aus? ‘siete ar
ann) ie
s
<a
