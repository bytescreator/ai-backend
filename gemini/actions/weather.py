"""
this file defines weather actions usable by gemini
"""

import logging

import requests

common_headers = {
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Referrer": "https://www.mgm.gov.tr/",
    "Origin": "https://www.mgm.gov.tr",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.5",
}

plaka = {
    1: "Adana",
    2: "Adıyaman",
    3: "Afyonkarahisar",
    4: "Ağrı",
    5: "Amasya",
    6: "Ankara",
    7: "Antalya",
    8: "Artvin",
    9: "Aydın",
    10: "Balıkesir",
    11: "Bilecik",
    12: "Bingöl",
    13: "Bitlis",
    14: "Bolu",
    15: "Burdur",
    16: "Bursa",
    17: "Çanakkale",
    18: "Çankırı",
    19: "Çorum",
    20: "Denizli",
    21: "Diyarbakır",
    22: "Edirne",
    23: "Elazığ",
    24: "Erzincan",
    25: "Erzurum",
    26: "Eskişehir",
    27: "Gaziantep",
    28: "Giresun",
    29: "Gümüşhane",
    30: "Hakkâri",
    31: "Hatay",
    32: "Isparta",
    33: "Mersin",
    34: "İstanbul",
    35: "İzmir",
    36: "Kars",
    37: "Kastamonu",
    38: "Kayseri",
    39: "Kırklareli",
    40: "Kırşehir",
    41: "Kocaeli",
    42: "Konya",
    43: "Kütahya",
    44: "Malatya",
    45: "Manisa",
    46: "Kahramanmaraş",
    47: "Mardin",
    48: "Muğla",
    49: "Muş",
    50: "Nevşehir",
    51: "Niğde",
    52: "Ordu",
    53: "Rize",
    54: "Sakarya",
    55: "Samsun",
    56: "Siirt",
    57: "Sinop",
    58: "Sivas",
    59: "Tekirdağ",
    60: "Tokat",
    61: "Trabzon",
    62: "Tunceli",
    63: "Şanlıurfa",
    64: "Uşak",
    65: "Van",
    66: "Yozgat",
    67: "Zonguldak",
    68: "Aksaray",
    69: "Bayburt",
    70: "Karaman",
    71: "Kırıkkale",
    72: "Batman",
    73: "Şırnak",
    74: "Bartın",
    75: "Ardahan",
    76: "Iğdır",
    77: "Yalova",
    78: "Karabük",
    79: "Kilis",
    80: "Osmaniye",
    81: "Düzce"
}


def invokable_mgm_weather_report_by_province(plate_num: int):
    """
    Gets real time weather report of given province in Turkey from Meteoroloji Genel Müdürlüğü.
    Cannot be used for cities outside turkey. This function is synchronous, can be called in demand fast.

    Parameters:
    province (int): plate number of the province in int type, should not be asked from
    the user, instead the model should provide it by itself.

    Returns:
    current real time weather information of given city pulled from mgm

    Weather data dictionary containing meteorological information:
    - 'aktuelBasinc': Current atmospheric pressure (in hPa).
    - 'denizSicaklik': Sea temperature (in degrees Celsius, -9999 indicates no data).
    - 'denizeIndirgenmisBasinc': Sea-level adjusted atmospheric pressure (in hPa).
    - 'gorus': Visibility (in meters, -9999 indicates no data).
    - 'hadiseKodu': Weather event code (e.g., 'CB' for cumulonimbus clouds).
    - 'istNo': Station number (identifier for the weather station).
    - 'kapalilik': Cloud cover (percentage, -9999 indicates no data).
    - 'karYukseklik': Snow depth (in centimeters, -9999 indicates no data).
    - 'nem': Relative humidity (in percentage).
    - 'rasatMetar': METAR report (observational weather data, -9999 indicates no data).
    - 'rasatSinoptik': Synoptic observation report (weather data, -9999 indicates no data).
    - 'rasatTaf': TAF report (weather forecast data, -9999 indicates no data).
    - 'ruzgarHiz': Wind speed (in meters per second).
    - 'ruzgarYon': Wind direction (in degrees, where 0 is North).
    - 'sicaklik': Temperature (in degrees Celsius).
    - 'veriZamani': Timestamp of the recorded data (in ISO 8601 format).
    - 'yagis00Now': Current precipitation (in millimeters for the last 0 hours).
    - 'yagis10Dk': Precipitation in the last 10 minutes (in millimeters).
    - 'yagis12Saat': Precipitation in the last 12 hours (in millimeters).
    - 'yagis1Saat': Precipitation in the last 1 hour (in millimeters).
    - 'yagis24Saat': Precipitation in the last 24 hours (in millimeters).
    - 'yagis6Saat': Precipitation in the last 6 hours (in millimeters).
    - 'denizVeriZamani': Timestamp for the sea data (in ISO 8601 format).
    """

    province = plaka[int(plate_num)]
    data = requests.get(
        f"https://servis.mgm.gov.tr/web/merkezler?il={province}", headers=common_headers).json()

    data = requests.get(
        f'https://servis.mgm.gov.tr/web/sondurumlar?merkezid={data[0]["gunlukTahminIstNo"]}', headers=common_headers).json()[0]

    logging.debug(f"mgm_weather_report_by_province called returned {data}")
    return data
