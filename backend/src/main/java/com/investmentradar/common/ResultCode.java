package com.investmentradar.common;

public enum ResultCode {

	SUCCESS(200, "success"),
	BAD_REQUEST(400, "请求参数错误"),
	UNAUTHORIZED(401, "未授权"),
	FORBIDDEN(403, "禁止访问"),
	NOT_FOUND(404, "资源不存在"),
	INTERNAL_ERROR(500, "系统异常");

	private final Integer code;
	private final String message;

	ResultCode(Integer code, String message) {
		this.code = code;
		this.message = message;
	}

	public Integer getCode() {
		return code;
	}

	public String getMessage() {
		return message;
	}

}
