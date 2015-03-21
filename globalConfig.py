from table_config.trading import d_trade
from table_config.trading import d_cust
from table_config.trading import d_stat
from table_config.company import compsec

dateSetFormat = "%d/%m/%Y"
dateTimeSetFormat = "%d/%m/%Y%H:%M"
root_file_path = "C:/Users/admin/Downloads/PSIMS data test/" 
trading_file_path = "/trading/" 
company_file_path = "/company/"
global_configs = [{
					"FileName" : "d_trade.Dat",
					"FilePath" : trading_file_path,
					"DatabaseTableName" : "d_trade",
					"Config" : d_trade.configs
				},{
					"FileName" : "d_cust.Dat",
					"FilePath" : trading_file_path,
					"DatabaseTableName" : "d_cust",
					"Config" : d_cust.configs
				},{
					"FileName" : "d_stat.Dat",
					"FilePath" : trading_file_path,
					"DatabaseTableName" : "d_stat",
					"Config" : d_stat.configs
				},{
					"FileName" : "compsec.Dat",
					"FilePath" : company_file_path,
					"DatabaseTableName" : "compsec",
					"Config" : compsec.configs
				}]

def getFileConfig(fileName):
	for global_config in global_configs:
		if global_config["FileName"] == fileName:
			return global_config





