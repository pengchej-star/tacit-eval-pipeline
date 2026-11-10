# %% [markdown]
# ## HMS 2024 - Brain ... cont. ...

# %% [markdown]
# Classifying different types of <b>Harmful Brain Activity</b>, <b>HBA</b>, using EEG recordings and spectra.
# 
# A previous notebook, [HMS 2024 - Brain Clusters](https://www.kaggle.com/code/dan3dewey/hms-2024-brain-clusters), looked at general properties of the training targets (the HBA votes/probabilities) including the k-means clustering of the 6-dimension probability vectors of the HBA samples. 
# 
# This notebook continues by looking at the spectrograms, creating simple features, and using them in a multiclass (clusters) classifier.

# %%
# Version history
#       LB /"CV",Train
#  v6 2.42 /3.00  Worst case: assign clusters randomly to the samples.
# v17     Processing scheme for the middle 4s of the spectrograms for a sub id:
#           average the two middle 2s spectra, divide by a reference spectrum,
#           calculate the mean and median, and divide by the mean.
#           smooth by n with a rolling window.
#         Created one large plot with overplotting of ~450 x 4 of these spectra; 
#         color coding by cluster (for the 6 basic clusters) shows some variation.
# v18     Using the spectrogram processing, create features from the spectrograms
#         and use them to fit cluster id with a Random Forest model.
# v20 1.74 /---- Training overfitting gives 0.37 on X sized 354, clust=8, smooth=7.
# v21 1.72 /---- Add mean/median for each of the "LL","RL","LP","RP" spectra.
# v23 1.56 /1.58 clusts=6, smooth=7, leaf_nodes=4*clusts, features=0.5, samples=0.7
# v24     Do the log10() before the smoothing and downsample of spectra.
#     1.64 /1.74,1.03
# v26     "Tamed" the cluster center loc.s/prob.s for best validation KL --
#         linear mix between center values and all 1/6, set by tamefac = 0.5
#     1.01 /1.18(tamed),1.14(not tamed)
# v27     Scan for the best tamed fraction (same for all clusters) - expect ~ v26
#     0.98 /1.18,0.88  <-- all tamed, clusts=6 width=7
# v28 0.99 /1.19,0.79  <-- all tamed, clusts=*8* width=7
# v29 0.95 /1.17,0.84  <-- all tamed, clusts=6 width=*5*
# v30 0.99 /1.16,0.82  <-- all tamed, clusts=6 width=*3*
# v31 0.98 /1.16,0.68  <-- all tamed, clusts=*10* width=*5*
# v32 ---- /1.17,0.83  <-- all tamed, clusts=6 width=*5*   Added the lowest freqs too.
# v33 0.96 /1.14,0.82  <-- indiv tamed, clusts=6 width=*5* 
# v34 0.95 /1.18,0.79  <-- indiv tamed, clusts=6 width=*5*  * Added LR features, blur=0.7*
# v35 0.96 /1.21,0.71  <-- indiv tamed, clusts=*9* width=*5*   with LR features, blur=0.7*
# v36 0.94 /1.13,1.05  <--   " ", clusts=*9* width=*5* , LR features(0.7), x5 samples
# v37 0.95 /1.14,1.06  <--   " ", clusts=*9* width=*5* , LR-no means,l1,0.42, x5 samples
# v38     Adjust the RForest hyper parameters roughly, got e.g. min leaf = 3, ...
#     0.95 /1.04,0.29  <--   " ", clusts=*9* width=*5* , LR-no means,l1,0.42, x5 samples
# v39     Use "soft" cluster assignment: predicted probs = RF proba-weighted average
#         of the cluster centers, sharpened by a power and tamed toward the mean probs;
#         power and tame fraction are chosen by validation KL.


# %% [markdown]
# #### Key Hyper-Hyper parameters

# %%
# For target classes creation:
NUM_CLUSTS = 9      # 6 to 10

# For feature generation:
# - include LR features
SMOOTH_WIDTH = 5    # Odd>1: 3,5,7,9,...

# Directory prefix for the data
above_dir = "../input/hms-harmful-brain-activity-classification/"
# or, offline, use my local directory
##above_dir = "D:/Kaggle/input/hms-harmful-brain-activity-classification/"

# %% [markdown]
# <HR>
#     
# ## Things To Use

# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# For k-means
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

# Use this for parquet: https://arrow.apache.org/docs/python/parquet.html 
import pyarrow
import pyarrow.parquet as pq
import pyarrow.dataset as pads

# Simple random forest model:
from sklearn.ensemble import RandomForestClassifier

# Logistic Regression (to add features)
from sklearn.linear_model import LogisticRegression

# %% [markdown]
# #### Functions, Etc.

# %%
# Define these since they get used a lot
HBA_number = 6
HBA_names = ["seizure", "lpd", "gpd", "lrda", "grda", "other"]
HBA_expert_names = ["Seizure","LPD","GPD","LRDA","GRDA","Other"]
iHBA_of_expert = {"Seizure":0,"LPD":1,"GPD":2,"LRDA":3,"GRDA":4,"Other":5}
HBA_votes = ["seizure_vote", "lpd_vote", "gpd_vote",
             "lrda_vote", "grda_vote", "other_vote"]
HBA_probs = ["seizure_prob", "lpd_prob", "gpd_prob",
             "lrda_prob", "grda_prob", "other_prob"]
the4chains = ["LL","RL","LP","RP"]

# Output format for arrays
np.set_printoptions(precision=6, suppress=True)

# %%
def kld_score(solution, submission):
    '''
    Calculate the average KL divergence score.
    Ignores the "row id" assumed in the first column.
    '''
    sumsum = 0.0
    # Go through the probabilities
    for prob_col in solution.columns.values:
        sumsum += np.nansum(-1.0*solution[prob_col] *
                        np.log(submission[prob_col] / solution[prob_col]))
    return sumsum/(len(solution))

