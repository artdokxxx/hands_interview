# PHONES_SCRAPER - the task for testing

## Description

Parser numbers in the format of the Russian Federation, on sites.  
The database contains site and uri for page with contacts.  
**The format of the output numbers** - `8KKKNNNNNNN`.  
If the site for the number is not specified area code, the city of Moscow.  
 
## Requirements

Python - `3.6.4`  
Python packages - `See requirements.txt`  

## How use

You need install all requirements, use for this:
```bash
pip install -r requirements.txt
```

If you want just run in cli for test:  

```bash
python main.py
```

If you want using this as module just `see main.py`

## Structure

`config.py` - File for configuration (Timeout, regexp_rules, etc)  
`sites.py` - File with sites list  
`common/scraper.py` - Main code for get page and parse phones  
`common/state.py` - State manager for save every step and result to file.  

## API 

Just one point - `run()`.

