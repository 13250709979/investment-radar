package com.investmentradar.controller;

import com.investmentradar.common.ApiResponse;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class TestController {

	@GetMapping("/test/error")
	public ApiResponse<String> testError() {
		int i = 1 / 0;
		return ApiResponse.success("OK");
	}

}
