from typing import Union, List
from fastapi import FastAPI
from pydantic import BaseModel, TypeAdapter
from datetime import datetime
import sqlalchemy as sa
from sqlalchemy import text
import psycopg2
import pandas as pd
from pandas.tseries.offsets import DateOffset
from utils import curr_convert
from postgres_config import conn_str



class Item(BaseModel):
    model: str
    color: str
    currency: str # vnd|usd|hkd|eur
    rangeType: str  # m|y
    rangeValue: int  # 1|3|5|6

class Value(BaseModel):
    id: int
    time: str
    value:float
    percent:str
    
class PriceList(BaseModel):
    currency: str # vnd|usd|hkd|eur
    value: List[Value]

# initiate engine
engine = sa.create_engine(conn_str)    

# get static currency due to posibility of time-out request to VCB
curr_df = pd.read_pickle('curr_data.pkl')

app = FastAPI()

@app.post('/getListPrice')
def getListPrice(item:Item) -> PriceList:
    # calculate date range
    end_date = datetime.now().strftime('%Y-%m-%d') # today
    if item.rangeType == 'm':
        delta = DateOffset(months=item.rangeValue)
    elif item.rangeType == 'y':
        delta = DateOffset(years=item.rangeValue)
        
    start_date = (datetime.now() - delta).strftime('%Y-%m-%d')
    
    query = f'''
    SELECT "Date", "mean"
    FROM public."daily_price"
    WHERE model = '{item.model}' 
    AND color = '{item.color}' 
    AND "Date" BETWEEN '{start_date}' AND '{end_date}'
    ORDER BY "Date" ASC;
    '''
    
    with engine.connect() as conn:
        results = pd.read_sql(text(query), conn)
    
    results['percent'] = (results['mean'] - results['mean'].shift(1))/results['mean'].shift(1)*100
    results.reset_index(inplace=True)
    results.rename(columns={'index':'id',
                            'Date':'time',
                            'mean':'value'}, inplace=True)
    results['time'] = results['time'].apply(lambda x: x.strftime('%d/%m/%Y'))
    results['value'] = results['value'].apply(lambda x: curr_convert(x, curr_df, 'eur'))
    results.fillna('', inplace=True)
    results['percent'] = results['percent'].astype(str)
    
    ta = TypeAdapter(List[Value])
    values = ta.validate_python(results.to_dict('records'))
    
    return PriceList(currency=item.currency,
                     value=values)

    
    
    
    
    