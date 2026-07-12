package com.investmentradar.dto.response;

import lombok.AllArgsConstructor;
import lombok.Data;

@Data
@AllArgsConstructor
public class ResearchTaskStatusResponse {

	private String taskId;

	private String status;

	private Integer progress;

}
