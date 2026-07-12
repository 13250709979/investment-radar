package com.investmentradar.common;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class ApiResponse<T> {

	private static final int SUCCESS_CODE = 0;
	private static final String SUCCESS_MESSAGE = "success";

	private int code;
	private String message;
	private T data;

	public static <T> ApiResponse<T> success(T data) {
		return new ApiResponse<>(SUCCESS_CODE, SUCCESS_MESSAGE, data);
	}

	public static <T> ApiResponse<T> success() {
		return success(null);
	}

	public static <T> ApiResponse<T> fail(int code, String message) {
		return new ApiResponse<>(code, message, null);
	}

}
