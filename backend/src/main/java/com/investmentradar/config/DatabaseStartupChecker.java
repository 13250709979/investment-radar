package com.investmentradar.config;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.ApplicationArguments;
import org.springframework.boot.ApplicationRunner;
import org.springframework.stereotype.Component;

@Component
public class DatabaseStartupChecker implements ApplicationRunner {

	private static final Logger log = LoggerFactory.getLogger(DatabaseStartupChecker.class);

	private final DatabaseHealthChecker databaseHealthChecker;

	public DatabaseStartupChecker(DatabaseHealthChecker databaseHealthChecker) {
		this.databaseHealthChecker = databaseHealthChecker;
	}

	@Override
	public void run(ApplicationArguments args) {
		log.info("正在检查数据库连接...");
		databaseHealthChecker.validateConnectionOrThrow();
		log.info("数据库连接正常");
	}

}
