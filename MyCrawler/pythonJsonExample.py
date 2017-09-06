#coding=utf-8
import json
b= 'b'
c='c'
a='a'
data1 = '{b: 789, c: 456, a: 123}'
dictData = eval(data1)
print(type(dictData),dictData)
print(type(dictData))
encode_json = json.dumps(dictData)
print (type(encode_json), encode_json)
 
decode_json = json.loads(encode_json)
print (type(decode_json))
print (decode_json['a'])
print (decode_json)

