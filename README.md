# Graphilm
Un projet incluant Graphes de connaissance

# Data

## Data sources 
The data was taken from 
- https://developer.imdb.com/non-commercial-datasets/
- https://www.wikidata.org/wiki/Wikidata:Main_Page
- only the films produced from 2000 to now were collected from wikidata

## Data prep
1. I consider only film that are produced after 1960 (i keep a row if either start or end date is after 1960 due to missing data)
2. I clean unrelevant data on other files with films Ids i juste dropped
    For this, I created a script `filter_titles.py` which produces in output a file containing films Ids that I dropped
    then those Ids are used to filter other files with `clean_by_ids.py` script. 

