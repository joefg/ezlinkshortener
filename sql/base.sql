CREATE TABLE link (
	ID        INTEGER  PRIMARY KEY AUTOINCREMENT NOT NULL,
	HASH      TEXT                           NOT NULL,
	URL       TEXT                           NOT NULL,
	UNIQUE(HASH, URL)
);

INSERT INTO link (ID, HASH, URL)
VALUES (0, '5ababd603b', 'example.com')
