package com.investmentradar.controller;

import com.investmentradar.common.ApiResponse;
import com.investmentradar.dto.response.ResearchReportResponse;
import com.investmentradar.service.ResearchReportService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/report")
public class ReportController {

	@Autowired
	private ResearchReportService researchReportService;

	@GetMapping("/{taskId}")
	public ApiResponse<ResearchReportResponse> getReport(@PathVariable String taskId) {
		return ApiResponse.success(researchReportService.getReportByTaskId(taskId));
	}

}
