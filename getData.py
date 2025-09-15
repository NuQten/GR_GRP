# -*- coding: utf-8 -*-
"""Script to get all data from the html file of all GR and GRP in gr_list.txt and grp_list.txt
and save it in all_gr_data.json and all_grp_data.json"""

import os
import re
import requests
import html
from bs4 import BeautifulSoup
import json


# * CONSTANT * 
ABSPATH_FILE = os.path.abspath(__file__)
ABSPATH_PROJECT = os.path.dirname(ABSPATH_FILE)
PATTERN_URL = re.compile(r'https?://(?:www\.)?[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(?:/[^\s]*)?')
PATTERN_PATH = re.compile(r'/(.*)$')
PATTERN_GR_NAME = re.compile(r'(gr[0-9]{1,4}_?[A-Z]?[A-Z]?[A-Z]?|grr[0-9]|grp-[a-zA-Z-]+[0-9]?)')
PATTERN_GR_INFO_DISTANCE = re.compile(r'Distance:\s*(\d+,?\d?\d?)\s*km', re.IGNORECASE)
PATTERN_GR_INFO_ALTITUDE_MAX = re.compile(r'Altitude maximum:\s*(\d+)\s*m', re.IGNORECASE)
PATTERN_GR_INFO_ALTITUDE_MIN = re.compile(r'Altitude minimum:\s*(\d+)\s*m', re.IGNORECASE)
PATTERN_GR_INFO_DENIVELE = re.compile(r'D[ée]nivel[ée] cumul[ée] mont[ée]e:\s*(\d+)\s*m', re.IGNORECASE)
PATTERN_MULT_NEWLINE = re.compile(r'(?:\n\s*){2,}')
URL_DOMAINE = 'https://www.gr-infos.com'
PATH_ELEVATION = '/divers/elevation/'
PATH_IGN = '/divers/ign/'
PATH_GPX = '/divers/gpx/'
PNG = '.png'
JPG = '.jpg'
GPX = '.gpx'
HTML = '.html'


# * Define function *

def get_soup(name:str) -> BeautifulSoup | Exception:
    """Returns a BeautifulSoup object from the gr's name

    Args:
        name (str): name of the GR (in the gr_list.txt)

    Raises:
        ValueError: if the url is not conform

    Returns:
        BeautifulSoup: object of the page    
    """
    try : 
        with open(os.path.join(ABSPATH_PROJECT, 'data', 'gr', name, name + HTML), 'r', encoding='utf-8') as file :
            html_content = file.read()
            text_html = html.unescape(html_content) #Replace all html entity (&eacute) by unicode caract (é)
            soup = BeautifulSoup(text_html, 'html.parser')        
            return soup
    except Exception as error :
        print(error)
        return error

def get_elevation(gr_name:str) -> requests.Response | Exception:
    """Get elevation file from gr_name

    Args:
        gr_name (str): name of the GR (in the gr_list.txt)

    Returns:
        requests.Response|None: png of the elevation if the file is found else None
    """

    try : 
        response = requests.get(URL_DOMAINE + PATH_ELEVATION + gr_name + '-min' + PNG)
    except Exception as error :  
        print(f'file unfound : {error}')
        return error

    return response

def save_elevation(path:str, content) -> bool | Exception:
    try :
        with open(path, 'wb') as file :
            file.write(content)
        return True
    except Exception as error :
        print(f'Save unsuccessful : {error}')
        return error

def get_gpx(gr_name:str) -> requests.Response | Exception:
    try : 
        response = requests.get(URL_DOMAINE + PATH_GPX + gr_name + GPX)
    except Exception as error :  
        print(f'file unfound : {error}')
        return error

    return response

def save_gpx(path:str, content) -> bool | Exception:
    try :
        with open(path, 'wb') as file :
            file.write(content)
        return True
    except Exception as error :
        print(f'Save unsuccessful : {error}')
        return error

def get_ign(gr_name:str) -> requests.Response | Exception:
    try : 
        response = requests.get(URL_DOMAINE + PATH_IGN + gr_name + '-min' + JPG)
    except Exception as error :  
        print(f'file unfound : {error}')
        return error

    return response

