package com.investmentradar.dto.response;

import lombok.AllArgsConstructor;
import lombok.Data;

import java.util.List;

@Data
@AllArgsConstructor
public class AiAnalysisPageResponse {

	private Long total;

	private Integer page;

	private Integer size;

	private List<AiAnalysisResponse> items;

}
