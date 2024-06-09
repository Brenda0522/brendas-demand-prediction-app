# Brenda’s Demand Prediction APP

Welcome to Brenda’s demand prediction app! This app aims to help you predict demand based on historical data from the previous years.

## APP Instructions

Click on the region(s) you are interested in analyzing. You can select one, two, or all available regions.

Use the slider to adjust the weight of the demand from the previous year. The weight for the year before last will be adjusted automatically to sum up to 1 (Note: Weights are between 0 and 1).

The predicted demand is visualized with a red line on the graph. You have the option to enter actual demand data for the current year; the prediction line will update automatically to reflect this.

Check the box at the bottom of the app to display a detailed table with precise predicted demand values.

## Code Flow

Load demand data for the past two years from CSV files.

Calculate the total demand for all selected regions, adjusting based on user input from the checkboxes.

Derive the price factor based on the weighted average of demand from the two previous years, and calculate the estimated demand of Superman for this year based on the slider's setting to weigh the most recent year's data.

If actual demand for Superman is provided, fit a linear regression model on the relationship between demand and price for the three years to obtain a new price factor. Use this new price factor to update demand estimates for Superman.

Plot the graph with different colors for the three years. If the user opts to view the precise predicted demand, display this data in a table format.
