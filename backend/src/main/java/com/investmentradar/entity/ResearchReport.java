package com.investmentradar.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;

import java.time.LocalDateTime;

@Data
@TableName(value = "research_report", schema = "investment_radar")
public class ResearchReport {

	@TableId(type = IdType.AUTO)
	private Long id;

	private String taskId;

	private String companyName;

	private String reportMarkdown;

	private String aiModel;

	private Integer reportVersion;

	private LocalDateTime createdAt;

}
