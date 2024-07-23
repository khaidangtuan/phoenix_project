input_json = { \
&ensp"model": string, \
&ensp"color": string, \
&ensp"currency": string, \
&ensp"rangeType": string, # m|y \
&ensp"rangeValue": integer # 1|3|5|6 \
}

response_json = {
  "currency": string,
  "value":[
    {
      "id": integer,
      "time": string,
      "value": float,
      "percent": string # relative difference in price
    }
  ]

}
