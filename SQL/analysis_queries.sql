CREATE TABLE rag_query_logs (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP,
    question TEXT NOT NULL,
    answer TEXT,
    sources TEXT
);

SELECT * FROM rag_query_logs;

SELECT *
FROM rag_query_logs
ORDER BY id;

--Total questions

SELECT COUNT(*) AS total_questions
FROM rag_query_logs;

--Latest questions

SELECT
    id,
    timestamp,
    question
FROM rag_query_logs
ORDER BY timestamp DESC;


--Questions by date

SELECT
    DATE(timestamp) AS question_date,
    COUNT(*) AS total_questions
FROM rag_query_logs
GROUP BY DATE(timestamp)
ORDER BY question_date;

--Questions containing specific words

SELECT
    id,
    question,
    answer
FROM rag_query_logs
WHERE question ILIKE '%annual report%';

SELECT
    sources,
    COUNT(*) AS usage_count
FROM rag_query_logs
GROUP BY sources
ORDER BY usage_count DESC;

