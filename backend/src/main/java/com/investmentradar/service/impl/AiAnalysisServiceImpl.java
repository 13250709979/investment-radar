package com.investmentradar.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.investmentradar.common.ResultCode;
import com.investmentradar.dto.response.AiAnalysisPageResponse;
import com.investmentradar.dto.response.AiAnalysisResponse;
import com.investmentradar.entity.AiAnalysis;
import com.investmentradar.exception.BusinessException;
import com.investmentradar.mapper.AiAnalysisMapper;
import com.investmentradar.service.AiAnalysisService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.util.StringUtils;

import java.util.stream.Collectors;

@Service
public class AiAnalysisServiceImpl implements AiAnalysisService {

	private static final int DEFAULT_PAGE = 1;
	private static final int DEFAULT_SIZE = 20;
	private static final int MAX_SIZE = 100;

	@Autowired
	private AiAnalysisMapper aiAnalysisMapper;

	@Autowired
	private ObjectMapper objectMapper;

	@Override
	public AiAnalysisPageResponse list(String companyCode, String companyName, Integer analysisStatus,
			int page, int size) {
		int safePage = page < 1 ? DEFAULT_PAGE : page;
		int safeSize = size < 1 ? DEFAULT_SIZE : Math.min(size, MAX_SIZE);

		LambdaQueryWrapper<AiAnalysis> wrapper = new LambdaQueryWrapper<AiAnalysis>()
				.eq(StringUtils.hasText(companyCode), AiAnalysis::getCompanyCode, companyCode)
				.like(StringUtils.hasText(companyName), AiAnalysis::getCompanyName, companyName)
				.eq(analysisStatus != null, AiAnalysis::getAnalysisStatus, analysisStatus)
				.orderByDesc(AiAnalysis::getAnalysisTime)
				.orderByDesc(AiAnalysis::getId);

		Page<AiAnalysis> result = aiAnalysisMapper.selectPage(new Page<>(safePage, safeSize), wrapper);

		return new AiAnalysisPageResponse(
				result.getTotal(),
				safePage,
				safeSize,
				result.getRecords().stream()
						.map(row -> toResponse(row, false))
						.collect(Collectors.toList()));
	}

	@Override
	public AiAnalysisResponse getById(Long id) {
		AiAnalysis row = aiAnalysisMapper.selectById(id);
		if (row == null) {
			throw new BusinessException(ResultCode.NOT_FOUND, "AI分析结果不存在");
		}
		return toResponse(row, true);
	}

	private AiAnalysisResponse toResponse(AiAnalysis row, boolean detail) {
		AiAnalysisResponse.AiAnalysisResponseBuilder builder = AiAnalysisResponse.builder()
				.id(row.getId())
				.dataType(row.getDataType())
				.dataId(row.getDataId())
				.companyCode(row.getCompanyCode())
				.companyName(row.getCompanyName())
				.industry(row.getIndustry())
				.eventType(row.getEventType())
				.eventLevel(row.getEventLevel())
				.sentiment(row.getSentiment())
				.confidence(row.getConfidence())
				.title(row.getTitle())
				.summary(row.getSummary())
				.tags(parseJson(row.getTags()))
				.entities(parseJson(row.getEntities()))
				.modelProvider(row.getModelProvider())
				.modelName(row.getModelName())
				.promptVersion(row.getPromptVersion())
				.inputTokens(row.getInputTokens())
				.outputTokens(row.getOutputTokens())
				.totalTokens(row.getTotalTokens())
				.analysisStatus(row.getAnalysisStatus())
				.errorMessage(row.getErrorMessage())
				.analysisTime(row.getAnalysisTime())
				.createTime(row.getCreateTime());

		if (detail) {
			builder.reasoning(row.getReasoning())
					.investmentOpinion(row.getInvestmentOpinion())
					.riskWarning(row.getRiskWarning());
		}
		return builder.build();
	}

	private Object parseJson(String raw) {
		if (!StringUtils.hasText(raw)) {
			return null;
		}
		try {
			return objectMapper.readValue(raw, Object.class);
		}
		catch (JsonProcessingException ex) {
			return raw;
		}
	}

}
