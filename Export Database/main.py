import mysql.connector
import csv
from mysql.connector import errorcode

def writesome(mycursor, some,csv_writer):
    fetch = mycursor.fetchmany
    while True:
        rows = fetch(some)
        if not rows: break
        csv_writer.writerows(rows)

try:
	conn = mysql.connector.connect(user='root',password='067792862',host='localhost',database='set2')
	mycursor = conn.cursor()

	mycursor.execute("""
       			select SecurityId,SecurityName
             	from compsec   
            	where SecurityId = 1             
               """)
	rows_firstQuery = mycursor.fetchall()
	for row_firstQuery in rows_firstQuery:
		mycursor.execute("""
   			select Date,SecurityName,Open,High,Low,Close
         	from d_trade   
        	where SecurityId = %s 
        	and TradingMethod = %s
           """,[str(row_firstQuery[0]),'A'])		
		with open("C:/Repository/SiamQuant/Export Database/trading/"+str(row_firstQuery[1])+".csv", "w") as csv_file:
			csv_writer = csv.writer(csv_file)
	   		csv_writer.writerow([i[0] for i in mycursor.description]) # write headers
			writesome(mycursor,1000,csv_writer)

except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)
else:
  conn.close()	

  #select d_trade.Date,d_trade.SecurityName,d_trade.Open,d_trade.High,d_trade.Low,d_trade.Close,d_stat.Benefit,d_stat.DividendYield,d_stat.ParValue
  #       	from d_trade   
  #          inner join d_stat
  #          on d_trade.Date = d_stat.Date
  #          and d_trade.SecurityId = d_stat.SecurityId
  #      	where d_trade.SecurityId = 1 
  #      	and d_trade.TradingMethod = 'A'
  #          and d_trade.Date <= '19760101'
            