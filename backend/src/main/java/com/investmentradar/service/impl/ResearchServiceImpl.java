package com.investmentradar.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.investmentradar.common.ResultCode;
import com.investmentradar.common.enums.ResearchTaskStatus;
import com.investmentradar.dto.request.CreateResearchRequest;
import com.investmentradar.dto.response.CreateResearchResponse;
import com.investmentradar.dto.response.ResearchTaskListItemResponse;
import com.investmentradar.dto.response.ResearchTaskStatusResponse;
import com.investmentradar.entity.ResearchTask;
import com.investmentradar.exception.BusinessException;
import com.investmentradar.mapper.ResearchTaskMapper;
import com.investmentradar.service.ResearchService;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.List;
import java.util.UUID;
import java.util.stream.Collectors;

@Service
public class ResearchServiceImpl implements ResearchService {

	private final ResearchTaskMapper researchTaskMapper;

	public ResearchServiceImpl(ResearchTaskMapper researchTaskMapper) {
		this.researchTaskMapper = researchTaskMapper;
	}

	@Override
	public CreateResearchResponse createTask(CreateResearchRequest request) {
		String taskId = UUID.randomUUID().toString();
		LocalDateTime now = LocalDateTime.now();

		ResearchTask task = new ResearchTask();
		task.setTaskId(taskId);
		task.setCompanyName(request.getCompanyName());
		task.setStockCode(request.getStockCode());
		task.setStatus(ResearchTaskStatus.PENDING.name());
		task.setProgress(0);
		task.setCreatedAt(now);
		task.setUpdatedAt(now);

		researchTaskMapper.insert(task);
		return new CreateResearchResponse(taskId, ResearchTaskStatus.PENDING.name());
	}

	@Override
	public ResearchTaskStatusResponse getTaskStatus(String taskId) {
		ResearchTask task = findTaskOrThrow(taskId);
		return new ResearchTaskStatusResponse(task.getTaskId(), task.getStatus(), task.getProgress());
	}

	@Override
	public List<ResearchTaskListItemResponse> listTasks() {
		LambdaQueryWrapper<ResearchTask> wrapper = new LambdaQueryWrapper<ResearchTask>()
				.orderByDesc(ResearchTask::getCreatedAt);
		return researchTaskMapper.selectList(wrapper).stream()
				.map(task -> new ResearchTaskListItemResponse(
						task.getTaskId(),
						task.getCompanyName(),
						task.getStockCode(),
						task.getStatus(),
						task.getProgress(),
						task.getCreatedAt()))
				.collect(Collectors.toList());
	}

	private ResearchTask findTaskOrThrow(String taskId) {
		LambdaQueryWrapper<ResearchTask> wrapper = new LambdaQueryWrapper<ResearchTask>()
				.eq(ResearchTask::getTaskId, taskId);
		ResearchTask task = researchTaskMapper.selectOne(wrapper);
		if (task == null) {
			throw new BusinessException(ResultCode.NOT_FOUND, "研究任务不存在");
		}
		return task;
	}

}
