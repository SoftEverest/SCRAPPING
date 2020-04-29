#!/usr/bin/python

import logging

products = []
flag = False
desc_flag = False
image_flag = False
product_text = ''
product_id = []
product_code = []
producer_name = []
category_name = []
series_name = []
name_eng = []
name_ger = []
name_pol = []
desc_eng = []
desc_ger = []
desc_pol = []
# unit = []
# warranty_name = []
page_url = []
description = []
image = []
price = []
stock = []


with open('hurtel.xml', 'r', encoding="utf8") as fh:
    buffer = fh.readline()
    while buffer:
        if '<product id=' in buffer:
            flag = True
        if '</product>' in buffer:
            flag = False

        if flag == True:
            product_text = product_text + buffer

            buffer = fh.readline()
        else:
            buffer = fh.readline()
            if product_text != '':
                products.append(product_text + '</product>')
                product_text = ''        

# print('-------------------' + '\n')

for i in range(0, len(products)):
    lines = products[i].split('\n')
    desc = ''
    price_temp = ''
    stock_temp = ''
    name_eng_temp = ''
    name_ger_temp = ''
    name_pol_temp = ''
    img = [ ]
    if '<series' not in products[i]:
        series_name.append(' ')

    if '<stock' not in products[i]:
        stock.append(' ')

    if '<name xml:lang="eng">' not in products[i]:
        name_eng.append(' ')

    if '<name xml:lang="ger">' not in products[i]:
        name_ger.append(' ')

    if '<name xml:lang="pol">' not in products[i]:
        name_pol.append(' ')

    if '<long_desc xml:lang="eng">' not in products[i]:
        desc_eng.append(' ')

    if '<long_desc xml:lang="ger">' not in products[i]:
        desc_ger.append(' ')

    if '<long_desc xml:lang="pol">' not in products[i]:
        desc_pol.append(' ')
    # if '<large>' not in products[i]:
    #     image.append(' ')
    
    for j in range(0, len(lines)):
        image_flag = False
        if '<product id' in lines[j]:
            product_id.append(lines[j].split('id')[1].split('"')[1])
            try:
                product_code.append(lines[j].split('code_producer')[1].split('"')[1])
            except:
                product_code.append('')
        elif '<producer id' in lines[j]:
            producer_name.append(lines[j].split('name')[1].split('"')[1])
        elif '<category id' in lines[j]:
            category_name.append(lines[j].split('name')[1].split('"')[1].replace(',', ' '))
        elif '<series id' in lines[j]:
            series_name.append(lines[j].split('name')[1].split('"')[1].replace(',', ' '))
        elif '<card url' in lines[j]:
            page_url.append(lines[j].split(' ')[-1].split('"')[1])
        elif '<description>' in lines[j]:
            desc_flag = True
        elif '</description>' in lines[j]:
            desc_flag = False
        elif '<price' in lines[j]:
            if price_temp == '':
                price_temp = lines[j].split('gross')[1].split('"')[1]
                price.append(price_temp)
        elif '<stock' in lines[j]:
            if stock_temp == '':
                stock_temp = lines[j].split('quantity')[1].split('"')[1]
                stock.append(stock_temp)
        elif '<image url=' in lines[j]:
            img.append(lines[j].split('url')[1].split('"')[1])
        elif '<name xml:lang="eng">' in lines[j]:
            if name_eng_temp == '':
                name_eng_temp = lines[j].split('[')[-1].split(']')[0].replace(',', ' ')
                name_eng.append(name_eng_temp.strip())
        elif '<name xml:lang="ger">' in lines[j]:
            if name_ger_temp == '':
                name_ger_temp = lines[j].split('[')[-1].split(']')[0].replace(',', ' ')
                name_ger.append(name_ger_temp.strip())
        elif '<name xml:lang="pol">' in lines[j]:
            if name_pol_temp == '':
                name_pol_temp = lines[j].split('[')[-1].split(']')[0].replace(',', ' ')
                name_pol.append(name_pol_temp.strip())
        elif '<long_desc xml:lang="eng">' in lines[j]:
            desc_eng.append(lines[j].split('[')[-1].split(']')[0].replace(',', ' ').strip())
        elif '<long_desc xml:lang="ger">' in lines[j]:
            desc_ger.append(lines[j].split('[')[-1].split(']')[0].replace(',', ' ').strip())
        elif '<long_desc xml:lang="pol">' in lines[j]:
            desc_pol.append(lines[j].split('[')[-1].split(']')[0].replace(',', ' ').strip())
        # elif '<large>' in lines[j]:
        #     image_flag = True
        # elif '</large>' in lines[j]:
        #     image_flag = False

        # if desc_flag == True:
        #     desc = desc + lines[j].replace(',', ' ')
        #     if '<name xml:lang="eng">' in lines[j]:
        #         name_eng.append(lines[j].split('[')[-1].split(']')[0].replace(',', ' '))
        #     if '<name xml:lang="ger">' in lines[j]:
        #         if name_eng_temp == '':
        #         name_eng_temp = lines[j].split('[')[-1].split(']')[0].replace(',', ' ')
        #         name_eng.append(name_eng_temp)
        #     if '<name xml:lang="pol">' in lines[j]:
        #         name_pol.append(lines[j].split('[')[-1].split(']')[0].replace(',', ' '))
        #     if '<long_desc xml:lang="eng">' in lines[j]:
        #         desc_eng.append(lines[j].split('[')[-1].split(']')[0].replace(',', ' '))
        #     if '<long_desc xml:lang="ger">' in lines[j]:
        #         desc_ger.append(lines[j].split('[')[-1].split(']')[0].replace(',', ' '))
        #     if '<long_desc xml:lang="pol">' in lines[j]:
        #         desc_pol.append(lines[j].split('[')[-1].split(']')[0].replace(',', ' '))

        # if image_flag == True:
        #     img = '*'.join(lines[j].split('url')[1].split('"')[1]) 
            # try:
            # image.append(lines[j].split('url')[1].split('"')[1])
    image.append(img)
