# BEGIN IMPORTS
import xml.etree.ElementTree as ET
import pandas as pd
# END IMPORTS

xml_data = ET.parse('export.xml')


milage = []
startDate = []
endDate = []
for tag in xml_data.findall('Record'):
	if tag.attrib['type']=='HKQuantityTypeIdentifierDistanceWalkingRunning':
		milage.append(tag.attrib['value']) 
		startDate.append(tag.attrib['startDate'])
		endDate.append(tag.attrib['endDate']) 

data = pd.DataFrame({'startDate':startDate, 'endDate': endDate, 'milage':milage})
print(data.head())

