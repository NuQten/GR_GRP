# -*- coding: utf-8 -*-
"""Script to get the list of all GR and GRP from the main page of gr-infos.com"""

import os
import re
import requests
from bs4 import BeautifulSoup


# * Define constant *
PATTERN_LINK = re.compile(r'<a[^>]+href=["\'](.*?)["\']')
URL_DOMAINE = 'https://www.gr-infos.com/'
URL = 'https://www.gr-infos.com/gr-fr.htm'
URL_BAN_SET = {'https://www.gr-infos.com/gr-en.htm',
               'https://www.gr-infos.com/gr-nl.htm',
               'https://www.gr-infos.com/gr-de.htm',
               'https://www.gr-infos.com/gr-ru.htm',
               'https://www.gr-infos.com/gr-cn.htm'
}
ABSPATH_FILE = os.path.abspath(__file__)
ABSPATH_PROJECT = os.path.dirname(ABSPATH_FILE)


def parcours_link(url, set_url: set, set_url_ban: set) -> set : 
    """Parcours recursively all link in the page and return a set of link of all GR and GRP

    Args:
        url (str): url of the page to parse
        set_url (list): set of url already parsed
        set_url_ban (set): set of url to ignore

    Returns:
        set: set of link of all GR and GRP
    """

    # * Get all link in the page *
    try : 

        # * Get soup of the page *
        response = requests.get(url)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, "html.parser")

        # * Find all link in the page *
        links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].lower().endswith(('.html', '.htm'))]

        # * Create list of href *
        href_list = []
        
        # * Add link to the list of href according to the different case *
        for link in links:
            
            if re.match(r'^https://www.gr-infos.com/gr[^.]', link):  
                if link not in set_url : 
                    href_list.append(link)
            elif not re.match(r'^https', link)  and not re.match(r'^\.\.|^en', link):    
                    href_list.append(URL_DOMAINE + link)
            else :
                pass
                    
        # * For each link in the list of href, if the link is not in the set of url and not in the set of ban, add it to the set of url and call the function recursively *
        for href in href_list:
            if href in set_url or href in set_url_ban :
                continue
            else : 
                set_url.add(href)
                set_url.union(parcours_link(href, set_url, set_url_ban))

        return set_url
    
    
    except Exception as erreur:
        print(f'erreur : {erreur}')

    return set()


def getGrList() -> bool:
    """Get the list of all GR and GRP from the main page of gr-infos.com and write it in gr_list.txt and grp_list.txt
    
    Returns:
        bool: True if the function is successful, else return False and the error
    """

    # * Define constant *
    PATTERN_NB = re.compile(r'[0-9]{1,4}')
    PATTERN_GRP = re.compile(r'https://www.gr-infos.com/grp.*')
    PATTERN_GR = re.compile(r'https://www.gr-infos.com/gr[^r].*')
    PATTERN_GRR = re.compile(r'.*grr.*')
    
    # * Create set of link *
    set_link = parcours_link(URL, set(), URL_BAN_SET)


    # * Create different list for all grs, gr, grp, grr, and errors * 
    list_link = list(set_link)
    list_sort = list()
    list_gr = list()
    list_grp = list()
    list_grr = list()
    list_error = list()

    # * Classify link in different list *
    for link in list_link : 
        try : 
            if PATTERN_GRP.match(link):
                list_grp.append(link)
            elif PATTERN_GRR.match(link):
                list_grr.append(link)
            elif PATTERN_GR.match(link): 
                nb = int(PATTERN_NB.findall(link)[0]) 
                list_gr.append(link)
                list_sort.append(nb)
            else :
                raise Exception('link not conform') 

        except Exception as error :
            list_error.append(link)
            print(error, link)

    # * Sort list gr according to number of the gr *
    list_sort = [x for _, x in sorted(zip(list_sort, list_gr))]

    # * Create string for lists *	
    str_list_link_gr = ''
    str_list_link_grp = ''
    str_list_link_error = ''

    # * Wrtie string for files *
    for link in list_sort:
        str_list_link_gr += link + '\n'

    for link in sorted(list_grr):
        str_list_link_gr += link + '\n'

    for link in list_grp:
        str_list_link_grp += link + '\n'

    for link in list_error:
        str_list_link_error += link + '\n'


    # * Write files *
    try : 
        with open(os.path.join(ABSPATH_PROJECT, 'data', 'url_gr_list.txt'), 'w') as file :
            file.write(str_list_link_gr)

        with open(os.path.join(ABSPATH_PROJECT, 'data', 'url_grp_list.txt'), 'w') as file :
            file.write(str_list_link_grp)

        with open(os.path.join(ABSPATH_PROJECT, 'data', 'url_error_list.txt'), 'w') as file :
            file.write(str_list_link_error)

    except Exception as error :
        return False, error
    else : 
        return True
    

    
if __name__ == "__main__":
    None
