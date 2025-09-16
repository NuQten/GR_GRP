# -*- coding: utf-8 -*-
"""Script to get the html file of all GR and GRP from the list in gr_list.txt and grp_list.txt"""

import requests
import re
import os
from typing import Tuple


# * Define constant *
ABSPATH_FILE = os.path.abspath(__file__)
ABSPATH_PROJECT = os.path.dirname(ABSPATH_FILE)


def getFileHTML() -> Tuple[bool, Exception] | Tuple[bool, int] | bool :
    """Get the html file of all GR and GRP from the list in gr_list.txt and grp_list.txt
    and save it in a folder named after the GR/GRP name

    Returns:
        bool: True if the function is successful
        Tuple[bool, int] : False, number of error(s)
        Tuple[bool, Exception] : False, name of error (can't create list of link)
    """

    # * Define constant *
    PATTERN_NAME = re.compile(r'(gr[0-9]{1,4}_?[A-Z]?[A-Z]?[A-Z]?|grr[0-9]|grp-[a-zA-Z-]+[0-9]?)')

    # * Create list of link *
    try : 
        with open(os.path.join(ABSPATH_PROJECT, 'data', 'url_gr_list.txt'), 'r') as file : 
            url_list = file.readlines()

        with open(os.path.join(ABSPATH_PROJECT, 'data', 'url_grp_list.txt'), 'r') as file : 
            url_list.extend(file.readlines())
    except Exception as error:
        return (False, error)


    # * For each link in the list, get the html file and save it in a folder named after the GR/GRP name *
    list_name = []
    nb_error = 0
    for url in url_list : 
        try :
            search = re.search(PATTERN_NAME, url)
            if search is None :
                name = 'unfound'
            else : 
                name = search.group(1)
                list_name.append(name)

            response = requests.get(url[:-1])
            response.encoding = 'utf-8'
            html_text = response.text


            os.makedirs(os.path.join(ABSPATH_PROJECT, 'data', 'gr', name), exist_ok=True)
            with open(os.path.join(ABSPATH_PROJECT, 'data', 'gr', name, name+'.html'), 'w', encoding='utf-8', newline='\n') as file :
                file.write(html_text)

        except Exception as error: 
            nb_error += 1
            print(error)

        str_gr_name = ''
        for link in list_name:
            str_gr_name += link + '\n'

        with open(os.path.join(ABSPATH_PROJECT, 'data', 'gr_name.txt'), 'w') as file :
            file.write(str_gr_name)
    
    else : 
        if nb_error == 0 : 
            return True
        else : 
            return (False, nb_error)

if __name__ == "__main__":

    result = getFileHTML()
    if result is True :
        print('All files downloaded successfully')
    else : 
        if result is tuple[bool, int] : 
            print(f'Error(s) occurred: {result[1]} file(s) not downloaded')
        else :
            print('Url list file not found')