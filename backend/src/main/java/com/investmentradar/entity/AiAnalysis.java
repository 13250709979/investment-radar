package com.investmentradar.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import com.investmentradar.config.JsonbStringTypeHandler;
import lombok.Data;

import java.math.BigDecimal;
import java.time.LocalDateTime;

@Data
@TableName(value = "ai_analysis", schema = "investment_radar", autoResultMap = true)
public class AiAnalysis {

	@TableId(type = IdType.AUTO)
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

	private String reasoning;

	private String investmentOpinion;

	private String riskWarning;

	/** JSON 原文（JSONB） */
	@TableField(typeHandler = JsonbStringTypeHandler.class)
	private String tags;

	/** JSON 原文（JSONB） */
	@TableField(typeHandler = JsonbStringTypeHandler.class)
	private String entities;

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

	private LocalDateTime updateTime;

}
