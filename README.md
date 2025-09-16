# GR_GRP - Extraction et génération de données

## Table of contents :

- 📖 [About](#-about)  
- 📦 [Installation](#-installation)  
- [Project hierarchy](#project-hierarchy)  

## 📖 About  

This project automates the extraction of data for French GR and GRP hiking trails:  
1. Retrieve the list of all GR/GRP  
2. Download the HTML files  
3. Extract and process the data  
4. Generate a CSV and JSON file  

> The entire process is automated via a launch script (`launch.bat` on Windows or `launch.sh` on Linux/macOS).

---

## 📦 Installation  

### Prerequisites  

- [Python 3.11+](https://www.python.org/downloads/) installed on your machine  
- Ability to create a virtual environment (`venv`)  
- `git` (optional, if you want to clone the repository)  

### Steps  

1. **Clone the repository**:  

   ```bash
   git clone https://github.com/user/GR_GRP.git
   cd GR_GRP
   ```

2. **🚀 Run the appropriate launch script :** : 
   
   1. **Windows :**
        ```bash
        .\GR_GRP\Scripts\launch.bat
        ```

   2. **Linus/macOS :**
        ```bash
        ./GR_GRP/Scripts/launch.sh
        ```

## Project hierarchy
```texte
GR_GRP
|
|-- data/
|   |-- gr/                  # Folder containing the data for each GR
|   |   |-- gr1/             # Folder for each GR, with the extracted files
|   |   |   |-- gp1.gpx      # GPX file of the track
|   |   |   |-- gp1.html     # HTML page of the track
|   |   |   |-- gp1.jpg      # Image of the track (if available)
|   |   |   |-- gp1.json     # Data in JSON format
|   |   |   |-- gp1.png      # Image of the track (if available)
|   |   |   `-- ...
|   |   `-- ...
|   |-- all_gr_data.csv      # CSV file consolidating data from all GR
|   |-- all_gr_data.json     # JSON file consolidating data from all GR
|   |-- error_list.txt       # List of errors encountered during scraping
|   |-- gr_name.txt          # List of GR names
|   |-- url_error_list.txt   # List of URLs that caused an error
|   |-- url_gr_list.txt      # List of URLs of GR pages
|   `-- url_grp_list.txt     # List of URLs of GR group pages
|
|-- Scripts/
|   |-- launch.bat           # Launch script for Windows
|   `-- launch.sh            # Launch script for Linux/macOS
|
|-- getCSV.py                # Script to create the final CSV file
|-- getData.py               # Script for scraping data
|-- getFileHTML.py           # Script to download HTML files
|-- getGrList.py             # Script to retrieve the GR list
|-- README.md                # This file
`-- requirements.txt         # Project dependencies
```
