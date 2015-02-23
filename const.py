import random
from os import listdir
random.seed(42)

# Paths
ORIGINAL_DATA_PATH = '../Data/drivers/'
FEATURIZED_DATA_PATH = '../Competition3Shared/featurized_drivers/'
FEATURIZED_DATA_2_PATH = '../Competition3Shared/featurized_drivers_2/'
FEATURIZED_DATA_PICKLED_PATH = '../Competition3Shared/featurized_drivers.pickle'
FEATURIZED_DATA_2_PICKLED_PATH = '../Competition3Shared/featurized_drivers_2.pickle'
PICKLED_MODEL_PATH = '../Competition3Shared/models/model_%s.pickle'
OUTPUT_PATH = '../Competition3Shared/predictions/predictions_%s.txt'
MODEL_DATA_FILE = '../Competition3Shared/model_data.csv'


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
6  - max of speed
7  - 25th percentile of speed
8  - 50th percentile of speed
9  - 75th percentile of speed
10 - mean of speed
11 - std of speed
12 - min of speed
13 - max of speed
14 - 25th percentile of acc_lin
15 - 50th percentile of acc_lin
16 - 75th percentile of acc_lin
17 - mean of acc_cen
18 - std of acc_cen
19 - min of acc_cen
20 - max of acc_cen
21 - 25th percentile of acc_cen
22 - 50th percentile of acc_cen
23 - 75th percentile of acc_cen
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
8  - max of speed
9  - 12.5th percentile of speed
10 - 25th percentile of speed
11 - 37.5th percentile of speed
12 - 50th percentile of speed
13 - 62.5th percentile of speed
14 - 75th percentile of speed
15 - 87.5th percentile of speed
16 - mean of speed_angular  -EX
17 - std of speed_angular -EX
18 - min of speed_angular -EX
19 - max of speed_angular -EX
20 - 12.5th percentile of speed_angular -EX
21 - 25th percentile of speed_angular -EX
22 - 37.5th percentile of speed_angular -EX
23 - 50th percentile of speed_angular -EX
24 - 62.5th percentile of speed_angular -EX
25 - 75th percentile of speed_angular -EX
26 - 87.5th percentile of speed_angular -EX
27 - mean of acc_angular  -EX
28 - std of acc_angular -EX
29 - min of acc_angular -EX
30 - max of acc_angular -EX
31 - 12.5th percentile of acc_angular -EX
32 - 25th percentile of acc_angular -EX
33 - 37.5th percentile of acc_angular -EX
34 - 50th percentile of acc_angular -EX
35 - 62.5th percentile of acc_angular -EX
36 - 75th percentile of acc_angular -EX
37 - 87.5th percentile of acc_angular -EX
38 - mean of acc_lin -EX
39 - std of acc_lin -EX
40 - min of acc_lin -EX
41 - max of acc_lin
42 - 12.5th percentile of acc_lin
43 - 25th percentile of acc_lin
44 - 37.5th percentile of acc_lin
45 - 50th percentile of acc_lin
46 - 62.5th percentile of acc_lin
47 - 75th percentile of acc_lin
48 - 87.5th percentile of acc_lin
49 - mean of acc_cen -EX
50 - std of acc_cen -EX
51 - min of acc_cen -EX
52 - max of acc_cen
53 - 12.5th percentile of acc_cen
54 - 25th percentile of acc_cen
55 - 37.5th percentile of acc_cen
56 - 50th percentile of acc_cen
57 - 62.5th percentile of acc_cen
58 - 75th percentile of acc_cen
59 - 87.5th percentile of acc_cen
60 - mean of speed_angular absolute -EX
61 - std of speed_angular absolute -EX
62 - min of speed_angular absolute -EX
63 - max of speed_angular absolute
64 - 12.5th percentile of speed_angular absolute
65 - 25th percentile of speed_angular absolute
66 - 37.5th percentile of speed_angular absolute
67 - 50th percentile of speed_angular absolute
68 - 62.5th percentile of speed_angular absolute
69 - 75th percentile of speed_angular absolute
70 - 87.5th percentile of speed_angular absolute
71 - mean of acc_angular absolute -EX
72 - std of acc_angular absolute -EX
73 - min of acc_angular absolute -EX
74 - max of acc_angular absolute
75 - 12.5th percentile of acc_angular absolute
76 - 25th percentile of acc_angular absolute
77 - 37.5th percentile of acc_angular absolute
78 - 50th percentile of acc_angular absolute
79 - 62.5th percentile of acc_angular absolute
80 - 75th percentile of acc_angular absolute
81 - 87.5th percentile of acc_angular absolute
'''