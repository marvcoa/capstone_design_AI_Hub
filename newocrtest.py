
import requests
import uuid
import time
import base64
import json
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.font_manager as fm
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
# 한글 글꼴 경로 지정
font_path = 'C:/Windows/Fonts/malgun.ttf'
font_name = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font_name)
matplotlib.rcParams['axes.unicode_minus'] = False

def extract_product_info(result):
    products = []
    for subresult in result['images'][0]['receipt']['result']['subResults']:
        for item in subresult['items']:
            name = item['name']['text']
            count = item['count']['text']
            price = item['price']['price']['text']
            unit_price = item["price"]["unitPrice"]["text"]
            products.append({'제품명': name, '단가': unit_price, '수량': count, '가격': price})
    return products

api_url = 'your_api_url'
secret_key = 'your_api_key'
image_file = 'a7.jpg'
with open(image_file,'rb') as f:
 file_data = f.read()

request_json = {
    'images': [
        {
            'format': 'jpg',
            'name': 'demo',
            'data': base64.b64encode(file_data).decode()
        }
    ],
    'requestId': str(uuid.uuid4()),
    'version': 'V2',
    'timestamp': int(round(time.time() * 1000))
}

payload = json.dumps(request_json).encode('UTF-8')
headers = {
  'X-OCR-SECRET': secret_key,
  'Content-Type': 'application/json'
}

response = requests.request("POST", api_url, headers=headers, data = payload)
result = response.json()

products = extract_product_info(result)


def plot_product_info(products):
    # 제품명과 가격 정보 추출
    names = [product['제품명'] for product in products]
    prices = [float(product['가격'].replace(',', '')) for product in products]

    # 제품명별 가격 계산
    name_to_price = {}
    for name, price in zip(names, prices):
        if name in name_to_price:
            name_to_price[name] += price
        else:
            name_to_price[name] = price

    # 막대 그래프로 나타내기
    x = np.arange(len(name_to_price))
    plt.bar(x, name_to_price.values())
    plt.xticks(x, name_to_price.keys(), rotation=45)
    plt.xlabel('제품명')
    plt.ylabel('가격')
    plt.title('물건 분류 결과')

    # x축 레이블 축소
    labels = [label[:10] + '...' if len(label) > 10 else label for label in name_to_price.keys()]
    plt.xticks(x, labels)

    plt.show()


products = extract_product_info(result)
plot_product_info(products)


products = extract_product_info(result)
plot_product_info(products)
print(products)
print(response.text)
