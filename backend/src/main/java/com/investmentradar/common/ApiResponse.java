package com.investmentradar.common;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class ApiResponse<T> {

	private Integer code;
	private String message;
	private T data;

	public static <T> ApiResponse<T> success(T data) {
		return of(ResultCode.SUCCESS, data);
	}

	public static <T> ApiResponse<T> success() {
		return success(null);
	}

	public static <T> ApiResponse<T> fail(ResultCode resultCode) {
		return of(resultCode, null);
	}

	public static <T> ApiResponse<T> fail(ResultCode resultCode, String message) {
		return new ApiResponse<>(resultCode.getCode(), message, null);
	}

	private static <T> ApiResponse<T> of(ResultCode resultCode, T data) {
		return new ApiResponse<>(resultCode.getCode(), resultCode.getMessage(), data);
	}

}
