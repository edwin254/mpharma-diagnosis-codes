import logging

import pandas as pd

from .models import Diagnosis, DiagnosisCategory

logger = logging.getLogger(__name__)

def clean_diagnosis_data(data):
    """
    Cleans the diagnosis data.

    Args:
        data (pandas.DataFrame): The diagnosis data.

    Returns:
        pandas.DataFrame: The cleaned diagnosis data.
    """

    # drop duplicates
    data = data.drop_duplicates()

    # drop rows with missing values
    data = data.dropna()

    # drop rows with null values
    data = data.dropna(axis=0)

    return data

def create_diagnosis_categories(data):
    """
    Creates the diagnosis categories.

    Args:
        data (pandas.DataFrame): The diagnosis data.

    Returns:
        pandas.DataFrame: The cleaned diagnosis data.
    """

    # clean diagnosis data
    clean_df = clean_diagnosis_data(data=data)

    # create diagnosis categories
    try:
        categories = []
        for i in range(len(data)):
            categories.append(DiagnosisCategory(
                code=data.iloc[i]['code'],
                description=data.iloc[i]['description']
            ))

        DiagnosisCategory.objects.bulk_create(categories)
        logger.info(f' {len(categories)} Diagnosis categories created.')
    except Exception as e:
        logger.error(e)


def create_diagnoses(data, version):
    """
    Creates the diagnoses.

    Args:
        data (pandas.DataFrame): The diagnosis data.

    Returns:
        pandas.DataFrame: The cleaned diagnosis data.
    """

    # clean diagnosis data
    clean_df = clean_diagnosis_data(data=data)
    diagnosis_df = clean_df[['category', 'code', 'full_code', 'abbreviated_description', 'full_description']]

    # create diagnoses
    try:
        diagnoses = []
        for i in range(len(clean_df)):
            category = DiagnosisCategory.objects.get_or_create(code=diagnosis_df.iloc[i]['category'])
            diagnoses.append(Diagnosis(
                icd_version=version,
                category=category,
                code=clean_df.iloc[i]['code'],
                full_code=clean_df.iloc[i]['full_code'],
                abbreviated_description=clean_df.iloc[i]['abbreviated_description'],
                full_description=clean_df.iloc[i]['full_description'],
                )
            )

        Diagnosis.objects.bulk_create(diagnoses)
        logger.info(f' {len(diagnoses)} Diagnoses created.')

    except Exception as e:
        logger.error(e)