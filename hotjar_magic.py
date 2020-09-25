# -*- coding: utf-8 -*-
"""
Created on Sun Jun  7 17:33:58 2020

@author: Pippa Gittings
"""

# Hello, and welcome to my HotJar magic script!

# This script takes a downloaded CSV file from HotJar. 

# It finds columns that contain multiple values per user (by default, spread across multiple rows). 
# For all the values in each of these columns, it creates a new column that holds a true/false value for every user's response.

# For example, if a user responded 'Blueberry', 'Apples' and 'Grapes' to a survey question 'Pick your top 3 fruit'...
# ... the script creates columns for 'Blueberry', 'Apples' and 'Grapes', and changes the value in each to 'True' for each user.

# This means that you can analyse the exported spreadsheet for questions combining multiple-answer columns.

#%%

# 1. Install pandas
# ---------------------------------

# If you're using Jupyter Notebooks, uncomment this first part

# Install a conda package in the current Jupyter kernel
# import sys
# !conda install --yes --prefix {sys.prefix} pandas

# Import pandas
import pandas as pd

# **


# 2. Import data from a CSV file
# ------------------------------

# Create new DataFrame object, data, that holds the CSV file data. Make sure the file name and location are correct. Be careful that you've not ended up with empty rows somewhere!

print('Enter the file path of the HotJar data you would like to import. Make sure you include the full file path (i.e. C:\ etc) and that your file is a CSV.')

import_path = input('Enter import path: ')

print(' ')
print('***')
print(' ')

data = pd.read_csv(import_path)

# **


# 3. Print out information on the file you have
# ---------------------------------------------

# Print out key information about the CSV file

# Print out basic info

print("The data file has " + str(len(data)) + " rows, and " + str(len(data.columns)) + " columns.")
print(' ')
print('***')
print(' ')

# Print column names

# Set column index to start at 0
col_ind = 0

print("The original column labels are...")
print('---------------------------------')

# Print column names

while col_ind < len(data.columns) :
    print("-- " + str(data.count().index.to_list()[col_ind]))
    col_ind = col_ind + 1

print(' ')
print('***')
print(' ')

# **

#%%

# 4. Identify any multiselect columns; print them out and create a list
# ---------------------------------------------------------------------

# Create an empty list called 'multi'

multi = []

# Print the introductory statement

print("The multi-select columns are...")
print('-------------------------------')

# Iterate over the data

for label, row in data.iterrows() :

# Iterate over the values in the row (as a list)        

        for m in row.tolist() :
            
# Check for the presence of the vertical pipe symbol | that separates each multiselect answer

            if '|' in str(m) :
                
# If it's present, add the name of the column to the multi list
                
                if data.columns[row.tolist().index(m)] not in multi : 
                    multi.append(data.columns[row.tolist().index(m)])
                    print('-- ' + str(data.columns[row.tolist().index(m)]))

print(' ')
print('***')
print(' ')

# **

#%%

# 5. Identify unique values in a multiselect column, removing NaN and any 'Other' answers
# ---------------------------------------------------------------------------------------

# Iterate over all values in multi

for y in multi :
    
# Print introductory statement

    print("The unique column values in " + str(y) + " are: ")
    
# Create a blank list for unique column values

    unique_col = []

# Create a blank list for split values
    
    split = []

# Iterate over the unique values in each multiselect column, as a list

    for x in data[y].unique().tolist() :
        
# Split the separated values into a list
        
        if type(x) == str :
            split = x.split(" | ")
            
# For each value in the split list, add it to the list of unique column values
            
            for s in split :
                
# Check that it's not a free text entry field (i.e. contains 'Other')
                
                if 'Other' not in str(s):
                    
# Check it's not already in the unique column values list; add if not
                    
                    if s not in unique_col :
                        unique_col.append(s)

# Print each value

    for u in unique_col :
        print('-- ' + str(u))
    
    print(' ')
    print('***')
    print(' ')

# **

#%%
    
# 6. Create new columns in data for each unique column value, e.g. 'likes_blueberry_pie'. 
# ---------------------------------------------------------------------------------------

# We need to create Boolean values in a column for each unique value. For example, if the original column was 'What pie do you like?' and one of the answers was 'Blueberry', we want to create a column called 'likes_blueberry' and have the answer as either yes or no.

# Start by creating the new columns, ready for data

for x in unique_col :
    data.insert(len(data.columns), "ms_" + str(multi.index(y) + 1) + "_" + x.lower(), False, allow_duplicates = False)

# Note that this creates columns labelled with multiselect, the index of the multiselect column, and the unique value label, as follows: ms_1_blueberry.

print('Here is the updated column list, with new columns for all multiselect answers...')
print('--------------------------------------------------------------------------------')

for z in data.columns.tolist(): 
    print('-- ' + str(z))

print(' ')
print('***')
print(' ')

# **

#%%

# 7. Update the first row of each response to have the correct Boolean values for each multiselect answer
# -------------------------------------------------------------------------------------------------------

# Iterate over the data table

for label, row in data.iterrows() :
    
# Iterate over the row values as a list
    
    for r in row.tolist() :
        
# Iterate over the multiselect columns
    
        for y in multi :
            
# Iterate over the unique answers within the column (separated by |)
            
            for u in unique_col :
                
# Recreate the new column name to use as a reference in a moment...
                
                bool_col = "ms_" + str(multi.index(y) + 1) + "_" + u.lower()
                
# Check if the unique answer is contained within a cell
                
                if u in str(r) :
                    
# If it is, change the corresponding Boolean column to a 'True' value
                    
                    data.at[label, bool_col] = True
        

print('New columns updated with True wherever user selected it...')

print(' ')
print('***')
print(' ')

# **

#%%

# 8. Export data
# ----------------------------

# Now we just need to export the data.

print('Enter the file path where you would like the data exported. Make sure you include the full file path (i.e. C:\ etc) and that your file is a CSV.')

export_path = input('Enter export path: ')

data.to_csv(export_path, index=False)

print(' ')

print("Export complete. Get analysing!")

print(' ')
print('***')
print(' ')

print('Reminder: the multiselect columns are as follows:')

for c in multi:
    print('-- Multiselect ' + str(multi.index(c) + 1) + '. ' + str(c))

print(' ')
print('***')
print(' ')


# **