# %%
def read_hms_meta():
    '''
    Read in the train.csv and test.csv files.
    Add total_vote, _prob columns, and vote entropy to train_meta.
    Add extra cols to test to allow the same processing as train:
        eeg[spectro]_sub_id, eeg[spectro]_label_offset_seconds, label_id
    Make various plots of the train_meta values.
    '''

    # Read the test meta data
    test_meta = pd.read_csv(above_dir+"test.csv")
    test_meta_len = len(test_meta)
    print("Test has length", test_meta_len)
    # Add columns to allow similar train/test processing:
    test_meta["eeg_sub_id"] = 0
    test_meta["eeg_label_offset_seconds"] = 0.0
    test_meta["spectrogram_sub_id"] = 0
    test_meta["spectrogram_label_offset_seconds"] = 0.0
    test_meta["label_id"] = test_meta.eeg_id
    # Can decide to replace the not-real test with training data instead
    if test_meta_len > 1:
        REAL_TEST = True
    else:
        REAL_TEST = False
        print("  --> not the real LB test data.\n")
        # Replace the test_meta?
        pass
  
    # Read the train meta data
    train_meta = pd.read_csv(above_dir+"train.csv")
    train_meta_len = len(train_meta)
    print("Train has length", train_meta_len, " with:")
    
    # Add a total_vote column
    train_meta["total_vote"] = ( train_meta["seizure_vote"] +
                    train_meta["lpd_vote"] + train_meta["gpd_vote"] +
                    train_meta["lrda_vote"] + train_meta["grda_vote"] +
                                    train_meta["other_vote"] )
    # Add a max_vote column (i.e. number of votes in the expert consensus)
    train_meta["max_vote"] = np.max(np.array([train_meta["seizure_vote"] ,
                    train_meta["lpd_vote"] , train_meta["gpd_vote"] ,
                    train_meta["lrda_vote"] , train_meta["grda_vote"] ,
                    train_meta["other_vote"]]), axis=0)
    
    # Show various unique numbers
    for this_col in ["label_id","eeg_id","spectrogram_id",
                     "patient_id","total_vote"]:
        print("   ", len(train_meta[this_col].unique()),
            "unique "+this_col+" values.")
    
    # Look at the total votes values:  1 to 28 with missing 8 and 9
    print("\nHistogram of the total votes")
    plt.figure(figsize=(6,3))
    plt.hist(train_meta["total_vote"],bins=55,log=True)
    plt.title("Histogram of Total Votes")
    plt.show()
    
    # Distribution of the "Expert consensus" for less/more than 9 votes
    allvt = train_meta.expert_consensus.value_counts()
    less9 = train_meta[train_meta["total_vote"] < 9].expert_consensus.value_counts()
    more9 = train_meta[train_meta["total_vote"] > 9].expert_consensus.value_counts()
    vnot3 = train_meta[train_meta["total_vote"] != 3].expert_consensus.value_counts()
    ##print("Counts for votes less than 9:\n",less9[allvt.index])
    ##print("\nCounts for votes more than 9:\n",more9[allvt.index])
    ##print("\nCounts for votes not equal to 3:\n",vnot3[allvt.index])
    
    # Create _prob values from the _vote values
    print("\nHistograms of the probabilites of the different HBAs:")
    print("   (note that the large Prob=0 bin is not included.)")
    for col_pre in HBA_names:
        train_meta[col_pre + "_prob"] = (train_meta[col_pre + "_vote"] / 
                                     train_meta["total_vote"] )
        # Show the probability histogram for each type
        if False:
            plt.figure(figsize=(6,1.5))
            plt.hist(train_meta[col_pre + "_prob"],bins=20,range=(0.02,1))
            plt.ylim(0,len(train_meta)/5)
            plt.title("Histogram of   "+col_pre+"_prob")
            plt.show()
        
    # Calculate the entropy for each row (~ amount of vote variation)
    print("Calculating voting entropy values ...")
    def calc_entropy(row):
        the_probs = np.clip(row[16:21+1].values.astype(float), 1.e-8,1.0)
        return np.nansum(the_probs * -1*np.log(the_probs))
    # Add an entropy column
    train_meta["entropy"] = train_meta.apply(calc_entropy, axis=1)
    
    return train_meta, test_meta


# %%
def prob_prob_scatter(name1, name2, probs2plot, clust_ids, iclust_order=[0]):
    '''
    Make a prob1 vs prob2 scatter plot.
    - name1, name2 are 2 of the 6 HBA expert_consensus labels.
    - probs2plot is 6-column dataframe, e.g., train_meta[HBA_probs]
    - clust_ids is an array of cluster id integers, e.g., train_meta["clust_id"]
    Include an x at the cluster centers in the chosen axes.
    Use sqrt scaling to emphasize lower values.
    External: HBA_probs, iHBA_of_expert[ ], clust_centers
    '''
    # Color-code the vectors by their k-means label, this is in HBA order
    hba_clrs = ["orange","blue","red","black","green","purple",
              "green","red","blue","orange"]  # up to 10 clusters
    if len(iclust_order) > 2:
        # adjust the colors to the cluster order
        kmclrs = hba_clrs.copy()
        for iord, iclust in enumerate(iclust_order):
            kmclrs[iclust] = hba_clrs[iord]
   
    clstclrs = []
    for ilab in clust_ids:
        clstclrs.append(kmclrs[ilab])
        
    ixax = iHBA_of_expert[name1]
    iyax = iHBA_of_expert[name2]
    lenprob = len(probs2plot)
    plt.figure(figsize=(5,5))
    plt.scatter(np.sqrt(probs2plot[HBA_probs[ixax]]) + 
                0.04*(np.random.rand(lenprob)-0.5),
            np.sqrt(probs2plot[HBA_probs[iyax]]) + 
                0.04*(np.random.rand(lenprob)-0.5),
           s=3, c=clstclrs, alpha=0.02)
    # Add the centers
    for iclust in range(0,len(clust_centers)):
        plt.plot(np.sqrt([clust_centers[iclust,ixax]]),
                 np.sqrt([clust_centers[iclust,iyax]]),
                 c=kmclrs[iclust],marker="x",markersize=15)
    plt.xlabel("sqrt( "+name1+" )")
    plt.ylabel("sqrt( "+name2+" )")
    plt.show()
    return kmclrs  # returns cluster colors appropriate for iclust

