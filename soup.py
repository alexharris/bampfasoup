# Showtime One x
# Showtime Two x
# Film Series x
# Film Screening Title / Odds and Ends  x
# Film Title 
# Alternate Title
# Long Description
# Film Note Author
# Film Note Author Title
# Legacy Credits
# Director
# Screenwriter x
# Cinematographer x
# Cast/With x
# Country
# Film Year
# Film Run Time
# Print Source x
# Permission
# In Person Guest
# Location

# Some good example screenings
# Series of shorts: https://bampfa.org/event/ernies-urban-delights
# Two screenings of one film: https://bampfa.org/event/white-building


from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import csv
import re
# this lets us do a progress bar in the terminal
from tqdm import tqdm 

f = open('output.csv', "w")   

# test_nids = ['239940','238464','239764','239782','239789','196477','196491','196492','196494','196495','196508']
test_nids = ['239940']

# get the real dataset from nodes.csv
get_nids = open("nodes.csv", "r")
nids = csv.reader(get_nids, delimiter=",")
data = list(nids)
all_nids = data[0]

#test_nids to test, all_nids to run 4 real
for nid in tqdm(test_nids):
    req = Request('https://soup-bampfa-site.pantheon.berkeley.edu/node/' + nid, headers={'User-Agent': 'Mozilla/5.0'})
    html_page = urlopen(req).read()

    soup = BeautifulSoup(html_page, 'html.parser')

    title = soup.css.select('.field-name-title h2')[0]
    dates = soup.find_all("span", "date-display-single")
   
    # Parent Series
    # this structure lets us test if something exists before using it, otherwise error
    get_series = soup.select('.block-views-relatedfilms-in-series-block .view-grouping-header a')
    if len(get_series)>0:
        series = get_series[0].string
    else:
        series = 'NOSERIES'

    # Long Description
    get_long_desc = soup.select('.views-field-field-ao-curator-description .field-content p')    
    if len(get_long_desc)>0:
        long_desc = str(get_long_desc[0])
    else:
        long_desc = 'NOLONGDESCRIPTION'

    # Crew
    screenwriter = ''
    cinematographer = ''
    source = ''

    film_details = soup.select('.block-views-film-details-block .bampfa-accordion-content *')
    for i in range(0,len(film_details)):
        if(film_details[i].string == 'Screenwriter'):
            for i in film_details[i+1]:
                screenwriter += i.string.strip()
        elif(film_details[i].string == 'Cinematographer'):
            for i in film_details[i+1]:
                cinematographer += i.string.strip() 
        elif(film_details[i].string == 'Source'):
            for i in film_details[i+1]:
                source += i.string.strip()    

    # Actors                           
    body = soup.select('#node-event-full-group-body')
    actors = body[0].select('.label-above')[0].find_next_siblings('section')[0].text.strip()
    actors = re.sub('\s+',' ',actors)
   
    # Put it all into output.csv
    for date in dates:
        f.write(title.string)
        f.write(' | ')
        f.write(date.string)
        f.write(' | ')
        f.write(series) 
        f.write(' | ')
        f.write(long_desc)
        f.write(' | ')
        f.write(screenwriter)       
        f.write(' | ')
        f.write(cinematographer)   
        f.write(' | ')
        f.write(source)    
        f.write(' | ')
        f.write(actors)                                                 
        f.write('\n')