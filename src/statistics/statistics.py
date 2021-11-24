import pandas as pd
from datetime import date


class Stats:
    """
    Singleton class to house all of the stat card values.
    """

    def __init__(self, dict, lower, upper) -> None:
        self.tir = Stats.getTimeInRange(lower, upper)
        self.timeHigh = Stats.getTimeHigh()
        self.timeLow = Stats.getTimeLow()
        self.avgBG = Stats.getAvgBG()
        self.highestDay = Stats.getHighestDay()
        self.lowestDay = Stats.getLowestDay()
        self.longestStint = Stats.getLongestStint()
        self.carbsConsumed = Stats.getCarbsConsumed()
        self.bolusTotal = Stats.getBolusTotal()
        pass

    def updateAll(low_bound: int, high_bound: int) -> bool:
        """
        Updates all statistics based on input.
        """
        pass

    def getTimeInRange(df: pd.DataFrame, low_bound: int, high_bound: int) -> str:
        """
        Calculates percent of time in range based on user bounds
        """
        temp = df["Sensor Glucose (mg/dL)"].fillna(
            df["Sensor Glucose (mg/dL)"].median()
        )
        count = temp.between(low_bound, high_bound, inclusive="both").value_counts()[
            True
        ]
        percent = int(round(count / len(temp), 2) * 100)
        return str(percent) + "%"

    def getTimeHigh(df: pd.DataFrame, high_bound: int) -> str:
        """
        Calculates percent of time high based on upper bound
        """
        temp = df["Sensor Glucose (mg/dL)"].fillna(
            df["Sensor Glucose (mg/dL)"].median()
        )
        temp = temp > high_bound
        count = temp.value_counts()[True]
        percent = int(round(count / len(temp), 2) * 100)
        return str(percent) + "%"

    def getTimeLow(df: pd.DataFrame, low_bound: int) -> str:
        """
        Calculates percent of time low based on lower bound
        """
        temp = df["Sensor Glucose (mg/dL)"].fillna(
            df["Sensor Glucose (mg/dL)"].median()
        )
        temp = temp < low_bound
        count = temp.value_counts()[True]
        percent = int(round(count / len(temp), 2) * 100)
        return str(percent) + "%"

    def getAvgBG(df: pd.DataFrame) -> str:
        """
        Calculates average Blood sugar through all of the data
        """
        average = df["Sensor Glucose (mg/dL)"].mean().astype("int32")
        return str(average) + "mg/dL"

    def getHighestDay(df: pd.DataFrame) -> str:
        """
        Calculates and returns the day with the highest average blood sugar.
        """
        # Need to exclude today
        days = df["Date"].unique()
        ret_dict = {"Date": None, "Value": 0}

        for day in days:
            # If date is today's date then skip it due to possibility of incomplete data
            if pd.Timestamp(day) == pd.Timestamp(date.today()):
                break

            found_value = (
                df.loc[df["Date"] == pd.Timestamp(day)]["Sensor Glucose (mg/dL)"].mean()
            ).astype("int")

            found_value = found_value.item()

            if found_value > ret_dict["Value"]:
                ret_dict["Date"] = pd.Timestamp(day).strftime("%A %m-%d")
                ret_dict["Value"] = found_value

        return ret_dict["Date"] + " " + str(ret_dict["Value"])

    def getLowestDay(df: pd.DataFrame) -> str:
        """
        Calculates and returns the day with the lowest average blood sugar.
        """
        # Need to exclude today
        days = df["Date"].unique()
        ret_dict = {"Date": None, "Value": 500}

        for day in days:
            # If date is today's date then skip it due to possibility of incomplete data
            if pd.Timestamp(day) == pd.Timestamp(date.today()):
                break

            found_value = (
                df.loc[df["Date"] == pd.Timestamp(day)]["Sensor Glucose (mg/dL)"].mean()
            ).astype("int")

            found_value = found_value.item()

            if found_value < ret_dict["Value"]:
                ret_dict["Date"] = pd.Timestamp(day).strftime("%A %m-%d")
                ret_dict["Value"] = found_value

        return ret_dict["Date"] + " " + str(ret_dict["Value"])

    def getLongestStint(df: pd.DataFrame, lower_bound: int, upper_bound: int) -> str:
        """
        Finds the longest duration of hours that sensor perceived a blood sugar value in range.
        (Excludes any NaN values.)
        """

        sorted_df = df.sort_values(["Date", "Time"], ascending=(True, True))
        sorted_df = sorted_df.dropna(axis=0)

        duration = None
        # Set the initial start time
        start = pd.Timestamp.combine(sorted_df.iloc[0, 1], sorted_df.iloc[0, 2])

        for index, row in df.iterrows():
            if (row["Sensor Glucose (mg/dL)"] >= lower_bound) and (
                row["Sensor Glucose (mg/dL)"] <= upper_bound
            ):
                continue
            else:
                stop = pd.Timestamp.combine(row["Date"], row["Time"])
                duration = pd.to_timedelta(stop - start, unit="hours")
                print(duration)
                start = stop

        # do string formatting on duration before exiting
        return duration.components

    def getCarbsConsumed(df: pd.DataFrame) -> str:
        """ """
        total = df["BWZ Carb Input (grams)"].sum().item()
        return str(total) + "g"

    def getBolusTotal(df: pd.DataFrame) -> str:
        """ """
        total = int(df["Bolus Volume Delivered (U)"].sum())
        return str(total) + "U"