# %%
def assemble_features(meta_frame, traintest="train", smooth_width=5,
                     SHOW_PLOT=True):
    '''
    Create a dataframe of spectrogram features from the meta_frame rows.
    Will include clust_id (i.e, the y) if it is in the input meta_frame.
    Assumes these are available: above_dir, num_clusts
    '''
    # The frequencies and general trend (for normalization)
    freqs = np.array(range(100))*0.19525 + 0.59
    spect_trend = 150.0/(1.0**2.3+freqs**(2.3))
    # freqs are only used for plotting from here on
    freqs[0] = 0.0   # separate the (unsmoothed) first bin from others
    # Extend the trend to 4 copies
    freqs4 = np.array(4*list(freqs))
    spect_trend4 = np.array(4*list(spect_trend))
    if SHOW_PLOT:
        plt.figure(figsize=(10,8))
    # Go through the rows and extract the features from spectrogram
    feats_frame=[]
    last_spectro_id_str = "starting"
    for irow in meta_frame.index:
        this_row = meta_frame.loc[irow]
        # Get this row's spectrogram (could save last spectro_id_str, skip read if same)
        spectro_id_str = str(int(this_row.spectrogram_id)) # make sure int
        if spectro_id_str != last_spectro_id_str:
            spectro_file = above_dir+traintest+"_spectrograms/"+spectro_id_str+".parquet"
            pads_spectro = pads.dataset(spectro_file)
            this_spectro = pads_spectro.to_table().to_pandas()
        last_spectro_id_str = spectro_id_str
        # the offset into the spectro
        loc_offset = int(this_row.spectrogram_label_offset_seconds/2)
        # The average of middle 2 rows and divided by the spectral trend
        # Skip first column, the rest include 100 each for "LL","RL","LP","RP"
        middle4s = ((this_spectro.iloc[loc_offset+149, 1:] +
                    this_spectro.iloc[loc_offset+150, 1:])/
                        (2.0*spect_trend4)) # 4 copies of trend
        # Clip and clean the values of 0s, etc.
        middle4s = np.clip(middle4s,0.001,1000.0)
        middle4s = middle4s.replace([np.nan, -np.inf, np.inf], 0.001)
        # Get means/medians for overall and the individual "LL","RL","LP","RP"
        spect_mean = np.mean(middle4s)  # over all 4 spectra
        spect_median = np.median(middle4s)
        the4means=[]
        the4medians = []
        for ispec in range(4):
            ibeg = ([0,100,200,300])[ispec]
            iend = ibeg+100
            the4means.append(np.mean(middle4s[ibeg:iend]))
            the4medians.append(np.median(middle4s[ibeg:iend]))
        # Scale all the spectra relative to the 4-spectra mean
        # and take the log10
        middle4spre = np.log10(middle4s / spect_mean)
        # smooth the logged values with smooth_width
        middle4s = middle4spre.rolling(smooth_width, min_periods=smooth_width, 
                                        center=True, closed=None).mean()
        # Set the values of the first few in each spectrum to unsmoothed
        for ioff in range(0, 400, 100):
            for ibin in range(int((smooth_width-1)/2)):  # assumes width is odd
                middle4s[ibin+ioff] = middle4spre[ibin+ioff]
        # downselect by the smoothing width; include the first value too
        baseinds = np.insert(np.arange(int((smooth_width-1)/2), 100, smooth_width),
                             0, 0)
        select_inds = np.concatenate((baseinds,100+baseinds,
                                      200+baseinds,300+baseinds))
        freqs4ds = freqs4[select_inds]
        middle4sds = middle4s[select_inds]
        # Create a single feature-frame row
        these_feats = middle4sds.to_frame().T  # already log10()
        # Include log10()s of means/medians
        spect_mean = np.log10(spect_mean)
        spect_median = np.log10(spect_median)
        the4means = np.log10(the4means)
        the4medians = np.log10(the4medians)
        these_feats["Mean"] = spect_mean
        these_feats["Median"] = spect_median
        for ispec in range(4):
            these_feats[the4chains[ispec]+"mean"] = the4means[ispec]
            these_feats[the4chains[ispec]+"median"] = the4medians[ispec]
        # Include the clust_id (the y) if present
        if "clust_id" in meta_frame.columns:
            these_feats["clust_id"] = this_row.clust_id
        # If this is the first row make it the features frame
        if len(feats_frame) == 0:
            feats_frame = these_feats.copy()
        else:
            feats_frame = pd.concat([feats_frame, these_feats])
        # Show progress
        if len(feats_frame) % 100 == 0:
            print("... {} done...".format(len(feats_frame)))
        #
        # Can make a summary plot of all features, if desired
        if SHOW_PLOT:
            this_clr = "blue"
            title_start = "Middle-4s Feature Values"
            plt.title(title_start+" (smooth={})".format(smooth_width))
            if "clust_id" in meta_frame.columns:
                this_clust = this_row.clust_id
                this_clr = kmclrs[this_clust]
                plt.title(title_start+" (color-coded by the "+
                          "{} clusters, smooth={})".format(
                              num_clusts, smooth_width))
            the_alpha = np.clip(0.05*350/len(meta_frame),0.003,0.5)
            plt.plot(freqs4ds+smooth_width*0.15*(np.random.rand(len(freqs4ds))-0.5),
                     middle4sds, ".",c=this_clr,markersize=10,alpha=the_alpha)
            # The means too - the 4 chain means
            plt.plot(-1.2+smooth_width*0.15*(np.random.rand(4)-0.5),
                     the4means+(0.0*(np.random.rand(4)-0.5)), ".",
                     c=this_clr,markersize=10,alpha=the_alpha)
            plt.ylim(-1.5,1.5)
            plt.xlabel("<-- Means are band < 0"+20*" "+"Frequency Bands (Hz)"+50*" ")
            plt.ylabel("Amplitude (/ref-spectrum, /mean, and smoothed n={})".format(
                                            smooth_width))
    if SHOW_PLOT:
        plt.savefig("middle4s_"+traintest+"_features.png")
        plt.show()
    # Return the features (including clust_id if given)
    return feats_frame.reset_index().drop(columns=["index"])
   

