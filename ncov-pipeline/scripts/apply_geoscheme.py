from bs4 import BeautifulSoup as BS
import pycountry_convert as pyCountry
import pycountry
import pandas as pd
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Reformat metadata file by adding column with subcontinental regions based on the UN geo-scheme",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("--metadata", required=True, help="Nextstrain metadata file")
    parser.add_argument("--geoscheme", required=True, help="XML file with geographic classifications")
    parser.add_argument("--output", required=True, help="Updated metadata file")
    args = parser.parse_args()

    metadata = args.metadata
    geoscheme = args.geoscheme
    output = args.output

    # path = "/Users/anderson/GLab Dropbox/Anderson Brito/projects/ncov/nextstrain/20200413_update3b/preanalyses/"
    # metadata = path + 'metadata_filtered.tsv'
    # geoscheme = path + "geoscheme.xml"
    # output = path + 'metadata_geo.tsv'

    infile = open(geoscheme, "r").read()
    soup = BS(infile, 'xml')
    levels = soup.find('levels')

    # get ISO alpha3 country codes
    isos = {}
    def get_iso(country):
        global isos
        if country not in isos.keys():
            try:
                isoCode = pyCountry.country_name_to_country_alpha3(country, cn_name_format="default")
                isos[country] = isoCode
            except:
                try:
                    isoCode = pycountry.countries.search_fuzzy(country)[0].alpha_3
                    isos[country] = isoCode
                except:
                    isos[country] = '?'
        return isos[country]

    # locate subcontinental regions in geoscheme
    geoLevels = {}
    c = 0
    for column in levels.find_all('region'):
        colName = column.name
        for area in column.find_all('area'):
            id = area['id']
            for country in area.string.split(','):
                iso = get_iso(country.strip())
                geoLevels[iso] = id

    # locate subnational regions for countries in geoscheme
    for column in levels.find_all('country'):
        colName = column.name
        for area in column.find_all('area'):
            for state in area.string.split(','):
                if state.strip() not in geoLevels.keys():
                    geoLevels[state.strip()] = area['id']

    # open metadata file as dataframe:
    dfN = pd.read_csv(metadata, encoding='ISO-8859-1', sep='\t')
    try:
        dfN.insert(4, 'region', '')
    except:
        pass
    dfN['region'] = dfN['iso'].map(geoLevels) # add column region in metadata


    # convert set of states into subnational regions
    for idx, row in dfN.iterrows():
        if dfN.loc[idx, 'division'] not in ['?', '', 'unknown']:
            if dfN.loc[idx, 'division'] in geoLevels.keys():
                dfN.loc[idx, 'country'] = geoLevels[dfN.loc[idx, 'division']]
            else:
                dfN.loc[idx, 'country'] = dfN.loc[idx, 'country']

    dfN.to_csv(output, sep='\t', index=False)
print('\nMetadata file successfully reformatted applying geo-scheme!\n')
