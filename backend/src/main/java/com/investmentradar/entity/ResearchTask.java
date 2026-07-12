package com.investmentradar.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;

import java.time.LocalDateTime;

@Data
@TableName(value = "research_task", schema = "investment_radar")
public class ResearchTask {

	@TableId(type = IdType.AUTO)
	private Long id;

	private String taskId;

	private String companyName;

	private String stockCode;

	private String market;

	private String status;

	private Integer progress;

	private Long reportId;

	private String errorMessage;

	private LocalDateTime createdAt;

	private LocalDateTime updatedAt;

}
