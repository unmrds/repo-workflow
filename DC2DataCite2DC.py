#!/usr/bin/env python

import config
import repositories

# define connection info for Digital Commons repository
dc_test = repositories.DigitalCommons(
    config.dc_endpoint,
    config.dc_host,
    config.dc_api_token,
)

# dc_test.test()
# print()

results = dc_test.query(
    metadata_field=("parent_link","http://digitalrepository.unm.edu/amst_etds"),
    limit=1,
)

print(results)


