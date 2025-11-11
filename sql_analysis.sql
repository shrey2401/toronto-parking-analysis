USE toronto_parking_db;
-- Toronto Parking Analysis SQL Queries
-- Run these in MySQL Workbench to analyze parking ticket data

-- ============================================
-- 1. BASIC DATABASE CHECK
-- ============================================

-- How many total records do we have?
SELECT COUNT(*) as total_records 
FROM parking_tickets;

-- Show first 10 records to see the data
SELECT * 
FROM parking_tickets 
LIMIT 10;


-- ============================================
-- 2. SUMMARY STATISTICS
-- ============================================

-- Overall statistics about all tickets
SELECT 
    COUNT(*) as total_tickets,
    COUNT(DISTINCT DATE(date_of_infraction)) as unique_dates,
    COUNT(DISTINCT ward) as wards_affected,
    ROUND(AVG(set_fine_amount), 2) as avg_fine,
    MIN(set_fine_amount) as min_fine,
    MAX(set_fine_amount) as max_fine,
    SUM(set_fine_amount) as total_fines_issued
FROM parking_tickets;


-- ============================================
-- 3. TOP 15 INFRACTION TYPES
-- ============================================

-- Which parking violations are most common?
SELECT 
    infraction_description,
    COUNT(*) as frequency,
    ROUND(AVG(set_fine_amount), 2) as avg_fine,
    MIN(set_fine_amount) as min_fine,
    MAX(set_fine_amount) as max_fine
FROM parking_tickets
WHERE infraction_description IS NOT NULL
GROUP BY infraction_description
ORDER BY frequency DESC
LIMIT 15;


-- ============================================
-- 4. TICKETS BY WARD (Top 15)
-- ============================================

-- Which wards have the most parking tickets?
SELECT 
    ward,
    COUNT(*) as ticket_count,
    ROUND(AVG(set_fine_amount), 2) as avg_fine,
    SUM(set_fine_amount) as total_fines
FROM parking_tickets
WHERE ward IS NOT NULL
GROUP BY ward
ORDER BY ticket_count DESC
LIMIT 15;


-- ============================================
-- 5. MONTHLY TREND ANALYSIS
-- ============================================

-- How do tickets vary by month?
SELECT 
    DATE_FORMAT(date_of_infraction, '%Y-%m') as month,
    COUNT(*) as ticket_count,
    ROUND(AVG(set_fine_amount), 2) as avg_fine
FROM parking_tickets
WHERE date_of_infraction IS NOT NULL
GROUP BY DATE_FORMAT(date_of_infraction, '%Y-%m')
ORDER BY month;


-- ============================================
-- 6. FINE AMOUNT DISTRIBUTION
-- ============================================

-- How many tickets fall into each fine range?
SELECT 
    CASE 
        WHEN set_fine_amount < 50 THEN 'Under $50'
        WHEN set_fine_amount < 100 THEN '$50-$100'
        WHEN set_fine_amount < 150 THEN '$100-$150'
        WHEN set_fine_amount < 200 THEN '$150-$200'
        ELSE 'Over $200'
    END as fine_range,
    COUNT(*) as count,
    ROUND(100 * COUNT(*) / (SELECT COUNT(*) FROM parking_tickets WHERE set_fine_amount IS NOT NULL), 2) as percentage
FROM parking_tickets
WHERE set_fine_amount IS NOT NULL
GROUP BY fine_range
ORDER BY fine_range;


-- ============================================
-- 7. STREET ANALYSIS (Top 20 Streets)
-- ============================================

-- Which streets have the most parking tickets?
SELECT 
    location_street,
    COUNT(*) as ticket_count,
    ROUND(AVG(set_fine_amount), 2) as avg_fine
FROM parking_tickets
WHERE location_street IS NOT NULL AND location_street != ''
GROUP BY location_street
ORDER BY ticket_count DESC
LIMIT 20;


-- ============================================
-- 8. DAY OF WEEK ANALYSIS
-- ============================================

-- Do certain days of the week have more tickets?
SELECT 
    DAYNAME(date_of_infraction) as day_of_week,
    COUNT(*) as ticket_count,
    ROUND(AVG(set_fine_amount), 2) as avg_fine
FROM parking_tickets
WHERE date_of_infraction IS NOT NULL
GROUP BY DAYNAME(date_of_infraction), DAYOFWEEK(date_of_infraction)
ORDER BY DAYOFWEEK(date_of_infraction);


-- ============================================
-- 9. GEOSPATIAL SUMMARY (Coordinates)
-- ============================================

-- What's the geographic spread of parking tickets?
SELECT 
    COUNT(*) as total_with_coords,
    ROUND(AVG(latitude), 4) as avg_latitude,
    ROUND(AVG(longitude), 4) as avg_longitude,
    MIN(latitude) as min_latitude,
    MAX(latitude) as max_latitude,
    MIN(longitude) as min_longitude,
    MAX(longitude) as max_longitude
FROM parking_tickets
WHERE latitude IS NOT NULL AND longitude IS NOT NULL;


-- ============================================
-- 10. DATA QUALITY CHECK
-- ============================================

-- How much data is missing?
SELECT 
    'total_records' as metric,
    COUNT(*) as value
FROM parking_tickets
UNION ALL
SELECT 'null_dates', COUNT(*) FROM parking_tickets WHERE date_of_infraction IS NULL
UNION ALL
SELECT 'null_wards', COUNT(*) FROM parking_tickets WHERE ward IS NULL
UNION ALL
SELECT 'null_fines', COUNT(*) FROM parking_tickets WHERE set_fine_amount IS NULL
UNION ALL
SELECT 'null_streets', COUNT(*) FROM parking_tickets WHERE location_street IS NULL
UNION ALL
SELECT 'null_coords', COUNT(*) FROM parking_tickets WHERE latitude IS NULL OR longitude IS NULL;