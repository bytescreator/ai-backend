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

# TODO: geliştirilecek


def invokable_mgm_weather_report_by_province(province: str):
    """
    Gets real time weather report of given province in Turkey from Meteoroloji Genel Müdürlüğü.
    Cannot be used for cities outside turkey. This function is synchronous, can be called in demand fast.

    Parameters:
    province (str): name of the province, should be correct form

    Returns:
    current real time weather information of given city pulled from mgm

    -9999 values are interpreted as unknown
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

    data = requests.get(
        f"https://servis.mgm.gov.tr/web/merkezler?il={province}", headers=common_headers).json()

    data = requests.get(
        f'https://servis.mgm.gov.tr/web/sondurumlar?merkezid={data[0]["gunlukTahminIstNo"]}', headers=common_headers).json()[0]

    logging.debug(f"mgm_weather_report_by_province called returned {data}")
    return data
