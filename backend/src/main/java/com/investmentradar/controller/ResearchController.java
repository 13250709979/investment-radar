package com.investmentradar.controller;

import com.investmentradar.common.ApiResponse;
import com.investmentradar.dto.request.CreateResearchRequest;
import com.investmentradar.dto.response.CreateResearchResponse;
import com.investmentradar.dto.response.ResearchTaskStatusResponse;
import com.investmentradar.service.ResearchService;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import javax.validation.Valid;

@Validated
@RestController
@RequestMapping("/api/research")
public class ResearchController {

	private final ResearchService researchService;

	public ResearchController(ResearchService researchService) {
		this.researchService = researchService;
	}

	@PostMapping
	public ApiResponse<CreateResearchResponse> createResearch(@Valid @RequestBody CreateResearchRequest request) {
		return ApiResponse.success(researchService.createTask(request));
	}

	@GetMapping("/{taskId}")
	public ApiResponse<ResearchTaskStatusResponse> getTaskStatus(@PathVariable String taskId) {
		return ApiResponse.success(researchService.getTaskStatus(taskId));
	}

}
