package com.investmentradar.config;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Component;

import javax.sql.DataSource;
import java.sql.Connection;
import java.sql.SQLException;

@Component
public class DatabaseHealthChecker {

	private static final Logger log = LoggerFactory.getLogger(DatabaseHealthChecker.class);

	private final DataSource dataSource;

	public DatabaseHealthChecker(DataSource dataSource) {
		this.dataSource = dataSource;
	}

	public boolean checkConnection() {
		try (Connection connection = dataSource.getConnection()) {
			return connection.isValid(3);
		} catch (SQLException e) {
			log.error("数据库连接失败", e);
			return false;
		}
	}

	public void validateConnectionOrThrow() {
		if (!checkConnection()) {
			throw new IllegalStateException("数据库连接失败，请检查 PostgreSQL 服务及 application.yml 配置");
		}
	}

}
