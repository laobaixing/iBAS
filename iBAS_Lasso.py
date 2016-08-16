from sklearn.linear_model import LassoCV, ElasticNetCV
import pandas as pd
import numpy as np 

# define a lasso class for iBAS from LassoCV

class iBAS_Lasso(LassoCV):
    """
    This class evaluate the efficient of lasso;
    output the features selected by lasso;
    predict the independent set in the future if needed;
    
    This class get the data from iBAS. And directly output the result required by iBAS with one method
    getCoefs
    getMSE (mean square error)
    
    why class?
    getCoefs, getMSE may be used by many algorithm 
    
    In the future, try to use feature_selection class
    
    """
    
    # will raise key error if doesn't list all the parameters in subclass
    def __init__(self, tol=1e-4, cv=20, max_iter=10000, fit_intercept=True, normalize=False, eps=1e-3, n_alphas=100, alphas=None,
                 precompute='auto', copy_X=True,verbose=False, n_jobs=1,
                 positive=False, random_state=None, selection='cyclic'):
        super(iBAS_Lasso, self).__init__(eps=eps, n_alphas=n_alphas, alphas=alphas, fit_intercept=fit_intercept,
                 normalize = normalize, precompute=precompute, max_iter=max_iter, tol=tol,
                 copy_X=copy_X, cv=cv, verbose=verbose, n_jobs=n_jobs,
                 positive=positive, random_state=random_state, selection=selection)    
    def getMinMSE(self, X, y):  # X is a matrix
        # model_lasso = self.fit(X, y)  # raise error     fit_intercept = path_params['fit_intercept'] KeyError: 'fit_intercept'
        model_lasso = LassoCV(cv=20, tol=1e-4, max_iter=10000).fit(X, y)
        lassoBestMSE = min(model_lasso.mse_path_.mean(axis=-1)) 
        return getMinMSE         
    def getCoefs(self, X, y, features):
        model_lasso = self.fit(X, y)
        # model_lasso = LassoCV(cv=20, tol=1e-4, max_iter=10000).fit(X, y)
        lassoCoefs = model_lasso.coef_
        valid_i = [ i for i in range(len(lassoCoefs)) if lassoCoefs[i] != 0]
        validFeatures = features[ valid_i] 
        lassoCoefs = [ x for x in lassoCoefs if x!=0]
        validFeatures = zip(validFeatures, lassoCoefs)
        return validFeatures 
    def getCoefsFromList(self, oriData, yCol, XCols):   
        # XCols = range(XColStart, len(oriData[0]))
        X, y, features = self.getDataFromList(oriData,yCol, XCols)
        validFeatures = self.getCoefs(X, y, features)
        return validFeatures
    def getDataFromDF(self, df, yCol, XCols):  # yCol and XCols are the numbers
        X = np.array(df.ix[ :, XCols])
        y = np.array(df.ix[: , yCol])
        features = df.columns.values[XCols]
        return X, y, features    
    def getDataFromList(self, oriData, yCol, XCols):  # input is a two dimension list
        df = pd.DataFrame(oriData[1:], columns= oriData[0])
        X, y, features = self.getDataFromDF(df, yCol, XCols)
        return X, y, features
    
if __name__ == '__main__':    
    test = iBAS_Lasso(n_jobs=2)
    df = pd.DataFrame(np.random.randn(50, 5), columns = list("ABCDE"))
    yCol =1
    XCols = [2, 3,4]
    X, y , features = test.getDataFromDF(df, yCol, XCols)
    twoDList = np.random.randn(100, 10)
    twoDList = [list("ABCDEFGHIK")] + twoDList.tolist()
    X, y , features = test.getDataFromList(twoDList, yCol, XCols)
    print test.cv
    validFeatures = test.getCoefsFromList(twoDList, 0, 1)
    test.fit(X, y)
    
    