package com.investmentradar.controller;

import com.investmentradar.common.ApiResponse;
import com.investmentradar.dto.request.CreateResearchRequest;
import com.investmentradar.dto.response.CreateResearchResponse;
import com.investmentradar.dto.response.ResearchTaskResponse;
import com.investmentradar.service.ResearchService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import javax.validation.Valid;

/**
 * 研究任务接口。
 */
@Validated
@RestController
@RequestMapping("/api/research")
public class ResearchController {

	@Autowired
	private ResearchService researchService;

	/**
	 * 创建研究任务，异步分析由 Worker 后续处理。
	 */
	@PostMapping
	public ApiResponse<CreateResearchResponse> createResearch(@Valid @RequestBody CreateResearchRequest request) {
		return ApiResponse.success(researchService.createTask(request));
	}

	/**
	 * 查询任务状态与进度。
	 */
	@GetMapping("/{taskId}")
	public ApiResponse<ResearchTaskResponse> getTask(@PathVariable String taskId) {
		return ApiResponse.success(researchService.getTaskByTaskId(taskId));
	}

}