# %%
def find_best_tamed_kl():
    '''
    Adjust the taming fraction for each cluster center to optimize KL
    Assumed inputs in environment:
        submission, pred_ids, solution
    Assumed useful values available:
        clust_centers, NUM_CLUSTS, HBA_number, HBA_votes
    '''
    # Adjust, tame, the cluster_center values?
    mean_all_probs = np.array([0.208319, 0.132120, 0.128532,
                           0.138913, 0.179294, 0.212822])
    # Start all with the mean values, i.e., tamed_frac=0.
    tamed_fracs = 0.0 * np.ones(NUM_CLUSTS)
    tamed_centers = clust_centers.copy()
    for iclust in range(NUM_CLUSTS):
        tamed_centers[iclust,:] = mean_all_probs
    # Go through the clusters
    for iclust in range(NUM_CLUSTS):
        last_kl = 10.0
        # Find the best overall tame frac for this cluster
        for this_frac in np.arange(0.0, 1.0, 0.05):
            tamed_fracs[iclust] = this_frac
            this_cent = (tamed_fracs[iclust]*clust_centers[iclust,:] +
                         (1.0-tamed_fracs[iclust])*mean_all_probs)
            tamed_centers[iclust,:] = this_cent

            # Put the probs into the submission column by column
            for iprob in range(HBA_number):
                this_col_probs = tamed_centers[: , iprob]
                submission[HBA_votes[iprob]] = this_col_probs[pred_ids]
            # Evaluate the KL divergence using predicted cluster ids
            this_kl = kld_score(solution, submission)
            if (this_kl < last_kl):
                best_fracs = tamed_fracs.copy()
                best_centers = tamed_centers.copy()
                last_kl = this_kl
            else:
                # restore the best one
                tamed_fracs[iclust] = best_fracs[iclust]
                tamed_centers[iclust, :] = best_centers[iclust, :]
                break
                # go to the next cluster
        #
    # done with all clusters
    return best_fracs, best_centers

# %% [markdown]
# <HR>
# 
# ## Get (and look at) the Meta Data

# %%
# Read in the meta data, routine also looks at the train values
train_meta, test_meta = read_hms_meta()

# %%
# Look at the values of the spectro sub id
##print("Spectrogram_sub_id unique values:",
##            np.sort(train_meta.spectrogram_sub_id.unique()))
# Show a histogram
plt.figure(figsize=(5,2))
plt.hist(train_meta["spectrogram_sub_id"],bins=55,log=True)
plt.title("Histogram of spectrogram_sub_id")
plt.show()

# Look at the values of the eeg sub id
##print("eeg_sub_id unique values:",np.sort(train_meta.eeg_sub_id.unique()))
# Show a histogram
plt.figure(figsize=(5,2))
plt.hist(train_meta["eeg_sub_id"],bins=55,log=True)
plt.title("Histogram of eeg_sub_id")
plt.show()

# %% [markdown]
# <HR>
# 
# ## Clustering of HBA Probability Vectors

# %%
# Choose the number of clusters
num_clusts = NUM_CLUSTS   # 6 to 10

# Choose which rows to use for clustering
# Use all the HBA samples:
##prob_vectors = train_meta.loc[(train_meta.eeg_sub_id > -1), HBA_probs]
#    or
# Use one (or more) per eeg by selecting some of the sub_id values.
clust_rows_bool = (((train_meta.eeg_sub_id < 56) &
                     (train_meta.eeg_sub_id % 7 == 6)) |
                    # Use about 1/2 of the eeg_sub_id=0 ones
                    (train_meta.eeg_sub_id == 0) &
                      (train_meta.eeg_id%4 < 2)) # include odd and even eeg_ids
# Has 16635:  8055 non-zero eeg_sub_ids and 8580 ones that are 0.

# %%
# Get the vectors and run k-means clustering on them
prob_vectors = train_meta.loc[clust_rows_bool, HBA_probs]

# Look at the votes distribution of the selected prob_vectors
print("\nUsing {} HBA samples for clustering.".format(len(prob_vectors)))
print("These include {} unique eeg_ids".format(
                train_meta.loc[clust_rows_bool, "eeg_id"].nunique()),
                "and {} unique patient ids.".format(
                train_meta.loc[clust_rows_bool, "patient_id"].nunique()))
plt.figure(figsize=(6,3))
plt.hist(train_meta.loc[clust_rows_bool,"total_vote"],bins=100,log=True)
plt.title("Histogram of total_vote in HBA samples clustered")
plt.show()
    
# Find the centers for a specified number of clusters 
prob_array = np.array(prob_vectors)
kmeans = KMeans(n_clusters = num_clusts, init = 'k-means++', n_init = 10,
                    max_iter = 300, random_state=None)
kmeans.fit(prob_array)

# Get the cluster center coord.s/probs
clust_centers = kmeans.cluster_centers_
# They are very close to normalized, make them closer  :)
for iclust in range(HBA_number):
    clust_centers[iclust ,:] = (clust_centers[iclust ,:]/
                            np.sum(clust_centers[iclust ,:]))

# Map iclust to standard order of the HBAs followed by hybrids
iclust_of_order = []
# The first dim_centers (6) are the close-to-unit vectors
for icol in range(HBA_number):
    iclust_of_order.append(np.argmax(clust_centers[:,icol]))
# Add the remaining num_clusts-HBA_number (3) in order by max component
# index ordered by largest to smallest
clust_by_max = np.argsort(-1*np.max(clust_centers,axis=1))
# Add the last ones:
for iord in range(HBA_number,num_clusts):
    iclust_of_order.append(clust_by_max[iord])    
    
# Make some names for the clusters in standard order
kmnames = HBA_expert_names.copy()
for ihyb in range(1,(num_clusts-HBA_number)+1):
    kmnames.append("Hybrid-"+str(ihyb))


# %%
# Not sure what is the best way to view the cluster results.
# Try scatter plots of pairs of the HBA probs, use sqrt scaling.

# Use all the data: assign the clusters to all of the train_meta
train_meta["clust_id"] = kmeans.predict(np.array(train_meta[HBA_probs]))

all_probs = train_meta[HBA_probs]
all_ids = train_meta["clust_id"]

if True:
    kmclrs = prob_prob_scatter("Seizure","GPD", all_probs, all_ids, iclust_of_order)
    
    kmclrs = prob_prob_scatter("LPD","GRDA", all_probs, all_ids, iclust_of_order)

    kmclrs = prob_prob_scatter("LRDA","Other", all_probs, all_ids, iclust_of_order)

