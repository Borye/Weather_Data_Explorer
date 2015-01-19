
import urllib, urllib2, json, os, sys 
from pandas import Series, DataFrame
import pandas as pd
import time 

def fetch(cityid):
	apikey = '8fb46ebbbb9295ded27ca9c4269c3f2b'
	apicode = 'weather_today_sk'
	rettype = 'json'

	# link address
	url = 'http://api.datatang.com/data/open'
	paramsData = {'apikey': apikey, 'apicode': apicode, 'rettype': rettype, 'cityid': cityid}
	params = urllib.urlencode(paramsData)

	# URL request
	add_header = {'User-Agent': 'Chrome'}
	req = urllib2.Request(url, params, add_header)
	resp = urllib2.urlopen(req)
	content = resp.read()

	return content

def transform(weather_data):
	df = DataFrame(weather_data['weatherinfo'], 
		           columns = ['city',
		                      'cityid',
		                      'temp',
		                      'WD',  
		                      'SD', 
		                      'WSE', 
		                      'time', 
		                      'isRadar', 
		                      'Radar'], 
		           index = [0])
	#df['city'] = "Beijing"
	return df

def addcol(weather_dataframe, weather_final):
	add = weather_dataframe.ix[0, :].tolist()
	num = len(weather_final.index)
	weather_final.loc[num] = add
	return weather_final

if __name__ == "__main__":
	for i in range(6, 30):
		print "--------------------Start fetch api (10 min) " + " " + str(i) + "------------------"  
		
		try:
			weather_final = DataFrame({'city': 0, 'cityid': 0, 'temp': 0, 'WD': 0, 'SD': 0, 'WSE': 0, 'time': 0, 'isRadar': 0, 'Radar': 0}, index = [0])
			# cityid = ['101010100']
			cityid = ['101010100', '101020100', '101030100', '101040100', '101050101', '101060101', '101070101', '101080101', '101090101', '101130101', '101160101', '101150101', '101110101', '101170101', '101180101', '101120101', '101100101', '101220101', '101200101', '101250101', '101190101', '101270101', '101260101', '101290101', '101300101', '101140101', '101210101', '101240101', '101280101', '101230101', '101310101']
			for id in cityid:
				try:
					weather_data = json.loads(fetch(id))
				except Exception, exp:
					print exp
					print "???" + str(id)
					continue
				print id
				weather_dataframe = transform(weather_data)
				weather_final = addcol(weather_dataframe, weather_final)

			weather_final.columns = ['city', 'cityid', 'temp', 'WD', 'SD', 'WSE', 'time', 'isRadar', 'Radar']    # change col names to the right order
			weather_final = weather_final.drop(0)     # delete the first row which contian all 0 values

			# change chinese name to english name
			# weather_final['city'] = ['Beijing', 'Shanghai', 'Tianjin', 'Chongqing', 'Haerbin', 'Changchun', 'Shenyang', 'Huhehaote', 'Shijiazhuang', 'Wulumuqi', 'Lanzhou', 'Xining', 'Xian', 'Yinchuan', 'Zhengzhou', 'Jinan', 'Taiyuan', 'Hefei', 'Wuhan', 'Changsha', 'Nanjing', 'Chengdu', 'Guiyang', 'Kunming', 'Nanning', 'Lasa', 'Hangzhou', 'Nanchang', 'Guangzhou', 'Fuzhou', 'Haikou']

			direc = 'weather_10min_' + str(i) +'.csv'
			weather_final.to_csv(direc, index = False, header = True, encoding = "utf-8")
			print weather_final

		except Exception, exp:
			print exp

		print "--------------------Finish fetch api (10 min) " + " " + str(i) + "-----------------"

		print "time ticker on"
		time.sleep(600)
		print "time ticker off"


