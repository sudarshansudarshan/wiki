"""
This python program will consider a city and extract all the proper nouns from
the city and create a list of words with their time of arrival, in the revision
history. 

*India is a country in south asia. The place is more of a sub-continent than a
country. There are 26 languages spoken in the country with *Hindi being one of
the widely used official language. India got its independence on 15th of August
1947. Although, many freedom fighters were involved in the freedom struggle,
*Mahatma *Gandhi is considered to have played a major role. Post Independence,
the country got sub-divided into states with *Delhi being the capital.
*Bangladesh and *Pakistan saw itself distancing from the country, thus creating
the partition of this region for the first time in the documented history 

(There are a total of 7 proper nouns in the above paragraph.) 
"""
import spacy
nlp = spacy.load("en_core_web_sm")

def list_of_articles(L):
    """


    """

def extract_timeseries_propernouns(article_name):
    """
    Given an article_name, let us say _India_, we need to extract all the
    proper nouns across the revision history of the given article and return a
    list in the form: [(time,timestep,no_propernouns),...]. Where time is the
    date/time of revision, timestep represents the
    revision history number and the no_propernouns is the total number of
    proper nouns added in that revision history.
    List of tasks:
    1) Download the master json file: Jayant
    2) Read the json file, one revision at a time and populate the triple as
    stated above: Nivedita/Shahid.
    """

def no_of_propernouns(s):
    """
    Given a string s, return the proper nouns as a set
    """
    doc = nlp(s)
	count = 0
	for tok in doc:
    		if tok.pos_ == "PROPN":
			count += 1
def master_json(article_name):
    """
    Given the article_name create a master json file containing all the
    revisions. Include more details on this docstring.
    """
