import re

text = '{m_x:123}{m_x:3}cde'
text = '{m_x:1998,m_y:41,m_text:citations:41 (year 1998),m_Visible:true}'

m = re.findall('{m_x:.*?,m_y:.*?,m_text:citations.*?}', text)

# m_x:1998,m_y:41,m_text:citations:41 (year 1998),m_Visible:true',

print m