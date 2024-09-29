import requests
from bs4 import BeautifulSoup
import re
import os
import json
import persons_wiki
import urllib

#has 3 tables for congressional session: past, current, future
def get_full_congress_dict():
    page_url = "https://en.wikipedia.org/wiki/List_of_United_States_Congresses"
    response = requests.get(page_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    congress_dict = {}
    #below variables has "previous congress" and "current congress" in two tables in a list
    congress_tables = soup.findAll("table",{'class': "wikitable"})[:2]
    for congress_table in congress_tables:
        for row in congress_table.findAll("tr"):
            if row.find("a") is not None:
                congress_num = int(row.find("a").text.split()[0][:-2])
                URL = "https://en.wikipedia.org" + row.find("a").get("href")
                start_date = row.findAll("td")[0].text.strip()
                end_date = row.findAll("td")[-1].text.strip()
                congress_dict[congress_num] = {'start_date': start_date, 'end_date': end_date, 'URL': URL}
    return congress_dict



#shortcut for output to get_all_parties_dict()
#1-3 = {'A': 'Anti-Administration', 'P': 'Pro-Administration'}
#4-18 = {'DR': 'Democratic-Republican', 'F': 'Federalist'}
#19-24 = Jacksonian era
#25-34 = Democratic vs Whig vs Others
#100 - Present = Only Democrat, Republican, and Independent now
def get_all_parties_dict_fast():
    return {1: {'A': 'Anti-Administration', 'P': 'Pro-Administration'}, 2: {'A': 'Anti-Administration', 'P': 'Pro-Administration'}, 3: {'A': 'Anti-Administration', 'P': 'Pro-Administration'}, 4: {'DR': 'Democratic-Republican', 'F': 'Federalist'}, 5: {'DR': 'Democratic-Republican', 'F': 'Federalist'}, 6: {'DR': 'Democratic-Republican', 'F': 'Federalist'}, 7: {'DR': 'Democratic-Republican', 'F': 'Federalist'}, 8: {'DR': 'Democratic-Republican', 'F': 'Federalist'}, 9: {'DR': 'Democratic-Republican', 'F': 'Federalist'}, 10: {'DR': 'Democratic-Republican', 'F': 'Federalist'}, 11: {'DR': 'Democratic-Republican', 'F': 'Federalist'}, 12: {'DR': 'Democratic-Republican', 'F': 'Federalist'}, 13: {'DR': 'Democratic-Republican', 'F': 'Federalist'}, 14: {'DR': 'Democratic-Republican', 'F': 'Federalist'}, 15: {'DR': 'Democratic-Republican', 'F': 'Federalist'}, 16: {'DR': 'Democratic-Republican', 'F': 'Federalist'}, 17: {'DR': 'Democratic-Republican', 'F': 'Federalist'}, 18: {'DR': 'Democratic-Republican', 'F': 'Federalist', 'D': 'Democratic-Republican'}, 19: {'A': 'Anti-Jacksonian', 'J': 'Jacksonian'}, 20: {'NR': 'National Republican', 'J': 'Jacksonian'}, 21: {'NR': 'National Republican', 'J': 'Jacksonian', 'AM': 'Anti-Masonic'}, 22: {'NR': 'National Republican', 'J': 'Jacksonian', 'N': 'Nullifier', 'AM': 'Anti-Masonic'}, 23: {'NR': 'National Republican', 'J': 'Jacksonian', 'N': 'Nullifier', 'AM': 'Anti-Masonic'}, 24: {'NR': 'National Republican', 'J': 'Jacksonian', 'N': 'Nullifier', 'AM': 'Anti-Masonic', 'SR': "States' Rights"}, 25: {'D': 'Democratic', 'W': 'Whig', 'AM': 'Anti-Masonic', 'N': 'Nullifier'}, 26: {'D': 'Democratic', 'W': 'Whig', 'AM': 'Anti-Masonic', 'C': 'Conservative'}, 27: {'D': 'Democratic', 'W': 'Whig', 'ID': 'Independent Democratic'}, 28: {'D': 'Democratic', 'LO': 'Law and Order', 'W': 'Whig', 'ID': 'Independent Democratic', 'IW': 'Independent Whig'}, 29: {'D': 'Democratic', 'L': 'Liberty', 'W': 'Whig', 'A': 'American'}, 30: {'D': 'Democratic', 'ID': 'Independent Democratic', 'L': 'Liberty', 'W': 'Whig', 'A': 'American', 'I': 'Independent'}, 31: {'D': 'Democratic', 'FS': 'Free Soil', 'W': 'Whig', 'A': 'Know Nothing', 'I': 'Independent'}, 32: {'D': 'Democratic', 'FS': 'Free Soil', 'W': 'Whig', 'ID': 'Independent Democratic', 'SR': 'Southern Rights', 'U': 'Union'}, 33: {'A': 'Know Nothing', 'D': 'Democratic', 'F': 'Free Soil', 'W': 'Whig', 'ID': 'Independent Democratic', 'FS': 'Free Soil', 'I': 'Independent'}, 34: {'D': 'Democratic', 'O': 'Opposition', 'FS': 'Free Soil', 'R': 'Republican', 'W': 'Whig', 'A': 'Know Nothing'}, 35: {'A': 'Know Nothing', 'D': 'Democratic', 'R': 'Republican', 'ID': 'Independent Democratic'}, 36: {'A': 'Know Nothing', 'D': 'Democratic', 'R': 'Republican', 'ALD': 'Anti-Lecompton Democratic', 'ID': 'Independent Democratic', 'O': 'Opposition'}, 37: {'D': 'Democratic', 'R': 'Republican', 'UU': 'Unconditional Union', 'U': 'National Union', 'CU': 'Constitutional Union', 'ID': 'Independent Democratic'}, 38: {'D': 'Democratic', 'R': 'Republican', 'U': 'Unionist', 'UU': 'Unconditional Unionist', 'IR': 'Independent Republican'}, 39: {'D': 'Democratic', 'R': 'Republican', 'U': 'Unionist', 'UU': 'Unconditional Unionist', 'IR': 'Independent Republican'}, 40: {'D': 'Democratic', 'R': 'Republican', 'IR': 'Independent Republican', 'CR': 'Conservative Republican', 'C': 'Conservative'}, 41: {'D': 'Democratic', 'R': 'Republican', 'C': 'Conservative'}, 42: {'D': 'Democratic', 'LR': 'Liberal Republican', 'R': 'Republican', 'IR': 'Independent Republican'}, 43: {'D': 'Democratic', 'AM': 'Anti-Monopoly', 'LR': 'Liberal Republican', 'R': 'Republican', 'ID': 'Independent Democratic', 'I': 'Independent', 'IR': 'Independent Republican'}, 44: {'D': 'Democratic', 'AM': 'Anti-Monopoly', 'R': 'Republican', 'ID': 'Independent Democratic', 'I': 'Independent', 'IR': 'Independent Republican'}, 45: {'AM': 'Anti-Monopoly', 'D': 'Democratic', 'R': 'Republican', 'I': 'Independent Republican', 'ID': 'Independent Democratic', 'G': 'Greenback'}, 46: {'AM': 'Anti-Monopoly', 'D': 'Democratic', 'R': 'Republican', 'I': 'Independent', 'ID': 'Independent Democratic', 'GB': 'Greenback'}, 47: {'D': 'Democratic', 'I': 'Independent', 'RA': 'Readjuster', 'R': 'Republican', 'ID': 'Independent Democrat', 'GB': 'Greenback', 'IR': 'Independent Republican'}, 48: {'D': 'Democratic', 'RA': 'Readjuster', 'R': 'Republican', 'ID': 'Independent Democratic', 'I': 'Independent', 'GB': 'Greenback', 'IR': 'Independent Republican', 'AM': 'Anti-Monopoly'}, 49: {'D': 'Democratic', 'RA': 'Readjuster', 'R': 'Republican', 'GB': 'Greenback'}, 50: {'D': 'Democratic', 'RA': 'Readjuster', 'R': 'Republican', 'L': 'Labor', 'GB': 'Greenback', 'I': 'Independent', 'IR': 'Independent Republican'}, 51: {'D': 'Democratic', 'R': 'Republican', 'L': 'Labor'}, 52: {'D': 'Democratic', 'P': 'Populist', 'I': 'Independent', 'R': 'Republican'}, 53: {'D': 'Democratic', 'P': 'Populist', 'R': 'Republican', 'S': 'Silver', 'ID': 'Independent Democratic'}, 54: {'D': 'Democratic', 'P': 'Populist', 'R': 'Republican', 'SR': 'Silver Republican', 'S': 'Silver'}, 55: {'D': 'Democratic', 'P': 'Populist', 'R': 'Republican', 'SR': 'Silver Republican', 'S': 'Silver', 'IR': 'Independent Republican'}, 56: {'D': 'Democratic', 'P': 'Populist', 'R': 'Republican', 'SR': 'Silver Republican', 'S': 'Silver'}, 57: {'D': 'Democratic', 'P': 'Populist', 'R': 'Republican', 'SR': 'Silver Republican', 'S': 'Silver'}, 58: {'D': 'Democratic', 'P': 'Populist', 'R': 'Republican', 'SR': 'Silver Republican'}, 59: {'D': 'Democratic', 'R': 'Republican'}, 60: {'D': 'Democratic', 'R': 'Republican', 'ID': 'Independent Democratic'}, 61: {'D': 'Democratic', 'R': 'Republican', 'ID': 'Independent Democratic'}, 62: {'D': 'Democratic', 'Prog.': 'Bull Moose', 'R': 'Republican', 'S': 'Socialist'}, 63: {'D': 'Democratic', 'Prog.': 'Bull Moose', 'R': 'Republican', 'I': 'Independent'}, 64: {'D': 'Democratic', 'R': 'Republican', 'Prog.': 'Bull Moose', 'Soc.': 'Socialist', 'I': 'Independent', 'Proh.': 'Prohibition'}, 65: {'D': 'Democratic', 'R': 'Republican', 'Prog.': 'Bull Moose', 'Soc.': 'Socialist', 'Proh.': 'Prohibition'}, 66: {'D': 'Democratic', 'R': 'Republican', 'Soc.': 'Socialist', 'FL': 'Farmer-Labor', 'IR': 'Independent Republican', 'Proh.': 'Prohibition'}, 67: {'D': 'Democratic', 'FL': 'Farmer-Labor', 'R': 'Republican', 'Soc.': 'Socialist', 'IR': 'Independent Republican'}, 68: {'D': 'Democratic', 'FL': 'Farmer-Labor', 'R': 'Republican', 'Soc.': 'Socialist'}, 69: {'D': 'Democratic', 'FL': 'Farmer-Labor', 'R': 'Republican', 'Soc.': 'Socialist'}, 70: {'D': 'Democratic', 'FL': 'Farmer-Labor', 'R': 'Republican', 'S': 'Socialist'}, 71: {'D': 'Democratic', 'FL': 'Farmer-Labor', 'R': 'Republican'}, 72: {'D': 'Democratic', 'FL': 'Farmer-Labor', 'R': 'Republican', 'F': 'Farmer-Labor'}, 73: {'D': 'Democratic', 'F': 'Farmer-Labor', 'P': 'Progressive', 'R': 'Republican'}, 74: {'D': 'Democratic', 'FL': 'Farmer-Labor', 'P': 'Wisconsin Progressive', 'R': 'Republican'}, 75: {'D': 'Democratic', 'F': 'Farmer-Labor', 'P': 'Wisconsin Progressive', 'R': 'Republican', 'I': 'Independent', 'FL': 'Farmer-Labor'}, 76: {'D': 'Democratic', 'FL': 'Farmer-Labor', 'P': 'Wisconsin Progressive', 'R': 'Republican', 'I': 'Independent', 'AL': 'American Labor', 'WP': 'Wisconsin Progressive'}, 77: {'D': 'Democratic', 'FL': 'Farmer-Labor', 'P': 'Wisconsin Progressive', 'R': 'Republican', 'I': 'Independent', 'AL': 'American Labor'}, 78: {'D': 'Democratic', 'WP': 'Wisconsin Progressive', 'R': 'Republican', 'FL': 'Farmer-Labor', 'AL': 'American Labor'}, 79: {'D': 'Democratic', 'P': 'Progressive', 'R': 'Republican', 'FL': 'Farmer-Labor', 'AL': 'American Labor'}, 80: {'D': 'Democratic', 'P': 'Progressive', 'R': 'Republican', 'A': 'American Labor'}, 81: {'D': 'Democratic', 'R': 'Republican', 'AL': 'American Labor', 'Lib': 'Liberal', 'I': 'Independent'}, 82: {'D': 'Democratic', 'I': 'Independent', 'R': 'Republican'}, 83: {'D': 'Democratic', 'R': 'Republican', 'I': 'Independent'}, 84: {'D': 'Democratic', 'I': 'Independent', 'R': 'Republican'}, 85: {'D': 'Democratic', 'R': 'Republican'}, 86: {'D': 'Democratic', 'R': 'Republican'}, 87: {'D': 'Democratic', 'R': 'Republican'}, 88: {'D': 'Democratic', 'R': 'Republican'}, 89: {'D': 'Democratic', 'R': 'Republican'}, 90: {'D': 'Democratic', 'R': 'Republican'}, 91: {'D': 'Democratic', 'R': 'Republican'}, 92: {'D': 'Democratic', 'R': 'Republican'}, 93: {'D': 'Democratic', 'R': 'Republican', 'C': 'Conservative', 'I': 'Independent'}, 94: {'D': 'Democratic', 'I': 'Independent', 'C': 'Conservative', 'R': 'Republican'}, 95: {'C': 'Conservative', 'D': 'Democratic', 'I': 'Independent', 'R': 'Republican'}, 96: {'D': 'Democratic', 'I': 'Independent', 'R': 'Republican', 'C': 'Conservative'}, 97: {'D': 'Democratic', 'I': 'Independent', 'R': 'Republican', 'C': 'Conservative'}, 98: {'D': 'Democratic', 'I': 'Independent', 'R': 'Republican', 'C': 'Conservative'}, 99: {'D': 'Democratic', 'R': 'Republican', 'C': 'Conservative'}, 100: {'D': 'Democratic', 'R': 'Republican'}, 101: {'D': 'Democratic', 'R': 'Republican', 'I': 'Independent'}, 102: {'D': 'Democratic', 'R': 'Republican'}, 103: {'D': 'Democratic', 'R': 'Republican'}, 104: {'D': 'Democratic', 'R': 'Republican', 'I': 'Independent'}, 105: {'R': 'Republican', 'D': 'Democratic'}, 106: {'D': 'Democratic', 'R': 'Republican'}, 107: {'D': 'Democratic', 'I': 'Independent', 'IPM': 'Independence', 'R': 'Republican'}, 108: {'D': 'Democratic', 'I': 'Independent', 'R': 'Republican'}, 109: {'D': 'Democratic', 'I': 'Independent', 'R': 'Republican'}, 110: {'D': 'Democratic', 'I': 'Independent', 'R': 'Republican'}, 111: {'D': 'Democratic', 'I': 'Independent', 'R': 'Republican'}, 112: {'D': 'Democratic', 'I': 'Independent', 'R': 'Republican'}, 113: {'D': 'Democratic', 'I': 'Independent', 'R': 'Republican'}, 114: {'D': 'Democratic', 'I': 'Independent', 'R': 'Republican'}, 115: {'D': 'Democratic', 'I': 'Independent', 'R': 'Republican'}, 116: {'D': 'Democratic', 'I': 'Independent', 'R': 'Republican', 'L': 'Libertarian'}, 117: {'D': 'Democratic', 'I': 'Independent', 'R': 'Republican', 'L': 'Libertarian'}, 118: {'D': 'Democratic', 'I': 'Independent', 'R': 'Republican'}}

#shortcut for output to get_all_parties_dict()
def get_party_to_URL_dict_fast():
    return {'Anti-Administration': 'https://en.wikipedia.org/wiki/Anti-Administration_Party_(United_States)', 'Pro-Administration': 'https://en.wikipedia.org/wiki/Pro-Administration_Party_(United_States)', 'Democratic-Republican': 'https://en.wikipedia.org/wiki/Democratic-Republican_Party_(United_States)', 'Federalist': 'https://en.wikipedia.org/wiki/Federalist_Party_(United_States)', 'Anti-Jacksonian': 'https://en.wikipedia.org/wiki/Anti-Jacksonian_Party_(United_States)', 'Jacksonian': 'https://en.wikipedia.org/wiki/Jacksonian_Party_(United_States)', 'National Republican': 'https://en.wikipedia.org/wiki/National_Republican_Party_(United_States)', 'Anti-Masonic': 'https://en.wikipedia.org/wiki/Anti-Masonic_Party_(United_States)', 'Nullifier': 'https://en.wikipedia.org/wiki/Nullifier_Party_(United_States)', "States' Rights": 'https://en.wikipedia.org/wiki/States%27_Rights_Party_(United_States)', 'Democratic': 'https://en.wikipedia.org/wiki/Democratic_Party_(United_States)', 'Whig': 'https://en.wikipedia.org/wiki/Whig_Party_(United_States)', 'Conservative': 'https://en.wikipedia.org/wiki/Conservative_Party_of_New_York_State', 'Independent Democratic': 'https://en.wikipedia.org/wiki/Independent_Democratic_Party_(United_States)', 'Law and Order': 'https://en.wikipedia.org/wiki/Law_and_Order_Party_(United_States)', 'Independent Whig': 'https://en.wikipedia.org/wiki/Whig_Party_(United_States)', 'Liberty': 'https://en.wikipedia.org/wiki/Liberty_Party_(United_States,_1840)', 'American': 'https://en.wikipedia.org/wiki/Know_Nothing', 'Independent': 'https://en.wikipedia.org/wiki/Independent_(United_States)', 'Free Soil': 'https://en.wikipedia.org/wiki/Free_Soil_Party_(United_States)', 'Know Nothing': 'https://en.wikipedia.org/wiki/Know_Nothing_Party_(United_States)', 'Southern Rights': 'https://en.wikipedia.org/wiki/Southern_Rights_Party', 'Union': 'https://en.wikipedia.org/wiki/Union_Party_(United_States,_1850)', 'Opposition': 'https://en.wikipedia.org/wiki/Opposition_Party_(Southern_U.S.)', 'Republican': 'https://en.wikipedia.org/wiki/Republican_Party_(United_States)', 'Anti-Lecompton Democratic': 'https://en.wikipedia.org/wiki/Lecompton_Constitution', 'Unconditional Union': 'https://en.wikipedia.org/wiki/Unconditional_Union_Party_(United_States)', 'National Union': 'https://en.wikipedia.org/wiki/National_Union_Party_(United_States)', 'Constitutional Union': 'https://en.wikipedia.org/wiki/Constitutional_Union_Party_(United_States)', 'Unionist': 'https://en.wikipedia.org/wiki/Unionist_Party_(United_States)', 'Unconditional Unionist': 'https://en.wikipedia.org/wiki/Unconditional_Unionist_Party_(United_States)', 'Independent Republican': 'https://en.wikipedia.org/wiki/Independent_Republican_Party_(United_States)', 'Conservative Republican': 'https://en.wikipedia.org/wiki/Conservative_Republican_Party_(United_States)', 'Liberal Republican': 'https://en.wikipedia.org/wiki/Liberal_Republican_Party_(United_States)', 'Anti-Monopoly': 'https://en.wikipedia.org/wiki/Anti-Monopoly_Party_(United_States)', 'Greenback': 'https://en.wikipedia.org/wiki/Greenback_Party_(United_States)', 'Readjuster': 'https://en.wikipedia.org/wiki/Readjuster_Party_(United_States)', 'Independent Democrat': 'https://en.wikipedia.org/wiki/Independent_Democrat', 'Labor': 'https://en.wikipedia.org/wiki/Labor_Party_(United_States,_19th_century)', 'Populist': 'https://en.wikipedia.org/wiki/Populist_Party_(United_States)', 'Silver': 'https://en.wikipedia.org/wiki/Silver_Party_(United_States)', 'Silver Republican': 'https://en.wikipedia.org/wiki/Silver_Republican_Party_(United_States)', 'Bull Moose': 'https://en.wikipedia.org/wiki/Progressive_Party_(United_States,_1912)', 'Socialist': 'https://en.wikipedia.org/wiki/Socialist_Party_(United_States)', 'Prohibition': 'https://en.wikipedia.org/wiki/Prohibition_Party_(United_States)', 'Farmer-Labor': 'https://en.wikipedia.org/wiki/Farmer%E2%80%93Labor_Party_(United_States)', 'Progressive': 'https://en.wikipedia.org/wiki/Wisconsin_Progressive_Party', 'Wisconsin Progressive': 'https://en.wikipedia.org/wiki/Wisconsin_Progressive_Party_(United_States)', 'American Labor': 'https://en.wikipedia.org/wiki/American_Labor_Party_(United_States)', 'Liberal': 'https://en.wikipedia.org/wiki/Liberal_Party_of_New_York', 'Independence': 'https://en.wikipedia.org/wiki/Independence_Party_of_Minnesota', 'Libertarian': 'https://en.wikipedia.org/wiki/Libertarian_Party_(United_States)'}


def get_party_to_URL_dict():
    URL_dict = {1: {'A': 'Anti-Administration', 'P': 'Pro-Administration'}, 2: {'A': '/wiki/Anti-Administration_Party_(United_States)', 'P': '/wiki/Pro-Administration_Party_(United_States)'}, 3: {'A': '/wiki/Anti-Administration_Party_(United_States)', 'P': '/wiki/Pro-Administration_Party_(United_States)'}, 4: {'DR': '/wiki/Democratic-Republican_Party_(United_States)', 'F': '/wiki/Federalist_Party_(United_States)'}, 5: {'DR': '/wiki/Democratic-Republican_Party_(United_States)', 'F': '/wiki/Federalist_Party_(United_States)'}, 6: {'DR': '/wiki/Democratic-Republican_Party_(United_States)', 'F': '/wiki/Federalist_Party_(United_States)'}, 7: {'DR': '/wiki/Democratic-Republican_Party_(United_States)', 'F': '/wiki/Federalist_Party_(United_States)'}, 8: {'DR': '/wiki/Democratic-Republican_Party_(United_States)', 'F': '/wiki/Federalist_Party_(United_States)'}, 9: {'DR': '/wiki/Democratic-Republican_Party_(United_States)', 'F': '/wiki/Federalist_Party_(United_States)'}, 10: {'DR': '/wiki/Democratic-Republican_Party_(United_States)', 'F': '/wiki/Federalist_Party_(United_States)'}, 11: {'DR': '/wiki/Democratic-Republican_Party_(United_States)', 'F': '/wiki/Federalist_Party_(United_States)'}, 12: {'DR': '/wiki/Democratic-Republican_Party_(United_States)', 'F': '/wiki/Federalist_Party_(United_States)'}, 13: {'DR': '/wiki/Democratic-Republican_Party_(United_States)', 'F': '/wiki/Federalist_Party_(United_States)'}, 14: {'DR': '/wiki/Democratic-Republican_Party_(United_States)', 'F': '/wiki/Federalist_Party_(United_States)'}, 15: {'DR': '/wiki/Democratic-Republican_Party_(United_States)', 'F': '/wiki/Federalist_Party_(United_States)'}, 16: {'DR': '/wiki/Democratic-Republican_Party_(United_States)', 'F': '/wiki/Federalist_Party_(United_States)'}, 17: {'DR': '/wiki/Democratic-Republican_Party_(United_States)', 'F': '/wiki/Federalist_Party_(United_States)'}, 18: {'DR': '/wiki/Democratic-Republican_Party_(United_States)', 'F': '/wiki/Federalist_Party_(United_States)', 'D': '/wiki/Democratic-Republican_Party_(United_States)'}, 19: {'A': '/wiki/Anti-Jacksonian_Party_(United_States)', 'J': '/wiki/Jacksonian_Party_(United_States)'}, 20: {'NR': '/wiki/National_Republican_Party_(United_States)', 'J': '/wiki/Jacksonian_Party_(United_States)'}, 21: {'NR': '/wiki/National_Republican_Party_(United_States)', 'J': '/wiki/Jacksonian_Party_(United_States)', 'AM': '/wiki/Anti-Masonic_Party_(United_States)'}, 22: {'NR': '/wiki/National_Republican_Party_(United_States)', 'J': '/wiki/Jacksonian_Party_(United_States)', 'N': '/wiki/Nullifier_Party_(United_States)', 'AM': '/wiki/Anti-Masonic_Party_(United_States)'}, 23: {'NR': '/wiki/National_Republican_Party_(United_States)', 'J': '/wiki/Jacksonian_Party_(United_States)', 'N': '/wiki/Nullifier_Party_(United_States)', 'AM': '/wiki/Anti-Masonic_Party_(United_States)'}, 24: {'NR': '/wiki/National_Republican_Party_(United_States)', 'J': '/wiki/Jacksonian_Party_(United_States)', 'N': '/wiki/Nullifier_Party_(United_States)', 'AM': '/wiki/Anti-Masonic_Party_(United_States)', 'SR': '/wiki/States%27_Rights_Party_(United_States)'}, 25: {'D': '/wiki/Democratic_Party_(United_States)', 'W': '/wiki/Whig_Party_(United_States)', 'AM': '/wiki/Anti-Masonic_Party_(United_States)', 'N': '/wiki/Nullifier_Party_(United_States)'}, 26: {'D': '/wiki/Democratic_Party_(United_States)', 'W': '/wiki/Whig_Party_(United_States)', 'AM': '/wiki/Anti-Masonic_Party_(United_States)', 'C': '/wiki/Conservative_Party_(Virginia,_1834)'}, 27: {'D': '/wiki/Democratic_Party_(United_States)', 'W': '/wiki/Whig_Party_(United_States)', 'ID': '/wiki/Independent_Democratic_Party_(United_States)'}, 28: {'D': '/wiki/Democratic_Party_(United_States)', 'LO': '/wiki/Law_and_Order_Party_(United_States)', 'W': '/wiki/Whig_Party_(United_States)', 'ID': '/wiki/Independent_Democratic_Party_(United_States)', 'IW': '/wiki/Whig_Party_(United_States)'}, 29: {'D': '/wiki/Democratic_Party_(United_States)', 'L': '/wiki/Liberty_Party_(United_States,_1840)', 'W': '/wiki/Whig_Party_(United_States)', 'A': '/wiki/Know_Nothing'}, 30: {'D': '/wiki/Democratic_Party_(United_States)', 'ID': '/wiki/Independent_Democrat', 'L': '/wiki/Liberty_Party_(United_States,_1840)', 'W': '/wiki/Whig_Party_(United_States)', 'A': '/wiki/Know_Nothing', 'I': '/wiki/Independent_Party_(United_States)'}, 31: {'D': '/wiki/Democratic_Party_(United_States)', 'FS': '/wiki/Free_Soil_Party_(United_States)', 'W': '/wiki/Whig_Party_(United_States)', 'A': '/wiki/Know_Nothing_Party_(United_States)', 'I': '/wiki/Independent_Party_(United_States)'}, 32: {'D': '/wiki/Democratic_Party_(United_States)', 'FS': '/wiki/Free_Soil_Party', 'W': '/wiki/Whig_Party_(United_States)', 'ID': '/wiki/Independent_Democratic', 'SR': '/wiki/Southern_Rights_Party', 'U': '/wiki/Union_Party_(United_States,_1850)'}, 33: {'A': '/wiki/Know_Nothing_Party_(United_States)', 'D': '/wiki/Democratic_Party_(United_States)', 'F': '/wiki/Free_Soil_Party_(United_States)', 'W': '/wiki/Whig_Party_(United_States)', 'ID': '/wiki/Independent_Democratic', 'FS': '/wiki/Free_Soil_Party_(United_States)', 'I': '/wiki/Independent_Party_(United_States)'}, 34: {'D': '/wiki/Democratic_Party_(United_States)', 'O': '/wiki/Opposition_Party_(Northern_U.S.)', 'FS': '/wiki/Free_Soil_Party_(United_States)', 'R': '/wiki/Republican_Party_(United_States)', 'W': '/wiki/Whig_Party_(United_States)', 'A': '/wiki/Know_Nothing'}, 35: {'A': '/wiki/Know_Nothing_Party_(United_States)', 'D': '/wiki/Democratic_Party_(United_States)', 'R': '/wiki/Republican_Party_(United_States)', 'ID': '/wiki/Independent_Democratic_Party_(United_States)'}, 36: {'A': '/wiki/Know_Nothing_Party_(United_States)', 'D': '/wiki/Democratic_Party_(United_States)', 'R': '/wiki/Republican_Party_(United_States)', 'ALD': '/wiki/Lecompton_Constitution', 'ID': '/wiki/Independent_Democratic_Party_(United_States)', 'O': '/wiki/Opposition_Party_(Southern_U.S.)'}, 37: {'D': '/wiki/Democratic_Party_(United_States)', 'R': '/wiki/Republican_Party_(United_States)', 'UU': '/wiki/Unconditional_Union_Party_(United_States)', 'U': '/wiki/National_Union_Party_(United_States)', 'CU': '/wiki/Constitutional_Union_Party_(United_States)', 'ID': '/wiki/Independent_Democratic_Party_(United_States)'}, 38: {'D': '/wiki/Democratic_Party_(United_States)', 'R': '/wiki/Republican_Party_(United_States)', 'U': '/wiki/Unionist_Party_(United_States)', 'UU': '/wiki/Unconditional_Unionist_Party_(United_States)', 'IR': '/wiki/Independent_Republican_Party_(United_States)'}, 39: {'D': '/wiki/Democratic_Party_(United_States)', 'R': '/wiki/Republican_Party_(United_States)', 'U': '/wiki/Unionist_Party_(United_States)', 'UU': '/wiki/Unconditional_Unionist_Party_(United_States)', 'IR': '/wiki/Independent_Republican_Party_(United_States)'}, 40: {'D': '/wiki/Democratic_Party_(United_States)', 'R': '/wiki/Republican_Party_(United_States)', 'IR': '/wiki/Independent_Republican_Party_(United_States)', 'CR': '/wiki/Conservative_Republican_Party_(United_States)', 'C': '/wiki/Conservative_Party_(United_States)'}, 41: {'D': '/wiki/Democratic_Party_(United_States)', 'R': '/wiki/Republican_Party_(United_States)', 'C': '/wiki/Conservative_Party_(United_States)'}, 42: {'D': '/wiki/Democratic_Party_(United_States)', 'LR': '/wiki/Liberal_Republican_Party_(United_States)', 'R': '/wiki/Republican_Party_(United_States)', 'IR': '/wiki/Independent_Republican_Party_(United_States)'}, 43: {'D': '/wiki/Democratic_Party_(United_States)', 'AM': '/wiki/Anti-Monopoly_Party', 'LR': '/wiki/Liberal_Republican_Party_(United_States)', 'R': '/wiki/Republican_Party_(United_States)', 'ID': '/wiki/Independent_Democratic_Party_(United_States)', 'I': '/wiki/Independent_Party_(United_States)', 'IR': '/wiki/Independent_Republican_Party_(United_States)'}, 44: {'D': '/wiki/Democratic_Party_(United_States)', 'AM': '/wiki/Anti-Monopoly_Party', 'R': '/wiki/Republican_Party_(United_States)', 'ID': '/wiki/Independent_Democrat_(United_States)', 'I': '/wiki/Independent_(United_States)', 'IR': '/wiki/Independent_Republican_(United_States)'}, 45: {'AM': '/wiki/Anti-Monopoly_Party', 'D': '/wiki/Democratic_Party_(United_States)', 'R': '/wiki/Republican_Party_(United_States)', 'I': '/wiki/Independent_Republican_Party_(United_States)', 'ID': '/wiki/Independent_Democratic_Party_(United_States)', 'G': '/wiki/Greenback_Party_(United_States)'}, 46: {'AM': '/wiki/Anti-Monopoly_Party', 'D': '/wiki/Democratic_Party_(United_States)', 'R': '/wiki/Republican_Party_(United_States)', 'I': '/wiki/Independent_Party_(United_States)', 'ID': '/wiki/Independent_Democratic_Party_(United_States)', 'GB': '/wiki/Greenback_Party_(United_States)'}, 47: {'D': '/wiki/Democratic_Party_(United_States)', 'I': '/wiki/Independent_(politics)', 'RA': '/wiki/Readjuster_Party', 'R': '/wiki/Republican_Party_(United_States)', 'ID': '/wiki/Independent_Democrat', 'GB': '/wiki/Greenback_Party', 'IR': '/wiki/Independent_Republican_(United_States)'}, 48: {'D': '/wiki/Democratic_Party_(United_States)', 'RA': '/wiki/Readjuster_Party_(United_States)', 'R': '/wiki/Republican_Party_(United_States)', 'ID': '/wiki/Independent_Democratic_Party_(United_States)', 'I': '/wiki/Independent_Party_(United_States)', 'GB': '/wiki/Greenback_Party_(United_States)', 'IR': '/wiki/Independent_Republican_Party_(United_States)', 'AM': '/wiki/Anti-Monopoly_Party_(United_States)'}, 49: {'D': '/wiki/Democratic_Party_(United_States)', 'RA': '/wiki/Readjuster_Party_(United_States)', 'R': '/wiki/Republican_Party_(United_States)', 'GB': '/wiki/Greenback_Party_(United_States)'}, 50: {'D': '/wiki/Democratic_Party_(United_States)', 'RA': '/wiki/Readjuster_Party_(United_States)', 'R': '/wiki/Republican_Party_(United_States)', 'L': '/wiki/Labor_Party_(United_States,_19th_century)', 'GB': '/wiki/Greenback_Party_(United_States)', 'I': '/wiki/Independent_Party_(United_States)', 'IR': '/wiki/Independent_Republican_Party_(United_States)'}, 51: {'D': '/wiki/Democratic_Party_(United_States)', 'R': '/wiki/Republican_Party_(United_States)', 'L': '/wiki/Labor_Party_(United_States,_19th_century)'}, 52: {'D': '/wiki/Democratic_Party_(United_States)', 'P': '/wiki/Populist_Party_(United_States)', 'I': '/wiki/Independent_Party_(United_States)', 'R': '/wiki/Republican_Party_(United_States)'}, 53: {'D': '/wiki/Democratic_Party_(United_States)', 'P': '/wiki/Populist_Party_(United_States)', 'R': '/wiki/Republican_Party_(United_States)', 'S': '/wiki/Silver_Party_(United_States)', 'ID': '/wiki/Independent_Democratic_Party_(United_States)'}, 54: {'D': '/wiki/Democratic_Party_(United_States)', 'P': '/wiki/Populist_Party_(United_States)', 'R': '/wiki/Republican_Party_(United_States)', 'SR': '/wiki/Silver_Republican_Party_(United_States)', 'S': '/wiki/Silver_Party_(United_States)'}, 55: {'D': '/wiki/Democratic_Party_(United_States)', 'P': '/wiki/Populist_Party_(United_States)', 'R': '/wiki/Republican_Party_(United_States)', 'SR': '/wiki/Silver_Republican_Party_(United_States)', 'S': '/wiki/Silver_Party_(United_States)', 'IR': '/wiki/Independent_Republican_Party_(United_States)'}, 56: {'D': '/wiki/Democratic_Party_(United_States)', 'P': '/wiki/Populist_Party_(United_States)', 'R': '/wiki/Republican_Party_(United_States)', 'SR': '/wiki/Silver_Republican_Party_(United_States)', 'S': '/wiki/Silver_Party_(United_States)'}, 57: {'D': '/wiki/Democratic_Party_(United_States)', 'P': '/wiki/Populist_Party_(United_States)', 'R': '/wiki/Republican_Party_(United_States)', 'SR': '/wiki/Silver_Republican_Party_(United_States)', 'S': '/wiki/Silver_Party_(United_States)'}, 58: {'D': '/wiki/Democratic_Party_(United_States)', 'P': '/wiki/Populist_Party_(United_States)', 'R': '/wiki/Republican_Party_(United_States)', 'SR': '/wiki/Silver_Republican_Party_(United_States)'}, 59: {'D': '/wiki/Democratic_Party_(United_States)', 'R': '/wiki/Republican_Party_(United_States)'}, 60: {'D': '/wiki/Democratic_Party_(United_States)', 'R': '/wiki/Republican_Party_(United_States)', 'ID': '/wiki/Independent_Democratic_Party_(United_States)'}, 61: {'D': '/wiki/Democratic_Party_(United_States)', 'R': '/wiki/Republican_Party_(United_States)', 'ID': '/wiki/Independent_Democratic_Party_(United_States)'}, 62: {'D': '/wiki/Democratic_Party_(United_States)', 'Prog.': '/wiki/Progressive_Party_(United_States,_1912)', 'R': '/wiki/Republican_Party_(United_States)', 'S': '/wiki/Socialist_Party_(United_States)'}, 63: {'D': '/wiki/Democratic_Party_(United_States)', 'Prog.': '/wiki/Progressive_Party_(United_States,_1912)', 'R': '/wiki/Republican_Party_(United_States)', 'I': '/wiki/Independent_Party_(United_States)'}, 64: {'D': '/wiki/Democratic_Party_(United_States)', 'R': '/wiki/Republican_Party_(United_States)', 'Prog.': '/wiki/Progressive_Party_(United_States,_1912)', 'Soc.': '/wiki/Socialist_Party_of_America', 'I': '/wiki/Independent_Party_(United_States)', 'Proh.': '/wiki/Prohibition_Party_(United_States)'}, 65: {'D': '/wiki/Democratic_Party_(United_States)', 'R': '/wiki/Republican_Party_(United_States)', 'Prog.': '/wiki/Progressive_Party_(United_States,_1912)', 'Soc.': '/wiki/Socialist_Party_of_America', 'Proh.': '/wiki/Prohibition_Party_(United_States)'}, 66: {'D': '/wiki/Democratic_Party_(United_States)', 'R': '/wiki/Republican_Party_(United_States)', 'Soc.': '/wiki/Socialist_Party_of_America', 'FL': '/wiki/Farmer-Labor_Party_(United_States)', 'IR': '/wiki/Independent_Republican_Party_(United_States)', 'Proh.': '/wiki/Prohibition_Party_(United_States)'}, 67: {'D': '/wiki/Democratic_Party_(United_States)', 'FL': '/wiki/Farmer%E2%80%93Labor_Party_(United_States)', 'R': '/wiki/Republican_Party_(United_States)', 'Soc.': '/wiki/Socialist_Party_of_America', 'IR': '/wiki/Independent_Republican_Party_(United_States)'}, 68: {'D': '/wiki/Democratic_Party_(United_States)', 'FL': '/wiki/Farmer%E2%80%93Labor_Party_(United_States)', 'R': '/wiki/Republican_Party_(United_States)', 'Soc.': '/wiki/Socialist_Party_of_America'}, 69: {'D': '/wiki/Democratic_Party_(United_States)', 'FL': '/wiki/Farmer%E2%80%93Labor_Party_(United_States)', 'R': '/wiki/Republican_Party_(United_States)', 'Soc.': '/wiki/Socialist_Party_(United_States)'}, 70: {'D': '/wiki/Democratic_Party_(United_States)', 'FL': '/wiki/Farmer%E2%80%93Labor_Party_(United_States)', 'R': '/wiki/Republican_Party_(United_States)', 'S': '/wiki/Socialist_Party_(United_States)'}, 71: {'D': '/wiki/Democratic_Party_(United_States)', 'FL': '/wiki/Farmer%E2%80%93Labor_Party_(United_States)', 'R': '/wiki/Republican_Party_(United_States)'}, 72: {'D': '/wiki/Democratic_Party_(United_States)', 'FL': '/wiki/Farmer%E2%80%93Labor_Party_(United_States)', 'R': '/wiki/Republican_Party_(United_States)', 'F': '/wiki/Farmer%E2%80%93Labor_Party_(United_States)'}, 73: {'D': '/wiki/Democratic_Party_(United_States)', 'F': '/wiki/Farmer%E2%80%93Labor_Party', 'P': '/wiki/Wisconsin_Progressive_Party', 'R': '/wiki/Republican_Party_(United_States)'}, 74: {'D': '/wiki/Democratic_Party_(United_States)', 'FL': '/wiki/Farmer%E2%80%93Labor_Party_(United_States)', 'P': '/wiki/Wisconsin_Progressive_Party_(United_States)', 'R': '/wiki/Republican_Party_(United_States)'}, 75: {'D': '/wiki/Democratic_Party_(United_States)', 'F': '/wiki/Farmer%E2%80%93Labor_Party_(United_States)', 'P': '/wiki/Wisconsin_Progressive_Party_(United_States)', 'R': '/wiki/Republican_Party_(United_States)', 'I': '/wiki/Independent_Party_(United_States)', 'FL': '/wiki/Farmer%E2%80%93Labor_Party_(United_States)'}, 76: {'D': '/wiki/Democratic_Party_(United_States)', 'FL': '/wiki/Farmer%E2%80%93Labor_Party_(United_States)', 'P': '/wiki/Wisconsin_Progressive_Party_(United_States)', 'R': '/wiki/Republican_Party_(United_States)', 'I': '/wiki/Independent_Party_(United_States)', 'AL': '/wiki/American_Labor_Party_(United_States)', 'WP': '/wiki/Wisconsin_Progressive_Party_(United_States)'}, 77: {'D': '/wiki/Democratic_Party_(United_States)', 'FL': '/wiki/Farmer%E2%80%93Labor_Party_(United_States)', 'P': '/wiki/Wisconsin_Progressive_Party_(United_States)', 'R': '/wiki/Republican_Party_(United_States)', 'I': '/wiki/Independent_Party_(United_States)', 'AL': '/wiki/American_Labor_Party_(United_States)'}, 78: {'D': '/wiki/Democratic_Party_(United_States)', 'WP': '/wiki/Wisconsin_Progressive_Party_(United_States)', 'R': '/wiki/Republican_Party_(United_States)', 'FL': '/wiki/Farmer%E2%80%93Labor_Party_(United_States)', 'AL': '/wiki/American_Labor_Party_(United_States)'}, 79: {'D': '/wiki/Democratic_Party_(United_States)', 'P': '/wiki/Wisconsin_Progressive_Party', 'R': '/wiki/Republican_Party_(United_States)', 'FL': '/wiki/Farmer%E2%80%93Labor_Party_(United_States)', 'AL': '/wiki/American_Labor_Party_(United_States)'}, 80: {'D': '/wiki/Democratic_Party_(United_States)', 'P': '/wiki/Wisconsin_Progressive_Party', 'R': '/wiki/Republican_Party_(United_States)', 'A': '/wiki/American_Labor_Party'}, 81: {'D': '/wiki/Democratic_Party_(United_States)', 'R': '/wiki/Republican_Party_(United_States)', 'AL': '/wiki/American_Labor_Party_(United_States)', 'Lib': '/wiki/Liberal_Party_of_New_York', 'I': '/wiki/Independent_Party_(United_States)'}, 82: {'D': '/wiki/Democratic_Party_(United_States)', 'I': '/wiki/Independent_(politician)', 'R': '/wiki/Republican_Party_(United_States)'}, 83: {'D': '/wiki/Democratic_Party_(United_States)', 'R': '/wiki/Republican_Party_(United_States)', 'I': '/wiki/Independent_(politician)'}, 84: {'D': '/wiki/Democratic_Party_(United_States)', 'I': '/wiki/Independent_Party_(United_States)', 'R': '/wiki/Republican_Party_(United_States)'}, 85: {'D': '/wiki/Democratic_Party_(United_States)', 'R': '/wiki/Republican_Party_(United_States)'}, 86: {'D': '/wiki/Democratic_Party_(United_States)', 'R': '/wiki/Republican_Party_(United_States)'}, 87: {'D': '/wiki/Democratic_Party_(United_States)', 'R': '/wiki/Republican_Party_(United_States)'}, 88: {'D': '/wiki/Democratic_Party_(United_States)', 'R': '/wiki/Republican_Party_(United_States)'}, 89: {'D': '/wiki/Democratic_Party_(United_States)', 'R': '/wiki/Republican_Party_(United_States)'}, 90: {'D': '/wiki/Democratic_Party_(United_States)', 'R': '/wiki/Republican_Party_(United_States)'}, 91: {'D': '/wiki/Democratic_Party_(United_States)', 'R': '/wiki/Republican_Party_(United_States)'}, 92: {'D': '/wiki/Democratic_Party_(United_States)', 'R': '/wiki/Republican_Party_(United_States)'}, 93: {'D': '/wiki/Democratic_Party_(United_States)', 'R': '/wiki/Republican_Party_(United_States)', 'C': '/wiki/Conservative_Party_of_New_York', 'I': '/wiki/Independent_(politician)'}, 94: {'D': '/wiki/Democratic_Party_(United_States)', 'I': '/wiki/Independent_(politician)', 'C': '/wiki/Conservative_Party_of_New_York', 'R': '/wiki/Republican_Party_(United_States)'}, 95: {'C': '/wiki/Conservative_Party_(New_York)', 'D': '/wiki/Democratic_Party_(United_States)', 'I': '/wiki/Independent_Party_(United_States)', 'R': '/wiki/Republican_Party_(United_States)'}, 96: {'D': '/wiki/Democratic_Party_(United_States)', 'I': '/wiki/Independent_Party_(United_States)', 'R': '/wiki/Republican_Party_(United_States)', 'C': '/wiki/Conservative_Party_of_New_York_State'}, 97: {'D': '/wiki/Democratic_Party_(United_States)', 'I': '/wiki/Independent_Party_(United_States)', 'R': '/wiki/Republican_Party_(United_States)', 'C': '/wiki/Conservative_Party_of_New_York_State'}, 98: {'D': '/wiki/Democratic_Party_(United_States)', 'I': '/wiki/Independent_Party_(United_States)', 'R': '/wiki/Republican_Party_(United_States)', 'C': '/wiki/Conservative_Party_of_New_York_State'}, 99: {'D': '/wiki/Democratic_Party_(United_States)', 'R': '/wiki/Republican_Party_(United_States)', 'C': '/wiki/Conservative_Party_of_New_York_State'}, 100: {'D': '/wiki/Democratic_Party_(United_States)', 'R': '/wiki/Republican_Party_(United_States)'}, 101: {'D': '/wiki/Democratic_Party_(United_States)', 'R': '/wiki/Republican_Party_(United_States)', 'I': '/wiki/Independent_Party_(United_States)'}, 102: {'D': '/wiki/Democratic_Party_(United_States)', 'R': '/wiki/Republican_Party_(United_States)'}, 103: {'D': '/wiki/Democratic_Party_(United_States)', 'R': '/wiki/Republican_Party_(United_States)'}, 104: {'D': '/wiki/Democratic_Party_(United_States)', 'R': '/wiki/Republican_Party_(United_States)', 'I': '/wiki/Independent_Party_(United_States)'}, 105: {'R': '/wiki/Republican_Party_(United_States)', 'D': '/wiki/Democratic_Party_(United_States)'}, 106: {'D': '/wiki/Democratic_Party_(United_States)', 'R': '/wiki/Republican_Party_(United_States)'}, 107: {'D': '/wiki/Democratic_Party_(United_States)', 'I': '/wiki/Independent_(politics)', 'IPM': '/wiki/Independence_Party_of_Minnesota', 'R': '/wiki/Republican_Party_(United_States)'}, 108: {'D': '/wiki/Democratic_Party_(United_States)', 'I': '/wiki/Independent_(United_States)', 'R': '/wiki/Republican_Party_(United_States)'}, 109: {'D': '/wiki/Democratic_Party_(United_States)', 'I': '/wiki/Independent_Party_(United_States)', 'R': '/wiki/Republican_Party_(United_States)'}, 110: {'D': '/wiki/Democratic_Party_(United_States)', 'I': '/wiki/Independent_(politician)', 'R': '/wiki/Republican_Party_(United_States)'}, 111: {'D': '/wiki/Democratic_Party_(United_States)', 'I': '/wiki/Independent_(United_States)', 'R': '/wiki/Republican_Party_(United_States)'}, 112: {'D': '/wiki/Democratic_Party_(United_States)', 'I': '/wiki/Independent_(politician)', 'R': '/wiki/Republican_Party_(United_States)'}, 113: {'D': '/wiki/Democratic_Party_(United_States)', 'I': '/wiki/Independent_(politician)', 'R': '/wiki/Republican_Party_(United_States)'}, 114: {'D': '/wiki/Democratic_Party_(United_States)', 'I': '/wiki/Independent_politician', 'R': '/wiki/Republican_Party_(United_States)'}, 115: {'D': '/wiki/Democratic_Party_(United_States)', 'I': '/wiki/Independent_(United_States)', 'R': '/wiki/Republican_Party_(United_States)'}, 116: {'D': '/wiki/Democratic_Party_(United_States)', 'I': '/wiki/Independent_(United_States)', 'R': '/wiki/Republican_Party_(United_States)', 'L': '/wiki/Libertarian_Party_(United_States)'}, 117: {'D': '/wiki/Democratic_Party_(United_States)', 'I': '/wiki/Independent_(United_States)', 'R': '/wiki/Republican_Party_(United_States)', 'L': '/wiki/Libertarian_Party_(United_States)'}, 118: {'D': '/wiki/Democratic_Party_(United_States)', 'I': '/wiki/Independent_(United_States)', 'R': '/wiki/Republican_Party_(United_States)'}}
    parties_per_congress_dict = get_all_parties_dict_fast()
    party_URL_dict = {}
    for congress_num in parties_per_congress_dict.keys():
        dict_keys = list(parties_per_congress_dict[congress_num].keys())
        for key in dict_keys:
            party = parties_per_congress_dict[congress_num][key]
            URL = "https://en.wikipedia.org" + URL_dict[congress_num][key]
            party_URL_dict[party] = URL
    return party_URL_dict


#NEED to re-test
#get political parties/affiations for each congress
def get_all_parties_dict():
    congress_list = get_full_congress_dict() #will skip the first congress for convience on "previous congress" check
    party_dict = {1: {'A': 'Anti-Administration', 'P': 'Pro-Administration'}}
    for congress in congress_list:
        congress_num = congress['congress_num']
        party_dict[congress_num] = {}
        print("Congress Num: " + str(congress['congress_num']))
        URL = congress["URL"]
        response = requests.get(URL)
        soup = BeautifulSoup(response.content, 'html.parser')

        all_tables = soup.find_all("table",{'class':"wikitable"})
        party_tables = [] #will be a list of 2 HTML elements with the parties in the senate and house respectively 
        for table in all_tables: #will find the two correct tables and add to above list
            for row in table.find_all("th"):
                if row.get("colspan") != None:
                    if "Party" in row.text or "Faction" in row.text: #no parties until 4th congress, only factions
                        party_tables.append(table)

        for table in party_tables:
            for row in table.find_all("a"):
                if row.text in ["previous Congress", "previous congress"]: #indicates end of parties listed
                    break
                if row.text == '[d]': #unique case to skip
                    continue
                temp_list = re.findall('[A-Z][^A-Z]*', row.text) #will separate a string by uppercase letters
                temp_list = [val.strip() for val in temp_list]
                party = ' '.join(temp_list).strip() if temp_list[0][-1] != '-' else ''.join(temp_list).strip()
                #get text inside parenthesis that represents an abbreviation
                temp_list = re.search(r'\((.*?)\)', row.parent.text)
                abbreviation = temp_list.group(1) if temp_list != None else party[0]
                abbreviation = abbreviation if abbreviation != "caucusing withDemocrats" else 'I' #unique case to fix
                if party == "Farmer– Labor": #67th-79th congress
                    party = "Farmer-Labor"
                party_dict[congress_num][abbreviation] = party
                # print("\t" + abbreviation + ":   " + party)
    #fix unique case in 28th congress
    party_dict[28]['LO'] = "Law and Order"
    #fix unique case in 33rd congress
    del party_dict[33]["United States"]
    party_dict[33]['I'] = "Independent"
    #fix unique case in 34th congress
    del party_dict[34]["Know Nothing"]
    party_dict[34]['A'] = "Know Nothing"
    #fix unique case in 36th congress
    party_dict[36]['ALD'] = "Anti-Lecompton Democratic"
    print(party_dict)
    return party_dict





def get_congresspeople_for_a_congress(page_url, congress_num, congress_start_date=None):
    response = requests.get(page_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    print("\n" + page_url)


    #24th congress wiki page does not use tables; fix using a modified html file with two tables elements to read
    if page_url == "https://en.wikipedia.org/wiki/24th_United_States_Congress":
        with open("html/24th_congress_data.html", 'r', encoding='utf-8') as file:
            html_content = file.read()
            soup = BeautifulSoup(html_content, 'html.parser')

    tables = soup.find_all("table",{'class':"col-begin", 'role':"presentation"})[:2]


    # senate_table, representative_table = tables[:2]
    # #check for connecticut or alabama id ; alabama starts as of 16th congress 
    # check_senate = senate_table.find('div', class_="mw-heading mw-heading4").find("h4").get("id") in ["Alabama", "Connecticut"]
    # check_representative = representative_table.find('div', class_="mw-heading mw-heading4").find("h4").get("id") in ["Alabama_2", "Connecticut_2"]
    # if (check_senate and check_representative) is not True:
    #     print("Issue")

    congress_parties_dict = get_all_parties_dict_fast()

    all_congresspersons_data_list = []
    type = "Senator" #will change to "Representative" at bottom of while loop for 2nd table
    for table in tables:
        states = [heading.find("h4").text.strip() for heading in table.find_all('div', class_='mw-heading4')]
        congressmen_by_state_HTML = table.find_all("dl") #need to remove senators not at the start of congress session
        #below line: removes senators not at start of congress session; is written as a sub-dl tag in the html code 
        congressmen_by_state_HTML = [dl for dl in congressmen_by_state_HTML if dl.find_parent('dl') is None] 

    
        for index in range(len(states)): #for each state
            state = states[index]
            if state in ["Non-voting members", "Non-voting delegates", "Foreign Relations", 
                         "Non-voting member", "Delegates", "Non-voting delegations"]:
                continue
            # Check if the parent of the <a> tag is a direct child of the <dl> tag; 
                # to prevent recording of substitute congressman
            for a in congressmen_by_state_HTML[index].find_all('a', resurive=False):
                # print(a.text)
                if a.text in ["Skip to House of Representatives", "data missing"] or a.text[0] == '[':
                    continue
                #filter for no "span" direct parent tag; is unneeded data
                if a.find_parent('dl') == congressmen_by_state_HTML[index] and a.parent.name != "span":
                    #get party affiation below
                    name = urllib.parse.unquote(a.text.strip())
                    URL = urllib.parse.unquote("https://en.wikipedia.org" + a.get("href"))
                    text = a.parent.text
                    match = re.search(r'\((.*?)\)', text) #get text inside parenthesis that represents party affiation
                    if match == None:
                        if name == "William G. McAdoo": #edge case for Senate, 73th congress
                            match = re.search(r'\((.*?)\)', "(D)")
                    party = match.group(1)
                    if URL == "https://en.wikipedia.org/wiki/Nullifier_Party": #found in 23rd congress
                        continue
                    if URL == "https://en.wikipedia.org/wiki/Law_and_Order_Party_of_Rhode_Island": #found in 28rd congress
                        continue                  
                    if URL == "https://en.wikipedia.org/wiki/Independent_Democrat": #found in 32nd congress  
                        continue
                    if URL == "https://en.wikipedia.org/wiki/Liberal_Republican_Party_(United_States)": #found in 43th congress
                        continue  
                    if URL == "https://en.wikipedia.org/wiki/Democratic_Party_(United_States)": #found in 47th congress
                        continue
                    if URL == "https://en.wikipedia.org/wiki/Liberal_Party_of_New_York": #found in 84th congress
                        continue
                    if URL == "https://en.wikipedia.org/wiki/Conservative_Party_of_New_York": #found in 92nd congress
                        continue
                    if URL == "https://en.wikipedia.org/wiki/Independent_(politician)": #found in 93rd congress
                        continue
                    if URL == "https://en.wikipedia.org/wiki/Conservative_Party_of_New_York_State": #found in 94th congress
                        continue
                    if URL == "https://en.wikipedia.org/wiki/New_Progressive_Party_of_Puerto_Rico": #105th congress
                        continue

                    if congress_num == 35 and name == "John C. Kunkel": #wrong URL; got grandson's URL
                        URL = "https://en.wikipedia.org/wiki/John_Christian_Kunkel"
                    possible_party_full_name = congress_parties_dict[congress_num].get(party)
                    if possible_party_full_name == None:
                        if congress_num == 18:
                            if "DR" in party:
                                party = "Democratic-Republican"
                            if "F" in party:
                                party = "Federalist"
                        elif party == "DFL": #the Minnesota subset of the Democratic Party
                            party = "Democratic"
                        elif party == "Anti-M":
                            party = "Anti-Masonic"
                        elif party == "States Rights D": #for Franklin H. Elmore of 25th congress
                            party = "Democratic"
                        elif party == "Ind. D":      #for Zadok Casey of 27th Congress
                            party = "Independent Democrat"
                        elif party in ["Ind. W", "IW"]:      
                            party = "Independent Whig"                                   
                        elif party == "UA":
                            party = "Unconditional Union"
                        elif party == "I, later P": #for James H. Kyle of 52nd congress
                            party ="Independent"
                        elif party == "D/S": #for Francis G. Newlands of 53rd congress
                            party = "Silver"
                        elif party == "R-NPL": #for Lynn Frazier of 68th - 70th congress
                            party = "Republican"
                        elif party == "FL": #for 73rd congress
                            party = "Farmer-Labor"
                        elif congress_num == 69 and party == "S":
                            party = "Socialist"
                        elif congress_num == 78 and party == "P":
                            party = "Wisconsin Progressive"
                        elif congress_num == 80 and party == "AL":
                            party = "American Labor"
                        elif congress_num == 84 and party == "D-L":
                            party = "Democratic"
                        elif party == "D-NPL": #for Quentin Burdick of 86-88 congress
                            party = "Democratic"
                        elif party == "C":
                            party = "Conservative"
                        elif congress_num >= 92 and party == "I":
                            party = "Independent"
                        elif party == "D, then R": 
                            party = "Democratic"
                        elif congress_num== 99 and party == "C; changed to R on October 7, 1985": #for William Carney
                            party = "Conservative"
                        elif congress_num == 101 and party == "D then R": 
                            party = "Democratic"
                        elif party == "D, then R from November 9, 1994":
                            party = "Democratic"
                        elif party == "D, switched to R July 27, 2000":
                            party = "Democratic"
                        elif party == "D, switched to I January 27, 2000":
                            party = "Democratic"
                        elif party == "R until June 6, 2001, then I":
                            party = "Republican"
                        elif congress_num == 110 and party == "ID":
                            party = "Independent"
                        elif party == "R, then I, then L": #116th congress
                            party = "Republican"
                        elif party == "R, then I": #116th congress
                            party = "Republican"
                        elif name == "Joe Manchin" and congress_num == 118: #Democratic until May 31, 2024
                            party = "Democratic"
                        else:
                            print("Party Abbrev. Error: " + party + "; " + URL)
                    else:
                        party = possible_party_full_name


                    individual_congressperson_data_dict = {'name':name, 'URL': URL,'party': party, 
                            'type': type, 'state': state}
                    new_data = (persons_wiki.get_politician_data(URL, congress_start_date, congress_num))
                    individual_congressperson_data_dict.update(new_data)

                    all_congresspersons_data_list.append(individual_congressperson_data_dict)

                    # print(URL)


        type = "Representative"
    return all_congresspersons_data_list


if __name__ == "__main__":
    congress_dict = get_full_congress_dict()
    count = 0
    for congress in congress_dict:
        congress_num = congress
        congress_URL = congress_dict[congress_num]["URL"]
        congress_start_date = congress_dict[congress_num]["start_date"]
        # print(str(congress_num) + ": " + congress_start_date)

        if 53 <= congress_num <= 53:
            data = get_congresspeople_for_a_congress(congress_URL, congress_num, congress_start_date)
            file_path = "json_data/congress" + str(congress_num) + ".json"
            # Ensure the directory exists
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w') as file:
                json.dump(data, file, indent=4)
        # count += len(result)
        # print(count)



    #NOTE: json dumps automatically encrypts special characters into json files; must decrypt when receiving
