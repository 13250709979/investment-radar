package com.investmentradar.controller;

import com.investmentradar.common.ApiResponse;
import com.investmentradar.dto.response.HealthData;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class HealthController {

	@GetMapping("/health")
	public ApiResponse<HealthData> health() {
		return ApiResponse.success(new HealthData("UP"));
	}

}
