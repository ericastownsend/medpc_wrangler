#!/usr/bin/env python
# coding: utf-8
'''
* file: medpc_wrangler.py
* created on: feb 24, 2024
* created by: erica townsend
* last revised on: oct 3, 2025

~ ~ ~

functions for conversion of medpc files to a more
useable & digestible format for further analysis

~ ~ ~

REQUIREMENTS:
IF TWO ARRAYS ARE SAVED:
* event codes must be in Y array
* timestamps must be in Z array
to change, edit the letters in extract_data_from_file function.

IF ONE ARRAY IS SAVED:
* requires event/timestamp pairs to be saved as the following:
    event code: X0000
    timestamp in seconds (X.XXX)
    example (event code 30000, timestamp 180.970): 30180.970
    * IF EVENT CODES ARE DIFFERENT: change the values of event 
    codes in the time_event function
* requires Experiment to be a session value (eg, day_12; 12; session_12; session 12)
* requires data to be saved in B array
    * IF DATA SAVED IN DIFFERENT ARRAY: change 'B:' to array letter and 'C:' to 
    array letter directly following data array in your datafiles in the 
    extract_data_from_file function
'''

import numpy as np
import re
import string
import pandas as pd
import glob

# convert mpc datafile to strings
def mpc_to_strings(filename):
    fid = open(filename)
    lines = fid.readlines() 
    fid.close()
    lines = [line for line in lines if ':        0.000' not in line]
    subjects_data = [] 
    current_subject_data = []  
    for line in lines:
        if line.startswith('Start Date:'): 
            if current_subject_data: 
                subjects_data.append(current_subject_data) 
            current_subject_data = [] 
        current_subject_data.append(line.strip())  
    if current_subject_data:
        subjects_data.append(current_subject_data)
    return subjects_data

# cleaning support for next function
def extract_data(subject_data):
    extracted_data = []
    for line in subject_data:
        cleaned_line = line.split(':')[-1].strip()
        if cleaned_line:
            numbers = cleaned_line.split()
            for number in numbers:
                extracted_data.append(number)
    return extracted_data

# extract each event-timestamp instance from strings into a list of event-timestamps
def extract_data_from_file(file_data, multi_array = True):
    raw_data = []
    all_subjects_data = []
    if multi_array == True:
        for subject_lines in file_data:
            subject_data = []
            subject_time = []
            subject_identifier = None
            session_id = None
            is_data_line = False
            is_time_line = False
            for line in subject_lines:
                if line.startswith('Subject:'):
                    subject_identifier = line.split(':')[-1].strip()
                elif line.startswith('Experiment:'):
                    session_id = line.split(':')[-1].strip()
                elif line.startswith('Y:'):
                    is_data_line = True
                elif line.startswith('Z:'):
                    is_data_line = False
                    is_time_line = True
                elif is_data_line:
                    subject_data.append(line)
                elif is_time_line:
                    subject_time.append(line)
            if subject_identifier and subject_data:
                raw_data.append((subject_identifier, session_id, extract_data(subject_data), extract_data(subject_time)))
        return raw_data
    elif multi_array == False:
        for subject_lines in file_data:
            subject_data = []
            subject_identifier = None
            session_id = None
            is_data_line = False
            for line in subject_lines:
                if line.startswith('Subject:'):
                    subject_identifier = line.split(':')[-1].strip()
                elif line.startswith('Experiment:'):
                    session_id = line.split(':')[-1].strip()
                elif line.startswith('B:'):
                    is_data_line = True
                elif line.startswith('C:'):
                    is_data_line = False
                elif is_data_line:
                    subject_data.append(line)
            if subject_identifier and subject_data:
                all_subjects_data.append((subject_identifier, session_id, extract_data(subject_data)))
        return all_subjects_data

