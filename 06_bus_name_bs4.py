from bs4 import BeautifulSoup
import requests

# Send a GET request to the URL
r = requests.get('https://www.shohoz.com/booking/bus/search?fromcity=Dhaka&tocity=Barisal&doj=27-Apr-2024&dor=30-Apr-2024')

# Check if the request was successful (status code 200)
if r.status_code == 200:
    html = r.text
    soup = BeautifulSoup(html, 'html.parser')
    
    with open('busname.csv', 'w') as f:
        # Find all elements containing bus names and having data-title attribute 'Operator'
        bus_name_tags = soup.find_all('li', {'class': 'op_name shohoz_green', 'data-title': 'Operator'})
        
        # Check if bus names were found
        if bus_name_tags:
            for tag in bus_name_tags:
                f.write(tag.text.strip() + '\n')
            print("Bus names scraped successfully!")
        else:
            print("No bus names found on the page.")
else:
    print('Failed to retrieve the webpage. Status code:', r.status_code)
