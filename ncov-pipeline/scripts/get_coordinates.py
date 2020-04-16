# coding=utf-8
import pandas as pd
from geopy.geocoders import Nominatim
import argparse
from bs4 import BeautifulSoup as BS
import numpy as np

geolocator = Nominatim(user_agent="email@gmail.com")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Generate file with latitudes and longitudes of samples listed in a metadata file",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("--metadata", required=True, help="Nextstrain metadata file")
    parser.add_argument("--geoscheme", required=True, help="XML file with geographic schemes")
    parser.add_argument("--columns", nargs='+', type=str,  help="list of columns that need coordinates")
    parser.add_argument("--cache", required=False,  help="list preexisting latitudes and longitudes")
    parser.add_argument("--output", required=True, help="TSV file containing geographic coordinates")
    args = parser.parse_args()

    metadata = args.metadata
    geoscheme = args.geoscheme
    columns = args.columns
    # columns = [field for field in args.columns[0].split()]
    cache = args.cache
    output = args.output

    # path = "/Users/anderson/GLab Dropbox/Anderson Brito/projects/ncov/nextstrain/20200413_update3b/preanalyses/"
    # metadata = path + 'metadata_geo.tsv'
    # geoscheme = path + "geoscheme.xml"
    # columns = ['region', 'country', 'division', 'location']
    # cache = path + 'cache.tsv'
    # output = path + 'lat_longs.tsv'


    force_coordinates = {'Washington': ('47.468284', '-120.491620')}


    infile = open(geoscheme, "r").read()
    soup = BS(infile, 'xml')

    results = {trait: {} for trait in columns} # content to be exported as final result

    # extract coordinates from cache file
    try:
        for line in open(cache).readlines():
            if not line.startswith('\n'):
                try:
                    trait, place, lat, long = line.strip().split('\t')
                    if trait in results.keys():
                        entry = {place: (str(lat), str(long))}
                        results[trait].update(entry) # save as pre-existing result
                except:
                    pass
    except:
        pass

    # extract coordinates from XML file
    dont_search = []
    set_countries = []
    levels = soup.find('levels')
    for trait in columns:
        if levels.find(trait):
            content = levels.find(trait)
            for area in content.find_all('area'):
                coordinates = {}
                try:
                    area_name = area['id'] # name of the pre-defined region in the XML file
                    entry = {area_name: (area['lat'], area['long'])}
                    coordinates.update(entry)
                    if area_name not in results[trait]:
                        results[trait].update(coordinates)
                        dont_search.append(area_name)
                        country_name = area_name.split('-')[0]
                        if trait == 'country' and country_name not in set_countries:
                            set_countries.append(country_name)
                except:
                    pass

    # find coordinates for locations not found in cache or XML file
    def find_coordinates(place):
        try:
            location = geolocator.geocode(place, language='en')
            lat, long = location.latitude, location.longitude
            coord = (str(lat), str(long))
            return coord
        except:
            coord = ('?', '?')
            return coord

    # open metadata file as dataframe
    dfN = pd.read_csv(metadata, encoding='ISO-8859-1', sep='\t')

    queries = []
    pinpoints = [dfN[trait].values.tolist() for trait in columns if trait != 'region']
    for address in zip(*pinpoints):
        traits = [trait for trait in columns if trait != 'region']
        for position, place in enumerate(address):
            level = traits[position]
            query = list(address[0:position+1])
            queries.append((level, query))

    not_found = []
    for unknown_location in queries:
        trait, location = unknown_location[0], unknown_location[1]
        target = location[-1]
        if target not in ['?', '', 'NA', 'NAN', 'unknown', '-', np.nan, None]:
            if target not in results[trait]:
                new_query = []
                for name in location:
                    try:
                        if name.split('-')[0] in set_countries:
                            new_query.append(name.split('-')[0]) # correcting XML pre-defined country names
                    except:
                        pass
                    if name not in dont_search:
                        new_query.append(name)

                item = (trait, ', '.join(new_query))
                coord = ('?', '?')
                if item not in not_found:
                    coord = find_coordinates(new_query)
                if '?' in coord:
                    if item not in not_found:
                        not_found.append(item)
                        print('\t* WARNING! Coordinates not found for: ' + trait + ', ' + ', '.join(new_query))
                else:
                    print(trait + ', ' + target + '. Coordinates = ' + ', '.join(coord))
                    entry = {target: coord}
                    results[trait].update(entry)

    print('\n### These coordinates were found and saved in the output file:')
    with open(output, 'w') as outfile:
        for trait, lines in results.items():
            print('\n* ' + trait)
            for place, coord in lines.items():
                # print(place, coord)
                if place in force_coordinates:
                    lat, long = force_coordinates[place][0], force_coordinates[place][1]
                else:
                    lat, long = coord[0], coord[1]
                print(place + ': ' + lat + ', ' + long)
                line = "{}\t{}\t{}\t{}\n".format(trait, place, lat, long)
                outfile.write(line)
            outfile.write('\n')

    if len(not_found) > 1:
        print('\n### WARNING! Some coordinates were not found (see below).'
              '\nTypos or especial characters on place name my explain such errors.'
              '\nPlease fix them, and run the script again, or add coordinates manually:\n')
        for trait, address in not_found:
            print(trait + ': ' + address)
    print('\n')
