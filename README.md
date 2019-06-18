# Wordsworth 📜

Wordsworth is a web app to identify anachronistic words and phrases in historical fiction by comparing it to fiction written during the selected decade.

As of Bloomsday (June 16) 2019, Wordsworth is publicly deployed and running on http://wordsworth.us.

### Inspiration & Methodology

Wordsworth is inspired by the work of [Ben Schmidt](benschmidt.org), a digital-humanities professor who, in the early 2010s, [wrote about](https://www.theatlantic.com/entertainment/archive/2013/01/did-anyone-say-racial-equality-in-1865-the-language-of-i-lincoln-i/266990/) finding linguistic anachronisms in historical-fiction screenplays by comparing their language to texts written during the period when they were set. Schmidt's program and corpus is not publicly available; Wordsworth is an attempt to create a tool based on this principle that writers can freely use.

There is no good API that allows you to search for words or phrases within books from a certain decade, so Wordsworth looks up words and phrases using its own proprietary corpus. This corpus consists of English-language novels written between 1800 and 1923, downloaded from [Project Gutenberg](gutenberg.org) and processed into word sets and bigram dictionaries using Python. When the user searches for a word or phrase, the app combines all of the word sets/bigram dictionaries from the selected decade into one large set/dictionary, then looks up the words/phrase in that decade-wide data set.

### Usage

Site operation is fairly self-explanatory. Users can search for a [specific bigram](http://www.wordsworth.us/bigram-search) (two-word phrase) in fiction from a selected decade, or analyze [a passage of text](http://www.wordsworth.us/word-search) to see if any words in it do not appear in the selected decade. The results pages for both words and bigrams can load [Google Ngram](https://books.google.com/ngrams) charts in an iframe so that the user can learn more about that word/phrase's use over time.

Users can also [register](http://www.wordsworth.us/register) for a free account. This allows them to save a list of words that Wordsworth will ignore automatically when analyzing the logged-in user's passages of text. This may be useful for authors who are working on longer projects and want to automatically ignore things like character names.

Other questions may be answered in the [FAQs](http://www.wordsworth.us/faqs) on the site. Wordsworth's current fiction corpus can be viewed [here](http://www.wordsworth.us/corpus).

### Questions, Issues, and Suggestions

You can submit issues/pull requests here on GitHub, or email me at marissa (dot) wordsworth (at) gmail (dot) com. I want to make this a useful tool for historical fiction writers, but bear in mind that I'm just one woman and this project has the potential to involve massive amounts of data.

### Use & Share!

Please share Wordsworth with your writer friends _and_ your developer friends! I am a San Francisco-based developer and I'll be looking for a junior engineering position as of July 1, 2019.
