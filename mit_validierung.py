import re
from zeep import Client

def validate_vat_id(uid):
    patterns = {
        "AT": r"^ATU\d{8}$",  # Austria: 'ATU' followed by 8 digits
        "BE": r"^BE\d{10}$|^BE0\d{9}$",  # Belgium: 'BE' followed by 10 digits or 9 digits prefixed with '0'
        "BG": r"^BG\d{9}$|^BG\d{10}$",  # Bulgaria: 'BG' followed by 9 or 10 digits
        "HR": r"^HR\d{11}$",  # Croatia: 'HR' followed by 11 digits
        "CY": r"^CY\d{8}[A-Z]$",  # Cyprus: 'CY' followed by 8 digits and a letter
        "CZ": r"^CZ\d{8,10}$",  # Czech Republic: 'CZ' followed by 8, 9, or 10 digits
        "DK": r"^DK\d{8}$",  # Denmark: 'DK' followed by 8 digits
        "EE": r"^EE\d{9}$",  # Estonia: 'EE' followed by 9 digits
        "FI": r"^FI\d{8}$",  # Finland: 'FI' followed by 8 digits
        "FR": r"^FR\d{11}$|^FR[A-HJ-NP-Z]\d{10}$|^FR\d[A-HJ-NP-Z]\d{9}$|^FR[A-HJ-NP-Z]{2}\d{9}$",  
        # France: 'FR' followed by 
        # 11 digits or
        # 1 letter (not O or I) followed by 10 digits or
        # 1 digit followed by 1 letter (not O or I) and 9 digits or
        # 2 letters (not O or I) followed by 9 digits
        "DE": r"^DE\d{9}$",  # Germany: 'DE' followed by 9 digits
        "EL": r"^EL\d{9}$",  # Greece: 'EL' followed by 9 digits
        "HU": r"^HU\d{8}$",  # Hungary: 'HU' followed by 8 digits
        "IE": r"^IE\d{7}[A-W]{1,2}$",  # Ireland: 'IE' followed by 7 digits and 1 or 2 letters (A-W)
        "IT": r"^IT\d{11}$",  # Italy: 'IT' followed by 11 digits
        "LV": r"^LV\d{11}$",  # Latvia: 'LV' followed by 11 digits
        "LT": r"^LT\d{9}$|^LT\d{12}$",  # Lithuania: 'LT' followed by 9 or 12 digits
        "LU": r"^LU\d{8}$",  # Luxembourg: 'LU' followed by 8 digits
        "MT": r"^MT\d{8}$",  # Malta: 'MT' followed by 8 digits
        "NL": r"^NL\d{9}B0[12]$",  # Netherlands: 'NL' followed by 9 digits and 'B01' or 'B02'
        "NO": r"^NO\d{9}MVA$",  # Norway: 'NO' followed by 9 digits and 'MVA'
        "PL": r"^PL\d{10}$",  # Poland: 'PL' followed by 10 digits
        "PT": r"^PT\d{9}$",  # Portugal: 'PT' followed by 9 digits
        "RO": r"^RO\d{10}$",  # Romania: 'RO' followed by 10 digits
        "SK": r"^SK\d{10}$",  # Slovakia: 'SK' followed by 10 digits
        "SI": r"^SI\d{8}$",  # Slovenia: 'SI' followed by 8 digits
        "ES": r"^ES[A-Z]\d{8}$|^ES\d{8}[A-Z]$|^ES[A-Z]\d{7}[A-Z]$",  
        # Spain: 'ES' followed by 
        # 1 letter and 8 digits or
        # 8 digits and 1 letter or
        # 1 letter, 7 digits, and 1 letter
        "SE": r"^SE\d{12}$",  # Sweden: 'SE' followed by 12 digits
    }
    
    for country_code, pattern in patterns.items():
        if re.match(pattern, uid):
            return country_code, True
    return None, False

def vat_check(uid):
    country_code, is_valid = validate_vat_id(uid)
    if not is_valid:
        return False, "Invalid VAT ID format."
    
    # Remove the country code part to get the VAT number
    vat_number = uid[len(country_code):]
    
    # Create a SOAP client with the WSDL URL
    client = Client('http://ec.europa.eu/taxation_customs/vies/checkVatService.wsdl')

    # Call the checkVat operation
    try:
        result = client.service.checkVat(countryCode=country_code, vatNumber=vat_number)
        return result.valid, result
    except Exception as e:
        return False, str(e)

# Example usage:
print(vat_check("ATU123456789"))  # false, Invalid VAT ID format.)
print(vat_check("ATU12345678"))  # (True, <result object>)
#print(vat_check("BE1234567890")) # (True, <result object>)
#print(vat_check("CY12345678X"))  # (True, <result object>)
#print(vat_check("FRX1234567890"))# (True, <result object>)
#print(vat_check("NL123456789B01")) # (True, <result object>)
