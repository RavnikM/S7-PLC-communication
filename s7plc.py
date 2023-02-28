import ctypes

import snap7
from snap7.common import check_error
from snap7.types import S7DataItem, S7AreaDB, S7WLByte
client = snap7.client.Client()
client.connect('192.168.110.5', 0, 1)

# Byte index    Variable name  Datatype
read_db_num = 3
read_db_layout = """
0	          REQ            INT
2             COMPLETE	     INT
4             ID             INT
6.0           data_bool      BOOL
8             data_str       STRING[255]
264           data_real      REAL
268           data_int       INT
270           data_date      DATE
"""

write_db_num = 4
write_db_layout = """
0	          REQ            INT
2             COMPLETE	     INT
4             ID             INT
6.0           data_bool      BOOL
8             data_str       STRING[255]
264           data_real      REAL
268           data_int       INT
270           data_date      DATE
"""

all_data_read = client.db_read(read_db_num,0,270+2)
all_data_write = client.db_read(write_db_num,0,270+2)

db_read = snap7.util.DB(
        read_db_num,            # the db we use
        all_data_read,          # bytearray from the plc
        read_db_layout,         # layout specification DB variable data
                                # A DB specification is the specification of a
                                # DB object in the PLC you can find it using
                                # the dataview option on a DB object in PCS7

        270+2,                   # size of the specification 17 is start
                                # of last value
                                # which is a DWORD which is 2 bytes,

        1,                      # number of row's / specifications
        layout_offset=0,        # sometimes specification does not start a 0
                                # like in our example
        db_offset=0             # At which point in 'all_data' should we start
                                # reading. if could be that the specification
                                # does not start at 0
    )

db_write = snap7.util.DB(
        write_db_num,           # the db we use
        all_data_write,         # bytearray from the plc
        write_db_layout,        # layout specification DB variable data
                                # A DB specification is the specification of a
                                # DB object in the PLC you can find it using
                                # the dataview option on a DB object in PCS7

        270+2,                  # size of the specification 17 is start
                                # of last value
                                # which is a DWORD which is 2 bytes,

        1,                      # number of row's / specifications
        layout_offset=0,        # sometimes specification does not start a 0
                                # like in our example
        db_offset=0             # At which point in 'all_data' should we start
                                # reading. if could be that the specification
                                # does not start at 0
    )

print(db_write[0])
db_write[0].read(client)
db_write[0]
db_write[0]['data_bool'] = False
db_write[0].write(client)

