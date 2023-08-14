#!/usr/bin/env python


################################ system lib ##########################################
import os, sys
from pickle import TRUE
os.environ['OPENBLAS_NUM_THREADS'] = '1'
import pandas as pd
import numpy as np
from map.Map import Map
##########################################################################


class M2D(Map):
    """ 
    Float data 2D map
    """
    HEADER_DTYPE = np.dtype('U33')
    SIZE_DTYPE = np.dtype('uint32')
    SYMBOL_DTYPE = np.dtype('U9')
    DATE_TYPE = np.dtype('uint32')
    DATA_DTYPE = np.dtype('float32')
    
    # EXT_NAME = 'f2d'
    
    @classmethod
    def __fp__(cls, path: str, section: str, mode: str):
        try:
            # 0. read dtype
            offset = 0
            fp = np.memmap(path, dtype=cls.HEADER_DTYPE, offset=offset, mode='r', shape = (4))
            dtypes = tuple(fp)
            del fp
            # 1. read size 
            offset = 4 * cls.HEADER_DTYPE.itemsize
            fp = np.memmap(path, dtype=cls.SIZE_DTYPE, offset=offset, mode='r', shape = (2))
            m , n  = tuple(fp)
            del fp
            if section == 0:
                offset = 4 * cls.HEADER_DTYPE.itemsize
                fp = np.memmap(path, dtype=cls.SIZE_DTYPE, offset=offset, mode=mode, shape = (2))
                return (fp, 2)
            elif section == 1:
                offset = 4 * cls.HEADER_DTYPE.itemsize+2 * cls.SIZE_DTYPE.itemsize
                fp = np.memmap(path, dtype=cls.SYMBOL_DTYPE, mode=mode, offset = offset,  shape = m)
                return (fp, m)
            elif section == 2:
                offset = 4 * cls.HEADER_DTYPE.itemsize+2 * cls.SIZE_DTYPE.itemsize + m * cls.SYMBOL_DTYPE.itemsize
                fp = np.memmap(path, dtype=cls.DATE_TYPE, mode=mode, offset = offset,  shape = n)
                return (fp, n)
            elif section == 3:
                offset = 4 * cls.HEADER_DTYPE.itemsize+2 * cls.SIZE_DTYPE.itemsize+\
                    m * cls.SYMBOL_DTYPE.itemsize + n * cls.DATE_TYPE.itemsize
                fp = np.memmap(path, dtype=cls.DATA_DTYPE, mode=mode, offset = offset,  shape = (m,n))
                return (fp, (m,n))
            
        except Exception as e:
            print(e)
            return None
        
    @classmethod
    def __save__(cls, df:pd.DataFrame, path: str):
        """index is symbols[str](will be truncated to U9), columns is dates[int], data point is float

        Args:
            df (pd.DataFrame): 
            
                       20090105  20090106  20090107  20090108  20090109  20090112  
            000001.SZ      9.71      10.3      9.99      9.60      9.85      9.86   
            000002.SZ      6.70       6.9      6.86      6.90      6.89      6.81   
            000004.SZ      3.69       3.8      3.99      4.19      4.35      4.26   

            path (str): path: alpha_name.jmap
        """
        try:
            assert df.index.is_object(), "index must be symbols[str] "
            assert df.columns.is_integer(), "column must be dates[int] "
            # sort dataframe by index:symbol and column:date
            df.sort_index(axis = 0, inplace =True)
            df.sort_index(axis = 1, inplace =True)

            # 0. save dtype
            offset = 0
            fp = np.memmap(path, dtype=cls.HEADER_DTYPE, offset=offset, mode='w+', shape = (4))
            fp[:] = [str(cls.SIZE_DTYPE), str(cls.SYMBOL_DTYPE),str(cls.DATE_TYPE),str(cls.DATA_DTYPE)]
            fp.flush()
            del fp
            
            # 1. save size 
            offset = 4 * cls.HEADER_DTYPE.itemsize 
            fp = np.memmap(path, dtype=cls.SIZE_DTYPE, offset=offset, mode='r+', shape = (2))
            fp[:] = df.shape
            fp.flush()
            del fp

            # 2. save symbol 
            offset = 4 * cls.HEADER_DTYPE.itemsize+2 * cls.SIZE_DTYPE.itemsize
            fp = np.memmap(path, dtype=cls.SYMBOL_DTYPE, mode='r+', offset = offset,  shape = df.shape[0])
            fp[:] = df.index.values.astype(cls.SYMBOL_DTYPE)
            fp.flush()
            del fp
            
            # 3. save date 
            offset = 4 * cls.HEADER_DTYPE.itemsize+2 * cls.SIZE_DTYPE.itemsize+  df.shape[0] * cls.SYMBOL_DTYPE.itemsize
            fp = np.memmap(path, dtype=cls.DATE_TYPE, mode='r+', offset = offset,  shape = df.shape[1])
            fp[:] = df.columns.values.astype(cls.DATE_TYPE)
            fp.flush()
            del fp
            
            # 4. save data 
            offset = 4 * cls.HEADER_DTYPE.itemsize+2 * cls.SIZE_DTYPE.itemsize+  \
                df.shape[0] * cls.SYMBOL_DTYPE.itemsize + df.shape[1] * cls.DATE_TYPE.itemsize
            fp = np.memmap(path, dtype=cls.DATA_DTYPE, mode='r+', offset = offset,  shape = df.shape)
            fp[:] = df.values.astype(cls.DATA_DTYPE)
            fp.flush()
            del fp
            return True
        except Exception as e:
            print(e)
            return False
        
    @classmethod
    def __update__(cls, df:pd.DataFrame, path: str):
        """only update number within the jmap. do not create new data point, will overrite all data
        Args:
            df (pd.DataFrame): 
            
                       20090105  20090106  20090107  20090108  20090109  20090112  
            000001.SZ      9.71      10.3      9.99      9.60      9.85      9.86   
            000002.SZ      6.70       6.9      6.86      6.90      6.89      6.81   
            000004.SZ      3.69       3.8      3.99      4.19      4.35      4.26   

            path (str): path: alpha_name.jmap
        """
        try:
            assert df.index.is_object(), "index must be symbols[str] "
            assert df.columns.is_integer(), "column must be dates[int] "
            
            # 0. save dtype
            offset = 0
            fp = np.memmap(path, dtype=cls.HEADER_DTYPE, offset=offset, mode='r', shape = (4))
            dtypes = tuple(fp)
            del fp
            
            # 1. read size 
            offset = 4 * cls.HEADER_DTYPE.itemsize 
            fp = np.memmap(path, dtype=cls.SIZE_DTYPE, offset=offset, mode='r', shape = (2))
            m , n  = tuple(fp)
            del fp

            # 2. read symbol 
            offset = 4 * cls.HEADER_DTYPE.itemsize +2 * cls.SIZE_DTYPE.itemsize
            fp = np.memmap(path, dtype=cls.SYMBOL_DTYPE, mode='r', offset = offset,  shape = m)
            symbols = np.array(fp)
            del fp
            
            # 3. read date 
            offset = 4 * cls.HEADER_DTYPE.itemsize +2 * cls.SIZE_DTYPE.itemsize + m * cls.SYMBOL_DTYPE.itemsize
            fp = np.memmap(path, dtype=cls.DATE_TYPE, mode='r', offset = offset,  shape = n)
            dates = np.array(fp)
            del fp
            
            # filter dataframe
            df_filtered = df.loc[df.index.isin(symbols), df.columns.isin(dates)]
            
            
            # 4. read data 
            offset = 4 * cls.HEADER_DTYPE.itemsize +2 * cls.SIZE_DTYPE.itemsize+ \
                m * cls.SYMBOL_DTYPE.itemsize + n * cls.DATE_TYPE.itemsize
            fp = np.memmap(path, dtype=cls.DATA_DTYPE, mode='r+', offset = offset,  shape = (m,n))

            filter_index = exact_searchsorted(symbols, df_filtered.index)
            assert np.all(filter_index>=0), "unknow index exists when update jmap"
            filter_columns = exact_searchsorted(dates, df_filtered.columns)
            assert np.all(filter_index>=0), "unknow column exists when update jmap"
            for i,j in zip(filter_columns,range(len(df_filtered.columns))):
                fp[filter_index,i] = df_filtered.values[filter_index,j].astype(cls.DATA_DTYPE)
            del fp
            return True
        except Exception as e:
            print(e)
            return False   
        
    @classmethod
    def __upsert__(cls, df:pd.DataFrame, path: str):
        """upsert data, write all new data into jmap. will create new data point

        Args:
            df (pd.DataFrame): 
            
                       20090105  20090106  20090107  20090108  20090109  20090112  
            000001.SZ      9.71      10.3      9.99      9.60      9.85      9.86   
            000002.SZ      6.70       6.9      6.86      6.90      6.89      6.81   
            000004.SZ      3.69       3.8      3.99      4.19      4.35      4.26   

            path (str): path: alpha_name.jmap
        """
        try:
            assert df.index.is_object(), "index must be symbols[str] "
            assert df.columns.is_integer(), "column must be dates[int] "
            df.columns = df.columns.astype('uint')
            old_df = cls.__read__(path)
            
            # new_index = list(df.index.values[exact_searchsorted(old_df.index.values, df.index.values)<0])
            # new_column = list(df.columns.values[exact_searchsorted(old_df.columns.values, df.columns.values)<0])
            new_index =  np.sort(pd.Series(np.concatenate([old_df.index.values, df.index.values])).unique())
            new_column = np.sort(pd.Series(np.concatenate([old_df.columns.values, df.columns.values])).unique())
            new_df = old_df.reindex(index = new_index, columns = new_column, copy = True)
            new_df.update(df, overwrite=True)
            return cls.__save__(new_df, path)
        except Exception as e:
            print(e)
            return False      
    
    @classmethod
    def __read__(cls, path: str ,sd = None, ed = None)-> pd.DataFrame: 
        
        """_summary_

        Args:
            df (pd.DataFrame): 
            
                       20090105  20090106  20090107  20090108  20090109  20090112  
            000001.SZ      9.71      10.3      9.99      9.60      9.85      9.86   
            000002.SZ      6.70       6.9      6.86      6.90      6.89      6.81   
            000004.SZ      3.69       3.8      3.99      4.19      4.35      4.26   

            path (str): path: alpha_name.jmap
        """
        try:
            # 0. save dtype
            offset = 0
            fp = np.memmap(path, dtype=cls.HEADER_DTYPE, offset=offset, mode='r', shape = (4))
            a = 1
            dtypes = tuple(fp)
            del fp
            
            # 1. read size 
            offset = 4 * cls.HEADER_DTYPE.itemsize
            fp = np.memmap(path, dtype=cls.SIZE_DTYPE, offset=offset, mode='r', shape = (2))
            m , n  = tuple(fp)
            del fp

            # 2. read symbol 
            offset = 4 * cls.HEADER_DTYPE.itemsize+2 * cls.SIZE_DTYPE.itemsize
            fp = np.memmap(path, dtype=cls.SYMBOL_DTYPE, mode='r', offset = offset,  shape = m)
            symbols = np.array(fp)
            del fp
           
            # 3. read date 
            #myList3 = []
            #myList4 = []
            #for i in range(100):
            #start = time.time()
            offset = 4 * cls.HEADER_DTYPE.itemsize+2 * cls.SIZE_DTYPE.itemsize + m * cls.SYMBOL_DTYPE.itemsize
            fp = np.memmap(path, dtype=cls.DATE_TYPE, mode='r', offset = offset,  shape = n)
            dates = np.array(fp)
            #end = time.time()
            #exeTime1 = end - start
            #myList3.append(exeTime1)
            del fp
                
            # 4. read data 
            #start = time.time()
            offset = 4 * cls.HEADER_DTYPE.itemsize+2 * cls.SIZE_DTYPE.itemsize+ \
                m * cls.SYMBOL_DTYPE.itemsize + n * cls.DATE_TYPE.itemsize
            fp = np.memmap(path, dtype=cls.DATA_DTYPE, mode='r', offset = offset,  shape = (m,n))
            sd_idx = 0
            ed_idx = None
            if not (sd is None): sd_idx = np.searchsorted(dates, sd, side ='left') 
            if not (ed is None): ed_idx = np.searchsorted(dates, ed, side ='right') 
            data = np.array(fp[:,sd_idx:ed_idx])
            del fp
            df = pd.DataFrame(data, index = symbols, columns = dates[sd_idx:ed_idx])
            return df
        except Exception as e:
            print(e)
            return None
        
    def __init__(self, path):
        self.path = path 
        
        # fp
        self._size_fp = self.__class__.__fp__(self.path, 0, 'r')[0]
        self._symbol_fp = self.__class__.__fp__(self.path, 1, 'r')[0]
        self._date_fp = self.__class__.__fp__(self.path, 2, 'r')[0]
        self._data_fp = self.__class__.__fp__(self.path, 3, 'r')[0]
        
        # size
        self.size =  tuple(self._size_fp)
        # symbol
        self.symbols =  np.array(self._symbol_fp)
        # date
        self.dates = np.array(self._data_fp)
        
        self.counter = 0
        
    def save(self,df):
        return self.__class__.__save__(df, self.path)  
    
    def update(self,df):
        return self.__class__.__update__(df, self.path)  
    
    def upsert(self,df):
        return self.__class__.__upsert__(df, self.path)  
    
    def read(self,sd = None, ed = None):
        return self.__class__.__read__(self.path, sd, ed)   
    
    def get_n(self, n=0):
        if n < self.size[1]:
            return np.array(self._data_fp[:,-n-1]) 
        else:
            return None
    
    def get(self):
        data = self.get_n(self.counter)
        self.counter += 1
        return data

