-- 骨质疏松症随访系统数据库初始化脚本

-- 创建扩展
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- 创建用户类型枚举
CREATE TYPE user_type AS ENUM ('institutional', 'personal');
CREATE TYPE gender AS ENUM ('male', 'female');
CREATE TYPE risk_level AS ENUM ('low', 'medium', 'high');
CREATE TYPE report_type AS ENUM ('dxa', 'ct', 'xray', 'blood', 'other');
CREATE TYPE report_status AS ENUM ('pending', 'processing', 'completed', 'error');
CREATE TYPE followup_status AS ENUM ('scheduled', 'in_progress', 'completed', 'cancelled', 'missed');
CREATE TYPE followup_type AS ENUM ('bone_density', 'medication_review', 'lifestyle_assessment', 'general_checkup', 'emergency');

-- 创建用户表
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    user_type user_type NOT NULL,
    institution VARCHAR(200),
    department VARCHAR(100),
    age INTEGER,
    gender gender,
    is_active BOOLEAN DEFAULT TRUE,
    is_verified BOOLEAN DEFAULT FALSE,
    avatar VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 创建患者表
CREATE TABLE IF NOT EXISTS patients (
    id SERIAL PRIMARY KEY,
    patient_id VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    age INTEGER NOT NULL,
    gender gender NOT NULL,
    phone VARCHAR(20),
    email VARCHAR(100),
    address TEXT,
    height FLOAT,
    weight FLOAT,
    bmi FLOAT,
    t_score FLOAT,
    z_score FLOAT,
    risk_level risk_level DEFAULT 'medium',
    medical_history TEXT,
    family_history TEXT,
    medications TEXT,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 创建报告表
CREATE TABLE IF NOT EXISTS reports (
    id SERIAL PRIMARY KEY,
    report_id VARCHAR(50) UNIQUE NOT NULL,
    patient_id INTEGER REFERENCES patients(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    report_type report_type NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    file_path VARCHAR(500),
    file_size INTEGER,
    t_score FLOAT,
    z_score FLOAT,
    bone_density FLOAT,
    risk_assessment TEXT,
    ai_analysis TEXT,
    ai_recommendations TEXT,
    status report_status DEFAULT 'pending',
    processing_start_time TIMESTAMP WITH TIME ZONE,
    processing_end_time TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 创建随访表
CREATE TABLE IF NOT EXISTS followups (
    id SERIAL PRIMARY KEY,
    followup_id VARCHAR(50) UNIQUE NOT NULL,
    patient_id INTEGER REFERENCES patients(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    followup_type followup_type NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    scheduled_date TIMESTAMP WITH TIME ZONE NOT NULL,
    actual_date TIMESTAMP WITH TIME ZONE,
    duration_minutes INTEGER DEFAULT 30,
    status followup_status DEFAULT 'scheduled',
    is_reminder_sent BOOLEAN DEFAULT FALSE,
    reminder_sent_at TIMESTAMP WITH TIME ZONE,
    findings TEXT,
    recommendations TEXT,
    next_followup_date TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 创建随访应答表
CREATE TABLE IF NOT EXISTS followup_responses (
    id SERIAL PRIMARY KEY,
    followup_id INTEGER REFERENCES followup_records(id) ON DELETE CASCADE,
    patient_id INTEGER REFERENCES patients(id) ON DELETE CASCADE,
    response_time TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    is_completed BOOLEAN DEFAULT FALSE,
    overall_feeling VARCHAR(100),
    improvement_level VARCHAR(100),
    medication_adherence VARCHAR(100),
    exercise_volume TEXT,
    diet_adjustment TEXT,
    pain_level INTEGER CHECK (pain_level >= 1 AND pain_level <= 10),
    sleep_quality VARCHAR(100),
    daily_activity VARCHAR(100),
    mood_status VARCHAR(100),
    social_activity VARCHAR(100),
    side_effects TEXT,
    concerns TEXT,
    suggestions TEXT,
    additional_info TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 创建提醒日志表
CREATE TABLE IF NOT EXISTS reminder_logs (
    id SERIAL PRIMARY KEY,
    followup_id INTEGER REFERENCES followups(id) ON DELETE CASCADE,
    reminder_type VARCHAR(50) NOT NULL,
    sent_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'sent',
    message TEXT,
    recipient VARCHAR(100)
);

-- 创建系统日志表
CREATE TABLE IF NOT EXISTS system_logs (
    id SERIAL PRIMARY KEY,
    level VARCHAR(10) NOT NULL,
    message TEXT NOT NULL,
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 创建索引
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_patients_patient_id ON patients(patient_id);
CREATE INDEX idx_patients_user_id ON patients(user_id);
CREATE INDEX idx_reports_report_id ON reports(report_id);
CREATE INDEX idx_reports_patient_id ON reports(patient_id);
CREATE INDEX idx_reports_user_id ON reports(user_id);
CREATE INDEX idx_reports_status ON reports(status);
CREATE INDEX idx_followups_followup_id ON followups(followup_id);
CREATE INDEX idx_followups_patient_id ON followups(patient_id);
CREATE INDEX idx_followups_user_id ON followups(user_id);
CREATE INDEX idx_followups_scheduled_date ON followups(scheduled_date);
CREATE INDEX idx_followups_status ON followups(status);

-- 创建全文搜索索引
CREATE INDEX idx_patients_name_gin ON patients USING gin(name gin_trgm_ops);
CREATE INDEX idx_reports_title_gin ON reports USING gin(title gin_trgm_ops);
CREATE INDEX idx_followups_title_gin ON followups USING gin(title gin_trgm_ops);

-- 创建触发器函数
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- 创建触发器
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_patients_updated_at BEFORE UPDATE ON patients
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_reports_updated_at BEFORE UPDATE ON reports
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_followups_updated_at BEFORE UPDATE ON followups
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- 插入测试数据
INSERT INTO users (username, email, hashed_password, name, user_type, institution, department) VALUES
('admin', 'admin@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4tbQJ8Kj1G', '系统管理员', 'institutional', '测试医院', '骨科'),
('doctor1', 'doctor1@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4tbQJ8Kj1G', '张医生', 'institutional', '测试医院', '骨科'),
('patient1', 'patient1@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4tbQJ8Kj1G', '李患者', 'personal', '测试医院', NULL)
ON CONFLICT (username) DO NOTHING;

-- 插入测试患者数据
INSERT INTO patients (patient_id, name, age, gender, phone, email, height, weight, bmi, t_score, z_score, risk_level, user_id) VALUES
('P001', '张三', 65, 'female', '13800138001', 'zhangsan@example.com', 160, 55, 21.5, -2.5, -1.8, 'medium', 2),
('P002', '李四', 72, 'male', '13800138002', 'lisi@example.com', 170, 68, 23.5, -3.2, -2.1, 'high', 2),
('P003', '王五', 58, 'female', '13800138003', 'wangwu@example.com', 155, 50, 20.8, -1.8, -1.2, 'low', 2)
ON CONFLICT (patient_id) DO NOTHING; 