
import pandas as pd
import matplotlib.pyplot as plt

class DataCleaning:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def select_columns(self): #selection of columns required for data analysis
        self.df = self.df.loc[:,
                  ['DATE OF DECLARATION', 'IMPORTER NAME', 'TARIFF', 'GLOSSARY TARIFF', 'PRODUCT', 'BRAND', 'VARIETY',
                   'COUNTRY OF ORIGIN', 'QUANT. MERC.', 'UNIT. CIF (US$)']]

    def format_TARIFF_Column(self): #Information from Polyester market are found in TARIFF 3907.209 and 3907.91
        self.df['TARIFF'] = self.df['TARIFF'].astype(str)
        self.df['TARIFF'] = self.df['TARIFF'].str.replace(' ', '')
        self.df = self.df[self.df['TARIFF'].isin(['3907.209', '3907.91'])]

    def fill_blanks(self):
        self.df['IMPORTER NAME'].fillna('NO NAME', inplace=True)

    def format_data_types(self):
        self.df['DATE OF DECLARATION'] = pd.to_datetime(self.df['DATE OF DECLARATION'], dayfirst=True)
        self.df['MONTH'] = self.df['DATE OF DECLARATION'].dt.month
        self.df['YEAR'] = self.df['DATE OF DECLARATION'].dt.year
        self.df['IMPORTER NAME'] = self.df['IMPORTER NAME'].astype(str)
        self.df['GLOSSARY TARIFF'] = self.df['GLOSSARY TARIFF'].astype(str)
        self.df['PRODUCT'] = self.df['PRODUCT'].astype(str)
        self.df['BRAND'] = self.df['BRAND'].astype(str)
        self.df['VARIETY'] = self.df['VARIETY'].astype(str)
        self.df['COUNTRY OF ORIGIN'] = self.df['COUNTRY OF ORIGIN'].astype(str)
        self.df['QUANT. MERC.'] = self.df['QUANT. MERC.'].astype(float)
        self.df['UNIT. CIF (US$)'] = self.df['UNIT. CIF (US$)'].astype(float)

    def rename_columns(self): #Modify column names for better readability
        new_column_names = {'DATE OF DECLARATION': 'DATE', 'IMPORTER NAME': 'IMPORTER', 'QUANT. MERC.': 'QUANTITY'}
        self.df = self.df.rename(columns=new_column_names)

    def finding_brands(self): #Obtain the brands that make up the polyester market
        self.df['BRAND1'] = ''
        self.df.loc[self.df['BRAND'].str.contains('ANDERCOL', case=False), 'BRAND1'] = 'ANDERCOL'
        self.df.loc[self.df['BRAND'].str.contains('AOC', case=False), 'BRAND1'] = 'AOC'
        self.df.loc[self.df['BRAND'].str.contains('PLAQUIMET', case=False), 'BRAND1'] = 'PLAQUIMET'
        self.df.loc[self.df['BRAND'].str.contains('POLIYA', case=False), 'BRAND1'] = 'POLIYA'
        self.df.loc[self.df['BRAND'].str.contains('REICHHOLD', case=False), 'BRAND1'] = 'REICHOLD'
        self.df.loc[self.df['BRAND'].str.contains('REICHOLD', case=False), 'BRAND1'] = 'REICHOLD'
        self.df.loc[self.df['BRAND'].str.contains('SHANGHAI', case=False), 'BRAND1'] = 'SHANGHAI'
        self.df.loc[self.df['BRAND'].str.contains('TURKUAZ', case=False), 'BRAND1'] = 'TURKUAZ'

    def filtered_by_market_assumptions(self): #Important market assumption for the polyester product line
        self.df = self.df.loc[(self.df['UNIT. CIF (US$)'] > 0) & (self.df['UNIT. CIF (US$)'] < 3) & (self.df['QUANTITY'] > 1000)]

    def clean_and_export(self): #Apply all data cleaning methods in a specific order.
        self.select_columns()
        self.format_TARIFF_Column()
        self.fill_blanks()
        self.format_data_types()
        self.rename_columns()
        self.finding_brands()
        self.filtered_by_market_assumptions()
        self.export_to_excel()

    def export_to_excel(self):
        self.df.to_excel('output_data_cleaning.xlsx', index=False)



class Datavisualization:

    def __init__(self, df_plot: pd.DataFrame):
        self.df_plot = df_plot

    def calculate_data(self): #Filters the DataFrame to include only specific brands that are the polyester market,
    #Calculates total quantity, total UN. CIF (US$), and total sales. All these parameters are used to plot.

        polyester_brands = ['ANDERCOL', 'AOC', 'PLAQUIMET', 'POLIYA', 'REICHOLD', 'SHANGHAI', 'TURKUAZ']
        self.polyester_data = self.df_plot[self.df_plot['BRAND1'].isin(polyester_brands)]
        self.polyester_total = self.polyester_data.groupby('YEAR')['QUANTITY'].sum()
        self.total_UNIT_CIF = self.polyester_data.groupby('YEAR')['UNIT. CIF (US$)'].sum()

        sales_per_year = {
            2017: 2.3,
            2018: 2,
            2019: 2.8,
            2020: 2.7,
            2021: 2.5
        }
        self.total_sales = self.polyester_total * pd.Series(sales_per_year)

    def barplot_quantity(self):
        plt.figure(figsize=(8, 6))
        years = self.polyester_total.index.tolist()
        plt.bar(years, self.polyester_total)
        plt.xlabel('Year')
        plt.ylabel('Total Polyester')
        plt.title('Total Polyester in Each Year')
        for i, value in enumerate(self.polyester_total.values):
            plt.text(self.polyester_total.index[i], value, str(int(value)), ha='center', va='bottom')
        plt.show()

    def barplot_sales(self):

        plt.figure(figsize=(8, 6))
        plt.bar(self.total_sales.index, self.total_sales.values)
        plt.xlabel('Year')
        plt.ylabel('Total Sales (in euros)')
        plt.title('Total Polyester Sales per Year')
        for i, value in enumerate(self.total_sales.values):
            plt.text(self.total_sales.index[i], value, str(int(value)), ha='center', va='bottom')
        plt.show()

    def piechart_years(self):

        self.polyester_totalbrands_years = self.polyester_data[
            self.polyester_data['YEAR'] == 2020]

        self.brand_quantity_total_2020 = self.polyester_totalbrands_years.groupby('BRAND1')[
            'QUANTITY'].sum()
        plt.pie(self.brand_quantity_total_2020, labels=self.brand_quantity_total_2020.index,
                autopct='%1.1f%%')
        plt.title("Distribution of Brands 2020")
        plt.axis('equal')
        plt.show()
