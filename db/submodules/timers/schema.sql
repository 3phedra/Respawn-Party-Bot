CREATE TABLE IF NOT EXISTS `reminders` (
    `id` int(11) NOT NULL,
    `user_id` varchar(20) NOT NULL,
    `server_id` varchar(20) NOT NULL,
    `reason` varchar(255) NOT NULL,
    `termination_time` varchar(11) NOT NULL,
    `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
    );