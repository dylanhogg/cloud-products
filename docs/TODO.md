# TODO

1) Add Github build and release actions to pypi
1) Manifest file fixes & check manifest is ok: https://github.com/mgedmin/check-manifest
1) Ensure pypi source is compilable
1) Fix extras_require and test_requiremetns etc (e.g. pandas)
1) Run static type checking with https://mypy.readthedocs.io/en/stable/
1) Compare output with: https://d1.awsstatic.com/whitepapers/aws-overview.pdf 
1) Fix faq crawling for non-standard links:
    FAQ page did not exist: https://aws.amazon.com/aws-cost-management/aws-budgets/faq/
    FAQ page did not exist: https://aws.amazon.com/aws-cost-management/aws-cost-and-usage-reporting/faq/
    FAQ page did not exist: https://aws.amazon.com/aws-cost-management/aws-cost-explorer/faq/
    FAQ page did not exist: https://aws.amazon.com/aws-cost-management/reserved-instance-reporting/faq/
    FAQ page did not exist: https://aws.amazon.com/cli/faq/
    FAQ page did not exist: https://aws.amazon.com/cloudendure-disaster-recovery/faq/
    FAQ page did not exist: https://aws.amazon.com/cloudendure-migration/faq/
    FAQ page did not exist: https://aws.amazon.com/elastic-inference/faq/
    FAQ page did not exist: https://aws.amazon.com/elemental-appliances-software/faq/
    FAQ page did not exist: https://aws.amazon.com/getting-started/tools-sdks/faq/
    FAQ page did not exist: https://aws.amazon.com/glacier1/faq/
    FAQ page did not exist: https://aws.amazon.com/inferentia/faq/
    FAQ page did not exist: https://aws.amazon.com/iot/button/faq/
    FAQ page did not exist: https://aws.amazon.com/machine-learning/amis/faq/
    FAQ page did not exist: https://aws.amazon.com/mxnet/faq/
    FAQ page did not exist: https://aws.amazon.com/premiumsupport/phd/faq/
    FAQ page did not exist: https://aws.amazon.com/privatelink/faq/
    FAQ page did not exist: https://aws.amazon.com/pytorch/faq/
    FAQ page did not exist: https://aws.amazon.com/rds/aurora/serverless/faq/
    FAQ page did not exist: https://aws.amazon.com/sagemaker/data-wrangler/faq/
    FAQ page did not exist: https://aws.amazon.com/serverlessrepo/faq/
    FAQ page did not exist: https://aws.amazon.com/tensorflow/faq/
    FAQ page did not exist: https://aws.amazon.com/trustedadvisor/faq/


# NOTES

## Python packaging references

[Packaging Python Projects](https://packaging.python.org/tutorials/packaging-projects/)

[How To Package Your Python Code](https://python-packaging.readthedocs.io/en/latest/)

[Less known packaging features and tricks presentation](https://blog.ionelmc.ro/presentations/packaging/)


## GitHub Action references

[Workflow syntax for GitHub Actions](https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions)

[Reference for building actions and creating workflows](https://docs.github.com/en/actions/reference)

[Using Python with GitHub Actions](https://help.github.com/en/actions/language-and-framework-guides/using-python-with-github-actions)

[Python Github Actions](https://github.com/actions/starter-workflows/tree/master/ci)

    https://fastpages.fast.ai/actions/markdown/2020/03/06/fastpages-actions.html
    https://github.com/actions/starter-workflows/blob/master/ci/python-app.yml
    older: https://github.com/macbre/sql-metadata/blob/master/.github/workflows/pythonapp.yml
    https://github.com/actions/starter-workflows/blob/master/ci/python-package.yml
    https://github.com/actions/starter-workflows/blob/master/ci/python-publish.yml
