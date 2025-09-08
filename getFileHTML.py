# -*- coding: utf-8 -*-
"""Script to get the html file of all GR and GRP from the list in gr_list.txt and grp_list.txt"""

import requests
import re
import os


# * Define constant *
ABSPATH_FILE = os.path.abspath(__file__)
ABSPATH_PROJECT = os.path.dirname(ABSPATH_FILE)


def getFileHTML() -> bool:
    """Get the html file of all GR and GRP from the list in gr_list.txt and grp_list.txt
    and save it in a folder named after the GR/GRP name
    Returns:
        bool: True if the function is successful, else False and the error
    """

    # * Define constant *
    PATTERN_NAME = re.compile(r'(gr[0-9]{1,4}_?[A-Z]?|grr[0-9]|grp-[a-zA-Z-]+)')

    # * Create list of link *
    try : 
        with open(os.path.join(ABSPATH_PROJECT, 'data', 'url_gr_list.txt'), 'r') as file : 
            url_list = file.readlines()

        with open(os.path.join(ABSPATH_PROJECT, 'data', 'url_grp_list.txt'), 'r') as file : 
            url_list.extend(file.readlines())
    except Exception as e:
        return False, e


    # * For each link in the list, get the html file and save it in a folder named after the GR/GRP name *
    nb_error = 0
    for url in url_list : 
        try :
            name = re.search(PATTERN_NAME, url).group(1)
            response = requests.get(url[:-1])
            response.encoding = 'utf-8'
            html_text = response.text


            os.makedirs(os.path.join(ABSPATH_PROJECT, 'data', 'gr', name), exist_ok=True)
            with open(os.path.join(ABSPATH_PROJECT, 'data', 'gr', name, name+'.html'), 'w', encoding='utf-8', newline='\n') as file :
                file.write(html_text)

        except Exception as e: 
            nb_error += 1
            print(e)
        finally :
            if nb_error == 0 : 
                return True
            else : 
                return False, nb_error

if __name__ == "__main__":

    result = getFileHTML()
    if result is True :
        print('All files downloaded successfully')
    else : 
        if result is int : 
            print(f'Error(s) occurred: {result[1]} file(s) not downloaded')
        else :
            print(f'Error occurred: {result[1]}')