import listsCatalog

def calculateQuo(filmDict):
    filmQuo = {}
    catalog = listsCatalog.listcatalog
    for key, value in filmDict.items():
        lists = value['lists']
        if len(lists) == 1: continue
        quo = 0
        detail = ''
        for (keyLi, indexLi) in lists:
            criterium = catalog[keyLi]['criterium']
            isRank = catalog[keyLi]['rank']
            detailLi = f'{catalog[keyLi]['name']}: '
            if isRank:
                if indexLi <= 10 and indexLi > 1:
                    criterium = criterium + (10/8)
                elif indexLi == 1:
                    criterium = criterium + (10/6)
                else:
                    criterium = criterium + (10/indexLi)
                detailLi = f'{detailLi} ({indexLi}i)'
            detailLi = f'<b>{detailLi}</b> {criterium}<br/>'
            detail = f'{detail}{detailLi}'
            quo = quo + criterium
        if quo < 7: continue
        filmQuo[key] = {'year': value['year'],'quo': quo, 'detail': detail}
    return dict(sorted(filmQuo.items(), key=lambda x:x[1]['quo'], reverse=True))
    # print(filmQuo.items())
    # print(list(filmQuo).sort(key=lambda x:x[0]['quo']))