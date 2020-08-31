--
-- Выводим дату и результат распознавания
--

SELECT datetime, result 
FROM voice_call 
WHERE datetime>'2020-08-01' and datetime<'2020-09-01';


--
-- Далее для каждого результата распознавания: кол-во за каждую дату (если указан промежуток), длительность всех аудио, проект и сервер.
--

SELECT datetime::TIMESTAMP::DATE as date, COUNT(CASE WHEN result THEN 1 END) as results, SUM(duration) as total_duration, 
project.name as project_name, server.name as server_name, server.ip_address
FROM voice_call
JOIN project ON project.id = voice_call.project_id
JOIN server ON server.id = voice_call.server_id 
WHERE datetime>'2020-08-01' and datetime<'2020-09-01'
GROUP BY date, project_name, server_name, server.ip_address;
