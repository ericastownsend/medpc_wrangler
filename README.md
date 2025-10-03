# med_wrangler
a set of functions to read and clean medPC data files, as well as pull out specific events and their latencies

files:
medpc_wrangler.py - functions written in python  
medpc_wrangler_example.ipynb - walkthrough of function use for users who store data in one array (ie, data formats in event+timestamp format)
medpc_data_example - one of two medpc data files used in the example .ipynb file above  
medpc_wrangler_example_multiarray.ipynb - walkthrough of function use for users who store data in two arrays (ie, events in one array and corresponding timestamps in a separate array). *beware that some auxillary functions may not be useable, as many of them were created for pavlovian trial based data*

*event codes and arrays are malleable. some functions may require minor editing if anything is hardcoded (eg, array identifiers or event codes beyond 9000 if your data is stored entirely in one array.*
