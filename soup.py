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

test_nids = ['240575', '240480', '239940', '239930', '239946' ,'238464','239764','239782','239789','196477','196491','196492','196494','196495','196508']
# test_nids = ['240575'] #one film, multiple showtimes
# test_nids = ['240480'] #program of shorts
# test_nids = ['240480', '239940'] #program of shorts

# get the real dataset from nodes.csv
get_nids = open("nodes.csv", "r")
nids = csv.reader(get_nids, delimiter=",")
data = list(nids)
all_nids = data[0]

f.write('Date | Showtime One | Showtime Two | Film Series | Film Screening Title / Odds and Ends | Film Title | Alternate Title	| Long Description	| Film Note Author | Film Note Author Title	| Legacy Credits | Director | Screenwriter | Cinematographer | Cast/With | Country | Film Year | Film Run Time | Print Source | Permission | In Person Guest | Location')
f.write('\n')

#test_nids to test, all_nids to run 4 real
for nid in tqdm(test_nids):
    req = Request('https://soup-bampfa-site.pantheon.berkeley.edu/node/' + nid, headers={'User-Agent': 'Mozilla/5.0'})
    html_page = urlopen(req).read()

    soup = BeautifulSoup(html_page, 'html.parser')

    title = soup.css.select('.field-name-title h2')[0]
    dates = soup.find_all("span", "date-display-single")
    times = soup.find_all("div", "just-time")

    get_times = soup.find_all("div", "just-time")
    if len(get_times)>0:
        time1 = get_times[0].string
        if len(get_times)>1:
            time2 = get_times[1].string
        else:
            time2 = 'NOTIME2'
    else:
        time1, time2 = 'NOTIMES'
   
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

    # Guests 
    guests = ''                          
    get_guests = soup.select('.inperson-txt h5')
    for i in get_guests:
        guests += i.string + ', ' 

    # Cast 
    cast = ''                          
    get_cast = soup.select('.cast')
    for i in get_cast:
        cast += i.string.strip() + ' '                                  

    # Put it all into output.csv
    # go through multiple showtimes of a single screening
    j = 0 #track the iteration
    for date in dates:
        
        # Write main screening info    
        f.write(date.string)
        f.write(' | ')   
        f.write(time1)
        f.write(' | ') 
        f.write(time2)
        f.write(' | ')   
        f.write(series)
        f.write(' | ') 
        f.write(title.string)
        f.write(' | ')   
        f.write(title.string)
        f.write(' | ')   
        f.write('alt title')        
        f.write(' | ')  
        f.write(long_desc)
        f.write(' | ')   
        f.write('film note author')
        f.write(' | ')  
        f.write('film note author title')
        f.write(' | ') 
        f.write('legacy credits')     
        f.write(' | ') 
        f.write(director) 
        f.write(' | ') 
        f.write(screenwriters) 
        f.write(' | ') 
        f.write(cinematographers) 
        f.write(' | ') 
        f.write(cast)
        f.write(' | ') 
        f.write(country)
        f.write(' | ') 
        f.write(year)
        f.write(' | ') 
        f.write('run time')                                                                                                                                                                                                                                                          
        f.write(' | ') 
        f.write(sources)   
        f.write(' | ') 
        f.write(permissions)
        f.write(' | ') 
        f.write(guests)    
        f.write(' | ') 
        f.write(location)                                         
        f.write('\n')
        # Check for program of shorts
        # if they exist then we do a new row with short film info for what exists
        # and the general screening info for the rest
        if(soup.select('.block-views-multiple-films-block > h5')):
            shorts = soup.select('.block-views-multiple-films-block > section')
            for short in shorts:  
                f.write(date.string)
                f.write(' | ')   
                f.write(time1)
                f.write(' | ') 
                f.write(time2)
                f.write(' | ')   
                f.write(series)
                f.write(' | ') 
                f.write(title.string)
                f.write(' | ')
                f.write(short.select('p strong')[0].string)
                f.write(' | ')                  
                f.write('alt title')                
                f.write(' | ')  
                f.write(long_desc)
                f.write(' | ')   
                f.write('film note author')
                f.write(' | ')  
                f.write('film note author title')
                f.write(' | ') 
                f.write('legacy credits')     
                f.write(' | ') 
                f.write(director) 
                f.write(' | ') 
                f.write(screenwriters) 
                f.write(' | ') 
                f.write(cinematographers) 
                f.write(' | ') 
                f.write(cast)
                f.write(' | ') 
                f.write(country)
                f.write(' | ') 
                f.write(year)
                f.write(' | ') 
                f.write('run time')                                                                                                                                                                                                                                                          
                f.write(' | ') 
                f.write(sources)   
                f.write(' | ') 
                f.write(permissions)
                f.write(' | ') 
                f.write(guests)    
                f.write(' | ') 
                f.write(location)                                                                                                                                                                  
                f.write('\n')   
        j = j + 1