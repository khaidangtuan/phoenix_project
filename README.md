input_json = { \
\t"model": string, \
\t"color": string, \
\t"currency": string, \
\t"rangeType": string, # m|y \
\t"rangeValue": integer # 1|3|5|6 \
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
