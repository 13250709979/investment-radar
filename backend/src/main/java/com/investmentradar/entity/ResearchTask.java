package com.investmentradar.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;

import java.time.LocalDateTime;

/**
 * 研究任务实体，对应表 investment_radar.research_task。
 */
@Data
@TableName(value = "research_task", schema = "investment_radar")
public class ResearchTask {

	@TableId(type = IdType.AUTO)
	private Long id;

	/** 业务任务 ID（UUID） */
	private String taskId;

	private String companyName;

	private String stockCode;

	private String market;

	/** 任务状态：PENDING / RUNNING / SUCCESS / FAILED */
	private String status;

	/** 执行进度（0-100） */
	private Integer progress;

	private Long reportId;

	private String errorMessage;

	private LocalDateTime createdAt;

	private LocalDateTime updatedAt;

}
