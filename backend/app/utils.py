import hashlib
import os

def md5(raw_password):
    return hashlib.md5(raw_password.encode('utf-8')).hexdigest()


def to_dict(self):
    return {c.name: getattr(self, c.name) for c in self.__table__.columns}


def rand_str():
    """生成随机字符串"""
    m = hashlib.md5()
    m.update(os.urandom(32)) 
    return m.hexdigest()


def dict_to_url(paraMap, urlencode=True):
    slist = sorted(paraMap)
    buff = []
    for k in slist:
        value = paraMap[k]
        if isinstance(value, dict):
            v = str(value)
        elif isinstance(value, bytes):
            v = str(value) 
        elif value:
            v = value 
        else:
            del paraMap[k]
            continue
  
        buff.append("{0}={1}".format(k, v))

    return "&".join(buff)


def mk_sign(params):
    """字符串转sign
    """
    m = hashlib.md5(params.encode('utf-8')).hexdigest()
    sign = m.upper()
    return sign


def trans_xml_to_dict(xml):
  from bs4 import BeautifulSoup
  """
  将微信支付交互返回的 XML 格式数据转化为 Python Dict 对象
 
  :param xml: 原始 XML 格式数据
  :return: dict 对象
  """
 
  soup = BeautifulSoup(xml, features='xml')
  xml = soup.find('xml')
  if not xml:
    return {}
 
  # 将 XML 数据转化为 Dict
  data = dict([(item.name, item.text) for item in xml.find_all()])
  return data



def trans_dict_to_xml(data):
  """
  将 dict 对象转换成微信支付交互所需的 XML 格式数据
 
  :param data: dict 对象
  :return: xml 格式数据
  """
 
  xml = []
  for k in sorted(data.keys()):
    v = data.get(k)
    if k == 'detail' and not v.startswith('<![CDATA['):
      v = '<![CDATA[{}]]>'.format(v)
    xml.append('<{key}>{value}</{key}>'.format(key=k, value=v))
  return '<xml>{}</xml>'.format(''.join(xml))