def save_ign(path:str, content) -> bool | Exception:
    try :
        with open(path, 'wb') as file :
            file.write(content)
        return True
    except Exception as error :
        print(f'Save unsuccessful : {error}')
        return error

def get_name(url) -> str | Exception:
    try : 
        search = re.search(PATTERN_GR_NAME, url)
        if search is None :
            raise Exception(f'No name found in url : {url}')
        else : 
            name = search.group(1)
            name = name[0:3].upper() + name[3:] 
    except Exception as error :
        print(f'No name found : {error}')
        return error
    
    return name 
     
def get_distance(soup: BeautifulSoup) -> int | float | Exception:
    """Get distance of the GR
    Args:
        soup (BeautifulSoup): soup of the page
    
    Raises:
        Exception: if no distance found

    Returns:
        int | float | Exception: int or float of the distance if found else the error
    """
    
    try :
        search = re.search(PATTERN_GR_INFO_DISTANCE, soup.text)
        if search is None :
            raise Exception('No distance found')    
        else :
            distance = search.group(1)

        if ',' in distance:
            return float(distance.replace(',', '.'))
        elif '.' in distance:
            return float(distance)
        else:  
            return int(distance)
    except Exception as error :
        print(f'distance no found : {error}')
        return error

def get_denivele(soup: BeautifulSoup) -> int | Exception:
    """Get denivele of the GR
    Args:
        soup (BeautifulSoup): soup of the page
    
    Raises:
        Exception: if no denivele found
    
    Returns:
        int | Exception: int of the denivele if found else the error
    """

    try :
        search = re.search(PATTERN_GR_INFO_DENIVELE, soup.text)
        if search is None :
            raise Exception('No denivele found')    
        else :
            denivele = search.group(1)
            return int(denivele)
    except Exception as error :
        print(f'denivele no found : {error}')
        return error 

def get_alt_max(soup: BeautifulSoup) -> int | Exception:
    """Get altitude max of the GR
    Args:
        soup (BeautifulSoup): soup of the page
    
    Raises:
        Exception: if no altitude max found
    
    Returns:
        int | Exception: int of the altitude max if found else the error
    """

    try :
        search = re.search(PATTERN_GR_INFO_ALTITUDE_MAX, soup.text)
        if search is None :
            raise Exception('No altitude max found')    
        else :
            alt_max = search.group(1)
            return int(alt_max)
    except Exception as error :
        print(f'altitude max no found : {error}')
        return error  

def get_alt_min(soup: BeautifulSoup) -> int | Exception:
    """Get altitude min of the GR
    Args:
        soup (BeautifulSoup): soup of the page
        
    Raises:
        Exception: if no altitude min found
        
    Returns:
        int | Exception: int of the altitude min if found else the error
    """
    
    try :
        search = re.search(PATTERN_GR_INFO_ALTITUDE_MIN, soup.text)
        if search is None :
            raise Exception('No altitude min found')    
        else :
            alt_min = search.group(1)
            return int(alt_min)
    except Exception as error :
        print(f'altitude min no found : {error}')
        return error 

def get_title(soup: BeautifulSoup) -> str | Exception:
    """Get title of the GR

    Args:
        soup (BeautifulSoup): soup of the page

    Raises:
        Exception: if no title found

    Returns:
        list | Exception: str of the title if found else the error
    """
    try :
        search = soup.find('h1')
        if search is None :
            raise Exception('No title found')
        else : 
            title = search.text
            return title
            
    except Exception as error :
        print(f'titles no found : {error}')
        return error

def is_url(url: str) -> bool:
    """Know if it's an url

    Args:
        url (str): str of the url

    Returns:
        bool: TRUE if is an url FALSE elif
    """
    if re.match(PATTERN_URL, url):
        return True
    else :
        return False
    
