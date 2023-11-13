# Soft-Power-Index

The following Soft Power Index (SPI) is loosely inspired by the work of Jonathan McClory for Portland (https://softpower30.com/) and the conceptual idea from Nye (1990). Within my Master's thesis, I am using this index to study the effects of soft power on bilateral trade over a timespan of up to 30 years. This repo is used to explain my choice of datasets and to combine my data collection and cleaning efforts.

The Soft Power: "This power tends to arise from such resources as cultural and ideological attraction as well as rules and
institutions of international regulations" (Nye 1990, p. 168).

## The target for this SPI is:
1) a timespan of at least 30 years
2) at least the inclusion of the G20
3) ideally consisting of over 100 countries
4) create a internally valid ranking system
5) avoid a systemic bias for Western liberal democracies

### The following list will explain my choice of sub-indices. 

Based on McClory's 6 main sub-indices:
1.	Government Sub-index:
  - Polity 5 project [1812-2018] 
2.	Culture Sub-index:
  - Music Global Top 50 Charts + Global Charts by Spotify
  - World Value Survey Global Culture Map [1998-2023] 
      - Needs lots of interpolation, limited amount of countries represented. But very interesting.
  - World Religion Data [1950-2010; 5 year steps]
3.	Global Engagement Sub-index:
  - Net Migration (rate) [1960-2020] 
     - Includes both voluntarily migration and refugees (https://ourworldindata.org/migration-definition)
  - Number of refugees living in the host country per 1,000 people (Number of refugees living in the host country per 1,000 people)
     - specify direct impact of refugess
  -	Number of Embassies Abroad
     - Difficulty finding complete Data set for whole 	
  -	Membership of Multilateral Organizations
  -	Overseas Development Aid
  -	Permanent Member UN Security Council and Presidency Bonus
4.	Education Sub-index:
  - Scimago Country Citations Ranking [1996-2022] 
      - Rough estimate of the scientific power only based on Elsevier / Scopus database. Will be used as a composite index, e.g.
        Ranking = Citations per (citable) document * H-Index
  - R&D Spending by GDP per capita [1996-2022] 
      - A higher R&D spending results in higher tech output with well known brands like Samsung, Siemens, Google etc. This helps the     
        cultural perception as a technologically advanced nation.
5.	Enterprise Sub-index:
  - Corruption Perceptions Index (CPI) [1995-2022] 
      - Will only lower SPI. A high corruption level is bad for the perception in any case. However, the CPI has been criticised for its reliability and validity.
  - Forbes Global 2000 [2003-2023] Global 500 [1990 - 2023] (SOURCE OF EVERY DATA?)
      - "Multinational corporations are another source of cooptive power" (Nye 1990, p.168)
6.	Digital Sub-index: Questionable wether to include or omit. Unclear which variables to use which could represent soft power.. 


# Source: 
CPI: 
    - https://www.transparency.org/en/cpi/2010
    - https://www.transparency.org/en/cpi/2011
    - https://de.wikipedia.org/wiki/Korruptionswahrnehmungsindex#2022](https://en.wikipedia.org/wiki/Corruption_Perceptions_Index
    
Polity 5:
    - https://www.systemicpeace.org/polityproject.html

Net Migration:
    - https://data.worldbank.org/indicator/SM.POP.NETM?end=1985&start=1985&view=map&year=2013

Nye, J. S. (1990). Soft Power. Foreign Policy, 80, 153–171. https://doi.org/10.2307/1148580

R&D Spending:
    - https://ourworldindata.org/research-and-development

Scimago: 
    - https://www.scimagojr.com/countryrank.php?order=itp&ord=desc

World Religion Data:
    - https://correlatesofwar.org/data-sets/world-religion-data/ 

World Value Survey: 
    - https://www.worldvaluessurvey.org/WVSNewsShow.jsp?ID=467
