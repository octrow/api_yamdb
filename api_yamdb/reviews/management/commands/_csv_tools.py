# Import the necessary modules
from django.db.models import AutoField
import csv
import os


# Define a function to get the model fields, excluding the auto id field
def get_model_fields(model_class):
    # Get all the fields from the model class
    all_fields = model_class._meta.fields
    # Filter out the auto id field using isinstance function
    model_fields = [
        f.attname for f in all_fields if not isinstance(f, AutoField)
    ]
    # Return the model fields as a list
    return model_fields


# Define a function to get the csv file name from the file name
def get_csv_file_name(file_name):
    # Get the current directory path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Get the parent directory path
    parent_dir = os.path.dirname(current_dir)
    # Get the data directory path by joining the parent directory and the data folder name
    data_dir = os.path.join(parent_dir, "/static/data")
    # Get the csv file name by joining the data directory and the file name
    csv_file_name = os.path.join(data_dir, file_name)
    # Return the csv file name as a string
    return csv_file_name


# Define a function to get the csv data from the csv file name
def get_csv_data(csv_file_name):
    # Open the csv file in read mode
    with open(csv_file_name, "r") as f:
        # Create a csv reader object from the file object
        reader = csv.reader(f)
        # Skip the header row
        next(reader)
        # Return the csv data as a list of lists
        return list(reader)
