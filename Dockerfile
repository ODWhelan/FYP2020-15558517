FROM python:3
ADD *.py node_data_out.json nodes.txt
RUN pip install pymongo bson
CMD bash ./runtime.sh