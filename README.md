# BAMPFA Soup

This is a scraper meant to grab all of the film screening data on bampfa.org that is required by the film archive.

The idea is that scraping it from the frontend, where all of the logic for grouping the data from across the big insane database is already in place, will be a lot faster to develop and run, rather than recreating the complex drupal field logic, deal with php timeouts etc.

To run
- install dependencies (python, beautifulsoup, tqdm)
- run `python3 soup.py`
- output is put into output.csv