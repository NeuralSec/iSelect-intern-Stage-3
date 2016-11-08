import pandas as pd
import numpy as np
import math
import operator

def DataFrame_Read_in():
	Data = []
	Data_file = open("Data.txt", 'rt')
	for line in Data_file:
		(Customer_ID, result_rank, provider_Nm, product_name, dummy_quote_value, Sale_made, Sale_source) = line.split('\t')
		Data.append([Customer_ID, result_rank, provider_Nm, product_name, dummy_quote_value, Sale_made, Sale_source])
	Data = np.array(Data)
	Data = pd.DataFrame(Data, columns=['Customer_ID', 'result_rank', 'provider_Nm', 'product_name', 'dummy_quote_value', 'Sale_made', 'Sale_source'])
	#Data[['result_rank', 'dummy_quote_value']] = Data[['result_rank', 'dummy_quote_value']].apply(pd.to_numeric)
	print(Data)
	return Data


def Effectiveness(Data):
	Groups1 = Data.groupby('Customer_ID')['Sale_made'].apply(list)
	#print(Groups1)
	Custom_Num = len(Groups1)

	Hit_number = 0
	for index, row in pd.DataFrame(Groups1).iterrows():
		#print(row[0])
		if '1' in row[0]:
			Hit_number += 1
	SRR = Hit_number/Custom_Num

	Rank_Error = 0
	Sale_Num = 0
	for index, row in pd.DataFrame(Data).iterrows():
		#print(row[5], row[1])
		if row[5] == '1':
			Sale_Num += 1
			Rank_Error += (float(row[1]) - 1)
	MRE = float(Rank_Error/Sale_Num)
	return SRR, MRE


def Online_Callcentre_Data(Data):
	Online_Sales = Data.loc[Data['Sale_source'] == 'online\n']
	Callcentre_Sales = Data.loc[Data['Sale_source'] == 'callcentre\n']
	print(Online_Sales, Callcentre_Sales)
	return Online_Sales, Callcentre_Sales


def Online_Callcentre_Difference(OnlineData, CallcentreData):
	# Analyse differences of rank, value, and provider.
	Rank_O = OnlineData['result_rank'].loc[OnlineData['result_rank'] != 'MISSING'].astype(float)
	Value_O = OnlineData['dummy_quote_value'].loc[OnlineData['dummy_quote_value'] != 'MISSING'].astype(float)
	Provider_O = OnlineData['provider_Nm']

	Rank_C = CallcentreData['result_rank'].loc[CallcentreData['result_rank'] != 'MISSING'].astype(float)
	Value_C = CallcentreData['dummy_quote_value'].loc[CallcentreData['dummy_quote_value'] != 'MISSING'].astype(float)
	Provider_C = CallcentreData['provider_Nm']

	Online_Mean_Rank = np.mean(Rank_O)
	Online_Rank_STD = np.std(Rank_O)
	Callcentre_Mean_Rank = np.mean(Rank_C)
	Callcentre_Rank_STD = np.std(Rank_C)

	Online_Mean_Value = np.mean(Value_O)
	Online_Value_STD = np.std(Value_O)
	Callcentre_Mean_Value = np.mean(Value_C)
	Callcentre_Value_STD = np.std(Value_C)

	Online_Provider_Distribution = [len(Provider_O.loc[OnlineData['provider_Nm'] == 'Provider A']), 
									len(Provider_O.loc[OnlineData['provider_Nm'] == 'Provider B'])]

	Callcentre_Provider_Distribution = [len(Provider_C.loc[CallcentreData['provider_Nm'] == 'Provider A']), 
									len(Provider_C.loc[CallcentreData['provider_Nm'] == 'Provider B'])]

	return Online_Mean_Rank, Online_Rank_STD, Callcentre_Mean_Rank, Callcentre_Rank_STD, Online_Mean_Value, Online_Value_STD, Callcentre_Mean_Value, Callcentre_Value_STD, Online_Provider_Distribution, Callcentre_Provider_Distribution


