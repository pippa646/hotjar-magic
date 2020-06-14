# hotjar-magic

Ever run a survey on HotJar with a checkbox question, and then found it hard to analyse the download file for questions factoring in multiple columns?

I've created this little bit of code to help. Download your HotJar data as a CSV, then run hotjar-magic.py to get the multiple-response answers from  single-column, multiple-row format to True/False columns for every possible answer. No more blank rows; all the responses from one user will be in a single row.

The CSV you get will make it much easier to answer questions that combine single- and multiple-response answers. 

Happy analysing!

-------

Here are the steps the script takes:

1. Installs the extra Python packages needed (numpy, pandas, and math).
2. Asks the user for the location of the CSV file to import, and imports it as a pandas DataFrame.
3. Prints out some information about the file (e.g. column numbers and rows).
4. Identifies columns that correspond to multiple-response questions, by seeing if other cells in the same row are blank; prints out the title of these columns.
5. For each of these multiple-response columns, finds all possible unique values — except blank values and any answers that contain ‘Other’ (as this is usually how I specify free text answers).
6. For each of these unique values, the script creates a brand new column in the file, labelled in the format ms_1_blueberry (multiselect, multiselect column 1, unique value).
7. For each of these columns, all values are set to False.
8. Go down the first column (where the response ID number is); for any blank value, take the response ID from the row above. This means every multiple-response answer has a corresponding response ID
9. For each response ID, look at the multiple select columns; wherever the answer matches one of the new columns, update its value to True for the first row where the response ID appears (as they’re all in numeric order)
10. Clear out all the unnecessary rows created by the original file format, reducing it to one row per user response
11. Clear out the old multiselect columns as they’re no longer needed
12. Export the data as a CSV to a user’s chosen file path.
