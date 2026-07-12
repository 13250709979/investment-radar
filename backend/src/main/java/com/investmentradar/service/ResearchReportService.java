package com.investmentradar.service;

import com.investmentradar.dto.response.ResearchReportResponse;

public interface ResearchReportService {

	ResearchReportResponse getReportByTaskId(String taskId);

}
