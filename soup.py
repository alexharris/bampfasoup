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
# Screenwriter
# Cinematographer
# Cast/With
# Country
# Film Year
# Film Run Time
# Print Source
# Permission
# In Person Guest
# Location

# Some good example screenings
# Series of shorts: https://bampfa.org/event/ernies-urban-delights
# Two screenings of one film: https://bampfa.org/event/white-building


from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import csv
# this lets us do a progress bar in the terminal
from tqdm import tqdm 

f = open('output.csv', "w")   

test_nids = ['239940','238464','239764','239782','239789','196477','196491','196492','196494','196495','196508']

# get the real dataset from nodes.csv
get_nids = open("nodes.csv", "r")
nids = csv.reader(get_nids, delimiter=",")
data = list(nids)
all_nids = data[0]

#test_nids to test, all_nids to run 4 real
for nid in tqdm(test_nids):
    req = Request('https://bampfa.org/node/' + nid, headers={'User-Agent': 'Mozilla/5.0'})
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

    print(long_desc)
    
    # Put it all into output.csv
    for date in dates:
        f.write(title.string)
        f.write(' | ')
        f.write(date.string)
        f.write(' | ')
        f.write(series) 
        f.write(' | ')
        f.write(long_desc)                       
        f.write('\n')