package com.investmentradar.controller;

import com.investmentradar.common.ApiResponse;
import com.investmentradar.dto.response.AiAnalysisPageResponse;
import com.investmentradar.dto.response.AiAnalysisResponse;
import com.investmentradar.service.AiAnalysisService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

/**
 * AI 分析结果查询。
 */
@RestController
@RequestMapping("/api/ai-analysis")
public class AiAnalysisController {

	@Autowired
	private AiAnalysisService aiAnalysisService;

	/**
	 * 分页查询 AI 分析结果。
	 */
	@GetMapping
	public ApiResponse<AiAnalysisPageResponse> list(
			@RequestParam(required = false) String companyCode,
			@RequestParam(required = false) String companyName,
			@RequestParam(required = false) Integer analysisStatus,
			@RequestParam(defaultValue = "1") int page,
			@RequestParam(defaultValue = "20") int size) {
		return ApiResponse.success(
				aiAnalysisService.list(companyCode, companyName, analysisStatus, page, size));
	}

	/**
	 * 按 ID 查询单条 AI 分析详情。
	 */
	@GetMapping("/{id}")
	public ApiResponse<AiAnalysisResponse> getById(@PathVariable Long id) {
		return ApiResponse.success(aiAnalysisService.getById(id));
	}

}
