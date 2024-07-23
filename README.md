input_json = { \
  "model": string, \
  "color": string, \
  "currency": string,
  "rangeType": string, # m|y
  "rangeValue": integer # 1|3|5|6
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
