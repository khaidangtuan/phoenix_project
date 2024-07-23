input_json = { \
&ensp;"model": string, \
&ensp;"color": string, \
&ensp;"currency": string, \
&ensp;"rangeType": string, # m|y \
&ensp;"rangeValue": integer # 1|3|5|6 \
}

response_json = { \
&ensp;"currency": string, \
&ensp;"value":[ \
&ensp;{ \
&emsp;"id": integer, \
&emsp;"time": string, \
&emsp;"value": float, \
&emsp;"percent": string # relative difference in price \
&ensp;} \
&ensp;] \
}
