# Wordsworth 📜

Wordsworth is a web app to identify anachronistic words and phrases in historical fiction by comparing it to fiction written during the selected decade.

As of Bloomsday 2019, Wordsworth is publicly deployed and running on http://wordsworth.us.

### Inspiration & Methodology

Wordsworth is inspired by the work of Ben Schmidt, a digital-humanities professor who, in the early 2010s, wrote some articles about finding linguistic anachronisms in historical-fiction screenplays by comparing their language to the language of books written during the time period. Schmidt's program and corpus is not publicly available; Wordsworth is an attempt to create a tool based on this principle that writers can freely use.

There is no good API that allows you to search for words or phrases within books from a certain decade, so Wordsworth looks up words and phrases from its own proprietary corpus. This corpus consists of English-language novels written between 1800 and 1923, downloaded from Project Gutenberg and processed into word sets and bigram dictionaries using Python. When the user tries to search for a word or phrase, the app combines all of the word sets/bigram dictionaries from that decade into one large set/dictionary, then looks up the words/phrase in that larger data set.
