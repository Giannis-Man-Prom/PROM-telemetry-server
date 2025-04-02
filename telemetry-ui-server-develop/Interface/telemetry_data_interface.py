from pandas import DataFrame
from flask import jsonify
from typing import Union

'''
Δεν χρειάζεται στο app.py
'''

class TelemetryDataInterface:
    def __init__(self, df: DataFrame):
        """
        Initializes the TelemetryDataInterface with a DataFrame.

        Args:
            df (DataFrame): The DataFrame containing telemetry data.
        """
        self.df = df

    def dataframe_to_json(self) -> Union[str, jsonify]:
        """
        Converts the DataFrame to JSON format.

        Returns:
            Union[str, jsonify]: The JSON representation of the DataFrame or an error message in JSON format.
        """
        pass  # Implement this method in the subclass

    def get_column(self, index: int) -> Union[str, jsonify]:
        """
        Retrieves a column from the DataFrame based on the provided index.

        Args:
            index (int): The index of the column to retrieve.

        Returns:
            Union[str, jsonify]: The JSON representation of the column data or an error message in JSON format.
        """
        pass  # Implement this method in the subclass

    def process_data(self):
        """
        Processes the telemetry data.
        """
        pass  # Implement this method in the subclass