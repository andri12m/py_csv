
import xml.etree.ElementTree as ET
import re
import sys

class Node:
  def __init__(self, name, data):
    self.name = name
    self.data = data
    self.next = None

  def __repr__(self):
    return [self.name, self.data]


class Tree:
  def __init__(self):
    self.head = None
    self.last = None

  def __repr__(self):
    node = self.head
    nodes = []
    while node is not None:
        nodes.append([node.name, node.data])
        node = node.next
    nodes.append("None")
    return " -> ".join(nodes)

  def __iter__(self):
    node = self.head
    while node is not None:
      yield node
      node = node.next

  def add_last(self, node):
    if self.head is None:
      self.head = node
      self.last = node
      return
    self.last.next = node
    self.last = node

  def add_cat(self, node):
    if self.head is None:
      self.head = node
      return
    for current_node in self:
      pass
    current_node.next = node


def cleanhtml(raw_html):
  # cleanr = re.compile('<.*?>')
  cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
  cleantext = re.sub(cleanr, '', raw_html)
  # cl = cleantext.replace('&quot', '')
  return cleantext


list_category = []
list_category_chain = []
list_offer = []

def proc_category(e):
  lens=len(e.attrib.items())
  if lens==1:
    list_category.append([e.text, e.attrib['id'], '0'])
  if lens==2:
    list_category.append([e.text, e.attrib['id'], e.attrib['parentId']])
  # print(list_category[-1])


def proc_build_category_chains():
  cur = ''
  curlist = []
  def getParentName(cat1):
    curlist.append(cat1[0])
    if cat1[2] != '0':
      for cat2 in list_category:
        if cat2[1] == cat1[2]:
          getParentName(cat2)
    return
  for cat in list_category:
    cur = ''
    curlist = []
    getParentName(cat)
    for cat3 in reversed(curlist):
      cur = cur + cat3 + ' > '
    cur = cur.replace(',',';')
    list_category_chain.append('"' + cur[:-3] + '"')
    # print(list_category_chain[-1])


file_xml = 'dat/t3.xml'
file_csv = 'dat/test.csv'
file_chunk = 'dat/tv'

etree = ET.parse(file_xml)
for e in etree.iter():
  if e.tag=='category':
    proc_category(e)
proc_build_category_chains()
print('Категорій: ', len(list_category))
# print('Categories chains: ', len(list_category_chain))