def get_data(name: str) -> tuple[dict, list[str]]:
    """Get data from an url

    Args:
        url (str): url of the page

    Returns:
        dict: dict with the data
    """

    soup = get_soup(name)
    list_error = []
    

    # * If the soup is correct, get the information *
    if not isinstance(soup, Exception) :
        
        name_data = name[0:3].upper() + name[3:] 

        distance = get_distance(soup) # distance of the GR
        if isinstance(distance, Exception) :
            list_error.append(name + ' : distance unfound')
            distance = None

        denivele = get_denivele(soup) # denivele of the GR
        if isinstance(denivele, Exception) :
            list_error.append(name + ' : denivele unfound')
            denivele = None

        alt_max = get_alt_max(soup) # altitude max of the GR
        if isinstance(alt_max, Exception) :
            list_error.append(name + ' : alt_max unfound')   
            alt_max = None

        alt_min = get_alt_min(soup) # altitude min of the GR
        if isinstance(alt_min, Exception) :    
            list_error.append(name + ' : alt_min unfound')
            alt_min = None

        title = get_title(soup) # titles of the GR
        if isinstance(title, Exception) :
            list_error.append(name + ' : titles unfound')
            title = None
        
        elevation = get_elevation(name.lower()) # get elevation file
        if isinstance(elevation, Exception) :
            list_error.append(name + ' : elevation file unfound')
        else : 
            result = save_elevation(os.path.join(ABSPATH_PROJECT, 'data', 'gr', name, name + PNG), elevation.content)
            if not result :
                list_error.append(name + ' : elevation save error')

        gpx = get_gpx(name.lower()) # get gpx file
        if isinstance(gpx, Exception) :
            list_error.append(name + ' : gpx file unfound')
        else :   
            result = save_gpx(os.path.join(ABSPATH_PROJECT, 'data', 'gr', name, name + GPX), gpx.content)
            if not result :
                list_error.append(name + ' : gpx save error')

        ign = get_ign(name.lower()) # get ign file
        if isinstance(ign, Exception) :
            list_error.append(name + ' : ign file unfound')
        else :    
            result = save_ign(os.path.join(ABSPATH_PROJECT, 'data', 'gr', name, name + JPG), ign.content)
            if not result :
                list_error.append(name + ' : ign save error')

        # * Save information in json file *
        dict_info = {
            'name': name_data,
            'distance': distance,
            'denivele': denivele,
            'altitude_max': alt_max,
            'altitude_min': alt_min,
            'title': title
        }

        try  :
            with open(os.path.join(ABSPATH_PROJECT, 'data', 'gr', name, name + '.json'), 'w', encoding='utf-8') as file :
                json.dump(dict_info, file, ensure_ascii=False, indent=4, default=str)
        except Exception as error : 
            print(f'json save error : {error}')
            list_error.append(name + ' : json save error')

        return (dict_info, list_error)

    else : 
        list_error.append('Soup error for url : ' + url)
        return ({}, list_error)


if __name__ == "__main__":
    

    # * Read list of name *
    with open(os.path.join(ABSPATH_PROJECT, 'data', 'gr_name.txt'), 'r') as file :
        list_all_gr = file.readlines()

    list_error = []
    dict_all_gr = {}

    # * Browse the list of link *
    for url in list_all_gr :
        dict, errors = get_data(url[:-1])
        for error in errors :
            list_error.append(error)
        if dict != {} :
            dict_all_gr[dict['name']] = dict
        print(f'End of {url}')
        
    # * Write data file *
    try :
        with open(os.path.join(ABSPATH_PROJECT, 'data', 'all_gr_data.json'), 'w', encoding='utf-8') as file :
            json.dump(dict_all_gr, file, ensure_ascii=False, indent=4, default=str)
    except Exception as error :
        print(f'Error write data file : {error}')
        
    # * Write error file *
    str_list_error = ''

    for error in list_error:
        str_list_error += error + '\n'

    try :
        with open(os.path.join(ABSPATH_PROJECT, 'data', 'error_list.txt'), 'w') as file :
            file.write(str_list_error)
    except Exception as error :
        print(f'Error write error file : {error}')

        
        