import pandas as pd
from datetime import date


class Stats:
    """
    Class to house and update all of the stat card values.
    """

    def __init__(
        self, cleaned_dict: dict, low_bound: int, high_bound: int, basal_rate: float
    ) -> None:
        # TODO: Change these to setX methods.
        if cleaned_dict == None:
            self.tir = "NaN"
            self.timeHigh = "NaN"
            self.timeLow = "NaN"
            self.avgBG = "NaN"
            self.highestDay = "NaN"
            self.lowestDay = "NaN"
            self.longestStint = "NaN"
            self.carbsConsumed = "NaN"
            self.insulinTotal = "NaN"
            self.a1c = "NaN"
            self.resEstimate = "NaN"
        else:
            self.tir = Stats.getTimeInRange(
                cleaned_dict["chunk3"], low_bound, high_bound
            )
            self.timeHigh = Stats.getTimeHigh(cleaned_dict["chunk3"], high_bound)
            self.timeLow = Stats.getTimeLow(cleaned_dict["chunk3"], low_bound)
            self.avgBG = Stats.getAvgBG(cleaned_dict["chunk3"])
            self.highestDay = Stats.getHighestDay(cleaned_dict["chunk3"])
            self.lowestDay = Stats.getLowestDay(cleaned_dict["chunk3"])
            self.longestStint = Stats.getLongestStint(
                cleaned_dict["chunk3"], low_bound, high_bound
            )
            self.carbsConsumed = Stats.getCarbsConsumed(cleaned_dict["chunk1"])
            self.insulinTotal = Stats.getInsulinTotal(
                cleaned_dict["chunk1"], basal_rate
            )
            self.a1c = Stats.getProjectedA1C(cleaned_dict["chunk3"])
            self.resEstimate = Stats.getReservoirEstimate(
                cleaned_dict["chunk1"], basal_rate
            )
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
        try:
            count = temp.value_counts()[True]
            percent = int(round(count / len(temp), 2) * 100)
            return str(percent) + "%"
        except KeyError:
            # This is the scenario in which no low values are found in the dataset.
            return "0%"

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
                ret_dict["Date"] = pd.Timestamp(day).strftime("%A %m/%d")
                ret_dict["Value"] = found_value

        return ret_dict["Date"] + " " + str(ret_dict["Value"]) + " mg/dL"

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
                ret_dict["Date"] = pd.Timestamp(day).strftime("%A %m/%d")
                ret_dict["Value"] = found_value

        return ret_dict["Date"] + " " + str(ret_dict["Value"]) + " mg/dL"

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
                start = stop

        # TODO: do string formatting on duration before exiting
        return duration.components

    def getCarbsConsumed(df: pd.DataFrame) -> str:
        """ """
        total = df["BWZ Carb Input (grams)"].sum().item()
        return str(total) + "g"

    def getInsulinTotal(df: pd.DataFrame, basal_rate: float) -> str:
        """
        Calculates the approximate amount of insulin used throughout the given period

        ## Parameters:
        `df`
        `basal_rate`: The basal rate defined in the form on the main app page.
        """
        basal_total = basal_rate * 7
        total = int(df["Bolus Volume Delivered (U)"].sum()) + basal_total
        return "~" + str(total) + " Units"

    def getProjectedA1C(df: pd.DataFrame) -> str:
        """
        Calculates an **projected** A1C based on blood glucose data.

        Incredibly important note: This is not an accurate estimation
        or representation of true A1C given that only 7 days of blood
        glucose data is available. It is only a representation of an A1C
        value of the previous 7 days and is intended to show the user a projection
        of an A1C value should the previous 7 days be characteristic of the next
        3 months.


        Described as:
        28.7 X A1C ??? 46.7 = eAG
        therefore
        (eAG + 46.7) / 28.7 = A1C
        Equation was sourced from: https://care.diabetesjournals.org/content/diacare/early/2008/06/07/dc08-0545.full.pdf
        See the description of table 2 on page 4.
        """

        eAG = df["Sensor Glucose (mg/dL)"].mean().astype("int32")
        A1C = (eAG + 46.7) / 28.7

        # Rounding for readability
        A1C = round(A1C, 2)

        return str(A1C) + "%*"

    def getReservoirEstimate(df: pd.DataFrame, basal_rate: float) -> str:
        """
        Calculates and returns the estimated amount of insulin used every three days.
        """
        basal_total = basal_rate * 7
        ins_total = int(df["Bolus Volume Delivered (U)"].sum()) + basal_total

        resEstimate = ins_total / 3

        return str(resEstimate) + "U per res."
