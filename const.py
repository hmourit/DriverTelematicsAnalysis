import random
from os import listdir
from os.path import join, isdir
random.seed(42)

# Paths
ORIGINAL_DATA_PATH = '../Data/drivers/'
FEATURIZED_DATA_PATH = '../Competition3Shared/featurized_drivers/'
FEATURIZED_DATA_2_PATH = '../Competition3Shared/featurized_drivers_2/'
FEATURIZED_DATA_3_FOLDER = '../Competition3Shared/featurized_drivers_3/'
FEATURIZED_DATA_PICKLED_PATH = '../Competition3Shared/featurized_drivers.pickle'
FEATURIZED_DATA_2_PICKLED_PATH = '../Competition3Shared/featurized_drivers_2.pickle'
PICKLED_MODEL_PATH = '../Competition3Shared/models/model_%s.pickle'
OUTPUT_PATH = '../Competition3Shared/predictions/predictions_%s.txt'
MODEL_DATA_FILE = '../Competition3Shared/model_data.csv'

SINGLE_FILE = 'all.csv'
INDIVIDUAL_FILE = '%d.csv'

DRIVERS_SET = set([int(d[d.rfind('/') + 1:]) for d in listdir(ORIGINAL_DATA_PATH)
               if not d.startswith('.') and isdir(join(ORIGINAL_DATA_PATH, d))])
FEATURIZED_DATA_FILES = listdir(FEATURIZED_DATA_PATH)
N_DRIVERS = len(FEATURIZED_DATA_FILES)

'''
FEATURIZED_DATA:
0  - trip ID
1  - euclidean distance of trip (actual length of trip)
2  - time of trip
3  - mean of speed
4  - std of speed
5  - min of speed
6  - 25th percentile of speed
7  - 50th percentile of speed
8  - 75th percentile of speed
9  - max of speed
10 - mean of acc_lin
11 - std of acc_lin
12 - min of acc_lin
13 - 25th percentile of acc_lin
14 - 50th percentile of acc_lin
15 - 75th percentile of acc_lin
16 - max of acc_lin
17 - mean of acc_cen
18 - std of acc_cen
19 - min of acc_cen
20 - 25th percentile of acc_cen
21 - 50th percentile of acc_cen
22 - 75th percentile of acc_cen
23 - max of acc_cen
'''

'''
FEATURIZED_DATA_2:
0  - trip ID
1  - euclidean distance of trip (actual length of trip)
2  - sum of acc_lin -EX
3  - sum of acc_cen -EX
4  - time of trip
5  - mean of speed -EX
6  - std of speed -EX
7  - min of speed -EX
8  - 12.5th percentile of speed
9 - 25th percentile of speed
10 - 37.5th percentile of speed
11 - 50th percentile of speed
12 - 62.5th percentile of speed
13 - 75th percentile of speed
14 - 87.5th percentile of speed
15 - max of speed
16 - mean of speed_angular  -EX
17 - std of speed_angular -EX
18 - min of speed_angular -EX
19 - 12.5th percentile of speed_angular -EX
20 - 25th percentile of speed_angular -EX
21 - 37.5th percentile of speed_angular -EX
22 - 50th percentile of speed_angular -EX
23 - 62.5th percentile of speed_angular -EX
24 - 75th percentile of speed_angular -EX
25 - 87.5th percentile of speed_angular -EX
26 - max of speed_angular -EX
27 - mean of acc_angular  -EX
28 - std of acc_angular -EX
29 - min of acc_angular -EX
30 - 12.5th percentile of acc_angular -EX
31 - 25th percentile of acc_angular -EX
32 - 37.5th percentile of acc_angular -EX
33 - 50th percentile of acc_angular -EX
34 - 62.5th percentile of acc_angular -EX
35 - 75th percentile of acc_angular -EX
36 - 87.5th percentile of acc_angular -EX
37 - max of acc_angular -EX
38 - mean of acc_lin -EX
39 - std of acc_lin -EX
40 - min of acc_lin -EX
41 - 12.5th percentile of acc_lin
42 - 25th percentile of acc_lin
43 - 37.5th percentile of acc_lin
44 - 50th percentile of acc_lin
45 - 62.5th percentile of acc_lin
46 - 75th percentile of acc_lin
47 - 87.5th percentile of acc_lin
48 - max of acc_lin
49 - mean of acc_cen -EX
50 - std of acc_cen -EX
51 - min of acc_cen -EX
52 - 12.5th percentile of acc_cen
53 - 25th percentile of acc_cen
54 - 37.5th percentile of acc_cen
55 - 50th percentile of acc_cen
56 - 62.5th percentile of acc_cen
57 - 75th percentile of acc_cen
58 - 87.5th percentile of acc_cen
59 - max of acc_cen
60 - mean of speed_angular absolute -EX
61 - std of speed_angular absolute -EX
62 - min of speed_angular absolute -EX
63 - 12.5th percentile of speed_angular absolute
64 - 25th percentile of speed_angular absolute
65 - 37.5th percentile of speed_angular absolute
66 - 50th percentile of speed_angular absolute
67 - 62.5th percentile of speed_angular absolute
68 - 75th percentile of speed_angular absolute
69 - 87.5th percentile of speed_angular absolute
70 - max of speed_angular absolute
71 - mean of acc_angular absolute -EX
72 - std of acc_angular absolute -EX
73 - min of acc_angular absolute -EX
74 - 12.5th percentile of acc_angular absolute
75 - 25th percentile of acc_angular absolute
76 - 37.5th percentile of acc_angular absolute
77 - 50th percentile of acc_angular absolute
78 - 62.5th percentile of acc_angular absolute
79 - 75th percentile of acc_angular absolute
80 - 87.5th percentile of acc_angular absolute
81 - max of acc_angular absolute
'''