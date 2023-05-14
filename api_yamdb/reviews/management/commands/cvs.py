# Import the necessary modules
from django.core.management.base import BaseCommand
from django.db.models import AutoField
import csv
import logging
from reviews.models import Category, Genre, Title, Review, Comment

# Define a helper module to store some functions for importing csv data
from ._csv_tools import get_model_fields, get_csv_file_name, get_csv_data

# Define a dictionary to map the models to their csv files
models_to_files = {
    "Genre": "genre.csv",
    "Category": "category.csv",
    "Title": "titles.csv",
    "Review": "review.csv",
    "Comment": "comments.csv",
}


# Define a custom management command class
class Command(BaseCommand):
    # Define a help attribute to describe the command
    help = "Populates the database from csv files"

    # Define a handle method to execute the command logic
    def handle(self, *args, **options):
        # Loop over the models and their csv files in the dictionary
        for model, file in models_to_files.items():
            # Get the model class from the model name
            model_class = globals()[model]
            # Get the model fields, excluding the auto id field
            model_fields = get_model_fields(model_class)
            # Get the csv file name from the file name
            csv_file_name = get_csv_file_name(file)
            # Get the csv data from the csv file name
            csv_data = get_csv_data(csv_file_name)
            # Create a logger object to report the progress and results of the command
            logger = logging.getLogger(__name__)
            # Log a message to indicate the start of the import process for the model
            logger.info(f"Starting to import data for {model} model")
            # Initialize a counter variable to keep track of the number of records imported
            counter = 0
            # Loop over the rows in the csv data
            for row in csv_data:
                # Initialize an empty dictionary to store the field-value pairs for creating a model instance
                insert_dict = {}
                # Loop over the model fields and their corresponding values in the row
                for field, value in zip(model_fields, row):
                    # Add the field-value pair to the insert dictionary
                    insert_dict[field] = value
                # Try to create a model instance with the insert dictionary using get_or_create method
                try:
                    _, created = model_class.objects.get_or_create(
                        **insert_dict
                    )
                    # If a new instance is created, increment the counter and log a message
                    if created:
                        counter += 1
                        logger.info(
                            f"Created {model} instance with {insert_dict}"
                        )
                # If an error occurs, log an error message and continue with the next row
                except Exception as e:
                    logger.error(
                        f"Failed to create {model} instance with {insert_dict}: {e}"
                    )
                    continue
            # Log a message to indicate the end of the import process for the model and report the number of records imported
            logger.info(
                f"Finished importing data for {model} model. Imported {counter} records."
            )
