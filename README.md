# Wordsworth 📜

Wordsworth is a web app to identify anachronistic words and phrases in historical fiction by comparing it to fiction written during the selected decade.

As of Bloomsday (June 16) 2019, Wordsworth is publicly deployed and running on http://wordsworth.us.

### Inspiration & Methodology

Wordsworth is inspired by the work of [Ben Schmidt](https://benschmidt.org), a digital-humanities professor who, in the early 2010s, [wrote about](https://www.theatlantic.com/entertainment/archive/2013/01/did-anyone-say-racial-equality-in-1865-the-language-of-i-lincoln-i/266990/) finding linguistic anachronisms in historical-fiction screenplays by comparing their language to texts written during the period when they were set. Schmidt's program and corpus is not publicly available; Wordsworth is an attempt to create a tool based on this principle that writers can freely use.

There is no good API that allows you to search for words or phrases within books from a certain decade, so Wordsworth looks up words and phrases within its own curated corpus. This corpus consists of English-language novels written between 1800 and 1923, downloaded from [Project Gutenberg](https://gutenberg.org) and processed into word sets and bigram dictionaries using Python. When the user searches for a word or phrase, the app combines all of the word sets/bigram dictionaries from the selected decade into one large set/dictionary, then looks up the words/phrase in that decade-wide data set.

### Features

Site operation is fairly self-explanatory. Users can search for a [specific bigram](http://www.wordsworth.us/bigram-search) (two-word phrase) in fiction from a selected decade, or analyze [a passage of text](http://www.wordsworth.us/word-search) to see if any words in it do not appear in the selected decade. The results pages for both words and bigrams can load [Google Ngram](https://books.google.com/ngrams) charts in an iframe so that the user can learn more about that word/phrase's use over time.

Users can also [register](http://www.wordsworth.us/register) for a free account. This allows them to save a list of words that Wordsworth will ignore automatically when analyzing the logged-in user's passages of text. This may be useful for authors who are working on longer projects and want to automatically ignore things like character names.

Other questions may be answered in the [FAQs](http://www.wordsworth.us/faqs) on the site. Wordsworth's current fiction corpus can be viewed [here](http://www.wordsworth.us/corpus).

### Running Wordsworth On Your Own Server

If you want to clone Wordsworth to your computer and run it locally, here's how to do it.
These instructions are written for installation on Ubuntu 18.04 using the bash shell.
Wordsworth requires Python 3.6 or later.

#### Initial Setup

Clone the Wordsworth repo onto your computer:
```$ git clone https://github.com/MarissaSkud/Wordsworth.git```

Install required Python and Postgres packages:
```$ ubuntu-18.04-setup.bash```

Install the Python module requirements:
```$ pip3 install -r requirements.txt```

In the repo working directory, create a file called secrets.sh containing a single line of code:
```export FlaskSecretKey="[YOUR SECRET KEY]"```,
where ```[YOUR SECRET KEY]``` could be 24 random bytes.

Then, activate the secrets file: 
```$ source secrets.sh```

Establish yourself as a database superuser:
```$ sudo -u postgres createuser -s <your_userid>```

Create the Postgresql database for the app: 
```$ createdb anach_app```

Seed the database:
```$ python3 seed.py```
 
After that, you can run Wordsworth locally, using ```$ python3 server.py```. It will default to running on port 5000 (localhost:5000) but you can modify this in the server.py file.

The server is not currently set to run in debug mode, which means you will need to stop and restart the server for changes to your code to be reflected on localhost. You can put the server into debug mode if you want it to auto-restart when it detects a change.

#### Adding a New Text to Your Local Copy's Corpus

First, add a new line to the file sql_data/books with information about the book you are adding, in the format:
```Title|Author|Year|Country|Decade|word_sets/bookX_set.pickle|bigram_dicts/bookX_dict.pickle```
 
“X” represents the number of this book in the corpus, and should be the same as the line number for this book in the sql_data/books file.
 
If the Country and/or Decade for the book you are trying to add do not appear in the sql_data/countries and/or sql_data/decades files, you will need to add them there as well, for referential integrity.

Then, create a folder in the repo named full_texts. Save the full text of the book that you want to add as a file named bookX_full.txt. (It may also be a good idea to delete extraneous stuff from the full text, such as footnotes, illustration captions, introductions that may have been written at a later date, etc.) Update the file textprocessor.py so that its final line reads ```prepare_texts(X, X+1)```. 

Run the following in python3:
```
>>> import nltk
>>> nltk.download(‘punkt’)
>>> quit()
```

Then, run 
    ```$ python3 textprocessor.py```
from the command line. This will create the word set and bigram dictionary for text X, saved as bookX_set.pickle and bookX_dict.pickle in their respective folders.
 
Finally, from the command line, enter the PostgreSQL database:
    ```$ psql anach_app```
Enter the command:
    ```DROP TABLE books;```
Note that the trailing semicolon is required.
If you also updated the Countries or Decades table, you will also need to ```DROP TABLE countries;``` and/or ```DROP TABLE decades;```.

Exit out of PostgreSQL (```\q```) and run 
    ```$ python3 seed.py```.
This will re-seed the Books table to include information on the new book you added.

### Questions, Issues, and Suggestions

You can submit issues/pull requests here on GitHub, or email me at marissa (dot) wordsworth (at) gmail (dot) com. I want to make this a useful tool for historical fiction writers, but bear in mind that I'm just one woman and this project has the potential to involve massive amounts of data.

### Use & Share!

Please share Wordsworth with your writer friends _and_ your developer friends! I am a San Francisco-based junior engineer and am always seeking ways to learn more. You can get in touch with me here or on [my LinkedIn](https://www.linkedin.com/in/marissa-skudlarek/).
