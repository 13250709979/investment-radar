package com.investmentradar.config;

import org.apache.ibatis.type.BaseTypeHandler;
import org.apache.ibatis.type.JdbcType;
import org.apache.ibatis.type.MappedJdbcTypes;
import org.apache.ibatis.type.MappedTypes;
import org.postgresql.util.PGobject;

import java.sql.CallableStatement;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;

/**
 * PostgreSQL JSONB ↔ String；H2 等环境回退为普通字符串。
 */
@MappedTypes(String.class)
@MappedJdbcTypes(JdbcType.OTHER)
public class JsonbStringTypeHandler extends BaseTypeHandler<String> {

	@Override
	public void setNonNullParameter(PreparedStatement ps, int i, String parameter, JdbcType jdbcType)
			throws SQLException {
		String product = ps.getConnection().getMetaData().getDatabaseProductName();
		if (product != null && product.toLowerCase().contains("postgresql")) {
			PGobject jsonObject = new PGobject();
			jsonObject.setType("jsonb");
			jsonObject.setValue(parameter);
			ps.setObject(i, jsonObject);
			return;
		}
		ps.setString(i, parameter);
	}

	@Override
	public String getNullableResult(ResultSet rs, String columnName) throws SQLException {
		return toString(rs.getObject(columnName));
	}

	@Override
	public String getNullableResult(ResultSet rs, int columnIndex) throws SQLException {
		return toString(rs.getObject(columnIndex));
	}

	@Override
	public String getNullableResult(CallableStatement cs, int columnIndex) throws SQLException {
		return toString(cs.getObject(columnIndex));
	}

	private String toString(Object value) {
		if (value == null) {
			return null;
		}
		if (value instanceof PGobject) {
			return ((PGobject) value).getValue();
		}
		return String.valueOf(value);
	}

}
