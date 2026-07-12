package com.investmentradar.dto.response;

import lombok.AllArgsConstructor;
import lombok.Data;

/**
 * 研究任务状态响应。
 */
@Data
@AllArgsConstructor
public class ResearchTaskResponse {

	/** 任务 ID（UUID） */
	private String taskId;

	/** 任务状态：PENDING / RUNNING / SUCCESS / FAILED */
	private String status;

	/** 执行进度（0-100） */
	private Integer progress;

}
