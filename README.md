# cloud-products 

A package for getting cloud products and product descriptions from a cloud provider website with cache support.

Currently supports getting AWS product information from  
[https://aws.amazon.com/products](https://aws.amazon.com/products)


### Install from PyPi
```
pip install cloud-products
```


### Example 1: List AWS products
```
from crawler.aws import AwsCrawler
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
from crawler.aws import AwsCrawler
crawler = AwsCrawler()
product = crawler.get_products()[0]
lines = crawler.get_product_text(product)
print(lines[4])
```

Example output:
```
Alexa for Business is a service that enables organizations and employees to use Alexa to ...
```


### Example 3: Usage to get matching product(s):
```
from crawler import aws
crawler = aws.AwsCrawler()
sagemaker_products = crawler.get_products_matching("sagemaker")
sagemaker_description = crawler.get_product_text(sagemaker_products[0])
print(sagemaker_description[3])
```

Example output:
```
Amazon SageMaker is a fully managed service that provides every developer and data scientist with ...
```


### Example 4: Save product descriptions to files:
```
from crawler.aws import AwsCrawler
for product in AwsCrawler().get_products():
    print(f"Saving {product.name}")
    crawler.save_product(product, output_path)
```

Example output:
```
Saving Alexa for Business
Saving Amazon MQ
Saving AWS Amplify
Saving Amazon API Gateway
...
```


Cloud Products is distributed under the MIT license.
