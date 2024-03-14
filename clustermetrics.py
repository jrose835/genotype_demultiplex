#Python code for assessing demultiplexing via either HTO or genotype (via souporcell)
# Using confusion matrix visualization, and Adjustted rand score for similarity
#jrose
#18Dec2023

from sklearn.metrics import confusion_matrix, adjusted_rand_score, ConfusionMatrixDisplay
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

HTO = pd.read_csv("./HTO_data.tsv", sep="\t")
geno = pd.read_csv("./clusters.tsv", sep="\t")

#HTO_ind = HTO.set_index('barcode').reindex(geno['barcode']).reset_index()
#^Ran into problem where some HTO are missing compared to geno...perhaps QC filters?
geno_ind = geno.set_index('barcode').reindex(HTO['barcode']).reset_index()

#Fix geno labels
geno_ind.loc[geno_ind['status'] == 'unassigned','assignment'] = 'Negative'
geno_ind['assignment_fix'] = geno_ind['assignment']
geno_ind.loc[geno_ind['status'] == 'doublet', 'assignment_fix'] = 'doublet'

replace = {
    '3': '4',
    '2': '3',
    '1': '2',
    '0': '1',
}

for old, new in replace.items():
    geno_ind['assignment_fix'] = geno_ind['assignment_fix'].str.replace(old, new)

#Fix HTO labels
HTO['class_fix'] = HTO['class'].str.replace('TSB-HTO', '')
HTO['class_fix'] = HTO['class_fix'].str.replace('_',"/")
HTO.loc[HTO['classGlobal']=='Doublet', 'class_fix'] = 'doublet'

#Confusion matrix
labels=['Negative', 'doublet','1','2','3','4']

cm = confusion_matrix(geno_ind['assignment_fix'], HTO['class_fix'], labels=labels)

#Plot
# plot = ConfusionMatrixDisplay(confusion_matrix=cm)
plot = sns.heatmap(cm, annot=True, xticklabels=labels, yticklabels=labels, fmt='.0f')
plot.set(xlabel="HTO", ylabel='Genotype')

plt.savefig('confusion.pdf', dpi=300)


# Note: Upon inspection of the results using a quantification of simiarilty (i.e. Adjusting rand score) didn't seem necessary...they are quite different!
