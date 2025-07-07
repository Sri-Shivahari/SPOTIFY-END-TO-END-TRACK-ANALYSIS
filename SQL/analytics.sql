select * from spotify_tracks_;


SELECT track_name, artist, album, popularity
FROM spotify_tracks_
ORDER BY popularity DESC
LIMIT 1;


SELECT AVG(popularity) AS average_popularity
FROM spotify_tracks_;


SELECT track_name, artist, duration_minutes
FROM spotify_tracks_
WHERE duration_minutes > 4.0;

SELECT 
    CASE 
        WHEN popularity >= 80 THEN 'Very Popular'
        WHEN popularity >= 50 THEN 'Popular'
        ELSE 'Less Popular'
    END AS popularity_range,
    COUNT(*) AS track_count
FROM spotify_tracks_
GROUP BY popularity_range;