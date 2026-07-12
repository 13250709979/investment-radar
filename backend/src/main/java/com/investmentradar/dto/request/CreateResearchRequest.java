package com.investmentradar.dto.request;

import lombok.Data;

import javax.validation.constraints.NotBlank;

/**
 * 创建研究任务请求。
 */
@Data
public class CreateResearchRequest {

	/** 公司名称 */
	@NotBlank(message = "公司名称不能为空")
	private String companyName;

	/** 股票代码（可选） */
	private String stockCode;

}