print('product_id====' + str(len(product_id)))
print('producer_name====' + str(len(producer_name)))
print('category_name====' + str(len(category_name)))
print('series_name====' + str(len(series_name)))
print('page_url====' + str(len(page_url)))
print('price====' + str(len(price)))
print('stock====' + str(len(stock)))
print('image====' + str(len(image)))
print('name_eng====' + str(len(name_eng)))
print('name_ger====' + str(len(name_ger)))
print('name_pol====' + str(len(name_pol)))
print('desc_eng====' + str(len(desc_eng)))
print('desc_ger====' + str(len(desc_ger)))
print('desc_pol====' + str(len(desc_pol)))
            # except:
            #     logging.warning('error')
        
# print(len(image))


with open('hurtel.csv', 'w', encoding="utf8") as fw:
    fw.write('product_id' + ',' + 'product_code' + ',' + 'producer_name' + ',' + 'category_name' + ',' + 'series_name' + ',' + 'page_url' + ',' + 'price' + ',' + 'stock' + ',' + 'name xml:lang="eng"' + ',' + 'long_desc xml:lang="eng"' + ',' + 'name xml:lang="ger"' + ',' + 'long_desc xml:lang="ger"' + ',' + 'name xml:lang="pol"' + ',' + 'long_desc xml:lang="pol"' + ',' + 'image1' + ',' + 'image2' + ',' + 'image3' + ',' + 'image4' + ',' + 'image5' + ',' + 'image6' + ',' + 'image7' + ',' + 'image8' + ',' + 'image9' + ',' + 'image10' + ',' + 'image11' + ',' + 'image12' + ',' + 'image13' + ',' + 'image14' + ',' + 'image15' + ',' + '\n')
    for k in range(0, len(product_id)):
        # print('**********************************' + '\n')
        # print(len(image[k]))
        # print(image[k][0])
        if len(image[k]) == 1:
            fw.write(product_id[k] + ',' + product_code[k] + ',' + producer_name[k] + ',' + category_name[k] + ',' + series_name[k] + ',' + page_url[k] + ',' + price[k] + ',' + stock[k] + ',' + name_eng[k] + ',' + desc_eng[k] + ',' + name_ger[k] + ',' + desc_ger[k] + ',' + name_pol[k] + ',' + desc_pol[k] + ',' + image[k][0] + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' '+ ',' + ' ' + '\n')
        if len(image[k]) == 2:
            fw.write(product_id[k] + ',' + product_code[k] + ',' + producer_name[k] + ',' + category_name[k] + ',' + series_name[k] + ',' + page_url[k] + ',' + price[k] + ',' + stock[k] + ',' + name_eng[k] + ',' + desc_eng[k] + ',' + name_ger[k] + ',' + desc_ger[k] + ',' + name_pol[k] + ',' + desc_pol[k] + ',' + image[k][0] + ',' + image[k][1] + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' '+ ',' + ' ' + '\n')
        if len(image[k]) == 3:
            fw.write(product_id[k] + ',' + product_code[k] + ',' + producer_name[k] + ',' + category_name[k] + ',' + series_name[k] + ',' + page_url[k] + ',' + price[k] + ',' + stock[k] + ',' + name_eng[k] + ',' + desc_eng[k] + ',' + name_ger[k] + ',' + desc_ger[k] + ',' + name_pol[k] + ',' + desc_pol[k] + ',' + image[k][0] + ',' + image[k][1] + ',' + image[k][2] + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' '+ ',' + ' ' + '\n')
        if len(image[k]) == 4:
            fw.write(product_id[k] + ',' + product_code[k] + ',' + producer_name[k] + ',' + category_name[k] + ',' + series_name[k] + ',' + page_url[k] + ',' + price[k] + ',' + stock[k] + ',' + name_eng[k] + ',' + desc_eng[k] + ',' + name_ger[k] + ',' + desc_ger[k] + ',' + name_pol[k] + ',' + desc_pol[k] + ',' + image[k][0] + ',' + image[k][1] + ',' + image[k][2] + ',' + image[k][3] + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' '+ ',' + ' ' + '\n')
        if len(image[k]) == 5:
            fw.write(product_id[k] + ',' + product_code[k] + ',' + producer_name[k] + ',' + category_name[k] + ',' + series_name[k] + ',' + page_url[k] + ',' + price[k] + ',' + stock[k] + ',' + name_eng[k] + ',' + desc_eng[k] + ',' + name_ger[k] + ',' + desc_ger[k] + ',' + name_pol[k] + ',' + desc_pol[k] + ',' + image[k][0] + ',' + image[k][1] + ',' + image[k][2] + ',' + image[k][3] + ',' + image[k][4] + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' '+ ',' + ' ' + '\n')
        if len(image[k]) == 6:
            fw.write(product_id[k] + ',' + product_code[k] + ',' + producer_name[k] + ',' + category_name[k] + ',' + series_name[k] + ',' + page_url[k] + ',' + price[k] + ',' + stock[k] + ',' + name_eng[k] + ',' + desc_eng[k] + ',' + name_ger[k] + ',' + desc_ger[k] + ',' + name_pol[k] + ',' + desc_pol[k] + ',' + image[k][0] + ',' + image[k][1] + ',' + image[k][2] + ',' + image[k][3] + ',' + image[k][4] + ',' + image[k][5] + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' '+ ',' + ' ' + '\n')
        if len(image[k]) == 7:
            fw.write(product_id[k] + ',' + product_code[k] + ',' + producer_name[k] + ',' + category_name[k] + ',' + series_name[k] + ',' + page_url[k] + ',' + price[k] + ',' + stock[k] + ',' + name_eng[k] + ',' + desc_eng[k] + ',' + name_ger[k] + ',' + desc_ger[k] + ',' + name_pol[k] + ',' + desc_pol[k] + ',' + image[k][0] + ',' + image[k][1] + ',' + image[k][2] + ',' + image[k][3] + ',' + image[k][4] + ',' + image[k][5] + ',' + image[k][6] + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' '+ ',' + ' ' + '\n')
        if len(image[k]) == 8:
            fw.write(product_id[k] + ',' + product_code[k] + ',' + producer_name[k] + ',' + category_name[k] + ',' + series_name[k] + ',' + page_url[k] + ',' + price[k] + ',' + stock[k] + ',' + name_eng[k] + ',' + desc_eng[k] + ',' + name_ger[k] + ',' + desc_ger[k] + ',' + name_pol[k] + ',' + desc_pol[k] + ',' + image[k][0] + ',' + image[k][1] + ',' + image[k][2] + ',' + image[k][3] + ',' + image[k][4] + ',' + image[k][5] + ',' + image[k][6] + ',' + image[k][7] + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' '+ ',' + ' ' + '\n')
        if len(image[k]) == 9:
            fw.write(product_id[k] + ',' + product_code[k] + ',' + producer_name[k] + ',' + category_name[k] + ',' + series_name[k] + ',' + page_url[k] + ',' + price[k] + ',' + stock[k] + ',' + name_eng[k] + ',' + desc_eng[k] + ',' + name_ger[k] + ',' + desc_ger[k] + ',' + name_pol[k] + ',' + desc_pol[k] + ',' + image[k][0] + ',' + image[k][1] + ',' + image[k][2] + ',' + image[k][3] + ',' + image[k][4] + ',' + image[k][5] + ',' + image[k][6] + ',' + image[k][7] + ',' + image[k][8] + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' '+ ',' + ' ' + '\n')
            # fw.write(product_id[k] + ',' + product_code[k] + ',' + producer_name[k] + ',' + category_name[k] + ',' + series_name[k] + ',' + ' ' + '\n')
        if len(image[k]) == 10:
            fw.write(product_id[k] + ',' + product_code[k] + ',' + producer_name[k] + ',' + category_name[k] + ',' + series_name[k] + ',' + page_url[k] + ',' + price[k] + ',' + stock[k] + ',' + name_eng[k] + ',' + desc_eng[k] + ',' + name_ger[k] + ',' + desc_ger[k] + ',' + name_pol[k] + ',' + desc_pol[k] + ',' + image[k][0] + ',' + image[k][1] + ',' + image[k][2] + ',' + image[k][3] + ',' + image[k][4] + ',' + image[k][5] + ',' + image[k][6] + ',' + image[k][7] + ',' + image[k][8] + ',' + image[k][9] + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' '+ ',' + ' ' + '\n')
        if len(image[k]) == 11:
            fw.write(product_id[k] + ',' + product_code[k] + ',' + producer_name[k] + ',' + category_name[k] + ',' + series_name[k] + ',' + page_url[k] + ',' + price[k] + ',' + stock[k] + ',' + name_eng[k] + ',' + desc_eng[k] + ',' + name_ger[k] + ',' + desc_ger[k] + ',' + name_pol[k] + ',' + desc_pol[k] + ',' + image[k][0] + ',' + image[k][1] + ',' + image[k][2] + ',' + image[k][3] + ',' + image[k][4] + ',' + image[k][5] + ',' + image[k][6] + ',' + image[k][7] + ',' + image[k][8] + ',' + image[k][9] + ',' + image[k][10] + ',' + ' ' + ',' + ' ' + ',' + ' '+ ',' + ' ' + '\n')
        if len(image[k]) == 12:
            fw.write(product_id[k] + ',' + product_code[k] + ',' + producer_name[k] + ',' + category_name[k] + ',' + series_name[k] + ',' + page_url[k] + ',' + price[k] + ',' + stock[k] + ',' + name_eng[k] + ',' + desc_eng[k] + ',' + name_ger[k] + ',' + desc_ger[k] + ',' + name_pol[k] + ',' + desc_pol[k] + ',' + image[k][0] + ',' + image[k][1] + ',' + image[k][2] + ',' + image[k][3] + ',' + image[k][4] + ',' + image[k][5] + ',' + image[k][6] + ',' + image[k][7] + ',' + image[k][8] + ',' + image[k][9] + ',' + image[k][10] + ',' + image[k][11] + ',' + ' ' + ',' + ' '+ ',' + ' ' + '\n')
        if len(image[k]) == 13:
            fw.write(product_id[k] + ',' + product_code[k] + ',' + producer_name[k] + ',' + category_name[k] + ',' + series_name[k] + ',' + page_url[k] + ',' + price[k] + ',' + stock[k] + ',' + name_eng[k] + ',' + desc_eng[k] + ',' + name_ger[k] + ',' + desc_ger[k] + ',' + name_pol[k] + ',' + desc_pol[k] + ',' + image[k][0] + ',' + image[k][1] + ',' + image[k][2] + ',' + image[k][3] + ',' + image[k][4] + ',' + image[k][5] + ',' + image[k][6] + ',' + image[k][7] + ',' + image[k][8] + ',' + image[k][9] + ',' + image[k][10] + ',' + image[k][11] + ',' + image[k][12] + ',' + ' '+ ',' + ' ' + '\n')
        if len(image[k]) == 14:
            fw.write(product_id[k] + ',' + product_code[k] + ',' + producer_name[k] + ',' + category_name[k] + ',' + series_name[k] + ',' + page_url[k] + ',' + price[k] + ',' + stock[k] + ',' + name_eng[k] + ',' + desc_eng[k] + ',' + name_ger[k] + ',' + desc_ger[k] + ',' + name_pol[k] + ',' + desc_pol[k] + ',' + image[k][0] + ',' + image[k][1] + ',' + image[k][2] + ',' + image[k][3] + ',' + image[k][4] + ',' + image[k][5] + ',' + image[k][6] + ',' + image[k][7] + ',' + image[k][8] + ',' + image[k][9] + ',' + image[k][10] + ',' + image[k][11] + ',' + image[k][12] + ',' + image[k][13]+ ',' + ' ' + '\n')
            # fw.write(name_eng[k] + ',' + desc_eng[k] + ',' + name_ger[k] + ',' + desc_ger[k] + ',' + name_pol[k] + ',' + desc_pol[k])
        if len(image[k]) == 15:
            fw.write(product_id[k] + ',' + product_code[k] + ',' + producer_name[k] + ',' + category_name[k] + ',' + series_name[k] + ',' + page_url[k] + ',' + price[k] + ',' + stock[k] + ',' + name_eng[k] + ',' + desc_eng[k] + ',' + name_ger[k] + ',' + desc_ger[k] + ',' + name_pol[k] + ',' + desc_pol[k] + ',' + image[k][0] + ',' + image[k][1] + ',' + image[k][2] + ',' + image[k][3] + ',' + image[k][4] + ',' + image[k][5] + ',' + image[k][6] + ',' + image[k][7] + ',' + image[k][8] + ',' + image[k][9] + ',' + image[k][10] + ',' + image[k][11] + ',' + image[k][12] + ',' + image[k][13]+ ',' + image[k][14] + '\n')
        if len(image[k]) > 16:
            fw.write(product_id[k] + ',' + product_code[k] + ',' + producer_name[k] + ',' + category_name[k] + ',' + series_name[k] + ',' + page_url[k] + ',' + price[k] + ',' + stock[k] + ',' + name_eng[k] + ',' + desc_eng[k] + ',' + name_ger[k] + ',' + desc_ger[k] + ',' + name_pol[k] + ',' + desc_pol[k] + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' '+ ',' + ' ' + '\n')
        if len(image[k]) == 0:
            fw.write(product_id[k] + ',' + product_code[k] + ',' + producer_name[k] + ',' + category_name[k] + ',' + series_name[k] + ',' + page_url[k] + ',' + price[k] + ',' + stock[k] + ',' + name_eng[k] + ',' + desc_eng[k] + ',' + name_ger[k] + ',' + desc_ger[k] + ',' + name_pol[k] + ',' + desc_pol[k] + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' ' + ',' + ' '+ ',' + ' ' + '\n')