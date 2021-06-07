
import xml.etree.ElementTree as ET
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
  def getParentName(nextCat):
    text = ' > '
    text = text + nextCat[0]
    if nextCat[2] != '0':
      for cat2 in list_category:
        if cat2[1] == nextCat[2]:
          text = text + getParentName(cat2)
    return text
  for cat in list_category:
    cur = cat[0]
    if cat[2] != '0':
      for cat1 in list_category:
        if cat1[1] == cat[2]:
          cur = cur + getParentName(cat1)
    cur = cur.replace(',',';')
    list_category_chain.append('"' + cur + '"')
    # print(list_category_chain[-1])


etree = ET.parse('t3.xml')
for e in etree.iter():
  if e.tag=='category':
    proc_category(e)
proc_build_category_chains()
print('Категорій: ', len(list_category))
# print('Categories chains: ', len(list_category_chain))


text_file = open("test.csv", "w", encoding='utf-8')
offer = [''] * 189
e_count = 0
pics_count = 0
pics = ''
vend = ''
vendCode = ''
coo = ''
param_count = 0
params = []               # ['name', 'all variations']
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
    offer = [''] * 189
    offer[0]=''
    offer[2]=e.attrib['id']   # write id in sku
  # -------------------------------- e section
  if pos=='e':
    e_count = e_count + 1
    if e.tag=='price':
      offer[25] = e.text
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
      offer[26] = list_category_chain[cc]
    elif e.tag=='vendor':
      vend = e.text
      # then add to attrib in end section
    elif e.tag=='vendorCode':
      vendCode = e.text
      # then add to attrib in end section
    elif e.tag=='description':
      st = e.text
      offer[8] = '"' + (st.replace('\n', '')).replace('\"', '\'') + '"'
    elif e.tag=='country_of_origin':
      coo = e.text
      # then add to attrib in end section
    elif e.tag=='param':                            ###########   MAXIMUM 27 params   ###########   5*27 + 5*3 + 39 = 189
      param_count += 1
      t1 = (e.attrib['name']).replace('\n', '')
      name = '"' + t1 + '"'
      t2 = (e.text).replace('\n', '')
      text = '"' + t2 + '"'
      params.append([name, text])
      # print(' - count: ', param_count, ' name: ', name, '  text: ', text)
      # print('   --- params -   name: ', params[-1][0], ' text: ', params[-1][1])
      # then add to attrib in end section
  # -------------------------------------------------------- end section
  if pos=='end':
    if e_count > 0:
      # offer[0] = 'id'                       # ID
      offer[1] = 'simple'                     # Type
      # offer[2] = ''                           # SKU
      # offer[3] = 'name'                     # Name
      offer[4] = '1'                          # Published
      offer[5] = '0'                          # Is featured?
      offer[6] = 'visible'                    # Visibility in catalog
      offer[7] = ''                           # Short description
      # offer[8] = 'description'              # Description
      offer[9] = ''                           # Date sale price starts
      offer[10] = ''                          # Date sale price ends
      offer[11] = 'taxable'                   # Tax status
      offer[12] = 'standard'                  # Tax class
      offer[13] = '1'                         # In stock?
      offer[14] = ''                          # Stock
      offer[15] = ''                          # Low stock amount
      offer[16] = '0'                         # Backorders allowed?
      offer[17] = '0'                         # Sold individually?
      offer[18] = ''                          # Weight (unit)
      offer[19] = ''                          # Length (unit)
      offer[20] = ''                          # Width (unit)
      offer[21] = ''                          # Height (unit)
      offer[22] = '1'                         # Allow customer reviews?
      offer[23] = ''                          # Purchase Note
      offer[24] = ''                          # Sale price
      # offer[25] = ''                        # Regular price
      # offer[26] = ''                        # Categories
      offer[27] = ''                          # Tags
      offer[28] = ''                          # Shipping class
      offer[29] = '"' + pics[:-2] + '"'       # Images
      offer[30] = ''                          # Download limit
      offer[31] = ''                          # Download expiry days
      offer[32] = ''                          # Parent
      offer[33] = ''                          # Grouped products
      offer[34] = ''                          # Upsells
      offer[35] = ''                          # Cross-sells
      offer[36] = ''                          # External URL
      offer[37] = ''                          # Button text
      offer[38] = ''                          # Position

      # attribs here:
      if vend != '':
        offer[39] = 'производитель'           # Attribute name        # offer[39]
        offer[40] = vend                      # Attribute values      # vendor
        offer[41] = ''                        # Attribute default
        offer[42] = '1'                       # Attribute visible
        offer[43] = '0'                       # Attribute global
        vend = ''
      else:
        offer[39] = ''                        # Attribute name
        offer[40] = ''                        # Attribute values
        offer[41] = ''                        # Attribute default
        offer[42] = ''                        # Attribute visible
        offer[43] = ''                        # Attribute global

      if vendCode != '':
        offer[44] = 'код производителя'       # Attribute name        # offer[44]
        offer[45] = vendCode                  # Attribute values      # vendor code
        offer[46] = ''                        # Attribute default
        offer[47] = '1'                       # Attribute visible
        offer[48] = '0'                       # Attribute global
        vendCode = ''
      else:
        offer[44] = ''                        # Attribute name
        offer[45] = ''                        # Attribute values
        offer[46] = ''                        # Attribute default
        offer[47] = ''                        # Attribute visible
        offer[48] = ''                        # Attribute global

      if coo != '':
        offer[49] = 'страна происхождения'    # Attribute name        # offer[49]
        offer[50] = coo                       # Attribute values      # country of origin
        offer[51] = ''                        # Attribute default
        offer[52] = '1'                       # Attribute visible
        offer[53] = '0'                       # Attribute global      # offer[53]     # offer[189]
        coo = ''
      else:
        offer[49] = ''                        # Attribute name
        offer[50] = ''                        # Attribute values
        offer[51] = ''                        # Attribute default
        offer[52] = ''                        # Attribute visible
        offer[53] = ''                        # Attribute global

      pp = 54
      pc = 0
      for p in range(27):                           # 5*27 + 5*3 + 39 = 189          4*27 + 4*3 + 39 = 159
        if param_count > pc:
          offer[pp+p*5] = params[pc][0]               # Attribute name
          offer[pp+p*5+1] = params[pc][1]             # Attribute values
          offer[pp+p*5+2] = ''                        # Attribute default
          offer[pp+p*5+3] = '1'                       # Attribute visible
          offer[pp+p*5+4] = '0'                       # Attribute global
        else:
          offer[pp+p*5] = ''                          # Attribute name
          offer[pp+p*5+1] = ''                        # Attribute values
          offer[pp+p*5+2] = ''                        # Attribute default
          offer[pp+p*5+3] = ''                        # Attribute visible
          offer[pp+p*5+4] = ''                        # Attribute global
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

