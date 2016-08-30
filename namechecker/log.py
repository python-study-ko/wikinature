import logging

"""
namechecker의 각종 정보를 로깅하는 로그객체 모음
"""

# 업로드된 파일 정보 로깅
# 로거 생성
upload_logger = logging.getLogger('wikinature.namechecker.uploadlog')
upload_logger.setLevel(logging.INFO)
# 로거 핸들러 생성
upload_handler = logging.FileHandler('upload.log')
upload_handler.setLevel(logging.INFO)
# 로거 포맷 지정
upload_formatter = logging.Formatter('%(asctime)s/%(name)s/%(levelname)s : %(message)s')
# 로거 할당
upload_handler.setFormatter(upload_formatter)
upload_logger.addHandler(upload_handler)

def uploadlog(filename='null',sheet='null',listnum='null',listtitle='null',type='null',result='null'):
    """
    업로드된 폼 정보를 로깅
    :param filename: 업로드된 파일명
    :param sheet: 폼에 입력한 시트명
    :param listnum: 폼에 입력한 식물목록 머리열 번호
    :param listtitle: 폼에 입력한 식물목록 머리열 이름
    :param type: requsets.file의 콘텐츠 타입
    :param result: 처리 성공 여부
    :return:
    """
    message = "파일 정보 : ({0}, {1})/ 구조 정보 : ({2}, {3}, {4})/ 결과 : {5}".format(filename,type,sheet,listnum,listtitle,result)
    upload_logger.info(message)