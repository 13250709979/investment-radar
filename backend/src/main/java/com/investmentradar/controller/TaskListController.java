package com.investmentradar.controller;

import com.investmentradar.common.ApiResponse;
import com.investmentradar.dto.response.ResearchTaskListItemResponse;
import com.investmentradar.service.ResearchService;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/api/task")
public class TaskListController {

	private final ResearchService researchService;

	public TaskListController(ResearchService researchService) {
		this.researchService = researchService;
	}

	@GetMapping("/list")
	public ApiResponse<List<ResearchTaskListItemResponse>> listTasks() {
		return ApiResponse.success(researchService.listTasks());
	}

}
