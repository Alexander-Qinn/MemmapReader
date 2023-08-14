# MemmapReader
## Background

I completed this as a joint project with 欧阳俊 in order to increase file reading and writing speed when compared to using the standard pandas pickle library. I have created this in order to more effectively organize data in for backtesting purposes since the functions for this memorymap should run at linear time. In order to use this repo, you need to have numpy and pandas installed.

## What is it?

This is a memory map data structure, implemented from scratch,that directly allocates memory and uses the numpy.flush() function to directly write changes from the array to the disk. In doing so, this becomes a very useful data structure to utilize in order to write and read files in linear time, saving processing speed for a multitude of data management processes. This file will include functions for Reading the data from some start to end, Saving the dataframe from some path into a pandas dataframe, Updating existing values of a dataframe with data from some dataframe, as well as upserting a process which we update data from existing points and insert new data points for those that don't exist. This also saves the data into the dataframe into the data type we desire, including int8 -> int64, uint8 -> uint64, float16 -> float64 and boolean.

## How does it work?

## Example Usages
To use the functions, we need to call the function in regards to an alias, in the case of the examples below we will be using M2D_F4, but you can replace that part of each function call with any alias in the M2D.py file.

Before we test our code, we are given a pkl file at some path and when converted to a pandas dataframe will look like:
#### Input:
```
if __name__ == '__main__':
  pandas_dataframe = pd.read_pickle(path_to_pklfile)
  print(close)
```
#### Output:
```
           20150105   20150106  20150107  20150108  20150109
000001.SZ     16.02  15.780000     15.48     14.96     15.08
000002.SZ     14.91  14.360000     14.23     13.59     13.45
000004.SZ     15.69  16.459999     16.41     16.92     16.43
000005.SZ       NaN        NaN       NaN       NaN       NaN
000006.SZ      7.08   6.850000      6.86      6.78      6.70
```

### .\_\_read__()
This will read the file from the path from column sd to column ed and return a pandas dataframe

#### Input:
```
if __name__ == '__main__':
  pandas_dataframe = M2D_F4.__read__(filepath) 
  print(pandas_dataframe)
```
#### Output:
```
           20150105   20150106  20150107  20150108  20150109
000001.SZ     16.02  15.780000     15.48     14.96     15.08
000002.SZ     14.91  14.360000     14.23     13.59     13.45
000004.SZ     15.69  16.459999     16.41     16.92     16.43
000005.SZ       NaN        NaN       NaN       NaN       NaN
000006.SZ      7.08   6.850000      6.86      6.78      6.70
```

#### Input:
```
if __name__ == '__main__':
  pandas_dataframe = M2D_F4.__read__(filepath, 20150106, 20150108) 
  print(pandas_dataframe)
```
#### Output:
```
            20150106  20150107  20150108
000001.SZ  15.780000     15.48     14.96
000002.SZ  14.360000     14.23     13.59
000004.SZ  16.459999     16.41     16.92
000005.SZ        NaN       NaN       NaN
000006.SZ   6.850000      6.86      6.78
```

### .\_\_save__()
This will save the pandas_dataframe into some file path as a .m2d file (ie. [filename].m2d_f4)
#### Input:
```
if __name__ == '__main__':
  pandas_dataframe = M2D_F4.__read__(filepath, 20150106, 20150108) 
  pandas_dataframe = M2D_F4.__save__(pandas_dataframe, newfilepath) 
  print(M2D_F4.__read__(newfilepath)) #This file can now be read by the read function.
```
#### Output:
```
            20150106  20150107  20150108
000001.SZ  15.780000     15.48     14.96
000002.SZ  14.360000     14.23     13.59
000004.SZ  16.459999     16.41     16.92
000005.SZ        NaN       NaN       NaN
000006.SZ   6.850000      6.86      6.78
```

#### Input:
```
if __name__ == '__main__':
  pandas_dataframe = M2D_F4.__read__(filepath, 20150106, 20150108) 
  pandas_dataframe = M2D_F4.__save__(pandas_dataframe.iloc[0:2,:], newfilepath) 
  print(M2D_F4.__read__(newfilepath)) #This file can now be read by the read function.
```
#### Output:
```
           20150106  20150107  20150108
000001.SZ     15.78     15.48     14.96
000002.SZ     14.36     14.23     13.59

```

#### Input:
```
if __name__ == '__main__':
  pandas_dataframe = M2D_F4.__read__(filepath, 20150106, 20150109) 
  pandas_dataframe = M2D_F4.__save__(pandas_dataframe.iloc[0:2,:], newfilepath) 
  print(M2D_F4.__read__(newfilepath)) #This file can now be read by the read function.
```
#### Output:
```
           20150106  20150107  20150108  20150109
000001.SZ     15.78     15.48     14.96     15.08
000002.SZ     14.36     14.23     13.59     13.45

```

### .\_\_update__()
This will compare the dataframe and the m2d file corresponding to path and update all values with corresponding index, column to the updated dataframes values.

#### Input:
```
if __name__ == '__main__':
  pandas_dataframe = M2D_F4.__read__(filepath, 20150106, 20150109)
  updater = pandas_dataframe
  updater.iloc[0:1,:] = np.nan
  pandas_dataframe = M2D_F4.__update__(updater, filepath) 
  print(M2D_F4.__read__(filepath))
```
#### Output:
```
           20150105   20150106  20150107  20150108  20150109
000001.SZ       NaN        NaN       NaN       NaN       NaN
000002.SZ     14.91  14.360000     14.23     13.59     13.45
000004.SZ     15.69  16.459999     16.41     16.92     16.43
000005.SZ       NaN        NaN       NaN       NaN       NaN
000006.SZ      7.08   6.850000      6.86      6.78      6.70
```

### .\_\_upsert__()
This does the same thing as update, except if a index column pair in the pandas_dataframe doesn't exist in the file then it simply adds that value into the dataframe as a new row column pair.

#### Input:
```
if __name__ == '__main__':
  pandas_dataframe = M2D_F4.__read__(filepath, 20150106, 20150109)
  updater = pandas_dataframe.iloc[:,[0,2]].copy()
  updater.loc['test',:] = np.nan
  updater.loc[:,:] = 999
  M2D_F4.__upsert__(updater, path = filepath)
  print(M2D_F4.__read__(filepath))
```
#### Output:
```
           20150105   20150106  20150107  20150108  20150109
000001.SZ     999.0  15.780000     999.0     14.96     15.08
000002.SZ     999.0  14.360000     999.0     13.59     13.45
000004.SZ     999.0  16.459999     999.0     16.92     16.43
000005.SZ     999.0        NaN     999.0       NaN       NaN
000006.SZ     999.0   6.850000     999.0      6.78      6.70
test          999.0        NaN     999.0       NaN       NaN
```

If you want to change the index and column labels or data types manually modify the dtype to whatever you need. In this instance SYMBOL_DTYPE is the index datatype and DATE_TYPE is the columns. For now the default has the index as Strings and the columns as ints, this is because the original version was meant for time-series stock data:

```
HEADER_DTYPE = np.dtype('U33')
SIZE_DTYPE = np.dtype('uint32')
SYMBOL_DTYPE = np.dtype('U9')
DATE_TYPE = np.dtype('uint32')
DATA_DTYPE = np.dtype('float32')
```

