import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

"""
This may be converted into a class at some point.
"""


def combineTimeAndDate(date, time) -> any:
    """
    Simple lambda function used to combine time and date into a single timestamp.
    """
    return pd.Timestamp.combine(date, time)


def getLinePlot(df: pd.DataFrame) -> any:
    """
    Creates and returns a line plot of all blood sugar data.
    """
    df = df.sort_values(["Date", "Time"], ascending=(True, True))
    df["Date and Time"] = ""
    df["Date and Time"] = df[["Date", "Time"]].apply(
        lambda x: combineTimeAndDate(*x), axis=1
    )

    fig = px.line(df, x="Date and Time", y="Sensor Glucose (mg/dL)")

    fig.add_shape(
        type="line",
        x0=min(df["Date and Time"]),
        y0=80,
        x1=max(df["Date and Time"]),
        y1=80,
        line=dict(color="Red"),
    )

    fig.add_shape(
        type="line",
        x0=min(df["Date and Time"]),
        y0=180,
        x1=max(df["Date and Time"]),
        y1=180,
        line=dict(color="Orange"),
    )

    return fig


def getViolinPlot(df: pd.DataFrame) -> any:
    """
    Creates and returns a violin plot for each day in the data.
    Note: This plot may need to omit the day on which the data was pulled.
    """
    days = df["Date"].unique()

    fig = go.Figure()

    for day in days:
        window = df.loc[df["Date"] == pd.Timestamp(day)]

        fig.add_trace(
            go.Violin(
                x=window["Date"],
                y=window["Sensor Glucose (mg/dL)"],
                name=pd.Timestamp(day).strftime("%A %m/%d"),
                box_visible=True,
                meanline_visible=True,
            )
        )

    return fig
