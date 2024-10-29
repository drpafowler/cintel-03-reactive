# Import data from shared.py
from shared import app_dir, df
import plotly.express as px
from shiny import reactive
from shiny.express import input, render, ui
from shinywidgets import render_widget  
import seaborn as sns


ui.page_opts(title=ui.h1("Philip's Penguins", style="text-align: center;"), fillable=True)


with ui.sidebar(title=ui.h2("Display Controls"), width="400px"):
    # Input for selecting the type of plot
    ui.input_select("plot", "Plot Type", ["Scatterplot", "Histogram"])
    
    # Input for selecting the x-axis variable for all plots
    ui.input_select("xaxis", "X-axis (all plots)", ["bill_length_mm", "bill_depth_mm", "body_mass_g"], selected="bill_length_mm")
    
    # Input for selecting the y-axis variable for scatterplots
    ui.input_select("yaxis", "Scatterplot Y-axis", ["bill_length_mm", "bill_depth_mm", "body_mass_g"], selected="bill_depth_mm")
    
    # Input for selecting the hue control variable
    ui.input_select("hue_control", "Hue Control", ["sex", "species", "island"], selected="species")
    
    # Input slider for selecting the number of bins for histograms
    ui.input_slider("bins", "Number of bins (histogram)", 5, 50, 20, post=" bins")

    ui.hr()

    ui.h2("Filter Controls")
    
    # Switch for enabling/disabling data filtering
    ui.input_switch("filter", "Filter Data", True)
    
    # Input slider for filtering by body mass
    ui.input_slider("mass", "Body Mass (g)", 2000, 6000, [2000,6000], post=" g")
    
    # Input slider for filtering by bill depth
    ui.input_slider("bill_depth", "Bill Depth (mm)", 10, 25, [10, 25], post=" mm")
    
    # Input slider for filtering by bill length
    ui.input_slider("bill_length", "Bill Length (mm)", 30, 60, [30, 60], post=" mm")
    
    # Checkbox group for filtering by sex
    ui.input_checkbox_group(
        "sex",
        "Sex",
        ["Male", "Female"],
        selected=["Male", "Female"],
        inline=True,
    )
    
    # Checkbox group for filtering by species
    ui.input_checkbox_group(
        "species",
        "Species",
        ["Adelie", "Gentoo", "Chinstrap"],
        selected=["Adelie", "Gentoo", "Chinstrap"],
        inline=True,
    )
    
    # Checkbox group for filtering by island
    ui.input_checkbox_group(
        "island",
        "Island",
        ["Biscoe", "Dream", "Torgersen"],
        selected=["Biscoe", "Dream", "Torgersen"],
        inline=True,
    )   
    # Button to reset all filters to their initial settings
    ui.input_action_button("reset", "Reset Filters")


    # Link to GitHub repository
    ui.a("GitHub", href="https://github.com/drpafowler/cintel-02-data", target="_blank")



