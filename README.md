# SLAIU_Repo

The official repository for the Ski Lessons Aggregation and Insight Utility:

This is just a collection of source files, the actual project is hosted in a top secret undisclosed Raspberry Pi :)

Current Features:
- Fully interactive Web application
- Flask backend server for handling requests
- Automated web scraping and database management scripts
  
Website can be accessed through this link:

  https://slaiu.pythonanywhere.com/

  -> Username: Boofy
  -> Password: Boof

The flow of scripts (row row row your boat):

1) searchengine.py - gets links to ski lesson provider websites
2) checkinglinks.py - checks robots.txt files for website owner permissions
3) getlessonlinks1.py - gets lessons links from provider websites
4) getlessonlinks2.py - refines the links even further and removes duplicates
5) SLAIU_nogui.py - gets lesson details and uploads to database
6) providerinfo.py - gets provider info and uploads to database
7) Website/SLAIU_website.py - runs the backend server of the end user web interface
