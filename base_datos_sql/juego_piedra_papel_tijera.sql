-- phpMyAdmin SQL Dump
-- version 4.7.4
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 12-06-2019 a las 09:17:36
-- Versión del servidor: 10.1.26-MariaDB
-- Versión de PHP: 7.1.9

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `juego_piedra_papel_tijera`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `juegos`
--

CREATE TABLE `juegos` (
  `Codigo` bigint(20) UNSIGNED NOT NULL COMMENT 'Código de la tabla',
  `Jugador1` varchar(70) NOT NULL COMMENT 'Nombre del jugador 1',
  `Jugador2` varchar(70) NOT NULL COMMENT 'Nombre del jugador 2',
  `Resultado` enum('1','2','3','4') NOT NULL DEFAULT '4' COMMENT '1 gana jugador uno, 2 gana jugador dos, 3 empate, 4 error',
  `Fecha_juego` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Fecha del juego'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `juegos`
--

INSERT INTO `juegos` (`Codigo`, `Jugador1`, `Jugador2`, `Resultado`, `Fecha_juego`) VALUES
(1, 'j1', 'j2', '1', '2019-06-10 18:28:28'),
(2, 'j1', 'j2', '1', '2019-06-10 18:47:58'),
(3, 'j2', 'j1', '1', '2019-06-10 18:55:18'),
(4, 'j1', 'j2', '2', '2019-06-10 18:59:10'),
(5, 'j1', 'j2', '1', '2019-06-10 19:21:22'),
(6, 'j2', 'j3', '1', '2019-06-11 03:06:21'),
(7, 'j1', 'j2', '1', '2019-06-11 03:08:23'),
(8, 'j1', 'j2', '2', '2019-06-11 03:09:21'),
(10, 'j1', 'j2', '2', '2019-06-11 03:13:16'),
(11, 'j1', 'j3', '2', '2019-06-11 07:48:28'),
(12, 'j1', 'j2', '1', '2019-06-11 07:53:21'),
(16, 'j1', 'j2', '2', '2019-06-11 18:27:55'),
(23, 'j3', 'j4', '2', '2019-06-12 03:14:26'),
(27, 'j1', 'j5', '2', '2019-06-12 04:59:39'),
(28, 'j1', 'j2', '1', '2019-06-12 05:03:17'),
(30, 'j1', 'j2', '2', '2019-06-12 05:03:34'),
(31, 'j1', 'j2', '2', '2019-06-12 05:40:05'),
(33, 'j1', 'j2', '1', '2019-06-12 05:53:49'),
(47, 'j3', 'j4', '1', '2019-06-12 06:28:30'),
(49, 'j2', 'j4', '2', '2019-06-12 06:36:18'),
(50, 'j2', 'j4', '2', '2019-06-12 06:36:34');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `jugadores`
--

CREATE TABLE `jugadores` (
  `Codigo` bigint(20) UNSIGNED NOT NULL COMMENT 'Codigo de la tabla',
  `Nombre` varchar(70) NOT NULL COMMENT 'Nombre del usuario',
  `Usuario` varchar(70) NOT NULL COMMENT 'Nombre usuario del juego',
  `Contrasena` varchar(70) NOT NULL COMMENT 'Contraseña para el juego',
  `Puntos` int(5) NOT NULL DEFAULT '0' COMMENT 'Puntuación, +10 si gana, +5 si empata, +0 si pierde',
  `Rol` enum('admin','player') NOT NULL COMMENT 'Tipo de rol (player, admin)',
  `Estado` enum('activo','inactivo') NOT NULL DEFAULT 'inactivo' COMMENT 'activo = jugando, inactivo = no jugando'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `jugadores`
--

INSERT INTO `jugadores` (`Codigo`, `Nombre`, `Usuario`, `Contrasena`, `Puntos`, `Rol`, `Estado`) VALUES
(1, 'admin', 'admin', 'd033e22ae348aeb5660fc2140aec35850c4da997', 0, 'admin', 'inactivo'),
(2, 'jugador1', 'j1', '67921242516c48ac712807f98c98ee138e64a471', 195, 'player', 'inactivo'),
(3, 'j2', 'j2', 'bf263578ed340df40117b46a9780568ac070291f', 200, 'player', 'inactivo'),
(4, 'jugador3', 'j3', '5a4e2a663e71c130df00fdef77d09bfdb96785ba', 45, 'player', 'inactivo'),
(5, 'jugador4', 'j4', '952eed7e1f3691320c7f751483f2078b48717178', 45, 'player', 'inactivo'),
(7, 'jugador5', 'j5', '461fb23181eeb203eaee91cfc48f645fd20af91f', 15, 'player', 'inactivo');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `juegos`
--
ALTER TABLE `juegos`
  ADD PRIMARY KEY (`Codigo`),
  ADD UNIQUE KEY `Codigo` (`Codigo`);

--
-- Indices de la tabla `jugadores`
--
ALTER TABLE `jugadores`
  ADD PRIMARY KEY (`Codigo`),
  ADD UNIQUE KEY `Codigo` (`Codigo`),
  ADD UNIQUE KEY `Usuario` (`Usuario`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `juegos`
--
ALTER TABLE `juegos`
  MODIFY `Codigo` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'Código de la tabla', AUTO_INCREMENT=51;

--
-- AUTO_INCREMENT de la tabla `jugadores`
--
ALTER TABLE `jugadores`
  MODIFY `Codigo` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'Codigo de la tabla', AUTO_INCREMENT=8;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
