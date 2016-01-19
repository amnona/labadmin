from collections import defaultdict
survey_type = {
    1: "Human",
    2: "Animal"
}

# Columns to remove for EBI or other public submissions of metadata
ebi_remove = ['ABOUT_YOURSELF_TEXT', 'ANTIBIOTIC_CONDITION', 'ANTIBIOTIC_MED',
              'BIRTH_MONTH', 'CAT_CONTACT', 'CAT_LOCATION',
              'CONDITIONS_MEDICATION', 'DIET_RESTRICTIONS_LIST', 'DOG_CONTACT',
              'DOG_LOCATION', 'GENDER', 'MEDICATION_LIST',
              'OTHER_CONDITIONS_LIST', 'PREGNANT_DUE_DATE', 'RACE_OTHER',
              'RELATIONSHIPS_WITH_OTHERS_IN_STUDY', 'SPECIAL_RESTRICTIONS',
              'SUPPLEMENTS', 'TRAVEL_LOCATIONS_LIST', 'ZIP_CODE',
              'WILLING_TO_BE_CONTACTED']
# standard fields that are set based on sampling site
md_lookup = {
    'Hair':
        {'BODY_PRODUCT': 'UBERON:sebum',
         'COMMON_NAME': 'human skin metagenome',
         'SAMPLE_TYPE': 'Hair',
         'SCIENTIFIC_NAME': 'Homo sapiens sapiens',
         'TAXON_ID': '539655',
         'BODY_HABITAT': 'UBERON:hair',
         'ENV_MATTER': 'ENVO:sebum',
         'DESCRIPTION': 'American Gut Project Hair sample',
         'BODY_SITE': 'UBERON:hair'},
    'Nares': {
        'BODY_PRODUCT': 'UBERON:mucus',
        'COMMON_NAME': 'human nasal/pharyngeal metagenome',
        'SAMPLE_TYPE': 'Nares',
        'SCIENTIFIC_NAME': 'Homo sapiens sapiens',
        'TAXON_ID': '1131769',
        'BODY_HABITAT': 'UBERON:nose',
        'ENV_MATTER': 'ENVO:mucus',
        'DESCRIPTION': 'American Gut Project Nares sample',
        'BODY_SITE': 'UBERON:nostril'},
    'Vaginal mucus': {
        'BODY_PRODUCT': 'UBERON:mucus',
        'COMMON_NAME': 'vaginal metagenome',
        'SAMPLE_TYPE': 'Vaginal mucus',
        'SCIENTIFIC_NAME': 'Homo sapiens sapiens',
        'TAXON_ID': '1549736',
        'BODY_HABITAT': 'UBERON:vagina',
        'ENV_MATTER': 'ENVO:mucus',
        'DESCRIPTION': 'American Gut Project Vaginal mucus sample',
        'BODY_SITE': 'UBERON:vaginal introitus'},
    'Sole of foot': {
        'BODY_PRODUCT': 'UBERON:sebum',
        'COMMON_NAME': 'human skin metagenome',
        'SAMPLE_TYPE': 'Sole of foot',
        'SCIENTIFIC_NAME': 'Homo sapiens sapiens',
        'TAXON_ID': '539655',
        'BODY_HABITAT': 'UBERON:skin',
        'ENV_MATTER': 'ENVO:sebum',
        'DESCRIPTION': 'American Gut Project Sole of foot sample',
        'BODY_SITE': 'UBERON:skin of foot'},
    'Nasal mucus': {
        'BODY_PRODUCT': 'UBERON:mucus',
        'COMMON_NAME': 'human nasal/pharyngeal metagenome',
        'SAMPLE_TYPE': 'Nasal mucus',
        'SCIENTIFIC_NAME': 'Homo sapiens sapiens',
        'TAXON_ID': '1131769',
        'BODY_HABITAT': 'UBERON:nose',
        'ENV_MATTER': 'ENVO:mucus',
        'DESCRIPTION': 'American Gut Project Nasal mucus sample',
        'BODY_SITE': 'UBERON:nostril'},
    'Stool': {
        'BODY_PRODUCT': 'UBERON:feces',
        'COMMON_NAME': 'human gut metagenome',
        'SAMPLE_TYPE': 'Stool',
        'SCIENTIFIC_NAME': 'Homo sapiens sapiens',
        'TAXON_ID': '408170',
        'BODY_HABITAT': 'UBERON:feces',
        'ENV_MATTER': 'ENVO:feces',
        'DESCRIPTION': 'American Gut Project Stool sample',
        'BODY_SITE': 'UBERON:feces'},
    'Forehead': {
        'BODY_PRODUCT': 'UBERON:sebum',
        'COMMON_NAME': 'human skin metagenome',
        'SAMPLE_TYPE': 'Forehead',
        'SCIENTIFIC_NAME': 'Homo sapiens sapiens',
        'TAXON_ID': '539655',
        'BODY_HABITAT': 'UBERON:skin',
        'ENV_MATTER': 'ENVO:sebum',
        'DESCRIPTION': 'American Gut Project Forehead sample',
        'BODY_SITE': 'UBERON:skin of head'},
    'Tears': {
        'BODY_PRODUCT': 'UBERON:tears',
        'COMMON_NAME': 'human metagenome',
        'SAMPLE_TYPE': 'Tears',
        'SCIENTIFIC_NAME': 'Homo sapiens sapiens',
        'TAXON_ID': '646099',
        'BODY_HABITAT': 'UBERON:eye',
        'ENV_MATTER': 'ENVO:tears',
        'DESCRIPTION': 'American Gut Project Tears sample',
        'BODY_SITE': 'UBERON:eye'},
    'Right hand': {
        'BODY_PRODUCT': 'UBERON:sebum',
        'COMMON_NAME': 'human skin metagenome',
        'SAMPLE_TYPE': 'Right Hand',
        'SCIENTIFIC_NAME': 'Homo sapiens sapiens',
        'TAXON_ID': '539655',
        'BODY_HABITAT': 'UBERON:skin',
        'ENV_MATTER': 'ENVO:sebum',
        'DESCRIPTION': 'American Gut Project Right Hand sample',
        'BODY_SITE': 'UBERON:skin of hand'},
    'Mouth': {
        'BODY_PRODUCT': 'UBERON:saliva',
        'COMMON_NAME': 'human oral metagenome',
        'SAMPLE_TYPE': 'Mouth',
        'SCIENTIFIC_NAME': 'Homo sapiens sapiens',
        'TAXON_ID': '447426',
        'BODY_HABITAT': 'UBERON:oral cavity',
        'ENV_MATTER': 'ENVO:saliva',
        'DESCRIPTION': 'American Gut Project Mouth sample',
        'BODY_SITE': 'UBERON:tongue'},
    'Left hand': {
        'BODY_PRODUCT': 'UBERON:sebum',
        'COMMON_NAME': 'human skin metagenome',
        'SAMPLE_TYPE': 'Left Hand',
        'SCIENTIFIC_NAME': 'Homo sapiens sapiens',
        'TAXON_ID': '539655',
        'BODY_HABITAT': 'UBERON:skin',
        'ENV_MATTER': 'ENVO:sebum',
        'DESCRIPTION': 'American Gut Project Left Hand sample',
        'BODY_SITE': 'UBERON:skin of hand'},
    'Ear wax': {
        'BODY_PRODUCT': 'UBERON:ear wax',
        'COMMON_NAME': 'human metagenome',
        'SAMPLE_TYPE': 'Ear wax',
        'SCIENTIFIC_NAME': 'Homo sapiens sapiens',
        'TAXON_ID': '646099',
        'BODY_HABITAT': 'UBERON:ear',
        'ENV_MATTER': 'ENVO:ear wax',
        'DESCRIPTION': 'American Gut Project Ear wax sample',
        'BODY_SITE': 'UBERON:external auditory meatus'}
}

