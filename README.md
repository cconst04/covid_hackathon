# SNITCH
SNITCH(SMS Novel Insights Towards Coronavirus Halt) is a web platform for data visualization of the SMS service 8998 being in operation in Republic of Cyprus to restrict people's movement during the coronavirus outbreak.
The user can upload various files containing SMS data, postal codes along with coordinates, demographics, and data about fines issued by Police officers. 
This system is intended to be used by the cypriot government.

##Demo Video
https://www.youtube.com/watch?v=noDIflSOxoI&t=80s

## Tech stack:
SNITCH utilizes Python3, Django Framework, PostgreSQL, Javascript chart libraries (amCharts and Highcharts), and Google Maps. The solution is built and run as Docker containers.

## Installation
```
sudo apt-get install docker docker-compose  
docker-compose up --build
```
Now, on your browser navigate to localhost:8000

## Data generation
Since we don't have access to all these data, we've written some scripts to generate random data.
If you want to upload random data, follow these steps:
1. In file covid/settings.py set DEMO=False


2. Navigate in folder Event_generator
3. Generate random people data:
```
python3 people.py
```
A file named people.csv will be generated.
Upload the file on the web platform.  
4. Generate random fines:
```
python3 fines_generator.py
```
A file named fines.csv will be generated.
Upload the file on the web platform.  
5. Postal codes:
geocoding_script.py generates a csv file which contains the mapping between each postal code and coordinates.
We've generated this file for you using google geocoding API and data from https://www.data.gov.cy/node/1577?language=en 
you can find them for each city under the name Paphos_out.csv,Larnaca_out.csv,Limassol_out.csv,Nicosia_out.csv
Upload the file on the web platform.  
6. SMS data:
```
python3 data.py <geocoding_mapping.csv>
```
This will generate random SMS data . <geocoding_mapping.csv> is the file generated from geocoding_script.py , e.g Paphos_out.csv
Upload the file on the web platform

Covid hackathon implementation
