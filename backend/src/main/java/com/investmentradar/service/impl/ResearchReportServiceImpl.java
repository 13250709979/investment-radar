package com.investmentradar.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.investmentradar.common.ResultCode;
import com.investmentradar.dto.response.ResearchReportResponse;
import com.investmentradar.entity.ResearchReport;
import com.investmentradar.exception.BusinessException;
import com.investmentradar.mapper.ResearchReportMapper;
import com.investmentradar.service.ResearchReportService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class ResearchReportServiceImpl implements ResearchReportService {

	@Autowired
	private ResearchReportMapper researchReportMapper;

	@Override
	public ResearchReportResponse getReportByTaskId(String taskId) {
		LambdaQueryWrapper<ResearchReport> wrapper = new LambdaQueryWrapper<ResearchReport>()
				.eq(ResearchReport::getTaskId, taskId)
				.orderByDesc(ResearchReport::getReportVersion)
				.last("LIMIT 1");
		ResearchReport report = researchReportMapper.selectOne(wrapper);
		if (report == null) {
			throw new BusinessException(ResultCode.NOT_FOUND, "研究报告不存在");
		}
		return new ResearchReportResponse(
				report.getTaskId(),
				report.getCompanyName(),
				report.getReportMarkdown(),
				report.getAiModel(),
				report.getReportVersion(),
				report.getCreatedAt());
	}

}
