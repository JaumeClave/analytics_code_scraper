TEC-10586 Analytics Traffic Code Scraper
==============================

Python code which searches for Google Analytics, Chartbeat and Facebook Pixel JavaScript requests on a website. This will help the user determine if a website has any of these codes without manually checking themselves.

The main Python file for this project is called ```check_javascript.py``` found in the ```src``` folder.

### Running ```check_javascript.py``` From Your Terminal
You can run ```check_javascript.py``` from the terminal by providing the websites for which the scraper should check by using the ```--domains``` argument.
The format passed must be "www.XYZ.com" (without the quotations). For instance:

```python check_javascript.py --domains www.echobox.com``` 

A dictionary will be returned containing the URL of the scraped website and a boolean (True/False) value for its Google Analytics, Chartbeat and Facebook Pixel JavaScript request.

```{'URL': 'www.echobox.com', 'Google Analytics': True, 'Chartbeat': False, 'Facebook Pixel': True}```

From this result one could infer that the www.echobox.com website has a Google Analytics tracking code, a Facebook Pixel tracking code and no Chartbeat tracking code. 

From the terminal, it is also possible to provide several websites for the scraper to check. To do this, pass two or more websites after the ```--domains``` argument. For instance:

```python check_javascript.py --domains www.echobox.com www.wikipedia.com```

This will return one dictionary (as above) for each website.


### Using ```check_javascript.py``` as a Module in Your Python Scripts
The file may be imported as a module and used to return JavaScript requests of any website. 

```python
import check_javascript as cs 

echobox_js = cs.check_website_for_analytics_javascript('www.echobox.com')
print(echobox_js)

skysports_js = cs.check_website_for_analytics_javascript('www.skysports.com')
print(skysports_js)

wikipedia_js = cs.check_website_for_analytics_javascript('www.wikipedia.org')
print(wikipedia_js)
```


### Technologies
This project is created with 
- [Selenium](https://pypi.org/project/selenium/) a popular Python library used to automate web browser interaction. Version: 3.141.0
- [Webdrive-Manager](https://pypi.org/project/webdriver-manager/) which simplifies the management of binary drivers for different browsers. Version: 3.2.2


### Documentation
This section outlines the names of each Analytics Tracking code JavaScript request the code searches for and provides the 
implementation documentation for each one.  

#### Google Analytics 
An example of the script request is ```https://www.google-analytics.com/analytics.js```. The name of this script is 
```analytics.js```. Documentation can be found [here](https://developers.google.com/analytics/devguides/collection/analyticsjs) 

#### Charbeat 
An example of the script request is ```https://static.chartbeat.com/js/chartbeat.js```. The name of this script is 
```chartbeat.js```. Documentation can be found [here](https://docs.chartbeat.com/cbp/tracking/standard-websites/our-javascript) 

#### Facebook Pixel
An example of the script request is ```https://connect.facebook.net/en_US/fbevents.js```. The name of this script is 
```fbevents.js```. Documentation can be found [here](https://developers.facebook.com/docs/facebook-pixel/implementation/) 


### Manually Testing for Website JavaScript
At Echobox we may use this code to ensure that our clients do in fact have correctly installed analytics trackers. It also helps
identify clients which are lacking these qualities and from there on we may approach them explaining them 
why and how to add these analytic tracking codes.

Checking for these tracking codes manually is simple as well, however it is time consuming...

1. Open desired webpage on Google Chrome
2. Right click on the page > ```Inspect``` or ```Ctrl+Shift+I```
3. Find and click the ```Network``` tab
4. Reload the page ```Ctrl+R```
5. In the ```Filter``` search bar type the name of the desired JavaScript request 


### GDPR Compliance
As of May 25, 2018 the General Data Protection Regulation ([GDPR](https://gdpr.eu/what-is-gdpr
)) came into affect which aimed to improve consumer data protection and privacy in Europe. The
legislation states that "*Companies do have a right to process their users’ data as long as they
receive consent or if they have a legitimate interest.*". 

Google Analytics (and other Analytic Tracking codes) and its personal data processing cookies
cannot be classified as necessary cookies. They are third-party statistics cookies and therefore
need the prior consent from users in order to be activated and run on your website. 

By law a website must *wait* until you give consent (by accepting the cookie banner) before
loading Analytics Tracking code JavaScript. When running the ```check_javascript.py``` code it is
therefore recommended to have the user *accept* the cookie banner on the site as soon as it is
automatically opened.
  
However, all websites tested during the building of this code *did not* comply with GDPR law and
fired their Analytics Tracking code JavaScript before accepting the cookie banner. 

Therefore, it is recommended to run ```check_javascript.py``` on a domain, if the returned
Dictionary values are all ```False```, run ```check_javascript.py``` and this time accept the cookie
banner to be sure the JavaScript requests are correctly fired. If any of the Dictionary values are
```True``` on the first run of ```check_javascript.py``` then there is no need to re-run as this
website is not GDPR compliant. 

