import requests
from django.conf import settings

# 국명 검색 API endpoint
def NameInfo(num):
    """
    학명번호로 상세정보 조회
    :param num: 학명 번호
    :return:
    """
    InfoUrl = 'http://openapi.nature.go.kr/openapi/service/rest/KpniService/btncInfo'
    parms = {'ServiceKey': getattr(settings, 'NAME_APIKEY'), 'q1': num, '_type': 'json'}
    # 학명 번호로 상세 정보 요청
    r = requests.get(InfoUrl, parms)

    # test code
    # print(r.json()['ns1.BtncInfoResponse']['ns1.body']['ns1.item'])

    # 식물 상세 정보에서 필요한 자료만 추출
    data = r.json()['ns1.BtncInfoResponse']['ns1.body']['ns1.item']
    info = {'국명':data['ns1.korname'],'학명':data['ns1.plantTtnm']}
    return info


def search(name,st=3):
    """
    식물이름을 검색하여 매칭되는 국명이 있을경우 해당 국명의 상세정보를 조회하여 딕셔너리 값으로 반환/없을 경우 Nnoe
    :param name:
    :param st:
    :return:
    """
    SearchUrl = 'http://openapi.nature.go.kr/openapi/service/rest/KpniService/korSearch'
    parms = {'ServiceKey': getattr(settings, 'NAME_APIKEY'), 'st': st, 'sw': name, '_type': 'json'}
    r = requests.get(SearchUrl,params=parms)
    item = r.json()['ns1.KorSearchResponse']['ns1.body']['ns1.item']

    # test code
    # print('item={0}, type={1}'.format(item,type(item)))

    if item != '':
        if type(item['ns1.KorSearchVO']) == type(list()):
            print('list // {0}'.format(item['ns1.KorSearchVO']))
            """ 결과값이 두개 이상 나올경우 """
            data = '동일한 이름의 학명ID가 2개이상 있습니다'
            return '동일한 이름의 학명ID가 2개이상 있습니다'
        elif type(item['ns1.KorSearchVO']) == type(dict()):
            """ 결과값이 1개일 경우 """
            # 매칭된 국명 번호
            num = item['ns1.KorSearchVO']['ns1.plantScnmId']
            try:
                # 국명번호 상세 조회 요청
                data = NameInfo(num)
            except EOFError as e: # 정보 죄회중 오류 발생시 None값으로 반환
                print(e)
                data = '해당 식물의 학명ID는 {0}입니다만.. 학명에 대한 조회를 실패했습니다'.format(num)
    else:
        data = '해당 식물의 이름으로 검색이 안됩니다.'
    return data

