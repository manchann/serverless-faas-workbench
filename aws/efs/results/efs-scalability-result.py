
# coding: utf-8

# In[205]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# In[262]:


df_2048 = pd.read_csv('efs-scalability-2048.csv')
df_2048_2 = pd.read_csv('efs-scalability-2048-2.csv')
df_512 = pd.read_csv('efs-scalability-512.csv')
df_512_2 = pd.read_csv('efs-scalability-512-2.csv')


# In[263]:


df


# In[264]:


df_ran = df.copy()
df_seq = df.copy()
df_dd = df.copy()

df_ran = df_ran[df_ran['second_type/S'].isin(['random'])]
df_seq = df_seq[df_seq['second_type/S'].isin(['sequence'])]
df_dd = df_dd[df_dd['second_type/S'].isin(['dd'])]

concurrency = ['efs_strong1',
             'efs_strong10',
             'efs_strong20',
             'efs_strong50',
             'efs_strong100',
             'efs_strong200']


# In[274]:


df_ran = df_512_2.copy()
df_seq = df_512_2.copy()
df_dd = df_512_2.copy()

file_size = 200
df_ran = df_ran[df_ran['second_type/S'].isin(['random'])]
df_seq = df_seq[df_seq['second_type/S'].isin(['sequence'])]
df_dd = df_dd[df_dd['second_type/S'].isin(['dd'])]

concurrency = ['efs_strong1',
             'efs_strong10',
             'efs_strong20',
             'efs_strong50',
             'efs_strong100',
             'efs_strong200']

ran_latency = []
ran_bw = []
ran_err = []
for ran in concurrency:
    df_col = df_ran[df_ran['test/S'].isin([ran])]
    avg_latency = df_col['disk_read_latency/N'].mean()
    avg_bandwidth = df_col['disk_read_bandwidth/N'].mean()
    ran_latency.append(avg_latency)
    ran_bw.append(avg_bandwidth)
    ran_err.append((avg_latency - df_col['disk_read_latency/N'].min(),df_col['disk_read_latency/N'].max() - avg_latency)) 
    
error_ran = np.array(ran_err)
print(error_ran)

seq_latency = []
seq_bw = []
seq_err = []
for seq in concurrency:
    df_col = df_seq[df_seq['test/S'].isin([seq])]
    avg_latency = df_col['disk_read_latency/N'].mean()
    avg_bandwidth = df_col['disk_read_bandwidth/N'].mean()
    seq_latency.append(avg_latency)
    seq_bw.append(avg_bandwidth)
    seq_err.append((avg_latency - df_col['disk_read_latency/N'].min(),df_col['disk_read_latency/N'].max() - avg_latency)) 
print(seq_latency)
error_seq = np.array(seq_err)
print(error_seq)

dd_latency = []
dd_bw = []
dd_err = []
for d in concurrency:
    df_col = df_dd[df_dd['test/S'].isin([d])]
    avg_latency = df_col['latency/N'].mean()
    avg_bandwidth = df_col['disk_read_bandwidth/N'].mean()
    dd_latency.append(avg_latency)
    dd_bw.append(file_size/avg_latency)
    dd_err.append((avg_latency - df_col['latency/N'].min(),df_col['latency/N'].max() - avg_latency)) 
    
error_dd = np.array(dd_err)
print(error_dd)


# In[272]:


df_ran = df_2048_2.copy()
df_seq = df_2048_2.copy()
df_dd = df_2048_2.copy()

df_ran = df_ran[df_ran['second_type/S'].isin(['random'])]
df_seq = df_seq[df_seq['second_type/S'].isin(['sequence'])]
df_dd = df_dd[df_dd['second_type/S'].isin(['dd'])]

concurrency = ['efs_strong1',
             'efs_strong10',
             'efs_strong20',
             'efs_strong50',
             'efs_strong100',
             'efs_strong200']
concurrency_num = ['1','10','20','50','100','200']
ran_latency = []
ran_err = []
for ran in concurrency:
    df_col = df_ran[df_ran['test/S'].isin([ran])]
    avg_latency = df_col['disk_read_latency/N'].mean()
    avg_bandwidth = df_col['disk_read_bandwidth/N'].mean()
    ran_latency.append(avg_latency)
    ran_err.append((avg_latency - df_col['disk_read_latency/N'].min(),df_col['disk_read_latency/N'].max() - avg_latency)) 
    
