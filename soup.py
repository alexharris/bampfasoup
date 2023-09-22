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
# Director x
# Screenwriter x
# Cinematographer x
# Cast/With x
# Country x
# Film Year x
# Film Run Time
# Print Source x
# Permission x
# In Person Guest x
# Location x

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

test_nids = ['239940', '239930', '239946' ,'238464','239764','239782','239789','196477','196491','196492','196494','196495','196508']
# test_nids = ['239946']

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

    # Director                           
    director = soup.select('.director')
    director = director[0].text

    # Country                           
    country = soup.select('.country')
    country = country[0].text

    # Location                           
    location = soup.select('.location')
    location = location[0].text    

    # Year                           
    year = soup.select('.year')
    year = year[0].text      

    # Screenwriters
    screenwriters = ''                          
    get_screenwriters = soup.select('.screenwriters li')
    for i in get_screenwriters:
        screenwriters += i.string + ', '

    # Cinematographers 
    cinematographers = ''                          
    get_cinematographers = soup.select('.cinematographers li')
    for i in get_cinematographers:
        cinematographers += i.string + ', '     

    # Source 
    sources = ''                          
    get_sources = soup.select('.source li')
    for i in get_sources:
        sources += i.string + ', '  

    # Permissions 
    permissions = ''                          
    get_permissions = soup.select('.permissions li')
    for i in get_permissions:
        permissions += i.string + ', '     

    # Permissions 
    guests = ''                          
    get_guests = soup.select('.inperson-txt h5')
    for i in get_guests:
        guests += i.string + ', ' 

    # Cast 
    cast = ''                          
    get_cast = soup.select('.cast')
    for i in get_cast:
        cast += i.string.strip() + ' '                                  





    # Actors               
    # print('hello')            
    # body = soup.select('#node-event-full-group-body')
    # print(body[0] )
    # actors = body[0].select('.label-above')[0].find_next_siblings('section')[0].text.strip()
    # actors = re.sub('\s+',' ',actors)
   
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
        f.write(screenwriters) 
        f.write(' | ')
        f.write(cinematographers)               
        f.write(' | ')
        f.write(director)       
        f.write(' | ')
        f.write(country)  
        f.write(' | ')
        f.write(location)
        f.write(' | ')
        f.write(sources)  
        f.write(' | ')
        f.write(permissions)  
        f.write(' | ')
        f.write(year) 
        f.write(' | ')
        f.write(guests) 
        f.write(' | ')
        f.write(cast)                                                                                                               
        f.write('\n')