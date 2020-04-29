#!/usr/bin/python

import logging
example_content = """
<dataroot>
	<torrent>
		<id>8133976</id>
		<title>lool</title>
		<magnet>fce1f6eee4c669c4ff81d89595194cbe7d6f6eb5</magnet>
	</torrent>
	<torrent>
		<id>8133975</id>
		<title>Car.SOS.S01E01.HDTV.XviD-AFG</title>
		<magnet>dc85a53abffebd3b9206182c216fb6b0f810fd0d</magnet>
	</torrent>
</dataroot>
"""

# expects table-like XML
# <rows>
#  <row>
#    <col>COL1</col>
#    <col>COL2</col>
#    <col>COL3</col>
#  </row>    
# </rows>

sep = ','
endl = "\n"
content = ""
text = ""
depth = 0
flag = False

rows = []
header = []
row = []

product_id = []
category_id = []
producer_id = []
price = []
rec_price = []
stock = []
manufacturer = []


with open('data.xml', 'r', encoding="utf8") as ft:
    buffer = ft.readline()
    with open('temp.xml', 'w', encoding="utf8") as tf:
        tf.write('<?xml version="1.0" encoding="UTF-8"?>' + '\n')
        while buffer:
            if '<produk' in buffer:
                flag = True
            
            if flag == True:
                if buffer != '<![CDATA[\n' and buffer != ']]>\n':
                    logging.warning(buffer)
                    buffer = buffer.replace('<![CDATA[ ', '').replace(' ]]>', '')
                    if '<div>' in buffer:
                        buffer = buffer.replace('<', '[').replace('>', ']').replace('/', '&')
                    if '<p>' in buffer:
                        buffer = buffer.replace('<', '[').replace('>', ']').replace('/', '&')    
                    if '<iframe' in buffer:
                        buffer = buffer.replace('<', '[').replace('>', ']').replace('/', '&')
                    if 'z url' in buffer:
                        buffer = buffer.replace('<', '[').replace('>', ']').replace('/', '&')
                    if '<mi' in buffer:
                        buffer = buffer.replace('<', '[').replace('>', ']').replace('/', '&')
                    if '<br' in buffer or '<strong' in buffer:
                        buffer = buffer.replace('<', '[').replace('>', ']').replace('/', '&')
                    if '<' not in buffer:
                        tf.write(buffer.replace(',', '|').replace('/', '&').rstrip())
                    else:
                        if '<p' in buffer:
                            tf.write(buffer.replace(',', '|'))
                        elif '</' in buffer:
                            tf.write(buffer.replace(',', '|'))
                        elif '<?' in buffer:
                            tf.write(buffer.replace(',', '|'))
                        else:
                            tf.write(buffer.replace(',', '|').replace('/', '&').rstrip())
                buffer = ft.readline()
            else:
                buffer = ft.readline()


with open('temp.xml', 'r', encoding="utf8") as fp:
    with open('log.txt', 'w', encoding="utf8") as lf:
        buffer0 = fp.read(10)

        count = 0
        while buffer0:
            logging.warning(str(count))
            lf.write(str(count) + '\n')
            count = count + 1
            content += buffer0
            try:
                # ignore root <?xml...
                if '<?' in content:
                    index1 = content.index('<', content.index('<?') + 1) + 1
                    # logging.warning('this is index   ' + str(content.index('<', 1)))
                else:
                    index1 = content.index('<') + 1

                # find end of the tag
                index2 = content.index('>', index1)

                # strip attributes (if any)
                if ' ' in content[index1:]:
                    index2 = min(index2, content.index(' ', index1))

                # detect if it's a closing one </..>
                endTag = content[index1] == '/' if index1 < len(content) - 1 else False

                # extract only the tag name (without </)
                if endTag:
                    index1 += 1

            except ValueError:
                index1 = False
                index2 = False
                
            
            if index1 and index2 and index1 and len(content) - 1:
                # tag start detected
                if not endTag:
                    tagname = content[index1:index2]
                    depth += 1
                    # print 'tag', depth, tagname
                    content = content[index2:]

                    # extract column names
                    if depth == 3 and tagname not in header:
                        header.append(tagname)

                else:
                    tagname = content[index1:index2]
                    text = content[:index1].strip("</>").replace('|', ' ').replace('&', '/').replace('[', '<').replace(']', '>')
                    # print 'tag end', depth, tagname, text
                    content = content[index2+1:]
                    depth -= 1

                    # push new row
                    if depth == 1:
                        if len(row) == 9:
                            row.insert(1, '')
                            row.insert(2, '')
                            row.insert(6, '')
                            row.insert(8, '')
                        if len(row) == 10:
                            row.insert(1, '')
                            row.insert(2, '')
                            row.insert(6, '')
                        if len(row) == 11:
                            row.insert(6, '')
                            row.insert(8, '')
                        if len(row) == 12:
                            row.insert(6, '')

                        rows.append(row)
                        row = []
                    elif depth == 2:
                        row.insert(header.index(tagname), text)

            buffer0 = fp.read(10)

