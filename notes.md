### Project naming
-Some ideas: Trivia Research Equipment (for) Broad Enhancement (of) Knowledge - T.R.E.B.E.K.

### Master project TODOs
TODO - Categorization, more review of entity types

TODO - Evaluate the alternate_answer handling (perhaps only try the last name thing if the NLP determines that it's a person?  This is probably necessary to handle South Africa, New York, etc.)

TODO - NLP to group answers (HARD) (Word2Vec, doc2Vec, GloVe) (https://pythonprogramminglanguage.com/kmeans-elbow-method/, https://pythonprogramminglanguage.com/kmeans-text-clustering/)

TODO - Break some of these functions out into other files?

TODO - Handle quotes in answers? (which I guess happens when Alex has to say the answer after a triple stumper?) (See "On, Wisconsin", game S25URL3070)

TODO - Move to formatted strings rather than concatenation

TODO - Marie Antoinette? (Still some strangeness with foreign words?) (This actually seems to be working now)

TODO - Abbreviation/nickname handling (FDR, JFK, etc.)

TODO - It's probably to download the page once, save it locally, and then you can parse both quicker and multiple times if need be (Would like to do this when I scrape again to get daily double data, so I can try and figure out my hit rate on DDs)

TODO - Check requirements.txt (Remember that some of them are silent dependencies of wordcloud)

TODO - Get that last game that failed scraping

TODO - Some of the answers still have stop words in them (e.g. the liver, an elephant).  I think ideally what I would have done is strip stop words on the initial scrape. Perhaps I can do this when I re scrape to save the pages

TODO - Do I need all these re.complie lines?

TODO - Add a SQL schema file
### Stretch goals
-Knowledge analyzer like Roger Craig made

-Flashcard app (asks you a random answer and after a few seconds shows you the flashcard to see if you know the big ones.  Also the ability to annotate the card so you can explain a reference if it's not immediately obvious) (Might want to reshape the word clouds for phone screen sizes)

-Perhaps the best way to do flashcards is to do title-less word clouds and then turn them into a spaced repitition deck in Anki (this lacks the notation element which would be nice)

### Helpful links
https://www.reddit.com/r/Jeopardy/comments/9rr8yg/archive_of_categorized_questions/ (Not used any of this code...yet)
https://www.reddit.com/r/Jeopardy/comments/768qv2/trivia_trainer_my_attempt_at_roger_craigs/
https://en.wikipedia.org/wiki/Leitner_system
https://en.wikipedia.org/wiki/Anki_(software)
https://en.wikipedia.org/wiki/Roger_Craig_%28Jeopardy!_contestant%29
https://www.reddit.com/r/Jeopardy/comments/7xjthd/how_to_sort_clues_into_categories_and/ ( ROGER CRAIG ACTUALLY RESPONDS HERE )
https://vimeo.com/48070812