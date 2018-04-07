# BEGIN IMPORTS
import xml.etree.ElementTree as ET
import pandas as pd
import luigi
# END IMPORTS



#############
#############
# WORKING
#############
#############

# xml_data = ET.parse('export.xml')

# milage = []
# startDate = []
# endDate = []
# for tag in xml_data.findall('Record'):
# 	if tag.attrib['type']=='HKQuantityTypeIdentifierDistanceWalkingRunning':
# 		milage.append(tag.attrib['value']) 
# 		startDate.append(tag.attrib['startDate'])
# 		endDate.append(tag.attrib['endDate']) 

# data = pd.DataFrame({'startDate':startDate, 'endDate': endDate, 'milage':milage})
# print(data.head())

#############
#############
#############
#############

# TRYING SAME W LUIGI. ALSO WORKS BUT SEEMS hacky having the input in the run function

# run in command line : python to_csv.py XML_to_PD --local-scheduler

# class input_xml_file(luigi.ExternalTask):
# 	'''Simply assign path to local df'''
# 	def output(self):
# 		return luigi.LocalTarget('./export.xml')

class XML_to_PD(luigi.Task):
 
    # def requires(self):
    	# yield input_xml_file()
 
    def output(self):
        return luigi.LocalTarget("health_data.csv")
 
    def run(self):
    	xml_data = ET.parse('./export.xml')
    	milage, startDate, endDate = [], [], []
    	for tag in xml_data.findall('Record'):
    		if tag.attrib['type']=='HKQuantityTypeIdentifierDistanceWalkingRunning':
    			milage.append(tag.attrib['value']) 
    			startDate.append(tag.attrib['startDate'])
    			endDate.append(tag.attrib['endDate']) 
    	df = pd.DataFrame({'startDate':startDate, 'endDate': endDate, 'milage':milage})
    	with self.output().open('w') as out_file: 
    		print (df.to_csv(header=True, index=False), file=out_file) 

if __name__ == '__main__':
    luigi.run()