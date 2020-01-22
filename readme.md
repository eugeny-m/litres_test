# LitRes test script

This is a test challenge for LitRes interviewing process.  
The script satisfy this conditions:

```
Напишите скрипт, получающий в качестве аргумента путь к CSV-файлу и выдающий в STDOUT следующее:
- посчитать общий профит с точностью до цента
- найти самые лучшие продукты по продажам, по количеству продаж и по профиту соответственно
- найти самые худшие продукты по продажам, по количеству продаж и по профиту соответственно
- найти средний срок доставки товара клиенту
- найти стандартное отклонение от среднего срока доставки товара клиенту
- посчитать и вывести в CSV-файл продажи, количество продаж и профит по каждому продукту
``` 

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

* Python 3.8.1

### Installing

* get project files from github  
`git clone https://github.com/eugeny-m/litres_test.git`  
`cd litres_test`
* create python environment  
`python3.8 -m venv venv`
* activate venv  
`source venv/bin/activate`
* install requirements  
`pip install -U pip`  
`pip install -r requirements.txt`

## Running

* create Orders.csv file   
csv file format example:
```
Row ID;Order ID;Order Date;Ship Date;Ship Mode;Customer ID;Customer Name;Segment;Country;City;State;Postal Code;Region;Product ID;Category;Sub-Category;Product Name;Sales;Quantity;Discount;Profit
1;CA-2016-152156;11/8/16;11/11/16;Second Class;CG-12520;Claire Gute;Consumer;United States;Henderson;Kentucky;42420;South;FUR-BO-10001798;Furniture;Bookcases;Bush Somerset Collection Bookcase;261,96;2;0;41,9136
2;CA-2016-152156;11/8/16;11/11/16;Second Class;CG-12520;Claire Gute;Consumer;United States;Henderson;Kentucky;42420;South;FUR-CH-10000454;Furniture;Chairs;Hon Deluxe Fabric Upholstered Stacking Chairs, Rounded Back;731,94;3;0;219,582
```
* run script `python orders_statistics.py  --csv_file Orders.csv`


## Built With

* [Python 3.8.1](https://www.python.org)
* numpy 1.18.1
* pandas 0.25.3

## Authors

* **Eugeny Maksimov** -  [eugeny-m](https://github.com/eugeny-m)  
