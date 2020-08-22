#!/bin/bash

cp python/objects/currency.py python_plain/

cp python/objects/percentage.py python_plain/

cp python/github.py python_plain/

cp python/myconfigparser.py python_plain/
sed -i -e 's/\.datetime_functions/datetime_functions/' python_plain/myconfigparser.py
sed -i -e 's/\.casts/casts/' python_plain/myconfigparser.py

cp python/casts.py python_plain/
sed -i -e 's/ \.objects./ /' python_plain/casts.py

cp python/admin_pg.py python_plain/
sed -i -e 's/ \.connection/ connection/' python_plain/admin_pg.py

cp python/call_by_name.py python_plain/

cp python/connection_pg.py python_plain/
sed -i -e 's/\.casts/casts/' python_plain/connection_pg.py

cp python/package_resources.py python_plain/

cp python/libmanagers.py python_plain/
sed -i -e 's/ \.call_by_name/ call_by_name/' python_plain/libmanagers.py
sed -i -e 's/\.datetime_functions/datetime_functions/' python_plain/libmanagers.py
