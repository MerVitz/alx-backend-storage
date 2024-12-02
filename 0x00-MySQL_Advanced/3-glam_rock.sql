-- List bands with Glam Rock as main style, ranked by longevity
SELECT 
    name AS band_name,
    (2022 - formed) - (CASE WHEN split IS NOT NULL THEN (2022 - split) ELSE 0 END) AS lifespan
FROM 
    metal_bands
WHERE 
    main_style = 'Glam rock'
ORDER BY 
    lifespan DESC;

