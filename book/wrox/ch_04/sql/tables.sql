DROP TABLE IF EXISTS WROX_SEARCH_CRAWL;
DROP TABLE IF EXISTS WROX_SEARCH_STOP_WORD;
DROP TABLE IF EXISTS WROX_SEARCH_INDEX;
DROP TABLE IF EXISTS WROX_SEARCH_DOCUMENT;
DROP TABLE IF EXISTS WROX_SEARCH_TERM;

CREATE TABLE WROX_SEARCH_CRAWL (
    DOCUMENT_URL  VARCHAR(255)  NOT NULL
)
ENGINE=InnoDB DEFAULT CHARACTER SET latin1
    COLLATE latin1_general_cs;

CREATE TABLE WROX_SEARCH_STOP_WORD (
    TERM_VALUE  VARCHAR(255)  NOT NULL
)
ENGINE=InnoDB DEFAULT CHARACTER SET latin1
    COLLATE latin1_general_cs;

CREATE TABLE WROX_SEARCH_DOCUMENT (
    DOCUMENT_ID     INTEGER UNSIGNED  NOT NULL  AUTO_INCREMENT,
    DOCUMENT_URL    VARCHAR(255)      NOT NULL,
    DOCUMENT_TITLE  VARCHAR(255),
    DESCRIPTION     VARCHAR(255),

    PRIMARY KEY (DOCUMENT_ID),

    CONSTRAINT UNIQUE (DOCUMENT_URL)
)
ENGINE=InnoDB DEFAULT CHARACTER SET latin1
    COLLATE latin1_general_cs AUTO_INCREMENT=0;

CREATE TABLE WROX_SEARCH_TERM (
    TERM_ID    INTEGER UNSIGNED  NOT NULL  AUTO_INCREMENT,
    TERM_VALUE VARCHAR(255)      NOT NULL,

    PRIMARY KEY (TERM_ID),

    CONSTRAINT UNIQUE (TERM_VALUE)
)
ENGINE=InnoDB DEFAULT CHARACTER SET latin1
    COLLATE latin1_general_cs AUTO_INCREMENT=0;

CREATE TABLE WROX_SEARCH_INDEX (
    TERM_ID       INTEGER UNSIGNED  NOT NULL,
    DOCUMENT_ID   INTEGER UNSIGNED  NOT NULL,
    OFFSET        INTEGER UNSIGNED  NOT NULL,

    PRIMARY KEY (DOCUMENT_ID, OFFSET),

    FOREIGN KEY (TERM_ID)
        REFERENCES WROX_SEARCH_TERM(TERM_ID),

    FOREIGN KEY (DOCUMENT_ID)
        REFERENCES WROX_SEARCH_DOCUMENT(DOCUMENT_ID)
)
ENGINE=InnoDB DEFAULT CHARACTER SET latin1
    COLLATE latin1_general_cs;