with ui.layout_column_wrap(fill=False):
    with ui.value_box():
        ui.h4("Dynamic Text1", style="color: white;")

        @render.text
        def count():
            # Display the number of penguins in the filtered dataset
            return f"{filtered_df().shape[0]} penguins"

    with ui.value_box():
        ui.h4("Dynamic Text2", style="color: white;")
        
        @render.text
        def dynamic_text2():
            # Display average bill length for scatterplot or average of selected x-axis variable for histogram
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
            # Display average bill depth for scatterplot or median of selected x-axis variable for histogram
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
            # Display average body mass for scatterplot or range of selected x-axis variable for histogram
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
            # Check if the selected plot type is Scatterplot
            if input.plot() == "Scatterplot":
                # If filtering is enabled, use filtered data
                if input.filter():
                    return sns.scatterplot(
                        data=filtered_df(),
                        x=input.xaxis(),
                        y=input.yaxis(),
                        hue=input.hue_control(),
                    )
                # If filtering is disabled, use unfiltered data
                else:
                    return sns.scatterplot(
                        data=filtered_df(),
                        x=input.xaxis(),
                        y=input.yaxis(),
                    )
            # Check if the selected plot type is Histogram
            elif input.plot() == "Histogram":
                # If filtering is enabled, use filtered data
                if input.filter():
                    return sns.histplot(
                        data=filtered_df(),
                        x=input.xaxis(),
                        bins=input.bins(),
                        hue=input.hue_control(),
                        multiple="stack",
                    )
                # If filtering is disabled, use unfiltered data
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
            # Check if the selected plot type is Scatterplot
            if input.plot() == "Scatterplot":
                # If filtering is enabled, use filtered data
                if input.filter():
                    fig = px.scatter(
                        filtered_df(),
                        x=input.xaxis(),
                        y=input.yaxis(),
                        color=input.hue_control(),
                        title="Scatterplot of Penguin Data"
                    )
                # If filtering is disabled, use unfiltered data
                else:
                    fig = px.scatter(
                        filtered_df(),
                        x=input.xaxis(),
                        y=input.yaxis(),
                        title="Scatterplot of Penguin Data"
                    )
            # Check if the selected plot type is Histogram
            elif input.plot() == "Histogram":
                # If filtering is enabled, use filtered data
                if input.filter():
                    fig = px.histogram(
                        filtered_df(),
                        x=input.xaxis(),
                        color=input.hue_control(),
                        marginal="box",
                        title="Histogram of Penguin Data",
                        nbins=input.bins()
                    )
                # If filtering is disabled, use unfiltered data
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
        # Card header for the data table
        ui.card_header("Penguin data")
        # Switch to toggle the display of the data table
        ui.input_switch("show_table", "Switch on to show a data table", False)
        
        @render.data_frame
        def summary_statistics():
            # Columns to be displayed in the data table
            cols = [
                "species",
                "island",
                "bill_length_mm",
                "bill_depth_mm",
                "body_mass_g",
                "sex",
            ]
            # Render the data table if the switch is on, otherwise render a data grid
            if input.show_table():
                return render.DataTable(filtered_df()[cols], filters=True)
            else:
                return render.DataGrid(filtered_df()[cols], filters=True)

    with ui.card(full_screen=True):
        # Card header for the correlation heatmap
        ui.card_header("Penguin Correlation Table")
        
        @render.plot
        def correlation_heatmap():
            # Columns to be used for the correlation heatmap
            cols = ["bill_length_mm", "bill_depth_mm", "body_mass_g"]
            # Calculate the correlation matrix
            corr = filtered_df()[cols].corr()
            # Render the heatmap with annotations and a color map
            return sns.heatmap(corr, annot=True, cmap="coolwarm", vmin=-1, vmax=1)

# Include custom CSS styles
ui.include_css(app_dir / "styles.css")


@reactive.calc
def filtered_df():
    # If filtering is not enabled, return the original dataframe
    if not input.filter():
        return df
    
    # Filter the dataframe based on selected species
    filt_df = df[df["species"].isin(input.species())]
    
    # Further filter the dataframe based on selected sex
    filt_df = filt_df[filt_df["sex"].isin(input.sex())]
    
    # Further filter the dataframe based on selected island
    filt_df = filt_df[filt_df["island"].isin(input.island())]
    
    # Further filter the dataframe based on selected body mass range
    filt_df = filt_df.loc[(filt_df["body_mass_g"] >= input.mass()[0]) & (filt_df["body_mass_g"] <= input.mass()[1])]
    
    # Further filter the dataframe based on selected bill depth range
    filt_df = filt_df.loc[(filt_df["bill_depth_mm"] >= input.bill_depth()[0]) & (filt_df["bill_depth_mm"] <= input.bill_depth()[1])]
    
    # Further filter the dataframe based on selected bill length range
    filt_df = filt_df.loc[(filt_df["bill_length_mm"] >= input.bill_length()[0]) & (filt_df["bill_length_mm"] <= input.bill_length()[1])]
    
    # Return the filtered dataframe
    return filt_df


