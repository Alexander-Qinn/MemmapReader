from Memmap2Dim import *

##########################################################################    
""" np.bool """
class M2D_B(M2D):
    """ 
    bool data 2D map
    """
    DATA_DTYPE = np.dtype('bool')
    
    EXT_NAME = 'm2d_b' 

##########################################################################
""" np.int8 """
class M2D_I1(M2D):
    """ 
    int8 data 2D map
    """
    DATA_DTYPE = np.dtype('int8')
    
    EXT_NAME = 'm2d_i1'
    
""" np.int16 """
class M2D_I2(M2D):
    """ 
    int16 data 2D map
    """
    DATA_DTYPE = np.dtype('int16')
    
    EXT_NAME = 'm2d_i2'
    
""" np.int32 """
class M2D_I4(M2D):
    """ 
    int32 data 2D map
    """
    DATA_DTYPE = np.dtype('int32')
    
    EXT_NAME = 'm2d_i4'
    
""" np.int64 """
class M2D_I8(M2D):
    """ 
    int64 data 2D map
    """
    DATA_DTYPE = np.dtype('int64')
    
    EXT_NAME = 'm2d_i8'
    
##########################################################################
""" np.uint8 """
class M2D_U1(M2D):
    """ 
    uint8 data 2D map
    """
    DATA_DTYPE = np.dtype('uint8')
    
    EXT_NAME = 'm2d_u1'
    
""" np.uint16 """
class M2D_U2(M2D):
    """ 
    uint16 data 2D map
    """
    DATA_DTYPE = np.dtype('uint16')
    
    EXT_NAME = 'm2d_u2'
    
""" np.uint32 """
class M2D_U4(M2D):
    """ 
    uint32 data 2D map
    """
    DATA_DTYPE = np.dtype('uint32')
    
    EXT_NAME = 'm2d_u4'
    
""" np.uint64 """
class M2D_U8(M2D):
    """ 
    uint64 data 2D map
    """
    DATA_DTYPE = np.dtype('uint64')
    
    EXT_NAME = 'm2d_u8'
    
##########################################################################
""" np.float16 """
class M2D_F2(M2D):
    """ 
    float16 data 2D map
    """
    DATA_DTYPE = np.dtype('float16')
    
    EXT_NAME = 'm2d_f2'
    
""" np.float32 """
class M2D_F4(M2D):
    """ 
    float32 data 2D map
    """
    DATA_DTYPE = np.dtype('float32')
    
    EXT_NAME = '.m2d_f4'
   
""" np.float64 """
class M2D_F8(M2D):
    """ 
    float64 data 2D map
    """
    DATA_DTYPE = np.dtype('float64')
    
    EXT_NAME = 'm2d_f8' 