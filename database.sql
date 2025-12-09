-- ================================================
-- AHMED Bot Database Setup
-- قاعدة بيانات بوت AHMED
-- ================================================

-- إنشاء قاعدة البيانات
CREATE DATABASE IF NOT EXISTS demo CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE demo;

-- جدول المستخدمين
CREATE TABLE IF NOT EXISTS persons (
    id INT AUTO_INCREMENT PRIMARY KEY,
    userid BIGINT NOT NULL UNIQUE,
    username VARCHAR(255),
    firstname VARCHAR(255),
    role VARCHAR(50) DEFAULT 'USER',
    credits INT DEFAULT 0,
    is_premium BOOLEAN DEFAULT FALSE,
    is_banned BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    last_used TIMESTAMP NULL,
    INDEX idx_userid (userid),
    INDEX idx_role (role),
    INDEX idx_premium (is_premium)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- جدول المعاملات
CREATE TABLE IF NOT EXISTS transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    userid BIGINT NOT NULL,
    transaction_type ENUM('credit_purchase', 'credit_usage', 'premium_upgrade') NOT NULL,
    amount INT NOT NULL,
    balance_after INT NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (userid) REFERENCES persons(userid) ON DELETE CASCADE,
    INDEX idx_userid (userid),
    INDEX idx_type (transaction_type),
    INDEX idx_date (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- جدول سجل الاستخدام
CREATE TABLE IF NOT EXISTS usage_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    userid BIGINT NOT NULL,
    command VARCHAR(100) NOT NULL,
    input_data TEXT,
    result VARCHAR(50),
    credits_used INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (userid) REFERENCES persons(userid) ON DELETE CASCADE,
    INDEX idx_userid (userid),
    INDEX idx_command (command),
    INDEX idx_date (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- جدول المجموعات المسموحة
CREATE TABLE IF NOT EXISTS allowed_groups (
    id INT AUTO_INCREMENT PRIMARY KEY,
    group_id BIGINT NOT NULL UNIQUE,
    group_name VARCHAR(255),
    is_premium BOOLEAN DEFAULT FALSE,
    added_by BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_group_id (group_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- جدول BIN المحظورة
CREATE TABLE IF NOT EXISTS banned_bins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    bin_number VARCHAR(12) NOT NULL UNIQUE,
    reason VARCHAR(255),
    banned_by BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_bin (bin_number)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- جدول إعدادات النظام
CREATE TABLE IF NOT EXISTS system_settings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    setting_key VARCHAR(100) NOT NULL UNIQUE,
    setting_value TEXT,
    description VARCHAR(255),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_key (setting_key)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- إدراج إعدادات افتراضية
INSERT INTO system_settings (setting_key, setting_value, description) VALUES
('maintenance_mode', 'false', 'وضع الصيانة'),
('default_credits', '0', 'الرصيد الافتراضي للمستخدمين الجدد'),
('credit_cost_bin', '1', 'تكلفة فحص BIN'),
('credit_cost_gen', '0', 'تكلفة توليد البطاقات'),
('credit_cost_key', '5', 'تكلفة فحص المفتاح'),
('max_gen_cards', '20', 'الحد الأقصى لتوليد البطاقات'),
('bot_version', '1.0.0', 'إصدار البوت'),
('bot_owner', 'AHMED', 'مالك البوت')
ON DUPLICATE KEY UPDATE setting_value=VALUES(setting_value);

-- إنشاء مستخدم إداري افتراضي (قم بتغيير ID)
INSERT INTO persons (userid, username, firstname, role, credits, is_premium) VALUES
(1234567890, 'AHMED', 'AHMED', 'ADMIN', 999999, TRUE)
ON DUPLICATE KEY UPDATE role='ADMIN', is_premium=TRUE;

-- Views للاستعلامات الشائعة

-- عرض إحصائيات المستخدمين
CREATE OR REPLACE VIEW user_statistics AS
SELECT 
    role,
    COUNT(*) as user_count,
    SUM(credits) as total_credits,
    SUM(CASE WHEN is_premium THEN 1 ELSE 0 END) as premium_count,
    SUM(CASE WHEN is_banned THEN 1 ELSE 0 END) as banned_count
FROM persons
GROUP BY role;

-- عرض المستخدمين النشطين
CREATE OR REPLACE VIEW active_users AS
SELECT 
    p.userid,
    p.username,
    p.firstname,
    p.role,
    p.credits,
    p.is_premium,
    COUNT(u.id) as usage_count,
    MAX(u.created_at) as last_activity
FROM persons p
LEFT JOIN usage_logs u ON p.userid = u.userid
WHERE p.is_banned = FALSE
GROUP BY p.userid
HAVING last_activity >= DATE_SUB(NOW(), INTERVAL 7 DAY)
ORDER BY usage_count DESC;

-- عرض أكثر الأوامر استخداماً
CREATE OR REPLACE VIEW popular_commands AS
SELECT 
    command,
    COUNT(*) as usage_count,
    COUNT(DISTINCT userid) as unique_users,
    SUM(credits_used) as total_credits_used
FROM usage_logs
WHERE created_at >= DATE_SUB(NOW(), INTERVAL 30 DAY)
GROUP BY command
ORDER BY usage_count DESC;

-- Stored Procedures

-- إضافة رصيد للمستخدم
DELIMITER //
CREATE PROCEDURE IF NOT EXISTS add_credits(
    IN p_userid BIGINT,
    IN p_amount INT,
    IN p_description TEXT
)
BEGIN
    DECLARE current_credits INT;
    
    -- الحصول على الرصيد الحالي
    SELECT credits INTO current_credits FROM persons WHERE userid = p_userid;
    
    -- تحديث الرصيد
    UPDATE persons 
    SET credits = credits + p_amount,
        updated_at = CURRENT_TIMESTAMP
    WHERE userid = p_userid;
    
    -- تسجيل المعاملة
    INSERT INTO transactions (userid, transaction_type, amount, balance_after, description)
    VALUES (p_userid, 'credit_purchase', p_amount, current_credits + p_amount, p_description);
END //
DELIMITER ;

-- خصم رصيد من المستخدم
DELIMITER //
CREATE PROCEDURE IF NOT EXISTS deduct_credits(
    IN p_userid BIGINT,
    IN p_amount INT,
    IN p_description TEXT
)
BEGIN
    DECLARE current_credits INT;
    
    -- الحصول على الرصيد الحالي
    SELECT credits INTO current_credits FROM persons WHERE userid = p_userid;
    
    -- التحقق من وجود رصيد كافٍ
    IF current_credits >= p_amount THEN
        -- خصم الرصيد
        UPDATE persons 
        SET credits = credits - p_amount,
            updated_at = CURRENT_TIMESTAMP
        WHERE userid = p_userid;
        
        -- تسجيل المعاملة
        INSERT INTO transactions (userid, transaction_type, amount, balance_after, description)
        VALUES (p_userid, 'credit_usage', -p_amount, current_credits - p_amount, p_description);
    END IF;
END //
DELIMITER ;

-- تسجيل استخدام أمر
DELIMITER //
CREATE PROCEDURE IF NOT EXISTS log_command_usage(
    IN p_userid BIGINT,
    IN p_command VARCHAR(100),
    IN p_input_data TEXT,
    IN p_result VARCHAR(50),
    IN p_credits_used INT
)
BEGIN
    -- تسجيل الاستخدام
    INSERT INTO usage_logs (userid, command, input_data, result, credits_used)
    VALUES (p_userid, p_command, p_input_data, p_result, p_credits_used);
    
    -- تحديث آخر استخدام
    UPDATE persons 
    SET last_used = CURRENT_TIMESTAMP
    WHERE userid = p_userid;
END //
DELIMITER ;

-- تنظيف السجلات القديمة (تشغيل دوري)
DELIMITER //
CREATE PROCEDURE IF NOT EXISTS cleanup_old_logs()
BEGIN
    -- حذف سجلات الاستخدام الأقدم من 90 يوم
    DELETE FROM usage_logs 
    WHERE created_at < DATE_SUB(NOW(), INTERVAL 90 DAY);
    
    -- حذف المعاملات القديمة (أقدم من سنة)
    DELETE FROM transactions 
    WHERE created_at < DATE_SUB(NOW(), INTERVAL 1 YEAR);
END //
DELIMITER ;

-- ================================================
-- إنشاء فهارس إضافية لتحسين الأداء
-- ================================================

-- فهرس مركب للاستعلامات الشائعة
CREATE INDEX idx_user_role_premium ON persons(role, is_premium);
CREATE INDEX idx_transaction_user_type ON transactions(userid, transaction_type);
CREATE INDEX idx_usage_user_command ON usage_logs(userid, command);

-- ================================================
-- منح الصلاحيات (إذا لزم الأمر)
-- ================================================

-- GRANT ALL PRIVILEGES ON demo.* TO 'your_user'@'localhost';
-- FLUSH PRIVILEGES;

-- ================================================
-- إكمال الإعداد
-- ================================================

SELECT 'Database setup completed successfully!' as Status;
SELECT COUNT(*) as total_users FROM persons;
SELECT * FROM system_settings;