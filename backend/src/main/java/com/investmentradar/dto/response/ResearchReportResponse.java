package com.investmentradar.dto.response;

import lombok.AllArgsConstructor;
import lombok.Data;

import java.time.LocalDateTime;

@Data
@AllArgsConstructor
public class ResearchReportResponse {

	private String taskId;

	private String companyName;

	private String reportMarkdown;

	private String aiModel;

	private Integer reportVersion;

	private LocalDateTime createdAt;

}
