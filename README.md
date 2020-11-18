WIP

The end goal of this project is to generate some tools to help with Jeopardy study, ranging from simple flash cards to more complex analysis

The files that actually scrape J! Archive have been intentionally omitted from the repo since scraping it without limits is discouraged.  My personal scrapes will have some safeguards on them to avoid overloading their servers and generally being a nuisance.

Eventually the complete clue/answer database will be available here which is the end goal of the scraping anyway.

SQL Stuff

-Formatting sqlite3

.mode Column

-Count number of rows

SELECT COUNT(\*) FROM answers;

-Getting repeated answers above a certain threshold

SELECT answer, COUNT(answer) as dupes

FROM answers

GROUP BY answer

HAVING dupes > some_threshold

ORDER BY dupes DESC;

-Checking number of distinct games for a given season

SELECT COUNT(DISTINCT gameid) FROM answers WHERE seasonid='some_season';

-Descending list of clues per game (to determine if any games were scraped twice or have a large number of missing clues)

SELECT COUNT(\*) FROM ANSWERS GROUP BY gameid ORDER BY COUNT(\*) DESC