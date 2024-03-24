-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 17, 2024 at 09:04 AM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `fyp`
--
CREATE DATABASE IF NOT EXISTS `fyp` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `fyp`;

-- --------------------------------------------------------

--
-- Table structure for table `genre`
--

CREATE TABLE `genre` (
  `id` int(11) NOT NULL,
  `type` varchar(45) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `genre`
--

INSERT INTO `genre` (`id`, `type`) VALUES
(1, 'Action'),
(2, 'Adventure'),
(3, 'Fantasy'),
(4, 'Science Fiction'),
(5, 'Mystery'),
(6, 'Romance'),
(7, 'Thriller'),
(8, 'Horror'),
(9, 'Historical Fiction'),
(10, 'Adventure'),
(11, 'Biography'),
(12, 'Autobiography'),
(13, 'Comedy'),
(14, 'Drama'),
(15, 'Crime'),
(16, 'Suspense'),
(17, 'Young Adult'),
(18, 'Children\'s Literature'),
(19, 'Poetry'),
(20, 'Science'),
(21, 'Self-help'),
(22, 'Travel'),
(23, 'Philosophy'),
(24, 'Religion'),
(25, 'Graphic Novel'),
(26, 'Satire'),
(27, 'Anthology');

-- --------------------------------------------------------

--
-- Table structure for table `product`
--

CREATE TABLE `product` (
  `id` int(11) NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `price` decimal(10,2) DEFAULT NULL,
  `author` varchar(255) DEFAULT NULL,
  `rating` varchar(5) DEFAULT NULL,
  `description` text DEFAULT NULL,
  `genre` varchar(255) DEFAULT NULL,
  `image` varchar(255) DEFAULT NULL,
  `datetime` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `product`
--

INSERT INTO `product` (`id`, `name`, `price`, `author`, `rating`, `description`, `genre`, `image`, `datetime`) VALUES
(1, 'Echoes of Eternity', 33.00, 'Aaron Dembski-Bowden', '4.8', 'The walls have fallen. The defenders’ unity is broken. The Inner Palace lies in ruins. The Warmaster’s horde advances through the fire and ash of Terra’s dying breaths, forcing the loyalists back to the Delphic Battlement, the very walls of the Sanctum Imperialis. Angron, Herald of Horus, has achieved immortality through annihilation – now he leads the armies of the damned in a wrathful tide, destroying all before them as the warp begins its poisonous corruption of Terra. For the Emperor’s beleaguered forces, the end has come. The Khan lies on the edge of death. Rogal Dorn is encircled, fighting his own war at Bhab Bastion. Guilliman will not reach Terra in time. Without his brothers, Sanguinius – the Angel of the Ninth Legion – waits on the final battlements, hoping to rally a desperate band of defenders and refugees for one last stand.', 'Action', 'Echoes of Eternity', '2024-03-17 06:08:54'),
(2, 'Thinking, Fast and Slow', 11.90, 'Daniel Kahneman', '4.6', NULL, 'Action', 'Thinking Fast and Slow', '2024-03-17 06:58:41'),
(3, 'The Psychology of Money: Timeless lessons on wealth, greed, and happiness', 0.00, 'Morgan Housel', '4.7', NULL, 'Action', 'The Psychology of Money Timeless lessons on wealth, greed, and happiness', '2024-03-17 06:58:41'),
(4, 'Never Split the Difference: Negotiating as if Your Life Depended on It', 13.40, 'Chris Voss', '4.7', NULL, 'Adventure', 'Never Split the Difference Negotiating as if Your Life Depended on It', '2024-03-17 06:58:41'),
(5, 'Hidden Potential: The Science of Achieving Greater Things', 15.20, 'Adam Grant', '4.7', NULL, 'Adventure', 'Hidden Potential The Science of Achieving Greater Things', '2024-03-17 06:58:41'),
(6, 'Atomic Habits: An Easy & Proven Way to Build Good Habits & Break Bad Ones', 16.20, 'James Clear', '4.8', NULL, 'Adventure', 'Atomic Habits An Easy Proven Way to Build Good Habits Break Bad Ones', '2024-03-17 06:58:41'),
(7, 'The Almanack of Naval Ravikant: A Guide to Wealth and Happiness', 14.98, 'Eric Jorgenson', '4.7', NULL, 'Adventure', 'The Almanack of Naval Ravikant A Guide to Wealth and Happiness', '2024-03-17 06:58:41'),
(8, 'Die With Zero: Getting All You Can from Your Money and Your Life', 18.00, 'Bill Perkins', '4.5', NULL, 'Romance', 'Die With Zero Getting All You Can from Your Money and Your Life', '2024-03-17 06:58:41'),
(9, 'The First 90 Days: Proven Strategies for Getting Up to Speed Faster and Smarter, Updated and Expanded', 25.40, 'Michael D. Watkins', '4.6', NULL, 'Romance', 'The First 90 Days Proven Strategies for Getting Up to Speed Faster and Smarter, Updated and Expanded', '2024-03-17 06:58:41'),
(10, 'The 48 Laws of Power', 23.13, 'Robert Greene', '4.7', NULL, NULL, 'The 48 Laws of Power', '2024-03-17 06:58:41'),
(11, 'The Intelligent Investor', 28.24, 'Benjamin Graham', '4.6', NULL, NULL, 'The Intelligent Investor', '2024-03-17 06:58:41'),
(12, 'The Diary of a CEO: The 33 Laws of Business and Life', 40.13, 'Steven Bartlett', '4.7', NULL, NULL, 'The Diary of a CEO The 33 Laws of Business and Life', '2024-03-17 06:58:41'),
(13, 'Dead in the Water: A True Story of Hijacking, Murder, and a Global Maritime Conspiracy', 30.68, 'Matthew Campbell', '4.6', NULL, NULL, 'Dead in the Water A True Story of Hijacking, Murder, and a Global Maritime Conspiracy', '2024-03-17 06:58:41'),
(14, 'Your Complete Guide to Factor-Based Investing: The Way Smart Money Invests Today', 23.37, 'Andrew L Berkin', '4.5', NULL, NULL, 'Your Complete Guide to Factor-Based Investing The Way Smart Money Invests Today', '2024-03-17 06:58:41'),
(15, 'Unreasonable Hospitality: The Remarkable Power of Giving People More Than They Expect', 17.25, 'Will Guidara', '4.8', NULL, NULL, 'Unreasonable Hospitality The Remarkable Power of Giving People More Than They Expect', '2024-03-17 06:58:41'),
(16, 'Why Women Don’t Talk Money', 27.14, 'Sharon Sim', '4.3', NULL, NULL, 'Why Women Dont Talk Money', '2024-03-17 06:58:41'),
(17, 'The Daily Stoic: 366 Meditations on Wisdom, Perseverance, and the Art of Living', 17.84, 'Ryan Holiday', '4.8', NULL, NULL, 'The Daily Stoic 366 Meditations on Wisdom, Perseverance, and the Art of Living', '2024-03-17 06:58:41'),
(18, 'Mastery', 22.84, 'Robert Greene', '4.7', NULL, NULL, 'Mastery', '2024-03-17 06:58:41'),
(19, 'How to Win Friends and Influence People', 12.85, 'Dale Carnegie', '4.7', NULL, NULL, 'How to Win Friends and Influence People', '2024-03-17 06:58:41'),
(20, 'Hacking Growth: How Today\'s Fastest-Growing Companies Drive Breakout Success', 31.99, 'Sean Ellis', '4.6', NULL, NULL, 'Hacking Growth How Today\'s Fastest-Growing Companies Drive Breakout Success', '2024-03-17 06:58:41'),
(21, '(ISC)2 CISSP Certified Information Systems Security Professional Official Study Guide & Practice Tests Bundle', 82.84, 'Mike Chapple', '4.8', NULL, NULL, 'ISC2 CISSP Certified Information Systems Security Professional Official Study Guide Practice Tests Bundle', '2024-03-17 06:58:41'),
(22, 'The World for Sale: Money, Power, and the Traders Who Barter the Earth\'s Resources', 28.89, 'Chief Energy Correspondent Javier Blas', '4.7', NULL, NULL, 'The World for Sale Money, Power, and the Traders Who Barter the Earth\'s Resources', '2024-03-17 06:58:41'),
(23, 'Million Dollar Weekend: The Surprisingly Simple Way to Launch a 7-Figure Business in 48 Hours', 37.37, 'Noah Kagan', '4.9', NULL, NULL, 'Million Dollar Weekend', '2024-03-17 06:58:41'),
(24, 'The Five Dysfunctions of a Team: A Leadership Fable: A Leadership Fable, 20th Anniversary Edition', 29.62, 'Patrick Lencioni', '4.6', NULL, NULL, 'The Five Dysfunctions of a Team A Leadership Fable A Leadership Fable, 20th Anniversary Edition', '2024-03-17 06:58:41'),
(25, 'Start with Why: How Great Leaders Inspire Everyone to Take Action', 17.94, 'Simon Sinek', '4.6', NULL, NULL, 'Start with Why How Great Leaders Inspire Everyone to Take Action', '2024-03-17 06:58:41'),
(26, 'Can\'t Hurt Me: Master Your Mind and Defy the Odds', 32.41, 'David Goggins', '4.8', NULL, NULL, 'Can\'t Hurt Me Master Your Mind and Defy the Odds', '2024-03-17 06:58:41'),
(27, 'End Times: Elites, Counter-Elites and the Path of Political Disintegration', 21.00, 'Peter Turchin', '4.4', NULL, NULL, 'End Times Elites, Counter-Elites and the Path of Political Disintegration', '2024-03-17 06:58:41'),
(28, 'Mastering Uncertainty: How great founders, entrepreneurs and business leaders thrive in an unpredictable world', 8.85, 'Matt Watkinson', '3.6', NULL, NULL, 'Mastering Uncertainty How great founders, entrepreneurs and business leaders thrive in an unpredictable world', '2024-03-17 06:58:41'),
(29, 'Nudge: The Final Edition', 22.74, 'Richard H. Thaler', '4.6', NULL, NULL, 'Nudge The Final Edition', '2024-03-17 06:58:41'),
(30, 'Flying Blind: The 737 MAX Tragedy and the Fall of Boeing', 22.04, 'Peter Robison', '4.5', NULL, NULL, 'Flying Blind The 737 MAX Tragedy and the Fall of Boeing', '2024-03-17 06:58:41'),
(31, 'Dare to Lead: Brave Work. Tough Conversations. Whole Hearts.', 20.00, 'Bren? Brown', '4.7', NULL, NULL, 'Dare to Lead: Brave Work. Tough Conversations. Whole Hearts.', '2024-03-17 06:58:41'),
(32, 'Iwoz: Computer Geek to Cult Icon', 27.50, 'Steve Wozniak', '4.5', NULL, NULL, 'Iwoz: Computer Geek to Cult Icon', '2024-03-17 06:58:41'),
(33, 'Just for Fun: The Story of an Accidental Revolutionary', 23.63, 'Linus Torvalds', '4.7', NULL, NULL, 'Just for Fun: The Story of an Accidental Revolutionary', '2024-03-17 06:58:41'),
(34, 'Iacocca: An Autobiography', 33.64, 'Lee Iacocca', '4.6', NULL, NULL, 'Iacocca An Autobiography', '2024-03-17 06:58:41'),
(35, 'Same as Ever: A Guide to What Never Changes', 22.87, 'Morgan Housel', '4.5', NULL, NULL, 'Same as Ever: A Guide to What Never Changes', '2024-03-17 06:58:41'),
(36, 'Trading: Technical Analysis Masterclass: Master the financial markets', 16.33, 'Rolf Schlotmann', '4.4', NULL, NULL, 'Trading: Technical Analysis Masterclass: Master the financial markets', '2024-03-17 06:58:41'),
(37, 'Same as Ever: Timeless Lessons on Risk, Opportunity and Living a Good Life', 17.83, 'Morgan Housel', '4.5', NULL, NULL, 'Same as Ever: Timeless Lessons on Risk, Opportunity and Living a Good Life', '2024-03-17 06:58:41'),
(38, 'The Bed of Procrustes: Philosophical and Practical Aphorisms: 4', 34.94, 'Nassim Nicholas Taleb', '4.4', NULL, NULL, 'The Bed of Procrustes: Philosophical and Practical Aphorisms: 4', '2024-03-17 06:58:41'),
(39, '12 Rules for Life: An Antidote to Chaos', 10.90, 'Jordan B. Peterson', '4.7', NULL, NULL, '12 Rules for Life An Antidote to Chaos', '2024-03-17 06:58:41'),
(40, 'Never Split the Difference: Negotiating As If Your Life Depended On It', 15.96, 'Chris Voss', '4.7', NULL, NULL, 'Never Split the Difference: Negotiating As If Your Life Depended On It', '2024-03-17 06:58:41'),
(41, 'The Woke Salaryman Crash Course on Capitalism & Money: Lessons from the World\'s Most Expensive City', 26.30, 'The Woke Salaryman', '4.6', NULL, NULL, 'The Woke Salaryman Crash Course on Capitalism & Money: Lessons from the World\'s Most Expensive City', '2024-03-17 06:58:41'),
(108, 'Echoes of Eternity 2', 89.80, 'Aaron Dembski-Bowden', '4.8', NULL, NULL, 'Echoes of Eternity', '2024-03-17 08:00:56'),
(109, 'Eat Fly Dream', 144.40, 'Daniel Kahneman', '4.5', NULL, NULL, 'Eat Fly Dream', '2024-03-17 08:02:14');

-- --------------------------------------------------------

--
-- Table structure for table `shopping_cart`
--

CREATE TABLE `shopping_cart` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `quantity` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `user_type` enum('user','admin') NOT NULL,
  `email` varchar(100) NOT NULL,
  `full_name` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `username`, `password`, `user_type`, `email`, `full_name`) VALUES
(1, 'wj', '$2y$10$7cAyvKlbAtOoFE6BMP1p0e2JMlord3UG8h7N6fsd5a2Ad86rckunK', 'user', 'weijie@gmail.com', 'Wei Jie'),
(16, 'jr', '$2y$10$pu6IgztxeRt7hi.Bwn19yezjb8EF8fjJyScyhKPXGpzOj0mUc/2XK', 'user', 'jr@gmail.com', 'Jun Ren'),
(17, 'asd', '$2y$10$v4UbhmXo2LGd3FFQlTESoOOEyRn2rMgc76rKDLIRL84w.xXeaIy8a', 'admin', 'asd@asd.com', 'asd');

-- --------------------------------------------------------

--
-- Table structure for table `user_details`
--

CREATE TABLE `user_details` (
  `id` int(11) NOT NULL,
  `username` varchar(255) NOT NULL,
  `age` int(11) DEFAULT NULL,
  `gender` enum('male','female','other') DEFAULT NULL,
  `occupation` varchar(255) DEFAULT NULL,
  `genre` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user_details`
--

INSERT INTO `user_details` (`id`, `username`, `age`, `gender`, `occupation`, `genre`) VALUES
(2, 'jr', 18, 'male', 'doctor', 'Romance'),
(3, 'wj', NULL, NULL, NULL, NULL),
(4, 'asd', 25, 'male', 'doctor', 'Romance');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `genre`
--
ALTER TABLE `genre`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `product`
--
ALTER TABLE `product`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `shopping_cart`
--
ALTER TABLE `shopping_cart`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `product_id` (`product_id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `user_details`
--
ALTER TABLE `user_details`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `genre`
--
ALTER TABLE `genre`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=28;

--
-- AUTO_INCREMENT for table `product`
--
ALTER TABLE `product`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=110;

--
-- AUTO_INCREMENT for table `shopping_cart`
--
ALTER TABLE `shopping_cart`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT for table `user_details`
--
ALTER TABLE `user_details`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `shopping_cart`
--
ALTER TABLE `shopping_cart`
  ADD CONSTRAINT `shopping_cart_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  ADD CONSTRAINT `shopping_cart_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `product` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
