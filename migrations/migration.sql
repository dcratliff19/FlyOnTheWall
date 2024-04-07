-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: db
-- Generation Time: Apr 02, 2024 at 12:13 PM
-- Server version: 8.3.0
-- PHP Version: 8.2.17

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

--
-- Database: `sound`
--

-- --------------------------------------------------------

--
-- Table structure for table `raw_sounds`
--

CREATE TABLE `raw_sounds` (
  `id` int NOT NULL,
  `raw_audio_bytes` longblob NOT NULL,
  `class_1` text NOT NULL,
  `class_2` text NOT NULL,
  `class_3` text NOT NULL,
  `class_4` text NOT NULL,
  `class_5` text NOT NULL,
  `class_1_percent` float NOT NULL,
  `class_2_percent` float NOT NULL,
  `class_3_percent` float NOT NULL,
  `class_4_percent` float NOT NULL,
  `class_5_percent` float NOT NULL,
  `decibel_reading` float NOT NULL,
  `record_datetime` datetime NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `raw_sounds`
--
ALTER TABLE `raw_sounds`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `raw_sounds`
--
ALTER TABLE `raw_sounds`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;
COMMIT;