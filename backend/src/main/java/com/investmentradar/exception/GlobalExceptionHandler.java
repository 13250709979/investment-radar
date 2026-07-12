package com.investmentradar.exception;

import com.investmentradar.common.ApiResponse;
import com.investmentradar.common.ResultCode;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.converter.HttpMessageNotReadableException;
import org.springframework.validation.BindException;
import org.springframework.web.HttpRequestMethodNotSupportedException;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.MissingServletRequestParameterException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

import javax.validation.ConstraintViolationException;
import java.util.stream.Collectors;

@RestControllerAdvice
public class GlobalExceptionHandler {

	private static final Logger log = LoggerFactory.getLogger(GlobalExceptionHandler.class);

	@ExceptionHandler(BusinessException.class)
	public ApiResponse<Void> handleBusinessException(BusinessException e) {
		if (e.getMessage() != null && !e.getMessage().equals(e.getResultCode().getMessage())) {
			return ApiResponse.fail(e.getResultCode(), e.getMessage());
		}
		return ApiResponse.fail(e.getResultCode());
	}

	@ExceptionHandler({
			MethodArgumentNotValidException.class,
			BindException.class,
			ConstraintViolationException.class,
			MissingServletRequestParameterException.class,
			HttpMessageNotReadableException.class
	})
	public ApiResponse<Void> handleBadRequest(Exception e) {
		return ApiResponse.fail(ResultCode.BAD_REQUEST, extractMessage(e));
	}

	@ExceptionHandler(HttpRequestMethodNotSupportedException.class)
	public ApiResponse<Void> handleMethodNotSupported(HttpRequestMethodNotSupportedException e) {
		return ApiResponse.fail(ResultCode.BAD_REQUEST, e.getMessage());
	}

	@ExceptionHandler(Exception.class)
	public ApiResponse<Void> handleException(Exception e) {
		log.error("系统异常", e);
		return ApiResponse.fail(ResultCode.INTERNAL_ERROR);
	}

	private String extractMessage(Exception e) {
		if (e instanceof MethodArgumentNotValidException) {
			MethodArgumentNotValidException ex = (MethodArgumentNotValidException) e;
			return ex.getBindingResult().getFieldErrors().stream()
					.map(error -> error.getField() + ": " + error.getDefaultMessage())
					.collect(Collectors.joining(", "));
		}
		if (e instanceof BindException) {
			BindException ex = (BindException) e;
			return ex.getBindingResult().getFieldErrors().stream()
					.map(error -> error.getField() + ": " + error.getDefaultMessage())
					.collect(Collectors.joining(", "));
		}
		if (e instanceof ConstraintViolationException) {
			ConstraintViolationException ex = (ConstraintViolationException) e;
			return ex.getConstraintViolations().stream()
					.map(violation -> violation.getPropertyPath() + ": " + violation.getMessage())
					.collect(Collectors.joining(", "));
		}
		return e.getMessage();
	}

}
