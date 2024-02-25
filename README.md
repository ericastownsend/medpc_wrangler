# med_wrangler
a set of functions to read and clean medPC data files, as well as pull out specific events and their latencies

files:
medpc_wrangler.py - functions written in python  
medpc_wrangler_example.ipynb - walkthrough of function use  
medpc_data_example - one of two medpc data files used in the example .ipynb file above  

## med pc file output requirements:  
**event codes are saved as event code + time in seconds**  
  
brief example:   
  
\event codes  
^RepA = 10000 \CS+ press  
^RepB = 20000 \CS- press  
^MS = 30000 \mag start  
^ME = 40000 \mag end  
^CSAS = 50000 \CS+ start  
^CSAE = 60000 \ CS+ end  
^CSBS = 70000 \CS- start  
^CSBE = 80000 \CS- end  
  
a CS+ press at second 456.78 would appear as 10456.78  
  
*these event codes are malleable. if the value of your event codes differ (but save in the data as (event code + timestamp)) or you have less/more than 9 event codes, the time_event function may require minor editing.*

finally, your data should be saved **only in the B: array** of the medpc file. an example of what this might look like can be seen in medpc_wrangler_example.ipynb or medpc_data_example. this is a simple tweak in the extract_data_from_file function.
