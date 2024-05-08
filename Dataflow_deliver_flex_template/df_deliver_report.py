#!/usr/bin/env python
#  Copyright 2023 Google LLC
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import apache_beam as beam

from apache_beam.options.pipeline_options import PipelineOptions


dataset_id = "bigquery-418908.dataset_py"
delivered_table_spec = 'bigquery-418908:dataset_py.delivered_orders'
other_orders_data_specs = 'bigquery-418908:dataset_py.other_orders'
table_schema = 'customer_id:STRING,date:STRING,timestamp:STRING,order_id:STRING,items:STRING,amount:STRING,mode:STRING,restaurant:STRING,status:STRING,rating:STRING,feedback:STRING,new_col:STRING'
other_table_spec = 'bigquery-418908:dataset_py.other_orders'


def remove_last_column(row: str):

    print("Removing last column ..... ")
    cols = row.split(',')
    item= str(cols[4])
    cols[4] = item[:-1] if item.endswith(':') else ''
    return ','.join(cols)

def remove_special_char (row:str) -> str:
    
    print(f"row: {row}" )
    print("Removing Special Characters...")
    import re 
    cols = row.split(',')
    ret = ''

    for col in cols: 
        clean_col = re.sub(r'[?%&]','' ,col)
        ret = ret + clean_col + ','
    return ret[:-1]

def print_row(row:str):
    print(row)

def to_json(csv_str:str):
    fields = csv_str.split(',')

    json_str = {
        "customer_id":fields[0],
        "date" : fields[1],
        "timestamp": fields[2],
        "order_id": fields[3],
        "items": fields[4],
        "amount": fields[5],
        "mode": fields[6],
        "restaurant": fields[7],
        "status": fields[8],
        "rating": fields[9],
        "feedback" : fields[10],
        "new_col":fields[11]
    }

    return json_str

def bigquery_insertion_process(argv=None):
    print("BigQuery Insertion Process...")
    # Parse the pipeline options passed into the application.
    class MyOptions(PipelineOptions):
        
        # Define a custom pipeline option that specfies the Cloud Storage bucket.
        @classmethod
        def _add_argparse_args(cls, parser):
            parser.add_argument("--input", required=True)
   
    options = MyOptions()
    print(f"input: {options.input}" )    

    print("Starting BigQuery Insertion Process...")
    with beam.Pipeline(options=options) as pipeline:
        cleaned_data = (
            pipeline
            | 'Read input file' >> beam.io.ReadFromText(options.input,skip_header_lines=1)
            | "Removing Last column" >> beam.Map(remove_last_column)
            | "Lower case conversion" >> beam.Map(lambda row:row.lower())
            | "Remove Special Characters" >> beam.Map(remove_special_char)
            | "Adding Incremental 1" >>beam.Map(lambda row: row+',1')
            
        )

        print("Data cleaning process completed...")
        print("Seperating delivered data from the rest of the data.")

        delivered_data = (            
            cleaned_data
           |"Delivered data filter" >> beam.Filter(lambda row: row.split(',')[8].lower() == 'delivered')
           
        )
        print ("delivered data filter completed...")
        other_orders_data = (
            cleaned_data            
            |"Other order data filter" >> beam.Filter(lambda row: row.split(',')[8].lower() != 'delivered')
          
        )
        print("Other order data filter completed....")
        (cleaned_data
            | "Count total cleanned data" >> beam.combiners.Count.Globally()
            | "Total map cleaned data" >> beam.Map(lambda x: 'Total Count : ' + str(x))
            | "print total cleaned data" >> beam.Map(print_row)
         )
        
        (delivered_data
            | 'count total delivered data' >> beam.combiners.Count.Globally() #Global count for all the elements in cleaned data P Collection. count =920
            | 'total map delivered data' >> beam.Map(lambda x: 'Total Count : '+str(x)) # Total Count : 920 
            | 'print total delivered data' >> beam.Map(print_row)
        )

        (other_orders_data
            | 'count total other orders' >> beam.combiners.Count.Globally() #Global count for all the elements in cleaned data P Collection. count =920
            | 'total map other orders' >> beam.Map(lambda x: 'Total Count : '+str(x)) # Total Count : 920 
            | 'print total other orders' >> beam.Map(print_row)
        )

        (delivered_data
            | "delivered to json delivered_orders" >> beam.Map(to_json)
            | "Write Delivered delivered_orders" >> beam.io.WriteToBigQuery(

                table= delivered_table_spec,
                schema = table_schema,
                create_disposition= beam.io.BigQueryDisposition.CREATE_IF_NEEDED, #if table isnt available it will create that.
                write_disposition= beam.io.BigQueryDisposition.WRITE_APPEND,
                additional_bq_parameters={'timePartitioning': {'type':'DAY'}}
                )
        )

        (other_orders_data
            | "other_orders_data to json delivered_orders" >> beam.Map(to_json)
            | "Write Delivered other_orders" >> beam.io.WriteToBigQuery(

                table= other_orders_data_specs,
                schema = table_schema,
                create_disposition= beam.io.BigQueryDisposition.CREATE_IF_NEEDED, #if table isnt available it will create that.
                write_disposition= beam.io.BigQueryDisposition.WRITE_APPEND,
                additional_bq_parameters={'timePartitioning': {'type':'DAY'}}

                )
        )


    print(f"Finished BigQuery Insertion Process...")


if __name__ == "__main__":
    bigquery_insertion_process()
