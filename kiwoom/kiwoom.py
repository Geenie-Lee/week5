from PyQt5.QAxContainer import QAxWidget
from PyQt5.QtCore import QEventLoop
from PyQt5.QtTest import QTest

from config.util import *
from config.message import *


class Kiwoom(QAxWidget):
    def __init__(self):
        super().__init__()
        print("[%s] Kiwoom class start." % current_time())
        
        self.account_number = None
        self.condition_screen_number = "0159"   # 조건검색식 스크린번호
        self.per_screen_number = "0026"         # per 스크린번호
        self.tr_data_screen_number = "2000"     # tr 요청 스크린번호
        self.stock_info_screen_number = "4000"
        
        self.event_loop_login = QEventLoop()    # login event loop
        self.event_loop_per = QEventLoop()      # per event loop
        self.event_loop_tr_data = QEventLoop()    # tr event loop

        self.get_ocx_instance()                 # kiwoom ocx instance
        self.event_slots()                      # event slots (login, tr)
        self.event_condition_slots()            # 사용자정의 조건식 이벤트 슬롯
        self.login_signal()                     # login signal
        self.condition_signal()                 # 사용자정의 조건식 시그널
#         self.per_signal()
#         self.get_stock_info()

    def get_ocx_instance(self):
        self.setControl("KHOPENAPI.KHOpenAPICtrl.1")

    def event_slots(self):
        self.OnEventConnect.connect(self.login_slot)
        self.OnReceiveTrData.connect(self.tr_data_slot)
        self.OnReceiveMsg.connect(self.message_slot)
        self.OnReceiveRealData.connect(self.real_slot)

    def event_condition_slots(self):
        self.OnReceiveConditionVer.connect(self.condition_slot)
        self.OnReceiveTrCondition.connect(self.condition_tr_slot)
        self.OnReceiveRealCondition.connect(self.condition_real_slot)

    def login_signal(self):
        self.dynamicCall("CommConnect()")
        self.event_loop_login.exec_()

    def condition_signal(self):
        self.dynamicCall("GetConditionLoad()")

    def per_signal(self):
        # PER구분 = 1:코스피저PER, 2:코스피고PER, 3:코스닥저PER, 4:코스닥고PER
        self.dynamicCall("SetInputValue(QString, QString)", "PER구분", "1")
        self.dynamicCall("CommRqData(QString, QString, int, QString)", "고저PER요청", "opt10026",  0, self.per_screen_number)
        self.event_loop_per.exec_()

    def get_stock_info(self):
        # [시장구분값] 0: 장내, 10: 코스닥, 3: ELW, 8: ETF, 50: KONEX, 4: 뮤추얼펀드, 5: 신주인수권, 6: 리츠, 9: 하이얼펀드, 30: K - OTC
        market_codes = ["10"]
        cnt = 0
        for market_code in market_codes:
            codes = self.dynamicCall("GetCodeListByMarket(QString)", market_code)
            code_list = codes.split(";")[:-1]
            for stock_code in code_list:
                self.dynamicCall("DisconnectRealData(QString)", self.stock_info_screen_number)
                cnt += 1
                print("")
                print("[%s] (%s).종목코드: %s" % (current_time(), cnt, stock_code))
                self.stock_base_signal(stock_code)

    # 종목코드에 해당하는 주식기본정보요청(opt10001)
    def stock_base_signal(self, stock_code=None):
