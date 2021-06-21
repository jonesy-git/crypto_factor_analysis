from data import get_price_data

import numpy
from sklearn.decomposition import PCA, FactorAnalysis

if __name__ == "__main__":
    df = get_price_data('EUR', max_symbols=10)

    pca = PCA()
    pca.fit_transform(df.values)
    print(df.corr())
    print(numpy.linalg.eig(df.values))