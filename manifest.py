from parsers import santafe, maine, minneapolis, sf, sf2005, sfnoid, old, prm
from functools import partial
competitions = {
    'Santa Fe Mayor 2018': {
        'path': 'Ballot_Images/Santa_Fe/csvFiles/CvrExport.csv',
        'parser': partial(santafe,0,1)
    },
    'Santa Fe Councilor District 4 2018': {
        'path': 'Ballot_Images/Santa_Fe/csvFiles/CvrExport.csv',
        'parser': partial(santafe,1,5)
    },
    'Santa Fe Councilor District 2 2018': {
        'path': 'Ballot_Images/Santa_Fe/csvFiles/CvrExport.csv',
        'parser': partial(santafe,1,3)
    },
    'Maine Democratic Primary for CD2 2018': {
        'path': 'Ballot_Images/Maine/csvMaine/Maine_Democratic_Primary_for_CD2_CVR.xlsx.csv',
        'parser': partial(maine,5),
        'break_on_repeated_undervotes': True,
        'write_ins': 1
    },
    'Maine Democratic Primary for Governor 2018': {
        'path': 'Ballot_Images/Maine/csvMaine/Maine Democratic Primary for Governor CVR.xlsx.csv',
        'parser': partial(maine,8),
        'break_on_repeated_undervotes': True,
        'write_ins': 1
    },
    'Maine General CD2 CVR Updated 2018': {
        'path': 'Ballot_Images/Maine/csvMaine/Maine General CD2 CVR Updated.xlsx.csv',
        'parser': partial(maine,5),
        'break_on_repeated_undervotes': True,
        'write_ins': 1
    },
    'Minneapolis Mayor 2017': {
        'path': 'Ballot_Images/Minneapolis/2017/csv2017/2017-mayor-cvr.xlsx.csv',
        'parser': minneapolis,
        'break_on_overvote': False
    },
    'Minneapolis BOE 2017': {
        'path': 'Ballot_Images/Minneapolis/2017/csv2017/2017-boe-cvr.xlsx.csv',
        'parser': minneapolis,
        'break_on_overvote': False
    },
    'Minneapolis Park At Large 2017': {
        'path': 'Ballot_Images/Minneapolis/2017/csv2017/2017-park-at-large-cvr.xlsx.csv',
        'parser': minneapolis,
        'break_on_overvote': False
    },
    'Minneapolis Park District 1 2017': {
        'path': 'Ballot_Images/Minneapolis/2017/csv2017/2017-park-district-1-cvr.xlsx.csv',
        'parser': minneapolis,
        'break_on_overvote': False
    },
    'Minneapolis Park District 2 2017': {
        'path': 'Ballot_Images/Minneapolis/2017/csv2017/2017-park-district-2-cvr.xlsx.csv',
        'parser': minneapolis,
        'break_on_overvote': False
    },
    'Minneapolis Park District 3 2017': {
        'path': 'Ballot_Images/Minneapolis/2017/csv2017/2017-park-district-3-cvr.xlsx.csv',
        'parser': minneapolis,
        'break_on_overvote': False
    },
    'Minneapolis Park District 4 2017': {
        'path': 'Ballot_Images/Minneapolis/2017/csv2017/2017-park-district-4-cvr.xlsx.csv',
        'parser': minneapolis,
        'break_on_overvote': False
    },
    'Minneapolis Park District 5 2017': {
        'path': 'Ballot_Images/Minneapolis/2017/csv2017/2017-park-district-5-cvr.xlsx.csv',
        'parser': minneapolis,
        'break_on_overvote': False
    },
    'Minneapolis Park District 6 2017': {
        'path': 'Ballot_Images/Minneapolis/2017/csv2017/2017-park-district-6-cvr.xlsx.csv',
        'parser': minneapolis,
        'break_on_overvote': False
    },
    'Minneapolis Ward 1 2017': {
        'path': 'Ballot_Images/Minneapolis/2017/csv2017/2017-ward-1-cvr.xlsx.csv',
        'parser': minneapolis,
        'break_on_overvote': False
    },
    'Minneapolis Ward 2 2017': {
        'path': 'Ballot_Images/Minneapolis/2017/csv2017/2017-ward-2-cvr.xlsx.csv',
        'parser': minneapolis,
        'break_on_overvote': False
    },
    'Minneapolis Ward 3 2017': {
        'path': 'Ballot_Images/Minneapolis/2017/csv2017/2017-ward-3-cvr.xlsx.csv',
        'parser': minneapolis,
        'break_on_overvote': False
    },
    'Minneapolis Ward 4 2017': {
        'path': 'Ballot_Images/Minneapolis/2017/csv2017/2017-ward-4-cvr.xlsx.csv',
        'parser': minneapolis,
        'break_on_overvote': False
    },
    'Minneapolis Ward 5 2017': {
        'path': 'Ballot_Images/Minneapolis/2017/csv2017/2017-ward-5-cvr.xlsx.csv',
        'parser': minneapolis,
        'break_on_overvote': False
    },
    'Minneapolis Ward 6 2017': {
        'path': 'Ballot_Images/Minneapolis/2017/csv2017/2017-ward-6-cvr.xlsx.csv',
        'parser': minneapolis,
        'break_on_overvote': False
    },
    'Minneapolis Ward 7 2017': {
        'path': 'Ballot_Images/Minneapolis/2017/csv2017/2017-ward-7-cvr.xlsx.csv',
        'parser': minneapolis,
        'break_on_overvote': False
    },
    'Minneapolis Ward 8 2017': {
        'path': 'Ballot_Images/Minneapolis/2017/csv2017/2017-ward-8-cvr.xlsx.csv',
        'parser': minneapolis,
        'break_on_overvote': False
    },
    'Minneapolis Ward 9 2017': {
        'path': 'Ballot_Images/Minneapolis/2017/csv2017/2017-ward-9-cvr.xlsx.csv',
        'parser': minneapolis,
        'break_on_overvote': False
    },
    'Minneapolis Ward 10 2017': {
        'path': 'Ballot_Images/Minneapolis/2017/csv2017/2017-ward-10-cvr.xlsx.csv',
        'parser': minneapolis,
        'break_on_overvote': False
    },
    'Minneapolis Ward 11 2017': {
        'path': 'Ballot_Images/Minneapolis/2017/csv2017/2017-ward-11-cvr.xlsx.csv',
        'parser': minneapolis,
        'break_on_overvote': False
    },
    'Minneapolis Ward 12 2017': {
        'path': 'Ballot_Images/Minneapolis/2017/csv2017/2017-ward-12-cvr.xlsx.csv',
        'parser': minneapolis,
        'break_on_overvote': False
    },
    'Minneapolis Ward 13 2017': {
        'path': 'Ballot_Images/Minneapolis/2017/csv2017/2017-ward-13-cvr.xlsx.csv',
        'parser': minneapolis,
        'break_on_overvote': False
    },
    'Minneapolis Mayor 2013': {
        'path': 'Ballot_Images/Minneapolis/2013_only those contested/csv2013/Minneapolis 2013-mayor-cvr.xlsx.csv',
        'parser': minneapolis,
        'break_on_overvote': False,
    },
    'Minneapolis BOE 2013': {
        'path': 'Ballot_Images/Minneapolis/2013_only those contested/csv2013/Minneapolis 2013-board of estimation and taxation cvr.xlsx.csv',
        'parser': minneapolis,
        'break_on_overvote': False,
    },
    'Minneapolis Park At Large 2013': {
        'path': 'Ballot_Images/Minneapolis/2013_only those contested/csv2013/Minneapolis 2013-park-at-large-cvr.xlsx.csv',
        'parser': minneapolis,
        'break_on_overvote': False,
        'number': 3,
    },
    'Minneapolis Park District 2 2013': {
        'path': 'Ballot_Images/Minneapolis/2013_only those contested/csv2013/Minneapolis 2013-park-district-2-cvr.xlsx.csv',
        'parser': minneapolis,
        'break_on_overvote': False,
    },
    'Minneapolis Park District 6 2013': {
        'path': 'Ballot_Images/Minneapolis/2013_only those contested/csv2013/Minneapolis 2013-park-district-6-cvr.xlsx.csv',
        'parser': minneapolis,
        'break_on_overvote': False,
    },
    'Minneapolis Ward 5 2013': {
        'path': 'Ballot_Images/Minneapolis/2013_only those contested/csv2013/Minneapolis 2013 Council - ward-5-cvr.xlsx.csv',
        'parser': minneapolis,
        'break_on_overvote': False,
    },
    'Minneapolis Ward 9 2013': {
        'path': 'Ballot_Images/Minneapolis/2013_only those contested/csv2013/Minneapolis 2013 Council - ward-9-cvr.xlsx.csv',
        'parser': minneapolis,
        'break_on_overvote': False,
    },
    'Minneapolis Ward 13 2013': {
        'path': 'Ballot_Images/Minneapolis/2013_only those contested/csv2013/Minneapolis 2013 Council - ward-13-cvr.xlsx.csv',
        'parser': minneapolis,
        'break_on_overvote': False,
    },
    'Minneapolis Mayor 2009': {
        'path': 'Ballot_Images/Minneapolis/2009/csv2009/Minneapolis 2009 Mayor.xls.csv',
        'parser': minneapolis,
        'break_on_overvote': False
    },
    'Minneapolis BOE 2009': {
        'path': 'Ballot_Images/Minneapolis/2009/csv2009/Minneapolis 2009 Board of Estimate and Taxation – At-Large – elect 2.xls.csv',
        'parser': minneapolis,
        'break_on_overvote': False
    },
    'Minneapolis Park At Large 2009': {
        'path': 'Ballot_Images/Minneapolis/2009/csv2009/Minneapolis 2009 Park and Recreation Board – At-Large – elect 3.xls.csv',
        'parser': minneapolis,
        'break_on_overvote': False
    },
    'Minneapolis Park District 1 2009': {
        'path': 'Ballot_Images/Minneapolis/2009/csv2009/Minneapolis Park and Recreation Board District 1.xls.csv',
        'parser': minneapolis,
        'break_on_overvote': False
    },
    'Minneapolis Park District 2 2009': {
        'path': 'Ballot_Images/Minneapolis/2009/csv2009/Minneapolis Park and Recreation Board District 2.xls.csv',
        'parser': minneapolis,
        'break_on_overvote': False
    },
    'Minneapolis Park District 3 2009': {
        'path': 'Ballot_Images/Minneapolis/2009/csv2009/Minneapolis Park and Recreation Board District 3.xls.csv',
        'parser': minneapolis,
        'break_on_overvote': False
    },
    'Minneapolis Park District 4 2009': {
        'path': 'Ballot_Images/Minneapolis/2009/csv2009/Minneapolis Park and Recreation Board District 4.xls.csv',
        'parser': minneapolis,
        'break_on_overvote': False
    },
    'Minneapolis Park District 5 2009': {
        'path': 'Ballot_Images/Minneapolis/2009/csv2009/Minneapolis Park and Recreation Board District 5.xls.csv',
        'parser': minneapolis,
        'break_on_overvote': False
    },
    'Minneapolis Park District 6 2009': {
        'path': 'Ballot_Images/Minneapolis/2009/csv2009/Minneapolis Park and Recreation Board District 6.xls.csv',
        'parser': minneapolis,
        'break_on_overvote': False
    },
    'Minneapolis Ward 1 2009': {
        'path': 'Ballot_Images/Minneapolis/2009/csv2009/Minneapolis 2009 Council Member Ward 1.xls.csv',
        'parser': minneapolis,
        'break_on_overvote': False
    },
    'Minneapolis Ward 2 2009': {
        'path': 'Ballot_Images/Minneapolis/2009/csv2009/Minneapolis 2009 Council Member Ward 2.xls.csv',
        'parser': minneapolis,
        'break_on_overvote': False
    },
    'Minneapolis Ward 3 2009': {
        'path': 'Ballot_Images/Minneapolis/2009/csv2009/Minneapolis 2009 Council Member Ward 3.xls.csv',
        'parser': minneapolis,
        'break_on_overvote': False
    },
    'Minneapolis Ward 4 2009': {
        'path': 'Ballot_Images/Minneapolis/2009/csv2009/Minneapolis 2009 Council Member Ward 4.xls.csv',
        'parser': minneapolis,
        'break_on_overvote': False
    },
    'Minneapolis Ward 5 2009': {
        'path': 'Ballot_Images/Minneapolis/2009/csv2009/Minneapolis 2009 Council Member Ward 5.xls.csv',
        'parser': minneapolis,
        'break_on_overvote': False
    },
    'Minneapolis Ward 6 2009': {
        'path': 'Ballot_Images/Minneapolis/2009/csv2009/Minneapolis 2009 Council Member Ward 6.xls.csv',
        'parser': minneapolis,
        'break_on_overvote': False
    },
    'Minneapolis Ward 7 2009': {
        'path': 'Ballot_Images/Minneapolis/2009/csv2009/Minneapolis 2009 Council Member Ward 7.xls.csv',
        'parser': minneapolis,
        'break_on_overvote': False
    },
    'Minneapolis Ward 8 2009': {
        'path': 'Ballot_Images/Minneapolis/2009/csv2009/Minneapolis 2009 Council Member Ward 8.xls.csv',
        'parser': minneapolis,
        'break_on_overvote': False
    },
    'Minneapolis Ward 9 2009': {
        'path': 'Ballot_Images/Minneapolis/2009/csv2009/Minneapolis 2009 Council Member Ward 9.xls.csv',
        'parser': minneapolis,
        'break_on_overvote': False
    },
    'Minneapolis Ward 10 2009': {
        'path': 'Ballot_Images/Minneapolis/2009/csv2009/Minneapolis 2009 Council Member Ward 10.xls.csv',
        'parser': minneapolis,
        'break_on_overvote': False
    },
    'Minneapolis Ward 11 2009': {
        'path': 'Ballot_Images/Minneapolis/2009/csv2009/Minneapolis 2009 Council Member Ward 11.xls.csv',
        'parser': minneapolis,
        'break_on_overvote': False
    },
    'Minneapolis Ward 12 2009': {
        'path': 'Ballot_Images/Minneapolis/2009/csv2009/Minneapolis 2009 Council Member Ward 12.xls.csv',
        'parser': minneapolis,
        'break_on_overvote': False
    },
    'Minneapolis Ward 13 2009': {
        'path': 'Ballot_Images/Minneapolis/2009/csv2009/Minneapolis 2009 Council Member Ward 13.xls.csv',
        'parser': minneapolis,
        'break_on_overvote': False
    },
    'San Francisco Mayor 2015': {
    # do not compare with https://sfelections.org/results/20151103/
    # compare with https://sfelections.org/results/20151103/data/20151119/mayor/20151119_mayor.html
        'path': 'Ballot_Images/San Francisco/2015 All offices/20151119_ballotimage.txt',
        'parser': partial(sf,'0000001'),
        'break_on_overvote': True,
        'break_on_repeated undervotes': False
    }, 
    'San Francisco Sheriff 2015': {
    # see note under 'San Francisco Mayor 2015'
        'path': 'Ballot_Images/San Francisco/2015 All offices/20151119_ballotimage.txt',
        'parser': partial(sf,'0000002'),
        'break_on_overvote': True,
        'break_on_repeated undervotes': False
    }, 
    'San Francisco Board of Supervisors, District 3 2015': {
    # see note under 'San Francisco Mayor 2015'
        'path': 'Ballot_Images/San Francisco/2015 All offices/20151119_ballotimage.txt',
        'parser': partial(sf,'0000003'),
        'break_on_overvote': True,
        'break_on_repeated undervotes': False
    },
    'San Francisco Assessor-Recorder 2018': {
        'path': 'Ballot_Images/San Francisco/San Fran_Nov 2018/20181127_assessor_ballotimage.txt',
        'parser': sfnoid,
        'break_on_overvote': True,
        'break_on_repeated undervotes': False
    },
    'San Francisco Public Defender 2018': {
        'path': 'Ballot_Images/San Francisco/San Fran_Nov 2018/20181127_defender_ballotimage.txt',
        'parser': sfnoid,
        'break_on_overvote': True,
        'break_on_repeated undervotes': False
    },
    'San Francisco Board of Supervisors, District 2 2018': {
        'path': 'Ballot_Images/San Francisco/San Fran_Nov 2018/20181127_d2_ballotimage.txt',
        'parser': sfnoid,
        'break_on_overvote': True,
        'break_on_repeated undervotes': False
    },
    'San Francisco Board of Supervisors, District 4 2018': {
        'path': 'Ballot_Images/San Francisco/San Fran_Nov 2018/20181127_d4_ballotimage.txt',
        'parser': sfnoid,
        'break_on_overvote': True,
        'break_on_repeated undervotes': False
    },
    'San Francisco Board of Supervisors, District 6 2018': {
        'path': 'Ballot_Images/San Francisco/San Fran_Nov 2018/20181127_d6_ballotimage.txt',
        'parser': sfnoid,
        'break_on_overvote': True,
        'break_on_repeated undervotes': False
    },
    'San Francisco Board of Supervisors, District 8 2018': {
        'path': 'Ballot_Images/San Francisco/San Fran_Nov 2018/20181127_d8_ballotimage.txt',
        'parser': sfnoid,
        'break_on_overvote': True,
        'break_on_repeated undervotes': False
    },
    'San Francisco Board of Supervisors, District 10 2018': {
        'path': 'Ballot_Images/San Francisco/San Fran_Nov 2018/20181127_d10_ballotimage.txt',
        'parser': sfnoid,
        'break_on_overvote': True,
        'break_on_repeated undervotes': False
    },
   'San Francisco Board of Supervisors, District 1 2016': {
        'path': 'Ballot_Images/San Francisco/San Fran_Nov 2016/20161206_ballotimage.txt',
        'parser': partial(sf,'0000009'),
        'break_on_overvote': True,
        'break_on_repeated undervotes': False
    },
   'San Francisco Board of Supervisors, District 3 2016': {
        'path': 'Ballot_Images/San Francisco/San Fran_Nov 2016/20161206_ballotimage.txt',
        'parser': partial(sf,'0000010'),
        'break_on_overvote': True,
        'break_on_repeated undervotes': False
    },
   'San Francisco Board of Supervisors, District 5 2016': {
        'path': 'Ballot_Images/San Francisco/San Fran_Nov 2016/20161206_ballotimage.txt',
        'parser': partial(sf,'0000011'),
        'break_on_overvote': True,
        'break_on_repeated undervotes': False
    },
   'San Francisco Board of Supervisors, District 7 2016': {
        'path': 'Ballot_Images/San Francisco/San Fran_Nov 2016/20161206_ballotimage.txt',
        'parser': partial(sf,'0000012'),
        'break_on_overvote': True,
        'break_on_repeated undervotes': False
    },
   'San Francisco Board of Supervisors, District 9 2016': {
        'path': 'Ballot_Images/San Francisco/San Fran_Nov 2016/20161206_ballotimage.txt',
        'parser': partial(sf,'0000013'),
        'break_on_overvote': True,
        'break_on_repeated undervotes': False
    },
   'San Francisco Board of Supervisors, District 11 2016': {
        'path': 'Ballot_Images/San Francisco/San Fran_Nov 2016/20161206_ballotimage.txt',
        'parser': partial(sf,'0000014'),
        'break_on_overvote': True,
        'break_on_repeated undervotes': False
    },
   'San Francisco Board of Supervisors, District 10 2014': {
        'path': 'Ballot_Images/San Francisco/San Fran_Nov 2014_District 10 Supervisors/D10_BallotImage.txt',
        'parser': sfnoid,
        'break_on_overvote': True,
        'break_on_repeated undervotes': False
    },
   'San Francisco Board of Supervisors, District 7 2012': {
        'path': 'Ballot_Images/San Francisco/San Fran_Nov 2012_District 7 Supervisors/D7-BallotImage.txt',
        'parser': sfnoid,
        'break_on_overvote': True,
        'break_on_repeated undervotes': False
    },
   'San Francisco Board of Supervisors, District 5 2012': {
        'path': 'Ballot_Images/San Francisco/San Fran_Nov 2012_District 5 Supervisors/D5-BallotImage.txt',
        'parser': sfnoid,
        'break_on_overvote': True,
        'break_on_repeated undervotes': False
    },
   'San Francisco Board of Supervisors, District 10 2010': {
        'path': 'Ballot_Images/San Francisco/San Fran_Nov 2010_District 10 Supervisors/BallotImage-D10.txt',
        'parser': sfnoid,
        'break_on_overvote': True,
        'break_on_repeated undervotes': False
    },
   'San Francisco Board of Supervisors, District 8 2010': {
        'path': 'Ballot_Images/San Francisco/San Fran_Nov 2010_District 8 Supervisors/BallotImage-D8.txt',
        'parser': sfnoid,
        'break_on_overvote': True,
        'break_on_repeated undervotes': False
    },
   'San Francisco Board of Supervisors, District 6 2010': {
        'path': 'Ballot_Images/San Francisco/San Fran_Nov 2010_District 6 Supervisors/BallotImage-D6.txt',
        'parser': sfnoid,
        'break_on_overvote': True,
        'break_on_repeated undervotes': False
    },
   'San Francisco Board of Supervisors, District 2 2010': {
        'path': 'Ballot_Images/San Francisco/San Fran_Nov 2010_District 2 Supervisors/BallotImage-D2.txt',
        'parser': sfnoid,
        'break_on_overvote': True,
        'break_on_repeated undervotes': False
    },
   'San Francisco Board of Supervisors, District 1 2008': {
        'path': 'Ballot_Images/San Francisco/San Fran_Nov 2008_All District races/CityWide_Ballot_Image.txt',
        'parser': partial(sf,'0000003'),
        'break_on_overvote': True,
        'break_on_repeated undervotes': False
    },
   'San Francisco Board of Supervisors, District 3 2008': {
        'path': 'Ballot_Images/San Francisco/San Fran_Nov 2008_All District races/CityWide_Ballot_Image.txt',
        'parser': partial(sf,'0000005'),
        'break_on_overvote': True,
        'break_on_repeated undervotes': False
    },
   'San Francisco Board of Supervisors, District 4 2008': {
        'path': 'Ballot_Images/San Francisco/San Fran_Nov 2008_All District races/CityWide_Ballot_Image.txt',
        'parser': partial(sf,'0000006'),
        'break_on_overvote': True,
        'break_on_repeated undervotes': False
    },
   'San Francisco Board of Supervisors, District 5 2008': {
        'path': 'Ballot_Images/San Francisco/San Fran_Nov 2008_All District races/CityWide_Ballot_Image.txt',
        'parser': partial(sf,'0000007'),
        'break_on_overvote': True,
        'break_on_repeated undervotes': False
    },
   'San Francisco Board of Supervisors, District 7 2008': {
        'path': 'Ballot_Images/San Francisco/San Fran_Nov 2008_All District races/CityWide_Ballot_Image.txt',
        'parser': partial(sf,'0000008'),
        'break_on_overvote': True,
        'break_on_repeated undervotes': False
    },
   'San Francisco Board of Supervisors, District 9 2008': {
        'path': 'Ballot_Images/San Francisco/San Fran_Nov 2008_All District races/CityWide_Ballot_Image.txt',
        'parser': partial(sf,'0000009'),
        'break_on_overvote': True,
        'break_on_repeated undervotes': False
    },
   'San Francisco Board of Supervisors, District 11 2008': {
        'path': 'Ballot_Images/San Francisco/San Fran_Nov 2008_All District races/CityWide_Ballot_Image.txt',
        'parser': partial(sf,'0000004'),
        'break_on_overvote': True,
        'break_on_repeated undervotes': False
    },
   'San Francisco Sheriff 2011': {
        'path': 'Ballot_Images/San Francisco/San Fran Nov 2011 Sheriff/Sheriff-BallotImage.txt',
        'parser': sfnoid,
        'break_on_overvote': True,
        'break_on_repeated undervotes': False
    },
   'San Francisco Mayor 2011': {
        'path': 'Ballot_Images/San Francisco/San Fran Nov 2011 Mayor/Mayor-BallotImage.txt',
        'parser': sfnoid,
        'break_on_overvote': True,
        'break_on_repeated undervotes': False
    },
   'San Francisco District Attorney 2011': {
        'path': 'Ballot_Images/San Francisco/San Fran Nov 2011 District Attorney/DA-BallotImage.txt',
        'parser': sfnoid,
        'break_on_overvote': True,
        'break_on_repeated undervotes': False
    },
   'San Francisco Mayor 2007': {
        'path': 'Ballot_Images/San Francisco/San Fran Nov 2007 Mayor/BallotImage_San Fran_Mayor_Nov 2007.txt',
        'parser': partial(sf2005, ['0100','0101','0102'],'19','20',None),
        'break_on_overvote': True,
        'break_on_repeated undervotes': False
    },
   'San Francisco District 1 2004': {
        #https://sfelections.sfgov.org/rcv-district-1-nov-2004
        'path': 'Ballot_Images/San Francisco/San Fran Nov 2004 All Supervisors/Nov2004_BallotImage.txt',
        'parser': partial(sf2005, ['1015','1016','1017'],'09','10',','),
        'break_on_overvote': True,
        'break_on_repeated undervotes': False
    },
   'San Francisco District 2 2004': {
        #values infered from ballot data, not documented here https://sfelections.sfgov.org/results-summary-nov-2004
        'path': 'Ballot_Images/San Francisco/San Fran Nov 2004 All Supervisors/Nov2004_BallotImage.txt',
        'parser': partial(sf2005, ['1020','1021','1022'],'07','08',','),
        'break_on_overvote': True,
        'break_on_repeated undervotes': False
    },
   'San Francisco District 3 2004': {
        #values infered from ballot data, not documented here https://sfelections.sfgov.org/results-summary-nov-2004
        'path': 'Ballot_Images/San Francisco/San Fran Nov 2004 All Supervisors/Nov2004_BallotImage.txt',
        'parser': partial(sf2005, ['1025','1026','1027'],'06','07',','),
        'break_on_overvote': True,
        'break_on_repeated undervotes': False
    },
   'San Francisco District 5 2004': {
        'path': 'Ballot_Images/San Francisco/San Fran Nov 2004 All Supervisors/Nov2004_BallotImage.txt',
        'parser': partial(sf2005, ['1030','1031','1032'],'24','25',','),
        'break_on_overvote': True,
        'break_on_repeated undervotes': False
    },
   'San Francisco District 7 2004': {
        'path': 'Ballot_Images/San Francisco/San Fran Nov 2004 All Supervisors/Nov2004_BallotImage.txt',
        'parser': partial(sf2005, ['1035','1036','1037'],'15','16',','),
        'break_on_overvote': True,
        'break_on_repeated undervotes': False
    },
   'San Francisco District 9 2004': {
        'path': 'Ballot_Images/San Francisco/San Fran Nov 2004 All Supervisors/Nov2004_BallotImage.txt',
        'parser': partial(sf2005, ['1040','1041','1042'],'08','09',','),
        'break_on_overvote': True,
        'break_on_repeated undervotes': False
    },
   'San Francisco District 11 2004': {
        'path': 'Ballot_Images/San Francisco/San Fran Nov 2004 All Supervisors/Nov2004_BallotImage.txt',
        'parser': partial(sf2005, ['1045','1046','1047'],'10','11',','),
        'break_on_overvote': True,
        'break_on_repeated undervotes': False
    },
   'San Francisco Mayor June 2018': {
        #https://sfelections.org/results/20180605/data/20180627/mayor/20180627_mayor.html
        'path': 'Ballot_Images/San Francisco/San Fran June 2018/20180621_ballotimage.txt',
        'parser': partial(sf,'0000020'),
        'break_on_overvote': True,
        'break_on_repeated undervotes': False
    },
   'San Francisco Board of Supervisors, District 8 June 2018': {
        'path': 'Ballot_Images/San Francisco/San Fran June 2018/20180621_ballotimage.txt',
        'parser': partial(sf,'0000021'),
        'break_on_overvote': True,
        'break_on_repeated undervotes': False
    },
   'San Francisco Mayor 2007': {
        'path': 'Ballot_Images/San Francisco/RCVCalc Ballot Images/2007/MYR-Ballots.txt',
        'parser': old,
        'break_on_overvote': True,
        'break_on_repeated undervotes': False
    },
   'San Francisco Board of Supervisors, District 2 2006': {
        'path': 'Ballot_Images/San Francisco/RCVCalc Ballot Images/2006/D02-Ballots.txt',
        'parser': old,
        'break_on_overvote': True,
        'break_on_repeated undervotes': False
    },
   'San Francisco Board of Supervisors, District 4 2006': {
        'path': 'Ballot_Images/San Francisco/RCVCalc Ballot Images/2006/D04-Ballots.txt',
        'parser': old,
        'break_on_overvote': True,
        'break_on_repeated undervotes': False
    },
   'San Francisco Board of Supervisors, District 6 2006': {
        'path': 'Ballot_Images/San Francisco/RCVCalc Ballot Images/2006/D06-Ballots.txt',
        'parser': old,
        'break_on_overvote': True,
        'break_on_repeated undervotes': False
    },
   'San Francisco Board of Supervisors, District 8 2006': {
        'path': 'Ballot_Images/San Francisco/RCVCalc Ballot Images/2006/D08-Ballots.txt',
        'parser': old,
        'break_on_overvote': True,
        'break_on_repeated undervotes': False
    },
   'San Francisco Board of Supervisors, District 10 2006': {
        'path': 'Ballot_Images/San Francisco/RCVCalc Ballot Images/2006/D10-Ballots.txt',
        'parser': old,
        'break_on_overvote': True,
        'break_on_repeated undervotes': False
    },
   'San Francisco Treasurer 2005': {
        'path': 'Ballot_Images/San Francisco/RCVCalc Ballot Images/2005/TR-Ballots.txt',
        'parser': old,
        'break_on_overvote': True,
        'break_on_repeated undervotes': False
    },
   'San Francisco Assessor-Recorder 2005': {
        'path': 'Ballot_Images/San Francisco/RCVCalc Ballot Images/2005/AR-Ballots.txt',
        'parser': old,
        'break_on_overvote': True,
        'break_on_repeated undervotes': False
    },
   'Pierce County Executive 2008': {
        'path': 'Ballot_Images/Pierce County/Pierce County Executive 2008 Ballot Image Data.txt',
        'parser': sfnoid,
        'break_on_overvote': True,
        'break_on_repeated undervotes': False
    },
   'Pierce County Council, District 2 2008': {
        'path': 'Ballot_Images/Pierce County/Pierce County Council, District No. 2 2008 Ballot Image.txt',
        'parser': sfnoid,
        'break_on_overvote': True,
        'break_on_repeated undervotes': False
    },
   'Pierce County Auditor 2009': {
        'path': 'Ballot_Images/Pierce County/Pierce County Auditor 2009 Ballot Image.txt',
        'parser': sfnoid,
        'break_on_overvote': True,
        'break_on_repeated undervotes': False
    },
   'Pierce County Assessor - Treasurer 2008': {
        'path': 'Ballot_Images/Pierce County/Pierce County Assessor - Treasurer 2008 Ballot Image.txt',
        'parser': sfnoid,
        'break_on_overvote': True,
        'break_on_repeated undervotes': False
    },
    '2012 City Attorney - Oakland Nov 2012': {
         'path': 'Ballot_Images/Alameda (Oakland, San Leandro, Berkeley)/Alameda (Oakland, San Leandro, Berkeley) 2012/ballot_image_City Attorney - Oakland_Nov 2012.txt',
         'parser': sfnoid,
         'break_on_overvote': True,
         'break_on_repeated undervotes': False
     },
    '2012 Member, City Council, District 3 - Berkeley Nov 2012': {
         'path': 'Ballot_Images/Alameda (Oakland, San Leandro, Berkeley)/Alameda (Oakland, San Leandro, Berkeley) 2012/ballot_image_Member, City Council, District 3 - Berkeley_Nov 2012.txt',
         'parser': sfnoid,
         'break_on_overvote': True,
         'break_on_repeated undervotes': False
     },
    '2012 Member, City Council, District 7- Oakland Nov 2012': {
         'path': 'Ballot_Images/Alameda (Oakland, San Leandro, Berkeley)/Alameda (Oakland, San Leandro, Berkeley) 2012/ballot_image_Member, City Council, District 7- Oakland_Nov 2012.txt',
         'parser': sfnoid,
         'break_on_overvote': True,
         'break_on_repeated undervotes': False
     },
    '2012 Member, City Council, District 5- Oakland Nov 2012': {
         'path': 'Ballot_Images/Alameda (Oakland, San Leandro, Berkeley)/Alameda (Oakland, San Leandro, Berkeley) 2012/ballot_image_Member, City Council, District 5- Oakland_Nov 2012.txt',
         'parser': sfnoid,
         'break_on_overvote': True,
         'break_on_repeated undervotes': False
     },
    '2012 Member, City Council, District 6 - San Leandro Nov 2012': {
         'path': 'Ballot_Images/Alameda (Oakland, San Leandro, Berkeley)/Alameda (Oakland, San Leandro, Berkeley) 2012/ballot_image_Member, City Council, District 6 - San Leandro_Nov 2012.txt',
         'parser': sfnoid,
         'break_on_overvote': True,
         'break_on_repeated undervotes': False
     },
    '2012 Member, City Council, At-Large - Oakland Nov 2012': {
         'path': 'Ballot_Images/Alameda (Oakland, San Leandro, Berkeley)/Alameda (Oakland, San Leandro, Berkeley) 2012/ballot_image_Member, City Council, At-Large - Oakland_Nov 2012.txt',
         'parser': sfnoid,
         'break_on_overvote': True,
         'break_on_repeated undervotes': False
     },
    '2012 Member, City Council, District 1- Oakland Nov 2012': {
         'path': 'Ballot_Images/Alameda (Oakland, San Leandro, Berkeley)/Alameda (Oakland, San Leandro, Berkeley) 2012/ballot_image_Member, City Council, District 1- Oakland_Nov 2012.txt',
         'parser': sfnoid,
         'break_on_overvote': True,
         'break_on_repeated undervotes': False
     },
    '2012 Member, City Council,District 3 - Oakland Nov 2012': {
         'path': 'Ballot_Images/Alameda (Oakland, San Leandro, Berkeley)/Alameda (Oakland, San Leandro, Berkeley) 2012/ballot_image_Member, City Council,District 3 - Oakland_Nov 2012.txt',
         'parser': sfnoid,
         'break_on_overvote': True,
         'break_on_repeated undervotes': False
     },
    '2012 School Director, District 3 - Oakland Nov 2012': {
         'path': 'Ballot_Images/Alameda (Oakland, San Leandro, Berkeley)/Alameda (Oakland, San Leandro, Berkeley) 2012/ballot_image_School Director, District 3 - Oakland_Nov 2012.txt',
         'parser': sfnoid,
         'break_on_overvote': True,
         'break_on_repeated undervotes': False
     },
    '2012 Member, City Council, District 6 - Berkeley Nov 2012': {
         'path': 'Ballot_Images/Alameda (Oakland, San Leandro, Berkeley)/Alameda (Oakland, San Leandro, Berkeley) 2012/ballot_image_Member, City Council, District 6 - Berkeley_Nov 2012.txt',
         'parser': sfnoid,
         'break_on_overvote': True,
         'break_on_repeated undervotes': False
     },
    '2012 Member, City Council, District 2 - Berkeley Nov 2012': {
         'path': 'Ballot_Images/Alameda (Oakland, San Leandro, Berkeley)/Alameda (Oakland, San Leandro, Berkeley) 2012/ballot_image_Member, City Council, District 2 - Berkeley_Nov 2012.txt',
         'parser': sfnoid,
         'break_on_overvote': True,
         'break_on_repeated undervotes': False
     },
    '2012 Member, City Council, District 2 - San Leandro Nov 2012': {
         'path': 'Ballot_Images/Alameda (Oakland, San Leandro, Berkeley)/Alameda (Oakland, San Leandro, Berkeley) 2012/ballot_image_Member, City Council, District 2 - San Leandro_Nov 2012.txt',
         'parser': sfnoid,
         'break_on_overvote': True,
         'break_on_repeated undervotes': False
     },
    '2012 School Director, District 7 - Oakland Nov 2012': {
         'path': 'Ballot_Images/Alameda (Oakland, San Leandro, Berkeley)/Alameda (Oakland, San Leandro, Berkeley) 2012/ballot_image_School Director, District 7 - Oakland_Nov 2012.txt',
         'parser': sfnoid,
         'break_on_overvote': True,
         'break_on_repeated undervotes': False
     },
    '2012 Mayor - Berkeley Nov 2012': {
         'path': 'Ballot_Images/Alameda (Oakland, San Leandro, Berkeley)/Alameda (Oakland, San Leandro, Berkeley) 2012/ballot_image_Mayor - Berkeley_Nov 2012.txt',
         'parser': sfnoid,
         'break_on_overvote': True,
         'break_on_repeated undervotes': False
     },
    '2012 School Director, District 1 - Oakland Nov 2012': {
         'path': 'Ballot_Images/Alameda (Oakland, San Leandro, Berkeley)/Alameda (Oakland, San Leandro, Berkeley) 2012/ballot_image_School Director, District 1 - Oakland_Nov 2012.txt',
         'parser': sfnoid,
         'break_on_overvote': True,
         'break_on_repeated undervotes': False
     },
    '2012 School Director, District 5 - Oakland Nov 2012': {
         'path': 'Ballot_Images/Alameda (Oakland, San Leandro, Berkeley)/Alameda (Oakland, San Leandro, Berkeley) 2012/ballot_image_School Director, District 5 - Oakland_Nov 2012.txt',
         'parser': sfnoid,
         'break_on_overvote': True,
         'break_on_repeated undervotes': False
     },
    '2012 Member, City Council, District 4 - San Leandro Nov 2012': {
         'path': 'Ballot_Images/Alameda (Oakland, San Leandro, Berkeley)/Alameda (Oakland, San Leandro, Berkeley) 2012/ballot_image_Member, City Council, District 4 - San Leandro_Nov 2012.txt',
         'parser': sfnoid,
         'break_on_overvote': True,
         'break_on_repeated undervotes': False
     },
    '2012 Member, City Council, District 5 - Berkeley Nov 2012': {
         'path': 'Ballot_Images/Alameda (Oakland, San Leandro, Berkeley)/Alameda (Oakland, San Leandro, Berkeley) 2012/ballot_image_Member, City Council, District 5 - Berkeley_Nov 2012.txt',
         'parser': sfnoid,
         'break_on_overvote': True,
         'break_on_repeated undervotes': False
     },
    '2014 Member, City Council, District 6 - Oakland Nov 2014': {
         'path': 'Ballot_Images/Alameda (Oakland, San Leandro, Berkeley)/Alameda (Oakland, San Leandro, Berkeley) 2014/ballot_image_Member, City Council, District 6 - Oakland_Nov 2014.txt',
         'parser': sfnoid,
         'break_on_overvote': True,
         'break_on_repeated undervotes': False
     },
    '2014 Member, City Council, District 7 - Berkeley Nov 2014': {
         'path': 'Ballot_Images/Alameda (Oakland, San Leandro, Berkeley)/Alameda (Oakland, San Leandro, Berkeley) 2014/ballot_image_Member, City Council, District 7 - Berkeley_Nov 2014.txt',
         'parser': sfnoid,
         'break_on_overvote': True,
         'break_on_repeated undervotes': False
     },
    '2014 Member, City Council, District 8 - Berkeley Nov 2014': {
         'path': 'Ballot_Images/Alameda (Oakland, San Leandro, Berkeley)/Alameda (Oakland, San Leandro, Berkeley) 2014/ballot_image_Member, City Council, District 8 - Berkeley_Nov 2014.txt',
         'parser': sfnoid,
         'break_on_overvote': True,
         'break_on_repeated undervotes': False
     },
    '2014 Member, City Council, District 1 - San Leandro Nov 2014': {
         'path': 'Ballot_Images/Alameda (Oakland, San Leandro, Berkeley)/Alameda (Oakland, San Leandro, Berkeley) 2014/ballot_image_Member, City Council, District 1 - San Leandro_Nov 2014.txt',
         'parser': sfnoid,
         'break_on_overvote': True,
         'break_on_repeated undervotes': False
     },
    '2014 Member, City Council, District 2 - Oakland Nov 2014': {
         'path': 'Ballot_Images/Alameda (Oakland, San Leandro, Berkeley)/Alameda (Oakland, San Leandro, Berkeley) 2014/ballot_image_Member, City Council, District 2 - Oakland_Nov 2014.txt',
         'parser': sfnoid,
         'break_on_overvote': True,
         'break_on_repeated undervotes': False
     },
    '2014 City Auditor - Oakland Nov 2014': {
         'path': 'Ballot_Images/Alameda (Oakland, San Leandro, Berkeley)/Alameda (Oakland, San Leandro, Berkeley) 2014/ballot_image_ City Auditor - Oakland_Nov 2014.txt',
         'parser': sfnoid,
         'break_on_overvote': True,
         'break_on_repeated undervotes': False
     },
    '2014 Member, City Council, District 4 - Oakland Nov 2014': {
         'path': 'Ballot_Images/Alameda (Oakland, San Leandro, Berkeley)/Alameda (Oakland, San Leandro, Berkeley) 2014/ballot_image_Member, City Council, District 4 - Oakland_Nov 2014.txt',
         'parser': sfnoid,
         'break_on_overvote': True,
         'break_on_repeated undervotes': False
     },
    '2014 Mayor of San Leandro Nov 2014': {
         'path': 'Ballot_Images/Alameda (Oakland, San Leandro, Berkeley)/Alameda (Oakland, San Leandro, Berkeley) 2014/ballot_image_ Mayor of San Leandro_Nov 2014.txt',
         'parser': sfnoid,
         'break_on_overvote': True,
         'break_on_repeated undervotes': False
     },
    '2014 Mayor - Oakland Nov 2014': {
         'path': 'Ballot_Images/Alameda (Oakland, San Leandro, Berkeley)/Alameda (Oakland, San Leandro, Berkeley) 2014/ballot_image_ Mayor - Oakland_Nov 2014.txt',
         'parser': sfnoid,
         'break_on_overvote': True,
         'break_on_repeated undervotes': False
     },
    '2014 City Auditor - Berkeley Nov 2014': {
         'path': 'Ballot_Images/Alameda (Oakland, San Leandro, Berkeley)/Alameda (Oakland, San Leandro, Berkeley) 2014/ballot_image_City Auditor - Berkeley_Nov 2014.txt',
         'parser': sfnoid,
         'break_on_overvote': True,
         'break_on_repeated undervotes': False
     },
    '2014 Member, City Council, District 5 - San Leandro Nov 2014': {
         'path': 'Ballot_Images/Alameda (Oakland, San Leandro, Berkeley)/Alameda (Oakland, San Leandro, Berkeley) 2014/ballot_image_Member, City Council, District 5 - San Leandro_Nov 2014.txt',
         'parser': sfnoid,
         'break_on_overvote': True,
         'break_on_repeated undervotes': False
     },
    '2014 School Director, District 4 - Oakland Nov 2014': {
         'path': 'Ballot_Images/Alameda (Oakland, San Leandro, Berkeley)/Alameda (Oakland, San Leandro, Berkeley) 2014/ballot_image_School Director, District 4 - Oakland_Nov 2014.txt',
         'parser': sfnoid,
         'break_on_overvote': True,
         'break_on_repeated undervotes': False
     },
    '2014 Member, City Council, District 1 - Berkeley Nov 2014': {
         'path': 'Ballot_Images/Alameda (Oakland, San Leandro, Berkeley)/Alameda (Oakland, San Leandro, Berkeley) 2014/ballot_image_Member, City Council, District 1 - Berkeley_Nov_2014.txt',
         'parser': sfnoid,
         'break_on_overvote': True,
         'break_on_repeated undervotes': False
     },
    '2014 School Director, District 2 - Oakland Nov 2014': {
         'path': 'Ballot_Images/Alameda (Oakland, San Leandro, Berkeley)/Alameda (Oakland, San Leandro, Berkeley) 2014/ballot_image_School Director, District 2 - Oakland_Nov 2014.txt',
         'parser': sfnoid,
         'break_on_overvote': True,
         'break_on_repeated undervotes': False
     },
    '2014 Member, City Council, District 3 - San Leandro Nov 2014': {
         'path': 'Ballot_Images/Alameda (Oakland, San Leandro, Berkeley)/Alameda (Oakland, San Leandro, Berkeley) 2014/ballot_image_Member, City Council, District 3 - San Leandro_Nov 2014.txt',
         'parser': sfnoid,
         'break_on_overvote': True,
         'break_on_repeated undervotes': False
     },
    '2014 School Director, District 6 - Oakland Nov 2014': {
         'path': 'Ballot_Images/Alameda (Oakland, San Leandro, Berkeley)/Alameda (Oakland, San Leandro, Berkeley) 2014/ballot_image_School Director, District 6 - Oakland_Nov 2014.txt',
         'parser': sfnoid,
         'break_on_overvote': True,
         'break_on_repeated undervotes': False
     },
    '2016 BerkeleyCouncilD3': {
         'path': 'Ballot_Images/Alameda (Oakland, San Leandro, Berkeley)/Alameda (Oakland, San Leandro, Berkeley) 2016/BerkeleyCouncilD3/ballot_image.txt',
         'parser': sfnoid,
         'break_on_overvote': True,
         'break_on_repeated undervotes': False
     },
    '2016 BerkeleyCouncilD2': {
         'path': 'Ballot_Images/Alameda (Oakland, San Leandro, Berkeley)/Alameda (Oakland, San Leandro, Berkeley) 2016/BerkeleyCouncilD2/ballot_image.txt',
         'parser': sfnoid,
         'break_on_overvote': True,
         'break_on_repeated undervotes': False
     },
    '2016 BerkeleyCouncilD5': {
         'path': 'Ballot_Images/Alameda (Oakland, San Leandro, Berkeley)/Alameda (Oakland, San Leandro, Berkeley) 2016/BerkeleyCouncilD5/ballot_image.txt',
         'parser': sfnoid,
         'break_on_overvote': True,
         'break_on_repeated undervotes': False
     },
    '2016 OaklandSchoolD1': {
         'path': 'Ballot_Images/Alameda (Oakland, San Leandro, Berkeley)/Alameda (Oakland, San Leandro, Berkeley) 2016/OaklandSchoolD1/ballot_image.txt',
         'parser': sfnoid,
         'break_on_overvote': True,
         'break_on_repeated undervotes': False
     },
    '2016 OaklandCouncilD7': {
         'path': 'Ballot_Images/Alameda (Oakland, San Leandro, Berkeley)/Alameda (Oakland, San Leandro, Berkeley) 2016/OaklandCouncilD7/ballot_image.txt',
         'parser': sfnoid,
         'break_on_overvote': True,
         'break_on_repeated undervotes': False
     },
    '2016 BerkeleyMayor': {
         'path': 'Ballot_Images/Alameda (Oakland, San Leandro, Berkeley)/Alameda (Oakland, San Leandro, Berkeley) 2016/BerkeleyMayor/ballot_image.txt',
         'parser': sfnoid,
         'break_on_overvote': True,
         'break_on_repeated undervotes': False
     },
    '2016 OaklandCouncilD1': {
         'path': 'Ballot_Images/Alameda (Oakland, San Leandro, Berkeley)/Alameda (Oakland, San Leandro, Berkeley) 2016/OaklandCouncilD1/ballot_image.txt',
         'parser': sfnoid,
         'break_on_overvote': True,
         'break_on_repeated undervotes': False
     },
    '2016 OaklandSchoolD7': {
         'path': 'Ballot_Images/Alameda (Oakland, San Leandro, Berkeley)/Alameda (Oakland, San Leandro, Berkeley) 2016/OaklandSchoolD7/ballot_image.txt',
         'parser': sfnoid,
         'break_on_overvote': True,
         'break_on_repeated undervotes': False
     },
    '2016 SanLeandroCouncilD2': {
         'path': 'Ballot_Images/Alameda (Oakland, San Leandro, Berkeley)/Alameda (Oakland, San Leandro, Berkeley) 2016/SanLeandroCouncilD2/ballot_image.txt',
         'parser': sfnoid,
         'break_on_overvote': True,
         'break_on_repeated undervotes': False
     },
    '2016 SanLeandroCouncilD4': {
         'path': 'Ballot_Images/Alameda (Oakland, San Leandro, Berkeley)/Alameda (Oakland, San Leandro, Berkeley) 2016/SanLeandroCouncilD4/ballot_image.txt',
         'parser': sfnoid,
         'break_on_overvote': True,
         'break_on_repeated undervotes': False
     },
    '2016 BerkeleyCouncilD6': {
         'path': 'Ballot_Images/Alameda (Oakland, San Leandro, Berkeley)/Alameda (Oakland, San Leandro, Berkeley) 2016/BerkeleyCouncilD6/ballot_image.txt',
         'parser': sfnoid,
         'break_on_overvote': True,
         'break_on_repeated undervotes': False
     },
    '2016 OaklandSchoolD5': {
         'path': 'Ballot_Images/Alameda (Oakland, San Leandro, Berkeley)/Alameda (Oakland, San Leandro, Berkeley) 2016/OaklandSchoolD5/ballot_image.txt',
         'parser': sfnoid,
         'break_on_overvote': True,
         'break_on_repeated undervotes': False
     },
    '2016 OaklandCouncilD3': {
         'path': 'Ballot_Images/Alameda (Oakland, San Leandro, Berkeley)/Alameda (Oakland, San Leandro, Berkeley) 2016/OaklandCouncilD3/ballot_image.txt',
         'parser': sfnoid,
         'break_on_overvote': True,
         'break_on_repeated undervotes': False
     },
    '2016 OaklandCouncilD5': {
         'path': 'Ballot_Images/Alameda (Oakland, San Leandro, Berkeley)/Alameda (Oakland, San Leandro, Berkeley) 2016/OaklandCouncilD5/ballot_image.txt',
         'parser': sfnoid,
         'break_on_overvote': True,
         'break_on_repeated undervotes': False
     },
    '2016 OaklandSchoolD3': {
         'path': 'Ballot_Images/Alameda (Oakland, San Leandro, Berkeley)/Alameda (Oakland, San Leandro, Berkeley) 2016/OaklandSchoolD3/ballot_image.txt',
         'parser': sfnoid,
         'break_on_overvote': True,
         'break_on_repeated undervotes': False
     },
    '2016 OaklandCouncilAtLrg': {
         'path': 'Ballot_Images/Alameda (Oakland, San Leandro, Berkeley)/Alameda (Oakland, San Leandro, Berkeley) 2016/OaklandCouncilAtLrg/ballot_image.txt',
         'parser': sfnoid,
         'break_on_overvote': True,
         'break_on_repeated undervotes': False
     },
    '2016 OaklandAttorney': {
         'path': 'Ballot_Images/Alameda (Oakland, San Leandro, Berkeley)/Alameda (Oakland, San Leandro, Berkeley) 2016/OaklandAttorney/ballot_image.txt',
         'parser': sfnoid,
         'break_on_overvote': True,
         'break_on_repeated undervotes': False
     },
    '2016 SanLeandroCouncilD6': {
         'path': 'Ballot_Images/Alameda (Oakland, San Leandro, Berkeley)/Alameda (Oakland, San Leandro, Berkeley) 2016/SanLeandroCouncilD6/ballot_image.txt',
         'parser': sfnoid,
         'break_on_overvote': True,
         'break_on_repeated undervotes': False
     },
    '2010 Member, City Council, District 4 - Oakland Nov 2010': {
         'path': 'Ballot_Images/Alameda (Oakland, San Leandro, Berkeley)/Alameda (Oakland, San Leandro, Berkeley) 2010/ballot_image_ Member, City Council, District 4 - Oakland_Nov 2010.txt',
         'parser': sfnoid,
         'break_on_overvote': True,
         'break_on_repeated undervotes': False
     },
    '2010 Member, City Council, District 2 - Oakland Nov 2010': {
         'path': 'Ballot_Images/Alameda (Oakland, San Leandro, Berkeley)/Alameda (Oakland, San Leandro, Berkeley) 2010/ballot_image_Member, City Council, District 2 - Oakland_Nov 2010.txt',
         'parser': sfnoid,
         'break_on_overvote': True,
         'break_on_repeated undervotes': False
     },
    '2010 Member, City Council, District 1 - San Leandro Nov 2010': {
         'path': 'Ballot_Images/Alameda (Oakland, San Leandro, Berkeley)/Alameda (Oakland, San Leandro, Berkeley) 2010/ballot_image_Member, City Council, District 1 - San Leandro_Nov 2010.txt',
         'parser': sfnoid,
         'break_on_overvote': True,
         'break_on_repeated undervotes': False
     },
    '2010 Member, City Council, District 8 - Berkeley Nov 2010': {
         'path': 'Ballot_Images/Alameda (Oakland, San Leandro, Berkeley)/Alameda (Oakland, San Leandro, Berkeley) 2010/ballot_image_Member, City Council, District 8 - Berkeley_Nov 2010.txt',
         'parser': sfnoid,
         'break_on_overvote': True,
         'break_on_repeated undervotes': False
     },
    '2010 Member, City Council, District 7 - Berkeley Nov 2010': {
         'path': 'Ballot_Images/Alameda (Oakland, San Leandro, Berkeley)/Alameda (Oakland, San Leandro, Berkeley) 2010/ballot_image_Member, City Council, District 7 - Berkeley_Nov 2010.txt',
         'parser': sfnoid,
         'break_on_overvote': True,
         'break_on_repeated undervotes': False
     },
    '2010 Member, City Council, District 6 - Oakland Nov 2010': {
         'path': 'Ballot_Images/Alameda (Oakland, San Leandro, Berkeley)/Alameda (Oakland, San Leandro, Berkeley) 2010/ballot_image_Member, City Council, District 6 - Oakland_Nov 2010.txt',
         'parser': sfnoid,
         'break_on_overvote': True,
         'break_on_repeated undervotes': False
     },
    '2010 Member, City Council, District 4 - Berkeley Nov 2010': {
         'path': 'Ballot_Images/Alameda (Oakland, San Leandro, Berkeley)/Alameda (Oakland, San Leandro, Berkeley) 2010/ballot_image_Member, City Council, District 4 - Berkeley_Nov 2010.txt',
         'parser': sfnoid,
         'break_on_overvote': True,
         'break_on_repeated undervotes': False
     },
    '2010 City Auditor - Oakland Nov 2010': {
         'path': 'Ballot_Images/Alameda (Oakland, San Leandro, Berkeley)/Alameda (Oakland, San Leandro, Berkeley) 2010/ballot_image_City Auditor - Oakland_Nov 2010.txt',
         'parser': sfnoid,
         'break_on_overvote': True,
         'break_on_repeated undervotes': False
     },
    '2010 Member, City Council, District 5 - San Leandro Nov 2010': {
         'path': 'Ballot_Images/Alameda (Oakland, San Leandro, Berkeley)/Alameda (Oakland, San Leandro, Berkeley) 2010/ballot_image_Member, City Council, District 5 - San Leandro_Nov 2010.txt',
         'parser': sfnoid,
         'break_on_overvote': True,
         'break_on_repeated undervotes': False
     },
    '2010 Mayor of San Leandro Nov 2010': {
         'path': 'Ballot_Images/Alameda (Oakland, San Leandro, Berkeley)/Alameda (Oakland, San Leandro, Berkeley) 2010/ballot_image_Mayor of San Leandro_Nov 2010.txt',
         'parser': sfnoid,
         'break_on_overvote': True,
         'break_on_repeated undervotes': False
     },
    '2010 City Auditor - Berkeley Nov 2010': {
         'path': 'Ballot_Images/Alameda (Oakland, San Leandro, Berkeley)/Alameda (Oakland, San Leandro, Berkeley) 2010/ballot_image_City Auditor - Berkeley_Nov 2010.txt',
         'parser': sfnoid,
         'break_on_overvote': True,
         'break_on_repeated undervotes': False
     },
    '2010 School Director, District 6 - Oakland Nov 2010': {
         'path': 'Ballot_Images/Alameda (Oakland, San Leandro, Berkeley)/Alameda (Oakland, San Leandro, Berkeley) 2010/ballot_image_ School Director, District 6 - Oakland_Nov 2010.txt',
         'parser': sfnoid,
         'break_on_overvote': True,
         'break_on_repeated undervotes': False
     },
    '2010 Mayor of Oakland Nov 2010': {
         'path': 'Ballot_Images/Alameda (Oakland, San Leandro, Berkeley)/Alameda (Oakland, San Leandro, Berkeley) 2010/ballot_image_Mayor of Oakland_Nov 2010.txt',
         'parser': sfnoid,
         'break_on_overvote': True,
         'break_on_repeated undervotes': False
     },
    '2010 Member, City Council, District 1 - Berkeley Nov 2010': {
         'path': 'Ballot_Images/Alameda (Oakland, San Leandro, Berkeley)/Alameda (Oakland, San Leandro, Berkeley) 2010/ballot_image_Member, City Council, District 1 - Berkeley_Nov 2010.txt',
         'parser': sfnoid,
         'break_on_overvote': True,
         'break_on_repeated undervotes': False
     },
    '2010 School Director, District 4 - Oakland Nov 2010': {
         'path': 'Ballot_Images/Alameda (Oakland, San Leandro, Berkeley)/Alameda (Oakland, San Leandro, Berkeley) 2010/ballot_image_ School Director, District 4 - Oakland_Nov 2010.txt',
         'parser': sfnoid,
         'break_on_overvote': True,
         'break_on_repeated undervotes': False
     },
    '2010 School Director, District 2 - Oakland Nov 2010': {
         'path': 'Ballot_Images/Alameda (Oakland, San Leandro, Berkeley)/Alameda (Oakland, San Leandro, Berkeley) 2010/ballot_image_School Director, District 2 - Oakland_Nov 2010.txt',
         'parser': sfnoid,
         'break_on_overvote': True,
         'break_on_repeated undervotes': False
     },
    '2010 Member, City Council, District 3 - San Leandro Nov 2010': {
         'path': 'Ballot_Images/Alameda (Oakland, San Leandro, Berkeley)/Alameda (Oakland, San Leandro, Berkeley) 2010/ballot_image_ Member, City Council, District 3 - San Leandro_Nov 2010.txt',
         'parser': sfnoid,
         'break_on_overvote': True,
         'break_on_repeated undervotes': False
     },
    '2017 BerkCouncilD4': {
         'path': 'Ballot_Images/Alameda (Oakland, San Leandro, Berkeley)/Alameda (Oakland, San Leandro, Berkeley) 2017/BerkCouncilD4/ballot_image.txt',
         'parser': sfnoid,
         'break_on_overvote': True,
         'break_on_repeated undervotes': False
     },
    'Cambridge School Committee 2017': {
        'path': 'Ballot_Images/Cambridge/2017/2017/School Committee/*.prm',
        'parser': prm,
        'break_on_overvote': False,
        'break_on_repeated undervotes': False
    },
    'Cambridge City Council 2017': {
        'path': 'Ballot_Images/Cambridge/2017/2017/City Council/*.prm',
        'parser': prm,
        'break_on_overvote': False,
        'break_on_repeated undervotes': False
    },
    'Cambridge School Committee 2015': {
        'path': 'Ballot_Images/Cambridge/2015/school2015/*.prm',
        'parser': prm,
        'break_on_overvote': False,
        'break_on_repeated undervotes': False
    },
    'Cambridge City Council 2015': {
        'path': 'Ballot_Images/Cambridge/2015/council2015/*.prm',
        'parser': prm,
        'break_on_overvote': False,
        'break_on_repeated undervotes': False
    },
    'Cambridge School Committee 2013': {
        'path': 'Ballot_Images/Cambridge/2013/School/*/*.PRM',
        'parser': prm,
        'break_on_overvote': False,
        'break_on_repeated undervotes': False
    },
    'Cambridge City Council 2013': {
        'path': 'Ballot_Images/Cambridge/2013/Council/*/*.PRM',
        'parser': prm,
        'break_on_overvote': False,
        'break_on_repeated undervotes': False
    },
    'Cambridge School Committee 2011': {
        'path': 'Ballot_Images/Cambridge/2011/School/*/*.PRM',
        'parser': prm,
        'break_on_overvote': False,
        'break_on_repeated undervotes': False
    },
    'Cambridge City Council 2011': {
        'path': 'Ballot_Images/Cambridge/2011/Council/*/*.PRM',
        'parser': prm,
        'break_on_overvote': False,
        'break_on_repeated undervotes': False
    },
    ### Doesn't match with results here https://www.cambridgema.gov/~/media/Files/electioncommission/SchoolCommittee_results.pdf?la=en
    #'Cambridge School Committee 2009': {
    #    'path': 'Ballot_Images/Cambridge/2009/School/*/*.PRM',
    #    'parser': prm,
    #    'break_on_overvote': False,
    #    'break_on_repeated undervotes': False
    #},
    'Cambridge City Council 2009': {
        'path': 'Ballot_Images/Cambridge/2009/Council/*/*.PRM',
        'parser': prm,
        'break_on_overvote': False,
        'break_on_repeated undervotes': False
    },
    'Cambridge City Council 2007': {
        'path': 'Ballot_Images/Cambridge/2007/Council/*/*.[pP][rR][mM]',
        'parser': prm,
        'break_on_overvote': False,
        'break_on_repeated undervotes': False
    },
    'Cambridge School Committee 2007': {
        'path': 'Ballot_Images/Cambridge/2007/School/*/*.[pP][rR][mM]',
        'parser': prm,
        'break_on_overvote': False,
        'break_on_repeated undervotes': False
    },
    'Cambridge School Committee 2005': {
        'path': 'Ballot_Images/Cambridge/2005/School/*/*.[pP][rR][mM]',
        'parser': prm,
        'break_on_overvote': False,
        'break_on_repeated undervotes': False
    },
    'Cambridge City Council 2005': {
        'path': 'Ballot_Images/Cambridge/2005/Council/*/*.[pP][rR][mM]',
        'parser': prm,
        'break_on_overvote': False,
        'break_on_repeated undervotes': False
    },
    'Cambridge City Council 2003': {
        'path': 'Ballot_Images/Cambridge/2003/Council/*/*.[pPW][rRE][mMD]',
        'parser': prm,
        'break_on_overvote': False,
        'break_on_repeated undervotes': False
    },
    'Cambridge School Committee 2003': {
        'path': 'Ballot_Images/Cambridge/2003/School/*/*.[pPW][rRE][mMD]',
        'parser': prm,
        'break_on_overvote': False,
        'break_on_repeated undervotes': False
    },
    'Cambridge City Council 2001': {
        'path': 'Ballot_Images/Cambridge/2001/Council - Wednesday/*.PRM',
        'parser': prm,
        'break_on_overvote': False,
        'break_on_repeated undervotes': False
    },
}

    