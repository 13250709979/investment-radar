package com.investmentradar.service;

import com.investmentradar.dto.request.CreateResearchRequest;
import com.investmentradar.dto.response.CreateResearchResponse;
import com.investmentradar.dto.response.ResearchTaskResponse;

/**
 * 研究任务业务接口。
 */
public interface ResearchService {

	/**
	 * 创建研究任务，写入 research_task 表。
	 */
	CreateResearchResponse createTask(CreateResearchRequest request);

	/**
	 * 根据 taskId 查询任务状态。
	 */
	ResearchTaskResponse getTaskByTaskId(String taskId);

}