def PVR(Data):
	PVR_dict = {}
	Value_dict = {}
	Rank_dict = {}
	Sold_numbers = {}
	All_numbers = {}
	Product_number = {}
	Product_Mean_Rank = {}

	product_rank = pd.DataFrame(Data.groupby('product_name')['result_rank'].apply(list))
	product_price = pd.DataFrame(Data.groupby('product_name')['dummy_quote_value'].apply(list))
	print(product_rank, product_price, '\n')
	
	Sold_products = Data.loc[Data['Sale_source'] != '\n']
	Sold_product_rank = pd.DataFrame(Sold_products.groupby('product_name')['result_rank'].apply(list))
	Sold_product_price = pd.DataFrame(Sold_products.groupby('product_name')['dummy_quote_value'].apply(list))
	print(Sold_product_rank, Sold_product_price, '\n')

	for product in product_rank.index:
		#print(product)
		if product in Sold_product_rank.index:
			Ranks = product_rank.loc[product,'result_rank']
			Prices = product_price.loc[product,'dummy_quote_value']
			Sold_Ranks = Sold_product_rank.loc[product,'result_rank']
			Sold_price = Sold_product_price.loc[product,'dummy_quote_value']

			Sold_numbers[product] = len(Sold_Ranks)
			All_numbers[product] = len(Ranks)

			Divided = 0
			Divide = 0

			Value_Divided = 0
			Value_Divide = 0
			Rank_Divided = 0
			Rank_Divide = 0
			# Divide
			for i in range(len(Prices)):
				if Prices[i]!='MISSING' and Ranks[i]!='MISSING':
					Divide += float(Prices[i]) * math.log(1 + (1/float(Ranks[i])))
					Value_Divide += float(Prices[i])
					Rank_Divide += math.log(1 + (1/float(Ranks[i])))
			# Divided
			for j in range(len(Sold_price)):
				if Sold_price[j]!='MISSING' and Sold_Ranks[j]!='MISSING':
					Divided += float(Sold_price[j]) * math.log(1 + (1/float(Sold_Ranks[j])))
					Value_Divided += float(Sold_price[j])
					Rank_Divided += math.log(1 + (1/float(Sold_Ranks[j])))

			PVR_dict[product] = Divided/Divide
			Value_dict[product] = Value_Divided/Value_Divide
			Rank_dict[product] = Rank_Divided/Rank_Divide

		else:
			PVR_dict[product] = 0
			Value_dict[product] = 0
			Rank_dict[product] = 0

	Sorted_PVR_dict = sorted(PVR_dict.items(), key=operator.itemgetter(1))
	Sorted_Value_dict = sorted(Value_dict.items(), key=operator.itemgetter(1))
	print(Sorted_PVR_dict)

	PVR_Array = []
	Product_Array = []
	for Pair in Sorted_PVR_dict:
		print(Pair)
		Product_Array.append(Pair[0])
		PVR_Array.append(Pair[1])
	
	Value_Product_Array = []
	Value_array = []
	Rank_array = []
	for Pair in Sorted_Value_dict:
		print(Pair)
		Value_Product_Array.append(Pair[0])
		Value_array.append(Pair[1])
		Rank_array.append(Rank_dict[Pair[0]])

	PVR_Array = np.array(PVR_Array)
	Product_Array = np.array(Product_Array)
	Value_Product_Array = np.array(Value_Product_Array)
	Value_array = np.array(Value_array)
	Rank_array = np.array(Rank_array)

	print(Product_Array, PVR_Array, Value_Product_Array, Value_array, Rank_array)
	return Product_Array, PVR_Array, Value_Product_Array, Value_array, Rank_array
	 

if __name__ == '__main__':
	Data = DataFrame_Read_in()
	#Online_Sales, Callcentre_Sales = Online_Callcentre_Data(Data)

	# Q1
	#print(Effectiveness(Data))
	# Q2
	#print(Online_Callcentre_Difference(Online_Sales, Callcentre_Sales))
	# Q3
	PVR(Data)
	