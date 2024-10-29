import seaborn as sns

# Import data from shared.py
from shared import app_dir, df
import plotly.express as px
from shiny import reactive
from shiny.express import input, render, ui
from shinywidgets import render_widget  


ui.page_opts(title=ui.h1("Philip's Penguins", style="text-align: center;"), fillable=True)


with ui.sidebar(title=ui.h2("Display Controls"), width="400px"):
    ui.input_select("plot", "Plot Type", ["Scatterplot", "Histogram"])
    ui.input_select("xaxis", "X-axis (all plots)", ["bill_length_mm", "bill_depth_mm", "body_mass_g"], selected="bill_length_mm")
    ui.input_select("yaxis", "Scatterplot Y-axis", ["bill_length_mm", "bill_depth_mm", "body_mass_g"], selected="bill_depth_mm")
    ui.input_select("hue_control", "Hue Control", ["sex", "species", "island"], selected="species")
    ui.input_slider("bins", "Number of bins (histogram)", 5, 50, 20, post=" bins")

    ui.hr()

    ui.h2("Filter Controls")
    ui.input_switch("filter", "Filter Data", True)
    ui.input_slider("mass", "Body Mass (g)", 2000, 6000, [2000,6000], post=" g")
    ui.input_slider("bill_depth", "Bill Depth (mm)", 10, 25, [10, 25], post=" mm")
    ui.input_slider("bill_length", "Bill Length (mm)", 30, 60, [30, 60], post=" mm")
    ui.input_checkbox_group(
        "sex",
        "Sex",
        ["Male", "Female"],
        selected=["Male", "Female"],
        inline=True,
    )
    ui.input_checkbox_group(
        "species",
        "Species",
        ["Adelie", "Gentoo", "Chinstrap"],
        selected=["Adelie", "Gentoo", "Chinstrap"],
        inline=True,
    )
    ui.input_checkbox_group(
        "island",
        "Island",
        ["Biscoe", "Dream", "Torgersen"],
        selected=["Biscoe", "Dream", "Torgersen"],
        inline=True,
    )   



    ui.a("GitHub", href="https://github.com/drpafowler/cintel-02-data", target="_blank")



with ui.layout_column_wrap(fill=False):
    with ui.value_box():
        ui.h4("Dynamic Text1", style="color: white;")

        @render.text
        def count():
            return f"{filtered_df().shape[0]} penguins"

    with ui.value_box():
        ui.h4("Dynamic Text2", style="color: white;")
        @render.text
        def dynamic_text2():
            if input.plot() == "Scatterplot":
                return f"Average bill length: {filtered_df()['bill_length_mm'].mean():.1f} mm"
            elif input.plot() == "Histogram":
                if input.xaxis() == "bill_depth_mm":
                    return f"Average bill depth: {filtered_df()['bill_depth_mm'].mean():.1f} mm"
                elif input.xaxis() == "bill_length_mm":
                    return f"Average bill length: {filtered_df()['bill_length_mm'].mean():.1f} mm"
                elif input.xaxis() == "body_mass_g":
                    return f"Average body mass: {filtered_df()['body_mass_g'].mean():.1f} g"
            return "Select a valid plot type and x-axis"

    with ui.value_box():
        ui.h4("Dynamic Text3", style="color: white;")
        @render.text
        def dynamic_text3():
            if input.plot() == "Scatterplot":
                return f"Average bill depth: {filtered_df()['bill_depth_mm'].mean():.1f} mm"
            elif input.plot() == "Histogram":
                if input.xaxis() == "bill_depth_mm":
                    return f"Median bill depth: {filtered_df()['bill_depth_mm'].median():.1f} mm"
                elif input.xaxis() == "bill_length_mm":
                    return f"Median bill length: {filtered_df()['bill_length_mm'].median():.1f} mm"
                elif input.xaxis() == "body_mass_g":
                    return f"Median body mass: {filtered_df()['body_mass_g'].median():.1f} g"
            return "Select a valid plot type and x-axis"
    
    with ui.value_box():
        ui.h4("Dynamic Text4", style="color: white;")

        @render.text
        def dynamic_text4():
            if input.plot() == "Scatterplot":
                return f"Average body mass: {filtered_df()['body_mass_g'].mean():.1f} g"
            elif input.plot() == "Histogram":
                if input.xaxis() == "bill_length_mm":
                    return f"Range of bill length: {filtered_df()['bill_length_mm'].min():.1f} mm - {filtered_df()['bill_length_mm'].max():.1f} mm"
                elif input.xaxis() == "bill_depth_mm":
                    return f"Range of bill depth: {filtered_df()['bill_depth_mm'].min():.1f} mm - {filtered_df()['bill_depth_mm'].max():.1f} mm"
                elif input.xaxis() == "body_mass_g":
                    return f"Range of body mass: {filtered_df()['body_mass_g'].min():.1f} g - {filtered_df()['body_mass_g'].max():.1f} g"
            return "Select a valid plot type and x-axis"