#         QTest.qWait(500)  # 3600 Delay Time
        self.dynamicCall("SetInputValue(QString, QString)", "종목코드", stock_code)
        self.dynamicCall("CommRqData(QString, QString, int, QString)", "주식기본정보요청", "opt10001", 0, self.stock_info_screen_number)
        self.event_loop_tr_data.exec_()

    def tr_data_slot(self, screen_number, rq_name, tr_code, record_name, prev_next):
        print("")
        if tr_code == "opt10026":
            rows = self.dynamicCall("GetRepeatCnt(QString, QString)", tr_code, rq_name)
            print(">> opt10026.보유 종목 건수: %s" % rows)

            # 종목번호, 종목명, 보유수량, 매입가, 매입금액, 매매가능수량, 수익률(%), 현재가, 전일종가
            for i in range(rows):
                stock_code = self.dynamicCall("GetCommData(QString, QString, int, QString)", tr_code, rq_name, i, "종목코드").strip()[1:]
                stock_name = self.dynamicCall("GetCommData(QString, QString, int, QString)", tr_code, rq_name, i, "종목명").strip()
                per = self.dynamicCall("GetCommData(QString, QString, int, QString)", tr_code, rq_name, i, "PER").strip()
                close_price = self.dynamicCall("GetCommData(QString, QString, int, QString)", tr_code, rq_name, i, "현재가").strip()
                fluctuation_rate = self.dynamicCall("GetCommData(QString, QString, int, QString)", tr_code, rq_name, i, "등락률").strip()
                current_volume = self.dynamicCall("GetCommData(QString, QString, int, QString)", tr_code, rq_name, i, "현재거래량").strip()
                ask_price = self.dynamicCall("GetCommData(QString, QString, int, QString)", tr_code, rq_name, i,"매도호가").strip()
                
                print("")
                print("[%s] 종목코드: %s" % (current_time(), stock_code))
                print("[%s] 종목명: %s" % (current_time(), stock_name))
                print("[%s] PER: %s" % (current_time(), per))
                print("[%s] 현재가: %s" % (current_time(), close_price))
                print("[%s] 등락률: %s" % (current_time(), fluctuation_rate))
                print("[%s] 현재거래량: %s" % (current_time(), current_volume))
                print("[%s] 매도호가: %s" % (current_time(), ask_price))

            self.event_loop_per.exit()

        elif tr_code == "opt10001":

            stock_code = self.dynamicCall("GetCommData(QString, QString, int, QString)", tr_code, rq_name, 0, "종목코드").strip()
            stock_name = self.dynamicCall("GetCommData(QString, QString, int, QString)", tr_code, rq_name, 0, "종목명").strip()
            a_stock = self.dynamicCall("GetCommData(QString, QString, int, QString)", tr_code, rq_name, 0, "상장주식").strip()
            b_stock = self.dynamicCall("GetCommData(QString, QString, int, QString)", tr_code, rq_name, 0, "유통주식").strip()
            open_price = self.dynamicCall("GetCommData(QString, QString, int, QString)", tr_code, rq_name, 0, "시가").strip()
            close_price = self.dynamicCall("GetCommData(QString, QString, int, QString)", tr_code, rq_name, 0, "현재가").strip()
            high_price = self.dynamicCall("GetCommData(QString, QString, int, QString)", tr_code, rq_name, 0, "고가").strip()
            low_price = self.dynamicCall("GetCommData(QString, QString, int, QString)", tr_code, rq_name, 0, "저가").strip()

            print("")
            print("[%s] 종목코드: %s" % (current_time(), stock_code))
            print("[%s] 종목명: %s" % (current_time(), stock_name))
            print("[%s] 상장주식: %s" % (current_time(), a_stock))
            print("[%s] 유통주식: %s" % (current_time(), b_stock))
            print("[%s] 현재가: %s" % (current_time(), open_price))
            print("[%s] 시가: %s" % (current_time(), close_price))
            print("[%s] 고가: %s" % (current_time(), high_price))
            print("[%s] 저가: %s" % (current_time(), low_price))
            
#             send("[%s:%s] %s:%s:%s:%s" % (stock_code, stock_name, open_price, close_price, high_price, low_price))
            self.event_loop_tr_data.exit()


    def login_slot(self, error_code):
        print("[%s] 로그인(1:성공): [%s]" % (current_time(), error_code))
        self.get_login_info()
        self.event_loop_login.exit()

    def condition_slot(self, success, message):
        print("")
        print("[%s] 호출결과(%s): %s" % (current_time(), success, message))

        # 사용자 정의 조건식 목록
        conditions = self.dynamicCall("GetConditionNameList()")[:-1]
        print("[%s] 사용자정의 조건식: %s" % (current_time(), conditions))

        condition_list = conditions.split(";")
        for condition in condition_list:
            condition_index = int(condition.split("^")[0])
            condition_name = condition.split("^")[1]
            print(">> [%s][%s]" % (condition_index, condition_name))

            if condition_index in (7, 8, 22, 23, 24):
                self.dynamicCall("SendCondition(QString, QString, int, int)", self.condition_screen_number, condition_name, condition_index, 1)

    def condition_tr_slot(self, screen_number, stock_codes, condition_name, condition_index, prev_next):
        print("")
