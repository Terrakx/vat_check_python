from zeep import Client

# Create a SOAP client with the WSDL URL
client = Client('http://ec.europa.eu/taxation_customs/vies/checkVatService.wsdl')

# Define the parameters for the checkVat operation
country_code = 'AT'
vat_number = ''

# Call the checkVat operation
result = client.service.checkVat(countryCode=country_code, vatNumber=vat_number)

# Print the result
print(result)
