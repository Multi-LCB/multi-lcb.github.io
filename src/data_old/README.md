### Данные
    data/sample%03d.json - данные которые будут обновлятся со временем
    
### Какие вычисления нужно сделать на лендинге
```python
import glob
import pandas as pd
import numpy as np

# Load data
data_files = glob.glob("swe-mera/data/**.json")
df = pd.concat([pd.read_json(fn) for fn in data_files], ignore_index=True)
df.drop(columns='task_id', inplace=True)

# Define date range
start_date = '2025-02-26'
end_date = '2025-06-04'

# Filter by date
df_filtered = df[(df['date'] >= start_date) & (df['date'] <= end_date)]

# Group by model and calculate aggregations
def summarize_model(group):
    model_name = group.iloc[0]['model']
    return pd.Series({
        "pass@1": group['pass@1'].mean(),
        "pass@1_std": group['pass@1'].std() / np.sqrt(len(group)),
        "pass@5": group['pass@5'].mean(),
        "n_task": len(group),
        "trajectory": f'<a href="http://github.com/mera/swe-mera/trajectory/{model_name}">trajectory</a>'
    })

summary_df = df_filtered.groupby("model").apply(summarize_model).reset_index()
summary_df
```

### Как были замоканы данные (20250528)

```python
from datetime import timedelta
import pandas as pd
import numpy as np
models = ['gpt-4.1-2025-04-14',
          'gpt-4.1-mini-2025-04-14',
          'gemini-2.5-flash-preview-05-20 no-thinking',
          'DeepSeek-V3-0324',
          'DeepSeek-V3',
          'Qwen3-235B-A22B no-thinking',
          'Qwen3-32B no-thinking',
          'Qwen3-32B thinking',
          'Qwen3-235B-A22B thinking',
          'Llama-4-Maverick-17B-128E-Instruct',
          'Llama-3.3-70B-Instruct',
          'gemini-2.0-flash',
          'Llama-4-Scout-17B-16E-Instruct',
          'Qwen2.5-72B-Instruct',
          'gemma-3-27b-it',
          'Devstral-Small-2505',
          'Qwen2.5-Coder-32B-Instruct',
          'gpt-4.1-nano-2025-04-14'
         ]

models_ms = {}
for model in models:
    models_ms[model] = np.random.randint(2, 100)/100, np.random.randint(2, 100)/100

t_list = [pd.to_datetime("2025-01-01")]

for i in range(12):
    t_list.append(t_list[-1] + timedelta(days=14))

n_samples = np.random.randint(10, 100, size = len(t_list))    

data = []

for model in models:
    for ind, t in enumerate(t_list):
        np.random.seed(hash(str(t))%10000)
        n = n_samples[ind]
        pass_1 = np.random.randn(n)
        pass_1 += models_ms[model][0]
        pass_1 *= models_ms[model][1]
        pass_1 = pass_1**2
        pass_1 = np.clip(pass_1, 0, 1)
        
        pass_5 = pass_1 + (np.random.randint(1, 50, size = n)/50)
        pass_5 = np.clip(pass_5, 0, 1)

        for ind, (p1, p5) in enumerate(zip(pass_1, pass_5)):
            data.append({'model': model,
                         'date': t,
                         "pass@1": p1,
                         "pass@5": p5,
                         'task_id': "task-%s"%ind
                        })
            
data = pd.DataFrame(data)

# Skip one model for debug purposes
data = data[~((data['date'] < pd.to_datetime("2025-04-12")) & (data['model'].apply(lambda x: 'Qwen3' in x)))]
data = pd.DataFrame(data)


# Save to several batches as in real future
t_cutoff = pd.to_datetime(["2020-03-12 00:00:00", "2025-03-12 00:00:00", 
          '2025-04-23 00:00:00',
          '2025-05-07 00:00:00', 
          '2025-05-21 00:00:00', 
          '2025-06-04 00:00:00',
          '2025-06-28 00:00:00'
         ])

for ind, (l, r) in enumerate(zip(t_cutoff[:-1], t_cutoff[1:])):
    fn_output = 'sample%03d'%ind
    data[(data['date']>=l) & (data['date']<r)].reset_index(drop=True).to_json(fn_output)
```