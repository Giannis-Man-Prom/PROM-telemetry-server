from pandas import DataFrame
from flask import Flask, jsonify
class telemetry_data_class:
    def __init__(self, df: DataFrame):
        #Απλά αποθηκεύουμε μέσα στο object τα δεδομένα με τα οποία αρχικοποιείται
        self.df = df

    def dataframe_to_json(self):
        try:
            # Read CSV file into DataFrame
            if self.df is not None:
                # Convert DataFrame to JSON and return
                df_json = self.df.to_json(orient='records')
                return jsonify(df_json)
            else:
                return jsonify({"error": "CSV file is None"})
        except Exception as e:
            print(f"Error converting DataFrame to JSON: {str(e)}")
            return jsonify({"error": "Failed to convert DataFrame to JSON"})

    #Εδώ παίρνουμε όλα τα columns του dataframe σε list
    def get_cols_all(self):
        try:
            return self.df.columns.tolist()

        except Exception as e:
            return f"There was an error fetching the columns: {e}"

    #Εδώ παίρνουμε δύο columns τύπου pandas dataframe και κάνουμε τα δεδομένα τους lists
    def get_two_cols(self, col_1, col_2):

        try:

            if col_1 and col_2 is not None:
                #Το return είναι dict με col_1 και col_2
                return {
                    "col_1": self.df.loc[:, col_1].values.tolist(),
                    "col_2": self.df.loc[:, col_2].values.tolist()
                }
        except Exception as e:
            return f"There was a problem fetching the columns"







