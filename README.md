# MemmapReader
## Background

I completed this as a joint project with 欧阳俊 in order to increase file reading and writing speed when compared to using the standard pandas pickle library. I have created this in order to more effectively organize data in for backtesting purposes since the functions for this memorymap should run at linear time. In order to use this repo, you need to have numpy and pandas installed.

## What is it?

This is a memory map data structure, implemented from scratch,that directly allocates memory and uses the numpy.flush() function to directly write changes from the array to the disk. In doing so, this becomes a very useful data structure to utilize in order to write and read files in linear time, saving processing speed for a multitude of data management processes. This file will include functions for Reading the data from some start to end, Saving the dataframe from some path into a pandas dataframe, Updating existing values of a dataframe with data from some dataframe, as well as upserting a process which we update data from existing points and insert new data points for those that don't exist. This also saves the data into the dataframe into the data type we desire, including int8 -> int64, uint8 -> uint64, float16 -> float64 and boolean.

## How does it work?

## Example Usages
To use the functions, we need to call the function in regards to an alias, in the case of the examples below we will be using M2D_F4, but you can replace that part of each function call with any alias in the M2D.py file.

```
if __name__ == '__main__':
  pandas_dataframe = M2D.__read__(path, sd, ed)
  print(pandas_dataframe)
  
  pandas_dataframe = M2D.__save__(path, sd, ed)
  print(pandas_dataframe)
  
  pandas_dataframe = M2D.__upsert__(path, sd, ed)
  print(pandas_dataframe)
  
  pandas_dataframe = M2D.__update__(path, sd, ed)
  print(pandas_dataframe)
```

If you want to change the index and column labels or data types manually:

```
HEADER_DTYPE = np.dtype('U33')
SIZE_DTYPE = np.dtype('uint32')
SYMBOL_DTYPE = np.dtype('U9')
DATE_TYPE = np.dtype('uint32')
DATA_DTYPE = np.dtype('float32')
```
simply modify the dtype to whatever you need. In this instance SYMBOL_DTYPE is the index datatype and DATE_TYPE is the columns.
For now the default has the index as Strings and the columns as ints, this is because the original version was meant for time-series stock data.

