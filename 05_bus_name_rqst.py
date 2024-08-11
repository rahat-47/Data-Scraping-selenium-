import requests
import re

# Send a GET request to the URL
r = requests.get('https://www.shohoz.com/booking/bus/search?fromcity=Dhaka&tocity=Barisal&doj=27-Apr-2024&dor=30-Apr-2024')

# Check if the request was successful (status code 200)
if r.status_code == 200:
    # Use regex to extract bus names from the HTML response
    bus_names = re.findall(r'<li class="op_name shohoz_green">(.*?)</li>', r.text, re.DOTALL)
    
    if bus_names:
        with open('busname.csv', 'w') as f:
            for name in bus_names:
                f.write(name.strip() + '\n')
        print("Bus names scraped successfully!")
    else:
        print("No bus names found on the page.")
else:
    print('Failed to retrieve the webpage. Status code:', r.status_code)