with open('parser_result.csv', 'w', encoding="utf8") as fp:
	fp.write(sep.join(header))
	fp.write(endl)
	fp.write(endl.join(map(lambda row: sep.join(row), rows)))


with open('data.xml', 'r', encoding="utf8") as kf:
    buffer = kf.readline()
    while buffer:
        if '</kategorie>' in buffer:
            break
        if '<k id=' in buffer:
            manufacturer.append(buffer.split(' ')[1].split('=')[1][1: -1] + '&' + buffer.split('=')[-1][1: -3])
        buffer = kf.readline()


with open('temp.xml', 'r', encoding="utf8") as ff:
    items = []
    line_temp = ff.readline()
    while line_temp:
        if 'kategoria_id' in line_temp:
            items = line_temp.split(' ')
            product_id.append(items[1].split('=')[1][1: -1])
            category_id.append(items[2].split('=')[1][1: -1])
            producer_id.append(items[3].split('=')[1][1: -1])
            price.append(items[4].split('=')[1][1: -1])
            rec_price.append(items[7].split('=')[1][1: -1])
            stock.append(items[10].split('=')[1][1: -1])
        line_temp = ff.readline()
    logging.warning(str(len(producer_id)))
        

with open('parser_result.csv', 'r', encoding="utf8") as fr:
    with open('distribution.csv', 'w', encoding="utf8") as fw:
        fw.write('product_id' + ',' + 'category_id' + ',' + 'producer_id' + ',' + 'name' + ',' + 'manufacturer' + ',' + 'price' + ',' + 'rec.price' + ',' + 'stock' + ',' + 'kod_producenta' + ',' + 'kod_ean' + ',' + 'html_title' + ',' + 'tekst_promocyjny' + ',' + 'opis' + ',' + 'promocja_kategorii' + ',' + 'image_1' + ',' + 'image_2' + ',' + 'image_3' + ',' + 'image_4' + ',' + 'image_5' + ',' + 'image_6' + ',' + 'image_7' + ',' + 'image_8' + ',' + 'image_9' + ',' + 'image_10' + ',' + 'image_11' + ',' + 'image_12' + ',' + 'image_13' + ',' + 'image_14' + ',' + 'image_15' + '\n')
        line_result = fr.readline()
        count = 0
        images = []
        while line_result:
            images = []
            if count != 0:
                for k in range(0, len(manufacturer)):
                    if manufacturer[k].split('&')[0] == category_id[count-1]:
                        csv_manufacturer = manufacturer[k].split('&')[1]
                logging.warning(str(count))
                csv_name = line_result.split(',')[0]
                csv_producenta = line_result.split(',')[1]
                csv_ean = line_result.split(',')[2]
                csv_title = line_result.split(',')[3]
                csv_desc = line_result.split(',')[4]
                csv_keyword = line_result.split(',')[5]
                csv_promocyjny = line_result.split(',')[6]
                csv_opis = line_result.split(',')[7]
                csv_filmy = line_result.split(',')[8]
                csv_promocja = line_result.split(',')[9]
                csv_wariantow = line_result.split(',')[10]

                images_temp = line_result.split(',')[11].split('/>')
                image_count = len(images_temp)-1
                for i in range(0, image_count):
                    images.append(images_temp[i].split('"')[1])

                if len(images) == 1:
                    fw.write(product_id[count-1] + ',' + category_id[count-1] + ',' + producer_id[count-1] + ',' + csv_name + ',' + csv_manufacturer + ',' + price[count-1] + ',' + rec_price[count-1] + ',' + stock[count-1] + ',' + csv_producenta + ',' + csv_ean + ',' + csv_title + ',' + csv_promocyjny + ',' + csv_opis + ',' + csv_promocja + ',' + images[0] + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + '\n')
                if len(images) == 2:
                    fw.write(product_id[count-1] + ',' + category_id[count-1] + ',' + producer_id[count-1] + ',' + csv_name + ',' + csv_manufacturer + ',' + price[count-1] + ',' + rec_price[count-1] + ',' + stock[count-1] + ',' + csv_producenta + ',' + csv_ean + ',' + csv_title + ',' + csv_promocyjny + ',' + csv_opis + ',' + csv_promocja + ',' + images[0] + ',' + images[1] + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + '\n')
                if len(images) == 3:
                    fw.write(product_id[count-1] + ',' + category_id[count-1] + ',' + producer_id[count-1] + ',' + csv_name + ',' + csv_manufacturer + ',' + price[count-1] + ',' + rec_price[count-1] + ',' + stock[count-1] + ',' + csv_producenta + ',' + csv_ean + ',' + csv_title + ',' + csv_promocyjny + ',' + csv_opis + ',' + csv_promocja + ',' + images[0] + ',' + images[1] + ',' + images[2] + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + '\n')
                if len(images) == 4:
                    fw.write(product_id[count-1] + ',' + category_id[count-1] + ',' + producer_id[count-1] + ',' + csv_name + ',' + csv_manufacturer + ',' + price[count-1] + ',' + rec_price[count-1] + ',' + stock[count-1] + ',' + csv_producenta + ',' + csv_ean + ',' + csv_title + ',' + csv_promocyjny + ',' + csv_opis + ',' + csv_promocja + ',' + images[0] + ',' + images[1] + ',' + images[2] + ',' + images[3] + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + '\n')
                if len(images) == 5:
                    fw.write(product_id[count-1] + ',' + category_id[count-1] + ',' + producer_id[count-1] + ',' + csv_name + ',' + csv_manufacturer + ',' + price[count-1] + ',' + rec_price[count-1] + ',' + stock[count-1] + ',' + csv_producenta + ',' + csv_ean + ',' + csv_title + ',' + csv_promocyjny + ',' + csv_opis + ',' + csv_promocja + ',' + images[0] + ',' + images[1] + ',' + images[2] + ',' + images[3] + ',' + images[4] + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + '\n')
                if len(images) == 6:
                    fw.write(product_id[count-1] + ',' + category_id[count-1] + ',' + producer_id[count-1] + ',' + csv_name + ',' + csv_manufacturer + ',' + price[count-1] + ',' + rec_price[count-1] + ',' + stock[count-1] + ',' + csv_producenta + ',' + csv_ean + ',' + csv_title + ',' + csv_promocyjny + ',' + csv_opis + ',' + csv_promocja + ',' + images[0] + ',' + images[1] + ',' + images[2] + ',' + images[3] + ',' + images[4] + ',' + images[5] + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + '\n')
                if len(images) == 7:
                    fw.write(product_id[count-1] + ',' + category_id[count-1] + ',' + producer_id[count-1] + ',' + csv_name + ',' + csv_manufacturer + ',' + price[count-1] + ',' + rec_price[count-1] + ',' + stock[count-1] + ',' + csv_producenta + ',' + csv_ean + ',' + csv_title + ',' + csv_promocyjny + ',' + csv_opis + ',' + csv_promocja + ',' + images[0] + ',' + images[1] + ',' + images[2] + ',' + images[3] + ',' + images[4] + ',' + images[5] + ',' + images[6] + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + '\n')
                if len(images) == 8:
                    fw.write(product_id[count-1] + ',' + category_id[count-1] + ',' + producer_id[count-1] + ',' + csv_name + ',' + csv_manufacturer + ',' + price[count-1] + ',' + rec_price[count-1] + ',' + stock[count-1] + ',' + csv_producenta + ',' + csv_ean + ',' + csv_title + ',' + csv_promocyjny + ',' + csv_opis + ',' + csv_promocja + ',' + images[0] + ',' + images[1] + ',' + images[2] + ',' + images[3] + ',' + images[4] + ',' + images[5] + ',' + images[6] + ',' + images[7] + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' +'\n')
                if len(images) == 9:
                    fw.write(product_id[count-1] + ',' + category_id[count-1] + ',' + producer_id[count-1] + ',' + csv_name + ',' + csv_manufacturer + ',' + price[count-1] + ',' + rec_price[count-1] + ',' + stock[count-1] + ',' + csv_producenta + ',' + csv_ean + ',' + csv_title + ',' + csv_promocyjny + ',' + csv_opis + ',' + csv_promocja + ',' + images[0] + ',' + images[1] + ',' + images[2] + ',' + images[3] + ',' + images[4] + ',' + images[5] + ',' + images[6] + ',' + images[7] + ',' + images[8] + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + '\n')
                if len(images) == 10:
                    fw.write(product_id[count-1] + ',' + category_id[count-1] + ',' + producer_id[count-1] + ',' + csv_name + ',' + csv_manufacturer + ',' + price[count-1] + ',' + rec_price[count-1] + ',' + stock[count-1] + ',' + csv_producenta + ',' + csv_ean + ',' + csv_title + ',' + csv_promocyjny + ',' + csv_opis + ',' + csv_promocja + ',' + images[0] + ',' + images[1] + ',' + images[2] + ',' + images[3] + ',' + images[4] + ',' + images[5] + ',' + images[6] + ',' + images[7] + ',' + images[8] + ',' + images[9] + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + '\n')
                if len(images) == 11:
                    fw.write(product_id[count-1] + ',' + category_id[count-1] + ',' + producer_id[count-1] + ',' + csv_name + ',' + csv_manufacturer + ',' + price[count-1] + ',' + rec_price[count-1] + ',' + stock[count-1] + ',' + csv_producenta + ',' + csv_ean + ',' + csv_title + ',' + csv_promocyjny + ',' + csv_opis + ',' + csv_promocja + ',' + images[0] + ',' + images[1] + ',' + images[2] + ',' + images[3] + ',' + images[4] + ',' + images[5] + ',' + images[6] + ',' + images[7] + ',' + images[8] + ',' + images[9] + ',' + images[10] + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + '\n')
                if len(images) == 12:
                    fw.write(product_id[count-1] + ',' + category_id[count-1] + ',' + producer_id[count-1] + ',' + csv_name + ',' + csv_manufacturer + ',' + price[count-1] + ',' + rec_price[count-1] + ',' + stock[count-1] + ',' + csv_producenta + ',' + csv_ean + ',' + csv_title + ',' + csv_promocyjny + ',' + csv_opis + ',' + csv_promocja + ',' + images[0] + ',' + images[1] + ',' + images[2] + ',' + images[3] + ',' + images[4] + ',' + images[5] + ',' + images[6] + ',' + images[7] + ',' + images[8] + ',' + images[9] + ',' + images[10] + ',' + images[11] + ',' + ' ' + ',' + ' ' + ',' + ' ' + '\n')
                if len(images) == 13:
                    fw.write(product_id[count-1] + ',' + category_id[count-1] + ',' + producer_id[count-1] + ',' + csv_name + ',' + csv_manufacturer + ',' + price[count-1] + ',' + rec_price[count-1] + ',' + stock[count-1] + ',' + csv_producenta + ',' + csv_ean + ',' + csv_title + ',' + csv_promocyjny + ',' + csv_opis + ',' + csv_promocja + ',' + images[0] + ',' + images[1] + ',' + images[2] + ',' + images[3] + ',' + images[4] + ',' + images[5] + ',' + images[6] + ',' + images[7] + ',' + images[8] + ',' + images[9] + ',' + images[10] + ',' + images[11] + ',' + images[12] + ',' + ' ' + ',' + ' ' + '\n')
                if len(images) == 14:
                    fw.write(product_id[count-1] + ',' + category_id[count-1] + ',' + producer_id[count-1] + ',' + csv_name + ',' + csv_manufacturer + ',' + price[count-1] + ',' + rec_price[count-1] + ',' + stock[count-1] + ',' + csv_producenta + ',' + csv_ean + ',' + csv_title + ',' + csv_promocyjny + ',' + csv_opis + ',' + csv_promocja + ',' + images[0] + ',' + images[1] + ',' + images[2] + ',' + images[3] + ',' + images[4] + ',' + images[5] + ',' + images[6] + ',' + images[7] + ',' + images[8] + ',' + images[9] + ',' + images[10] + ',' + images[11] + ',' + images[12] + ',' + images[13] + ',' + ' ' + '\n')
                if len(images) == 15:
                    fw.write(product_id[count-1] + ',' + category_id[count-1] + ',' + producer_id[count-1] + ',' + csv_name + ',' + csv_manufacturer + ',' + price[count-1] + ',' + rec_price[count-1] + ',' + stock[count-1] + ',' + csv_producenta + ',' + csv_ean + ',' + csv_title + ',' + csv_promocyjny + ',' + csv_opis + ',' + csv_promocja + ',' + images[0] + ',' + images[1] + ',' + images[2] + ',' + images[3] + ',' + images[4] + ',' + images[5] + ',' + images[6] + ',' + images[7] + ',' + images[8] + ',' + images[9] + ',' + images[10] + ',' + images[11] + ',' + images[12] + ',' + images[13] + ',' + images[14] + '\n')    

            count = count + 1
            line_result = fr.readline()