import pandas as pd

df = pd.read_csv('light_sensor_data.csv')
df.rename(columns={'created_at': 'date', 'field1': 'ldr', 'field2': 'red', 'field3': 'green', 'field4': 'blue'}, inplace=True) # rename columns as desired
df['time'] = ' ' # create new time column
df = df[['date', 'time', 'ldr', 'red', 'green', 'blue']] # reorder columns

df = df.values.tolist()
print(df)


def convert_date(df):
    # format datetime into date and time values
    for row in df:
        reading = row[0]
        
        reading_date = reading[8:10] + '/' + reading[5:7] + '/' + reading[0:4]
        reading_time = reading[11:13] + ':' + reading[14:16]
        
        # set date and time in correct column
        row[0] = reading_date
        row[1] = reading_time
    
    return df


def reduce_data(df):
    
    prev_val = '00:00'
    delete_rows = []
    
    for row in df:
        if row[1] == prev_val: # removing all duplicate values for the same minute interval
            delete_rows.append(df.index(row)) # adding to a list of rows to be deleted, as is being iterated through so cannot change here
        prev_val = row[1]
    
    return delete_rows



delete_rows = reduce_data(df)
delete_rows.reverse()

for val in delete_rows:
    del df[val] # deleting duplicate time entries

df_ = pd.DataFrame (df,columns =['date', 'time', 'ldr', 'red', 'green', 'blue']) # create dataframe
df_.to_csv('sensor_data.csv') # export as csv