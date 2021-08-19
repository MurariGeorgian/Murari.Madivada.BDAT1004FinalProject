from flask import Flask, render_template, request
from flask_mysqldb import MySQL
from flask_cors import CORS, cross_origin
import MySQLdb
import json
import time
import random

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'remotemysql.com'
app.config['MYSQL_USER'] = 'YZet9nbmXs'
app.config['MYSQL_PASSWORD'] = 'CfNUTaDk19'
app.config['MYSQL_DB'] = 'YZet9nbmXs'

mysql = MySQL(app)

CORS(app)

@app.route('/', methods=['GET', 'POST'])
@cross_origin(origin='*')
def index():
    # Get Items by State
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT State, COUNT(*) AS StateCount FROM `superstore` GROUP BY State")
    statecounts = cur.fetchall()

    # Get Items by Category
    cur.execute("SELECT Category, COUNT(*) AS CatCount FROM `superstore` GROUP BY Category")
    catcounts = cur.fetchall()

    # Get Items by SubCategory
    cur.execute("SELECT SubCategory, COUNT(*) AS SubCatCount FROM `superstore` GROUP BY SubCategory")
    subcatcounts = cur.fetchall()

    # Get Items by Region
    cur.execute("SELECT Region, COUNT(*) AS RegCount FROM `superstore` GROUP BY Region")
    regioncounts = cur.fetchall()

    # Get Items by Segment
    cur.execute("SELECT Segment, COUNT(*) AS SegCount FROM `superstore` GROUP BY Segment")
    segmentcounts = cur.fetchall()

    # Get Items by ShipMode
    cur.execute("SELECT ShipMode, COUNT(*) AS ShipCount FROM `superstore` GROUP BY ShipMode")
    shipmodecounts = cur.fetchall()

    # Get Profit by Month and Year
    cur.execute("SELECT MONTHNAME(OrderDate) AS OrderMonth, YEAR(OrderDate) AS OrderYear, SUM(SALES) AS TotalSales, SUM(Profit) As TotalProfit FROM `superstore` GROUP BY OrderYear, OrderMonth ORDER BY OrderYear ASC, OrderMonth ASC")
    ordertotalvalue = cur.fetchall()

    # Get Sales and Profit by Category
    cur.execute("SELECT Category, SUM(SALES) AS TotalSales, SUM(Profit) AS TotalProfit FROM `superstore` GROUP BY Category ORDER BY Category ASC")
    cattotalvalues = cur.fetchall()

    # Get Sales and Profit by SubCategory
    cur.execute("SELECT SubCategory, SUM(SALES) AS TotalSales, SUM(Profit) AS TotalProfit FROM `superstore` GROUP BY SubCategory ORDER BY SubCategory ASC")
    subcattotalvalues = cur.fetchall()

    data=dict()
    statenames_list=[]
    statecounts_list=[]
    statecolors=[]
    catnames_list=[]
    catcounts_list=[]
    catcolors=[]
    subcatnames_list=[]
    subcatcounts_list=[]
    subcatcolors=[]
    
    orderprofitlabels=[]
    orderprofitvalues=[]
    orderprofitcolors=[]

    ordersaleslabels=[]
    ordersalesvalues=[]
    ordersalescolors=[]

    catsaleslabels=[]; catprofitlabels=[]
    catsalesvalues=[]; catprofitvalues=[]
    catsalescolors=[]; catprofitcolors=[]

    subcatsaleslabels=[]; subcatprofitlabels=[]
    subcatsalesvalues=[]; subcatprofitvalues=[]
    subcatsalescolors=[]; subcatprofitcolors=[]

    data['state'] = statecounts
    data['category'] = catcounts
    data['subcategory'] = subcatcounts
    data['region'] = regioncounts
    data['segmentcounts'] = segmentcounts
    data['shipmodecounts'] = shipmodecounts

    r = lambda: random.randint(0,255)

    for itm in statecounts:
        statenames_list.append(str(itm['State']))
        statecounts_list.append(itm['StateCount'])
        statecolors.append('#%02X%02X%02X' % (r(),r(),r()))
    
    for itm in catcounts:
        catnames_list.append(str(itm['Category']))
        catcounts_list.append(itm['CatCount'])
        catcolors.append('#%02X%02X%02X' % (r(),r(),r()))
    
    for itm in subcatcounts:
        subcatnames_list.append(str(itm['SubCategory']))
        subcatcounts_list.append(itm['SubCatCount'])
        subcatcolors.append('#%02X%02X%02X' % (r(),r(),r()))
    
    for itm in ordertotalvalue:
        orderprofitlabels.append(str(itm['OrderMonth'])+" "+str(itm['OrderYear']))
        orderprofitvalues.append(itm['TotalProfit'])
        orderprofitcolors.append('#%02X%02X%02X' % (r(),r(),r()))
    
    for itm in ordertotalvalue:
        ordersaleslabels.append(str(itm['OrderMonth'])+" "+str(itm['OrderYear']))
        ordersalesvalues.append(itm['TotalSales'])
        ordersalescolors.append('#%02X%02X%02X' % (r(),r(),r()))

    for itm in cattotalvalues:
        catsaleslabels.append(itm['Category'])
        catprofitlabels.append(itm['Category'])
        catsalesvalues.append(itm['TotalSales'])
        catprofitvalues.append(itm['TotalProfit'])
        catsalescolors.append('#%02X%02X%02X' % (r(),r(),r()))
        catprofitcolors.append('#%02X%02X%02X' % (r(),r(),r()))
    
    for itm in subcattotalvalues:
        subcatsaleslabels.append(itm['SubCategory'])
        subcatprofitlabels.append(itm['SubCategory'])
        subcatsalesvalues.append(itm['TotalSales'])
        subcatprofitvalues.append(itm['TotalProfit'])
        subcatsalescolors.append('#%02X%02X%02X' % (r(),r(),r()))
        subcatprofitcolors.append('#%02X%02X%02X' % (r(),r(),r()))

    return render_template('index.html', catsaleslabels=catsaleslabels, catprofitlabels=catprofitlabels, catsalesvalues=catsalesvalues, catprofitvalues=catprofitvalues, catsalescolors=catsalescolors, catprofitcolors=catprofitcolors,
    subcatsaleslabels=subcatsaleslabels, subcatprofitlabels=subcatprofitlabels, subcatsalesvalues=subcatsalesvalues, subcatprofitvalues=subcatprofitvalues, subcatsalescolors=subcatsalescolors, subcatprofitcolors=subcatprofitcolors,
    orderprofitlabels=orderprofitlabels, orderprofitvalues=orderprofitvalues, orderprofitcolors=orderprofitcolors, ordersaleslabels=ordersaleslabels, ordersalesvalues=ordersalesvalues, ordersalescolors=ordersalescolors, data=data, statenames=statenames_list, statecounts=statecounts_list, statecolors=statecolors, catnames=catnames_list, catcounts=catcounts_list, catcolors=catcolors, subcatnames=subcatnames_list, subcatcounts=subcatcounts_list, subcatcolors=subcatcolors)

@app.route('/items', methods=['GET'])
@cross_origin(origin='*')
def getItems():
    # Get All Items
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM `superstore`")
    records = cur.fetchall()
    cur.close()

    return json.dumps({"items":records}, default=str)

@app.route('/item/<int:id>', methods=['GET'])
@cross_origin(origin='*')
def getItem(id):
    # Get Item By ID
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM `superstore` WHERE RowID = %s", (id,))
    record = cur.fetchone()
    cur.close()

    return json.dumps({"item":record}, default=str)

@app.route('/items/state/<state>', methods=['GET'])
@cross_origin(origin='*')
def getByState(state):
    # Get Item By State
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM `superstore` WHERE State = %s", (state,))
    records = cur.fetchall()
    cur.close()

    return json.dumps({"items":records}, default=str)

@app.route('/items/postal/<postal>', methods=['GET'])
@cross_origin(origin='*')
def getByPostalCode(postal):
    # Get Item By Postal Code
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM `superstore` WHERE PostalCode = %s", (postal,))
    records = cur.fetchall()
    cur.close()

    return json.dumps({"items":records}, default=str)

if __name__ == '__main__':
    app.run(debug=True)