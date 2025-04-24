class Univariate():
    
    def getQuanQual(data):
        Quan,Qual=[],[]
        for i in data.columns:
            if data[i].dtype=='O':
                Qual.append(i)
            elif data[i].dtype!='O':
                Quan.append(i)
        return Quan,Qual
    
    def univariated(dataset,quan):
        datanew=pd.DataFrame(index['Mean','Median','Mode','Q1:25%','Q2:50%','Q3:75%','99%','Q4:100%','IQR',
                                               '1.5Rule','LesserIQR','GreaterIQR','Min','Max'], columns=Quan)
        for i in datanew:
            datanew[i]['Mean']=dataset[i].mean()
            datanew[i]['Median']=dataset[i].median()
            datanew[i]['Mode']=dataset[i].mode()[0]
            datanew[i]['Q1:25%']=dataset.describe()[i]['25%']
            datanew[i]['Q2:50%']=dataset.describe()[i]['75%']
            datanew[i]['Q3:75%']=dataset.describe()[i]['75%']
            datanew[i]['99%']=np.percentile(dataset[i],99)
            datanew[i]['Q4:100%']=dataset.describe()[i]['max']
            datanew[i]['IQR']=datanew[i]['Q3:75%']-datanew[i]['Q1:25%']
            datanew[i]['1.5Rule']=1.5*datanew[i]['IQR']
            datanew[i]['LesserIQR']=datanew[i]['Q1:25%']-datanew[i]['1.5Rule']
            datanew[i]['GreaterIQR']=datanew[i]['Q3:75%']+datanew[i]['1.5Rule']
            datanew[i]['Min']=dataset[i].min()
            datanew[i]['Max']=dataset[i].max()
        return datanew
    
    def freqTable(dataset,columName):
        freqTable=pd.DataFrame(columns=['Unique_values','Frequency','Relative_frequency','CumSum'])
        freqTable['Unique_values']=dataset[columName].value_counts().index
        freqTable['Frequency']=dataset[columName].value_counts().values
        freqTable['Relative_frequency']=freqTable['Frequency']/len(freqTable)
        freqTable['CumSum']=freqTable['Relative_frequency'].cumsum()
        return freqTable
    
    def Outlier_column_Names(datanew):
        Lesser=[]
        Greater=[]
        for data in datanew:
            if datanew[data]['Min'] < datanew[data]['LesserIQR']:
                Lesser.append(data)
            if datanew[data]['Max'] > datanew[data]['GreaterIQR']:
                Greater.append(data)
        return Lesser,Greater
    
    def Replacing_Outlier(Lesser,Greater,dataset,datanew):
        for less in Lesser:
            dataset[less]=dataset[less].mask(dataset[less] < datanew[less]['LesserIQR'], datanew[less]['LesserIQR'])
        for great in Greater:
            dataset[great]=dataset[great].mask(dataset[great] > datanew[great]['GreaterIQR'], datanew[great]['GreaterIQR'])
        return dataset