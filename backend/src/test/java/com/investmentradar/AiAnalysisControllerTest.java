package com.investmentradar;

import com.investmentradar.entity.AiAnalysis;
import com.investmentradar.mapper.AiAnalysisMapper;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.web.servlet.MockMvc;

import java.time.LocalDateTime;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@SpringBootTest
@AutoConfigureMockMvc
@ActiveProfiles("test")
class AiAnalysisControllerTest {

	@Autowired
	private MockMvc mockMvc;

	@Autowired
	private AiAnalysisMapper aiAnalysisMapper;

	private Long savedId;

	@BeforeEach
	void setUp() {
		aiAnalysisMapper.delete(null);

		AiAnalysis row = new AiAnalysis();
		row.setDataType("ANNOUNCEMENT");
		row.setDataId(1001L);
		row.setCompanyCode("601012");
		row.setCompanyName("隆基绿能");
		row.setIndustry("光伏");
		row.setEventType("扩产");
		row.setEventLevel(4);
		row.setSentiment("POSITIVE");
		row.setTitle("扩产公告");
		row.setSummary("公司拟扩产硅片产能");
		row.setReasoning("产能扩张有利于份额提升");
		row.setInvestmentOpinion("关注执行进度");
		row.setRiskWarning("扩产落地不及预期");
		row.setTags("[\"扩产\",\"光伏\"]");
		row.setModelProvider("GoogleAIStudio");
		row.setModelName("gemini-2.5-flash");
		row.setPromptVersion("v1.0");
		row.setInputTokens(100);
		row.setOutputTokens(50);
		row.setTotalTokens(150);
		row.setAnalysisStatus(1);
		row.setAnalysisTime(LocalDateTime.of(2026, 7, 15, 12, 0));
		row.setCreateTime(LocalDateTime.of(2026, 7, 15, 12, 0));
		row.setUpdateTime(LocalDateTime.of(2026, 7, 15, 12, 0));
		aiAnalysisMapper.insert(row);
		savedId = row.getId();
	}

	@Test
	void listShouldReturnPagedItems() throws Exception {
		mockMvc.perform(get("/api/ai-analysis")
						.param("companyCode", "601012")
						.param("analysisStatus", "1")
						.param("page", "1")
						.param("size", "10"))
				.andExpect(status().isOk())
				.andExpect(jsonPath("$.code").value(200))
				.andExpect(jsonPath("$.data.total").value(1))
				.andExpect(jsonPath("$.data.items[0].companyCode").value("601012"))
				.andExpect(jsonPath("$.data.items[0].eventType").value("扩产"))
				.andExpect(jsonPath("$.data.items[0].summary").value("公司拟扩产硅片产能"))
				.andExpect(jsonPath("$.data.items[0].reasoning").doesNotExist());
	}

	@Test
	void getByIdShouldReturnDetail() throws Exception {
		mockMvc.perform(get("/api/ai-analysis/" + savedId))
				.andExpect(status().isOk())
				.andExpect(jsonPath("$.code").value(200))
				.andExpect(jsonPath("$.data.id").value(savedId))
				.andExpect(jsonPath("$.data.reasoning").value("产能扩张有利于份额提升"))
				.andExpect(jsonPath("$.data.investmentOpinion").value("关注执行进度"))
				.andExpect(jsonPath("$.data.riskWarning").value("扩产落地不及预期"));
	}

	@Test
	void getByIdShouldReturnNotFoundWhenMissing() throws Exception {
		mockMvc.perform(get("/api/ai-analysis/999999"))
				.andExpect(status().isOk())
				.andExpect(jsonPath("$.code").value(404))
				.andExpect(jsonPath("$.message").value("AI分析结果不存在"));
	}

}
