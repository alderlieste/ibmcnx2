######
#  Check ExId (GUID) by Email through JDBC
#
#  Author:        Christoph Stoettner
#  Mail:          christoph.stoettner@stoeps.de
#  Documentation: http://scripting101.stoeps.de
#
#  Version:       2.0
#  Date:          2014-06-04
#
#  License:       Apache 2.0
#
#  Check ExId of a User in all Connections Applications

# TODO: Script is not functional in the moment, need a function to get the properties of all datasources

import ibmcnx.functions

cell = AdminControl.getCell()
cellname = "/Cell:" + cell + "/"

# Get a list of all databases except DefaultEJBTimerDataSource and OTiSDataSource
dbs = AdminConfig.list('DataSource',AdminConfig.getid(cellname)).splitlines()
dsidlist = []
# remove unwanted databases
for db in dbs:
    dbname = db.split('(')
    n = 0
    for i in dbname:
        # i is only the name of the DataSource, db is DataSource ID!
        if n == 0 and i != "DefaultEJBTimerDataSource" and i != 'OTiSDataSource':
            dsidlist.append(str(db).replace('"',''))
        n += 1

dsidlist.sort()

for dsid in dsidlist:
    print dsid
    #propertySet = AdminConfig.showAttribute(dsid,"propertySet")
    #print propertySet
    #propertyList = AdminConfig.list("J2EEResourceProperty", propertySet).splitlines()
    #print propertyList