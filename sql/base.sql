CREATE TABLE link (
	ID        INTEGER  PRIMARY KEY AUTOINCREMENT NOT NULL,
	HASH      TEXT                           NOT NULL,
	URL       TEXT                           NOT NULL,
	UNIQUE(HASH, URL)
);

INSERT INTO link (ID, HASH, URL)
VALUES (0, '5ababd603b', 'example.com');

CREATE TABLE schema_changes (
	ID        INTEGER  PRIMARY KEY AUTOINCREMENT NOT NULL,
	FILENAME      TEXT                           NOT NULL,
	EXECUTED      DATETIME                       NOT NULL
);

INSERT INTO schema_changes (FILENAME, EXECUTED)
VALUES ('base.sql', datetime());
