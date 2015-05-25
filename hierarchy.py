import features
import utils
from scipy.cluster import hierarchy
from scipy.spatial.distance import pdist

DISTANCE_METRIC = 'cosine'
LINKAGE_METHOD = 'centroid'

def learn(dataset):
	return hierarchy.linkage(pdist(dataset, DISTANCE_METRIC),LINKAGE_METHOD,DISTANCE_METRIC)

def main():	
	dataset = utils.random_subset(features.load_dataset(), 100)
	hierarchy.dendrogram(learn(dataset))
	
if __name__ == "__main__":
	main()