# List the centers in order with other information
# Counts in the clusters
clust_counts = train_meta.clust_id.value_counts()
##print("   Seizure","  LPD","     GPD","     LRDA","    GRDA","    Other",
##     " Clust name","  color"," Number in clust")
##for iord, iclust in enumerate(iclust_of_order):
##    print(clust_centers[iclust,:]," {} {:10} {:6}  {:5}".format(
##        iclust, kmnames[iord],kmclrs[iclust],clust_counts[iclust]))
    
# And/or show them graphically
for iord, iclust in enumerate(iclust_of_order):
    ##print(clust_centers[iclust,:]," {} {:10} {:6}  {:5}".format(
    ##    iclust, kmnames[iord],kmclrs[iclust],clust_counts[iclust]))
    if iord == 0: print("The close-to-unit-vector cluster centers:")
    if iord == 6: print("The Hybrid cluster centers:")
    plt.figure(figsize=(5,1))
    plt.bar(HBA_expert_names, clust_centers[iclust,:],color=kmclrs[iclust])
    plt.ylim(-0.01,1.01)
    plt.title(kmnames[iord]+"  kmclust={} has {} samples".format(
        iclust,clust_counts[iclust]), size='medium')
    if iord < 5: plt.xticks([])
    plt.show()

# %% [markdown]
# #### KL score using cluster centers

# %%
# Create a 'solution' of actual probabilities from the training data
solution_train = train_meta[["eeg_id"] + HBA_votes]
# In solution_train replace the _votes values with probabilities
for col_pre in HBA_names:
    solution_train.loc[:, col_pre + "_vote"] = train_meta[col_pre + "_prob"]

# Create a 'submission' of the cluster probabilities
submission_train = solution_train.copy()
# Use clust_ids to select the correct clust_probs vector
clust_ids = train_meta["clust_id"]
if False:
    # How bad could it be? (with random clusters assigned) Ans: Bad ~ 3.0
    clust_ids = np.random.choice(9, size=len(train_meta),
                             replace=True, p=None)
# Put the probs into the submission
for iprob in range(HBA_number):
    this_col_probs = clust_centers[: , iprob]
    submission_train[HBA_votes[iprob]] = this_col_probs[clust_ids]

# Evaluate the KL divergence when predictions are the cluster probs
print("Score if HBA samples are correctly assigned cluster prob.s:",
      np.round(kld_score(solution_train, submission_train),4))

# %% [markdown]
# <HR>
# 
# ## Look at the Spectrograms

# %%
# Choose a smoothing window (which is also the downsample factor)
smooth_width = SMOOTH_WIDTH   # Here smooth_width is just for looking,
#                             # can be another value different from SMOOTH_WIDTH

# Choose what rows to show spectra from,
# start with the ones from clustering
spectro_meta = train_meta[clust_rows_bool].copy()
# Downsample them by a factor
every_nth = 37


# Frequencies of the 100 bins are LL_0.59 LL_0.78 LL_0.98 . . . LL_19.73 LL_19.92
# Roughly freq.s = 0.59 + 0.19525*ibin
freqs = np.array(range(100))*0.19525 + 0.59

# The signal amplitudes vary with frequency - divide out a general trend.
# Scaled it so the meadian(all_me[di]ans) is near 1.0
# Power-law with blowup tamed near 0.
spect_trend = 150.0/(1.0**2.3+freqs**(2.3))
# Exponential with "slope" by eye, lacks increase near 0.
##spect_trend = 5.0*np.exp(-1.0*freqs/5.0)

# %%
# Make one figure with selected spectra overplotted
plt.figure(figsize=(10,8))

# Go though the desired rows
all_medians = []
all_means = []
all_clusts = []
print("Plotting {} x 4 processed spectra".format(int(len(spectro_meta)/every_nth)))
for ilocrow in range(0,len(spectro_meta),every_nth):
    this_row = spectro_meta.iloc[ilocrow]
    this_clust = this_row.clust_id
    if True:
        # Get this row's spectrogram
        spectro_id_str = str(this_row.spectrogram_id)
        spectro_file = above_dir + "train_spectrograms/"+spectro_id_str+".parquet"
        pads_spectro = pads.dataset(spectro_file)
        this_spectro = pads_spectro.to_table().to_pandas()
        # offset into the spectro
        loc_offset = int(this_row.spectrogram_label_offset_seconds/2)
        # Look at the 4 spectra from the average of the 2 center 2s bins
        # fyi, the4chains = ["LL","RL","LP","RP"]
        for ispec in range(4):
            ibeg = ([1,101,201,301])[ispec]
            iend = ibeg+100
            # The average of middle two spectra, relative to the trend
            middle4s = (this_spectro.iloc[loc_offset+149, ibeg:iend] +
                    this_spectro.iloc[loc_offset+150, ibeg:iend])/(2.0*spect_trend)
            # Clean the values of 0s, etc.
            middle4s = np.clip(middle4s,0.001,1000.0)
            middle4s = middle4s.replace([np.nan, -np.inf, np.inf], 0.001)
            # The log10(mean) and log10(median) -- mean/median before the log
            spect_mean = np.log10(np.mean(middle4s))
            all_means.append(spect_mean)
            spect_median = np.log10(np.median(middle4s))
            all_medians.append(spect_median)
            all_clusts.append(this_clust)
            # Take the log10 of the trended spectral values
            middle4s = np.log10(middle4s)
            # - - - All spectro values are log10() after this point.
            # Further ratio it to its mean (or median) - subtract logs
            middle4spre = middle4s - spect_mean
            # smooth it with smooth_width (5 gives ~ 1 Hz)
            middle4s = middle4spre.rolling(smooth_width, min_periods=smooth_width, 
                                        center=True, closed=None).mean()
            # Set the values of the first few to unsmoothed
            for ibin in range(int((smooth_width-1)/2)):  # assumes width is odd
                middle4s[ibin] = middle4spre[ibin]
            plt.plot((freqs), middle4s, c=kmclrs[this_clust],lw=3,alpha=0.01)
    # Show progress
    if (ilocrow/every_nth + 1) % 100 == 0:
        print("... {} done...".format(int(ilocrow/every_nth)+1))

