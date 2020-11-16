WIP

The end goal of this project is to generate some tools to help with Jeopardy study, ranging from simple flash cards to more complex analysis

The files that actually scrape J! Archive have been intentionally omitted from the repo since scraping it without limits is discouraged.  My personal scrapes will have some safeguards on them to avoid overloading their servers and generally being a nuisance.

Eventually the complete clue/answer database will be available here which is the end goal of the scraping anyway.

SQL Stuff

-Formatting sqlite3

.mode Column

-Getting repeated answers above a certain threshold

SELECT answer, count(answer) as dupes

FROM answers

GROUP BY answer

HAVING count(answer) > some_threshold

ORDER BY count(answer) DESC;