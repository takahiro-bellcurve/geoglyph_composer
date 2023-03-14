# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

import os
import sentry_sdk

sentry_sdk.init(os.getenv("AIRFLOW__SENTRY__SENTRY_DSN"))
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "../../sodashi-default-service-account.json"