text_file = open(file_csv, "w", encoding='utf-8')
cols = 120              # 4*20 + 4*3 + 28 = 120
offer = [''] * cols      
e_count = 0
pics_count = 0
pics = ''
vend = ''
vendCode = ''
coo = ''
param_count = 0
params = []               # ['name', 'all variations']
pricetext = ''
listcat = ''
def proc_offer(pos, e):
  global offer
  global e_count
  global pics_count
  global pics
  global vend
  global vendCode
  global coo
  global param_count
  global params
  global pricetext
  global listcat
  # -------------------------------- start section
  if pos=='start':
    e_count=0
    pics_count = 0
    pics = ''    
    vend = ''
    vendCode = ''
    coo = ''
    param_count = 0
    params = []
    offer = [''] * cols
    offer[0]=''
    offer[2]=''
    # offer[2]=e.attrib['id']   # write id in sku
  # -------------------------------- e section
  if pos=='e':
    e_count = e_count + 1
    if e.tag=='price':
      pricetext = e.text
      # offer[23] = e.text
    elif e.tag=='picture':
      pics_count += 1
      pics = pics + e.text + ', '
    elif e.tag=='name':
      st = e.text
      offer[3] = '"' + (st.replace(',', ';')).replace('\"', '\'') + '"'
    elif e.tag=='categoryId':
      c = 0
      cc = 0
      cid = e.text
      for c1 in list_category:
        if c1[1]==cid:
          cc = c
          break
        c += 1
      listcat = list_category_chain[cc]
      # offer[24] = list_category_chain[cc]
    elif e.tag=='vendor':
      vend = e.text
      # then add to attrib in end section
    elif e.tag=='vendorCode':
      vendCode = e.text
      # then add to SKU in end section
    elif e.tag=='description':
      st = e.text
      st2 = st.replace('\n', ' ')
      st3 = cleanhtml(st2)
      st4 = st3.replace('\"', '\'')
      offer[8] = '"' + st4 + '"'
    elif e.tag=='country_of_origin':
      coo = e.text
      # then add to attrib in end section
    elif e.tag=='param':                   ###   MAXIMUM 20 params   ###########   4*20 + 4*3 + 28 = 120
      param_count += 1
      t1 = (e.attrib['name']).replace('\n', ' ')
      name = '"' + t1 + '"'
      t2 = (e.text).replace('\n', ' ')
      t22 = t2.replace('&quot', ' ')
      text = '"' + t22 + '"'
      params.append([name, text])
      # print(' - count: ', param_count, ' name: ', name, '  text: ', text)
      # print('   --- params -   name: ', params[-1][0], ' text: ', params[-1][1])
      # then add to attrib in end section
  # -------------------------------------------------------- end section
  if pos=='end':
    if e_count > 0:
      # offer[0] = 'id'                       # ID
      offer[1] = 'simple'                     # Type
      offer[2] = ''
      # offer[2] = vendCode                     # SKU
      # offer[3] = 'name'                     # Name
      offer[4] = '1'                          # Published
      offer[5] = '0'                          # Is featured?
      offer[6] = '"visible"'                    # Visibility in catalog
      offer[7] = ''                           # Short description
      # offer[8] = 'description'              # Description
      offer[9] = ''                           # Date sale price starts
      offer[10] = ''                          # Date sale price ends
      offer[11] = 'taxable'                   # Tax status
      offer[12] = 'standard'                  # Tax class
      offer[13] = '1'                         # In stock?
      # offer[14] = '1'                         # Stock
      # offer[15] = ''                         # Low stock amount
      offer[14] = ''                         # Backorders allowed?
      offer[15] = ''                         # Sold individually?
      offer[16] = ''                          # Weight (unit)
      offer[17] = ''                          # Length (unit)
      offer[18] = ''                          # Width (unit)
      offer[19] = ''                          # Height (unit)
      offer[20] = '1'                         # Allow customer reviews?
      offer[21] = ''                          # Purchase Note
      offer[22] = ''                          # Sale price
      offer[23] = pricetext                   # Regular price
      offer[24] = listcat                     # Categories
      offer[25] = ''                          # Tags
      offer[26] = ''                          # Shipping class
      offer[27] = '"' + pics[:-2] + '"'       # Images
      # offer[28] = ''                          # Download limit
      # offer[29] = ''                          # Download expiry days
      # offer[30] = ''                          # Parent
      # offer[31] = ''                          # Grouped products
      # offer[32] = ''                          # Upsells
      # offer[33] = ''                          # Cross-sells
      # offer[34] = ''                          # External URL
      # offer[35] = ''                          # Button text
      # offer[36] = ''                          # Position

      # attribs here:
      if vend != '':
        offer[28] = 'производитель'           # Attribute name        # offer[39]
        offer[29] = '"' + vend + '"'          # Attribute values      # vendor
        offer[30] = '1'                       # Attribute visible
        offer[31] = '0'                       # Attribute global
        vend = ''
      else:
        offer[28] = ''                        # Attribute name
        offer[29] = ''                        # Attribute values
        offer[30] = ''                        # Attribute visible
        offer[31] = ''                        # Attribute global

      if vendCode != '':
        offer[32] = '"код производителя"'     # Attribute name        # offer[44]
        offer[33] = '"' + vendCode + '"'      # Attribute values      # vendor code
        offer[34] = '1'                       # Attribute visible
        offer[35] = '0'                       # Attribute global
        vendCode = ''
      else:
        offer[32] = ''                        # Attribute name
        offer[33] = ''                        # Attribute values
        offer[34] = ''                        # Attribute visible
        offer[35] = ''                        # Attribute global

      if coo != '':
        offer[36] = '"страна происхождения"'    # Attribute name        # offer[49]
        offer[37] = coo                       # Attribute values      # country of origin
        offer[38] = '1'                       # Attribute visible
        offer[39] = '0'                       # Attribute global      # offer[53]     # offer[189]
        coo = ''
      else:
        offer[36] = ''                        # Attribute name
        offer[37] = ''                        # Attribute values
        offer[38] = ''                        # Attribute visible
        offer[39] = ''                        # Attribute global

      pp = 40
      pc = 0
      for p in range(20):                          #  4*20 + 4*3 + 28 = 120
        if param_count > pc:
          offer[pp+p*4] = params[pc][0]               # Attribute name
          offer[pp+p*4+1] = params[pc][1]             # Attribute values
          offer[pp+p*4+2] = '1'                       # Attribute visible
          offer[pp+p*4+3] = '0'                       # Attribute global
        else:
          offer[pp+p*4] = ''                          # Attribute name
          offer[pp+p*4+1] = ''                        # Attribute values
          offer[pp+p*4+2] = ''                        # Attribute visible
          offer[pp+p*4+3] = ''                        # Attribute global
        pc += 1

      # --------------------------------------- CREATE ROW NOW HERE:
      str = ', '.join(offer)
      # comas = str.count(',')
      # print('comas: ', comas)
      text_file.write(str+'\n')

    pics_count = 0
    param_count = 0
    e_count = 0


