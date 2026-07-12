package com.investmentradar.dto.response;

import lombok.AllArgsConstructor;
import lombok.Data;

/**
 * 创建研究任务响应。
 */
@Data
@AllArgsConstructor
public class CreateResearchResponse {

	/** 任务 ID（UUID） */
	private String taskId;

	/** 初始状态，固定为 PENDING */
	private String status;

}
