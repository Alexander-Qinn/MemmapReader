# MemmapReader
## Background

I completed this as a joint project with ______ in order to increase file reading and writing speed when compared to using the standard pandas pickle library. I have created this in order to more effectively organize data in for backtesting purposes since the functions for this memorymap should run at linear time.

## What is it?

This is a memory map data structure, implemented from scratch,that directly allocates memory and uses the numpy.flush() function to directly write changes from the array to the disk. In doing so, this becomes a very useful data structure to utilize in order to write and read files in linear time, saving processing speed for a multitude of data management processes. This file will include functions for Reading the data from some start to end, Saving the dataframe from some path into a pandas dataframe, Updating existing values of a dataframe with data from some dataframe, as well as upserting a process which we update data from existing points and insert new data points for those that don't exist. This also saves the data into the dataframe into the data type we desire, including int8 -> int64, uint8 -> uint64, float16 -> float64 and boolean.

## How does it work?

