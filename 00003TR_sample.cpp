void CStockSiseDlg::OnBnClickedButtonTest()
{
	
	g_iYuantaAPI.YOA_SetTRFieldLong( _T("000003"), _T("InBlock1"), _T("gubun"), 302 );
	m_nReqID_000003 = g_iYuantaAPI.YOA_Request( GetSafeHwnd(), _T("000003"), FALSE );

	if ( ERROR_MAX_CODE < m_nReqID_000003 )
	{
		CString strMsg;
		strMsg.Format( _T("[ReqID:%d] [000003] 종목조회를 요청하였습니다."), m_nReqID_000003 );

		m_pMainDlg->LogMessage( strMsg );
	}
	else
	{
		TCHAR msg[1024] = {0,};

		//int nErrorCode = g_iYuantaAPI.YOA_GetLastError();
		int nErrorCode = m_nReqID_000003;
		g_iYuantaAPI.YOA_GetErrorMessage( nErrorCode, msg, sizeof(msg) );

		CString strErrorMsg;
		strErrorMsg.Format( _T("[%d] %s"), nErrorCode, msg );

		m_pMainDlg->LogMessage( _T("[000003] 종목조회를 요청중 오류가 발생하였습니다."), 1 );
		m_pMainDlg->LogMessage( strErrorMsg, 1, FALSE );
	}
}

void CStockSiseDlg::Process000003()
{

	////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//	유안타증권 Open API 출력코드 예제입니다.
//	[000003] 국내선옵종목정보 - 출력블록
 
	TCHAR data[1024] = {0,};
 
	g_iYuantaAPI.YOA_SetTRInfo( _T("000003"), _T("OutBlock1") );			// TR정보(TR명, Block명)를 설정합니다.
	memset(data, 0x00, sizeof(data));
	//g_iYuantaAPI.YOA_GetFieldString( _T("next"),                     data, sizeof(data), 0 );		// 다음유무 값을 가져옵니다.
 

	byte byteData = 0;
	g_iYuantaAPI.YOA_GetTRFieldByte( _T("000003"), _T("OutBlock1"), _T("next"), &byteData );

	g_iYuantaAPI.YOA_SetTRInfo( _T("000003"), _T("OutBlock2") );			// TR정보(TR명, Block명)를 설정합니다.


	int nDataCount = g_iYuantaAPI.YOA_GetRowCount( _T("000003"), _T("OutBlock2") );

	for ( int i = 0; i < nDataCount; i++ )
	{
			
		memset(data, 0x00, sizeof(data));
		g_iYuantaAPI.YOA_GetFieldString( _T("shortcode"),                data, sizeof(data), 0 );		// 단축코드 값을 가져옵니다.
		memset(data, 0x00, sizeof(data));
		g_iYuantaAPI.YOA_GetFieldString( _T("stdcode"),                  data, sizeof(data), 0 );		// 표준코드 값을 가져옵니다.
		memset(data, 0x00, sizeof(data));
		g_iYuantaAPI.YOA_GetFieldString( _T("jongname"),                 data, sizeof(data), 0 );		// 종목이름 값을 가져옵니다.
		memset(data, 0x00, sizeof(data));
		g_iYuantaAPI.YOA_GetFieldString( _T("futrtp"),                   data, sizeof(data), 0 );		// 선물옵션구분 값을 가져옵니다.
		memset(data, 0x00, sizeof(data));
		g_iYuantaAPI.YOA_GetFieldString( _T("order"),                    data, sizeof(data), 0 );		// 월물순서 값을 가져옵니다.
		memset(data, 0x00, sizeof(data));
		g_iYuantaAPI.YOA_GetFieldString( _T("standardjuka"),             data, sizeof(data), 0 );		// 기준가 값을 가져옵니다.
		memset(data, 0x00, sizeof(data));
		g_iYuantaAPI.YOA_GetFieldString( _T("upjuka"),                   data, sizeof(data), 0 );		// 상한가 값을 가져옵니다.
		memset(data, 0x00, sizeof(data));
		g_iYuantaAPI.YOA_GetFieldString( _T("downjuka"),                 data, sizeof(data), 0 );		// 하한가 값을 가져옵니다.
	}


	if ( 1 == byteData )
		g_iYuantaAPI.YOA_Request( GetSafeHwnd(), _T("000003"), FALSE, m_nReqID_000003 );
	

}