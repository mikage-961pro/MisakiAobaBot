# -*- coding: UTF-8 -*-
#=========================================#
# A Roulette wheel algorithm program
# Written by Dephilia
# Copyright 2018
#=========================================#

from random import randrange

def call_random(num,*arg,**karg):
	"""Prevent to change the way to call random."""
	return randrange(num)

class weighted_random():
	def __init__(self):
		self.__pool=[]

	def add(self,data,value=0,*arg,**kwarg):
		if not isinstance(value, int):
			"""data needs to be dict"""
			raise TypeError('Value has to be an interger.')
			return

		if value<0:
			raise ValueError("Value can't be minus.")
			return
		if value==0:
			return

		import copy
		pool_data={'Data':[data],'Value':value}
		self.__pool.append(pool_data)

	def add_none(self,value,*arg,**kwarg):
		if not isinstance(value, int):
			"""data needs to be dict"""
			raise TypeError('Value has to be an interger.')
			return

		if value<0:
			raise ValueError("Value can't be minus.")
			return
		if value==0:
			return
		pool_data={'Data':None,'Value':value}
		self.__pool.append(pool_data)

	def delete(self,data,*arg,**kwarg):
		counter=0
		try:
			for i in self.__pool:
				if data==i['Data'][0]:
					del self.__pool[counter]
				counter+=1
		except:
			raise IndexError("No data can delete.")


	@property
	def pool(self):
		return self.__pool

	def output_one(self,*arg,**kwarg):
		pool=self.pool
		result=None
		if not pool:
			raise ValueError("No data in pool.")
		data_length=len(pool)
		total_probability=0
		temp=[]
		for i in pool:
			total_probability+=i['Value']
			temp.append([i['Data'],total_probability])
		rand_number=call_random(total_probability)
		for i in temp:
			if i[1]>rand_number:
				result = i[0]
				break
		return result
	def clear(self,*arg,**kwarg):
		del self.__pool
		self.__pool=[]

	def output(self,num=1,*arg,**kwarg):
		if num>len(self.__pool):
			raise ValueError("Output number can't over input.")

		counter=num

		def isin(ref,l):
			for ele in l:
				if ele is ref:
					return True
			return False

		temp=[]
		final=[]
		while counter>0:
			result=weighted_random.output_one(self)
			if isin(result,temp):
				continue
			temp.append(result)
			counter-=1
		# dispatcher
		for t in temp:
			final.append(t[0])
		del temp
		return final

def main():
	rand=weighted_random()
	rand.add("apple",12)
	rand.add("apple",12)
	rand.add("banana",10)
	rand.add("cat",15)
	rand.add("dog",20)
	rand.add("elephant",20)
	rand.add("fox",18)
	rand.add("lion",100)
	rand.delete("lion")

	print(rand.output(2))


if __name__=="__main__":
	main()
