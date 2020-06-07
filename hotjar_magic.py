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

# 1. Install pandas and math
# ---------------------------------

# If you're using Jupyter Notebooks, uncomment this first part

# Install a conda package in the current Jupyter kernel
# import sys
# !conda install --yes --prefix {sys.prefix} pandas

# Import pandas
import pandas as pd

# Import math
import math

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


# 4. Identify any multiselect columns; print them out and create a list
# ---------------------------------------------------------------------

# Create an empty list called 'multi'

multi = []

# Print the introductory statement

print("The multi-select columns are...")
print('-------------------------------')

# Iterate over the data

for label, row in data.iterrows() :
    
# Check if the first value in the row is NaN; if so, any non-NaN values in that row belong to a multiselect column

    if math.isnan(data.iat[label, 0]) == True :

# Iterate over the values in the row (as a list)        

        for m in row.tolist() :
            if type(m) != float :
                if data.columns[row.tolist().index(m)] not in multi : 
                    multi.append(data.columns[row.tolist().index(m)])
                    print('-- ' + str(data.columns[row.tolist().index(m)]))
            elif math.isnan(m) == False :
                if data.columns[row.tolist().index(m)] not in multi : 
                    multi.append(data.columns[row.tolist().index(m)])
                    print('-- ' + str(data.columns[row.tolist().index(m)]))

print(' ')
print('***')
print(' ')

# **


# 5. Identify unique values in a multiselect column, removing NaN and any 'Other' answers
# ---------------------------------------------------------------------------------------

# Iterate over all values in multi

for y in multi :
    
# Print introductory statement

    print("The unique column values in " + str(y) + " are: ")
    
# Create a blank list for unique column values

    unique_col = []

# Iterate over the unique values in each multiselect column, as a list

    for x in data[y].unique().tolist() :

# Don't add any NaN values
    
        if type(x) == float :
            if math.isnan(x) == False :
                unique_col.append(x)
        
# Don't add string values that contain 'Other', so we don't get a new column for any free text answers

        elif type(x) == str :
            if 'Other' not in str(x) :
                unique_col.append(x)
        
# Print each value

    for u in unique_col :
        print('-- ' + str(u))
    
    print(' ')
    print('***')
    print(' ')

# **


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


# 7. Edit the response ID column so every multiselect value has a corresponding ID
# --------------------------------------------------------------------------------

# Iterate over data

for label, row in data.iterrows() :

# Look for NaN values in the first column; replace any NaN values with the value of the row above

    if math.isnan(data.iat[label, 0]) == True :
        data.iat[label, 0] = data.iat[label - 1, 0]

# Print confirmation

print('Response ID values updated so every multiselect value has one...')

print(' ')
print('***')
print(' ')

# **


# 8. Update the first row of each response to have the correct Boolean values for each multiselect answer
# -------------------------------------------------------------------------------------------------------

# Set value of id_list

id_list = data.iloc[:, 0].unique().tolist()

# For each response ID...

for i in id_list :
    
# Generate a subset table...

    subset = data.loc[data[data.columns[0]] == i]

# Create a list of all the row labels in that subset (set as blank to start)
    
    label_list = []

# Iterate over the subset table...

    for label, row in subset.iterrows() :

# Add each row label you iterate over to the list...
        
        label_list.append(label)

# Then, for each multiselect column...
        
        for y in multi :
            
# Set Boolean column label

            bool_col = "ms_" + str(multi.index(y) + 1) + "_" + str(subset.at[label, y]).lower()

# Set Boolean column value, as long as it's not a NaN value

# If the value in the multiselect column isn't a float, it's not a NaN value: proceed

            if type(subset.at[label, y]) != float :

# Set value at the corresponding column to True

                data.at[label_list[0], bool_col] = True

# Or, if the multiselect column value is a float but isn't NaN, proceed: 

            elif math.isnan(subset.at[label, y]) == False :

# Set value at the corresponding column to True

                data.at[label_list[0], bool_col] = True

# Print confirmation

print('New columns updated with True wherever user selected it...')

print(' ')
print('***')
print(' ')

# **


# 9. Clear unnecessary rows
# -------------------------

# We now don't need the additional rows, and can cut the data down to just one row per response ID. Such a nice, simple function after all that iterating!

data.drop_duplicates(subset = data.columns[0], keep = 'first', inplace = True)


# Print confirmation

print('Unnecessary rows deleted...')
print("The data file now has " + str(len(data)) + " rows, and " + str(len(data.columns)) + " columns.")

print(' ')
print('***')
print(' ')

# **


# 10. Clear unnecessary columns
# ----------------------------

# We now don't need the multiselect columns, either. An even shorter, lovely function!

data = data.drop(multi, axis=1)

# Print confirmation

print('Unnecessary columns deleted...')
print("The data file now has " + str(len(data)) + " rows, and " + str(len(data.columns)) + " columns.")

print(' ')
print('***')
print(' ')

# **

# 11. Export data
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
