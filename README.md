# Soft-Power-Index

The following Soft Power Index (SPI) is loosely inspired by the work of Jonathan McClory for Portland (https://softpower30.com/) and the conceptual idea from Nye (1990). Within my Master's thesis, I am using this index to study the effects of soft power on bilateral trade over a timespan of up to 30 years. This repo is used to explain my choice of datasets and to combine my data collection and cleaning efforts.

Soft Power "tends to arise from such resources as cultural and ideological attraction as well as rules and
institutions of international regulations" (Nye 1990, p. 168). "Soft power is the ability to get what you want through attraction rather than coercion or payments. When you can get others to want what you want, you do not have to spend as much on sticks and carrots to move them in your direction. Hard power, the ability to coerce, grows out of a country’s military and economic might. Soft power arises from the attractiveness of a country’s culture, political ideals, and policies. When our policies are seen as legitimate in the eyes of others, our soft power is enhanced." (Nye 2004, p. 256).

## The target for this SPI is:
1) a timespan of at least 30 years
2) at least the inclusion of the G20
3) ideally consisting of over 100 countries
4) create a internally valid ranking system
5) avoid a systemic bias for Western liberal democracies
   - ‘the power of attraction is not inherently liberal or Western’,
      since a Hollywood flm, for example, ‘may produce attraction in Brazil at the same time it produces
      repulsion in Saudi Arabia’ (Nye 2021, p. 201; in Chitty et al 2023)  

## The following table explains my data choice which will be present in the soft power index

| Data                                        | Type       | Year Coverage               | Static / Yearly | Soft Power Category      | Interpolation | Extrapolation | Score   | Notes                                                                                                                                                            |
| ------------------------------------------- | ---------- | --------------------------- | --------------- | ------------------------ | ------------- | ------------- | ------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Country Similarity Index                    | Bilateral  | 1990 - 2020                 | Yearly          | Culture                  | unclear       | unclear       | unclear |                                                                                                                                                                  |
| Education: Inbound Int. Students by Country | Bilateral  | 1999 - 2020                 | Yearly          | Foreign Policy & Culture | Yes           | No            | 1,75    | Extrapolation would be irresponsible for this length of data. Interpolation for missing years by using the former annual value (for each bilateral combination). |
| Migration                                   | Bilateral  | 1990 - 2020 (every 5 years) | Yearly          | Foreign Policy           | Yes           | No            | 2,75    |                                                                                                                                                                  |
| Refugees                                    | Bilateral  |                             |                 | Foreign Policy           | unclear       | unclear       | unclear |                                                                                                                                                                  |
| Polity                                      | Bilateral  | 1990 - 2018                 | Yearly          | Political Values         | Yes           | Yes           | 2,25    | Interpolation for nan values.                                                                                                                                    |
| Corruption: CPI                             | Unilateral | 1995-2022                   | Yearly          | Political Values         | Yes           | Yes           | 1,25    | Backfill and Frontfill for a couple years                                                                                                                        |
| Science Citations                           | Unilateral | 1990 - 2020                 | Static (-0,5)   | Political Values         | No            | No            | 1,5     | Unsure whether to use static variable or not. Could als be proxied by other science related variables.                                                           |
| Science: R&D Spending by GDP                | Unilateral | 1996-2020                   | Yearly          | Political Values         | Yes           | Yes           | 1,25    |                                                                                                                                                                  |
| Tourism: Int Arrivals                       | Unilateral | 1995 - 2020                 | Yearly          | Culture                  | unclear       | unclear       | unclear |                                                                                                                                                                  |
| Tourism: Int Departures                     | Unilateral | 1995 - 2020                 | Yearly          | Culture                  | unclear       | unclear       | unclear | A lot of missing data for every country                                                                                                                          |
| Unesco Heritage Sites                       | Unilateral | 1990 - 2020                 | Yearly          | Culture                  | No            | No            | 2       |                                                                                                                                                                  |
### The following list will explain my choice of data and possible further extension. 

Based on McClory's 6 main sub-indices:
1.	Government Sub-index:
  - Polity 5 project [1812-2018]
  - Diplometrics Database [1960-2020]; Includes every state visit to foreign embassy for past 60 years