# take extracted data list and form a more digestible dataframe with events and timestamps
# if event codes are not in X0000 format or more/less event codes exist this will need updating
def time_event(data_list, multi_array = True):
    time_event_data = []
    if multi_array == True:
        list_of_temp_dfs = []
        for subject_id, session_id, datapoint, timepoint in data_list:
            temp_df = pd.DataFrame({'subject': subject_id, 'session':session_id,
                                    'event': datapoint, 'time': timepoint})
            list_of_temp_dfs.append(temp_df)
        time_event_df = pd.concat(list_of_temp_dfs)
        time_event_df = time_event_df.dropna()
        return time_event_df
    if multi_array == False: 
        for subject_id, session_id, datapoints in data_list:
            singlesubj_data = []
            for datapoint in datapoints:
                temp = []
                datapoint = float(datapoint)
                if datapoint > 10000 and datapoint < 20000:
                    temp = [(round((datapoint-10000), 4)), 10000]
                    singlesubj_data.append(temp)
                elif datapoint > 20000 and datapoint < 30000: 
                    temp = [(round((datapoint-20000), 4)), 20000]
                    singlesubj_data.append(temp)
                elif datapoint > 30000 and datapoint < 40000:
                    temp = [(round((datapoint-30000), 4)), 30000]
                    singlesubj_data.append(temp)
                elif datapoint > 40000 and datapoint < 50000:
                    temp = [(round((datapoint-40000), 4)), 40000]
                    singlesubj_data.append(temp)
                elif datapoint > 50000 and datapoint < 60000:
                    temp = [(round((datapoint-50000), 4)), 50000]
                    singlesubj_data.append(temp)
                elif datapoint > 60000 and datapoint < 70000: 
                    temp = [(round((datapoint-60000), 4)), 60000]
                    singlesubj_data.append(temp)
                elif datapoint > 70000 and datapoint < 80000: 
                    temp = [(round((datapoint-70000), 4)), 70000]
                    singlesubj_data.append(temp)
                elif datapoint > 80000 and datapoint < 90000:
                    temp = [(round((datapoint-80000), 4)), 80000]
                    singlesubj_data.append(temp)
                elif datapoint > 90000 and datapoint < (100000):
                    temp = [(round((datapoint-90000), 4)), 90000]
                    singlesubj_data.append(temp)
            time_event_data.append((subject_id, session_id, singlesubj_data))
        list_of_temp_dfs = []
        for subject_id, session_id, datapoints in time_event_data:
            for time, event in datapoints:
                temp_df = pd.DataFrame({'subject': subject_id, 'session':session_id,
                                        'event': event, 'time': time}, index=[0])
                list_of_temp_dfs.append(temp_df)
        time_event_df = pd.concat(list_of_temp_dfs)
        time_event_df = time_event_df.dropna()
        return time_event_df

# count number of x event between a trial start/end or end/start
# eg, presses between trial start and trial end
def event_trial_counts(df, event1, event2, event_of_interest):
    result_data = {'subject': [], 'session': [], 'trial': [], 'count': []}
    for animal_session, animal_session_data in df.groupby('animal_session'):
        trial_number = 1  # Reset trial number for each subject
        trial_event_counts = 0
        trial_start = None
        for index, row in animal_session_data.iterrows():
            if row['event'] == event1:
                trial_start = row['time']
            elif row['event'] == event2:
                result_data['subject'].append(animal_session_data.subject.values[0])
                result_data['session'].append(animal_session_data.session.values[0])
                result_data['trial'].append(trial_number)
                result_data['count'].append(trial_event_counts)
                trial_number += 1
                trial_event_counts = 0 
                trial_start = None
            elif row['event'] == event_of_interest and trial_start is not None:
                trial_event_counts += 1
    event_counts_df = pd.DataFrame(result_data)
    return event_counts_df

# count number of x event between a given event and given time in seconds
# eg, number of magazine entries 10 s after trials
def event_timed_counts(df, event1, seconds_post_event, event_of_interest):
    result_data = {'subject': [], 'session': [], 'instance': [], 'count': []}
    for animal_session, animal_session_data in df.groupby('animal_session'):
        instance_number = 1  # Reset trial number for each subject
        event_counts = 0
        event1_start = None
        event1_time = 0
        for index, row in animal_session_data.iterrows():
            if row['event'] == event1:
                event1_time = row['time']
                event1_start = row['time']
            elif row['time'] >= (event1_time + seconds_post_event) and event1_start is not None:
                result_data['subject'].append(animal_session_data.subject.values[0])
                result_data['session'].append(animal_session_data.session.values[0])
                result_data['instance'].append(instance_number)
                result_data['count'].append(event_counts)
                instance_number += 1
                event_counts = 0
                event1_start = None
                event1_time = 0
            elif row['event'] == event_of_interest and event1_start is not None:
                event_counts += 1
    event_timed_counts_df = pd.DataFrame(result_data)
    return event_timed_counts_df

