### Project naming
-Some ideas: Trivia Research Equipment (for) Broad Enhancement (of) Knowledge - T.R.E.B.E.K.

### Master project TODOs
TODO - NLP to group answers (HARD) (Word2Vec, doc2Vec, GloVe, https://www.kylepoole.me/blog/20200912_Wikipedia_Quiz/) (Thinking about it, there's gonna have to be some level of manual classification.  Absolutely no way for an algorithm to distinguish between Richard III the play and Richard III the monarch from the answer alone.  Perhaps if you included all the clue text as well?)

TODO - Break some of these functions out into other files?

TODO - Handle quotes in answers? (which I guess happens when Alex has to say the answer after a triple stumper?) (See "On, Wisconsin", game S25URL3070)

TODO - Learn how to do template strings rather than concatenation in Python

TODO - Marie Antoinette? (Still some strangeness with foreign words)

TODO - Abbreviation/nickname handling (FDR, JFK, etc.)

TODO - Evaluate the alternate_answer handling (perhaps only try the last name thing if the NLP determines that it's a person?  This is probably necessary to handle South Africa, New York, etc.)

TODO - It's probably to download the page once, save it locally, and then you can parse both quicker and multiple times if need be

### scrape_game.py TODOs
TODO - Do I need all these re.complie lines?

### Stretch goals
-Knowledge analyzer like Roger Craig made

-Flashcard app (asks you a random answer and after a few seconds shows you the flashcard to see if you know the big ones.  Also the ability to annotate the card so you can explain a reference if it's not immediately obvious)

### Helpful links
https://www.reddit.com/r/Jeopardy/comments/9rr8yg/archive_of_categorized_questions/ (Not used any of this code...yet)