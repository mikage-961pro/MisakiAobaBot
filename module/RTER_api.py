# coding=utf-8

def exrate_twbank(output_currency,input_currency='TWD',*arg,**kwarg):
	__source__="""

此服務由台灣銀行
https://rate.bot.com.tw/
所提供

"""
	from urllib import request
	import requests
	import csv
	from decimal import Decimal
	data={}
	url = "https://rate.bot.com.tw/xrt/flcsv/0/day"

	def csv_import(url):
		import io
		data={}
		url_open = request.urlopen(url)
		csvfile = csv.reader(io.TextIOWrapper(url_open, encoding = 'utf-8'), delimiter=',')
		index=None
		index_jump=True
		length=None
		for row in csvfile:

			if index_jump:
				index_jump=False
				index=row
				length=len(index)
				continue
			data[row[0]]={
			'本行買入':{
				'現金':row[2],
				'即期':row[3]
				},
			'本行賣出':{
				'現金':row[12],
				'即期':row[13]
				}

			}



		return data
	exrate_data=csv_import(url)
	aim_data=exrate_data[output_currency]
	return aim_data['本行賣出']['即期']




def exRate(input_currency,output_currency,*arg,**kwarg):
	__source__="""

此服務由即匯站
https://tw.rter.info/howto_currencyapi.php
所提供

"""
	import requests
	from decimal import Decimal
	data={}
	r=requests.get('https://tw.rter.info/capi.php')
	currency=r.json()
	usd2input="USD"+input_currency.upper()
	usd2output="USD"+output_currency.upper()
	try:
		output_data=currency[usd2input]['Exrate']/currency[usd2output]['Exrate']
		dealing=Decimal(output_data).quantize(Decimal('0.0000'))
		data['Exrate']=float(dealing)
		data['UTC']=currency[usd2input]['UTC']
	except KeyError:
		e_text="Unknown currency: "+input_currency+" > "+output_currency
		raise IndexError(e_text)

	return data

def main():
	try:
		data=exrate_twbank("JPY")
		print(data)
		#print("Exrate:\t",data['Exrate'])
		#print("Time:\t",data['UTC'])
	except IndexError as e:
		print(e)


if __name__=="__main__":
	main()