2.	Culture Sub-index:
  - Country Similarity Index (CSI) / Distance Matrix
    - no peer reviewed article citing it, difficulty of using it in academic context.
    - However, great methodology and useful application.
    - Similar in construction to this paper (https://zenodo.org/records/3275138) on the Trade Similarity Index for the EU
        - Use bilateral distance relationship within SPI 
  - Music Global Top 50 Charts + Global Charts by Spotify
    - Difficult to find; mostly dominated by US musicians 
  - World Value Survey Global Culture Map [1998-2023] 
      - Needs lots of interpolation, limited amount of countries represented. But very interesting.
  - World Religion Data [1950-2010; 5 year steps]
      - Will be interpolated for years 2015 and 2020
      - Interpolation for 4 years between each data point
      - Data as percent of religious denomination
        - e.g. catholic, anglican, protestant (see: https://correlatesofwar.org/wp-content/uploads/wrp-codebook-bibliography.pdf)
        - Either do superficial: Only Christianity, Islam etc. without specification or use specifics
          - Catholicism or Protestantism doesn't play a huge role for Christian nations anymore
          - However, divide between shia and sunni is still very important
            -> Will use specifics; calculate likeness between each country?
              - Use of clustering? Give each country their specific religious sphere 
3.	Global Engagement Sub-index:
  - Net Migration (rate) [1960-2020] 
     - Includes both voluntarily migration and refugees (https://ourworldindata.org/migration-definition)
  - Number of refugees living in the host country per 1,000 people 
     - specify direct impact of refugess
           -> Refugees are included in the net migration rate; problem of endogeneity?
             - Should be manageable 
  -	Number of Embassies Abroad
     - Difficulty finding complete Data set for whole timeframe
       - Maybe only use current year and assume it would stay relatively constant? Difficult to argue for this, irresponsible assumption
  -	Membership of Multilateral Organizations
      - G20, IMF, WTO, World Bank
      - Political Unions: EU, ASEAN, African Union (-> Why not include smaller ones?)
        - Also, the EU  has more political weigth / cohesion than most other supranational orgs., introduce some sort of weigth?   	
  -	Overseas Development Aid -> Questionable as it is highly tied to economic might; can be seen as buying influence.
  -	Permanent Member UN Security Council and Presidency Bonus
4.	Education Sub-index:
  - Scimago Country Citations Ranking [1996-2022] 
      - Rough estimate of the scientific power only based on Elsevier / Scopus database. Will be used as a composite index, e.g.
        Ranking = Citations per (citable) document * H-Index
  - R&D Spending by GDP per capita [1996-2022] 
      - A higher R&D spending results in higher tech output with well known brands like Samsung, Siemens, Google etc. This helps the     
        cultural perception as a technologically advanced nation. -> However, also strongly tied to economic might. 
5.	Enterprise Sub-index:
  - Corruption Perceptions Index (CPI) [1995-2022] 
      - Will only lower SPI. A high corruption level is bad for the perception in any case. However, the CPI has been criticised for its reliability and validity.
  - Forbes Global 2000 [2003-2023] Global 500 [1990 - 2023] (SOURCE OF EVERY DATA?)
      - "Multinational corporations are another source of cooptive power" (Nye 1990, p.168) -> However, strongly correlated to economic success.
6.	Digital Sub-index: Questionable wether to include or omit. Unclear which variables to use which could represent soft power.
  - could include: telephone, mail and post service, internet connectivity, TV as a whole
  - List of international broadcasters: https://en.wikipedia.org/wiki/List_of_international_broadcasters
        - TV and Radio   


# Source: 
CPI: 

    - https://www.transparency.org/en/cpi/2010
    
    - https://www.transparency.org/en/cpi/2011
    
    - https://de.wikipedia.org/wiki/Korruptionswahrnehmungsindex#2022](https://en.wikipedia.org/wiki/Corruption_Perceptions_Index

CSI:

    - https://objectivelists.com/2020/05/30/country-similarity-index/

Diplometrics:

    - https://korbel.du.edu/pardee/research/diplometrics/diplomatic-representation

Polity 5:

    - https://www.systemicpeace.org/polityproject.html

Net Migration:

    - https://data.worldbank.org/indicator/SM.POP.NETM?end=1985&start=1985&view=map&year=2013

Nye, J. S. (1990). Soft Power. Foreign Policy, 80, 153–171. https://doi.org/10.2307/1148580

Nye, J. S. (2004). Soft Power and American Foreign Policy. Political Science Quarterly, 119: 255-270. https://doi.org/10.2307/20202345

R&D Spending:
    
    - https://ourworldindata.org/research-and-development


Chitty, N., Ji, L., & Rawnsley, G.D. (Eds.). (2023). The Routledge Handbook of Soft Power (2nd ed.). Routledge. https://doi.org/10.4324/9781003189756


Scimago: 
    
    - https://www.scimagojr.com/countryrank.php?order=itp&ord=desc

World Religion Data:
    
    - https://correlatesofwar.org/data-sets/world-religion-data/ 

World Value Survey: 
    
    - https://www.worldvaluessurvey.org/WVSNewsShow.jsp?ID=467
