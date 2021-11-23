import pandas as pd


class WeeklyDataPipeline:
    """
    Pipeline dedicated to generating and cleaning the CSV data sourced from the MCL interface.

    WeeklyDataPipeline.pipe() performs the following methods in order:
    Proc 1: readData
    Proc 2: sectionalizeData
    Proc 3: scrubFeatures
    Proc 4: castFeatures
    """

    def readData(filename: str = "data/raw/raw_data.csv") -> pd.DataFrame:
        """
        Reads the updated Medtronic CareLink data export.
        Header set to 4 to offset the other headers on the file.
        """
        return pd.read_csv(filename, header=4)

    def sectionalizeData(df: pd.DataFrame) -> dict:
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

    def scrubFeatures(chunk_dict: dict) -> dict:
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

        # Chunk2 -- removed for space saving, currently does not have a use. (may change in future)
        del chunk_dict["chunk2"]

        # Chunk3
        chunk_dict["chunk3"] = chunk_dict["chunk3"][
            ["Index", "Date", "Time", "Sensor Glucose (mg/dL)"]
        ]

        return chunk_dict

    def castFeatures(chunk_dict: dict) -> dict:
        """
        Casts to appropriate type and re-sorts data.

        ## Parameters:
        `chunk_dict`: dict
            dictionary of chunks post-feature scrubbing

        ## Returns:
        `chunk_dict: dict
            Dictionary of DataFrames with features casted and re-sorted.
        """
        # Converting the Index, Date, and Time for chunks 1 and 3
        for _ in ["chunk1", "chunk3"]:
            chunk_dict[_]["Index"] = chunk_dict[_]["Index"].astype("float32")
            chunk_dict[_]["Date"] = pd.to_datetime(chunk_dict[_]["Date"])
            chunk_dict[_]["Time"] = pd.to_datetime(chunk_dict[_]["Time"]).apply(
                lambda x: x.time()
            )

        for _ in ["Bolus Volume Delivered (U)", "Basal Rate (U/h)"]:
            chunk_dict["chunk1"][_] = chunk_dict["chunk1"][_].astype("float32")

        # Chunk2 -- Nothing to do as of now

        # Chunk3 --
        chunk_dict["chunk3"]["Sensor Glucose (mg/dL)"] = chunk_dict["chunk3"][
            "Sensor Glucose (mg/dL)"
        ].astype("float32")

        return chunk_dict

    def pipe():
        """
        Placeholder Pipeline function.
        """
        raw_data = WeeklyDataPipeline.readData()
        data_dict = WeeklyDataPipeline.sectionalizeData(raw_data)
        data_dict = WeeklyDataPipeline.scrubFeatures(data_dict)
        data_dict = WeeklyDataPipeline.castFeatures(data_dict)
        return data_dict
