# cloud-products 

A package for getting cloud product descriptions from the provider website.

Currently supports aws only.

Usage:

```
products = crawler.get_products()
for product in products:
    lines = crawler.get_product_text(product, output_path)
```

Cloud Products is distributed under the MIT license.
