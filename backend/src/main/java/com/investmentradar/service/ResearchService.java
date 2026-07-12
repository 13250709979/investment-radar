package com.investmentradar.service;

import com.investmentradar.dto.request.CreateResearchRequest;
import com.investmentradar.dto.response.CreateResearchResponse;
import com.investmentradar.dto.response.ResearchTaskListItemResponse;
import com.investmentradar.dto.response.ResearchTaskStatusResponse;

import java.util.List;

public interface ResearchService {

	CreateResearchResponse createTask(CreateResearchRequest request);

	ResearchTaskStatusResponse getTaskStatus(String taskId);

	List<ResearchTaskListItemResponse> listTasks();

}
