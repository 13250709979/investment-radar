package com.investmentradar.dto.response;

import lombok.AllArgsConstructor;
import lombok.Data;

import java.time.LocalDateTime;

@Data
@AllArgsConstructor
public class ResearchTaskListItemResponse {

	private String taskId;

	private String companyName;

	private String stockCode;

	private String status;

	private Integer progress;

	private LocalDateTime createdAt;

}
