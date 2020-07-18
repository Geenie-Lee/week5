void CStockSiseDlg::OnBnClickedButtonTest()
{
	
	g_iYuantaAPI.YOA_SetTRFieldLong( _T("000003"), _T("InBlock1"), _T("gubun"), 302 );
	m_nReqID_000003 = g_iYuantaAPI.YOA_Request( GetSafeHwnd(), _T("000003"), FALSE );

	if ( ERROR_MAX_CODE < m_nReqID_000003 )
	{
		CString strMsg;
		strMsg.Format( _T("[ReqID:%d] [000003] ������ȸ�� ��û�Ͽ����ϴ�."), m_nReqID_000003 );

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

		m_pMainDlg->LogMessage( _T("[000003] ������ȸ�� ��û�� ������ �߻��Ͽ����ϴ�."), 1 );
		m_pMainDlg->LogMessage( strErrorMsg, 1, FALSE );
	}
}

void CStockSiseDlg::Process000003()
{

	////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//	����Ÿ���� Open API ����ڵ� �����Դϴ�.
//	[000003] ���������������� - ��º��
 
	TCHAR data[1024] = {0,};
 
	g_iYuantaAPI.YOA_SetTRInfo( _T("000003"), _T("OutBlock1") );			// TR����(TR��, Block��)�� �����մϴ�.
	memset(data, 0x00, sizeof(data));
	//g_iYuantaAPI.YOA_GetFieldString( _T("next"),                     data, sizeof(data), 0 );		// �������� ���� �����ɴϴ�.
 

	byte byteData = 0;
	g_iYuantaAPI.YOA_GetTRFieldByte( _T("000003"), _T("OutBlock1"), _T("next"), &byteData );

	g_iYuantaAPI.YOA_SetTRInfo( _T("000003"), _T("OutBlock2") );			// TR����(TR��, Block��)�� �����մϴ�.


	int nDataCount = g_iYuantaAPI.YOA_GetRowCount( _T("000003"), _T("OutBlock2") );

	for ( int i = 0; i < nDataCount; i++ )
	{
			
		memset(data, 0x00, sizeof(data));
		g_iYuantaAPI.YOA_GetFieldString( _T("shortcode"),                data, sizeof(data), 0 );		// �����ڵ� ���� �����ɴϴ�.
		memset(data, 0x00, sizeof(data));
		g_iYuantaAPI.YOA_GetFieldString( _T("stdcode"),                  data, sizeof(data), 0 );		// ǥ���ڵ� ���� �����ɴϴ�.
		memset(data, 0x00, sizeof(data));
		g_iYuantaAPI.YOA_GetFieldString( _T("jongname"),                 data, sizeof(data), 0 );		// �����̸� ���� �����ɴϴ�.
		memset(data, 0x00, sizeof(data));
		g_iYuantaAPI.YOA_GetFieldString( _T("futrtp"),                   data, sizeof(data), 0 );		// �����ɼǱ��� ���� �����ɴϴ�.
		memset(data, 0x00, sizeof(data));
		g_iYuantaAPI.YOA_GetFieldString( _T("order"),                    data, sizeof(data), 0 );		// �������� ���� �����ɴϴ�.
		memset(data, 0x00, sizeof(data));
		g_iYuantaAPI.YOA_GetFieldString( _T("standardjuka"),             data, sizeof(data), 0 );		// ���ذ� ���� �����ɴϴ�.
		memset(data, 0x00, sizeof(data));
		g_iYuantaAPI.YOA_GetFieldString( _T("upjuka"),                   data, sizeof(data), 0 );		// ���Ѱ� ���� �����ɴϴ�.
		memset(data, 0x00, sizeof(data));
		g_iYuantaAPI.YOA_GetFieldString( _T("downjuka"),                 data, sizeof(data), 0 );		// ���Ѱ� ���� �����ɴϴ�.
	}


	if ( 1 == byteData )
		g_iYuantaAPI.YOA_Request( GetSafeHwnd(), _T("000003"), FALSE, m_nReqID_000003 );
	

}