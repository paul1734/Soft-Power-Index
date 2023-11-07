# Soft-Power-Index

The following Soft Power Index (SPI) is created for my Master's thesis in Economics at the University of Kiel. It is losely inspired by the work of Jonathan McClory for Portland (https://softpower30.com/) and the conceptual idea from Nye (1990). Within my Master's thesis, I am using this index to study the effects of soft power on bilateral trade over a timespan of up to 30 years. This repo is used to explain my choice of datasets and to combine my data collection and cleaning efforts.

The Soft Power: "This power tends to arise from such resources as cultural and ideological attraction as well as rules and
institutions of international regulations" (Nye 1990, p. 168).

## The target for this SPI is:
1) a timespan of at least 30 years
2) at least the inclusion of the G20
3) ideally consisting of over 100 countries
4) create a internally valid ranking system
5) avoid a systemic bias for Western liberal democracies

### The following list will explain my choice of sub-indices. 
Shema:
1. Main Sub-index:
  - Data Source [timespan of complete data] (website source)
     - Explanation for usage, shortcomings and feasible remedies

Based on McClory's 6 main sub-indices:
1.	Government Sub-index:
  - Polity 5 project [1812-2018] (https://www.systemicpeace.org/polityproject.html)
3.	Culture Sub-index:
4.	Global Engagement Sub-index:
•	Number of Embassies/High Commissions Abroad
•	Membership of Multilateral Organizations
•	Overseas Development Aid
5.	Education Sub-index:
  - Scimago Country Citations Ranking [1996-2022] (https://www.scimagojr.com/countryrank.php?order=itp&ord=desc)
      - Rough estimate of the scientific power only based on Elsevier / Scopus database. Will be used as a composite index, e.g.
        Ranking = Citations per (citable) document * H-Index
  - R&D Spending by GDP per capita [1996-2022] (https://ourworldindata.org/research-and-development)
      - A higher R&D spending results in higher tech output with well known brands like Samsung, Siemens, Google etc. This helps the     
        cultural perception as a technologically advanced nation.
6.	Enterprise Sub-index:
  - Corruption Perceptions Index (CPI) [1995-2022] (https://de.wikipedia.org/wiki/Korruptionswahrnehmungsindex#2022 and )
      - Will only lower SPI. A high corruption level is bad for the perception in any case. However, the CPI has been criticised for its           reliability and validity.
  - Forbes Global 2000 [2003-2023] Global 500 [1990 - 2023] (SOURCE OF EVERY DATA?)
      - "Multinational corporations are another source of co-optive power" (Nye 1990, p.168)
7.	Digital Sub-index: Questionable wether to include or omit. Unclear which variables to use which could represent soft power.. 


# Source: 
Nye, J. S. (1990). Soft Power. Foreign Policy, 80, 153–171. https://doi.org/10.2307/1148580
