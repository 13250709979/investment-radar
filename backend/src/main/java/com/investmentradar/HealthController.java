package com.investmentradar;

import com.investmentradar.common.ApiResponse;
import com.investmentradar.dto.HealthData;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class HealthController {

	@GetMapping("/health")
	public ApiResponse<HealthData> health() {
		return ApiResponse.success(new HealthData("UP"));
	}

}
