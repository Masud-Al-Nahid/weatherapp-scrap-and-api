from django.shortcuts import render
import requests
from bs4 import BeautifulSoup as bs
import json


def get_weather_data(city):
    city = city.replace(' ', '+')
    url =f'https://www.google.com/search?q=weather+of+{city}'
    headers = {
        
        'user-agent' : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
            'cookie' : "SID=TAhSPSXM7p403eFFn3SGjzD4XArZq_tp6oJFfb9DZpMkthQMmTs7jmMAMBtf1OxdnHHlzw.; __Secure-1PSID=TAhSPSXM7p403eFFn3SGjzD4XArZq_tp6oJFfb9DZpMkthQMfz-x0ypM9uSAIqgUkIbkfQ.; __Secure-3PSID=TAhSPSXM7p403eFFn3SGjzD4XArZq_tp6oJFfb9DZpMkthQMGwY3Yxdosjd3Wy7VR1X8Hw.; HSID=A5s89lzvmhKCui7_l; SSID=A6eCLmjMhygKroGc9; APISID=7l8ynhCvwuoq7TJ6/AyBsvDdpCjVLVViMm; SAPISID=7GihbF17SoILFUc-/AhcA47vK06O2SIzVm; __Secure-1PAPISID=7GihbF17SoILFUc-/AhcA47vK06O2SIzVm; __Secure-3PAPISID=7GihbF17SoILFUc-/AhcA47vK06O2SIzVm; OTZ=6893358_32_32__32_; SEARCH_SAMESITE=CgQIzZcB; AEC=ARSKqsL1gMVPiKQnqt8rxDjt-lWKy4db8cmp5_6w4iDK2B7KaII5BcDIvA; 1P_JAR=2023-02-17-04; NID=511=hUwSoVVvZ_c7ywxBExK3g1AZgnFSTorzH5mQJiQuoTs_A9aA9I4S0NYbQqNXZK4hUCGvHk0O4SeAiGnxc6o8SgzkEQ_6gV1y7k_9NerOPLzOXKOKOTO68MQMU7K0BFdV69P3RQwZtYfhJx3B6sfqRn7yG_tr22Caae0IOs3Qs-NZD3BdzEcjZmJEHOImcvy8ZTJEFxjeNHTWf3QTYLOH2hOA9cCCajbGX00CA4utQ_iEY5y4FLszRA7dnuaAP00AgYnrsyL2Q2rCsWsQMvhCrTueIw2whDFi3ocmbYkU_Jluo80L-BKvKrYZrXkJoIg7yeFazYOROiNHcHjFGGU-50xveKvkmG9Q_ngvNzTATvKYukUuMK-GeYp1-DgF92iazgE70qKES5axhS6Ca2g2aSYJ0iXWjblDvvdab76qNF7rDDXUU0uXJW67u6haiG8aMQFxHlkEZUvymUa7wfxIlrkm0vbY-XnAf9Fw4FPba2fsTxoKZvoh0MWl3CN1vJ-wBLSCvTPMNeTNVUQfEUMXc7uhxu1w7TbYPAJfJT9D9tr-2aDDHC3G2htaTtZV2Gc5AYQ74SwnQ8D48KNNBOYD31jspGeACBlZtotwP-RR5lrj0Dy6NFiFH9NEjKWLSrCp5A0WcXURLGP8Skn06VYFQnLZv1miPtM; DV=MzPn7iExqx5WwEtSPKiaEkrKx3nZZZhvU3dyzytnNAIAAIBHfY3ypUEutAAAAFQ5Rwsg6qLjMgAAAKaqsXzyEc3TFAAAAA; SIDCC=AFvIBn91vEWOKjC6ob-dRuX425bI41hfGy6rm9cIPBq9O8-wK-LD_WVyL-qHw6HtqC2W_6mPKGE; __Secure-1PSIDCC=AFvIBn_VRBEM5E8XlTFac0Wc0TV0sWy65ALl_HKnjEj03Pw4UIZJq5dV1iZzmKYSx7UJFv604ERJ; __Secure-3PSIDCC=AFvIBn-yvgRM0HlXreVMEeoHrfdgZ1b9MmiqEVLEQ-EL-oAJgnQUcpBEHHNQjV7js9du1Ahr4Tc"
    }
    
    res = requests.get(url, headers=headers)
    soup = bs(res.text, "html.parser")
    
    results ={}
    results["region"] = soup.find('div', {'class': 'wob_loc q8U8x' }).text
    results["daytime"] = soup.find('div', {'class': 'wob_dts' }).text
    results["weather"] = soup.find('div', {'class': 'wob_dcp' }).text
    results["teamparature"] = soup.find('span', {'class': 'wob_t q8U8x' }).text
    
    #print(result)
    return results

# Create your views here.

def home_view(request):
    if request.method == "GET" and "city" in request.GET:
        city = request.GET.get("city")
        results = get_weather_data(city)
        context = {"results":results}
    else:
        context = {}
    return render(request, 'home.html', context)

def weather_api(city):
    api_key = 'b548c4f65bd7d27a750421dfb3dd12aa'
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&type=hour&units=metric'
    response = requests.get(url)
    data = json.loads(response.text)
    results = {}
    results['City_Name'] = data['name']
    results['Country'] = data['sys']['country']
    results['Weather'] = data['weather'][0]['description']
    results['Tem'] = data['main']['temp']
    results['Humidity'] = data['main']['humidity']
    results['Sunrise'] = data['sys']['sunrise']
    results['Sunset'] = data['sys']['sunset']
    return results

def api_view(request):
    if request.method =="POST" and "city" in request.POST:
        city = request.POST.get('city')
        results = weather_api(city)
        context = {'results':results}
    else:
        context = {}
    
    return render(request, 'api.html', context)