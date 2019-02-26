from bs4 import BeautifulSoup
import requests
import json

url = 'https://www.sourcewell-mn.gov/cooperative-purchasing/022217-wex'
response = requests.get(url, timeout=5)
content = BeautifulSoup(response.content, 'html.parser')

article = content.find('article', 'vendor-contract')
contractHeader = article.find('div', 'vendor-contract-header__content')
contractBody = article.find('div', 'vendor-contract-body')
vendorContact = contractBody.find('article', 'contract-marketing')
vendors = vendorContact.findAll('div', 'inline-user')
contractDocuments = contractBody.find('div', {'id': 'tab-contract-documents'})
documents = contractDocuments.findAll('div', 'field--item')

contacts = []
for vendor in vendors:
	contacts.append({
        'name': vendor.findAll('div')[0].text,
        'phone': vendor.findAll('div', 'field--item')[0].text,
        'email': vendor.findAll('div', 'field--item')[1].text
    });

files = []
for document in documents: 
    if (document.find('a').text.strip() == 'Contract Forms'):
        files.append({
            'contract-forms': document.find('a').attrs['href']
        })

contractNumber, dateRange = contractHeader.findAll('p')[1].stripped_strings

contract = {
    'title': contractHeader.find('p', 'lead').text,
    'expiration': dateRange.split()[2],
    'contract_number': contractNumber,
    'files': files,
    'vendor': {
        'name': contractHeader.find('h1', 'h2').text,
        'contacts': contacts
    }
}
with open('contractData.json', 'w') as outfile:
    json.dump(contract, outfile)