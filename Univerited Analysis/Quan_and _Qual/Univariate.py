class Univariate():
    
    def getQuanQual(data):
        Quan,Qual=[],[]
        for i in data.columns:
            if data[i].dtype=='O':
                Qual.append(i)
            elif data[i].dtype!='O':
                Quan.append(i)
        return Quan,Qual