# Show the 1 line and locations of every smooth_width frequency for reference
plt.plot([0.0,20.0],[0.0,0.0],c='black',lw=3,alpha=0.2)
# Down selected freqs - include the first one (it won't be smoothed)
downsel_freqs = np.insert(freqs[int((smooth_width-1)/2):100:smooth_width], 0, freqs[0])
plt.plot(downsel_freqs, len(downsel_freqs)*[0.0],'.k')
plt.ylim(-1.0,1.0)  # log already taken
plt.xlim(0.0,20.5)
plt.title("Middle-4s Spectra (color-coded by the {} clusters, smooth={})".format(
                                                num_clusts, smooth_width))
plt.xlabel("Frequency (Hz)")
plt.ylabel("log10[] Amplitude (/ref-spectrum, /mean, and smoothed n=3) ]")
plt.savefig("middle4s_spectra.png")
plt.show()

# %%
# Mean and Median (before the divide by mean or median)

print("\nMedian of the Means(below): {:.4f}".format(np.median(all_means)))
plt.figure(figsize=(6,2))
plt.hist(np.clip(all_means,-2.0,2.0),bins=100)
plt.xlim(-2.05,2.05)
plt.xlabel("Mean")
plt.title("Histogram of the Means of the log(Spectra/Ref-spect)")
plt.show()

print("\nMedian of the Medians(below): {:.4f}".format(np.median(all_medians)))
plt.figure(figsize=(6,2))
plt.hist(np.clip(all_medians,-2.0,2.0),bins=100)
plt.xlim(-2.05,2.05)
plt.xlabel("log10( Median )")
plt.title("Histogram of the Medians of the log(Spectra/Ref-spect)")
plt.show()

# Scatter plot show the means are greater than or equal to the medians: right skewed.
mmclrs = []
for ilab in all_clusts:
    mmclrs.append(kmclrs[ilab])
plt.figure(figsize=(3,3))
plt.scatter(all_medians, all_means, s=2,c=mmclrs,alpha=0.3)
plt.xlim(-1.,1); plt.ylim(-1.,1)
plt.xlabel("Median")
plt.ylabel("Mean")
plt.show()

# %% [markdown]
# <HR>
# 
# ## Generate Train and Validation Features
# Using the spectrograms.

# %% [markdown]
# #### The Training Spectro Features

# %%
# The train meta frame for features
# use the cluster selection, downsampled
Xy_train_meta = (train_meta[clust_rows_bool])[::4].copy()  # 23 or 4
Xy_train_meta = Xy_train_meta.reset_index().drop(columns=["index"])
print("Number of samples used for training =",len(Xy_train_meta))

# Get its features
Xy_train_feats = assemble_features(Xy_train_meta, traintest="train",
                            smooth_width=SMOOTH_WIDTH, SHOW_PLOT=False)
# Save the dataframes
Xy_train_meta.to_csv("Xy_train_meta.csv", header=True,
                    index=False, float_format='%.6f')
Xy_train_feats.to_csv("Xv_train_feats.csv", header=True,
                    index=False, float_format='%.6f')

# %%
# The training features
Xy_train_feats

# %% [markdown]
# #### The Validation Spectro Features

# %%
# For validation, select similar-to-clustering ones but no overlap
# Use one (or more) per eeg by selecting some of the sub_id values.
valid_rows_bool = (((train_meta.eeg_sub_id < 21) &
                    (train_meta.eeg_sub_id % 7 == 4)) |
                    # Use the other 1/2 of the eeg_sub_id=0 ones
                    (train_meta.eeg_sub_id == 0) &
                    (train_meta.eeg_id%4 > 1)) # include odd and even eeg_ids
# Has 17485:  8976 non-zero eeg_sub_ids and 8509 ones that are 0.

# The Validation meta frame for features
Xy_valid_meta = (train_meta[valid_rows_bool])[::19].copy()   # 47 or 19
Xy_valid_meta = Xy_valid_meta.reset_index().drop(columns=["index"])
print("Number of samples used for Validation =",len(Xy_valid_meta))

# Get its features
Xy_valid_feats = assemble_features(Xy_valid_meta, traintest="train",
                            smooth_width=SMOOTH_WIDTH, SHOW_PLOT=False)
# Save the dataframes
Xy_valid_meta.to_csv("Xy_valid_meta.csv", header=True,
                    index=False, float_format='%.6f')
Xy_valid_feats.to_csv("Xv_valid_feats.csv", header=True,
                    index=False, float_format='%.6f')

# %%
# The validation features
Xy_valid_feats

# %% [markdown]
# ### Add Logistic Regression proba values as Features

# %%
# LogisticRegression(penalty='l2', *, dual=False, tol=0.0001, C=1.0, fit_intercept=True,
#              intercept_scaling=1, class_weight=None, random_state=None, solver='lbfgs',
#              max_iter=100, multi_class='auto', verbose=0, warm_start=False,
#              n_jobs=None, l1_ratio=None)

# Train the LR model

X = Xy_train_feats.drop(columns=["clust_id"])
y = Xy_train_feats.clust_id

# Don't include the last 10 columns - the mean/medians
Xlr = X.drop(columns=X.columns[-10:])

lrmodel = LogisticRegression(penalty='l1', C=0.9, solver='saga', max_iter=1500,
                                multi_class='multinomial', # ovr or multinomial
                                n_jobs=-1).fit(Xlr,y)

print("\nLR model score for X,y = {:.1f}%\n".format(100*lrmodel.score(Xlr, y)))

# Cute figure of the coefficients. Means and medians are on the right side.
plt.figure(figsize=(8,4))
plt.plot(lrmodel.coef_.T,'-',alpha=0.5)
plt.plot(lrmodel.coef_.T,'.',alpha=1.0)
plt.title("Logistic Regression coefficients (colored by cluster)")
plt.show()

# %%
# Include a blur so they don't overpower the other features
lrblur = 0.42 # 0.60:1.134  0.50:1.139 0.45:1.134 0.42:1.11 0.40:1.124 0.35:1.127 0.30:1.153

# Add these values as new columns in Xy_train_wLRfeats
Xy_train_wLRfeats = Xy_train_feats.copy()
X = Xy_train_feats.drop(columns=["clust_id"])
Xlr = X.drop(columns=X.columns[-10:])
lrprobas = lrmodel.predict_proba(Xlr)
for iadd in range(NUM_CLUSTS):
    Xy_train_wLRfeats["lr"+str(iadd)] = (lrprobas[: , iadd] +
                            lrblur*(np.random.rand(len(lrprobas))-0.5))

