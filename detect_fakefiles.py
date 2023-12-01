import pandas as pd
import glob
import os
from itertools import combinations
from sklearn.metrics import cohen_kappa_score
from sklearn.preprocessing import LabelEncoder


# Set the path to the directory containing the submission files
path_to_files= os.path.abspath(".\P2a Labels\P2a Labels")
crowdworker_files= glob.glob(os.path.join(path_to_files, "*.xlsx"))
# path_to_files= os.path.abspath(".\z\z")
# crowdworker_files= glob.glob(os.path.join(path_to_files, "*.xlsx"))

kappa_values = {}

# Generate all possible pairs of files to produce Cohen's kappa 
file_pairs = combinations(crowdworker_files, 2)

for file1, file2 in file_pairs:
    df1 = pd.read_excel(file1)
    df2 = pd.read_excel(file2)

    #consider only the violation columns for kappa calc
    violations = ['First violation', 'Second violation', 'Third violation']

    # Considering the violations columns only for Cohen's Kappa values
    worker_annotations1 = df1.loc[:, violations].copy()
    worker_annotations2 = df2.loc[:, violations].copy()

    # Combine all the labels from both workers 
    all_labels = pd.concat([worker_annotations1, worker_annotations2], ignore_index=True)

    #Encode each value of violations
    label_encoder = LabelEncoder()
    for v in violations:
        all_labels[v] = label_encoder.fit_transform(all_labels[v])
        worker_annotations1[v] = label_encoder.transform(worker_annotations1[v])
        worker_annotations2[v] = label_encoder.transform(worker_annotations2[v])

    # Cohen's Kappa for each violation category
    kappa_values[(file1, file2)] = {}
    total_kappa = 0 
    for v in violations:
        kappa = cohen_kappa_score(worker_annotations1[v], worker_annotations2[v])
        kappa_values[(file1, file2)][v] = kappa
        total_kappa += kappa

    kappa_values[(file1, file2)]['Total Kappa'] = total_kappa

sorted_kappa_values = sorted(kappa_values.items(), key=lambda x: x[1]['Total Kappa'], reverse=True)

# Display Cohen's Kappa values for each pair and combined sum of each violation category
for (worker1, worker2), kappa_dict in sorted_kappa_values:
    print(f"Pair= {worker1} and {worker2}")
    print(f"Total Kappa= {kappa_dict['Total Kappa']}")
    print()




























