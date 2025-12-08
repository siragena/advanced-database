EXPLAIN QUERY PLAN
SELECT 
    t.Name   AS Track,
    a.Title  AS Album,
    ar.Name  AS Artist
FROM Track t
JOIN Album  a  ON t.AlbumId   = a.AlbumId
JOIN Artist ar ON a.ArtistId  = ar.ArtistId;

 