error_ran = np.array(ran_err)
print(error_ran)

seq_latency = []
seq_err = []
for seq in concurrency:
    df_col = df_seq[df_seq['test/S'].isin([seq])]
    avg_latency = df_col['disk_read_latency/N'].mean()
    avg_bandwidth = df_col['disk_read_bandwidth/N'].mean()
    seq_latency.append(avg_latency)
    seq_err.append((avg_latency - df_col['disk_read_latency/N'].min(),df_col['disk_read_latency/N'].max() - avg_latency)) 
print(seq_latency)
error_seq = np.array(seq_err)
print(error_seq)

dd_latency = []
dd_err = []
for d in concurrency:
    df_col = df_dd[df_dd['test/S'].isin([d])]
    avg_latency = df_col['latency/N'].mean()
    dd_latency.append(avg_latency)
    dd_err.append((avg_latency - df_col['latency/N'].min(),df_col['latency/N'].max() - avg_latency)) 
    
error_dd = np.array(dd_err)
print(error_dd)


# In[275]:


print(ran_bw)
print(seq_bw)
print(dd_bw)

fig, axes = plt.subplots(1,3,figsize=(10,7))

axes[0] = plt.subplot(1,3,1)
axes[1] = plt.subplot(1,3,2)
axes[2] = plt.subplot(1,3,3)
axes[0].bar(concurrency_num,ran_bw)
axes[0].set_xlabel('random read',fontsize=15)
axes[1].bar(concurrency_num,seq_latency,yerr=error_seq.T)
axes[1].set_xlabel('sequence read',fontsize=15)
print(error_seq)
axes[2].bar(concurrency_num,dd_latency,yerr=error_dd.T)
axes[2].set_xlabel('dd',fontsize=15)
axes[0].set_ylabel('Latency',fontsize=30)
fig.suptitle('Lambda:512MB',fontsize=30)


# In[269]:


fig, axes = plt.subplots(1,3,figsize=(10,7))

axes[0] = plt.subplot(1,3,1)
axes[1] = plt.subplot(1,3,2)
axes[2] = plt.subplot(1,3,3)
axes[0].bar(concurrency_num,ran_bw)
axes[0].set_xlabel('random read',fontsize=15)
axes[1].bar(concurrency_num,seq_latency,yerr=error_seq.T)
axes[1].set_xlabel('sequence read',fontsize=15)
print(error_seq)
axes[2].bar(concurrency_num,dd_latency,yerr=error_dd.T)
axes[2].set_xlabel('dd',fontsize=15)
axes[0].set_ylabel('Latency',fontsize=30)
fig.suptitle('Lambda:512MB',fontsize=30)


# In[273]:


fig, axes = plt.subplots(1,3,figsize=(10,7))

axes[0] = plt.subplot(1,3,1)
axes[1] = plt.subplot(1,3,2)
axes[2] = plt.subplot(1,3,3)
axes[0].bar(concurrency_num,ran_bw)
axes[0].set_xlabel('random read',fontsize=15)
axes[1].bar(concurrency_num,seq_latency,yerr=error_seq.T)
axes[1].set_xlabel('sequence read',fontsize=15)
print(error_seq)
axes[2].bar(concurrency_num,dd_latency,yerr=error_dd.T)
axes[2].set_xlabel('dd',fontsize=15)
axes[0].set_ylabel('Latency',fontsize=30)
fig.suptitle('Lambda:2048MB',fontsize=30)


# In[271]:


fig, axes = plt.subplots(1,3,figsize=(10,7))

axes[0] = plt.subplot(1,3,1)
axes[1] = plt.subplot(1,3,2)
axes[2] = plt.subplot(1,3,3)
axes[0].bar(concurrency_num,ran_bw)
axes[0].set_xlabel('random read',fontsize=15)
axes[1].bar(concurrency_num,seq_latency,yerr=error_seq.T)
axes[1].set_xlabel('sequence read',fontsize=15)
print(error_seq)
axes[2].bar(concurrency_num,dd_latency,yerr=error_dd.T)
axes[2].set_xlabel('dd',fontsize=15)
axes[0].set_ylabel('Latency',fontsize=30)
fig.suptitle('Lambda:2048MB',fontsize=30)


# In[214]:


plt.bar(['1','10','20','50','100','200'],
       dd_latency
        ,yerr=error_dd.T)
print(error_dd.T)

