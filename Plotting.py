import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import Answer_code

def Plotting_line(Y1, Y2, Av_Y1, Av_Y2):

	host = plt.subplot(111)

	host.set_xlim(0, len(Y1))
	print(len(Y2)+1)
	host.set_ylim(0, 1.2 * max(max(Y1), max(Y2)))

	host.set_xlabel("Sales")
	host.set_ylabel("Prices ($)")
	host.xaxis.set_ticks(np.arange(0, len(Y1)+10, 10))
	host.yaxis.label.set_size(20)
	host.xaxis.label.set_size(20)
	host.tick_params(labelsize=20)
	  
	x1 = np.arange(0, len(Y1), 1)
	y1 = np.array(Y1)
	Av_y1 = np.full(len(x1), Av_Y1)
	x2 = np.arange(0, len(Y2), 1)
	y2 = np.array(Y2)
	Av_y2 = np.full(len(x2), Av_Y2)

	print(len(x1), len(Av_y1))

	p1 = host.plot(x1, y1, label="Online", linewidth = 1, c = 'blue')
	Av_p1 = host.plot(x1, Av_y1, label="Online Mean", linewidth = 1, linestyle = '--', c = 'blue')
	p2 = host.plot(x2, y2, label="Call-centre", linewidth = 1, c = 'red')
	Av_p2 = host.plot(x2, Av_y2, label="Call-centre Mean", linewidth = 1, linestyle = '--', c = 'red')

	host.legend(fontsize = 20)

	plt.draw()
	plt.show()
	return


def Plotting_Scatter(Y1, Y2, Av_Y1, Av_Y2):

	host = plt.subplot(111)

	host.set_xlim(0, len(Y1))
	print(len(Y2)+1)
	host.set_ylim(0, 1.2 * max(max(Y1), max(Y2)))

	host.set_xlabel("Sales")
	host.set_ylabel("Ranks")
	host.xaxis.set_ticks(np.arange(0, len(Y1)+10, 10))
	host.yaxis.label.set_size(20)
	host.xaxis.label.set_size(20)
	host.tick_params(labelsize=20)
	  
	x1 = np.arange(0, len(Y1), 1)
	y1 = -np.sort(-np.array(Y1))
	Av_y1 = np.full(len(x1), Av_Y1)
	x2 = np.arange(0, len(Y2), 1)
	y2 = -np.sort(-np.array(Y2))
	Av_y2 = np.full(len(x2), Av_Y2)

	print(len(x1), len(Av_y1))

	p1 = host.scatter(x1, y1, label="Online", marker = 'o', s = 20, c = 'blue')
	Av_p1 = host.plot(x1, Av_y1, label="Online Mean", linewidth = 1.5, linestyle = '--', c = 'blue')
	p2 = host.scatter(x2, y2, label="Call-centre", marker = '+', s = 20, c = 'red')
	Av_p2 = host.plot(x2, Av_y2, label="Call-centre Mean", linewidth = 1.5, linestyle = '--', c = 'red')

	host.legend(fontsize = 20)

	plt.draw()
	plt.show()
	return


def Plotting_Column(A, B):

	host = plt.subplot(111)

	host.set_xlim(0.5, 2.5)
	host.set_ylim(0, 100)

	host.set_xlabel("Sale Source")
	host.set_ylabel("Number of Products from Providers")
	labels = ['Online','Call-centre']
	host.xaxis.set_ticks(np.array([1,2]))
	host.yaxis.label.set_size(20)
	host.xaxis.label.set_size(20)
	host.tick_params(labelsize=20)

	X = [1,2]
	x = np.array(X)
	y1 = np.array(A)
	y2 = np.array(B)
	
	width = 0.2
	p1_O = host.bar(x-width, y1, label="Provider A", width=width , color = '0.2')
	p1_C = host.bar(x, y2, label="Provider B", width=width , color = 'grey')

	host.legend(loc = "best", fontsize = 20)
	plt.tight_layout()
	plt.show()
	return

def Plotting_PVR(Product, PVR):

	fig, host = plt.subplots()

	host.set_xlim(0, 17)
	#host.set_ylim(0, 100)

	host.set_xlabel("Product")
	host.set_ylabel("PVR")
	labels = Product
	host.yaxis.label.set_size(20)
	host.xaxis.label.set_size(20)
	host.tick_params(labelsize=15)

	X = np.arange(1, len(PVR)+1, 1)
	Y = np.array(PVR)
	print(len(X), len(Y))
	plt.xticks(X,labels,rotation = 60)

	width = 0.5
	p1_O = host.bar(X, Y, width =width, color = 'black')

	host.legend(loc = "best", fontsize = 20)
	plt.tight_layout()
	plt.show()
	return

def Plotting_Correlation(X, Y):

	fig, host = plt.subplots()

	host.set_xlim(0, 0.3)
	host.set_ylim(0, 0.2)

	host.set_xlabel("Sold Value Ratio of product")
	host.set_ylabel("Sold Rank Ratio of product")
	
	host.yaxis.label.set_size(20)
	host.xaxis.label.set_size(20)
	host.tick_params(labelsize=15)

	X = np.array(X)
	Y = np.array(Y)
	print(len(X), len(Y))

	width = 0.5
	p = host.scatter(X, Y, marker = '+' , s = 50, color = 'black')
	plt.show()
	return

if __name__ == "__main__":
	Data = Answer_code.DataFrame_Read_in()
	OnlineData, CallcentreData = Answer_code.Online_Callcentre_Data(Data)

	Rank_O = OnlineData['result_rank'].loc[OnlineData['result_rank'] != 'MISSING'].astype(float)
	Value_O = OnlineData['dummy_quote_value'].loc[OnlineData['dummy_quote_value'] != 'MISSING'].astype(float)
	Provider_O = OnlineData['provider_Nm']

	Rank_C = CallcentreData['result_rank'].loc[CallcentreData['result_rank'] != 'MISSING'].astype(float)
	Value_C = CallcentreData['dummy_quote_value'].loc[CallcentreData['dummy_quote_value'] != 'MISSING'].astype(float)
	Provider_C = CallcentreData['provider_Nm']

	OR_M, OR_STD, CR_M, CR_STD, OV_M, OV_STD, CV_M, CV_STD, OPD, CPD = Answer_code.Online_Callcentre_Difference(OnlineData, CallcentreData)
	Product_name, PVR, Value_Product_name, Values, ranks = Answer_code.PVR(Data)

	#Plotting_line(Value_O, Value_C, OV_M, CV_M)
	#Plotting_Scatter(Rank_O, Rank_C, OR_M, CR_M)
	#Plotting_Column([81,99], [40,14])
	#Plotting_PVR(Product_name, PVR)
	Plotting_Correlation(Values, ranks)






