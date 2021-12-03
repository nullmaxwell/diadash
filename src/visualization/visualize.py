import pandas as pd
from dash import dcc
import plotly.express as px
import plotly.graph_objects as go


"""
This may be converted into a class at some point.
"""

color_bank = [
    "lightseagreen",
    "purple",
    "pink",
    "orange",
    "lightblue",
    "red",
    "brown",
    "grey",
]


def combineTimeAndDate(date, time) -> any:
    """
    Simple lambda function used to combine time and date into a single timestamp.
    """
    return pd.Timestamp.combine(date, time)


"""
Weekly View Plots
"""


def getWeeklyLinePlot(df: pd.DataFrame) -> any:
    """
    Creates and returns a line plot of all blood sugar data.
    """
    df = df.sort_values(["Date", "Time"], ascending=(True, True))
    df["Date and Time"] = ""
    df["Date and Time"] = df[["Date", "Time"]].apply(
        lambda x: combineTimeAndDate(*x), axis=1
    )

    fig = px.line(
        df,
        x="Date and Time",
        y="Sensor Glucose (mg/dL)",
        title="7 Day Sensor Glucose History",
    )

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

    fig.add_shape(
        type="rect",
        x0=min(df["Date and Time"]),
        y0=80,
        x1=max(df["Date and Time"]),
        y1=180,
        line=dict(
            color="LightGreen",
            width=2,
        ),
        fillcolor="LightGreen",
        opacity=0.30,
    )

    return dcc.Graph(id="weekly-line-plot", figure=fig)


def getViolinPlot(df: pd.DataFrame) -> any:
    """
    Creates and returns a violin plot for each day in the data.
    Note: This plot may need to omit the day on which the data was pulled.
    """
    global color_bank
    colors = color_bank.copy()

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
                line_color="black",
                fillcolor=colors.pop(),
                opacity=0.6,
            )
        )

    fig.update_layout(
        dict(
            title="7 Blood Glucose Range by Day",
            yaxis_title="Sensor Glucose (mg/dL)",
            xaxis_title="Date",
        )
    )

    return dcc.Graph(id="weekly-violin-plot", figure=fig)


"""
Daily View Plots
"""


def getDailyLinePlot(df: pd.DataFrame) -> any:
    """
    Creates and returns a violin plot for each day in the data.
    Note: This plot may need to omit the day on which the data was pulled.
    """
    global color_bank
    colors = color_bank.copy()

    days = df["Date"].unique()

    fig = go.Figure()

    for day in days:
        window = df.loc[df["Date"] == pd.Timestamp(day)]
        # window = window.sort_values(["Date", "Time"], ascending=(True, True))
        window = window.sort_values(["Time"], ascending=(True))

        fig.add_scatter(
            x=window["Time"],
            y=window["Sensor Glucose (mg/dL)"],
            name=pd.Timestamp(day).strftime("%A %m/%d"),
            line_color=colors.pop(),
        )

    # fig.update_xaxes(
    #     dict(
    #         type="category",
    #         categoryorder="category ascending",
    #         tickangle = 45,
    #         tickformat="%H:00",
    #         tickmode="auto",
    #         tickson="boundaries",
    #         nticks=8,
    #         tick0= time(hour=0, minute=0),
    #         dtick=time(hour=3, minute=0),
    #     )
    # )

    fig.update_xaxes(
        dict(
            type="category",
            categoryorder="category ascending",
            tickangle=45,
            tickformat="%H\n:00",
            tickmode="auto",
            nticks=8,
        )
    )

    # This will need to be changed into a single shape (shaded box)
    fig.add_shape(
        type="line",
        x0=min(df["Time"]),
        y0=80,
        x1=max(df["Time"]),
        y1=80,
        line=dict(color="Red"),
    )

    fig.add_shape(
        type="line",
        x0=min(df["Time"]),
        y0=180,
        x1=max(df["Time"]),
        y1=180,
    )

    fig.add_shape(
        type="rect",
        x0=min(df["Time"]),
        y0=80,
        x1=max(df["Time"]),
        y1=180,
        line=dict(
            color="LightGreen",
            width=2,
        ),
        fillcolor="LightGreen",
        opacity=0.30,
    )

    fig.update_layout(
        dict(
            title="Daily Sensor Glucose",
            yaxis_title="Sensor Glucose (mg/dL)",
            xaxis_title="Time",
        )
    )

    return dcc.Graph(id="daily-line-plot", figure=fig)


"""
Other view plots.
"""


def getCarbInsulinPlot(df: pd.DataFrame) -> any:
    """
    Creates and returns a bar graph of insulin dosed and carbs consumed by day.
    """

    days = df["Date"].unique()
    carb_sums = []
    insulin_sums = []

    for day in days:
        window = df.loc[df["Date"] == pd.Timestamp(day)]
        carb_sums.append(window["BWZ Carb Input (grams)"].sum().astype("int32"))
        insulin_sums.append(window["Bolus Volume Delivered (U)"].sum().astype("int32"))

    fig = go.Figure(
        data=[
            go.Bar(name="Carbs Consumed", x=days, y=carb_sums, marker_color="tan"),
            go.Bar(name="Insulin Dosed", x=days, y=insulin_sums, marker_color="pink"),
        ]
    )

    fig.update_layout(
        dict(
            barmode="group",
            title="Carbs consumed vs. Insulin Dosed by Day",
            yaxis_title="Value",
            xaxis_title="Date",
        )
    )

    return dcc.Graph(id="daily-line-plot", figure=fig)