# Add these values as new columns in Xy_valid_wLRfeats
Xy_valid_wLRfeats = Xy_valid_feats.copy()
X = Xy_valid_feats.drop(columns=["clust_id"])
Xlr = X.drop(columns=X.columns[-10:])
lrprobas = lrmodel.predict_proba(Xlr)
for iadd in range(NUM_CLUSTS):
    Xy_valid_wLRfeats["lr"+str(iadd)] = (lrprobas[: , iadd] +
                            lrblur*(np.random.rand(len(lrprobas))-0.5))

# Representative of the proba values
plt.figure(figsize=(6,3))
plt.hist(Xy_train_wLRfeats["lr0"],bins=50)
plt.show()

plt.figure(figsize=(6,3))
plt.hist(Xy_valid_wLRfeats["lr0"],bins=50)
plt.show()

# %% [markdown]
# <HR>
# 
# ## Train a Random Forest model

# %%
# RandomForestClassifier(n_estimators=100, *, criterion='gini', max_depth=None,
#    min_samples_split=2, min_samples_leaf=1, min_weight_fraction_leaf=0.0,
#    max_features='sqrt', # fraction of feat.s to consider when looking for best split
#                         # Note: the search for a split does not stop until
#                         # at least one valid partition of the node samples is found,
#                         # even if it requires inspecting more than max_features features.
#    max_leaf_nodes=None, min_impurity_decrease=0.0,
#    bootstrap=True, oob_score=False, n_jobs=None, random_state=None, verbose=0,
#    warm_start=False, class_weight=None, ccp_alpha=0.0,
#    max_samples=None, # fraction of samples from X used to train each estimator
#    monotonic_cst=None)

X = Xy_train_wLRfeats.drop(columns=["clust_id"])
y = Xy_train_wLRfeats.clust_id

ave_oob = []
nfits=5
for ifit in range(nfits):
    rfmodel = RandomForestClassifier(n_estimators=100,
                    ##max_leaf_nodes=int(scan_this*NUM_CLUSTS), # 1.096 for 9*
                    min_samples_leaf=3,
                    max_features=0.20,
                    max_samples=0.8,
                    oob_score=True, class_weight="balanced_subsample",
                    n_jobs=-1, verbose=0, random_state=None).fit(X,y)
    ave_oob.append(rfmodel.oob_score_)
    
# Show the feature importances
sort_inds = (rfmodel.feature_importances_.argsort())
plt.figure(figsize=(4,5))
plt.barh(rfmodel.feature_names_in_[sort_inds], rfmodel.feature_importances_[sort_inds])
plt.ylim(len(sort_inds)-25,len(sort_inds)+0.2)
plt.title("Feature Importances (top 25)")
plt.show()

print("\nRF model ave OOB score = {:.1f}% +/- {:.1f}".format(
        100*np.mean(ave_oob),100*np.std(ave_oob)))

print("\nRF model score for X,y = {:.1f}%\n".format(100*rfmodel.score(X, y)))

# %%
# Calculate the KL score for the train_meta

# Make and add the predicted clusters to Xy_train_meta
Xy_train_meta["pred_id"] = rfmodel.predict(Xy_train_wLRfeats.drop(columns=["clust_id"]))

# How high is the probability of the assigned (maximum prob) class for each X?
maxprobs_train = np.max(rfmodel.predict_proba(X),axis=1)
plt.figure(figsize=(6,2))
plt.hist(maxprobs_train, bins=20)
plt.xlim(0.,1.)
plt.title("Histogram of max(proba) for model-training samples")
plt.show()

# Create a 'solution' of actual probabilities from the Xy_train_meta
solution = Xy_train_meta[["eeg_id"] + HBA_votes]
# In solution replace the _votes values with probabilities
for col_pre in HBA_names:
    solution.loc[:, col_pre + "_vote"] = Xy_train_meta[col_pre + "_prob"]

# Create a 'submission' from the predicted cluster ids via clust_centers
submission = solution.copy()
pred_ids = Xy_train_meta["pred_id"] # putting clust_id gives the ideal value

# Calculate the KL score, include "taming" adjustments

best_fracs, best_centers = find_best_tamed_kl()

# Using the best_centers
# Put the probs into the submission column by column
for iprob in range(HBA_number):
    this_col_probs = best_centers[: , iprob]
    submission[HBA_votes[iprob]] = this_col_probs[pred_ids]
# Evaluate the KL divergence
this_kl = kld_score(solution, submission)
print("Tamed fractions:\n", best_fracs, "\nand centers:\n", best_centers)
print("\nKL from tamed centers: {:.4f}".format(this_kl))

# %% [markdown]
# #### Apply Model to Validation Data

# %%
# Make and add the predictions to Xy_valid_meta
Xy_valid_meta["pred_id"] = rfmodel.predict(Xy_valid_wLRfeats.drop(columns=["clust_id"]))
# For reference, randomly assign pred_ids to see zero-accuracy result
##Xy_valid_meta["pred_id"] = np.random.choice(num_clusts,
##                        size=len(Xy_valid_meta),replace=True, p=None)

# How high is the probability of the assigned (maximum prob) class for each X?
maxprobs_valid = np.max(rfmodel.predict_proba(
                    Xy_valid_wLRfeats.drop(columns=["clust_id"])),axis=1)
plt.figure(figsize=(6,2))
plt.hist(maxprobs_valid, bins=20)
plt.xlim(0.,1.)
plt.title("Histogram of max(proba) for validation samples")
plt.show()

# Create a 'solution' of actual probabilities from the Xy_valid_meta
solution = Xy_valid_meta[["eeg_id"] + HBA_votes]
# In solution replace the _votes values with probabilities
for col_pre in HBA_names:
    solution.loc[:, col_pre + "_vote"] = Xy_valid_meta[col_pre + "_prob"]

# Create a 'submission' template
submission = solution.copy()
pred_ids = Xy_valid_meta["pred_id"]

best_fracs, best_centers = find_best_tamed_kl()

# Using the best_centers
# Put the probs into the submission column by column
for iprob in range(HBA_number):
    this_col_probs = best_centers[: , iprob]
    submission[HBA_votes[iprob]] = this_col_probs[pred_ids]
