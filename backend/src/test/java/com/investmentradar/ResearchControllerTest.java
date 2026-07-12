package com.investmentradar;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.investmentradar.dto.request.CreateResearchRequest;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.web.servlet.MockMvc;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@SpringBootTest
@AutoConfigureMockMvc
@ActiveProfiles("test")
class ResearchControllerTest {

	@Autowired
	private MockMvc mockMvc;

	@Autowired
	private ObjectMapper objectMapper;

	@Test
	void createResearchShouldReturnTaskId() throws Exception {
		CreateResearchRequest request = new CreateResearchRequest();
		request.setCompanyName("隆基绿能");
		request.setStockCode("601012");

		mockMvc.perform(post("/api/research")
						.contentType(MediaType.APPLICATION_JSON)
						.content(objectMapper.writeValueAsString(request)))
				.andExpect(status().isOk())
				.andExpect(jsonPath("$.code").value(200))
				.andExpect(jsonPath("$.data.taskId").isNotEmpty())
				.andExpect(jsonPath("$.data.status").value("PENDING"));
	}

	@Test
	void getTaskStatusShouldReturnNotFoundWhenMissing() throws Exception {
		mockMvc.perform(get("/api/research/not-exists-task-id"))
				.andExpect(status().isOk())
				.andExpect(jsonPath("$.code").value(404))
				.andExpect(jsonPath("$.message").value("研究任务不存在"));
	}

	@Test
	void listTasksShouldReturnArray() throws Exception {
		mockMvc.perform(get("/api/task/list"))
				.andExpect(status().isOk())
				.andExpect(jsonPath("$.code").value(200))
				.andExpect(jsonPath("$.data").isArray());
	}

}
