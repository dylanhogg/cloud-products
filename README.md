# cloud-products 

[![pypi Version](https://img.shields.io/pypi/v/cloud-products.svg?logo=pypi)](https://pypi.org/project/cloud-products/)
![Latest Tag](https://img.shields.io/github/v/tag/dylanhogg/cloud-products)
![Dependencies](https://img.shields.io/librariesio/github/dylanhogg/cloud-products)
![Build](https://github.com/dylanhogg/cloud-products/workflows/build/badge.svg)

A package for getting cloud products and product descriptions from a cloud provider website with cache support.

Currently supports getting AWS product information from 
[https://aws.amazon.com/products](https://aws.amazon.com/products)

GCP and Azure product information will be added in time.


### Install from PyPi
```shell script
pip install cloud-products
```


### Example 1: List AWS products
```python
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
```python
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
```python
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
```python
from cloud_products import aws
cloud_products = aws.AwsCrawler()
for product in cloud_products.get_products():
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


### Example 5: Get [Pandas](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html) dataframe of products:
Note: requires the optional `pandas` package to be installed.  

This dataframe has the product name, code, url and full descriptions.

```python
from cloud_products.aws import AwsCrawler
df = AwsCrawler().get_products_as_df()
print(df)
```

Example output:
```
                   name            std_name              code  ...                          seed_url                                               desc                                       product_text
0    Alexa for Business  alexa for business  alexaforbusiness  ...  https://aws.amazon.com/products/               Empower your Organization with Alexa  Alexa for Business Use Alexa for work Get Star...
1             Amazon MQ              aws mq         amazon-mq  ...  https://aws.amazon.com/products/                     Managed Message Broker Service  Amazon MQ Fully managed service for open sourc...
2           AWS Amplify         aws amplify           amplify  ...  https://aws.amazon.com/products/       Build and deploy mobile and web applications  AWS Amplify Fastest, easiest way to build mobi...
3    Amazon API Gateway     aws api gateway       api-gateway  ...  https://aws.amazon.com/products/                     Build, Deploy, and Manage APIs  Amazon API Gateway Create, maintain, and secur...
4          AWS App Mesh        aws app mesh          app-mesh  ...  https://aws.amazon.com/products/                  Monitor and control microservices  AWS App Mesh Application-level networking for ...
```


Cloud Products is distributed under the MIT license.