# Evaluate the KL divergence
this_kl = kld_score(solution, submission)
print("Tamed fractions:\n", best_fracs, "\nand centers:\n", best_centers)
print("\nKL from tamed centers: {:.4f}".format(this_kl))
hard_kl = this_kl

# %% [markdown]
# #### Soft cluster assignment: proba-weighted cluster centers

# %%
def soft_cluster_probs(probas, power, frac):
    '''
    Combine the cluster centers weighted by the (sharpened) RF probas,
    then tame the result toward the mean of all probs by frac.
    '''
    mean_all_probs = np.array([0.208319, 0.132120, 0.128532,
                           0.138913, 0.179294, 0.212822])
    wts = probas**power
    wts = wts / np.sum(wts, axis=1, keepdims=True)
    # rfmodel.classes_ are the cluster ids 0,...,NUM_CLUSTS-1
    soft_probs = wts @ clust_centers[rfmodel.classes_, :]
    soft_probs = frac*soft_probs + (1.0-frac)*mean_all_probs
    return soft_probs / np.sum(soft_probs, axis=1, keepdims=True)

# Scan the power and tame fraction using the validation samples
valid_probas = rfmodel.predict_proba(Xy_valid_wLRfeats.drop(columns=["clust_id"]))
best_soft_kl = 10.0
for this_power in [0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 2.5, 3.0]:
    for this_frac in np.arange(0.50, 1.001, 0.05):
        soft_probs = soft_cluster_probs(valid_probas, this_power, this_frac)
        for iprob in range(HBA_number):
            submission[HBA_votes[iprob]] = soft_probs[:, iprob]
        this_kl = kld_score(solution, submission)
        if this_kl < best_soft_kl:
            best_soft_kl = this_kl
            best_power = this_power
            best_frac = this_frac
print("Soft clusters: best power = {}, frac = {:.2f}, KL = {:.4f}".format(
                best_power, best_frac, best_soft_kl))
print("  compared to KL from hard-assigned tamed centers: {:.4f}".format(hard_kl))
# Use the soft assignment if it is better
USE_SOFT = (best_soft_kl < hard_kl)

# %% [markdown]
# #### Scanning hyper parameters 'by hand'

# %%
# Do training fit and validation KL in a loop to chek hyper params.
if False:
    # Training X,y
    X = Xy_train_wLRfeats.drop(columns=["clust_id"])
    y = Xy_train_wLRfeats.clust_id
    # Create a 'solution' of actual probabilities from the Xy_valid_meta
    solution = Xy_valid_meta[["eeg_id"] + HBA_votes]
    # In solution replace the _votes values with probabilities
    for col_pre in HBA_names:
        solution.loc[:, col_pre + "_vote"] = Xy_valid_meta[col_pre + "_prob"]
    # Create a 'submission' template
    submission = solution.copy()

if False:   #for scan_this in [1,1,2,2,3,3,4,4,5,5,6,6]:
    rfmodel = RandomForestClassifier(n_estimators=100,
                    ##max_leaf_nodes=int(scan_this*NUM_CLUSTS), # 1.096 for 9*
                    min_samples_leaf=3,
                    max_features=0.20,
                    max_samples=0.8,
                    oob_score=True, class_weight="balanced_subsample",
                    n_jobs=-1, verbose=0, random_state=None).fit(X,y)
    print("\nRF model score for X,y = {:.1f}%".format(100*rfmodel.score(X, y)))
    # Make and add the predictions to Xy_valid_meta
    Xy_valid_meta["pred_id"] = rfmodel.predict(Xy_valid_wLRfeats.drop(
                                    columns=["clust_id"]))
    pred_ids = Xy_valid_meta["pred_id"]
    best_fracs, best_centers = find_best_tamed_kl()
    # Using the best_centers
    # Put the probs into the submission column by column
    for iprob in range(HBA_number):
        this_col_probs = best_centers[: , iprob]
        submission[HBA_votes[iprob]] = this_col_probs[pred_ids]
    # Evaluate the KL divergence
    this_kl = kld_score(solution, submission)
    ##print("Tamed fractions:\n", best_fracs, "\nand centers:\n", best_centers)
    print("KL from tamed centers: {:.4f}".format(this_kl))

# %% [markdown]
# <HR>

# %% [markdown]
# ## Create and Output the Test Predictions

# %%
# Assemble the submission with probabilites assigned by cluster id

# Generate the test features:
Xy_test_feats = assemble_features(test_meta, traintest="test",
                            smooth_width=SMOOTH_WIDTH, SHOW_PLOT=False)

# Add LR probas (Xy_test_feats has no clust_id, don't need to drop it)
Xy_test_wLRfeats = Xy_test_feats.copy()
Xlr = Xy_test_feats.drop(columns=Xy_test_feats.columns[-10:])
lrprobas = lrmodel.predict_proba(Xlr)
for iadd in range(NUM_CLUSTS):
    Xy_test_wLRfeats["lr"+str(iadd)] = (lrprobas[: , iadd] +
                            lrblur*(np.random.rand(len(lrprobas))-0.5))
    
# Use the RF model to assign cluster id predictions
pred_ids = rfmodel.predict(Xy_test_wLRfeats)

# Start submission with a dataframe of the eeg_id column from test_meta
test_submit = test_meta[["eeg_id"]].copy()
# Add "_vote" columns, initially all equal.
for new_col in HBA_votes:
    test_submit[new_col] = 1/HBA_number
# Put the best (validation) tamed cluster centers/probs into the submission
for iprob in range(HBA_number):
    this_col_probs = best_centers[: , iprob]
    test_submit[HBA_votes[iprob]] = this_col_probs[pred_ids]    
# Or use the soft cluster assignment
if USE_SOFT:
    test_probas = rfmodel.predict_proba(Xy_test_wLRfeats)
    soft_probs = soft_cluster_probs(test_probas, best_power, best_frac)
    for iprob in range(HBA_number):
        test_submit[HBA_votes[iprob]] = soft_probs[:, iprob]
    
print(test_submit)

# Output the file
test_submit.to_csv("submission.csv", header=True, 
                        index=False, na_rep='', float_format='%.6f')
# Look at the file
##!more submission.csv

# %% [markdown]
# <HR>
# ### The End
