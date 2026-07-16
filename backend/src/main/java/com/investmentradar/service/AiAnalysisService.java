package com.investmentradar.service;

import com.investmentradar.dto.response.AiAnalysisPageResponse;
import com.investmentradar.dto.response.AiAnalysisResponse;

public interface AiAnalysisService {

	AiAnalysisPageResponse list(String companyCode, String companyName, Integer analysisStatus,
			int page, int size);

	AiAnalysisResponse getById(Long id);

}
