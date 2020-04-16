import pycountry_convert as pyCountry
import argparse
from Bio import SeqIO
import pandas as pd
import numpy as np
import pycountry


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Filter nextstrain metadata files re-formmating and exporting only selected lines",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("--genomes", required=True, help="FASTA file genomes to be used")
    parser.add_argument("--metadata1", required=True, help="Metadata file from NextStrain")
    parser.add_argument("--metadata2", required=False, help="Custom lab metadata file")
    parser.add_argument("--output1", required=True, help="Filtered metadata file")
    parser.add_argument("--output2", required=True, help="TSV file for renaming virus IDs")
    parser.add_argument("--output3", required=True, help="Reformatted, final FASTA file")
    args = parser.parse_args()

    genomes = args.genomes
    metadata1 = args.metadata1
    metadata2 = args.metadata2
    output1 = args.output1
    output2 = args.output2
    output3 = args.output3


    # genomes = path + 'sequences_temp.fasta'
    # metadata1 = path + 'metadata.tsv'
    # metadata2 = path + 'COVID-19 sequencing.xlsx'
    # output1 = path + 'metadata_filtered.tsv'
    # output2 = path + 'rename.tsv'
    # output3 = path + 'sequences.fasta'


    # create a dict of existing sequences
    sequences = {}
    for fasta in SeqIO.parse(open(genomes), 'fasta'):  # as fasta:
        id, seq = fasta.description, fasta.seq
        if id not in sequences.keys():
            sequences[id] = str(seq)

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


    # nextstrain metadata
    dfN = pd.read_csv(metadata1, encoding='ISO-8859-1', sep='\t')
    try:
        dfN = dfN.drop(columns=['virus', 'region', 'segment', 'age', 'sex', 'title', 'date_submitted'])
        dfN.insert(4, 'iso', '')
    except:
        pass
    dfN['update'] = '?'
    dfN.fillna('?', inplace=True)
    # dfN.astype(str)
    lColumns = dfN.columns.values # list of column in the original metadata file
    fix_names = {'LiÃ¨ge': 'Liege', 'Auvergne-RhÃ´ne-Alpes': 'Auvergne-Rhone-Alpes', 'CompiÃ¨gne': 'Compiegne',
                 'Bourgogne-France-ComtÃÂÃÂ©': 'Bourgogne-Franche-Comté', 'Meudon la ForÃÂÃÂªt': 'Meudon la Foret',
                 'SmÃÂÃÂ¥land': 'Smaland', 'GraubÃÂÃÂ¼nden': 'Graubunden'}

    # Lab genomes metadata
    dfL = pd.read_excel(metadata2, index_col=None, header=0, sheet_name='Amplicon_Sequencing',
                        converters={'Yale ID*': str, 'Collection-date*': str, 'Update*': str})
    dfL.fillna('?', inplace = True)
    dfL.set_index("Yale ID*", inplace=True)


    dHeaders = {}
    notFound = []
    lstNewMetadata = []
    found = []
    lab_label = {}
    for id in sequences.keys():
        # check nextstrain metadata first
        dRow = {}
        if id in dfN['strain'].to_list() and 'Yale-' not in id:

            print('Exporting metadata for ' + id)
            fields = {column: '' for column in lColumns}
            row = dfN.loc[lambda dfN: dfN['strain'] == id]

            strain = row.strain.values[0]
            country = row.country.values[0]

            if country != row.country_exposure.values[0].strip(): # ignore travel cases
                continue
            try:
                division = row.division.values[0]
                if division != row.division_exposure.values[0].strip(): # ignore travel cases
                    continue
            except:
                division = 'NA'
            if len(country) < 2:
                country = 'unknown'
            if len(division) < 2:
                division = country

            iso = get_iso(country)
            row.iso.values[0] = iso # needed for exporting a renaming file
            date = row.date.values[0]
            header = '|'.join([strain, iso, division.replace(' ', '-'), date])
            dHeaders[strain] = header

            lValues = row.values[0]
            for field, value in zip(fields.keys(), lValues):
                # print(id)
                if value in ['', np.nan, None]:
                    value = '?'
                # fix names
                if field == 'division':
                    if row.division.values[0].strip() in fix_names.keys():
                        value = fix_names[row.division.values[0].strip()]
                if field == 'location':
                    if row.location.values[0].strip() in fix_names.keys():
                        value = fix_names[row.location.values[0].strip()]

                fields[field] = value
            if country == '':
                continue

            dRow[id] = fields
            found.append(strain)

        # check lab's metadata otherwise
        if id not in dRow.keys():
            # check lab metadata
            if 'Yale-' in id:
                try:
                    id = id.split('/')[1][3:]
                    lab_label[id] = ''
                except:
                    if id not in lab_label.keys():
                        lab_label[id] = ''
                if id in dfL.index:
                    fields = {column: '' for column in lColumns}
                    row = dfL.loc[id]
                    if row['State*'] == '?':
                        code = 'CT'
                    else:
                        code = row['State*']
                    strain = 'USA/' + code + '-' + id + '/2020' # revert to nextstrain strain name

                    if strain not in found:
                        gisaid_epi_isl = '?'
                        genbank_accession = '?'
                        if len(str(row['Collection-date*'])) > 1:
                            date = row['Collection-date*'].split(' ')[0].replace('.', '-')
                        else:
                            date = '?'
                        country = row['Country*']

                        division = row['Division*']
                        if row['Division*'] == '?':
                            code = 'Connecticut'
                        else:
                            code = row['Division*']

                        if len(str(row['City*'])) > 1:
                            location = row['City*'].replace('-', ' ')
                        else:
                            location = '?'
                        region_exposure = '?'
                        country_exposure = '?'
                        iso = 'USA'
                        division_exposure = '?'
                        try:
                            length = str(len(sequences[strain]))
                        except:
                            length = str(len(sequences[id]))
                        host = row['Host*']
                        originating_lab = row['Source*']
                        submitting_lab = 'Grubaugh Lab - Yale School of Public Health'
                        authors = 'Fauver et al'
                        url = '?'
                        update = 'Update' + str('0' * (2 - len(row['Update*']))) + row['Update*']
                        if update == 'Update00':
                            update = 'Initial'

                        lValues = [strain, gisaid_epi_isl, genbank_accession, date, iso, country, division,
                                   location, region_exposure, country_exposure, division_exposure, length, host, originating_lab,
                                   submitting_lab, authors, url, update]

                        header = '|'.join([strain, country, division.replace(' ', '-'), date])
                        dHeaders[strain] = header

                        for field, value in zip(fields.keys(), lValues):
                            fields[field] = value
                        dRow[id] = fields
                        found.append(strain)
                        if id in lab_label.keys():
                            lab_label[id] = strain
                    else:
                        continue
            # print(dRow)
            else: # Assign 'NA' if no metadata is available
                header = '|'.join([id, 'NA', 'NA', 'NA', 'NA'])
                dHeaders[id] = header
                notFound.append(id)
        lstNewMetadata = lstNewMetadata + list(dRow.values())

    # write new metadata files
    outputDF = pd.DataFrame(lstNewMetadata)
    outputDF.to_csv(output1, sep='\t', index=False)

    # write renaming file
    with open(output2, 'w') as outfile2:
        # export new metadata lines
        for id, header in dHeaders.items():
            # print(id)
            outfile2.write(id + '\t' + header + '\n')
        for id in notFound:
            print('\t* Warning! No metadata found for ' + id)

        if len(notFound) > 0:
            print('\nPlease check for inconsistencies (see above).')

    # write renaming file
    exported = []
    with open(output3, 'w') as outfile3:
        # export new metadata lines
        for id, sequence in sequences.items():
            if '/' not in id:
                if lab_label[id] not in exported:
                    entry = '>' + lab_label[id] + '\n' + sequence + '\n'
                    outfile3.write(entry)
                    print('* Exporting newly sequenced genome and metadata for ' + id)
                    exported.append(lab_label[id])
                    # print(lab_label[id])

            else:
                if id not in exported:
                    entry = '>' + id + '\n' + sequence + '\n'
                    outfile3.write(entry)
                    exported.append(id)
                    # print(id)



print('\nMetadata file successfully reformatted and exported!\n')
