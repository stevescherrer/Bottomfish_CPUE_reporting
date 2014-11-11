'''
Created on Nov 10, 2014

@author: stephenscherrer
'''
import numpy
import pandas
import os
from tabulate import tabulate

def gen_filename(start_data, end_data):
    '''
    generates a list of filenames for the data for importing.
    start date is of the format mmyy, end date of the format mmyy
    '''
    filenames = list()
    month_counter = int(start_data[:2])
    year_counter = year_2dig_to_4dig(start_data[2:])
    endyear = year_2dig_to_4dig(int(str(end_data[2:])))
    endmonth = int(end_data[:2])
    while year_counter <= endyear:
        if year_counter < endyear:
            filenames.append( (''.join(('hr' , str(month_counter).zfill(2), str(year_counter)[2:], '.xls'))))
            if month_counter < 12:
                month_counter += 1
            else:
                month_counter = 1
                year_counter += 1
        elif year_counter == endyear:
            if month_counter < endmonth:
                filenames.append( (''.join(('hr' , str(month_counter).zfill(2), str(year_counter)[2:], '.xls'))))
                month_counter += 1
            elif month_counter == endmonth:
                filenames.append( (''.join(('hr' , str(month_counter).zfill(2), str(year_counter)[2:], '.xls'))))
                year_counter += 1
    return filenames

        
def year_2dig_to_4dig(year_2dig):
    year_2dig_int = int(year_2dig)
    if (year_2dig_int < 20):
        year = int(year_2dig_int) + 2000
    else:
        year = int(year_2dig_int) + 1900
    return year


def scrape_month_year(filename):
    ''' 
    pulling month and year from filename
    '''
    month = filename[2:3]
    year_2dig = filename[4:5]
    if (year_2dig < 20):
        year = int(year_2dig) + 2000
    else:
        year = int(year_2dig) + 1900
    return (month, year)

"""class catch_data:
    '''
    convenience class for importing catch data records
    '''
    def __init__(self):
        pass
    
    def load_data(self, filename, data_to_extract = ('species', 'caught', 'sold', 'value', 'price/lb'), 
                  columns_to_extract = (0,1,2,3,4), skip_header = 3, delimiter = ',', dtype = str):
        self.data = {}
        self.data_to_extract = data_to_extract
        for column, name in zip(columns_to_extract, data_to_extract):
            self.data[name] = numpy.genfromtxt(filename, usecols = (column,), skip_header = skip_header, 
                                               delimiter = delimiter, dtype = dtype)
    
    def extract_species(self, species = ['Ehu (red snapper)','Gindai (flower snapper)','Lehi (silverjaw)','Onaga (red snapper)','Opakapaka (pink snapper)','Hapuupuu (hawaiian grouper)', 'Uku (gray snapper)']):
        darray = numpy.zeros((len(species), len(self.data_to_extract)))
        for ind, spp in enumerate(species):
            i = self.data['species'].index(spp)
            darray[ind,0] = ind; darray[ind,1] = self.data['caught'][i], darray[ind,2] = self.data['sold'][i]; darray[ind,3] = self.data['value'][i]; darray[ind,4] = self.data['price/lb'][i]
        return darray"""
    
def unicode2ascii(unicode_str):
    ascii_str = unicode_str.encode('ascii', 'ignore')
    return ascii_str

def extract_species(spp_list, species):
    i = spp_list.index(species)
    return i
    
        
def build_csv(path, start_date, end_date, data_to_extract, columns_to_extract, species_to_extract):
    filenames = gen_filename(start_date, end_date)
    n_rows = len(filenames)*len(species_to_extract)
    n_cols = len(data_to_extract)
    output_array = numpy.zeros((n_rows, n_cols))
    file_counter = 0
    for pass_counter, filename in enumerate(filenames):
        filepath = ''.join((path, '/' ,filename))
        darray = pandas.read_excel(filepath, sheetname = 0, skiprows = 2, skip_footer = 1, header = 0, index_col = None)
        new_columns = darray.columns.values
        new_columns[0] = 'Species'; new_columns[1] = 'Caught'; new_columns[2] = 'Sold'; new_columns[3] = 'Value'; new_columns[4] = 'PricePound'
        darray.columns = new_columns
        species_list = list()
        for row in range(0,len(darray.Species)):
            species_list.append(unicode2ascii(darray.Species[row].strip()))
        for i, species in enumerate(species_to_extract):
            index = species_list.index(species)
            output_array[pass_counter*i+i, 0] = i+1; 
            output_array[pass_counter*i+i, 1] = darray.Caught[index];
            output_array[pass_counter*i+i, 2] = darray.Sold[index]; 
            output_array[pass_counter*i+i, 3] = darray.Value[index];
            output_array[pass_counter*i+i, 4] = darray.PricePound[index];
        print tabulate(output_array, ('Species Number', 'Caught', 'Sold', 'Value', 'Price/Lb'))
    numpy.savetxt("catch_data.csv", output_array, delimiter  = ',' )

        
          
        
            
#### usage

def test():
    cwd = os.getcwd()  # Get the current working directory (cwd)
    files = os.listdir(cwd)  # Get all the files in that directory
    print("Files in '%s': %s" % (cwd, files))
    build_csv(path = '/Users/stephenscherrer/Documents/Programming/Python/Eclipse/Programming Workspace/Bottomfish_CPUE_reporting',
              start_date = '9001', 
              end_date = '9001', 
              data_to_extract = ('species', 'caught', 'sold', 'value', 'price/lb'), 
              columns_to_extract = (0,1,2,3,4), 
              species_to_extract = ('Ehu (red snapper)','Gindai (flower snapper)','Lehi (silverjaw)','Onaga (red snapper)','Opakapaka (pink snapper)','Hapuupuu (hawaiian grouper)', 'Uku (gray snapper)'))

    

    
if __name__ == "__main__":
    test()