with open('test.csv', 'r', encoding='utf-8') as fin:
  data = fin.read().splitlines(True)
  data[0] = '''ID, Type, SKU, Name, Published, "Is featured?", "Visibility in catalog", "Short description", Description, "Date sale price starts", "Date sale price ends", "Tax status", "Tax class", "In stock?", Stock, "Low stock amount", "Backorders allowed?", "Sold individually?", "Weight (unit)", "Length (unit)", "Width (unit)", "Height (unit)", "Allow customer reviews?", "Purchase Note", "Sale price", "Regular price", Categories, Tags, "Shipping class", Images,  "Download limit", "Download expiry days", Parent, "Grouped products", Upsells, "Cross-sells", "External URL", "Button text", Position, "Attribute 1 name", "Attribute 1 value(s)", "Attribute 1 default", "Attribute 1 visible", "Attribute 1 global", "Attribute 2 name", "Attribute 2 value(s)", "Attribute 2 default", "Attribute 2 visible", "Attribute 2 global", "Attribute 3 name", "Attribute 3 value(s)", "Attribute 3 default", "Attribute 3 visible", "Attribute 3 global", "Attribute 4 name", "Attribute 4 value(s)", "Attribute 4 default", "Attribute 4 visible", "Attribute 4 global", "Attribute 5 name", "Attribute 5 value(s)", "Attribute 5 default", "Attribute 5 visible", "Attribute 5 global", "Attribute 6 name", "Attribute 6 value(s)", "Attribute 6 default", "Attribute 6 visible", "Attribute 6 global", "Attribute 7 name", "Attribute 7 value(s)", "Attribute 7 default", "Attribute 7 visible", "Attribute 7 global", "Attribute 8 name", "Attribute 8 value(s)", "Attribute 8 default", "Attribute 8 visible", "Attribute 8 global", "Attribute 9 name", "Attribute 9 value(s)", "Attribute 9 default", "Attribute 9 visible", "Attribute 9 global", "Attribute 10 name", "Attribute 10 value(s)", "Attribute 10 default", "Attribute 10 visible", "Attribute 10 global", "Attribute 11 name", "Attribute 11 value(s)", "Attribute 11 default", "Attribute 11 visible", "Attribute 11 global", "Attribute 12 name", "Attribute 12 value(s)", "Attribute 12 default", "Attribute 12 visible", "Attribute 12 global", "Attribute 13 name", "Attribute 13 value(s)", "Attribute 13 default", "Attribute 13 visible", "Attribute 13 global", "Attribute 14 name", "Attribute 14 value(s)", "Attribute 14 default, "Attribute 14 visible", "Attribute 14 global", "Attribute 15 name", "Attribute 15 value(s)", "Attribute 15 default", "Attribute 15 visible", "Attribute 15 global", "Attribute 16 name", "Attribute 16 value(s)", "Attribute 16 default", "Attribute 16 visible", "Attribute 16 global", "Attribute 17 name", "Attribute 17 value(s)", "Attribute 17 default", "Attribute 17 visible", "Attribute 17 global", "Attribute 18 name", "Attribute 18 value(s)", "Attribute 18 default", "Attribute 18 visible", "Attribute 18 global", "Attribute 19 name", "Attribute 19 value(s)", "Attribute 19 default", "Attribute 19 visible", "Attribute 19 global", "Attribute 20 name", "Attribute 20 value(s)", "Attribute 20 default", "Attribute 20 visible", "Attribute 20 global", "Attribute 21 name, "Attribute 21 value(s)", "Attribute 21 default", "Attribute 21 visible", "Attribute 21 global", "Attribute 22 name", "Attribute 22 value(s)", "Attribute 22 default", "Attribute 22 visible", "Attribute 22 global", "Attribute 23 name", "Attribute 23 value(s)", "Attribute 23 default", "Attribute 23 visible", "Attribute 23 global", "Attribute 24 name", "Attribute 24 value(s)", "Attribute 24 default", "Attribute 24 visible", "Attribute 24 global", "Attribute 25 name", "Attribute 25 value(s)", "Attribute 25 default", "Attribute 25 visible", "Attribute 25 global", "Attribute 26 name", "Attribute 26 value(s)", "Attribute 26 default", "Attribute 26 visible", "Attribute 26 global", "Attribute 27 name", "Attribute 27 value(s)", "Attribute 27 default", "Attribute 27 visible", "Attribute 27 global"\n''' 
with open('test.csv', 'w', encoding='utf-8') as fileout:
  fileout.writelines(data[0:])

# print('Count vendor code = ', vc)
print('Товарів = ', oc)


# sys.stdout = open("test.txt", "w", encoding='utf-8')

  # print()
  # print(e.tag, e.text, ' ', end = '')
  # for name, value in e.attrib.items():
  #   print(('{0}="{1}"'.format(name, value)), ' ', end = '')

# sys.stdout.close()
