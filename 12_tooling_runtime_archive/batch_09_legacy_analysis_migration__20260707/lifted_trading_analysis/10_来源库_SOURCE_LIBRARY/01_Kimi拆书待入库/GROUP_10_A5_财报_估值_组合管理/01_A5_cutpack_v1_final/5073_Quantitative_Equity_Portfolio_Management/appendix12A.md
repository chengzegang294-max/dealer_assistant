# Quantitative Equity Portfolio Management: An Active Approach to Portfolio Construction and Management, Second Edition

- **book_name**: 5073 Quantitative Equity Portfolio Management, Second Ed.
- **main_source**: epub
- **cross_check_source**: none
- **pdf_role**: not_needed
- **split_scope**: chapter file = appendix12A

---

APPENDIX 12A
Fair-Value Computations
Fair value is a concept used commonly in futures markets. Since a futures contract trades on the basis of an underlying spot security, there should be some relationship between the underlying security price and the futures price. This theoretical price of the futures contract is known as
fair value
.
There is no perfect formula for computing the fair value of the futures contract. It will depend on the dividends paid by the underlying index, the timing of those dividends, the available interest rates in the market, the number of days until the expiration of the futures contract, and the current index level. Different banks have different ways of computing fair value; however, all fair values are based on a similar fundamental concept known as
present discounted value
. If one is using a continuously compounded interest rate to compute fair value, then the fair-value formula is expressed as
where
F
t
is the fair-value futures price,
S
t
is the current value of the underlying index,
i
is the prevailing interest rate over the time until expiration of the futures contract,
q
is the continuously compounded dividend yield of the index, and
T
−
t
is the time until the futures contract expires.
Most people in the market do not deal with continuous compounded interest; thus the more popular formula is a formula that involves money market interest conventions. Thus
where
i
is the money market interest rate,
k
is the number of days until the futures contract expires, and
d
t
is the present discounted value of dividend payments occurring on the index during the life of the futures contract. Ideally, one should know in advance the payment of all dividends and discount each one appropriately; unfortunately, this is not an easy task. Thus most people who compute fair value just use some estimated value of dividends to be paid on the index and present discount value them by some average time in which they are expected to be received. It really does not have a large effect on the fair value unless the dividend yield of the index is high and/or a lot of dividends are expected to be paid out shortly.
An example might help to illustrate the point. Suppose that the S&P 500 is trading at 1,000, that a 90-day futures contract exists, that the S&P 500 will pay 5 points of dividends at the end of the first month, and that the money market interest rate is 4%. The fair value of the futures contract using
Eq. (12A.2)
will be
