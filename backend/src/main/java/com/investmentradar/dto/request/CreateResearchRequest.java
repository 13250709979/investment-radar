package com.investmentradar.dto.request;

import lombok.Data;

import javax.validation.constraints.NotBlank;

@Data
public class CreateResearchRequest {

	@NotBlank(message = "公司名称不能为空")
	private String companyName;

	private String stockCode;

}
