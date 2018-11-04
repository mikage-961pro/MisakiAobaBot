# coding=utf-8
"""
此服務來源由
https://tw.rter.info/howto_currencyapi.php
所提供
"""
__source__="""

此服務由即匯站
https://tw.rter.info/howto_currencyapi.php
所提供

"""

def exRate(input_currency,output_currency,*arg,**kwarg):
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
		data=exrate("TWD","JPY")
		print("Exrate:\t",data['Exrate'])
		print("Time:\t",data['UTC'])
	except IndexError as e:
		print(e)

	print(__source__)

if __name__=="__main__":
	main()
