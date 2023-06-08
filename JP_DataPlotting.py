
import pandas as pd
import JP_Classes as jpd

try:
    df = pd.read_excel('BBDD_EN_2017-2021.xlsx')
    Data_cleaned = jpd.DataCleaning(df) #It creates an instance of the DataCleaning class from the "JP_Classes" module, passing the df DataFrame as an argument.
    Data_cleaned.clean_and_export() #Apply data cleaning methods in a specific order.

    df_plotted = jpd.Datavisualization(Data_cleaned.df) #It creates an instance of the Datavisualization class from the "JP_Classes" module.
    df_plotted.calculate_data()

    # Generating plots:
    df_plotted.barplot_quantity()
    df_plotted.barplot_sales()
    df_plotted.piechart_years()

except FileNotFoundError:
    print("Error:File not found.") # If the file 'BBDD_EN_2017-2021.xlsx' is not found, the code inside the except block will be executed,
                                   # and the message "Error: File not found." will be printed.

