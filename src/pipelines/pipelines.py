import pandas as pd


class WeeklyDataPipeline:
    """
    Pipeline dedicated to generating and cleaning the CSV data sourced from the MCL interface.
    """

    def readData(filename: str = "data/external/mcl_raw_data.csv"):
        """
        Reads the updated Medtronic CareLink data export.
        Header set to 4 to offset the other headers on the file.
        """
        return pd.read_csv(filename, header=4)

    def sectionalizeData(df: pd.DataFrame = readData) -> dict:
        """
        Slices a dataframe into 3 smaller DataFrames by index

        ## Parameters
        `df` pd.DataFrame:
            DataFrame produced by the readData() call.

        ## Returns
        `ret_dict` dict:
            dictionary of sliced DataFrames indexed by chunk.
        """
        ret_dict = {}
        arr = df[df["Index"] == "Index"].index.values.astype(int)

        # General Data and settings
        ret_dict["chunk1"] = df.iloc[0 : arr[0] - 1]
        # Carb and Insulin data
        ret_dict["chunk2"] = df.iloc[arr[0] + 1 : arr[1] - 2]
        # ISIG and Glucose data
        ret_dict["chunk3"] = df.iloc[arr[1] + 1 : len(df) - 1]

        del df
        return ret_dict

    def scrubFeatures(chunk_dict: dict = sectionalizeData):
        """
        Removes unnecessary columns from chunks.

        ## Parameters
        `chunk_dict`: dict
            dictionary of chunks post-slicing

        ## Returns
        `chunk_dict: dict
            Dictionary of DataFrames with the appropriate features removed.
        """
        # Chunk 1
        chunk_dict["chunk1"] = chunk_dict["chunk1"][
            ["Index", "Date", "Time", "Bolus Volume Delivered (U)", "Basal Rate (U/h)"]
        ]

        # Chunk2
        chunk_dict["chunk2"] = None

        # Chunk3
        chunk_dict["chunk3"] = chunk_dict["chunk3"][
            ["Index", "Date", "Time", "Sensor Glucose (mg/dL)"]
        ]

        return chunk_dict

    def pipe():
        """
        Placeholder Pipeline function.
        """
        print()
        pass
