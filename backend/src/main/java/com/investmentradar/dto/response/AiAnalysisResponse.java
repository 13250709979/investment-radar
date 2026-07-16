package com.investmentradar.dto.response;

import com.fasterxml.jackson.annotation.JsonInclude;
import lombok.Builder;
import lombok.Data;

import java.math.BigDecimal;
import java.time.LocalDateTime;

@Data
@Builder
@JsonInclude(JsonInclude.Include.NON_NULL)
public class AiAnalysisResponse {

	private Long id;

	private String dataType;

	private Long dataId;

	private String companyCode;

	private String companyName;

	private String industry;

	private String eventType;

	private Integer eventLevel;

	private String sentiment;

	private BigDecimal confidence;

	private String title;

	private String summary;

	/** 详情接口返回；列表接口为 null */
	private String reasoning;

	/** 详情接口返回；列表接口为 null */
	private String investmentOpinion;

	/** 详情接口返回；列表接口为 null */
	private String riskWarning;

	private Object tags;

	private Object entities;

	private String modelProvider;

	private String modelName;

	private String promptVersion;

	private Integer inputTokens;

	private Integer outputTokens;

	private Integer totalTokens;

	private Integer analysisStatus;

	private String errorMessage;

	private LocalDateTime analysisTime;

	private LocalDateTime createTime;

}
