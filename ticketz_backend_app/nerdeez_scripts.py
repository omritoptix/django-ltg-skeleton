'''
contains outer app scripts that i can run at my enjoyment

Created on October 15th, 2013
@author: Yariv Katz
@version: 1.0
@copyright: nerdeez.com
'''

#===============================================================================
# begin imports
#===============================================================================

import csv
from nerdeez_server_app.models import *
import re

#===============================================================================
# end imports
#===============================================================================

def from_csv_to_schoolgroup(file_path):
    f = csv.reader(open(file_path, "rU"), dialect=csv.excel_tab)
    for row in f:
        id = int(re.split(';',row[0])[0])
        title = (re.split(';',row[0])[1]).replace('"', '').replace("'", '')
        if len(title) == 5:
            title = '0' + title
        description = (re.split(';',row[0])[2]).replace('"', '').replace("'", '')
        parent = int(re.split(';',row[0])[3])
        school_type = int(re.split(';',row[0])[4])
        school_group = SchoolGroup()
        school_group.title = title
        school_group.description = description
        school_group.id = id
        if parent != None and parent != 0:
            school_group.parent = SchoolGroup.objects.get(id=parent)
        school_group.school_type = school_type
        school_group.save()
        
def from_csv_to_hw_files(file_path):
    f = csv.reader(open(file_path, "rU"), dialect=csv.excel_tab)
    for row in f:
        file_title = (re.split(';',row[0])[0]).replace('"', '').replace("'", '')
        file_path = 'https://s3-eu-west-1.amazonaws.com/' + (re.split(';',row[0])[1]).replace('"', '').replace("'", '')
        file_size = int(re.split(';',row[0])[2])
        schoolgroup_title = (re.split(';',row[0])[3]).replace('"', '').replace("'", '')
        hw_title = (re.split(';',row[0])[4]).replace('"', '').replace("'", '')
        hw, created = Hw.objects.get_or_create(title=hw_title, school_group=SchoolGroup.objects.get(title=schoolgroup_title))
        file = File()
        file.title = file_title
        file.file = file_path
        file.hw = hw
        file.size = file_size
        file.save()
        
        
        
    
    