offers = 0
vc = 0
oc = 0
e_count=0
for e in etree.iter():
  if e.tag=='vendorCode':
    vc += 1
  if e.tag=='offers':
    offers = 1
  if offers==1:
    if e.tag=='offer':
      oc += 1
      # print('offer ', oc)
      proc_offer('end', None)
      proc_offer('start', e)
    else:
      proc_offer('e', e)
proc_offer('end', None)
text_file.close()

hed = '''ID, Type, ID, Name, Published, "Is featured?", "Visibility in catalog", "Short description", Description, "Date sale price starts", "Date sale price ends", "Tax status", "Tax class", "In stock?", "Backorders allowed?", "Sold individually?", "Weight (kg)", "Length (cm)", "Width (cm)", "Height (cm)", "Allow customer reviews?", "Purchase Note", "Sale price", "Regular price", Categories, Tags, "Shipping class", Images, "Attribute 1 name", "Attribute 1 value(s)", "Attribute 1 visible", "Attribute 1 global", "Attribute 2 name", "Attribute 2 value(s)", "Attribute 2 visible", "Attribute 2 global", "Attribute 3 name", "Attribute 3 value(s)", "Attribute 3 visible", "Attribute 3 global", "Attribute 4 name", "Attribute 4 value(s)", "Attribute 4 visible", "Attribute 4 global", "Attribute 5 name", "Attribute 5 value(s)", "Attribute 5 visible", "Attribute 5 global", "Attribute 6 name", "Attribute 6 value(s)", "Attribute 6 visible", "Attribute 6 global", "Attribute 7 name", "Attribute 7 value(s)", "Attribute 7 visible", "Attribute 7 global", "Attribute 8 name", "Attribute 8 value(s)", "Attribute 8 visible", "Attribute 8 global", "Attribute 9 name", "Attribute 9 value(s)", "Attribute 9 visible", "Attribute 9 global", "Attribute 10 name", "Attribute 10 value(s)", "Attribute 10 visible", "Attribute 10 global", "Attribute 11 name", "Attribute 11 value(s)", "Attribute 11 visible", "Attribute 11 global", "Attribute 12 name", "Attribute 12 value(s)", "Attribute 12 visible", "Attribute 12 global", "Attribute 13 name", "Attribute 13 value(s)", "Attribute 13 visible", "Attribute 13 global", "Attribute 14 name", "Attribute 14 value(s)", "Attribute 14 visible", "Attribute 14 global", "Attribute 15 name", "Attribute 15 value(s)", "Attribute 15 visible", "Attribute 15 global", "Attribute 16 name", "Attribute 16 value(s)", "Attribute 16 visible", "Attribute 16 global", "Attribute 17 name", "Attribute 17 value(s)", "Attribute 17 visible", "Attribute 17 global", "Attribute 18 name", "Attribute 18 value(s)", "Attribute 18 visible", "Attribute 18 global", "Attribute 19 name", "Attribute 19 value(s)", "Attribute 19 visible", "Attribute 19 global", "Attribute 20 name", "Attribute 20 value(s)", "Attribute 20 visible", "Attribute 20 global"\n''' 

with open(file_csv, 'r', encoding='utf-8') as fin:
  data = fin.read().splitlines(True)
  data[0] = hed
with open(file_csv, 'w', encoding='utf-8') as fileout:
  fileout.writelines(data[0:])
  fileout.close()

# print('Count vendor code = ', vc)
print('Товарів = ', oc)

dat = data[1:]
dt = []
dtc = 0
dc = 0
for lin in dat:
  dc += 1
  if dc < 500:
    dt.append(lin)
  elif dc == 500:
    dt.append(lin)
    dtc += 1
    fs = open(file_chunk + str(dtc) +'.csv', 'w', encoding='utf-8')
    fs.writelines(hed)
    fs.writelines(dt)
    fs.close()
    dt = []
    dc = 0
if dc > 0:
  dtc += 1
  fs = open(file_chunk + str(dtc) +'.csv', 'w', encoding='utf-8')
  fs.writelines(hed)
  fs.writelines(dt)
  fs.close()
  dt = []
  dc = 0

# sys.stdout = open("test.txt", "w", encoding='utf-8')

  # print()
  # print(e.tag, e.text, ' ', end = '')
  # for name, value in e.attrib.items():
  #   print(('{0}="{1}"'.format(name, value)), ' ', end = '')

# sys.stdout.close()
