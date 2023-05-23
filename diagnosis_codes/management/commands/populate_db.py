import logging
import os
from os.path import abspath, dirname

import pandas as pd  # Use polars library is faster than pandas library
from django.core.management.base import BaseCommand

from diagnosis_codes.utils import create_diagnoses, create_diagnosis_categories

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Uploads diagnosis ICD codes from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('version', type=str, help='The version of the ICD CSV file to upload')


    def handle(self, *args, **options):
        version = options['version']
        try:
            project_root  = dirname(dirname(dirname(abspath(__file__) )))
            logger.info(f'{project_root} project root')
            data_directory  =  os.path.join(project_root , 'data')
            logger.info(f'{data_directory} data directory')

            # load data csv's
            category_data  =  os.path.join(data_directory , 'categories.csv')
            logger.info(f'{category_data} category data')

            diagnosis_data  =  os.path.join(data_directory, 'codes.csv' )
            logger.info(f'{diagnosis_data} diagnosis data')

            #  Load csv data into a dataframe
            category_data_df  =  pd.read_csv(category_data , header=None , names= ['code' , 'description'])
            #  populate DB
            category_data_df  = create_diagnosis_categories(category_data_df)


            names  = ['category' , 'code' , 'full_code', 'abbreviated_description' , 'full_description', 'category_title']
            diagnosis_test_df  = pd.read_csv(diagnosis_data , header=None , names= names)
            diagnosis_test_df = create_diagnoses(diagnosis_test_df, version)

            logging.info(f'Done loading diagnosis data')
        except Exception as e:
            logger.error(e)
            raise e
