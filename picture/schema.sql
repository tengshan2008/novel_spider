CREATE TABLE IF NOT EXISTS `picture_miss` (
    `id` INTEGER PRIMARY KEY AUTOINCERMENT,
    `title` TEXT NOT NULL,
    `url` TEXT NOT NULL,
    `filename` TEXT NOT NULL,
    `created` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
)