month_int_lookup = {'January': 1, 'February': 2, 'March': 3,
                    'April': 4, 'May': 5, 'June': 6,
                    'July': 7, 'August': 8, 'September': 9,
                    'October': 10, 'November': 11, 'December': 12}

month_str_lookup = {1: 'January', 2: 'February', 3: 'March',
                    4: 'April', 5: 'May', 6: 'June',
                    7: 'July', 8: 'August', 9: 'September',
                    10: 'October', 11: 'November', 12: 'December'}

season_lookup = {None: 'Unspecified',
                 1: 'Winter',
                 2: 'Winter',
                 3: 'Spring',
                 4: 'Spring',
                 5: 'Spring',
                 6: 'Summer',
                 7: 'Summer',
                 8: 'Summer',
                 9: 'Fall',
                 10: 'Fall',
                 11: 'Fall',
                 12: 'Winter'}

# The next two dictionaries are adapted from information presented in
#       Wikipedia. "List of regions of the United States". updated 7 June 2014,
#           accessed 7 June 2014.
#           http://en.wikipedia.org/wiki/List_of_regions_of_the_United_States

regions_by_state = {None: {'Census_1': 'Unspecified',
                           'Census_2': 'Unspecified',
                           'Economic': 'Unspecified'},
                    'AK': {'Census_1': 'West',
                           'Census_2': 'Pacific',
                           'Economic': 'Far West'},
                    'AL': {'Census_1': 'South',
                           'Census_2': 'East South Central',
                           'Economic': 'Southeast'},
                    'AR': {'Census_1': 'South',
                           'Census_2': 'West South Central',
                           'Economic': 'Southeast'},
                    'AZ': {'Census_1': 'West',
                           'Census_2': 'Mountain',
                           'Economic': 'Southwest'},
                    'CA': {'Census_1': 'West',
                           'Census_2': 'Pacific',
                           'Economic': 'Far West'},
                    'CO': {'Census_1': 'West',
                           'Census_2': 'Mountain',
                           'Economic': 'Rocky Mountain'},
                    'CT': {'Census_1': 'Northeast',
                           'Census_2': 'New England',
                           'Economic': 'New England'},
                    'DC': {'Census_1': 'South',
                           'Census_2': 'South Atlantic',
                           'Economic': 'Mideast'},
                    'DE': {'Census_1': 'Northeast',
                           'Census_2': 'Mid-Atlantic',
                           'Economic': 'Mideast'},
                    'FL': {'Census_1': 'South',
                           'Census_2': 'South Atlantic',
                           'Economic': 'Southeast'},
                    'GA': {'Census_1': 'South',
                           'Census_2': 'South Atlantic',
                           'Economic': 'Southeast'},
                    'HI': {'Census_1': 'West',
                           'Census_2': 'Pacific',
                           'Economic': 'Far West'},
                    'IA': {'Census_1': 'Midwest',
                           'Census_2': 'West North Central',
                           'Economic': 'Plains'},
                    'ID': {'Census_1': 'West',
                           'Census_2': 'Mountain',
                           'Economic': 'Rocky Mountain'},
                    'IL': {'Census_1': 'Midwest',
                           'Census_2': 'East North Central',
                           'Economic': 'Great Lakes'},
                    'IN': {'Census_1': 'Midwest',
                           'Census_2': 'East North Central',
                           'Economic': 'Great Lakes'},
                    'KS': {'Census_1': 'Midwest',
                           'Census_2': 'West North Central',
                           'Economic': 'Plains'},
                    'KY': {'Census_1': 'South',
                           'Census_2': 'East South Central',
                           'Economic': 'Southeast'},
                    'LA': {'Census_1': 'South',
                           'Census_2': 'West South Central',
                           'Economic': 'Southeast'},
                    'MA': {'Census_1': 'Northeast',
                           'Census_2': 'New England',
                           'Economic': 'New England'},
                    'MD': {'Census_1': 'South',
                           'Census_2': 'South Atlantic',
                           'Economic': 'Mideast'},
                    'ME': {'Census_1': 'Northeast',
                           'Census_2': 'New England',
                           'Economic': 'New England'},
                    'MI': {'Census_1': 'Midwest',
                           'Census_2': 'East North Central',
                           'Economic': 'Great Lakes'},
                    'MN': {'Census_1': 'Midwest',
                           'Census_2': 'West North Central',
                           'Economic': 'Plains'},
                    'MO': {'Census_1': 'Midwest',
                           'Census_2': 'West North Central',
                           'Economic': 'Plains'},
                    'MS': {'Census_1': 'South',
                           'Census_2': 'East South Central',
                           'Economic': 'Southeast'},
                    'MT': {'Census_1': 'West',
                           'Census_2': 'Mountain',
                           'Economic': 'Rocky Mountain'},
                    'NC': {'Census_1': 'South',
                           'Census_2': 'South Atlantic',
                           'Economic': 'Southeast'},
                    'ND': {'Census_1': 'Midwest',
                           'Census_2': 'West North Central',
                           'Economic': 'Plains'},
                    'NE': {'Census_1': 'Midwest',
                           'Census_2': 'West North Central',
                           'Economic': 'Plains'},
                    'NH': {'Census_1': 'Northeast',
                           'Census_2': 'New England',
                           'Economic': 'New England'},
                    'NJ': {'Census_1': 'Northeast',
                           'Census_2': 'Mid-Atlantic',
                           'Economic': 'Mideast'},
                    'NM': {'Census_1': 'West',
                           'Census_2': 'Mountain',
                           'Economic': 'Southwest'},
                    'NV': {'Census_1': 'West',
                           'Census_2': 'Mountain',
                           'Economic': 'Far West'},
                    'NY': {'Census_1': 'Northeast',
                           'Census_2': 'Mid-Atlantic',
                           'Economic': 'Mideast'},
                    'OH': {'Census_1': 'Midwest',
                           'Census_2': 'East North Central',
                           'Economic': 'Great Lakes'},
                    'OK': {'Census_1': 'South',
                           'Census_2': 'West South Central',
                           'Economic': 'Southwest'},
                    'OR': {'Census_1': 'West',
                           'Census_2': 'Pacific',
                           'Economic': 'Far West'},
                    'PA': {'Census_1': 'Northeast',
                           'Census_2': 'Mid-Atlantic',
                           'Economic': 'Mideast'},
                    'PR': {'Census_1': 'Territories',
                           'Census_2': 'Territories',
                           'Economic': 'Territories'},
                    'RI': {'Census_1': 'Northeast',
                           'Census_2': 'New England',
                           'Economic': 'New England'},
                    'SC': {'Census_1': 'South',
                           'Census_2': 'South Atlantic',
                           'Economic': 'Southeast'},
                    'SD': {'Census_1': 'Midwest',
                           'Census_2': 'West North Central',
                           'Economic': 'Plains'},
                    'TN': {'Census_1': 'South',
                           'Census_2': 'East South Central',
                           'Economic': 'Southeast'},
                    'TX': {'Census_1': 'South',
                           'Census_2': 'West South Central',
                           'Economic': 'Southwest'},
                    'UT': {'Census_1': 'West',
                           'Census_2': 'Mountain',
                           'Economic': 'Rocky Mountain'},
                    'VA': {'Census_1': 'South',
                           'Census_2': 'South Atlantic',
                           'Economic': 'Southeast'},
                    'VI': {'Census_1': 'Territories',
                           'Census_2': 'Territories',
                           'Economic': 'Territories'},
                    'VT': {'Census_1': 'Northeast',
                           'Census_2': 'New England',
                           'Economic': 'New England'},
                    'WA': {'Census_1': 'West',
                           'Census_2': 'Pacific',
                           'Economic': 'Far West'},
                    'WI': {'Census_1': 'Midwest',
                           'Census_2': 'East North Central',
                           'Economic': 'Great Lakes'},
                    'WV': {'Census_1': 'South',
                           'Census_2': 'South Atlantic',
                           'Economic': 'Southeast'},
                    'WY': {'Census_1': 'West',
                           'Census_2': 'Mountain',
                           'Economic': 'Rocky Mountain'}}


