import re
from pprint import pprint

import ctypes
tid = ctypes.CDLL('libc.so.6').syscall(186)
print tid

# text = '{m_x:1983,m_y:3,m_text:citations:3 (year 1983),m_Visible:true},{m_x:1984,m_y:9,m_text:citations:9 (year 1984),m_Visible:true},{m_x:1985,m_y:19,m_text:citations:19 (year 1985),m_Visible:true},{m_x:1986,m_y:33,m_text:citations:33 (year 1986),m_Visible:true},{m_x:1987,m_y:58,m_text:citations:58 (year 1987),m_Visible:true}'
# m = re.findall('{m_x:.*?,m_y:.*?,m_text:citations.*?}', text)
#
# # m_x:1998,m_y:41,m_text:citations:41 (year 1998),m_Visible:true',
#
# pprint(m)