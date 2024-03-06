import listsCatalog as listsCatalog

def calculate_quo(filmDict):
    filmQuo = {}
    catalog = listsCatalog.listcatalog
    for key, value in filmDict.items():
        lists = value['lists']
        if len(lists) == 1: continue
        quo = 0
        filmQuo[key] = {'quo': quo} # filmQuo = { "the-godfather": {"quo": 0} }
        for (keyli, indexLi) in lists:
            criterium = catalog[keyli]['criterium']
            isRank = catalog[keyli]['rank']
            # listkey = catalog[keyli]['name']
            detailli = f''

            if isRank:
                if indexLi <= 10 and indexLi > 1:
                    criterium = criterium + (10/8)
                elif indexLi == 1:
                    criterium = criterium + (10/6)
                else:
                    criterium = criterium + (10/indexLi)

                detailli = f'({indexLi}i)'

            detailli = f'{detailli}{criterium}'
            filmQuo[key][keyli] = detailli
            quo = quo + criterium
        # if quo < 7: continue
        filmQuo[key]['quo'] = quo

    return dict(sorted(filmQuo.items(), key=lambda x:x[1]['quo'], reverse=True))