def default_blank():
    return 'Unspecified'

blanks_values = defaultdict(default_blank,
                            ALTITUDE='0',
                            ASSIGNED_FROM_GEO="No",
                            COMMON_NAME="unclassified metagenome",
                            COUNTRY="USA",
                            ELEVATION='193.0',
                            ENV_BIOME="ENVO:aquatic biome",
                            ENV_FEATURE="ENVO:water",
                            ENV_MATTER="ENVO:sterile water",
                            TAXON_ID='408169',
                            HOST_TAXID='408169',
                            LATITUDE='32.8',
                            LONGITUDE='-117.2',
                            PUBLIC='Yes',
                            SAMPLE_TYPE='control blank',
                            SCIENTIFIC_NAME='unclassified metagenome',
                            STATE='CA',
                            TITLE='American Gut Project',
                            DNA_EXTRACTED='Yes',
                            HAS_PHYSICAL_SPECIMEN='Yes',
                            PHYSICAL_SPECIMEN_LOCATION='UCSDMI',
                            PHYSICAL_SPECIMEN_REMAINING='Yes',
                            REQUIRED_SAMPLE_INFO_STATUS='completed',
                            DESCRIPTION='American Gut control',
                            SUBSET_AGE=str(False),
                            SUBSET_DIABETES=str(False),
                            SUBSET_IBD=str(False),
                            SUBSET_ANTIBIOTIC_HISTORY=str(False),
                            SUBSET_BMI=str(False),
                            SUBSET_HEALTHY=str(False))