#         print("[%s] 화면번호: %s" % (current_time(), screen_number))
        print("[%s] 조건식인덱스: %s" % (current_time(), condition_index))
        print("[%s] 조건식이름: %s" % (current_time(), condition_name))
#         print("[%s] 종목코드리스트: %s" % (current_time(), stock_codes))
#         print("[%s] 연속조회여부: %s" % (current_time(), prev_next))

        code_list = stock_codes.split(";")[:-1]
        for code in code_list:
            code_name = self.dynamicCall("GetMasterCodeName(QString)", code)
            stock_cnt = int(self.dynamicCall("GetMasterListedStockCnt(QString)", code))
            print("[%s] %s: %s (주식수: %s)" % (current_time(), code, code_name, format(stock_cnt, ",")))

    def condition_real_slot(self, stock_code, event_type, condition_name, condition_index):
        print("")
        print("[%s] 조건식인덱스: %s" % (current_time(), condition_index))
        print("[%s] 조건식이름: %s" % (current_time(), condition_name))
        print("[%s] 종목코드: %s" % (current_time(), stock_code))
        code_name = self.dynamicCall("GetMasterCodeName(QString)", stock_code)
        
        # opt10001: 주식기본정보요청
        if event_type == "I":
            # 실시간 감시 추가 : strSavedScreenNo, strCode, _T("9001;302;10;11;25;12;13"), "1"
            fids = "20;10;12;15;16;17;18"
            self.dynamicCall("SetRealReg(QString, QString, QString, QString)", self.condition_screen_number, stock_code, fids, "1")
            print("[%s] 종목편입: %s" % (current_time(), event_type))
            
        elif event_type == "D":
            print("[%s] 종목이탈: %s" % (current_time(), event_type))
            self.dynamicCall("SetRealRemove(QString, QString)", self.condition_screen_number, stock_code)

        print("[%s] %s: %s" % (current_time(), stock_code, code_name))
        
        # "17", "18", "22", "23", "24"
        if condition_index in ("7", "8", "22", "23", "24"):
            send("[ %s ] %s:%s:%s" % (event_type, condition_name, stock_code, code_name))

    def real_slot(self, stock_code, real_type, real_data):
#         print("[%s] 리얼타입: %s" % (current_time(), real_type))
#         print("[%s] 실시간데이터전문: %s" % (current_time(), real_data))
        stock_name = self.dynamicCall("GetMasterCodeName(QString)", stock_code);
        
        if real_type == "주식체결":
            close_price = abs(int(self.dynamicCall("GetCommRealData(QString,int)", "현재가", 10).strip()))
            open_price = abs(int(self.dynamicCall("GetCommRealData(QString,int)", "시가", 16).strip()))
            high_price = abs(int(self.dynamicCall("GetCommRealData(QString,int)", "고가", 17).strip()))
            low_price = abs(int(self.dynamicCall("GetCommRealData(QString,int)", "저가", 18).strip()))
            fluctuation_rate = float(self.dynamicCall("GetCommRealData(QString,int)", "등락율", 12).strip())
            
#             print("[%s] %s:%s 현재가:%s,시가:%s,고가:%s,저가:%s,등락율:%s" % (current_time(), stock_code, stock_name, close_price, open_price, high_price, low_price, fluctuation_rate))
#             send("[%s] 종목코드: %s %s:%s:%s:%s:%s" % (current_time(), stock_code, close_price, open_price, high_price, low_price, fluctuation_rate))

    @staticmethod
    def message_slot(screen_number, rq_name, tr_code, message):
        print("")
        print("[%s] 화면번호: %s" % (current_time(), screen_number))
        print("[%s] 사용자구분명: %s" % (current_time(), rq_name))
        print("[%s] TR코드: %s" % (current_time(), tr_code))
        print("[%s] 서버전달메시지: %s" % (current_time(), message))

    def get_login_info(self):
        accounts = self.dynamicCall("GetLoginInfo(QString)", "ACCNO")
        self.account_number = accounts.split(";")[0]
        print("[%s] 계좌번호: %s" % (current_time(), self.account_number))