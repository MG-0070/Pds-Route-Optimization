-- phpMyAdmin SQL Dump
-- version 5.3.0-dev+20220709.4e08d2933b
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Feb 21, 2024 at 10:27 AM
-- Server version: 10.4.24-MariaDB
-- PHP Version: 8.1.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `pds`
--

-- --------------------------------------------------------

--
-- Table structure for table `districts`
--

CREATE TABLE `districts` (
  `id` varchar(50) NOT NULL,
  `name` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `districts`
--

INSERT INTO `districts` (`id`, `name`) VALUES
('65916ff76ad42', 'Amritsar'),
('659170076048c', 'Jalandhar'),
('65917012bfdfb', 'Ludhiana'),
('6591702263283', 'Pathankot'),
('6591709952cb4', 'Barnala'),
('659170aa56a86', 'Bathinda'),
('659170c19ae28', 'Faridkot'),
('659170da36eda', 'Fatehgarh Sahib'),
('659170febfd37', 'Firozpur'),
('6591710f723e3', 'Fazilka'),
('65917121e4326', 'Gurdaspur'),
('659171317e8cb', 'Hoshiapur'),
('65917144285b8', 'Kapurthala'),
('6591715d70045', 'Malerkotla '),
('6591716a0b936', 'Mansa'),
('65917174ee871', 'Moga'),
('65917188c216d', 'Sri Muktsar Sahib'),
('6591719b58050', 'Patiala'),
('659171adcdfb9', 'Rupnagar'),
('659171bed6792', 'SAS Nagar'),
('659171d335e05', 'SBS Nagar'),
('659171df3fb53', 'Sangrur'),
('659171f04260c', 'Tarn Taran');

-- --------------------------------------------------------

--
-- Table structure for table `fps`
--

CREATE TABLE `fps` (
  `district` varchar(100) NOT NULL,
  `name` varchar(100) NOT NULL,
  `id` varchar(100) NOT NULL,
  `type` varchar(100) NOT NULL,
  `demand` varchar(100) NOT NULL,
  `longitude` varchar(100) NOT NULL,
  `latitude` varchar(100) NOT NULL,
  `uniqueid` varchar(100) NOT NULL,
  `active` varchar(10) NOT NULL DEFAULT '1'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `fps`
--

INSERT INTO `fps` (`district`, `name`, `id`, `type`, `demand`, `longitude`, `latitude`, `uniqueid`, `active`) VALUES
('Gurdaspur', 'achd1', '103500300077', 'Motarable', '1.103141514', '75.0894', '32.01964', 'FPS_65d599374e5', '1'),
('Gurdaspur', 'achd2', '103500500124', 'Motarable', '26.57132167', '75.3264', '31.9164', 'FPS_65d59937503', '1'),
('Gurdaspur', 'achd3', '103500700168', 'Motarable', '16.59508538', '75.53278', '32.14334', 'FPS_65d5993750f', '1'),
('Amritsar', 'achd', '104900100029', 'Motarable', '1.199066863', '74.7617', '31.8550855', 'FPS_65d599a8eaf', '1'),
('Amritsar', 'achd', '104900400001', 'Motarable', '0.479626745', '74.809569', '31.630867', 'FPS_65d599a8f03', '1'),
('Amritsar', 'achd', '104900600009', 'Motarable', '64.03017046', '74.8529521', '31.6640351', 'FPS_65d599a8f27', '1'),
('Tarntaran', 'achd', '105000111623', 'Motarable', '1.294992212', '74.62712', '31.35369', 'FPS_65d599a8f30', '1'),
('Tarntaran', 'achd', '105000200006', 'Motarable', '0.431664071', '74.99141', '31.31129', 'FPS_65d599a8f39', '1'),
('Tarntaran', 'achd', '105000220008', 'Motarable', '28.48982865', '75.0226', '31.28307', 'FPS_65d599a9000', '1'),
('Rupnagar', 'achd', '105100880014', 'Motarable', '43.4541831', '76.538992', '30.96257', 'FPS_65d599a9009', '1'),
('Sasnagar', 'achd', '105200200005', 'Motarable', '77.65157002', '76.91577438', '30.36825993', 'FPS_65d599a9016', '1'),
('Sasnagar', 'achd', '105200200006', 'Motarable', '56.93169463', '76.93292074', '30.3934594', 'FPS_65d599a9023', '1'),
('Sangrur', 'achd', '105300300027', 'Motarable', '25.37225481', '76.002432', '30.149695', 'FPS_65d599a902d', '1'),
('Sangrur', 'achd', '105300344416', 'Motarable', '24.2691133', '75.965421', '30.292187', 'FPS_65d599a9037', '1'),
('Sangrur', 'achd', '105300344417', 'Motarable', '27.33872447', '75.965421', '30.292187', 'FPS_65d599a9041', '1'),
('Barnala', 'achd', '105400660002', 'Motarable', '67.5314457', '75.645671', '30.503885', 'FPS_65d599a904a', '1'),
('Barnala', 'achd', '105400660003', 'Motarable', '26.76317237', '75.6480254', '30.484784', 'FPS_65d599a9055', '1'),
('Barnala', 'achd', '105400660004', 'Motarable', '38.13032623', '75.540993', '30.3685732', 'FPS_65d599a9061', '1'),
('Pathankot', 'achd', '164700400001', 'Motarable', '0.719440118', '75.690493', '32.383088', 'FPS_65d599a906a', '1'),
('Pathankot', 'achd', '164700400012', 'Motarable', '0.191850698', '75.696729', '32.382791', 'FPS_65d599a9073', '1'),
('Pathankot', 'achd', '164700600288', 'Motarable', '23.07004643', '75.64757', '32.27871', 'FPS_65d599a907e', '1'),
('Fazilka', 'achd', '164800400103', 'Motarable', '36.35570727', '73.94737', '30.38604', 'FPS_65d599a9087', '1'),
('Malerkotla', 'achd', '178100110071', 'Motarable', '45.08491403', '75.863632', '30.63047', 'FPS_65d599a9091', '1'),
('Malerkotla', 'achd', '178100110072', 'Motarable', '38.3701396', '75.840179', '30.66139', 'FPS_65d599a909f', '1'),
('Jalandhar', 'achd', '103700100001', 'Motarable', '36.93125937', '75.7320938', '31.3729002', 'FPS_65d599a90a7', '1'),
('Sbsnagar', 'achd', '103900100001', 'Motarable', '24.41300132', '75.906126', '31.1801118', 'FPS_65d599a90b0', '1'),
('Sbsnagar', 'achd', '103900100002', 'Motarable', '22.73430771', '75.9399325', '31.1711445', 'FPS_65d599a90b9', '1'),
('Fatehgarhsahib', 'achd', '104000100001', 'Motarable', '25.9478069', '76.1529235', '30.5580174', 'FPS_65d599a90c2', '1'),
('Fatehgarhsahib', 'achd', '104000100002', 'Motarable', '24.2691133', '76.1800668', '30.554606', 'FPS_65d599a90cb', '1'),
('Moga', 'achd', '104200100001', 'Motarable', '52.99875532', '75.00705', '30.5922538', 'FPS_65d599a90d4', '1'),
('Moga', 'achd', '104200100002', 'Motarable', '38.41810227', '75.0111266', '30.5106007', 'FPS_65d599a90e0', '1'),
('Ferozepur', 'achd', '104300100002', 'Motarable', '48.53822659', '74.4982767', '30.9426969', 'FPS_65d599a90ea', '1'),
('Ferozepur', 'achd', '104300100003', 'Motarable', '15.68379456', '74.54432', '30.9606', 'FPS_65d599a90f3', '1'),
('Bathinda', 'achd', '104600100002', 'Motarable', '10.02419897', '74.9467538', '30.2117102', 'FPS_65d599a90fb', '1'),
('Bathinda', 'achd', '104600100003', 'Motarable', '29.97667156', '74.9306622', '30.1902925', 'FPS_65d599a9104', '1'),
('Bathinda', 'achd', '104600100004', 'Motarable', '38.753841', '74.9423529', '30.1891729', 'FPS_65d599a910c', '1');

-- --------------------------------------------------------

--
-- Table structure for table `fps_vtqbekb2asz4qi`
--

CREATE TABLE `fps_vtqbekb2asz4qi` (
  `district` varchar(100) NOT NULL,
  `name` varchar(100) NOT NULL,
  `id` varchar(100) NOT NULL,
  `type` varchar(100) NOT NULL,
  `demand` varchar(100) NOT NULL,
  `longitude` varchar(100) NOT NULL,
  `latitude` varchar(100) NOT NULL,
  `uniqueid` varchar(100) NOT NULL,
  `active` varchar(10) NOT NULL DEFAULT '1'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `fps_vtqbekb2asz4qi`
--

INSERT INTO `fps_vtqbekb2asz4qi` (`district`, `name`, `id`, `type`, `demand`, `longitude`, `latitude`, `uniqueid`, `active`) VALUES
('Gurdaspur', 'achd1', '103500300077', 'Motarable', '1.103141514', '75.0894', '32.01964', 'FPS_65d599374e5', '1'),
('Gurdaspur', 'achd2', '103500500124', 'Motarable', '26.57132167', '75.3264', '31.9164', 'FPS_65d59937503', '1'),
('Gurdaspur', 'achd3', '103500700168', 'Motarable', '16.59508538', '75.53278', '32.14334', 'FPS_65d5993750f', '1'),
('Amritsar', 'achd', '104900100029', 'Motarable', '1.199066863', '74.7617', '31.8550855', 'FPS_65d599a8eaf', '1'),
('Amritsar', 'achd', '104900400001', 'Motarable', '0.479626745', '74.809569', '31.630867', 'FPS_65d599a8f03', '1'),
('Amritsar', 'achd', '104900600009', 'Motarable', '64.03017046', '74.8529521', '31.6640351', 'FPS_65d599a8f27', '1'),
('Tarntaran', 'achd', '105000111623', 'Motarable', '1.294992212', '74.62712', '31.35369', 'FPS_65d599a8f30', '1'),
('Tarntaran', 'achd', '105000200006', 'Motarable', '0.431664071', '74.99141', '31.31129', 'FPS_65d599a8f39', '1'),
('Tarntaran', 'achd', '105000220008', 'Motarable', '28.48982865', '75.0226', '31.28307', 'FPS_65d599a9000', '1'),
('Rupnagar', 'achd', '105100880014', 'Motarable', '43.4541831', '76.538992', '30.96257', 'FPS_65d599a9009', '1'),
('Sasnagar', 'achd', '105200200005', 'Motarable', '77.65157002', '76.91577438', '30.36825993', 'FPS_65d599a9016', '1'),
('Sasnagar', 'achd', '105200200006', 'Motarable', '56.93169463', '76.93292074', '30.3934594', 'FPS_65d599a9023', '1'),
('Sangrur', 'achd', '105300300027', 'Motarable', '25.37225481', '76.002432', '30.149695', 'FPS_65d599a902d', '1'),
('Sangrur', 'achd', '105300344416', 'Motarable', '24.2691133', '75.965421', '30.292187', 'FPS_65d599a9037', '1'),
('Sangrur', 'achd', '105300344417', 'Motarable', '27.33872447', '75.965421', '30.292187', 'FPS_65d599a9041', '1'),
('Barnala', 'achd', '105400660002', 'Motarable', '67.5314457', '75.645671', '30.503885', 'FPS_65d599a904a', '1'),
('Barnala', 'achd', '105400660003', 'Motarable', '26.76317237', '75.6480254', '30.484784', 'FPS_65d599a9055', '1'),
('Barnala', 'achd', '105400660004', 'Motarable', '38.13032623', '75.540993', '30.3685732', 'FPS_65d599a9061', '1'),
('Pathankot', 'achd', '164700400001', 'Motarable', '0.719440118', '75.690493', '32.383088', 'FPS_65d599a906a', '1'),
('Pathankot', 'achd', '164700400012', 'Motarable', '0.191850698', '75.696729', '32.382791', 'FPS_65d599a9073', '1'),
('Pathankot', 'achd', '164700600288', 'Motarable', '23.07004643', '75.64757', '32.27871', 'FPS_65d599a907e', '1'),
('Fazilka', 'achd', '164800400103', 'Motarable', '36.35570727', '73.94737', '30.38604', 'FPS_65d599a9087', '1'),
('Malerkotla', 'achd', '178100110071', 'Motarable', '45.08491403', '75.863632', '30.63047', 'FPS_65d599a9091', '1'),
('Malerkotla', 'achd', '178100110072', 'Motarable', '38.3701396', '75.840179', '30.66139', 'FPS_65d599a909f', '1'),
('Jalandhar', 'achd', '103700100001', 'Motarable', '36.93125937', '75.7320938', '31.3729002', 'FPS_65d599a90a7', '1'),
('Sbsnagar', 'achd', '103900100001', 'Motarable', '24.41300132', '75.906126', '31.1801118', 'FPS_65d599a90b0', '1'),
('Sbsnagar', 'achd', '103900100002', 'Motarable', '22.73430771', '75.9399325', '31.1711445', 'FPS_65d599a90b9', '1'),
('Fatehgarhsahib', 'achd', '104000100001', 'Motarable', '25.9478069', '76.1529235', '30.5580174', 'FPS_65d599a90c2', '1'),
('Fatehgarhsahib', 'achd', '104000100002', 'Motarable', '24.2691133', '76.1800668', '30.554606', 'FPS_65d599a90cb', '1'),
('Moga', 'achd', '104200100001', 'Motarable', '52.99875532', '75.00705', '30.5922538', 'FPS_65d599a90d4', '1'),
('Moga', 'achd', '104200100002', 'Motarable', '38.41810227', '75.0111266', '30.5106007', 'FPS_65d599a90e0', '1'),
('Ferozepur', 'achd', '104300100002', 'Motarable', '48.53822659', '74.4982767', '30.9426969', 'FPS_65d599a90ea', '1'),
('Ferozepur', 'achd', '104300100003', 'Motarable', '15.68379456', '74.54432', '30.9606', 'FPS_65d599a90f3', '1'),
('Bathinda', 'achd', '104600100002', 'Motarable', '10.02419897', '74.9467538', '30.2117102', 'FPS_65d599a90fb', '1'),
('Bathinda', 'achd', '104600100003', 'Motarable', '29.97667156', '74.9306622', '30.1902925', 'FPS_65d599a9104', '1'),
('Bathinda', 'achd', '104600100004', 'Motarable', '38.753841', '74.9423529', '30.1891729', 'FPS_65d599a910c', '1');

-- --------------------------------------------------------

--
-- Table structure for table `login`
--

CREATE TABLE `login` (
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `uid` varchar(100) NOT NULL,
  `verified` varchar(10) NOT NULL DEFAULT '0',
  `role` varchar(255) NOT NULL DEFAULT 'admin',
  `token` varchar(255) NOT NULL,
  `lastlogin` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `login`
--

INSERT INTO `login` (`username`, `password`, `uid`, `verified`, `role`, `token`, `lastlogin`) VALUES
('admin@pds', 'admin', 'aqswdecf45', '1', 'admin', 'c4341994d86a8ee34a6e7d3f05735b01', '2024-02-21 14:52:09'),
('amritsar@pds', '11', '658473c823921', '1', 'amritsar', 'ab229e9a509d77108832160247505359', '2024-02-20 22:48:51'),
('PunjabUser', 'PunjabUser@123', 'ads46d', '1', 'admin', '', ''),
('bathinda@pds', '123456', '658556a9d53b1', '1', 'bathinda', '', ''),
('test@pds', '123', '65ccc9c29537f', '1', 'kapurthala', '', '');

-- --------------------------------------------------------

--
-- Table structure for table `optimiseddata_vtqbekb2asz4qi`
--

CREATE TABLE `optimiseddata_vtqbekb2asz4qi` (
  `scenario` varchar(150) NOT NULL,
  `from` varchar(150) NOT NULL,
  `from_state` varchar(150) NOT NULL,
  `from_id` varchar(150) NOT NULL,
  `from_name` varchar(150) NOT NULL,
  `from_district` varchar(150) NOT NULL,
  `from_lat` varchar(150) NOT NULL,
  `from_long` varchar(150) NOT NULL,
  `to` varchar(150) NOT NULL,
  `to_state` varchar(150) NOT NULL,
  `to_id` varchar(150) NOT NULL,
  `to_name` varchar(150) NOT NULL,
  `to_district` varchar(150) NOT NULL,
  `to_lat` varchar(150) NOT NULL,
  `to_long` varchar(150) NOT NULL,
  `commodity` varchar(150) NOT NULL,
  `quantity` varchar(150) NOT NULL,
  `distance` varchar(150) NOT NULL,
  `approve` varchar(100) DEFAULT NULL,
  `new_id` varchar(100) DEFAULT NULL,
  `new_id_admin` varchar(100) DEFAULT NULL,
  `old_id` varchar(100) DEFAULT NULL,
  `new_name` varchar(255) DEFAULT NULL,
  `reviewed` varchar(10) DEFAULT NULL,
  `reason` varchar(255) DEFAULT NULL,
  `new_distance` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `optimiseddata_vtqbekb2asz4qi`
--

INSERT INTO `optimiseddata_vtqbekb2asz4qi` (`scenario`, `from`, `from_state`, `from_id`, `from_name`, `from_district`, `from_lat`, `from_long`, `to`, `to_state`, `to_id`, `to_name`, `to_district`, `to_lat`, `to_long`, `commodity`, `quantity`, `distance`, `approve`, `new_id`, `new_id_admin`, `old_id`, `new_name`, `reviewed`, `reason`, `new_distance`) VALUES
('Optimized', 'Depot', 'Punjab', '1728', 'abc', 'Pathankot', '32.2565693', '75.5634061', 'FPS', 'Punjab', '164700400001', 'achd', 'Pathankot', '32.383088', '75.690493', 'Wheat', '0.71944012', '2', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
('Optimized', 'Depot', 'Punjab', '1728', 'abc', 'Pathankot', '32.2565693', '75.5634061', 'FPS', 'Punjab', '164700400012', 'achd', 'Pathankot', '32.382791', '75.696729', 'Wheat', '0.1918507', '2', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
('Optimized', 'Depot', 'Punjab', '1728', 'abc', 'Pathankot', '32.2565693', '75.5634061', 'FPS', 'Punjab', '164700600288', 'achd', 'Pathankot', '32.27871', '75.64757', 'Wheat', '23.070046', '2', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
('Optimized', 'Depot', 'Punjab', '1874', 'abc', 'Barnala', '30.37045', '75.54527', 'FPS', 'Punjab', '105400660004', 'achd', 'Barnala', '30.3685732', '75.540993', 'Wheat', '38.130326', '2', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
('Optimized', 'Depot', 'Punjab', '1994', 'abc', 'Amritsar', '31.8147', '74.76959', 'FPS', 'Punjab', '104900100029', 'achd', 'Amritsar', '31.8550855', '74.7617', 'Wheat', '1.1990669', '2', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
('Optimized', 'Depot', 'Punjab', '2024', 'abc', 'Fatehgarhsahib', '30.602018', '76.230886', 'FPS', 'Punjab', '104000100001', 'achd', 'Fatehgarhsahib', '30.5580174', '76.1529235', 'Wheat', '25.947807', '2', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
('Optimized', 'Depot', 'Punjab', '2024', 'abc', 'Fatehgarhsahib', '30.602018', '76.230886', 'FPS', 'Punjab', '104000100002', 'achd', 'Fatehgarhsahib', '30.554606', '76.1800668', 'Wheat', '24.269113', '2', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
('Optimized', 'Depot', 'Punjab', '2042', 'abc', 'Amritsar', '31.56566', '74.88854', 'FPS', 'Punjab', '104900400001', 'achd', 'Amritsar', '31.630867', '74.809569', 'Wheat', '0.47962675', '5', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
('Optimized', 'Depot', 'Punjab', '2042', 'abc', 'Amritsar', '31.56566', '74.88854', 'FPS', 'Punjab', '104900600009', 'achd', 'Amritsar', '31.6640351', '74.8529521', 'Wheat', '64.03017', '5', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
('Optimized', 'Depot', 'Punjab', '2042', 'abc', 'Amritsar', '31.56566', '74.88854', 'FPS', 'Punjab', '105000111623', 'achd', 'Tarntaran', '31.35369', '74.62712', 'Wheat', '1.2949922', '5', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
('Optimized', 'Depot', 'Punjab', '2061', 'abc', 'Gurdaspur', '32.05234', '75.43485', 'FPS', 'Punjab', '103500300077', 'achd1', 'Gurdaspur', '32.01964', '75.0894', 'Wheat', '1.1031415', '2', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
('Optimized', 'Depot', 'Punjab', '2061', 'abc', 'Gurdaspur', '32.05234', '75.43485', 'FPS', 'Punjab', '103500500124', 'achd2', 'Gurdaspur', '31.9164', '75.3264', 'Wheat', '26.571322', '2', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
('Optimized', 'Depot', 'Punjab', '2174', 'abc', 'Faridkot', '30.673873', '74.7814424', 'FPS', 'Punjab', '104200100001', 'achd', 'Moga', '30.5922538', '75.00705', 'Wheat', '52.998755', '2', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
('Optimized', 'Depot', 'Punjab', '2256', 'abc', 'Rupnagar', '30.8927', '76.42046', 'FPS', 'Punjab', '105100880014', 'achd', 'Rupnagar', '30.96257', '76.538992', 'Wheat', '43.454183', '2', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
('Optimized', 'Depot', 'Punjab', '4875', 'abc', 'Jalandhar', '31.40847', '75.6861', 'FPS', 'Punjab', '103700100001', 'achd', 'Jalandhar', '31.3729002', '75.7320938', 'Wheat', '36.931259', '2', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
('Optimized', 'Depot', 'Punjab', '5487', 'abc', 'Gurdaspur', '32.13353', '75.45755', 'FPS', 'Punjab', '103500700168', 'achd3', 'Gurdaspur', '32.14334', '75.53278', 'Wheat', '16.595085', '2', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
('Optimized', 'Depot', 'Punjab', '5525', 'abc', 'Jalandhar', '31.1003', '75.898', 'FPS', 'Punjab', '103900100001', 'achd', 'Sbsnagar', '31.1801118', '75.906126', 'Wheat', '24.413001', '2', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
('Optimized', 'Depot', 'Punjab', '5525', 'abc', 'Jalandhar', '31.1003', '75.898', 'FPS', 'Punjab', '103900100002', 'achd', 'Sbsnagar', '31.1711445', '75.9399325', 'Wheat', '22.734308', '2', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
('Optimized', 'Depot', 'Punjab', '5664', 'abc', 'Sasnagar', '30.4692615', '76.7912224', 'FPS', 'Punjab', '105200200005', 'achd', 'Sasnagar', '30.36825993', '76.91577438', 'Wheat', '77.65157', '2', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
('Optimized', 'Depot', 'Punjab', '5664', 'abc', 'Sasnagar', '30.4692615', '76.7912224', 'FPS', 'Punjab', '105200200006', 'achd', 'Sasnagar', '30.3934594', '76.93292074', 'Wheat', '56.931695', '2', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
('Optimized', 'Depot', 'Punjab', '7586', 'abc', 'Bathinda', '30.16206', '74.979929', 'FPS', 'Punjab', '104600100002', 'achd', 'Bathinda', '30.2117102', '74.9467538', 'Wheat', '10.024199', '2', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
('Optimized', 'Depot', 'Punjab', '7586', 'abc', 'Bathinda', '30.16206', '74.979929', 'FPS', 'Punjab', '104600100003', 'achd', 'Bathinda', '30.1902925', '74.9306622', 'Wheat', '29.976672', '2', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
('Optimized', 'Depot', 'Punjab', '7586', 'abc', 'Bathinda', '30.16206', '74.979929', 'FPS', 'Punjab', '104600100004', 'achd', 'Bathinda', '30.1891729', '74.9423529', 'Wheat', '38.753841', '2', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
('Optimized', 'Depot', 'Punjab', '7619', 'abc', 'Malerkotla', '30.557356', '75.69451', 'FPS', 'Punjab', '105400660002', 'achd', 'Barnala', '30.503885', '75.645671', 'Wheat', '67.531446', '2', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
('Optimized', 'Depot', 'Punjab', '7619', 'abc', 'Malerkotla', '30.557356', '75.69451', 'FPS', 'Punjab', '105400660003', 'achd', 'Barnala', '30.484784', '75.6480254', 'Wheat', '26.763172', '2', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
('Optimized', 'Depot', 'Punjab', '7674', 'abc', 'Bathinda', '30.33901', '74.906913', 'FPS', 'Punjab', '104200100002', 'achd', 'Moga', '30.5106007', '75.0111266', 'Wheat', '38.418102', '2', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
('Optimized', 'Depot', 'Punjab', '7682', 'abc', 'Sangrur', '30.253988', '76.027239', 'FPS', 'Punjab', '105300344416', 'achd', 'Sangrur', '30.292187', '75.965421', 'Wheat', '24.269113', '2', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
('Optimized', 'Depot', 'Punjab', '7682', 'abc', 'Sangrur', '30.253988', '76.027239', 'FPS', 'Punjab', '105300344417', 'achd', 'Sangrur', '30.292187', '75.965421', 'Wheat', '27.338724', '2', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
('Optimized', 'Depot', 'Punjab', '7732', 'abc', 'Ferozepur', '30.95982', '74.5877', 'FPS', 'Punjab', '104300100002', 'achd', 'Ferozepur', '30.9426969', '74.4982767', 'Wheat', '48.538227', '2', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
('Optimized', 'Depot', 'Punjab', '7732', 'abc', 'Ferozepur', '30.95982', '74.5877', 'FPS', 'Punjab', '104300100003', 'achd', 'Ferozepur', '30.9606', '74.54432', 'Wheat', '15.683795', '2', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
('Optimized', 'Depot', 'Punjab', '7750', 'abc', 'Ludhiana', '30.6169263', '75.9500728', 'FPS', 'Punjab', '178100110071', 'achd', 'Malerkotla', '30.63047', '75.863632', 'Wheat', '45.084914', '2', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
('Optimized', 'Depot', 'Punjab', '7750', 'abc', 'Ludhiana', '30.6169263', '75.9500728', 'FPS', 'Punjab', '178100110072', 'achd', 'Malerkotla', '30.66139', '75.840179', 'Wheat', '38.37014', '2', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
('Optimized', 'Depot', 'Punjab', '7752', 'abc', 'Fazilka', '30.4503168', '74.0426058', 'FPS', 'Punjab', '164800400103', 'achd', 'Fazilka', '30.38604', '73.94737', 'Wheat', '36.355707', '2', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
('Optimized', 'Depot', 'Punjab', '7760', 'abc', 'Sangrur', '30.247238', '76.043958', 'FPS', 'Punjab', '105300300027', 'achd', 'Sangrur', '30.149695', '76.002432', 'Wheat', '25.372255', '2', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
('Optimized', 'Depot', 'Punjab', '7904', 'abc', 'Tarntaran', '31.3454', '75.0252', 'FPS', 'Punjab', '105000200006', 'achd', 'Tarntaran', '31.31129', '74.99141', 'Wheat', '0.43166407', '2', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
('Optimized', 'Depot', 'Punjab', '7904', 'abc', 'Tarntaran', '31.3454', '75.0252', 'FPS', 'Punjab', '105000220008', 'achd', 'Tarntaran', '31.28307', '75.0226', 'Wheat', '28.489829', '2', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `optimised_table`
--

CREATE TABLE `optimised_table` (
  `id` varchar(255) NOT NULL,
  `month` varchar(255) NOT NULL,
  `year` varchar(255) NOT NULL,
  `applicable` varchar(255) NOT NULL,
  `data` varchar(255) NOT NULL,
  `last_updated` varchar(255) NOT NULL,
  `rolled_out` varchar(255) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `optimised_table`
--

INSERT INTO `optimised_table` (`id`, `month`, `year`, `applicable`, `data`, `last_updated`, `rolled_out`) VALUES
('vtqBEKb2ASz4qi', 'feb', '2024', 'feb', '2277.65148333', '2024-02-21 14:53:29', '1');

-- --------------------------------------------------------

--
-- Table structure for table `timer`
--

CREATE TABLE `timer` (
  `deadline_date` varchar(255) NOT NULL,
  `deadline_time` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `timer`
--

INSERT INTO `timer` (`deadline_date`, `deadline_time`) VALUES
('2024-02-23', '01:00');

-- --------------------------------------------------------

--
-- Table structure for table `warehouse`
--

CREATE TABLE `warehouse` (
  `district` varchar(100) NOT NULL,
  `name` varchar(100) NOT NULL,
  `id` varchar(100) NOT NULL,
  `warehousetype` varchar(100) NOT NULL,
  `type` varchar(100) NOT NULL,
  `latitude` varchar(100) NOT NULL,
  `longitude` varchar(100) NOT NULL,
  `storage` varchar(100) NOT NULL,
  `uniqueid` varchar(100) NOT NULL,
  `active` varchar(10) NOT NULL DEFAULT '1'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `warehouse`
--

INSERT INTO `warehouse` (`district`, `name`, `id`, `warehousetype`, `type`, `latitude`, `longitude`, `storage`, `uniqueid`, `active`) VALUES
('Amritsar', 'abc', '1994', 'SWC', 'Motarable', '31.8147', '74.76959', '1000', 'WH_65d58c6c4fbe', '1'),
('Amritsar', 'abc', '2042', 'SWC', 'Motarable', '31.56566', '74.88854', '1000', 'WH_65d58c6c5181', '1'),
('Tarntaran', 'abc', '7904', 'SWC', 'Motarable', '31.3454', '75.0252', '1000', 'WH_65d58c6c5283', '1'),
('Barnala', 'abc', '7742', 'SWC', 'Motarable', '30.37071', '75.54598', '1000', 'WH_65d58c6c54c8', '1'),
('Barnala', 'abc', '1874', 'SWC', 'Motarable', '30.37045', '75.54527', '1000', 'WH_65d58c6c562c', '1'),
('Barnala', 'abc', '7854', 'SWC', 'Motarable', '30.3029475', '75.5786355', '1000', 'WH_65d58c6c576f', '1'),
('Bathinda', 'abc', '7586', 'SWC', 'Motarable', '30.16206', '74.979929', '1000', 'WH_65d58c6c585e', '1'),
('Bathinda', 'abc', '1838', 'SWC', 'Motarable', '30.30961', '74.9337215', '1000', 'WH_65d58c6c5952', '1'),
('Bathinda', 'abc', '7616', 'SWC', 'Motarable', '30.3096071', '74.9337215', '1000', 'WH_65d58c6c5a46', '1'),
('Bathinda', 'abc', '7674', 'SWC', 'Motarable', '30.33901', '74.906913', '1000', 'WH_65d58c6c5b32', '1'),
('Faridkot', 'abc', '2174', 'SWC', 'Motarable', '30.673873', '74.7814424', '1000', 'WH_65d58c6c5c17', '1'),
('Faridkot', 'abc', '2252', 'SWC', 'Motarable', '30.70141', '74.61488', '1000', 'WH_65d58c6c5d24', '1'),
('Fatehgarhsahib', 'abc', '2024', 'SWC', 'Motarable', '30.602018', '76.230886', '1000', 'WH_65d58c6c5e23', '1'),
('Fazilka', 'abc', '7752', 'SWC', 'Motarable', '30.4503168', '74.0426058', '1000', 'WH_65d58c6c5f1f', '1'),
('Fazilka', 'abc', '7649', 'SWC', 'Motarable', '30.5625533', '74.2291467', '1000', 'WH_65d58c6c601a', '1'),
('Ferozepur', 'abc', '6948', 'SWC', 'Motarable', '30.960001', '74.59032', '1000', 'WH_65d58c6c610c', '1'),
('Ferozepur', 'abc', '7732', 'SWC', 'Motarable', '30.95982', '74.5877', '1000', 'WH_65d58c6c61fc', '1'),
('Gurdaspur', 'abc', '2061', 'SWC', 'Motarable', '32.05234', '75.43485', '1000', 'WH_65d58c6c62ec', '1'),
('Gurdaspur', 'abc', '5487', 'SWC', 'Motarable', '32.13353', '75.45755', '1000', 'WH_65d58c6c63e7', '1'),
('Hoshiarpur', 'abc', '1871', 'SWC', 'Motarable', '31.222113', '76.135585', '1000', 'WH_65d58c6c64c5', '1'),
('Hoshiarpur', 'abc', '1873', 'SWC', 'Motarable', '31.222113', '76.135585', '1000', 'WH_65d58c6c655b', '1'),
('Hoshiarpur', 'abc', '7684', 'SWC', 'Motarable', '31.626213', '75.641011', '1000', 'WH_65d58c6c65f4', '1'),
('Hoshiarpur', 'abc', '2046', 'SWC', 'Motarable', '31.93623', '75.61772', '1000', 'WH_65d58c6c66a9', '1'),
('Jalandhar', 'abc', '4875', 'SWC', 'Motarable', '31.40847', '75.6861', '1000', 'WH_65d58c6c6759', '1'),
('Jalandhar', 'abc', '5525', 'SWC', 'Motarable', '31.1003', '75.898', '1000', 'WH_65d58c6c6800', '1'),
('Kapurthala', 'abc', '2040', 'SWC', 'Motarable', '31.35305', '75.38815', '1000', 'WH_65d58c6c68ac', '1'),
('Kapurthala', 'abc', '7843', 'SWC', 'Motarable', '31.233041', '75.759592', '1000', 'WH_65d58c6c6952', '1'),
('Ludhiana', 'abc', '5586', 'SWC', 'Motarable', '30.8205074', '76.2154563', '1000', 'WH_65d58c6c69ee', '1'),
('Ludhiana', 'abc', '7750', 'SWC', 'Motarable', '30.6169263', '75.9500728', '1000', 'WH_65d58c6c6a90', '1'),
('Ludhiana', 'abc', '7518', 'SWC', 'Motarable', '30.6168185', '75.950269', '1000', 'WH_65d58c6c6b5d', '1'),
('Ludhiana', 'abc', '2108', 'SWC', 'Motarable', '30.7096', '76.04919', '1000', 'WH_65d58c6c6bea', '1'),
('Malerkotla', 'abc', '2254', 'SWC', 'Motarable', '30.555842', '75.704871', '1000', 'WH_65d58c6c6c79', '1'),
('Malerkotla', 'abc', '7619', 'SWC', 'Motarable', '30.557356', '75.69451', '1000', 'WH_65d58c6c6d1c', '1'),
('Malerkotla', 'abc', '7242', 'SWC', 'Motarable', '30.5407', '75.9093', '1000', 'WH_65d58c6c6dbc', '1'),
('Mansa', 'abc', '7626', 'SWC', 'Motarable', '29.798461', '75.338515', '1000', 'WH_65d58c6c6e59', '1'),
('Mansa', 'abc', '1813', 'SWC', 'Motarable', '29.671357', '75.244628', '1000', 'WH_65d58c6c6f0b', '1'),
('Mansa', 'abc', '1975', 'SWC', 'Motarable', '29.6658854', '75.2551168', '1000', 'WH_65d58c6c6fa1', '1'),
('Moga', 'abc', '4401', 'SWC', 'Motarable', '30.9332698', '75.1506411', '1000', 'WH_65d58c6c703f', '1'),
('Moga', 'abc', '7157', 'SWC', 'Motarable', '30.598269', '75.26439', '1000', 'WH_65d58c6c70d8', '1'),
('Pathankot', 'abc', '1795', 'SWC', 'Motarable', '32.2500863', '75.5242124', '1000', 'WH_65d58c6c7176', '1'),
('Pathankot', 'abc', '1728', 'SWC', 'Motarable', '32.2565693', '75.5634061', '1000', 'WH_65d58c6c7213', '1'),
('Patiala', 'abc', '6678', 'SWC', 'Motarable', '30.128709', '76.189141', '1000', 'WH_65d58c6c72bb', '1'),
('Patiala', 'abc', '7884', 'SWC', 'Motarable', '30.167827', '76.217977', '1000', 'WH_65d58c6c7353', '1'),
('Rupnagar', 'abc', '2256', 'SWC', 'Motarable', '30.8927', '76.42046', '1000', 'WH_65d58c6c73ea', '1'),
('Rupnagar', 'abc', '1771', 'SWC', 'Motarable', '30.81823', '76.55627', '1000', 'WH_65d58c6c7482', '1'),
('Sasnagar', 'abc', '2015', 'SWC', 'Motarable', '30.4911655', '76.8049029', '1000', 'WH_65d58c6c7519', '1'),
('Sasnagar', 'abc', '5664', 'SWC', 'Motarable', '30.4692615', '76.7912224', '1000', 'WH_65d58c6c75b2', '1'),
('Sangrur', 'abc', '6929', 'SWC', 'Motarable', '30.286259', '76.078054', '1000', 'WH_65d58c6c7653', '1'),
('Sangrur', 'abc', '7682', 'SWC', 'Motarable', '30.253988', '76.027239', '1000', 'WH_65d58c6c76f4', '1'),
('Sangrur', 'abc', '7760', 'SWC', 'Motarable', '30.247238', '76.043958', '1000', 'WH_65d58c6c7791', '1'),
('Sbsnagar', 'abc', '2083', 'SWC', 'Motarable', '31.10798', '76.11705', '1000', 'WH_65d58c6c7824', '1'),
('Muktsar', 'abc', '1696', 'SWC', 'Motarable', '30.4646866', '74.5153838', '1000', 'WH_65d58c6c78b6', '1'),
('Muktsar', 'abc', '1911', 'SWC', 'Motarable', '30.20785348', '74.50002675', '1000', 'WH_65d58c6c7947', '1');

-- --------------------------------------------------------

--
-- Table structure for table `warehouse_vtqbekb2asz4qi`
--

CREATE TABLE `warehouse_vtqbekb2asz4qi` (
  `district` varchar(100) NOT NULL,
  `name` varchar(100) NOT NULL,
  `id` varchar(100) NOT NULL,
  `warehousetype` varchar(100) NOT NULL,
  `type` varchar(100) NOT NULL,
  `latitude` varchar(100) NOT NULL,
  `longitude` varchar(100) NOT NULL,
  `storage` varchar(100) NOT NULL,
  `uniqueid` varchar(100) NOT NULL,
  `active` varchar(10) NOT NULL DEFAULT '1'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `warehouse_vtqbekb2asz4qi`
--

INSERT INTO `warehouse_vtqbekb2asz4qi` (`district`, `name`, `id`, `warehousetype`, `type`, `latitude`, `longitude`, `storage`, `uniqueid`, `active`) VALUES
('Amritsar', 'abc', '1994', 'SWC', 'Motarable', '31.8147', '74.76959', '1000', 'WH_65d58c6c4fbe', '1'),
('Amritsar', 'abc', '2042', 'SWC', 'Motarable', '31.56566', '74.88854', '1000', 'WH_65d58c6c5181', '1'),
('Tarntaran', 'abc', '7904', 'SWC', 'Motarable', '31.3454', '75.0252', '1000', 'WH_65d58c6c5283', '1'),
('Barnala', 'abc', '7742', 'SWC', 'Motarable', '30.37071', '75.54598', '1000', 'WH_65d58c6c54c8', '1'),
('Barnala', 'abc', '1874', 'SWC', 'Motarable', '30.37045', '75.54527', '1000', 'WH_65d58c6c562c', '1'),
('Barnala', 'abc', '7854', 'SWC', 'Motarable', '30.3029475', '75.5786355', '1000', 'WH_65d58c6c576f', '1'),
('Bathinda', 'abc', '7586', 'SWC', 'Motarable', '30.16206', '74.979929', '1000', 'WH_65d58c6c585e', '1'),
('Bathinda', 'abc', '1838', 'SWC', 'Motarable', '30.30961', '74.9337215', '1000', 'WH_65d58c6c5952', '1'),
('Bathinda', 'abc', '7616', 'SWC', 'Motarable', '30.3096071', '74.9337215', '1000', 'WH_65d58c6c5a46', '1'),
('Bathinda', 'abc', '7674', 'SWC', 'Motarable', '30.33901', '74.906913', '1000', 'WH_65d58c6c5b32', '1'),
('Faridkot', 'abc', '2174', 'SWC', 'Motarable', '30.673873', '74.7814424', '1000', 'WH_65d58c6c5c17', '1'),
('Faridkot', 'abc', '2252', 'SWC', 'Motarable', '30.70141', '74.61488', '1000', 'WH_65d58c6c5d24', '1'),
('Fatehgarhsahib', 'abc', '2024', 'SWC', 'Motarable', '30.602018', '76.230886', '1000', 'WH_65d58c6c5e23', '1'),
('Fazilka', 'abc', '7752', 'SWC', 'Motarable', '30.4503168', '74.0426058', '1000', 'WH_65d58c6c5f1f', '1'),
('Fazilka', 'abc', '7649', 'SWC', 'Motarable', '30.5625533', '74.2291467', '1000', 'WH_65d58c6c601a', '1'),
('Ferozepur', 'abc', '6948', 'SWC', 'Motarable', '30.960001', '74.59032', '1000', 'WH_65d58c6c610c', '1'),
('Ferozepur', 'abc', '7732', 'SWC', 'Motarable', '30.95982', '74.5877', '1000', 'WH_65d58c6c61fc', '1'),
('Gurdaspur', 'abc', '2061', 'SWC', 'Motarable', '32.05234', '75.43485', '1000', 'WH_65d58c6c62ec', '1'),
('Gurdaspur', 'abc', '5487', 'SWC', 'Motarable', '32.13353', '75.45755', '1000', 'WH_65d58c6c63e7', '1'),
('Hoshiarpur', 'abc', '1871', 'SWC', 'Motarable', '31.222113', '76.135585', '1000', 'WH_65d58c6c64c5', '1'),
('Hoshiarpur', 'abc', '1873', 'SWC', 'Motarable', '31.222113', '76.135585', '1000', 'WH_65d58c6c655b', '1'),
('Hoshiarpur', 'abc', '7684', 'SWC', 'Motarable', '31.626213', '75.641011', '1000', 'WH_65d58c6c65f4', '1'),
('Hoshiarpur', 'abc', '2046', 'SWC', 'Motarable', '31.93623', '75.61772', '1000', 'WH_65d58c6c66a9', '1'),
('Jalandhar', 'abc', '4875', 'SWC', 'Motarable', '31.40847', '75.6861', '1000', 'WH_65d58c6c6759', '1'),
('Jalandhar', 'abc', '5525', 'SWC', 'Motarable', '31.1003', '75.898', '1000', 'WH_65d58c6c6800', '1'),
('Kapurthala', 'abc', '2040', 'SWC', 'Motarable', '31.35305', '75.38815', '1000', 'WH_65d58c6c68ac', '1'),
('Kapurthala', 'abc', '7843', 'SWC', 'Motarable', '31.233041', '75.759592', '1000', 'WH_65d58c6c6952', '1'),
('Ludhiana', 'abc', '5586', 'SWC', 'Motarable', '30.8205074', '76.2154563', '1000', 'WH_65d58c6c69ee', '1'),
('Ludhiana', 'abc', '7750', 'SWC', 'Motarable', '30.6169263', '75.9500728', '1000', 'WH_65d58c6c6a90', '1'),
('Ludhiana', 'abc', '7518', 'SWC', 'Motarable', '30.6168185', '75.950269', '1000', 'WH_65d58c6c6b5d', '1'),
('Ludhiana', 'abc', '2108', 'SWC', 'Motarable', '30.7096', '76.04919', '1000', 'WH_65d58c6c6bea', '1'),
('Malerkotla', 'abc', '2254', 'SWC', 'Motarable', '30.555842', '75.704871', '1000', 'WH_65d58c6c6c79', '1'),
('Malerkotla', 'abc', '7619', 'SWC', 'Motarable', '30.557356', '75.69451', '1000', 'WH_65d58c6c6d1c', '1'),
('Malerkotla', 'abc', '7242', 'SWC', 'Motarable', '30.5407', '75.9093', '1000', 'WH_65d58c6c6dbc', '1'),
('Mansa', 'abc', '7626', 'SWC', 'Motarable', '29.798461', '75.338515', '1000', 'WH_65d58c6c6e59', '1'),
('Mansa', 'abc', '1813', 'SWC', 'Motarable', '29.671357', '75.244628', '1000', 'WH_65d58c6c6f0b', '1'),
('Mansa', 'abc', '1975', 'SWC', 'Motarable', '29.6658854', '75.2551168', '1000', 'WH_65d58c6c6fa1', '1'),
('Moga', 'abc', '4401', 'SWC', 'Motarable', '30.9332698', '75.1506411', '1000', 'WH_65d58c6c703f', '1'),
('Moga', 'abc', '7157', 'SWC', 'Motarable', '30.598269', '75.26439', '1000', 'WH_65d58c6c70d8', '1'),
('Pathankot', 'abc', '1795', 'SWC', 'Motarable', '32.2500863', '75.5242124', '1000', 'WH_65d58c6c7176', '1'),
('Pathankot', 'abc', '1728', 'SWC', 'Motarable', '32.2565693', '75.5634061', '1000', 'WH_65d58c6c7213', '1'),
('Patiala', 'abc', '6678', 'SWC', 'Motarable', '30.128709', '76.189141', '1000', 'WH_65d58c6c72bb', '1'),
('Patiala', 'abc', '7884', 'SWC', 'Motarable', '30.167827', '76.217977', '1000', 'WH_65d58c6c7353', '1'),
('Rupnagar', 'abc', '2256', 'SWC', 'Motarable', '30.8927', '76.42046', '1000', 'WH_65d58c6c73ea', '1'),
('Rupnagar', 'abc', '1771', 'SWC', 'Motarable', '30.81823', '76.55627', '1000', 'WH_65d58c6c7482', '1'),
('Sasnagar', 'abc', '2015', 'SWC', 'Motarable', '30.4911655', '76.8049029', '1000', 'WH_65d58c6c7519', '1'),
('Sasnagar', 'abc', '5664', 'SWC', 'Motarable', '30.4692615', '76.7912224', '1000', 'WH_65d58c6c75b2', '1'),
('Sangrur', 'abc', '6929', 'SWC', 'Motarable', '30.286259', '76.078054', '1000', 'WH_65d58c6c7653', '1'),
('Sangrur', 'abc', '7682', 'SWC', 'Motarable', '30.253988', '76.027239', '1000', 'WH_65d58c6c76f4', '1'),
('Sangrur', 'abc', '7760', 'SWC', 'Motarable', '30.247238', '76.043958', '1000', 'WH_65d58c6c7791', '1'),
('Sbsnagar', 'abc', '2083', 'SWC', 'Motarable', '31.10798', '76.11705', '1000', 'WH_65d58c6c7824', '1'),
('Muktsar', 'abc', '1696', 'SWC', 'Motarable', '30.4646866', '74.5153838', '1000', 'WH_65d58c6c78b6', '1'),
('Muktsar', 'abc', '1911', 'SWC', 'Motarable', '30.20785348', '74.50002675', '1000', 'WH_65d58c6c7947', '1');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `districts`
--
ALTER TABLE `districts`
  ADD PRIMARY KEY (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;