with ui.layout_columns():
    with ui.card(full_screen=True):
        ui.card_header("Seaborn Penguin Data Visualisation")

        @render.plot
        def length_depth():
            if input.plot() == "Scatterplot":
                if input.filter():
                    return sns.scatterplot(
                        data=filtered_df(),
                        x=input.xaxis(),
                        y=input.yaxis(),
                        hue=input.hue_control(),
                    )
                else:
                    return sns.scatterplot(
                        data=filtered_df(),
                        x=input.xaxis(),
                        y=input.yaxis(),
                    )
            elif input.plot() == "Histogram":
                if input.filter():
                    return sns.histplot(
                        data=filtered_df(),
                        x=input.xaxis(),
                        bins=input.bins(),
                        hue=input.hue_control(),
                        multiple="stack",
                    )
                else:
                    return sns.histplot(
                        data=filtered_df(),
                        x=input.xaxis(),
                        bins=input.bins(),
                    )

    with ui.card(full_screen=True):
        ui.card_header("Plotly Penguin Data Visualisation")

        @render_widget
        def plotly_plot():
            if input.plot() == "Scatterplot":
                if input.filter():
                    fig = px.scatter(
                    filtered_df(),
                    x=input.xaxis(),
                    y=input.yaxis(),
                    color=input.hue_control(),
                    title="Scatterplot of Penguin Data"
                    )
                else:
                    fig = px.scatter(
                    filtered_df(),
                    x=input.xaxis(),
                    y=input.yaxis(),
                    title="Scatterplot of Penguin Data"
                    )
            elif input.plot() == "Histogram":
                if input.filter():
                    fig = px.histogram(
                    filtered_df(),
                    x=input.xaxis(),
                    color=input.hue_control(),
                    marginal="box",
                    title="Histogram of Penguin Data",
                    nbins=input.bins()
                    )
                else:
                    fig = px.histogram(
                    filtered_df(),
                    x=input.xaxis(),
                    marginal="box",
                    title="Histogram of Penguin Data",
                    nbins=input.bins()
                    )
            return fig


with ui.layout_columns():

    with ui.card(full_screen=True):
        ui.card_header("Penguin data")
        ui.input_switch("show_table", "Switch on to show a data table", False)
        @render.data_frame
        def summary_statistics():
            cols = [
                "species",
                "island",
                "bill_length_mm",
                "bill_depth_mm",
                "body_mass_g",
                "sex",
            ]
            if input.show_table():
                return render.DataTable(filtered_df()[cols], filters=True)
            else:
                return render.DataGrid(filtered_df()[cols], filters=True)
    with ui.card(full_screen=True):
        ui.card_header("Penguin Correlation Table")
        @render.plot
        def correlation_heatmap():
            cols = ["bill_length_mm", "bill_depth_mm", "body_mass_g"]
            corr = filtered_df()[cols].corr()
            return sns.heatmap(corr, annot=True, cmap="coolwarm", vmin=-1, vmax=1)


ui.include_css(app_dir / "styles.css")


@reactive.calc
def filtered_df():
    if not input.filter():
        return df
    filt_df = df[df["species"].isin(input.species())]
    filt_df = filt_df[filt_df["sex"].isin(input.sex())]
    filt_df = filt_df[filt_df["island"].isin(input.island())]
    filt_df = filt_df.loc[(filt_df["body_mass_g"] >= input.mass()[0]) & (filt_df["body_mass_g"] <= input.mass()[1])]
    filt_df = filt_df.loc[(filt_df["bill_depth_mm"] >= input.bill_depth()[0]) & (filt_df["bill_depth_mm"] <= input.bill_depth()[1])]
    filt_df = filt_df.loc[(filt_df["bill_length_mm"] >= input.bill_length()[0]) & (filt_df["bill_length_mm"] <= input.bill_length()[1])]
    return filt_df
