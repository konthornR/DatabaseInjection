import mysql.connector
import sys
import datetime
from mysql.connector import errorcode
import globalConfig

dateFileFormat = "%d%m%Y"
readDateFrom = datetime.datetime.strptime(globalConfig.dateFrom,dateFileFormat)
readDateTo = datetime.datetime.strptime(globalConfig.dateTo,dateFileFormat)
readFiles = globalConfig.readFiles

def readLineAndSendToDatabase(lines,fileConfig,mycursor):
	for line in lines:
		sqlContentInput = {}	
		primaryKeyNames = []
		contentKeyNames = []	
		primaryContent = []
		infoContent = []	
		setphase = [] #SET content into Table
		wherephase = [] #condition 
		for config in fileConfig["Config"]:
			content = line[config["StartPosition"]-1:config["EndPosition"]]
			content = content.strip()
			if content: 
				if config["Type"] == "String":
					content = '"'+str(content)+'"'
				elif config["Type"] == "Date":
					content = datetime.datetime.strptime(content,globalConfig.dateSetFormat)
					content = content.strftime("%Y%m%d")
				elif config["Type"] == "DateTime":
					content = datetime.datetime.strptime(content,globalConfig.dateTimeSetFormat)
					content = content.strftime("%Y%m%d%H%M%S")
				elif config["Type"] == "Int":
					content = int(content)
				elif config["Type"] == "Decimal":
					content = float(content)
					decimalplaces = 2 #Default Decimal Places
					if config["DecimalPlaces"]:
						decimalplaces = config["DecimalPlaces"]
					content = ('{0:.'+str(decimalplaces)+'f}').format(content)

				content = str(content)
				if config["IsPrimaryKey"] == True:
					primaryKeyNames.append(config["Name"])	
				elif config["IsPrimaryKey"] == False:	
					contentKeyNames.append(config["Name"])
				sqlContentInput[config["Name"]] = content
		
		for primaryKeyName in primaryKeyNames:
			primaryContent.append(sqlContentInput[primaryKeyName])
			wherephase.append(primaryKeyName+"="+sqlContentInput[primaryKeyName])
		for contentKeyName in contentKeyNames:
			infoContent.append(sqlContentInput[contentKeyName])
			setphase.append(contentKeyName+"="+sqlContentInput[contentKeyName])	
			
		if sqlContentInput["RecordFlag"] == '"I"': #Insert into Database Only Primary Key						
			#print("INSERT INTO "+ fileConfig["DatabaseTableName"] +" ("+ ','.join(primaryKeyNames) +") VALUES("+  ','.join(primaryContent) +")")
			mycursor.execute("INSERT INTO "+ fileConfig["DatabaseTableName"] +" ("+ ','.join(primaryKeyNames) +") VALUES("+  ','.join(primaryContent) +")")

		if sqlContentInput["RecordFlag"] == '"I"' or sqlContentInput["RecordFlag"] == '"U"': #Insert(Update) into Database Content using Primary Key index	
			#print("UPDATE "+ fileConfig["DatabaseTableName"] +" SET "+','.join(setphase)+" WHERE "+' AND '.join(wherephase))
			mycursor.execute("UPDATE "+ fileConfig["DatabaseTableName"] +" SET "+','.join(setphase)+" WHERE "+' AND '.join(wherephase))
		
		if sqlContentInput["RecordFlag"] == '"D"':
			mycursor.execute("DELETE FROM "+ fileConfig["DatabaseTableName"] +" WHERE "+' AND '.join(wherephase))
	return

try:
	conn = mysql.connector.connect(user=globalConfig.database_username,password=globalConfig.database_password,host=globalConfig.database_host,database=globalConfig.database_schema)
	mycursor = conn.cursor()

	readingDate = readDateFrom
	while readingDate<=readDateTo:
		for readFile in readFiles:
			#Get readFile Config
			fileConfig = globalConfig.getFileConfig(readFile)
			try:
				text_file = open(globalConfig.root_file_path+readingDate.strftime("%d%m%Y")+fileConfig["FilePath"]+fileConfig["FileName"],"r")
				lines = text_file.readlines()
				text_file.close()				
				readLineAndSendToDatabase(lines,fileConfig,mycursor)	
				conn.commit()	
				print("Commit into Database for date:"+readingDate.strftime("%d%m%Y")+ " File:"+fileConfig["FileName"])				
			except IOError:
				print("Cannot find this text_file:"+ globalConfig.root_file_path+readingDate.strftime("%d%m%Y")+fileConfig["FilePath"]+fileConfig["FileName"])	
		readingDate += datetime.timedelta(days=1)

except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)
else:
  conn.close()	



input("Press Enter to continue...")
