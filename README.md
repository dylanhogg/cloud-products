# cloud-products 

[![pypi Version](https://img.shields.io/pypi/v/cloud-products.svg?logo=pypi)](https://pypi.org/project/cloud-products/)
![Latest Tag](https://img.shields.io/github/v/tag/dylanhogg/cloud-products)
![Depenencies](https://img.shields.io/librariesio/github/dylanhogg/cloud-products)

A package for getting cloud products and product descriptions from a cloud provider website with cache support.

Currently supports getting AWS product information from 
[https://aws.amazon.com/products](https://aws.amazon.com/products)

GCP and Azure product information will be added in time.


### Install from PyPi
```
pip install cloud-products
```


### Example 1: List AWS products
```
from cloud_products.aws import AwsCrawler
for product in AwsCrawler().get_products():
    print(f"{product.code}: {product.name}: {product.desc}")
```

Example output:
```
alexaforbusiness: Alexa for Business: Empower your Organization with Alexa
amazon-mq: Amazon MQ: Managed Message Broker for ActiveMQ
amplify: AWS Amplify: Build and deploy mobile and web applications
api-gateway: Amazon API Gateway: Build, Deploy, and Manage APIs
...
```


### Example 2: Get product descriptions as a list of lines
```
from cloud_products.aws import AwsCrawler
cloud_products = AwsCrawler()
product = cloud_products.get_products()[0]
lines = cloud_products.get_product_text(product)
print(lines[4])
```

Example output:
```
Alexa for Business is a service that enables organizations and employees to use Alexa to ...
```


### Example 3: Usage to get matching product(s):
```
from cloud_products import aws
cloud_products = aws.AwsCrawler()
sagemaker_products = cloud_products.get_products_matching("sagemaker")
sagemaker_description = cloud_products.get_product_text(sagemaker_products[0])
print(sagemaker_description[3])
```

Example output:
```
Amazon SageMaker is a fully managed service that provides every developer and data scientist with ...
```


### Example 4: Save product descriptions to files:
```
from cloud_products.aws import AwsCrawler
for product in AwsCrawler().get_products():
    print(f"Saving {product.name}")
    cloud_products.save_product(product, output_path)
```

Example output:
```
Saving Alexa for Business
Saving Amazon MQ
Saving AWS Amplify
Saving Amazon API Gateway
...
```


### Example 5: Convert list of products to [Pandas](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html) dataframe:
```
import pandas as pd
from cloud_products.aws import AwsCrawler
products = AwsCrawler().get_products()
df = pd.DataFrame.from_records([vars(p) for p in products])
```


Cloud Products is distributed under the MIT license.
