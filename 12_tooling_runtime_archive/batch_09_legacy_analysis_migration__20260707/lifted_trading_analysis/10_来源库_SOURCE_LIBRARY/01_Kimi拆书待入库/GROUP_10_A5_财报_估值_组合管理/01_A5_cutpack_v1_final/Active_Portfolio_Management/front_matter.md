# Front Matter (Preface, Contents, Acknowledgments)

- **book_name**: Active Portfolio Management
- **main_source**: pdf
- **cross_check_source**: none
- **pdf_role**: main_text_source
- **split_scope**: pages 1-22

---

ACTIV
PORTFOLIO
MANAGEMENT
A Quantitative Approach for Producing
Superior Returns and Controlling Risk
SECOND EDITION
pS
Se
RICHARD C. GRINOLD AND RONALD N. KAHN
Mathematically rigorous and meticulously orga-
nized, Active Portfolio Management broke new
ground when it first appeared in 1994. By outlining
an innovative process to uncover raw signals of
asset returns, develop them into refined forecasts,
then use those forecasts to construct portfolios
combining exceptional return and minimal
risk—i.e., portfolios that consistently beat the
market—this hallmark book helped thousands
of investment managers.
Active Portfolio Management, Second Edition, now
sets the bar even higher. Like its predecessor, this
volume details how to apply economics, econo-
metrics, and operations research to solving practical
investment problems—and finding superior profit
opportunities. It outlines an active management
framework that begins with a benchmark portfolio,
then defines exceptional returns as they relate to
that benchmark. Beyond the comprehensive treat-
ment of the active management process covered
previously, this new edition expands to cover asset
allocation, long/short investing, information hori-
zons, and other topics relevant today. It revisits a
number of discussions from the first edition, shed-
ding new light on some of today’s most pressing
issues, including risk, dispersion, market impact,
and performance analysis, while providing empiri-
cal evidence where appropriate.
The result is an updated, comprehensive set of
strategic concepts and rules of thumb for guiding
the process of—and increasing the profits from—
active investment management. Organized into
four sections—Foundations, Expected Returns
and Valuation, Information Processing, and
Implementation—that walk you step-by-step
through the entire process, Active Portfolio
Management introduces:
@ The appropriate framework for active man-
agement, and how to use basic portfolio
theory to navigate within that framework
@ Techniques to transform market insights into
specific, profitable investment strategies
@ Long/short strategies—when to use them,
when to avoid them, and why
M Proven rules for evaluating investment
strategies
(continued on back flap)
Digitized by the Internet Archive
in 2022 with funding from
Kahle/Austin Foundation
https://archive.org/details/activeportfoliom0000grin
ACTIVE PORTFOLIO
MANAGEMENT
SECOND EDITION
ACTIVE PORTFOLIO
MANAGEMENT
A QUANTITATIVE APPROACH
FOR PROVIDING SUPERIOR
RETURNS AND
CONTROLLING RISK
RICHARD C. GRINOLD
RONALD N. KAHN
McGraw-Hill
New York
San Francisco
Washington, D.C.
Auckland
Bogota
Caracas
Lisbon
London
Madrid
Mexico City
Milan
Montreal
New Delhi
San Juan
Singapore
Sydney Tokyo Toronto
N PUBLIC LIBRARY
EN
ROLI3b 4e%b3
e
Library of Congress Cataloging-in-Publication Data
Grinold, Richard C.
Active portfolio management : a quantitative approach for providing
superior returns and controlling risk
/ by Richard C. Grinold and Ronald N. Kahn.—2nd ed.
p.
cm.
Includes bibliographical references and index.
ISBN 0-07-024882-6
1. Portfolio management—Mathematical models.
I. Kahn, Ronald N.
II. Title.
HG4529.5.G75
1999
332.6'015’1—dc21
99-21967
CIP
McGraw-Hill
&2
A Division of The McGraw-Hill Companies
Copyright © 2000 by Richard C. Grinold and Ronald N. Kahn. All rights reserved. Printed
in the United States of America. Except as permitted under the United States Copyright
Act of 1976, no part of this publication may be reproduced or distributed in any form or
by any means, or stored in a data base or retrieval system, without the prior written
permission of the publisher.
IAOADO/
DW) WOC/DOe
YWO
7 © 43 2 iO
ISBN 0-07-024882-6
The sponsoring editor for this book was Stephen Isaacs, the editing supervisor was Paul R. Sobel,
and the production supervisor was Elizabeth J. Strange. It was set in Palatino by ATLIS Graphics
and Design.
Printed and bound by R. R. Donnelley & Sons Company.
McGraw-Hill books are available at special quantity discounts to use as premiums and sales
promotions, or for use in corporate training programs. For more information, please write
to the Director of Special Sales, McGraw-Hill, 11 West 19th Street,
New York, NY 10011. Or
contact your local bookstore.
s
This publication is designed to provide accurate and authoritative information in regard to
the subject matter covered. It is sold with the understanding that neither the author nor
the publisher is engaged in rendering legal, accounting, or other professional service. If
legal advice or other expert assistance is required, the services of a competent professional
person should be sought.
—From a Declaration of Principles jointly adopted by a Committee of the American Bar Association
and a Committee of Publishers.
This book is printed on recycled, acid-free paper containing a
minimum of 50% recycled de-inked fiber.
To Leilani
and to Bonnie
ee
-
-_— 7
7
-
=
a
>
~~
="
7
“4
—
_
_
‘ont? a We
:
¥
\
x
@
™
=,
-
COLNE UNS
a
a
ST rrr pn evens eat
ee ee
Preface
xi
Acknowledgments
xv
Chapter 1
Introduction
1
PART ONE
FOUNDATIONS
Chapter 2
Consensus Expected Returns: The Capital
Asset Pricing Model
11
Chapter 3
Risk
41
Chapter 4
Exceptional Return, Benchmarks, and Value Added
87
Chapter 5
Residual Risk and Return: The Information Ratio
109
Chapter 6
The Fundamental Law of Active Management
147
PART TWO
EXPECTED RETURNS AND VALUATION
Chapter 7
Expected Returns and the Arbitrage Pricing Theory
173
Viii
Contents
Chapter 8
Valuation in Theory
199
Chapter 9
Valuation in Practice
225
PART THREE
INFORMATION PROCESSING
Chapter 10
Forecasting Basics
261
Chapter 11
Advanced Forecasting
295
Chapter 12
Information Analysis
315
Chapter 13
The Information Horizon
347
PART FOUR
IMPLEMENTATION
Chapter 14
Portfolio Construction
377
Chapter 15
Long/Short Investing
419
Chapter 16
Transactions Costs, Turnover, and Trading
445
Chapter 17
Performance Analysis
477
Contents
ix
Chapter 18
Asset Allocation
517
Chapter 19
Benchmark Timing
541
Chapter 20
The Historical Record for Active Management
559
Chapter 21
Open Questions
573
Chapter 22
Summary
577
Appendix A
Standard Notation
581
Appendix B
Glossary
583
Appendix C
Return and Statistics Basics
587
INDEX
591
a
Das"
Be
)
sy
y
PY R_E.F
A CLE
Why a second edition? Why take time from busy lives? Why devote
the energy to improving an existing text rather than writing an
entirely new one? Why toy with success?
The short answer is: our readers. We have been extremely
gratified by Active Portfolio Management's reception in the invest-
ment community. The book seems to be on the shelf of every
practicing or aspiring quantitatively oriented investment manager,
and the shelves of many fundamental portfolio managers as well.
But while our readers have clearly valued the book, they have
also challenged us to improve it. Cover more topics of relevance
to today. Add empirical evidence where appropriate. Clarify
some discussions.
The long answer is that we have tried to improve Active Portfo-
lio Management along exactly these dimensions.
First, we have added significant amounts of new material in
the second edition.
New chapters cover Advanced Forecasting (Chap.
11), The Information Horizon (Chap. 13), Long/Short Investing (Chap.
15), Asset Allocation (Chap. 18), The Historical Record for Active Man-
agement (Chap. 20), and Open Questions (Chap. 21).
Some previously existing chapters also cover new material.
This includes a more detailed discussion of risk (Chap. 3), disper-
sion (Chap. 14), market impact (Chap. 16), and academic proposals
for performance analysis (Chap. 17).
Second, we receive exhortations to add more empirical evi-
dence, where appropriate. At the most general level: how do we
know this entire methodology works? Chapter 20, on The Historical
Record for Active Management, provides some answers. We have also
added empirical evidence about the accuracy of risk models, in
Chap. 3.
At the more detailed level, readers have wanted more informa-
tion on typical numbers for information ratios and active risk. Chap-
ter 5 now includes empirical distributions of these statistics. Chapter
15 provides similar empirical results for long /short portfolios. Chap-
ter 3 includes empirical distributions of asset level risk statistics.
xi
xii
Preface
Third, we have tried to clarify certain discussions. We received
feedback on how clearly we had conveyed certain ideas through
at least two channels. First, we presented a talk summarizing the
book at several investment management conferences.’ “Seven
Quantitative Insights into Active Management” presented the key
ideas as:
1. Active Management is Forecasting: consensus views lead
to the benchmark.
2. The Information Ratio (IR) is the Key to Value-Added.
3. The Fundamental Law of Active Management:
IR = IC: \/Breadth.
4. Alphas must control for volatility, skill, and expectations:
Alpha = Volatility - IC - Score.
5. Why Datamining is Easy, and guidelines to avoid it.
6. Implementation should subtract as little value as
possible.
7. Distinguishing skill from luck is difficult.
This talk provided many opportunities to gauge understanding
and confusion over these basic ideas.
We also presented a training course version of the book, called
“How to Research Active Strategies.” Over 500 investment profes-
sionals from New York to London to Hong Kong and Tokyo have
participated. This course, which involved not only lectures, but
problem sets and extensive discussions, helped to identify some
remaining confusions with the material. For example, how does the
forecasting methodology in the book, which involves information
about returns over time, apply to the standard case of information
about many assets at one time? We have devoted Chap. 11, Advanced
Forecasting, to that important discussion.
.
Finally, we have fixed some typographical errors, and added
more problems and exercises to each chapter. We even added a
new type of problem—applications exercises. These use commer-
cially available analytics to demonstrate many of the ideas in the
"The BARRA Newsletter presented a serialized version of this talk during 1997 and
1998.
Preface
xiii
book. These should help make some of the more technical results
accessible to less mathematical readers.
Beyond these many reader-inspired improvements, we may
also bring a different perspective to the second edition of Active
Portfolio Management. Both authors now earn their livelihoods as
active managers.
To readers of the first edition of Active Portfolio Management,
we hope this second edition answers your challenges. To new read-
ers, we hope you continue to find the book important, useful,
challenging, and comprehensive.
Richard C. Grinold
Ronald N. Kahn
bat da
oy, eee
"
ite aon tet
Lis
=
De
ahi
4
Git
Vi
pie etsy
.
TOA
hd ath at
ro
‘ey,
‘
~~
he
ok
.
~
=
et
CLL
it
iw
wi
“gt
we he
,
'
ee
SS
i
i
~~
~ ,
-
*
——
, aa
ly savy ens
gh peek
=i
_@
ait aaa
a!
Pt Ae onus
4 Py
-
ub gen, ,
i
e Re a
on ae
ae
ai aii, a4 by
p
3
oan
a
4 recuse
2)
eae tS»
=
ACKNOWLEDGMENTS
Many thanks to Andrew Rudd for his encouragement of this project
while the authors were employed at BARRA, and to Blake Gross-
man for his continued enthusiasm and support of this effort at
Barclays Global Investors.
Any close reader will realize that we have relied heavily on
the path breaking work of Barr Rosenberg. Barr was the pioneer
in applying economics, econometrics and operations research to
solve practical investment problems. To a lesser, but not less crucial
extent, we are indebted to the original and practical work of Bill
Sharpe and Fischer Black. Their ideas are the foundation of much
of our analysis.
Many people helped shape the final form of this book. Inter-
nally at BARRA and Barclays Global Investors, we benefited from
conversations with and feedback from Andrew Rudd, Blake Gross-
man, Peter Algert, Stan Beckers, Oliver Buckley, Vinod Chandra-
shekaran, Naozer Dadachanji, Arjun DiVecha, Mark Engerman,
Mark Ferrari, John Freeman, Ken Hui, Ken Kroner, Uzi Levin,
Richard Meese, Peter Muller, George Patterson, Scott Scheffler, Dan
Stefek, Nicolo Torre, Marco Vangelisti, Barton Waring, and Chris
Woods. Some chapters appeared in preliminary form at BARRA
seminars and as journal articles, and we benefited from broader
feedback from the quantitative investment community.
At the more detailed level, several members of the research
groups at BARRA and Barclays Global Investors helped generate
the examples in the book, especially Chip Castille, Mikhail Dvorkin,
Cliff Gong, Josh Rosenberg, Mike Shing, Jennifer Soller, and Ko
Ushigusa.
BARRA and Barclays Global Investors have also been support-
ive throughout.
Finally, we must thank Leslie Henrichsen, Amber Mayes, Car-
olyn Norton, and Mary Wang for their administrative help over
many years.
a
re
Pe
iy)
vil
ual
Hi
§
'
«jy!
a
+ > 1.
; py
>
5
Ay
cy
.
#!
Mi
Yt Mi
= vineieanie
ia
d
Prats
au ato
=
ays
Seam
NeMESS aie od ee
» AO
STeaM oh &
che
a! 4 Sekt Salt
ay dial
~ @ aco vie wl
vaibss
“coe ve al all
a
nish: Ht
ree Sell 0 sasiers 3
Vet, ins Caps Anahi
ge ivi
27 leita Sale sions scarey Aaeardeney ns
>
7
ti =
-
1! ea cae
tastit wcll epeatey belo
La
=
Desert, Gavbeatod
ti bas
boca nae Se
‘caleatt
ny
A
et sc
Sh
fear
+.¢
z
o>
wits) eee? o
.
et
scout ke
gge'd (gaa erat aie
ent
4,
— pute
fi pres icp emignil
Jeu Las oie coup fh
,
eA
Sen
Aw im
~Sanway
pete
y song
3
:
i
e
lr.
exe
ACTIVE PORTFOLIO
MANAGEMENT
