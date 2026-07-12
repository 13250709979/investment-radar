package com.investmentradar.controller;

import com.investmentradar.common.ApiResponse;
import com.investmentradar.config.DatabaseHealthChecker;
import com.investmentradar.dto.response.HealthData;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class HealthController {

	private final DatabaseHealthChecker databaseHealthChecker;

	public HealthController(DatabaseHealthChecker databaseHealthChecker) {
		this.databaseHealthChecker = databaseHealthChecker;
	}

	@GetMapping("/health")
	public ApiResponse<HealthData> health() {
		boolean databaseUp = databaseHealthChecker.checkConnection();
		String databaseStatus = databaseUp ? "UP" : "DOWN";
		String status = databaseUp ? "UP" : "DOWN";
		return ApiResponse.success(new HealthData(status, databaseStatus));
	}

}
