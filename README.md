Open Source Data Ingestion Engine for Sensor Data
Oisin Whelan 15558517

Supervisor - Dr Georgiana Ifrim
Co-Supervisor - Dr Fabiano Pallonetto

Running this project requires a MongoDB environment to be set up, as well as the pymongo, flask, ratelimit and bson
Python packages.
A shell script is included to run the entire project, otherwise db_setup.py is required to be run first,
and then either of get_all_data_from_node.py and poll_all_nodes.py can be run to extract data.