# pulls out latency to the FIRST x event between a trial start/end
def event_trial_latency(df, event1, event2, event_of_interest):
    result_data = {'subject': [], 'session': [], 'trial': [], 'latency': []}
    for animal_session, animal_session_data in df.groupby('animal_session'):
        trial_number = 1
        trial_start = None
        for index, row in animal_session_data.iterrows():
            if row['event'] == event1:
                trial_start = row['time']
                event_recorded_this_trial = False
            elif row['event'] == event2:
                trial_start = None
                if not event_recorded_this_trial: # append filler value
                    result_data['subject'].append(animal_session_data.subject.values[0])
                    result_data['trial'].append(trial_number)
                    result_data['latency'].append(np.nan)
                    result_data['session'].append(animal_session_data.session.values[0])
                trial_number += 1
            elif row['event'] == event_of_interest and trial_start is not None:
                latency = row['time'] - trial_start
                result_data['subject'].append(animal_session_data.subject.values[0])
                result_data['trial'].append(trial_number)
                result_data['latency'].append(latency)
                result_data['session'].append(animal_session_data.session.values[0])
                trial_start = None 
                event_recorded_this_trial = True
    
    result_df = pd.DataFrame(result_data)
    return result_df

# pulls out latency to the FIRST x event between a given event and given time in seconds
# eg, latency to first magazine entry 10 s after trials
def event_timed_latency(df, event1, seconds_post_event, event_of_interest):
    result_data = {'subject': [], 'session': [], 'instance': [], 'latency': []}
    for animal_session, animal_session_data in df.groupby('animal_session'):
        instance_number = 1
        event1_start = None
        event1_time = 0
        for index, row in animal_session_data.iterrows():
            if row['event'] == event1:
                event1_start = row['time']
                event1_time = row['time']
                event_recorded_this_instance = False
            elif row['time'] >= (event1_time + seconds_post_event) and event1_start is not None:
                event1_start = None
                if not event_recorded_this_instance: # append filler value
                    result_data['subject'].append(animal_session_data.subject.values[0])
                    result_data['instance'].append(instance_number)
                    result_data['latency'].append(np.nan)
                    result_data['session'].append(animal_session_data.session.values[0])
                instance_number += 1
                event1_time = 0
            elif row['event'] == event_of_interest and event1_start is not None:
                latency = row['time'] - event1_start
                result_data['subject'].append(animal_session_data.subject.values[0])
                result_data['instance'].append(instance_number)
                result_data['latency'].append(latency)
                result_data['session'].append(animal_session_data.session.values[0])
                event1_start = None 
                event_recorded_this_instance = True
    
    result_df = pd.DataFrame(result_data)
    return result_df


#gets average time between multiple instances of a single event
#eg, inter press intervals
def inter_event_interval(df, event):
    average_iei_df = {'subject': [], 'session': [], 'average_iei': []}
    animal_average = 0
    instance_lat_from_prev = 0
    event_count = 0
    prev_event_time = 0
    for animal_session, animal_session_data in df.groupby('animal_session'):
        for index, row in animal_session_data.iterrows():
            if row['event'] == event:
                if event_count == 0:
                    event_count += 1
                    prev_event_time = row['time']
                elif event_count > 0:
                    event_count +=1
                    instance_lat_from_prev = (row['time'] - prev_event_time)
                    animal_average += instance_lat_from_prev
                    prev_event_time = row['time']
        animal_average = animal_average/event_count
        average_iei_df['average_iei'].append(animal_average)
        average_iei_df['subject'].append(animal_session_data['subject'].values[0])
        average_iei_df['session'].append(animal_session_data['session'].values[0])
        animal_average = 0
        instance_lat_from_prev = 0
        event_count = 0
        prev_event_count = 0
    average_iei_df = pd.DataFrame(average_iei_df)
    return average_iei_df
